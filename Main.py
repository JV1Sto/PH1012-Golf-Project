#imports
import math
from math import atan2
from time import thread_time, sleep

import numpy
import numpy as np
import numpy.polynomial.polynomial as npp
import pandas as pd
import matplotlib.pyplot as plt

#constants

#gravity values in ms^-2
gravSta = 9.81
gravBolivia = 9.81
gravPhilippines = 9.81
gravAvg = 9.80665
#currently placeholders
gravUsed = 0

#velocity values in ms^-1
velLow = 45
velMed = 60
velHigh = 75
#also currently placeholders, but these are seemingly reasonable values found online
velUsed = 0


windHi = 30
windMed = 20
windLo = 10
windUsed = 0


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

initSpin = 5000 * (2*math.pi/60)
densityUsed = 1.007
ballMass = 0.0464
#methods

#currently also a placeholder
#uses the most basic form of projectile motion
#will be updated when more research has been done
ballRadius = 21.4
ballArea = (ballRadius*10**-3)**2 * math.pi
ZRef = 10
Z0 = 0.4
#k is a constant for dimpled balls
k = 0.5

yds2meters = 3.281


decayConstant = 24.5

def Cl(vel, time):
    w = initSpin * (math.e ** (-time / decayConstant))
    return (k * (ballRadius*10**-3) * w)/vel
def Cd(vel):
    return 46/(vel*yds2meters)

def findWindSPD(currentHeight):
    if currentHeight < Z0:
        return 0
    return windUsed*((math.log(currentHeight)-math.log(Z0))/(math.log(ZRef)-math.log(Z0)))

def Rd(vel, height):
    return 0.5 * Cd(vel) * densityUsed * ballArea * (abs((vel - findWindSPD(height)) * (vel - findWindSPD(height))))

def Rm(vel, height, time):
    return 0.5 * Cl(vel, time) * densityUsed * ballArea * (abs((vel - findWindSPD(height))) * (vel - findWindSPD(height)))
dist1 = []

def testAngle(vel, grav, angle):
    currentHeight = float(0.0001)
    velX = vel*math.cos(angle)
    velY = vel*math.sin(angle)
    distX = 0.0
    distY = 0.0
    timeCurrent = 0.0
    timePrevious = 0.0
    timeIncrement = float(1/1000)
    i = 0
    #while currentHeight > 0.0:
    while currentHeight > 0:
        i += 1
        #print("vel y ", velY)
        #print("dist y ", distY)
        timeCurrent = timeCurrent + timeIncrement
        distX += velX * (timeCurrent - timePrevious)
        distY += velY * (timeCurrent - timePrevious)
        #print(distY + (velY * (timeCurrent - timePrevious)))
        currentHeight = distY
        velTot = math.sqrt((velX**2) + (velY**2))
        alpha = math.atan2(velY, velX)
        #print("dist y ", distY)

        #print("")




        velX = velX + (((1/ballMass) * (Rd(velTot, currentHeight) * math.cos(alpha) -
                                       Rm(velTot, currentHeight, timeCurrent)* math.sin(alpha)))* (timeIncrement))

        velY = velY + ((((1/ballMass) * ((Rm(velTot, currentHeight, timeCurrent) * math.cos(alpha)) -
                                         (Rd(velTot, currentHeight) * math.sin(alpha)))) - grav) * (timeIncrement))


        timePrevious = timeCurrent

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
print(dist1)
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