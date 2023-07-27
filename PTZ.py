import Jetson.GPIO as GPIO
import time  

# Pin Definitions (TODO: find pin numbers)
ZOOM_IN_GPIO = 15
ZOOM_OUT_GPIO = 16
FOCUS_IN_GPIO = 3
FOCUS_OUT_GPIO = 4
IRIS_IN_GPIO = 5
IRIS_OUT_GPIO = 6


# PTZ methods
def zoomIn(durationMS):
	GPIO.output(ZOOM_IN_GPIO, GPIO.HIGH)
	GPIO.output(ZOOM_OUT_GPIO, GPIO.LOW)
	time.sleep(durationMS/1000)
	GPIO.output(ZOOM_IN_GPIO, GPIO.LOW)

def zoomOut(durationMS):
    GPIO.output(ZOOM_OUT_GPIO, GPIO.HIGH)
    GPIO.output(ZOOM_IN_GPIO, GPIO.LOW)
    time.sleep(durationMS/1000)
    GPIO.output(ZOOM_OUT_GPIO, GPIO.LOW)

def focusIn(durationMS):
	GPIO.output(FOCUS_IN_GPIO, GPIO.HIGH)
	GPIO.output(FOCUS_OUT_GPIO, GPIO.LOW)
	time.sleep(durationMS/1000)
	GPIO.output(FOCUS_IN_GPIO, GPIO.LOW)

def focusOut(durationMS):
    GPIO.output(FOCUS_OUT_GPIO, GPIO.HIGH)
    GPIO.output(FOCUS_IN_GPIO, GPIO.LOW)
    time.sleep(durationMS/1000)
    GPIO.output(FOCUS_OUT_GPIO, GPIO.LOW)

def irisIn(durationMS):
	GPIO.output(IRIS_IN_GPIO, GPIO.HIGH)
	GPIO.output(IRIS_OUT_GPIO, GPIO.LOW)
	time.sleep(durationMS/1000)
	GPIO.output(IRIS_IN_GPIO, GPIO.LOW)

def irisOut(durationMS):
    GPIO.output(IRIS_OUT_GPIO, GPIO.HIGH)
    GPIO.output(IRIS_IN_GPIO, GPIO.LOW)
    time.sleep(durationMS/1000)
    GPIO.output(IRIS_OUT_GPIO, GPIO.LOW)



def main():
    # Set BCM pin-numbering scheme
    GPIO.setmode(GPIO.BCM)

    # Set all pins to output with initial state LOW
    GPIO.setup(ZOOM_IN_GPIO, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(ZOOM_OUT_GPIO, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(FOCUS_IN_GPIO, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(FOCUS_OUT_GPIO, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IRIS_IN_GPIO, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IRIS_OUT_GPIO, GPIO.OUT, initial=GPIO.LOW)

    # Demo use case, zoom in for 1000 ms
    print("Starting demo now!")
    try:
        zoomIn(1000)
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()