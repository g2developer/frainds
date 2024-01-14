import asyncio
import queue
import sys
import threading
import platform
import time
import numpy as np

import speech_recognition as sr
import torch
import whisper
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication


class VoiceCommander(QObject):
    platform = None

    # 명령 전달 (type:str, data:str)
    sign_command = pyqtSignal(str, str)
    sign_model_loaded = pyqtSignal()

    recognizer = None

    thread_recorder = None
    thread_transcribe = None
    recognizer_stopper = None

    # 상태
    is_wait = False
    recording = False
    enabled = True

    mic_index = 0
    audio_source = None

    energy_threshold = 500
    pause_threshold = 0.8
    dynamic_energy_threshold = True

    # speech model
    speech_model = None

    def __init__(self):
        super().__init__()
        self.banned_results = ["", " ", "\n", None]
        self.platform = platform.system()
        self.audio_queue = queue.Queue()
        self.result_queue: queue.Queue[str] = queue.Queue()

    def setup_recognizer(self):
        self.audio_source = sr.Microphone(sample_rate=16000, device_index=self.mic_index)
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = self.energy_threshold
        self.recognizer.pause_threshold = self.pause_threshold
        self.recognizer.dynamic_energy_threshold = self.dynamic_energy_threshold
        with self.audio_source:
            self.recognizer.adjust_for_ambient_noise(self.audio_source)

    def setup_mic(self):
        print('setup mic')

        # print(sr.Microphone.list_microphone_names())
        self.mic_index = 0

    def setup_speech_model(self, model_name='base'):
    # def setup_speech_model(self, model_name='large-v3'):
        # device = ("cuda" if torch.cuda.is_available() else "cpu")
        # if self.platform == "darwin":
        #     if device == "mps":
        #         device = "mps"
        #         device = torch.device(device)

        # model_download_root = './model/whisper'
        # self.speech_model = whisper.load_model(model_name, download_root=model_download_root).to(device)

        # default model setting
        self.speech_model = whisper.load_model(model_name)
        print('setup speech model ' + model_name)
        self.sign_model_loaded.emit()

    # 말이 한번 끝난 경우 이 함수가 호출됨
    def __listen_callback(self, _, audio: sr.AudioData) -> None:
        print('listen_callback')
        data = audio.get_raw_data()
        self.audio_queue.put_nowait(data)

    def __get_audio_data(self, min_time: float = -1.):
        # print('__get_audio_data 1')
        audio = bytes()
        got_audio = False
        time_start = time.time()
        while not got_audio or time.time() - time_start < min_time:
            while not self.audio_queue.empty():
                audio += self.audio_queue.get()
                got_audio = True

        # print('__get_audio_data 2')
        data = sr.AudioData(audio, 16000, 2)
        data = data.get_raw_data()
        return data

    def __preprocess(self, data):
        return torch.from_numpy(np.frombuffer(data, np.int16).flatten().astype(np.float32) / 32768.0)

    def __transcribe(self):
        print('변환 시작')
        while self.recording:
            audio_data = self.__get_audio_data()
            audio_data = self.__preprocess(audio_data)
            result = self.speech_model.transcribe(audio_data)
            predicted_text = result["text"]

            if predicted_text not in self.banned_results:
                self.result_queue.put_nowait(predicted_text)



    def listen(self):
        if not self.enabled:
            return

        print('듣고 있어요')
        self.recording = True
        while self.recording:
            txt = self.result_queue.get()
            print(txt)
            self.command(txt)

        print('듣기 끝..')


    def start(self):
        if not self.enabled:
            return
        print('start recording')

        self.setup_mic()
        self.setup_recognizer()
        self.setup_speech_model()
        self.recognizer_stopper = self.recognizer.listen_in_background(self.audio_source, self.__listen_callback)
        self.thread_recorder = threading.Thread(target=self.listen, daemon=True)
        self.thread_recorder.start()
        self.thread_transcribe = threading.Thread(target=self.__transcribe, daemon=True)
        self.thread_transcribe.start()
        # self.listen()

    def stop(self):
        self.recording = False
        # self.thread_recorder.join()
        # self.thread_transcribe.join()
        # self.recognizer_stopper(True)
        # self.result_queue.join()
        # self.audio_queue.join()
        print('stop recording ', self.thread_recorder.is_alive())

    def command(self, txt):
        # print(f'커맨드를 찾습니다. |{txt}|')
        if txt.find('종료') > -1 or txt.find('끝내') > -1:
            print('종료 커맨드')
            self.sign_command.emit('exit', '')

        elif txt.find('찾아') > -1 or txt.find('알려줘') > -1 or txt.find('검색') > -1 or txt.find('계속해') > -1:
            print('찾기 커맨드')
            self.sign_command.emit('search', txt)

        # else:
        #     self.sign_command.emit('search', txt)
        #     print('찾기 커맨드')

    def findCommand(self, txt):
        pass
