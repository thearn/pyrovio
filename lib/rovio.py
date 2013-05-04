"""
A Python implementation of the Wowwee Rovio web-based API.

The Rovio mobile webcam is controlled through a web-based API.  The Rovio class
provides high level queries, and commands such and battery status and movement.

Classes:
  - Rovio: Higher level rovio functionality
  
Updated by Tristan Hearn (2013), tristanhearn@gmail.com
"""

import rovio_api 
import math
import time
try:
    from rovio_video import ipCamera
except:
    ipCamera = None

class Rovio:

    """
    An instance of the RovioApi class provides an usefull interface to one Rovio.

    This class provides usefull and convient functions like forward and 
    backward.  Also the who API can be accessed through the api object.

    You can set the hostname of the Rovio to connect to using the host
    property.  You can also set the IP address or host of the Rovio webcam
    itself using the Rovio API using SetHTTP.  After using SetHTTP, you are
    required to then set the host property to the same address in order to
    continue controlling the same Rovio object.  (Note: This was an arbitrary
    design decision in making the Rovio class.)  TODO: example

    Properties:
      - host:     hostname or IP address of the Rovio
      - port:     HTTP port number (default 80)
      - protocol: Protocol to use (read-only, default http)
      - speed:    Default Rovio speed (1 fastest, 10 slowest, default 1)
      - username: HTTP Auth name (default None)
      - password: HTTP Auth password (default None)

    Movement commands:

    All movement commands return a response code (SUCCESS for success, see
    Response Code Commands Table).  Non-camera movement commands have an
    optional speed parameter that defaults to the default speed of this Rovio
    object.

      - stop
      - forward
      - backward
      - left (straight left)
      - right (straight right)
      - rotate_left (by speed and angle)
      - rotate_right (by speed and angle)
      - forward_left
      - forward_right
      - back_left
      - back_right
      - head_up (camera)
      - head_down (camera)
      - head_middle (camera)
    """
    def __init__(self, host, username=None, password=None, port=80):
        """
        Initialize a new Rovio interface.

        Parameters:
          - host:     hostname or IP address
          - username: HTTP Auth name (default None)
          - password: HTTP Auth password (default None)
          - port:     HTTP port (default 80)
        """
        self.api= rovio_api.RovioApi( host = host, port=port,
                                      username = username, password=password)
        self.state = 0
        if ipCamera:
            url = "http://%s:%s/Jpeg/CamImg0000.jpg" % (host, port)
            self.camera = ipCamera(url, user = username, password=password)
        # Drive Functions

    def stop(self):
        """Stop if rovio is moving."""
        return self.api.manual_drive(0)

    def forward(self, speed=None):
        """Move Rovio forward."""
        return self.api.manual_drive(1, speed)

    def backward(self, speed=None):
        """Move Rovio backward."""
        return self.api.manual_drive(2, speed)

    def step_forward(self, dt=1, speed=None):
        """Move Rovio forward."""
        self.api.manual_drive(1, speed)
        time.sleep(dt)
        self.stop()

    def step_backward(self, dt=1, speed=None):
        """Move Rovio backward."""
        self.api.manual_drive(2, speed)
        time.sleep(dt)
        self.stop()

    def left(self, speed=None):
        """Move Rovio straight left."""
        return self.api.manual_drive(3, speed)

    def right(self, speed=None):
        """Move Rovio straight right."""
        return self.api.manual_drive(4, speed)

    def rotate_left(self, speed=None, angle=None):
        """ Rotate Rovio left by speed.
        The optional angle parameter turns the Rovio that many degrees

        Parameters:
          - speed
          - angle (optional)
        """
        if angle is None:
            return self.api.manual_drive(5, speed)
        else:
            return self.api.manual_drive(17, speed, self.degrees2angle(angle))
    def rotate_left_lag(self, tm=1,speed=None, angle=None):
        if angle is None:
            self.api.manual_drive(5, speed)
        else:
            self.api.manual_drive(17, speed, self.degrees2angle(angle))
        time.sleep(tm)
        self.api.manual_drive(0)
    def rotate_right_lag(self, tm=1,speed=None, angle=None):
        """ Rotate Rovio right by speed.
        The optional angle parameter turns the Rovio that many degrees

        Parameters:
          - speed
          - angle (optional)
        """
        if angle is None:
            self.api.manual_drive(6, speed)
        else:
            self.api.manual_drive(18, speed, self.degrees2angle(angle))
        time.sleep(tm)
        self.api.manual_drive(0)

    def rotate_right(self, speed=None, angle=None):
        """ Rotate Rovio right by speed.
        The optional angle parameter turns the Rovio that many degrees

        Parameters:
          - speed
          - angle (optional)
        """
        if angle is None:
            return self.api.manual_drive(6, speed)
        else:
            return self.api.manual_drive(18, speed, self.degrees2angle(angle))

    def degrees2angle(self,degrees):
        """Convert degress into rovio units"""
        full_circle = 10 * math.pi
        return degrees * full_circle / 360 

    def turn_around(self, speed=None):
        """ Turn the rovio 180 degress.  """
        self.rotate_right(speed=speed, angle=180)

    def forward_left(self, speed=None):
        """Move Rovio forward and left."""
        return self.api.manual_drive(7, speed)

    def forward_right(self, speed=None):
        """Move Rovio forward and right."""
        return self.api.manual_drive(8, speed)

    def back_left(self, speed=None):
        """Move Rovio backward and left."""
        return self.api.manual_drive(9, speed)

    def back_right(self, speed=None):
        """Move Rovio backward and right."""
        return self.api.manual_drive(10, speed)

    def head_up(self):
        """Move camera head looking up."""
        return self.api.manual_drive(11)

    def head_down(self):
        """Move camera head down, looking ahead."""
        return self.api.manual_drive(12)

    def head_middle(self):
        """Move camera head to middle position, looking ahead."""
        return self.api.manual_drive(13)

    # IR sensing
    def obstacal(self):
        """Returns True if IR detects obstacal, if ir is off returns false."""
        return self.isflag(2)

    def ir(self):
        """Is IR on?"""
        return self.isflag(4)

    def home(self):
        """Are you at you home?"""
        return self.isflag(1)

    def isflag(self, flag):
        """Is flag flag from flags true"""
        return int( self.api.get_report()['flags'] ) & flag != 0

    def position(self):
        """Returns the (x,y,theta) of the rover"""
        r = self.api.get_report()
        return (r['x'], r['y'], r['theta'] )

    def battery(self):
        """Returns the state of the battery"""
        report = self.api.get_report()
        
        return report['battery'], report['charging']


    # more complex functionality

    def forward_util_wall(self,speed=None):
        """Move forwards until a wall is encoutored"""
        if ( not self.ir() ):
            self.api.set_ir( 1 )
        while ( not self.obstacal() ):
            self.forward(speed)
        self.stop()

    def patrol(self, speed=None):
        """Move back and forth between two walls"""
        self.forward_util_wall(speed)
        self.turn_around(speed)
        time.sleep(2)
        self.forward_util_wall(speed)
        self.turn_around(speed)

    def dock_and_undock(self,times=72, secs=600):
        """dock and undoc evey secs seconds"""
        for t in range( times ):
            time.sleep(secs)
            self.api.go_home()
            time.sleep(15) # sleep 15 to let rovio get off dock
            self.api.go_home_and_dock()

# Note 
# 1: Movement speed
# 2: Turn Speed
# 3: Angle Trun Speed

# Speculation: angle is in radians /2 * 10