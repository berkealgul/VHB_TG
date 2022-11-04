import numpy as np
import cv2


class hbg:
    def __init__(self, fps=25, output_name="output.mp4"):
        self.fps = fps
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 1
        self.font_thickness = 2
        (self.label_width, self.label_height), self.baseline = cv2.getTextSize("9999", self.font, self.font_scale, self.font_thickness)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter(output_name, fourcc, fps, (self.label_width, self.label_height+self.baseline))

    def start(self, initial_beat):
        self.beat = initial_beat
        self.time = 0

    def write_frame(self):
        frame = np.zeros((self.label_height + self.baseline, self.label_width, 3), np.uint8)
        cv2.putText(frame, str(self.beat),(0, self.label_height), self.font, self.font_scale, (255, 255, 255), self.font_thickness, cv2.LINE_AA)  
        self.writer.write(frame)

    def linear_rise(self, dt):
        for i in range(1, dt*self.fps):
            self.beat = self.beat + 1
            self.write_frame() 

    def stop(self):
        self.writer.release()


# fast debug lines
#cv2.imshow("img", frame)
#cv2.waitKey(100)

def test():
    h = hbg(output_name="./output/output.mp4")
    h.start(80)
    h.linear_rise(50)
    h.stop()

if __name__ == "__main__":  
    test()