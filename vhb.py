import os
import cv2
import numpy as np
from math import sin, pi


# TODO: add alpha channel to lsg images

class lsg:
    def __init__(self, inner_color, outer_color, lung_dir, fps=25, anim_len=5, breating_size=1.3, output_dir="./output", video_name="output"):    
        self.fps = fps
        self.video_name = video_name
        self.output_dir = output_dir
        self.inner_color = inner_color # BGR format
        self.outer_color = outer_color
        self.anim_len = anim_len # len in secs
        self.breating_size = anim_len # max size of lung and must be >1
        # funcs
        self.split_layers(lung_dir)

    # animates 1 breating cycle
    def animate_breating(self):
        anim_frames = self.anim_len*self.fps
        lung = self.inner_lung + self.outer_lung
        w0, h0 = lung.shape[1], lung.shape[0]
        for i in range(anim_frames):
            # dunno why but w and h increases at different scale
            scale = (self.breating_size-1) * sin(pi*(i/anim_frames)) + 1
            w = int(w0*scale)
            h = int(h0*scale)
            frame = cv2.resize(lung, (w,h), interpolation = cv2.INTER_AREA)
            # cut the surrounding to remain the frame at original size
            bl = int((w-w0)/2)
            br = w - bl
            bu = int((h-h0)/2)
            bd = h - bu
            # god know how but frame remains at 1080x1000
            self.write_frame(frame[bu:bd, bl:br, :])
            # print(frame[bu:bd, bl:br, :].shape)
            # print(w,h)
            # print(sin(pi))

    def split_layers(self, lung_dir):
        lung = cv2.imread(lung_dir)
        self.inner_lung = self.extract_color(lung, self.inner_color)
        self.outer_lung = self.extract_color(lung, self.outer_color)
        # cv2.imshow("il", self.inner_lung)
        # cv2.imshow("ol", self.outer_lung)
        # cv2.waitKey(1500)

    def extract_color(self, img, color):
        # source image is rgb but seperated layers will be rgba
        mask = np.zeros(img.shape)
        for i in range(3):
            mask[:,:,i] = np.where(img[:,:,i] == color[i], color[i], 0)     
        return mask

    def start(self, initial_air=1.0):
        self.check_dirs()
        self.time = 0
        self.air = initial_air
        self.n_frames = 0

    def linear_change(self, t, final_beat):
        f = t*self.fps
        for i in range(t*self.fps):
            self.beat = self.beat + int((i * (final_beat - self.beat)) / f)
            self.write_frame() 

    def constant_change(self, t):
        for i in range(t*self.fps):
            self.write_frame() 

    def set_air_level(self, new_air):
        self.air = new_air

    def check_dirs(self):
        try:
            os.makedirs(self.output_dir+"/images_lung") 
        except OSError as error:
            print("output dirs already created")

    def write_frame(self, frame):
        cv2.imwrite(self.output_dir+"/images_lung/"+str(self.n_frames)+".png", frame)
        self.n_frames = self.n_frames + 1
    
    def write_frame(self):
        # todo: calculate inner lung size and color to represent air/water amounts
        return
        frame = self.inner_lung + self.outer_lung
        cv2.imwrite(self.output_dir+"/images_lung/"+str(self.n_frames)+".png", frame)
        self.n_frames = self.n_frames + 1
    
    def stop(self):
        # ffmpeg assumes output is 25 fps. it is not a problem now but maybe it will need to be changed later
        os.system("ffmpeg -i "+self.output_dir+"/images_lung/%d.png -vcodec qtrle "+self.output_dir+"/"+self.video_name+".mov")



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
    lsg_.start()
    lsg_.animate_breating()
    lsg_.stop()

if __name__ == "__main__":  
    lsg_test()
