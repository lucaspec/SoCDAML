import Jetson.GPIO as GPIO
import pandas as pd
import time 
import os 
import json

''' 
Python script to control the FIZ camera motors by applying voltage over the Jetson GPIOs.
The absolute level of focus, iris and zoom are given as active motor time in ms.
Their values are tracked and updated across different script calls within "values.json".
Note: use multiples of at least 100ms to attain consistent and reliable results.
'''

#==============================================================#
#----------------------- Definitions --------------------------#
#==============================================================#

# Pin Definitions
ZOOM_IN_GPIO = 12 # yellow
ZOOM_OUT_GPIO = 13 # green
FOCUS_NEAR_GPIO = 11 # purple
FOCUS_FAR_GPIO = 15 # blue
IRIS_OPEN_GPIO = 19 # white
IRIS_CLOSE_GPIO = 21 # grey

# max FIZ values -> corresponds to max motor duration @ 5V in milliseconds
max_zoom = 5800 # max zoom in
max_focus = 6600 # max focus far
max_iris = 3400 # max iris open


#==============================================================#
#------------------- FIZ control methods ----------------------#
#==============================================================#

''' 
Methods to manipulate zoom, focus and iris levels (relative and absolute).
All input arguments are with respect to max_zoom, max_focus and max_iris and use the same units (ms).
'''

def zoomIn(durationMS):
	# zoom in for given time
	GPIO.output(ZOOM_IN_GPIO, GPIO.HIGH)
	GPIO.output(ZOOM_OUT_GPIO, GPIO.LOW)
	time.sleep(durationMS/1000)
	GPIO.output(ZOOM_IN_GPIO, GPIO.LOW)

	# update values.json
	with open('values.json', 'r') as f:
		data = json.load(f)
		value = data["zoom"]
	new_value = value+durationMS if max_zoom > value+durationMS else max_zoom
	data["zoom"] = new_value
	with open('values.json', 'w') as f:
		json.dump(data, f)


def zoomOut(durationMS):
	# zoom out for given time
	GPIO.output(ZOOM_OUT_GPIO, GPIO.HIGH)
	GPIO.output(ZOOM_IN_GPIO, GPIO.LOW)
	time.sleep(durationMS/1000)
	GPIO.output(ZOOM_OUT_GPIO, GPIO.LOW)

	# update values.json
	with open('values.json', 'r') as f:
		data = json.load(f)
		value = data["zoom"]
	new_value = value-durationMS if 0 < value-durationMS else 0
	data["zoom"] = new_value
	with open('values.json', 'w') as f:
		json.dump(data, f)


def zoomSet(level):
	# read current zoom value
	with open('values.json', 'r') as f:
		data = json.load(f)
		value = data["zoom"]
	
	# zoom to the given level
	diff = level-value
	if diff > 0:
		zoomIn(diff)
	else:
		zoomOut(abs(diff))


def zoomReset():
	# make sure zoom is 0
	zoomOut(7000)

	# update values.json
	with open('values.json', 'r') as f:
		data = json.load(f)
	data["zoom"] = 0
	with open('values.json', 'w') as f:
		json.dump(data, f)


def focusNear(durationMS):
	# focus near for given time
	GPIO.output(FOCUS_NEAR_GPIO, GPIO.HIGH)
	GPIO.output(FOCUS_FAR_GPIO, GPIO.LOW)
	time.sleep(durationMS/1000)
	GPIO.output(FOCUS_NEAR_GPIO, GPIO.LOW)

	# update values.json
	with open('values.json', 'r') as f:
		data = json.load(f)
		value = data["focus"]
	new_value = value-durationMS if 0 < value-durationMS else 0
	data["focus"] = new_value
	with open('values.json', 'w') as f:
		json.dump(data, f)


def focusFar(durationMS):
	# focus far for given time
	GPIO.output(FOCUS_FAR_GPIO, GPIO.HIGH)
	GPIO.output(FOCUS_NEAR_GPIO, GPIO.LOW)
	time.sleep(durationMS/1000)
	GPIO.output(FOCUS_FAR_GPIO, GPIO.LOW)

	# update values.json
	with open('values.json', 'r') as f:
		data = json.load(f)
		value = data["focus"]
	new_value = value+durationMS if max_focus > value+durationMS else max_focus
	data["focus"] = new_value
	with open('values.json', 'w') as f:
		json.dump(data, f)


def focusSet(level):
	# read current zoom value
	with open('values.json', 'r') as f:
		data = json.load(f)
		value = data["focus"]
	
	# zoom to the given level
	diff = level-value
	if diff > 0:
		focusFar(diff)
	else:
		focusNear(abs(diff))


def focusReset():
	# make sure focus is 0
	focusNear(7000)

	# update values.json
	with open('values.json', 'r') as f:
		data = json.load(f)
	data["focus"] = 0
	with open('values.json', 'w') as f:
		json.dump(data, f)


