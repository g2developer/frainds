import queue, os, threading
import time
import numpy as np

import sounddevice as sd
import soundfile as sf

# from scipy.io.wavfile import write


class VoiceCommander:
    q = queue.Queue()

    recorder = False
    recording = False
    rec_micro_sec = 1
    is_wait = False

    def __init__(self, sec=3):
        self.rec_micro_sec = sec * 1000

    def complicated_record(self):
        with sd.Stream(callback=self.print_sound):
            sd.sleep(self.rec_micro_sec)

        with sf.SoundFile("./temp_waves/temp.wav", mode='w', samplerate=16000, subtype='PCM_16', channels=1) as file:
            # sd.sleep(self.rec_micro_sec)

            with sd.InputStream(samplerate=16000, dtype='int16', channels=1, callback=self.complicated_save):
                while self.recording:
                    print()
                    file.write(self.q.get())

    def complicated_save(self, indata, frames, time, status):
        self.q.put(indata.copy())

    def print_sound(self, indata, outdata=None, frames=None, time=None, status=None):
        volume_norm = np.linalg.norm(indata) * 5
        print("|" * int(volume_norm))

    def start(self):
        self.recording = True
        self.recorder = threading.Thread(target=self.complicated_record)
        print('start recording')
        self.recorder.start()

    def stop(self):
        self.recording = False
        self.recorder.join()
        print('stop recording')


# sec = 30
# v = VoiceCommander(sec)
# v.start()
# time.sleep(sec)
# v.stop()
