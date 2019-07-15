#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 08:43:13 2019

@author: karadowling
"""

class Ship():
  def __init__(self, shipName, loc, offensiveMissileTotal, defensiveMissileTotal):
    self.name = shipName
    self.hit = False #ship hit by missile
    #best known location of destroyer in 1D scale (to compare to other ship)
    self.loc = loc 
    self.omf = 0 #offensive missiles already fired (start with 0)
    #offensive missiles left in ship's arsenal (typically start with 20)
    self.oml = offensiveMissileTotal - self.omf 
    self.dmf = 0 #defensive missiles left in ship's arsenal (start with 0)
    #defensive missiles left in ship's arsenal ( typically start with 60)
    self.dml = defensiveMissileTotal - self.dmf 
   
  #print current information about instance of Ship
  def printShip(self):
    print(self.name + ":")
    if self.hit == True :
        print("The ship has been hit!!")
    else:
        print("Ship has not been hit")
    print("Current best known location is " + str(self.loc) + " on the 1D scale")
    print(str(self.omf) + " offensive missiles already fired")
    print(str(self.oml) + " offensive missiles left in ship's arsenal") 
    print(str(self.dmf) + " defensive missiles already fired")
    print(str(self.dml) + " defensive missiles left in ship's arsenal") 
    print('')
    
#test = Ship("Test Ship", 0, 20, 60)
#test.printShip()