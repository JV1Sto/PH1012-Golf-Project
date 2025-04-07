#imports
import math

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


#methods

#currently also a placeholder
#uses the most basic form of projectile motion
#will be updated when more research has been done
def testAngle(vel, grav, angle):
    return (vel**2 * math.sin(2 * angle))/grav


print("")
angles = []
distances = []

#tests angles between 0-90 deg in steps determined by the number of iterations
iterations = 10000
for i in range(iterations):
    angle = i*(90/iterations)
    angles.append(angle)
    distances.append(testAngle(velUsed, gravUsed, math.radians(angle)))


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