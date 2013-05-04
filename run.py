from lib import Rovio
import cv2
import numpy as np
from skimage import filter, img_as_ubyte


class rovioControl(object):
    def __init__(self,url, username, password, port = 80):
        self.rovio = Rovio(url,username=username,password=password, 
                                 port = port)
        self.last = None
        self.key = 0
        
    def night_vision(self,frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.equalizeHist(frame)
        return frame
    
    def show_battery(self,frame):
        sh = frame.shape
        m,n = sh[0], sh[1]
        battery,charging = self.rovio.battery()
        battery = 100*battery/130.
        bs = "Battery: %0.1f" % battery
        cs = "Status: Roaming"
        if charging == 80:
            cs = "Status: Charging"
        cv2.putText(frame,bs,(20,20),
                    cv2.FONT_HERSHEY_PLAIN,2,(255,0,0))
        
        cv2.putText(frame,cs,(300,20),
                    cv2.FONT_HERSHEY_PLAIN,2,(255,0,0))
        
        return frame
    
    def resize(self,frame, size = (640,480)):
        frame = cv2.resize(frame, size)
        return frame

    def main(self):
        frame = self.rovio.camera.get_frame()
        if not isinstance(frame, np.ndarray):
            return
        frame = self.night_vision(frame)
        #frame = filter.sobel(frame)
        #frame = img_as_ubyte(frame)
        frame = self.resize(frame)
        
        frame = cv2.merge([frame,frame,frame])
        
        frame = self.show_battery(frame)
        
        cv2.imshow("rovio", frame)
        
        self.key = cv2.waitKey(20)
        if self.key > 0:
            #print self.key
            pass
        if self.key == 114: #r
            self.rovio.turn_around()
        elif self.key == 63233 or self.key == 115: #down or s
            self.rovio.backward(speed=1)
        elif self.key == 63232 or self.key == 119: #up or w
            self.rovio.forward(speed=1)
        elif self.key == 63234 or self.key == 113: #left or a
            self.rovio.rotate_left(angle=12,speed=5)
        elif self.key == 63235 or self.key == 101: #right or d
            self.rovio.rotate_right(angle=12,speed=5)
        elif self.key == 97: #left or a
            self.rovio.left(speed=1)
        elif self.key == 100: #right or d
            self.rovio.right(speed=1)
        elif self.key == 44: #comma
            self.rovio.head_down()
        elif self.key == 46: #period
            self.rovio.head_middle()
        elif self.key == 47: #slash
            self.rovio.head_up()
        
if __name__ == "__main__":
    url = '192.168.1.1'
    user = 'myname'
    password = "12345"
    app = rovioControl(url, user, password)
    while True:
        app.main()
        if app.key == 27:
            break


    