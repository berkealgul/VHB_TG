import os
import cv2
import numpy as np
import shutil
from math import sin, pi


# TODO: add alpha channel to lsg images
# NOTE: imshow displays different colors. discovered at init_layers() and must research it

class lsg:
    def __init__(self, inner_color, outer_color, inner_water_color, lung_dir, fps=25, anim_len=5, breating_size=1.3, output_dir="./output", video_name="output"):    
        self.fps = fps
        self.video_name = video_name
        self.output_dir = output_dir
        self.inner_color = inner_color # BGR format
        self.outer_color = outer_color
        self.inner_water_color = inner_water_color
        self.anim_len = anim_len # len in secs
        self.breating_size = breating_size # max size of lung and must be >1
        self.inner_lung = None # in&outer and water in lungs are assinged at init_layers()
        self.outer_lung = None
        self.inner_water_lung = None 
        self.inner_lung_up = -1  # they are upper and lower limit of inner lung
        self.inner_lung_low = -1 # both are calculated at calculate_inner_lung_borders()
        self.air = 0
        self.n_frames = 0
        # funcs
        self.init_layers(lung_dir)
        self.calculate_inner_lung_borders()

    def calculate_inner_lung_borders(self):
        # search for up
        for i in range(self.inner_lung.shape[0]):
            b  = (self.inner_lung[i,:,0] == self.inner_color[0]).any()
            g  = (self.inner_lung[i,:,1] == self.inner_color[1]).any()
            r  = (self.inner_lung[i,:,2] == self.inner_color[2]).any()

            if b and g and r:
                self.inner_lung_up = i
                break
        
        # search for low
        for i in range(self.inner_lung.shape[1]-1, 0, -1):
            b  = (self.inner_lung[i,:,0] == self.inner_color[0]).any()
            g  = (self.inner_lung[i,:,1] == self.inner_color[1]).any()
            r  = (self.inner_lung[i,:,2] == self.inner_color[2]).any()

            if b and g and r:
                self.inner_lung_low = i
                break
        
        if self.inner_lung_low == -1 or self.inner_lung_up == -1:
            raise ValueError("Inner lung range is not desired (up, low)", self.inner_lung_up,  self.inner_lung_low)
        #print("ranges ","(", self.inner_lung_up, " ", self.inner_lung_low, ")")

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

    def init_layers(self, lung_dir):
        lung = cv2.imread(lung_dir)
        self.inner_lung = self.extract_color(lung, self.inner_color)
        self.outer_lung = self.extract_color(lung, self.outer_color)
        
        # initialize water filled lung
        self.inner_water_lung = np.zeros(self.inner_lung.shape)
        self.inner_water_lung[:,:,0] = np.where(self.inner_lung[:,:,0] == self.inner_color[0], self.inner_water_color[0], 0)
        self.inner_water_lung[:,:,1] = np.where(self.inner_lung[:,:,1] == self.inner_color[1], self.inner_water_color[1], 0)   
        self.inner_water_lung[:,:,2] = np.where(self.inner_lung[:,:,2] == self.inner_color[2], self.inner_water_color[2], 0)   

        # cv2.imshow("il", self.inner_lung)
        # cv2.imshow("ol", self.outer_lung)
        # cv2.imshow("iwl", self.inner_water_lung)
        # cv2.imwrite("iwl.png", self.outer_lung)
        # print(self.inner_color)
        # print(self.inner_water_color)
        # print(self.outer_color)
        # cv2.waitKey(1500)

    def extract_color(self, img, color):
        # source image is rgb but seperated layers will be rgba
        mask = np.zeros((img.shape[0], img.shape[1], 4))
        for i in range(3):
            mask[:,:,i] = np.where(img[:,:,i] == color[i], color[i], 0)     
        return mask

    def start(self, initial_air=1.0):
        self.check_dirs()
        self.air = initial_air
        self.n_frames = 0

    def linear_change(self, t, final_air):
        f = t*self.fps
        for i in range(f):
            self.air = self.air + int((i * (final_air - self.air)) / f)
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
    
    def write_frame(self, frame=None):
        if frame == None:
            # if lung is filled with water then chose water filled lung
            if self.air > 0:
                inner_lung = self.inner_lung
            else:
                inner_lung = self.inner_water_lung

            upper_range = int(self.inner_lung_up + (self.inner_lung_low - self.inner_lung_up) * (1 - abs(self.air)))
            inner_lung_sized = np.copy(inner_lung) 
            inner_lung_sized[:upper_range] = 0
            frame = inner_lung_sized + self.outer_lung

        cv2.imwrite(self.output_dir+"/images_lung/"+str(self.n_frames)+".png", frame)
        self.n_frames = self.n_frames + 1
    
    def stop(self):
        # ffmpeg assumes output is 25 fps. it is not a problem now but maybe it will need to be changed later
        os.system("ffmpeg -i "+self.output_dir+"/images_lung/%d.png -vcodec qtrle "+self.output_dir+"/"+self.video_name+".mov")
        shutil.rmtree(self.output_dir+"/images_lung/")


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
        for i in range(f):
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
        os.system("ffmpeg -i "+self.output_dir+"/images/%d.png -vcodec qtrle "+self.output_dir+"/"+self.video_name+".mov")
        shutil.rmtree(self.output_dir+"/images/")

# fast debug lines
#cv2.imshow("img", frame)
#cv2.waitKey(100)

def hbtg_test():
    h = hbtg()
    h.start(80)
    h.linear_change(10, 100)
    h.stop()

def lsg_test():
    lsg_ = lsg((255,216,0), (249, 77, 4), (124, 224, 9), "resources/full_lung_wb.png")
    lsg_.start(initial_air=-0.75)
    # lsg_.animate_breating()
    lsg_.linear_change(5, 1)
    lsg_.stop()

if __name__ == "__main__":  
    lsg_test()
