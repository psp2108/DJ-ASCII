import cv2
import RPi.GPIO as gpio
import time
import random
import requests
import json

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
        data.append(round(random.uniform(10.00, 5000.00),1))
    return data

def getThermalAverage(data):
    temp = 0
    for i in data:
        temp += i
    return temp/len(data)

def postData(weight, car_image="car_image.png",thermal_data=""):
    res = {}

    print("Calling API1")
    URL = "https://ca8f77e2.ngrok.io"
    api1 = "/insertRecordedDetails/" + str(weight).replace(".","*") + "/" + str(thermal_data).replace(".","*")
    api2 = "/uploader"

    try:
        r = requests.get(URL + api1) 
        data = r.json() 
        print("Setver Response",data.status)  
        res['status1'] = data.status
    except Exception as ex:
        print("Error ->>>",ex)  
        res['status1'] = False

    time.sleep(2)
    print("Calling API2")

    fin = open(car_image, 'rb')
    files = {'file': fin}
    try:
        r = requests.post(URL + api2, files=files)
        data = r.json() 
        print("Setver Response",data.status)    
        res['status2'] = data.status
    except Exception as ex:
        print("Error ->>>",ex)  
        res['status2'] = False
    finally:
        fin.close()
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

print("Preparing to read sample")
time.sleep(3)
sample= readCount()
print("Sample Readed")
flag=0
while 1:
    count= readCount()
    # w=0
    w=-(sample-count)/calibration_factor
    print(">>>>",w,"<<<<")
    if w > min_weight:
        print("Weight Detected",str(w) + "grams")
        time_counter += 1
        if delay_between_weight_reload * time_counter >= time_to_trigger_cam:
            print("Wait over")
            if not cam_triggered:
                print("Camera Triggered")
                #Capture Imaage 
                img = takeImage()
                #Take Thermal Data
                temp = getThermalAverage(getThermalData())
                #Post weight, car_image, theral_data to server
                res = postData(w,img,temp)
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
