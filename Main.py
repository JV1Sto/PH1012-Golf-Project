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


print("")
print("Select headwind or tailwind")
print("Input 1 for headwind")
print("Input 2 for tailwind")
print("Input 3 for no wind")
headWind = int(input("please select wind direction: "))


if headWind != 3:
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

if headWind == 1:
    windUsed = -windUsed
if headWind == 2:
    windUsed = windUsed
if headWind == 3:
    windUsed = 0
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

def findWindSPD(currentHeight):
    if currentHeight <= Z0 or windUsed == 0:
        return 0
    try:
        if currentHeight < 1e-5:
            currentHeight = 1e-5
        return windUsed * ((math.log(currentHeight) - math.log(Z0)) /
                           (math.log(ZRef) - math.log(Z0)))
    except (ValueError, OverflowError):
        return 0

def Rd(vel, height):
    if height > 1e-6:
        height = height
    else:
        height = 1e-6
    return 0.5 * Cd(vel) * airDensity(tempC, pressure, relHum) * ballArea * (abs((vel - findWindSPD(height)) * (vel - findWindSPD(height))))

def Rm(vel, height, time, initialspin):
    if height > 1e-6:
        height = height
    else:
        height = 1e-6
    return 0.5 * Cl(vel, time, initialspin) * airDensity(tempC, pressure, relHum) * ballArea * (abs((vel - findWindSPD(height))) * (vel - findWindSPD(height)))

distLog = []
heightLog = []
# noinspection DuplicatedCode
def testAngle(vel, grav, angle, withLogging):
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


        velX += (((1/ballMass) * (-Rd(velTot, currentHeight) * math.cos(alpha) -
                                       Rm(velTot, currentHeight, timeCurrent, initSpin)* math.sin(alpha))) * timeIncrement)

        velY += + ((((1/ballMass) * ((Rm(velTot, currentHeight, timeCurrent, initSpin) * math.cos(alpha)) -
                                         (Rd(velTot, currentHeight) * math.sin(alpha)))) - grav) * timeIncrement)

        #print(findWindSPD(currentHeight))
        if withLogging:
            distLog.append(distX)
            heightLog.append(distY)

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

            velX += (((1 / ballMass) * (-Rd(velTot, currentHeight) * math.cos(alpha) -
                                        Rm(velTot, currentHeight, timeCurrent, newSpinInit) * math.sin(
                        alpha))) * timeIncrement)

            velY += + ((((1 / ballMass) * ((Rm(velTot, currentHeight, timeCurrent, newSpinInit) * math.cos(alpha)) -
                                           (Rd(velTot, currentHeight) * math.sin(alpha)))) - grav) * timeIncrement)
            if withLogging:
                distLog.append(distX)
                heightLog.append(distY)
    return distX

print("")
angles = []
distances = []

#tests angles between 0-90 deg in steps determined by the number of iterations
iterations = 1000
for i in range(iterations):
    angle = i*(90/iterations)
    angles.append(angle)
    distances.append(testAngle(velUsed, gravUsed, math.radians(angle), False))
print(distances)

#currently a placeholder plot, we can do a lot more with these
#but currently the plot isn't particularly interesting
plt.plot(angles, distances)
plt.ylabel("Distance (m)")
plt.xlabel("Angle (degrees)")
plt.show()


distArr = np.array(distances)
angleIndex = np.where(distArr == max(distArr))

print("Maximum found by brute force: " + str(distArr.max()))
print("Found at an angle of " + str(angles[angleIndex[0][0]]) + " degrees")


print("")
print("trajectory at ", angles[angleIndex[0][0]], " degrees as shown below")

testAngle(velUsed, gravUsed, math.radians(angles[angleIndex[0][0]]), True)

plt.plot(distLog, heightLog)
plt.show()