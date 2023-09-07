import vosk
import sys
import sounddevice as sd
import queue
import json


def listen():
    model = vosk.Model("model")
    samplerate = 16000
    devices = sd.query_devices()
    #print("Select device id: \n", devices)
    q = queue.Queue()
    dev_id = 1

    def callback(indata, frames, time, status):
        q.put(bytes(indata))

    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=dev_id, dtype='int16',
                           channels=1, callback=callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                print(data)
                return data
