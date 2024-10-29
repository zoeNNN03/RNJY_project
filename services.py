from gtts import gTTS
import os
import pygame
import speech_recognition as sr
import cv2
import time
from ultralytics import YOLO
from serial.tools import list_ports
import pydobot

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[0].device

r = 10
home = [185.97, 143.61, -22]
red = [-36.89, 261.55, -45]
blue = [-60.53, 222.36, -45]
garbage = [185.97, 143.61, -22]
poduction = [108.12, 188.01, -45]

device = pydobot.Dobot(port=port, verbose=False)
device.suck(False)
device.move_to(device.pose()[0], device.pose()[1], home[2]+10, r, wait=True)
device.move_to(home[0], home[1], home[2]+10, r, wait=True)

# Create a Recognizer object
recognizer = sr.Recognizer()
mic = sr.Microphone(device_index=1)

red_point = 0
blue_point = 0

model = YOLO("best.pt")

def text2speech(text):
	tts = gTTS(text=text, lang='en', slow=False)
	tts.save("output.mp3")
	pygame.init()
	pygame.mixer.init()
	pygame.mixer.music.load("output.mp3")
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy():
		continue
	os.remove("output.mp3")

def button_a():
	global red_point, blue_point
	start, end = time.time(), time.time()
	while end-start < 15:
		if red_point == 2 and blue_point == 2:
			text2speech('Storage not enough')
			break
		else:
			result = yolov_detection()
			if result != None:
				start = time.time()
				if result == 'red':
					if red_point == 2:
						text2speech('Red storage full')
						dobot_croltrol('a', 'garbage')
					else:
						dobot_croltrol("a", "red")
						red_point += 1
				elif result == 'blue':
					if blue_point == 2:
						text2speech('Blue storage full')
						dobot_croltrol('a', 'garbage')
					else:
						dobot_croltrol("a", "blue")
						blue_point += 1
			end = time.time()

def button_b():
	global red_point, blue_point
	print(f'red: {red_point}')
	print(f'blue: {blue_point}')
	time.sleep(3)
	if red_point >= 2 and blue_point >= 2:
		dobot_croltrol("b")

def button_mic():
	# ~ (x, y, z, r, j1, j2, j3, j4) = device.pose()
	# ~ print(f'{x:.2f}, {y:.2f}, {z:.2f}')
	
	with mic as source:
		recognizer.adjust_for_ambient_noise(source)
		audio = recognizer.listen(source)
		
	try:
		said = recognizer.recognize_google(audio)
		print(said.lower().split())
		if 'a' in said.lower().split():
			text2speech("This is a show of sorting products from labels. If the products are in the standard section, they will be transported to the next process.")
			button_a()
		elif 'b' in said.lower().split():
			text2speech("This is an engine assembly simulation. If the products are in the standard section.")
			button_b()
		else:
			text2speech("I don't understand. Please say it again.")
			print("idk")
	except sr.UnknownValueError:
		print("Could not understand audio")
		text2speech("Could not understand audio")
	except sr.RequestError as e:
		print(f"Could not request results; {e}")
		text2speech("Error")

def yolov_detection():
    cam = cv2.VideoCapture(0)
    result, image = cam.read()
    if result: 
        results = model(image, save=True)
        for r in results:
            for box in r.boxes:
                cls = int(box.cls.item())
                if cls == 0:
                    return "blue"
                elif cls == 1:
                    return "red"
    return None