def irisOpen(durationMS):
	# open iris for given time
	GPIO.output(IRIS_OPEN_GPIO, GPIO.HIGH)
	GPIO.output(IRIS_CLOSE_GPIO, GPIO.LOW)
	time.sleep(durationMS/1000)
	GPIO.output(IRIS_OPEN_GPIO, GPIO.LOW)

	# update values.json
	with open('values.json', 'r') as f:
		data = json.load(f)
		value = data["iris"]
	new_value = value+durationMS if max_iris > value+durationMS else max_iris
	data["iris"] = new_value
	with open('values.json', 'w') as f:
		json.dump(data, f)


def irisClose(durationMS):
	# close iris for given time
	GPIO.output(IRIS_CLOSE_GPIO, GPIO.HIGH)
	GPIO.output(IRIS_OPEN_GPIO, GPIO.LOW)
	time.sleep(durationMS/1000)
	GPIO.output(IRIS_CLOSE_GPIO, GPIO.LOW)

	# update values.json
	with open('values.json', 'r') as f:
		data = json.load(f)
		value = data["iris"]
	new_value = value-durationMS if 0 < value-durationMS else 0
	data["iris"] = new_value
	with open('values.json', 'w') as f:
		json.dump(data, f)


def irisSet(level):
	# read current zoom value
	with open('values.json', 'r') as f:
		data = json.load(f)
		value = data["iris"]
	
	# zoom to the given level
	diff = level-value
	if diff > 0:
		irisOpen(diff)
	else:
		irisClose(abs(diff))


def irisReset():
	# make sure iris is 0 -> closed
	irisClose(4000)

	# update values.json
	with open('values.json', 'r') as f:
		data = json.load(f)
	data["iris"] = 0
	with open('values.json', 'w') as f:
		json.dump(data, f)


#==============================================================#
#-------------- Methods to manipulate FIZ values --------------#
#==============================================================#

def print_FIZ_values():
    try:
        with open('values.json', 'r') as f:
            data = json.load(f)
            print("zoom: ", int(data["zoom"]))
            print("focus: ", int(data["focus"]))
            print("iris: ", int(data["iris"]))
    except (FileNotFoundError, json.JSONDecodeError):
        return 0


def reset_FIZ_values():
    with open('values.json', 'w') as f:
        json.dump({"zoom": 0, "focus": 0, "iris": 0}, f)


#==============================================================#
#----------------------- Look up table ------------------------#
#==============================================================#

# read dataframe from csv
df = pd.read_csv('lookUp.csv', header=None)

# define row IDs (distance in m) and column IDs (zoom in %)
row_ids = [1.4, 1.5, 1.6, 1.8, 2, 2.2, 2.5, 2.8, 3, 3.5, 4, 4.5, 5, 5.5, 6, 7]
column_ids = [60, 65, 70, 75, 80, 85, 90, 95, 100]
df.index = row_ids
df.columns = column_ids

# return value from look up table
def lookUp(distance, zoom):
	return df.loc[distance, zoom]

# return number from array which is closest to target number
def find_closest_number(arr, target):
    closest = min(arr, key=lambda x: abs(x - target))
    return closest

# focus the camera given the distance (in m) and zoom (in %)
def focus(distance, zoom):
	# check validity of input values
	if distance > 7.5 or distance < 0:
		raise ValueError("Supported distances: [0, 7.5]")
	if zoom > 100 or zoom < 60:
		raise ValueError("Supported zoom: [60, 100]")

	# match to closest value in look up table
	distance = find_closest_number(row_ids, distance)
	zoom = find_closest_number(column_ids, zoom)
	focus = lookUp(distance, zoom)

	# focus camera accordingly
	if focus == 'x':
		raise Exception("Focus not possible")
	else:
		focus = int(focus)
		print('Setting zoom to {}%'.format(zoom))
		zoomSet(zoom/100 * max_zoom)
		print('Setting focus to {}%'.format(focus))
		focusSet(focus/100 * max_focus)
		

#==============================================================#
#----------------------- Main method --------------------------#
#==============================================================#

def main():
	# Set BCM pin-numbering scheme
	GPIO.setmode(GPIO.BOARD)

	# Ignore warnings
	GPIO.setwarnings(False)

	# Set all pins to output with initial state LOW
	GPIO.setup(ZOOM_IN_GPIO, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(ZOOM_OUT_GPIO, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(FOCUS_NEAR_GPIO, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(FOCUS_FAR_GPIO, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(IRIS_OPEN_GPIO, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(IRIS_CLOSE_GPIO, GPIO.OUT, initial=GPIO.LOW)

	# Demo use case
	print("start demo")
	distance = 2.966 # distance in m
	zoom = 91 # zoom in %
	focus(distance, zoom)
	print_FIZ_values()
	print("demo finished")

if __name__ == '__main__':
    main()
