#imports
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#constants

#gravity values in ms^-2
gravSta = 0
gravBolivia = 0
gravAvg = 9.80665
#currently placeholders
gravUsed = 0

#velocity values in ms^-1
velLow = 45
velMed = 60
velHigh = 75
#also currently placeholders, but values found online
velUsed = 0

print("Select Gravity Value")
print("Input 1 for St Andrews")
print("Input 2 for Bolivia")
print("Input 3 for Average")
print("Input 4 to input your own")


gravInput = int(input("Enter Gravity Value: "))
if gravInput == 1:
    gravUsed = gravSta
if gravInput == 2:
    gravUsed = gravBolivia
if gravInput == 3:
    gravUsed = gravAvg
if gravInput == 4:
    gravUsed = input("Please enter your own Gravity Value (in ms^-2): ")


#methods

#currently also a placeholder
#uses the most basic form of projectile motion
#will be updated when more research has been done
def testAngle(vel, grav, angle):
    return (vel**2 * math.sin(2 * angle))/grav



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
    velUsed = input("Please enter your own Velocity Value (in ms^-2): ")

print("")
print("Velocity Used: " + str(velUsed))

print("")
print(testAngle(velUsed, gravUsed, 45))

for i in range(500):
    print(i)