def dobot_croltrol(selection_, color = None):
	global red_point, blue_point
	if selection_ == "a":
		if color == "red":
			device.move_to(home[0], home[1], home[2], r, wait=True)
			device.suck(True)
			device.move_to(home[0], home[1], home[2]+10, r, wait=True)
	
			device.move_to(red[0], red[1], red[2]+(25*red_point)+10, r, wait=True)
			device.move_to(red[0], red[1], red[2]+(25*red_point), r, wait=True)
			device.suck(False)
			device.move_to(red[0], red[1], red[2]+(25*red_point)+10, r, wait=True)
			
			device.move_to(home[0], home[1], red[2]+(25*2)+10, r, wait=True)
			device.move_to(home[0], home[1], home[2]+10, r, wait=True)
		elif color == 'blue':
			device.move_to(home[0], home[1], home[2], r, wait=True)
			device.suck(True)
			device.move_to(home[0], home[1], home[2]+10, r, wait=True)
		
			device.move_to(blue[0], blue[1], blue[2]+(25*blue_point)+10, r, wait=True)
			device.move_to(blue[0], blue[1], blue[2]+(25*blue_point), r, wait=True)
			device.suck(False)
			device.move_to(blue[0], blue[1], blue[2]+(25*blue_point)+10, r, wait=True)
			
			device.move_to(home[0], home[1], blue[2]+(25*2)+10, r, wait=True)
			device.move_to(home[0], home[1], home[2]+10, r, wait=True)
		else:
			device.move_to(home[0], home[1], home[2], r, wait=True)
			device.suck(True)
			device.move_to(home[0], home[1], home[2]+10, r, wait=True)
		
			device.move_to(garbage[0], garbage[1], home[2]+10, r, wait=True)
			device.suck(False)
			device.move_to(garbage[0], garbage[1], home[2]+10, r, wait=True)
			
			device.move_to(home[0], home[1], home[2]+10, r, wait=True)
	else:
		print("Move dobot B")
		device.move_to(device.pose()[0], device.pose()[1], red[2]+(25*(red_point-1))+10, r, wait=True)
		device.move_to(red[0], red[1], red[2]+(25*(red_point-1))+10, r, wait=True)
		device.move_to(red[0], red[1], red[2]+(25*(red_point-1)), r, wait=True)
		device.suck(True)
		device.move_to(red[0], red[1], red[2]+(25*(red_point-1))+10, r, wait=True)
		device.move_to(poduction[0]+35, poduction[1], red[2]+(25*(red_point-1))+10, r, wait=True)
		device.move_to(poduction[0]+35, poduction[1], poduction[2], r, wait=True)
		device.suck(False)
		red_point -= 1
		
		device.move_to(poduction[0]+35, poduction[1], blue[2]+(25*(blue_point-1))+10, r, wait=True)
		device.move_to(blue[0], blue[1], blue[2]+(25*(blue_point-1))+10, r, wait=True)
		device.move_to(blue[0], blue[1], blue[2]+(25*(blue_point-1)), r, wait=True)
		device.suck(True)
		device.move_to(blue[0], blue[1], blue[2]+(25*(blue_point-1))+10, r, wait=True)
		device.move_to(poduction[0], poduction[1], blue[2]+(25*(blue_point-1))+10, r, wait=True)
		device.move_to(poduction[0], poduction[1], poduction[2], r, wait=True)
		device.suck(False)
		blue_point -= 1
		
		device.move_to(poduction[0], poduction[1], red[2]+(25*(red_point-1))+10, r, wait=True)
		device.move_to(red[0], red[1], red[2]+(25*(red_point-1))+10, r, wait=True)
		device.move_to(red[0], red[1], red[2]+(25*(red_point-1)), r, wait=True)
		device.suck(True)
		device.move_to(red[0], red[1], red[2]+(25*(red_point-1))+10, r, wait=True)
		device.move_to(poduction[0]-35, poduction[1], red[2]+(25*(red_point-1))+10, r, wait=True)
		device.move_to(poduction[0]-35, poduction[1], poduction[2], r, wait=True)
		device.suck(False)
		red_point -= 1
		
		device.move_to(poduction[0]-35, poduction[1], blue[2]+(25*(blue_point-1))+10, r, wait=True)
		device.move_to(blue[0], blue[1], blue[2]+(25*(blue_point-1))+10, r, wait=True)
		device.move_to(blue[0], blue[1], blue[2]+(25*(blue_point-1)), r, wait=True)
		device.suck(True)
		device.move_to(blue[0], blue[1], blue[2]+(25*(blue_point-1))+10, r, wait=True)
		device.move_to(poduction[0], poduction[1], poduction[2]+35, r, wait=True)
		device.move_to(poduction[0], poduction[1], poduction[2]+25, r, wait=True)
		device.suck(False)
		blue_point -= 1
		
		device.move_to(poduction[0], poduction[1], home[2]+10, r, wait=True)
		device.move_to(home[0], home[1], home[2]+10, r, wait=True)
