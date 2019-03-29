import random
def getThermalData():
    data = []
    for d in range(1, 64):
        data.append(round(random.uniform(10.00, 50.00),1))
    return data

print(getThermalData())