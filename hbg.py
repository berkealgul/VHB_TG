import os
import cv2
import numpy as np


class hbg:
    def __init__(self, fps=25, image_dir="/output/", video_name="output"):
        self.fps = fps
        self.video_name = video_name
        self.image_dir = image_dir
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 1
        self.font_thickness = 2
        (self.label_width, self.label_height), self.baseline = cv2.getTextSize("9999", self.font, self.font_scale, self.font_thickness)

    def start(self, initial_beat):
        self.beat = initial_beat
        self.time = 0
        self.n_frames = 0

    def write_frame(self):
        frame = np.zeros((self.label_height + self.baseline, self.label_width, 4), np.uint8)
        cv2.putText(frame, str(self.beat),(0, self.label_height), self.font, self.font_scale, (255, 255, 255), self.font_thickness, cv2.LINE_AA)  

        cv2.imwrite(self.image_dir+str(self.n_frames)+".png", frame)
        self.n_frames = self.n_frames + 1

    # t is time in seconds
    # final beat is desired end beat
    # linear function 
    def linear_change(self, t, final_beat):
        f = t*self.fps
        for i in range(t*self.fps):
            self.beat = self.beat + int((i * (final_beat - self.beat)) / f)
            self.write_frame() 
    
    # x^2 function 
    def rapid_change(self, t, final_beat):
        # not finished
        frames = t*self.fps
        for i in range(t*self.fps):
            self.beat = 0
            self.write_frame() 

    def constant_change(self, t):
        for i in range(t*self.fps):
            self.write_frame() 
    
    def sudden_change(self, new_beat):
        self.beat = new_beat
        self.write_frame()

    def stop(self):
        os.system("ffmpeg -i output/%d.png -vcodec qtrle "+self.video_name+".mov")


# fast debug lines
#cv2.imshow("img", frame)
#cv2.waitKey(100)

def test():
    h = hbg(image_dir="./output/")
    h.start(80)
    h.linear_change(10, 100)
    h.stop()

if __name__ == "__main__":  
    test()