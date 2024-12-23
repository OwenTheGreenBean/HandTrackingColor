# How the project works
Youtube video: https://www.youtube.com/watch?v=hPijy3M5150
I have created a project that takes the position of the finger using Google's media pipe library and an Arduino nano
## Setting up librarys

To install the librarys I will be using pip. Make sure pip is installed and up to date.First to get the camera feed we must use the open CV library. To install this use this command in the terminal

```
pip install opencv-python
```

With Open CV now installed we can now track the hand from the camera feed using Google's media pipe library. To install it run this command in the terminal

```
pip install mediapipe
```

To then communicate the colors we want to make the light on the arduino we can use the serial library. 

```
pip install pyserial
```

## Files

To start the program first upload the file in the arduino directory to the arduino of your choice and have the LED wired up. After this you can then connect the arduino to your laptop via serial cable. It is important to make sure that on line 7 of the main.py file the serial port is updated
```
ser = serial.Serial('/dev/cu.usbserial-210', 9600)
```
On mac to find the arduino serial port you can run the command
```
 ls /dev/tty.*
```
On windows you can navigate to the device manager and then port and hidden ports to find the directory of the arduino. Once this is finished when running the main.py file a window will popup with the video feed and this should allow you to change the color of the light with the position of your hand

## How it works

![](https://github.com/HandTrackingColor/howitworks.gif)


