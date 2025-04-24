#imports
import math
from math import atan2
import numpy as np
import numpy.polynomial.polynomial as npp
import matplotlib.pyplot as plt

#constants
k = 1.6
yds2meters = 3.281
decayConstant = 24.5
newtonCoeff = 0.7
meuK = 0.04
VminBounce = 0.4
minTheta = math.radians(10)
gasConstWaterVap = 461.5
gasConstAir = 287.05
ballMass = 0.0457
ballRadius = 21.35
ballArea = (ballRadius*10**-3)**2 * math.pi
ZRef = 10
Z0 = 0.4

tempSta = 12.8
tempBol = 13.7
tempPhil = 25.6


pressureSta  = 101200
pressureBol = 103200
pressurePhil = 101300


humSta = 80
humBol = 42
humPhil = 77
relHum = 90


#gravity values in ms^-2
gravSta = 9.81618225
gravBolivia = 9.774220451
gravPhilippines = 9.782893875
gravAvg = 9.81
gravUsed = 0

#velocity values in ms^-1
velLow = 61.7
velMed = 77.3
velHigh = 85
velUsed = 0


windSta = 4.37
windBol = 3
windPhil = 3.94
windUsed = 0

AvgProMenSpin = 2686
AvgProWomSpin = 2611

print("Select Gravity Value")
print("Input 1 for St Andrews")
print("Input 2 for Bolivia")
print("Input 3 for Average")
print("Input 4 for Philippines")
print("Input 5 to input your own")


gravInput = int(input("Enter Gravity Value: "))
if gravInput == 1:
    gravUsed = gravSta
if gravInput == 2:
    gravUsed = gravBolivia
if gravInput == 3:
    gravUsed = gravAvg
if gravInput == 4:
    gravUsed = gravPhilippines
if gravInput == 5:
    gravUsed = float(input("Please enter your own Gravity Value (in ms^-2): "))




print("")
print("Gravity Used: " + str(gravUsed))

print("")
print("Select Velocity Value")
print("Input 1 for Average Women's Pro Velocity")
print("Input 2 for Average Men's Pro Velocity")
print("Input 3 to input your own")

velInput = int(input("Enter Velocity Value: "))
if velInput == 1:
    velUsed = velLow
if velInput == 2:
    velUsed = velMed
if velInput == 4:
    velUsed = velHigh
if velInput == 3:
    velUsed = float(input("Please enter your own Velocity Value (in ms^-2): "))

print("")
print("Velocity Used: " + str(velUsed))


#print("")
#print("Select headwind or tailwind")
#print("Input 1 for headwind")
#print("Input 2 for tailwind")
#print("Input 3 for no wind")
#headWind = int(input("please select wind direction: "))


#if headWind != 3:
print("")
print("Select Wind Speed Value at Reference Height")
print("Input 1 for Saint Andrews")
print("Input 2 for Bolivia")
print("Input 3 for Philippines")
print("Input 4 to input your own")
windInput = int(input("Enter Wind Speed Value: "))
if windInput == 1:
    windUsed = windSta
if windInput == 2:
    windUsed = windBol
if windInput == 3:
    windUsed = windPhil
if windInput == 4:
    windUsed = float(input("Please enter your own Wind Speed Value (in m/s): "))


print("")
print("Wind Used: " + str(windUsed))

print("")
print("Select initial spin")
print("Input 1 for Average Pro Women's Spin")
print("Input 2 for Average Pro Men's Spin")
print("Input 3 to input your own")
spinPut = int(input("Enter Spin Value: "))
if spinPut == 1:
    spinUsd = AvgProWomSpin
if spinPut == 2:
    spinUsd = AvgProMenSpin
if spinPut == 3:
    spinUsd = float(input("Please enter your own Spin Speed Value (in RPM's): "))
else:
    spinUsd = AvgProWomSpin

print("")
print("Spin Used: " + str(spinUsd))
initSpin = spinUsd * (2*math.pi/60)

print("")
print("Select pressure")
print("Input 1 for Saint Andrews")
print("Input 2 for Bolivia")
print("Input 3 for Philippines")
print("Input 4 to input your own")
pinput = int(input("Enter pressure Value: "))

if pinput == 1:
    pressure = pressureSta
if pinput == 2:
    pressure = pressureBol
