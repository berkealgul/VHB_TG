import time
import simpleaudio as sa

class HBSoundGenerator:
    def __init__(self, sound_path, beat_time):
        self.sound_path = sound_path
        self.beat_time = beat_time # times are in secs
        self.wait_time = 0
        self.bpm = 0
        self.loop = True

    def play_loop(self): 
        wave_obj = sa.WaveObject.from_wave_file(self.sound_path)
        
        while self.loop:
            play_obj = wave_obj.play()
            play_obj.wait_done()  # Wait until sound has finished playing
            time.sleep(self.wait_time)
    
    def set_bpm(self, bpm):
        self.bpm = bpm
        self.calculate_wait_time()

    def calculate_wait_time(self):
        self.wait_time = (60/self.bpm) - self.beat_time
        print(self.wait_time)

if __name__ == "__main__":
    sound_path = "resources/heartbeat.wav"
    beat_time = 0.2
    hbg = HBSoundGenerator(sound_path, beat_time)
    hbg.set_bpm(80)
    hbg.play_loop()