# Mini-Project

Mini-Project of the "System-on-Chip for Data Analytics and Machine Learning" lecture 

**Task Description**: Control focus, iris and zoom of a PTZ camera using the GPIOs of a Jetson AGX Orin


## Files

- ```FIZ.py```: is the main python script that contains all the methods to control the camera 
- ```lookUp.csv```: is the look-up table used to keep the camera in focus for a given distance and zoom
- ```values.json```: is used to track the level of focus, zoom and iris across different script calls