if pinput == 4:
    pressure = float(input("Please enter your own pressure (in pascals): "))
if pinput == 3:
    pressure = pressurePhil

print("")
print("Pressure Used: " + str(pressure))

print("")
print("Select Temp")
print("Input 1 for Saint Andrews")
print("Input 2 for Bolivia")
print("Input 3 for Philippines")
print("Input 4 to input your own")
tinput = int(input("Enter pressure Value: "))
tempC = 0
if tinput == 1:
    tempC = tempSta
if tinput == 2:
    tempC = tempBol
if tinput == 4:
    tempC = float(input("Please enter your own temp (in deg C): "))
if tinput == 3:
    tempC = tempPhil

print("")
print("Temp Used: " + str(tempC))

print("")
print("Select Humidity in %")
print("Input 1 for Saint Andrews")
print("Input 2 for Bolivia")
print("Input 3 for Philippines")
print("Input 4 to input your own")
hinput = int(input("Enter pressure Value: "))
if hinput == 1:
    relHum = humSta
if hinput == 2:
    relHum = humBol
if hinput == 4:
    relHum = float(input("Please enter your own humidity (in % eg 90 = 90%): "))
if hinput == 3:
    relHum = humPhil
print("")
print("Humidity Used: " + str(relHum) + "%")

#methods


def airDensity(temp, pressure, RelHumid):
    return ((gasConstWaterVap * pressure) + (6.122 * (gasConstAir - gasConstWaterVap)) *
            (RelHumid * math.exp((17.62*temp)/(243.12+temp)))) / (gasConstAir * gasConstWaterVap * (temp + 273.15))


def Cl(vel, time, initSpn):
    w = initSpn * (math.exp(-time / decayConstant))
    return (k * (ballRadius*1e-3) * w)/vel
def Cd(vel):
    if vel < 1e-2:
        vel = 1e-2
    return 46/(vel*yds2meters)

def findWindSPD(currentHeight, wind):
    if currentHeight <= Z0 or wind == 0:
        return 0
    try:
        if currentHeight < 1e-5:
            currentHeight = 1e-5
        return wind * ((math.log(currentHeight) - math.log(Z0)) /
                           (math.log(ZRef) - math.log(Z0)))
    except (ValueError, OverflowError):
        return 0

def Rd(vel, height, wind):
    if height > 1e-6:
        height = height
    else:
        height = 1e-6
    return 0.5 * Cd(vel) * airDensity(tempC, pressure, relHum) * ballArea * (abs((vel - findWindSPD(height, wind)) * (vel - findWindSPD(height, wind))))

def Rm(vel, height, time, initialspin, wind):
    if height > 1e-6:
        height = height
    else:
        height = 1e-6
    return 0.5 * Cl(vel, time, initialspin) * airDensity(tempC, pressure, relHum) * ballArea * (abs((vel - findWindSPD(height, wind))) * (vel - findWindSPD(height, wind)))


# noinspection DuplicatedCode
def testAngle(vel, grav, angle, wind, withLogging, distLogger, heightLogger):
    bounce = True
    currentHeight = float(0.0001)
    velX = vel*math.cos(angle)
    velY = vel*math.sin(angle)
    distX = 0.0
    distY = 0.0
    timeCurrent = 0
    timeIncrement = float(1/1000)
    i = 0
    #while currentHeight > 0.0:
    while currentHeight > 0:
        timeCurrent += timeIncrement
        distX += velX * timeIncrement
        distY += velY * timeIncrement
        currentHeight = distY

        velTot = math.sqrt((velX**2) + (velY**2))
        alpha = math.atan2(velY, velX)


        velX += (((1/ballMass) * (-Rd(velTot, currentHeight, wind) * math.cos(alpha) -
                                       Rm(velTot, currentHeight, timeCurrent, initSpin, wind)* math.sin(alpha))) * timeIncrement)

        velY += + ((((1/ballMass) * ((Rm(velTot, currentHeight, timeCurrent, initSpin, wind) * math.cos(alpha)) -
                                         (Rd(velTot, currentHeight, wind) * math.sin(alpha)))) - grav) * timeIncrement)

        #print(findWindSPD(currentHeight))
        if withLogging:
            distLogger.append(distX)
            heightLogger.append(distY)

        #print(i)

    while bounce:
        if abs(velY) < VminBounce:
            bounce = False
        elif -minTheta < atan2(velY, velX):
            bounce = False
        else:
            bounce = True

        distY = 0.0001
        currentHeight = distY
        dt = 0
        velX = velX - (meuK * (1 + newtonCoeff) * abs(velY))
        velY = velY * -newtonCoeff
        newSpinInit = (5 / (2 * ballRadius) * (meuK * (1 + newtonCoeff) * abs(velY)))
        while currentHeight > 0:
            dt += timeIncrement
            distX += velX * timeIncrement
            distY += velY * timeIncrement
            currentHeight = distY

            velTot = math.sqrt((velX ** 2) + (velY ** 2))
            alpha = math.atan2(velY, velX)

            velX += (((1 / ballMass) * (-Rd(velTot, currentHeight, wind) * math.cos(alpha) -
                                        Rm(velTot, currentHeight, timeCurrent, newSpinInit, wind) * math.sin(
                        alpha))) * timeIncrement)

            velY += + ((((1 / ballMass) * ((Rm(velTot, currentHeight, timeCurrent, newSpinInit, wind) * math.cos(alpha)) -
                                           (Rd(velTot, currentHeight, wind) * math.sin(alpha)))) - grav) * timeIncrement)
            if withLogging:
                distLogger.append(distX)
                heightLogger.append(distY)
    return distX

