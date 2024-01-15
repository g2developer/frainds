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

from windows import VoiceTextWindow


class VoiceRecognition(QObject):
    language = 'ko'

    voiceTextWin = None
    platform = None

    # 명령 전달 (type:str, data:str)
    sign_model_loaded = pyqtSignal()
    sign_command = pyqtSignal(str, str)
    sign_listen = pyqtSignal(str)
    sign_voice_recgnized = pyqtSignal(str)

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

    ai_chatting = False

    start_on_mic = False
    # model_name = 'large-v3'
    model_name = 'base'

    def __init__(self, mic_start):
        super().__init__()
        self.start_on_mic = mic_start
        self.banned_results = ["", " ", "\n", None]
        self.platform = platform.system()

        self.voiceTextWin = VoiceTextWindow()
        self.voiceTextWin.show()

        self.setup_mic()
        self.setup_recognizer()
        threading.Thread(target=self.setup_speech_model, daemon=True).start()

        # self.voiceTextWin.show()


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

    def setup_speech_model(self):
    # def setup_speech_model(self, model_name='large-v3'):
        # device = ("cuda" if torch.cuda.is_available() else "cpu")
        # if self.platform == "darwin":
        #     if device == "mps":
        #         device = "mps"
        #         device = torch.device(device)

        # model_download_root = './model/whisper'
        # self.speech_model = whisper.load_model(model_name, download_root=model_download_root).to(device)

        # default model setting
        self.speech_model = whisper.load_model(self.model_name)
        print('setup speech model ' + self.model_name)
        self.voiceTextWin.set_text('')
        self.sign_model_loaded.emit()
        if self.start_on_mic:
            self.start()

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
            if not self.speech_model:
                print('아직 모델을 로드중입니다.')
                self.voiceTextWin.set_text('모델을 로드중입니다.')
                continue
            result = self.speech_model.transcribe(audio_data, language=self.language)
            predicted_text = result["text"]

            if predicted_text not in self.banned_results:
                self.result_queue.put_nowait(predicted_text)
                self.voiceTextWin.set_text(predicted_text)



    def listen(self):
        if not self.enabled:
            return

        print('듣고 있어요')
        while self.recording:
            txt = self.result_queue.get()
            print(txt)
            self.sign_listen.emit(txt)

        print('듣기 끝..')


    def start(self):
        if not self.enabled:
            return
        if self.recording:
            return
        print('start recording')
        self.recording = True
        self.audio_queue = queue.Queue()
        self.result_queue: queue.Queue[str] = queue.Queue()

        self.recognizer_stopper = self.recognizer.listen_in_background(self.audio_source, self.__listen_callback)
        self.thread_recorder = threading.Thread(target=self.listen, daemon=True)
        self.thread_recorder.start()
        self.thread_transcribe = threading.Thread(target=self.__transcribe, daemon=True)
        self.thread_transcribe.start()
        # self.listen()
        self.voiceTextWin.show()

    def stop(self):
        if not self.recording:
            return
        self.recording = False
        self.voiceTextWin.hide()
        # self.thread_recorder.join()
        # self.thread_transcribe.join()
        self.recognizer_stopper(True)
        # self.result_queue.join()
        # self.audio_queue.join()
        print('stop recording ', self.thread_recorder.is_alive())


