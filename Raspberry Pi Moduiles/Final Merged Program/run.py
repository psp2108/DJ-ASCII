import cv2
import RPi.GPIO as gpio
import time
import random
import requests
import json

def rgb_off():
    gpio.output(pred, False)
    gpio.output(pgreen, False)
    gpio.output(pblue, False)

def rgb_red():
    gpio.output(pred, True)
    gpio.output(pgreen, False)
    gpio.output(pblue, False)

def rgb_green():
    gpio.output(pred, False)
    gpio.output(pgreen, True)
    gpio.output(pblue, False)

def rgb_blue():
    gpio.output(pred, False)
    gpio.output(pgreen, False)
    gpio.output(pblue, True)

def rgb_yellow():
    gpio.output(pred, True)
    gpio.output(pgreen, True)
    gpio.output(pblue, False)

def rgb_pink():
    gpio.output(pred, True)
    gpio.output(pgreen, False)
    gpio.output(pblue, True)
    
def rgb_cyan():
    gpio.output(pred, False)
    gpio.output(pgreen, True)
    gpio.output(pblue, True)

def rgb_white():
    gpio.output(pred, True)
    gpio.output(pgreen, True)
    gpio.output(pblue, True)


def takeImage(img_name="car_image.png"):
    cam = cv2.VideoCapture(0)
    # cv2.namedWindow("test")
    for get_garbage_frames in range(15):
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
        data.append(round(random.uniform(80.00, 200.00),2))
    return data

def getThermalAverage(data):
    temp = 0
    for i in data:
        temp += i
    return temp/len(data)

def postData(weight, car_image="car_image.png",thermal_data=""):
    res = {}

    print("Calling API1")
    URL = "https://2e8f664d.ngrok.io"
    #URL = "https://e2213ee4.ngrok.io/"
    api1 = "/insertRecordedDetails/" + str(weight).replace(".","*") + "/" + str(thermal_data).replace(".","*")
    api2 = "/uploader"

    try:
        r = requests.get(URL + api1) 
        data = r.json() 
        print("Setver Response",data)  
        #res['status1'] = data.status
    except Exception as ex:
        print("Error ->>>",ex)  
        res['status1'] = False

    rgb_red()
    time.sleep(2)
    rgb_blue()

    print("Calling API2")

    fin = open(car_image, 'rb')
    files = {'file': fin}
    try:
        r = requests.post(URL + api2, files=files)
        data = r.json() 
        print("Setver Response",data)    
        #res['status2'] = data.status
    except Exception as ex:
        print("Error ->>>",ex)  
        res['status2'] = False
    finally:
        fin.close()
        rgb_green()

    return res
    
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

########################################################

##### RGB ####
pred = 23
pgreen = 24
pblue = 25
##############

DT =21
SCK=20
HIGH=1
LOW=0
sample=0
val=0
calibration_factor = 210
min_weight = 50
cam_triggered = False
time_counter = 0
time_to_trigger_cam = 4 #sec
delay_between_weight_reload = 1

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(SCK, gpio.OUT)

  
######## SETTING RGB ##########
gpio.setup(pred, gpio.OUT)
gpio.setup(pgreen, gpio.OUT)
gpio.setup(pblue, gpio.OUT)
###############################

rgb_cyan()

print("Preparing to read sample")
time.sleep(3)
sample= readCount()
print("Sample Readed")
flag=0
while 1:
    count= readCount()
    # w=0
    w=-(sample-count)/calibration_factor
    rgb_green()
    print(">>>>",w,"<<<<")

    if w > min_weight:
        rgb_yellow()
        print("Weight Detected",str(w) + "grams")
        time_counter += 1
        if delay_between_weight_reload * time_counter >= time_to_trigger_cam:
            rgb_red()
            print("Wait over")
            if not cam_triggered:
                print("Camera Triggered")
                #Capture Imaage 
                img = takeImage()
                #Take Thermal Data
                temp = getThermalAverage(getThermalData())
                #Post weight, car_image, theral_data to server
                rgb_blue()
                res = postData(w*3/200,img,temp)
                print(res)
                cam_triggered = True    
            else:
                print("Camera not triggered")
        else:
            print("Waiting..", time_counter)
    else:
        print("No Weight")
        time_counter = 0
        if cam_triggered:
            pass
        cam_triggered = False

    time.sleep(delay_between_weight_reload)