print("")
anglesTailwind = []
rangesTailwind = []
anglesHeadwind = []
rangesHeadwind = []
anglesNoWind = []
rangesNoWind = []
distLog1 = []
heightLog1 = []
distLog2 = []
heightLog2 = []
distLog3 = []
heightLog3 = []
#tests angles between 0-90 deg in steps determined by the number of iterations
iterations = 100
for i in range(iterations):
    angle = i*(90/iterations)
    anglesTailwind.append(angle)
    rangesTailwind.append(testAngle(velUsed, gravUsed, math.radians(angle),windUsed,False, None , None))


for i in range(iterations):
    angle = i*(90/iterations)
    anglesHeadwind.append(angle)
    rangesHeadwind.append(testAngle(velUsed, gravUsed, math.radians(angle), -windUsed,False, None , None))


for i in range(iterations):
    angle = i*(90/iterations)
    anglesNoWind.append(angle)
    rangesNoWind.append(testAngle(velUsed, gravUsed, math.radians(angle),0, False, None , None))


plt.plot(anglesTailwind, rangesTailwind)
plt.plot(anglesHeadwind, rangesHeadwind)
plt.plot(anglesNoWind, rangesNoWind)
plt.ylabel("Distance (m)")
plt.xlabel("Angle (degrees)")
plt.show()


tailArr = np.array(rangesTailwind)
tailAngleIndex = np.where(tailArr == max(tailArr))

headArr = np.array(rangesHeadwind)
headAngleIndex = np.where(headArr == max(headArr))

noArr = np.array(rangesNoWind)
noAngleIndex = np.where(noArr == max(noArr))


print("Maximum distance found by brute force for tailwind: " + str(tailArr.max()))
print("Found at an angle of " + str(anglesTailwind[tailAngleIndex[0][0]]) + " degrees")
print("")
print("Maximum distance found by brute force for headwind: " + str(headArr.max()))
print("Found at an angle of " + str(anglesHeadwind[headAngleIndex[0][0]]) + " degrees")
print("")
print("Maximum distance found by brute force for no wind: " + str(noArr.max()))
print("Found at an angle of " + str(anglesNoWind[noAngleIndex[0][0]]) + " degrees")

print("")
#print("trajectory at ", anglesTailwind[angleIndex[0][0]], " degrees as shown below")
print("trajectories as shown below")


testAngle(velUsed, gravUsed, math.radians(anglesTailwind[tailAngleIndex[0][0]]), windUsed,True, distLog1, heightLog1)
testAngle(velUsed, gravUsed, math.radians(anglesTailwind[headAngleIndex[0][0]]), -windUsed, True, distLog2, heightLog2)
testAngle(velUsed, gravUsed, math.radians(anglesTailwind[noAngleIndex[0][0]]),0, True, distLog3, heightLog3)


plt.plot(distLog1, heightLog1)
plt.plot(distLog2, heightLog2)
plt.plot(distLog3, heightLog3)
plt.xlabel("Distance (m)")
plt.ylabel("Height (m)")
plt.show()