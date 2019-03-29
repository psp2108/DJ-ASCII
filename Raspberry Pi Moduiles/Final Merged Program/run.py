import cv2
import RPi.GPIO as gpio
import time
import random
import requests

DT =21
SCK=20
HIGH=1
LOW=0
sample=0
val=0
calibration_factor = 212
min_weight = 50
cam_triggered = False
time_counter = 0
time_to_trigger_cam = 10 #sec
delay_between_weight_reload = 0.1

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(SCK, gpio.OUT)
    
def setCursor(x,y):
    if y == 0:
        n=128+x
    elif y == 1:
        n=192+x
    lcdcmd(n)

def readCount():
  i=0
  Count=0
  gpio.setup(DT, gpio.OUT)
  gpio.output(DT,1)
  gpio.output(SCK,0)
  gpio.setup(DT, gpio.IN)

  while gpio.input(DT) == 1:
      i=0
  for i in range(24):
        gpio.output(SCK,1)
        Count=Count<<1

        gpio.output(SCK,0)
        #time.sleep(0.001)
        if gpio.input(DT) == 0: 
            Count=Count+1
            #print Count
        
  gpio.output(SCK,1)
  Count=Count^0x800000
  #time.sleep(0.001)
  gpio.output(SCK,0)
  return Count  

#begin()

time.sleep(3)
sample= readCount()
flag=0
while 1:
    count= readCount()
    # w=0
    w=(sample-count)/calibration_factor

    if w > min_weight:
        time_counter += 1
        if delay_between_weight_reload * time_counter >= time_to_trigger_cam:
            if not cam_triggered:
                #Capture Imaage 
                img = takeImage()
                #Take Thermal Data
                data = getThermalData()
                #Post weight, car_image, theral_data to server
                res = postData(w,img,data)
                print(res)
                cam_triggered = True    
            pass
    else:
        time_counter = 0
        if cam_triggered:
            pass
        cam_triggered = False


    time.sleep(delay_between_weight_reload)

########################################################

def takeImage(img_name="car_image.png"):
    cam = cv2.VideoCapture(0)
    # cv2.namedWindow("test")
    ret, frame = cam.read()
    # cv2.imshow("test", frame)
    if ret: 
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
    
    return img_name
    # cam.release()
    # cv2.destroyAllWindows()

def getThermalData():
    data = []
    for d in range(1, 64):
        data.append(round(random.uniform(10.00, 50.00),1))
    return data

def postData(weight, car_image="car_image.png",theral_data=""):
    # url = "http://localhost:5000/uploader"
    # fin = open(car_image, 'rb')
    # files = {'file': fin}
    # try:
    #     r = requests.post(url, files=files)
    #     print(r.text)
    # finally:
    #     fin.close()

    
    # URL = "http://maps.googleapis.com/maps/api/geocode/json"
    
    # # location given here 
    # location = "delhi technological university"
    
    # # defining a params dict for the parameters to be sent to the API 
    # PARAMS = {'address':location} 
    
    # # sending get request and saving the response as response object 
    # r = requests.get(url = URL, params = PARAMS) 
    
    # # extracting data in json format 
    # data = r.json() 
    # print(data)  
    pass