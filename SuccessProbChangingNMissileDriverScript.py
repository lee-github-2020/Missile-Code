#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 11:14:19 2019

@author: karadowling
code adapted from ORF 411 AssetSelling problem code found at link below
https://github.com/wbpowell328/stochastic-optimization/tree/master/AssetSelling

This script runs multiple iterations of a two-agent surface ship missile engagement and changes
the offensive missile success probability over sets of iterations.  
Each simulation starts with one or both of the ships firing offensive missiles and ends when 
either ship is hit by a missle or both ships are out of missiles.
"""

#from collections import namedtuple
import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.ticker as ticker
import numpy as np
#from matplotlib.ticker import MaxNLocator
#from copy import copy
#import math
from Ship import Ship

if __name__ == "__main__":
    #read in policy parameters from an Excel spreadsheet, "missile_policy_parameters.xlsx"
    sheet1 = pd.read_excel("missile_policy_parameters.xlsx", sheet_name="Sheet1")
    sheet2 = pd.read_excel("missile_policy_parameters.xlsx", sheet_name="Sheet2")
    
    #state variables


    #time step for each iteration of "game" in minuntes
    timeStep = sheet2['Time Step (minutes)'][0]
    #print("Time step each iteration is " + str(timeStep) + " minutes")
    #print('')
    
    iterations = sheet2['Iterations of Simulation'][0]
    print("Simulation Iterations: " + str(iterations) + "\n")
    
    #initial data blueShip
    initialBlue = [sheet1['Ship\'s Name'][0], sheet1['Location (NM) 1D scale'][0], 
                sheet1['Offensive Missiles'][0], sheet1['Defensive Missiles'][0],
                sheet1['ESSMs'][0], sheet1['SeaRAMs'][0], 
                sheet1['CIWS (each has 1500 rounds)'][0],
                sheet1['Ship Speed (kn)'][0], sheet1['Missile Speed (kn)'][0], 
                timeStep, sheet1['Offensive Missile Range (NM)'][0], 
                sheet1['Offensive Missile Success Probability'][0],
                sheet1['Defensive Missile Success Probability (if target offensive missile is 100-20 NM from its target - phase 1)'][0],
                sheet1['Defensive Missile Success Probability (if target offensive missile is 20-5 NM from its target - phase 2)'][0],
                sheet1['Defensive Missile Success Probability (if target offensive missile is 5-1 NM from its target - phase 3)'][0],
                sheet1['ESSM Success Probability'][0],
                sheet1['SeaRAM Success Probability'][0],
                sheet1['CIWS Success Probability'][0],
                sheet1['Offensive Missile Salvo Size'][0],
                sheet1['Defensive Missile Salvo Size'][0],
                sheet1['ESSM Salvo Size'][0],
                sheet1['SeaRAM Salvo Size'][0],
                sheet1['CIWS Iteration Salvo Size'][0],
                sheet1['Satellite'][0], sheet1['Radar'][0], 
                sheet1['Electronic Surveillance'][0], 
                sheet1['Passive Sensors (Acoustic)'][0],
                sheet1['UAV'][0], sheet1['USV'][0]]
    
    initialRed = [sheet1['Ship\'s Name'][1], sheet1['Location (NM) 1D scale'][1], 
                sheet1['Offensive Missiles'][1], sheet1['Defensive Missiles'][1], 
                sheet1['ESSMs'][1], sheet1['SeaRAMs'][1], 
                sheet1['CIWS (each has 1500 rounds)'][1],
                sheet1['Ship Speed (kn)'][1], sheet1['Missile Speed (kn)'][1], 
                timeStep, sheet1['Offensive Missile Range (NM)'][1], 
                sheet1['Offensive Missile Success Probability'][1],
                sheet1['Defensive Missile Success Probability (if target offensive missile is 100-20 NM from its target - phase 1)'][1],
                sheet1['Defensive Missile Success Probability (if target offensive missile is 20-5 NM from its target - phase 2)'][1],
                sheet1['Defensive Missile Success Probability (if target offensive missile is 5-1 NM from its target - phase 3)'][1],
                sheet1['ESSM Success Probability'][1],
                sheet1['SeaRAM Success Probability'][1],
                sheet1['CIWS Success Probability'][1],
                sheet1['Offensive Missile Salvo Size'][1],
                sheet1['Defensive Missile Salvo Size'][1],
                sheet1['ESSM Salvo Size'][1],
                sheet1['SeaRAM Salvo Size'][1],
                sheet1['CIWS Iteration Salvo Size'][1],
                sheet1['Satellite'][1], sheet1['Radar'][1], 
                sheet1['Electronic Surveillance'][1], 
                sheet1['Passive Sensors (Acoustic)'][1],
                sheet1['UAV'][1 ], sheet1['USV'][1]]
    
    offensiveMissileSuccessProbability = [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1]
    
    BlueShipHitNumberArr = []
    BlueShipHitPropArr = []
    RedShipHitNumberArr = []
    RedShipHitPropArr = []
    BothShipHitNumberArr = []
    NoShipHitNumberArr = []
    BothShipHitPropArr = []
    NoShipHitPropArr = []
    
    AvgBlueOMFArr = []
    StdDevBlueOMFArr = []
    AvgRedOMFArr = []
    StdDevRedOMFArr = []
    
    AvgBlueDMFArr = []
    StdDevBlueDMFArr = []
    AvgRedDMFArr = []
    StdDevRedDMFArr = []
    
    AvgBlueEMFArr = []
    StdDevBlueEMFArr = []
    AvgRedEMFArr = []
    StdDevRedEMFArr = []
    
    AvgBlueSMFArr = []
    StdDevBlueSMFArr = []
    AvgRedSMFArr = []
    StdDevRedSMFArr = []
    
    AvgBlueCMFArr = []
    StdDevBlueCMFArr = []
    AvgRedCMFArr = []
    StdDevRedCMFArr = []
    
    AvgBlueOMRArr = []
    AvgRedOMRArr = []
    AvgRangeArr = []
    StdDevRangeArr = []
    
    AvgBlueCostArr = []
    StdDevBlueCostArr = []
    AvgRedCostArr = []
    StdDevRedCostArr = []
    
    AvgBlueMissileCostArr = []
    StdDevBlueMissileCostArr = []
    AvgRedMissileCostArr = []
    StdDevRedMissileCostArr = []
    
    
    for offSucc in offensiveMissileSuccessProbability:
       
    
    
        #Create Plot List for Missile Count Over Time
        iterationArray = [] 
        simulationTimeArray = []
        BlueNumberOffensiveMissiles = []
        BlueNumberDefensiveMissiles = []
        BlueNumberESSMs = []
        BlueNumberSeaRAMs = []
        BlueNumberCIWS = []
        BlueShipOffensiveMissileRange = []
        BlueShipHit = []
        BlueShipCost = []
        BlueMissileCost = []
        RedNumberOffensiveMissiles = []
        RedNumberDefensiveMissiles = []
        RedNumberESSMs = []
        RedNumberSeaRAMs = []
        RedNumberCIWS = []
        RedShipOffensiveMissileRange = []
        RedShipHit = []
        RedShipCost = []
        RedMissileCost = []
        ShipRange = []
        
        blueShip = Ship(initialBlue[0], initialBlue[1], 
                        initialBlue[2], initialBlue[3],
                        initialBlue[4], initialBlue[5], 
                        initialBlue[6],
                        initialBlue[7], initialBlue[8], 
                        initialBlue[9], initialBlue[10], 
                        offSucc,
                        initialBlue[12],
                        initialBlue[13],
                        initialBlue[14],
                        initialBlue[15],
                        initialBlue[16],
                        initialBlue[17],
                        initialBlue[18],
                        initialBlue[19],
                        initialBlue[20],
                        initialBlue[21],
                        initialBlue[22],
                        initialBlue[23], initialBlue[24], 
                        initialBlue[25], 
                        initialBlue[26],
                        initialBlue[27], initialBlue[28])
        redShip = Ship(initialRed[0], initialRed[1], 
                        initialRed[2], initialRed[3],
                        initialRed[4], initialRed[5], 
                        initialRed[6],
                        initialRed[7], initialRed[8], 
                        initialRed[9], initialRed[10], 
                        initialRed[11],
                        initialRed[12],
                        initialRed[13],
                        initialRed[14],
                        initialRed[15],
                        initialRed[16],
                        initialRed[17],
                        initialRed[18],
                        initialRed[19],
                        initialRed[20],
                        initialRed[21],
                        initialRed[22],
                        initialRed[23], initialRed[24], 
                        initialRed[25], 
                        initialRed[26],
                        initialRed[27], initialRed[28])
        print("Initial Ship Inputs")
        blueShip.printShipInputs(redShip)
    
        
        for i in range(iterations):
        
            #Initialize Ships
            blueShip = Ship(initialBlue[0], initialBlue[1], 
                            initialBlue[2], initialBlue[3],
                            initialBlue[4], initialBlue[5], 
                            initialBlue[6],
                            initialBlue[7], initialBlue[8], 
                            initialBlue[9], initialBlue[10], 
                            offSucc,
                            initialBlue[12],
                            initialBlue[13],
                            initialBlue[14],
                            initialBlue[15],
                            initialBlue[16],
                            initialBlue[17],
                            initialBlue[18],
                            initialBlue[19],
                            initialBlue[20],
                            initialBlue[21],
                            initialBlue[22],
                            initialBlue[23], initialBlue[24], 
                            initialBlue[25], 
                            initialBlue[26],
                            initialBlue[27], initialBlue[28])
            redShip = Ship(initialRed[0], initialRed[1], 
                            initialRed[2], initialRed[3],
                            initialRed[4], initialRed[5], 
                            initialRed[6],
                            initialRed[7], initialRed[8], 
                            initialRed[9], initialRed[10], 
                            initialRed[11],
                            initialRed[12],
                            initialRed[13],
                            initialRed[14],
                            initialRed[15],
                            initialRed[16],
                            initialRed[17],
                            initialRed[18],
                            initialRed[19],
                            initialRed[20],
                            initialRed[21],
                            initialRed[22],
                            initialRed[23], initialRed[24], 
                            initialRed[25], 
                            initialRed[26],
                            initialRed[27], initialRed[28])
            
            #Print Initialized Ships
            #redShip.printShip()
            #blueShip.printShip()
           
            #not incorporated yet
            #Weather affects scouting effectiveness
            goodWeather = False #bad weather (True is good weather)
            
            
            #Run Missile Simulation
            #keeps track of iterations that are representative of minutes
            simulationTime = 0.25 #in minutes
            #simulation ends when certain time passes to ensure no infinite loop can occur
            animationFile = open("animationFile.txt", "w")
            while(simulationTime <= 1000):
                
                #determines whether Blue or Red goes first each time step
                BlueFirst = np.random.binomial(1,0.5)
                #print(BlueFirst)

                if (BlueFirst == 1):
                    #checking for exit conditions
                    #stop simulation if either ship is hit
                    if(redShip.hit or blueShip.hit):
                        break
                    #stop simulation if both ships are out of ammunition(missiles)
                    if(redShip.outOfMissiles() and blueShip.outOfMissiles()):
                        break 
                    #if(redShip.offensiveMissileTotal - redShip.omf <= 0):
                        #break
                    #move ships if they are out of range
                    blueShip.moveShip(redShip, animationFile, simulationTime)
                    redShip.moveShip(blueShip, animationFile, simulationTime)
                    
                    #determine if there are target ships or missiles for the ships
                    blueShip.findShipTargets(redShip)
                    blueShip.findMissileTargets(redShip)
                    redShip.findShipTargets(blueShip)
                    redShip.findMissileTargets(blueShip)
                
                    #check if any flying missiles have hit their targets
                    blueShip.checkHitTargets(animationFile, simulationTime)
                    redShip.checkHitTargets(animationFile, simulationTime)
                    
        
                    #move all flying missiles forward to next state according to time and speed
                    blueShip.moveAllMissiles()
                    redShip.moveAllMissiles()
                   
                    
                    #increment the simulation time
                    simulationTime = simulationTime + 0.25
                
                else:
                    #checking for exit conditions
                    #stop simulation if either ship is hit
                    if(redShip.hit or blueShip.hit):
                        break
                    #stop simulation if both ships are out of ammunition(missiles)
                    if(redShip.outOfMissiles() and blueShip.outOfMissiles()):
                        break 
                    #if(redShip.offensiveMissileTotal - redShip.omf <= 0):
                        #break
                    #move ships if they are out of range
                    redShip.moveShip(blueShip, animationFile, simulationTime)
                    blueShip.moveShip(redShip, animationFile, simulationTime)
                    
                    #determine if there are target ships or missiles for the ships
                    redShip.findShipTargets(blueShip)
                    redShip.findMissileTargets(blueShip)
                    blueShip.findShipTargets(redShip)
                    blueShip.findMissileTargets(redShip)
                
                    #check if any flying missiles have hit their targets
                    redShip.checkHitTargets(animationFile, simulationTime)
                    blueShip.checkHitTargets(animationFile, simulationTime)
        
                    #move all flying missiles forward to next state according to time and speed
                    redShip.moveAllMissiles()
                    blueShip.moveAllMissiles()
                    
                    #increment the simulation time
                    simulationTime = simulationTime + 0.25
                    
                
            animationFile.close()
            #print("Iteration: " + str(i + 1))
            #print()
            #blueShip.printShip()
            #redShip.printShip()
            #if(redShip.outOfMissiles() and blueShip.outOfMissiles()):
                #print("Both ships out of missiles")
                #print()
            iterationArray.append(i)
            simulationTimeArray.append(simulationTime)
            BlueNumberOffensiveMissiles.append(blueShip.omf)
            BlueNumberDefensiveMissiles.append(blueShip.dmf)
            BlueNumberESSMs.append(blueShip.essmf)
            BlueNumberSeaRAMs.append(blueShip.seaRamf)
            BlueNumberCIWS.append(blueShip.ciwsf)
            BlueShipOffensiveMissileRange.append(blueShip.offensiveMissileRange)
            BlueShipHit.append(blueShip.hit)
            BlueShipCost.append(blueShip.engagementCost())
            BlueMissileCost.append(blueShip.missileCost())
            RedNumberOffensiveMissiles.append(redShip.omf)
            RedNumberDefensiveMissiles.append(redShip.dmf)
            RedNumberESSMs.append(redShip.essmf)
            RedNumberSeaRAMs.append(redShip.seaRamf)
            RedNumberCIWS.append(redShip.ciwsf)
            RedShipOffensiveMissileRange.append(redShip.offensiveMissileRange)
            RedShipHit.append(redShip.hit)
            RedShipCost.append(redShip.engagementCost())
            RedMissileCost.append(redShip.missileCost())
            ShipRange.append(abs(blueShip.loc-redShip.loc))
            
        #Number of simulation runs Blue Ship Hit
        BlueShipHitNumber = BlueShipHit.count(True)
        BlueShipHitNumberArr.append(BlueShipHitNumber)

        #Proportion of total simulation runs that blue ship is hit (loses)
        BlueShipHitProp = BlueShipHitNumber/len(BlueShipHit)
        BlueShipHitPropArr.append(BlueShipHitProp)
        
        #Number of simulation runs Blue Ship Hit
        RedShipHitNumber = RedShipHit.count(True)
        RedShipHitNumberArr.append(RedShipHitNumber)
        
        #Proportion of total simulation runs that red ship is hit (loses)
        RedShipHitProp = RedShipHitNumber/len(RedShipHit)
        RedShipHitPropArr.append(RedShipHitProp)
        
        BothShipHitNumber = 0
        NoShipHitNumber = 0
        for s in range(len(RedShipHit)):
            if(RedShipHit[s] == True and BlueShipHit[s] == True):
                BothShipHitNumber = BothShipHitNumber + 1
            if(RedShipHit[s] == False and BlueShipHit[s] == False):
                NoShipHitNumber = NoShipHitNumber + 1
        BothShipHitNumberArr.append(BothShipHitNumber)
        NoShipHitNumberArr.append(NoShipHitNumber)
            
        BothShipHitProp = BothShipHitNumber/len(RedShipHit)
        BothShipHitPropArr.append(BothShipHitProp)
        NoShipHitProp = NoShipHitNumber/len(RedShipHit)
        NoShipHitPropArr.append(NoShipHitProp)
        
        AvgBlueOMFArr.append(np.mean(BlueNumberOffensiveMissiles))
        StdDevBlueOMFArr.append(np.sqrt(np.var(BlueNumberOffensiveMissiles)))
        AvgRedOMFArr.append(np.mean(RedNumberOffensiveMissiles))
        StdDevRedOMFArr.append(np.sqrt(np.var(RedNumberOffensiveMissiles)))
        
        AvgBlueDMFArr.append(np.mean(BlueNumberDefensiveMissiles))
        StdDevBlueDMFArr.append(np.sqrt(np.var(BlueNumberDefensiveMissiles)))
        AvgRedDMFArr.append(np.mean(RedNumberDefensiveMissiles))
        StdDevRedDMFArr.append(np.sqrt(np.var(RedNumberDefensiveMissiles)))
        
        AvgBlueEMFArr.append(np.mean(BlueNumberESSMs))
        StdDevBlueEMFArr.append(np.sqrt(np.var(BlueNumberESSMs)))
        AvgRedEMFArr.append(np.mean(RedNumberESSMs))
        StdDevRedEMFArr.append(np.sqrt(np.var(RedNumberESSMs)))
        
        AvgBlueSMFArr.append(np.mean(BlueNumberSeaRAMs))
        StdDevBlueSMFArr.append(np.sqrt(np.var(BlueNumberSeaRAMs)))
        AvgRedSMFArr.append(np.mean(RedNumberSeaRAMs))
        StdDevRedSMFArr.append(np.sqrt(np.var(RedNumberSeaRAMs)))
        
        AvgBlueCMFArr.append(np.mean(BlueNumberCIWS))
        StdDevBlueCMFArr.append(np.sqrt(np.var(BlueNumberCIWS)))
        AvgRedCMFArr.append(np.mean(RedNumberCIWS))
        StdDevRedCMFArr.append(np.sqrt(np.var(RedNumberCIWS)))
        
        AvgBlueOMRArr.append(blueShip.offensiveMissileRange)
        AvgRedOMRArr.append(redShip.offensiveMissileRange)
        AvgRangeArr.append(np.mean(ShipRange))
        StdDevRangeArr.append(np.sqrt(np.var(ShipRange)))
        
        AvgBlueCostArr.append(np.mean(BlueShipCost))
        StdDevBlueCostArr.append(np.sqrt(np.var(BlueShipCost)))
        AvgRedCostArr.append(np.mean(RedShipCost))
        StdDevRedCostArr.append(np.sqrt(np.var(RedShipCost)))
        
        AvgBlueMissileCostArr.append(np.mean(BlueMissileCost))
        StdDevBlueMissileCostArr.append(np.var(BlueMissileCost))
        AvgRedMissileCostArr.append(np.mean(RedMissileCost))
        StdDevRedMissileCostArr.append(np.var(RedMissileCost))
       
        
    #Graph of Proportion of Iterations Ship Hit
    plt.plot(offensiveMissileSuccessProbability, BlueShipHitPropArr, color='blue', label='Blue')
    plt.plot(offensiveMissileSuccessProbability, RedShipHitPropArr, color='red', label='Red')
    plt.plot(offensiveMissileSuccessProbability, BothShipHitPropArr, color='black', label='Both')
    plt.plot(offensiveMissileSuccessProbability, NoShipHitPropArr, color='green', label='Neither')
    plt.legend()
    offMSPString = ['0', '1/10', '2/10', '3/10', '4/10', '5/10', '6/10', '7/10', '8/10', '9/10', '1']
    plt.xticks(offensiveMissileSuccessProbability, offMSPString)
    plt.xlabel('Blue Offensive Missile Success Probability')
    plt.ylabel('Proportion of Iterations Ship Hit')
    plt.title('Proportion of Iterations Ship Hit\nwhen Changing Blue Offensive Missile Success Probability\n(Red Offensive Missile Success Probability Set at 0.9)')
    plt.savefig('ProportionShipHitChangingBlueProb.png', dpi=600, bbox_inches='tight')
    plt.show()
    
    
    #Graph of Number of Iterations Ship Hit
    plt.plot(offensiveMissileSuccessProbability, BlueShipHitNumberArr, color='blue', label='Blue')
    plt.plot(offensiveMissileSuccessProbability, RedShipHitNumberArr, color='red', label='Red')
    plt.plot(offensiveMissileSuccessProbability, BothShipHitNumberArr, color='black', label='Both')
    plt.plot(offensiveMissileSuccessProbability, NoShipHitNumberArr, color='green', label='Neither')
    plt.legend()
    offMSPString = ['0', '1/10', '2/10', '3/10', '4/10', '5/10', '6/10', '7/10', '8/10', '9/10', '1']
    plt.xticks(offensiveMissileSuccessProbability, offMSPString)
    plt.xlabel('Blue Offensive Missile Success Probability')
    plt.ylabel('Average Number of Iterations Ship Hit')
    plt.title('Average Number of Iterations Ship Hit of ' + str(iterations) + ' total Iterations\nwhen Changing Blue Offensive Missile Success Probability\n(Red Offensive Missile Success Probability Set at 0.9)')
    plt.savefig('NumberShipHitChangingBlueProb.png', dpi=600, bbox_inches='tight')
    plt.show()
        
    
    #Graph of Average Range Between Ships
    plt.plot(offensiveMissileSuccessProbability, AvgBlueOMRArr, color='blue', label='Blue Offensive Missile Range')
    plt.plot(offensiveMissileSuccessProbability, AvgRedOMRArr, color='red', label='Red Offensive Missile Range')
    plt.plot(offensiveMissileSuccessProbability, AvgRangeArr, color='black', label='Range Between Ships')
    plt.legend()
    offMSPString = ['0', '1/10', '2/10', '3/10', '4/10', '5/10', '6/10', '7/10', '8/10', '9/10', '1']
    plt.xticks(offensiveMissileSuccessProbability, offMSPString)
    plt.xlabel('Blue Offensive Missile Success Probability')
    plt.ylabel('Range (NM)')
    plt.title('Average Range Between Ships at End of Simulation\nwhen Changing Blue Offensive Missile Success Probability\n(Red Offensive Missile Success Probability Set at 0.9)')
    plt.savefig('RangeChangingBlueProb.png', dpi=600, bbox_inches='tight')
    plt.show()
    
    
    #Graph of Average Missile Engagement Costs
    plt.plot(offensiveMissileSuccessProbability, AvgBlueCostArr, color='blue', label='Blue')
    plt.plot(offensiveMissileSuccessProbability, AvgRedCostArr, color='red', label='Red')
    plt.legend()
    offMSPString = ['0', '1/10', '2/10', '3/10', '4/10', '5/10', '6/10', '7/10', '8/10', '9/10', '1']
    plt.xticks(offensiveMissileSuccessProbability, offMSPString)
    plt.xlabel('Blue Offensive Missile Success Probability')
    plt.ylabel('Cost (USD)')
    plt.title('Average Missile Engagement Cost\nwhen Changing Blue Offensive Missile Success Probability\n(Red Offensive Missile Success Probability Set at 0.9)', pad=15)
    plt.savefig('CostChangingBlueProb.png', dpi=600, bbox_inches='tight')
    plt.show()
    
    #Graph of Average Cost of Missiles Fired
    plt.plot(offensiveMissileSuccessProbability, AvgBlueMissileCostArr, color='blue', label='Blue')
    plt.plot(offensiveMissileSuccessProbability, AvgRedMissileCostArr, color='red', label='Red')
    plt.legend()
    offMSPString = ['0', '1/10', '2/10', '3/10', '4/10', '5/10', '6/10', '7/10', '8/10', '9/10', '1']
    plt.xticks(offensiveMissileSuccessProbability, offMSPString)
    plt.xlabel('Blue Offensive Missile Success Probability')
    plt.ylabel('Cost (USD)')
    plt.title('Average Cost of Missiles Fired\nwhen Changing Blue Offensive Missile Success Probability\n(Red Offensive Missile Success Probability Set at 0.9)', pad=15)
    plt.savefig('MissileCostChangingBlueProb.png', dpi=600, bbox_inches='tight')
    plt.show()
    
    #Graph of Average Offensive Missiles Fired
    plt.plot(offensiveMissileSuccessProbability, AvgBlueOMFArr, color='blue', label='Blue')
    plt.plot(offensiveMissileSuccessProbability, AvgRedOMFArr, color='red', label='Red')
    plt.legend()
    offMSPString = ['0', '1/10', '2/10', '3/10', '4/10', '5/10', '6/10', '7/10', '8/10', '9/10', '1']
    plt.xticks(offensiveMissileSuccessProbability, offMSPString)
    plt.xlabel('Blue Offensive Missile Success Probability')
    plt.ylabel('Average Offensive Missiles Fired')
    plt.title('Average Number Offensive Missiles Fired\nwhen Changing Blue Offensive Missile Success Probability\n(Red Offensive Missile Success Probability Set at 0.9)')
    plt.savefig('OffensiveChangingBlueProb.png', dpi=600, bbox_inches='tight')
    plt.show()
    
    #Graph of Average Defensive Missiles Fired
    plt.plot(offensiveMissileSuccessProbability, AvgBlueDMFArr, color='blue', label='Blue')
    plt.plot(offensiveMissileSuccessProbability, AvgRedDMFArr, color='red', label='Red')
    plt.legend()
    offMSPString = ['0', '1/10', '2/10', '3/10', '4/10', '5/10', '6/10', '7/10', '8/10', '9/10', '1']
    plt.xticks(offensiveMissileSuccessProbability, offMSPString)
    plt.xlabel('Blue Offensive Missile Success Probability')
    plt.ylabel('Average Number Defensive Missiles Fired')
    plt.title('Average Defensive Missiles Fired\nwhen Changing Blue Offensive Missile Range\n(Red Offensive Missile Range Set at 300 NM)')
    plt.savefig('DefensiveChangingBlueProb.png', dpi=600, bbox_inches='tight')
    plt.show()
    
    #Graph of Average ESSMs Fired
    plt.plot(offensiveMissileSuccessProbability, AvgBlueEMFArr, color='blue', label='Blue')
    plt.plot(offensiveMissileSuccessProbability, AvgRedEMFArr, color='red', label='Red')
    plt.legend()
    offMSPString = ['0', '1/10', '2/10', '3/10', '4/10', '5/10', '6/10', '7/10', '8/10', '9/10', '1']
    plt.xticks(offensiveMissileSuccessProbability, offMSPString)
    plt.xlabel('Blue Offensive Missile Success Probability')
    plt.ylabel('Average ESSMs Fired')
    plt.title('Average Number ESSMs Fired\nwhen Changing Blue Offensive Missile Success Probability\n(Red Offensive Missile Success Probability Set at 0.9)')
    plt.savefig('ESSMChangingBlueProb.png', dpi=600, bbox_inches='tight')
    plt.show()
    
    #Graph of Average SeaRAMs Fired
    plt.plot(offensiveMissileSuccessProbability, AvgBlueSMFArr, color='blue', label='Blue')
    plt.plot(offensiveMissileSuccessProbability, AvgRedSMFArr, color='red', label='Red')
    plt.legend()
    offMSPString = ['0', '1/10', '2/10', '3/10', '4/10', '5/10', '6/10', '7/10', '8/10', '9/10', '1']
    plt.xticks(offensiveMissileSuccessProbability, offMSPString)
    plt.xlabel('Blue Offensive Missile Success Probability')
    plt.ylabel('Average SeaRAMs Fired')
    plt.title('Average Number SeaRAMs Fired\nwhen Changing Blue Offensive Missile Success Probability\n(Red Offensive Missile Success Probability Set at 0.9)')
    plt.savefig('SeaRAMChangingBlueProb.png', dpi=600, bbox_inches='tight')
    plt.show()
    
    #Graph of Average ESSMs Fired
    plt.plot(offensiveMissileSuccessProbability, AvgBlueCMFArr, color='blue', label='Blue')
    plt.plot(offensiveMissileSuccessProbability, AvgRedCMFArr, color='red', label='Red')
    plt.legend()
    offMSPString = ['0', '1/10', '2/10', '3/10', '4/10', '5/10', '6/10', '7/10', '8/10', '9/10', '1']
    plt.xticks(offensiveMissileSuccessProbability, offMSPString)
    plt.xlabel('Blue Offensive Missile Success Probability')
    plt.ylabel('Average CIWS Iterations Fired')
    plt.title('Average Number CIWS Iterations Fired\nwhen Changing Blue Offensive Missile Success Probability\n(Red Offensive Missile Success Probability Set at 0.9)')
    plt.savefig('CIWSChangingBlueProb.png', dpi=600, bbox_inches='tight')
    plt.show()
    
    
    
    
    
    
        
        
        
        