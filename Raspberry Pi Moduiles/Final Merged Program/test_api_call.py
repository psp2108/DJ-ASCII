import time
import requests
def postData(weight, car_image="car_image.png",thermal_data=""):
    print("Calling API1")
    URL = "https://3cc5aae9.ngrok.io"
    api1 = "/insertRecordedDetails/" + str(weight).replace(".","*") + "/" + str(thermal_data).replace(".","*")
    api2 = "/uploader"

    # URL = "http://maps.googleapis.com/maps/api/geocode/json"
    
    # # location given here 
    # location = "delhi technological university"
    
    # # defining a params dict for the parameters to be sent to the API 
    # PARAMS = {'address':location} 
    
    # # sending get request and saving the response as response object 
    r = requests.get(URL + api1) 
        
    # # extracting data in json format 
    # data = r.json() 
    # print("Setver Response",data.status)  
    print(r.text)
    time.sleep(2)
    print("Calling API2")

    # url = "http://localhost:5000/uploader"
    fin = open(car_image, 'rb')
    files = {'file': fin}
    try:
        r = requests.post(URL + api2, files=files)
        # data = r.json() 
        # print("Setver Response",data.status)  
        print(r.text)
    except:
        print("Error")
    finally:
        fin.close()

postData(1560.56,thermal_data = 345.2)
