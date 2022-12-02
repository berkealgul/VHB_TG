import os
import cv2
import numpy as np


class lsg:
    def __init__(self, inner_color, outer_color, lung_dir, fps=25, output_dir="/output", video_name="output"):
        self.fps = fps
        self.video_name = video_name
        self.output_dir = output_dir
        # BGR format
        self.inner_color = inner_color
        self.outer_color = outer_color
        self.split_layers(lung_dir)

    def split_layers(self, lung_dir):
        lung = cv2.imread(lung_dir)

        self.inner_lung = self.extract_color(lung, self.inner_color)
        self.outer_lung = self.extract_color(lung, self.outer_color)
    
        # cv2.imshow("il", self.inner_lung)
        # cv2.imshow("ol", self.outer_lung)
        # cv2.waitKey(1500)

    def extract_color(self, img, color):
        # source image is rgb but seperated layers will be rgba
        mask = np.zeros((img.shape[0], img.shape[1], 4))
        for i in range(3):
            mask[:,:,i] = np.where(img[:,:,i] == color[i], color[i], 0)     
        return mask

    def start(self, initial_air=1.0):
        self.time = 0
        self.air = min(1.0, initial_air) # range is [-1.0 1.0] below 0 represent water level

    def set_air_level(self, new_air):
        self.air = new_air

    def stop(self):
        # ffmpeg assumes output is 25 fps. it is not a problem now but maybe it will need to be changed later
        os.system("ffmpeg -i output/images/%d.png -vcodec qtrle "+self.output_dir+"/"+self.video_name+".mov")

    def start(self, initial_air):
        self.check_dirs()
        self.set_air_level(initial_air)
        self.time = 0
        self.n_frames = 0

    def check_dirs(self):
        try:
            os.makedirs(self.output_dir+"/images_lung") 
        except OSError as error:
            print("output dirs already created")

    def write_frame(self):
        frame = np.zeros((self.label_height + self.baseline, self.label_width, 4), np.uint8)
        cv2.imwrite(self.output_dir+"/images/"+str(self.n_frames)+".png", frame)
        self.n_frames = self.n_frames + 1


class hbtg:
    def __init__(self, fps=25, output_dir="./output", video_name="output"):
        self.fps = fps
        self.video_name = video_name
        self.output_dir = output_dir
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 1
        self.font_thickness = 2
        (self.label_width, self.label_height), self.baseline = cv2.getTextSize("9999", self.font, self.font_scale, self.font_thickness)

    def start(self, initial_beat):
        self.check_dirs()
        self.beat = initial_beat
        self.time = 0
        self.n_frames = 0

    def check_dirs(self):
        try:
            os.makedirs(self.output_dir+"/images") 
        except OSError as error:
            print("output dirs already created")

    def write_frame(self):
        frame = np.zeros((self.label_height + self.baseline, self.label_width, 4), np.uint8)
        cv2.putText(frame, str(self.beat),(0, self.label_height), self.font, self.font_scale, (255, 255, 255), self.font_thickness, cv2.LINE_AA)  
        cv2.imwrite(self.output_dir+"/images/"+str(self.n_frames)+".png", frame)
        self.n_frames = self.n_frames + 1

    # t is time in seconds
    # final beat is desired end beat
    # linear function 
    def linear_change(self, t, final_beat):
        f = t*self.fps
        for i in range(t*self.fps):
            self.beat = self.beat + int((i * (final_beat - self.beat)) / f)
            self.write_frame() 

    def constant_change(self, t):
        for i in range(t*self.fps):
            self.write_frame() 
    
    def sudden_change(self, new_beat):
        self.beat = new_beat
        self.write_frame()

    def stop(self):
        # ffmpeg assumes output is 25 fps. it is not a problem now but maybe it will need to be changed later
        os.system("ffmpeg -i output/images/%d.png -vcodec qtrle "+self.output_dir+"/"+self.video_name+".mov")


# fast debug lines
#cv2.imshow("img", frame)
#cv2.waitKey(100)

def hbtg_test():
    h = hbtg()
    h.start(80)
    h.linear_change(10, 100)
    h.stop()

def lsg_test():
    lsg_ = lsg((255,216,0), (249, 77, 4), "resources/full_lung_wb.png")


if __name__ == "__main__":  
    lsg_test()
