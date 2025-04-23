#imports
import math
from math import atan2
import numpy as np
import numpy.polynomial.polynomial as npp
import matplotlib.pyplot as plt

#constants
tempC = 15
relHum = 90
pressure = 100900
gasConstWaterVap = 461.5
gasConstAir = 287.05
ballMass = 0.0464
ballRadius = 21.4
ballArea = (ballRadius*10**-3)**2 * math.pi
ZRef = 10
Z0 = 0.4


#gravity values in ms^-2
gravSta = 9.81618225
gravBolivia = 9.774220451
gravPhilippines = 9.782893875
gravAvg = 9.81
gravUsed = 0

#velocity values in ms^-1
velLow = 60
velMed = 70
velHigh = 80
velUsed = 0


windLo = 1
windMed = 4
windHi = 8
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
print("Input 1 for 40 ms^-1")
print("Input 2 for 60 ms^-1")
print("Input 3 for 75 ms^-1")
print("Input 4 to input your own")

velInput = int(input("Enter Velocity Value: "))
if velInput == 1:
    velUsed = velLow
if velInput == 2:
    velUsed = velMed
if velInput == 3:
    velUsed = velHigh
if velInput == 4:
    velUsed = float(input("Please enter your own Velocity Value (in ms^-2): "))

print("")
print("Velocity Used: " + str(velUsed))

print("")
print("Select Wind Speed Value at Reference Height")
print("Input 1 for 10 m/s")
print("Input 2 for 20 m/s")
print("Input 3 for 30 m/s")
print("Input 4 to input your own")
windInput = int(input("Enter Wind Speed Value: "))
if windInput == 1:
    windUsed = windLo
if windInput == 2:
    windUsed = windMed
if windInput == 3:
    windUsed = windHi
if windInput == 4:
    windUsed = float(input("Please enter your own Wind Speed Value (in m/s): "))


print("")
print("Select initial spin")
print("Input 1 for Average Pro Women's Spin")
print("Input 2 for Average Pro Men's Spin")
print("Input 3 to input your own")
spinPut = int(input("Enter Wind Spin Value in RPM's: "))
if spinPut == 1:
    spinUsd = AvgProWomSpin
if spinPut == 2:
    spinUsd = AvgProMenSpin
if spinPut == 3:
    spinUsd = float(input("Please enter your own Spin Speed Value (in RPM's): "))
else:
    spinUsd = AvgProWomSpin

initSpin = spinUsd * (2*math.pi/60)

#methods

#currently also a placeholder
#uses the most basic form of projectile motion
#will be updated when more research has been done

#k is a constant for dimpled balls
k = 0.5

yds2meters = 3.281


decayConstant = 24.5

newtonCoeff = 0.7
mewK = 0.04
VminBounce = 0.4
minTheta = math.radians(10)

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


# noinspection DuplicatedCode
def testAngle(vel, grav, angle):
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
        velX = velX - (mewK * (1 + newtonCoeff) * abs(velY))
        velY = velY * -newtonCoeff
        newSpinInit = (5 / (2 * ballRadius) * (mewK * (1 + newtonCoeff) * abs(velY)))
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
    return distX

print("")
angles = []
distances = []

#tests angles between 0-90 deg in steps determined by the number of iterations
iterations = 100
for i in range(iterations):
    angle = i*(90/iterations)
    angles.append(angle)
    distances.append(testAngle(velUsed, gravUsed, math.radians(angle)))
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
#best fit line code
#currently also a placeholder
#I believe there's a way to get the code to determine the degree
#but for now I've entered it manually

#currently work in progress and does not function
fitLn = npp.polyfit(angles, distances, 2)
fitArr = np.array(fitLn)
poly = np.polynomial.polynomial.Polynomial(fitArr)
print("Best fit equation found: " + str(poly))
print("Best angle found by best fit: " + str(poly.deriv().roots()))
print("Distance at above angle according to best fit: " + str(poly(poly.deriv().roots())))