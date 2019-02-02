'''
Created on Oct 12, 2011
Modified on  August 2012

@author: Bhavesh Khemka(bkhemka), Ryan Friese(rfriese)
'''
import random
from math import sin, pi
import numpy as np
import os
import matplotlib.pyplot as plt 
import pylab as plot
import copy
import math
import gc

DUR_TASK_0=159
DUR_TASK_1=172
DUR_TASK_2=158
DUR_TASK_3=161
DUR_TASK_4=164
DUR_TASK_5=155
DUR_TASK_6=189
DUR_TASK_7=462
DUR_TASK_8=225
DUR_TASK_9=145
DUR_TASK_10=139
DUR_TASK_11=132
############configuratoin for different workloads###########Mohsen
#Workload_duration=4.75#workload with 2000 tasks (first one we generated)
#TIME_UNIT=3600 #60 for minute and 3600 for second
#NUM_TASKS=2600
#TIME_TO_START_DAY=2
#NUM_TRIAL=100
################################################################
#Workload_duration=24.5#workload2
#TIME_UNIT=60 #60 for minute and 3600 for second
#NUM_TASKS=3400 # to generate 2640 tasks during 24 hours (based on Bhavesh method when uses 33K. In fact we did 33K*8/100 to work out number of tasks when 8 machines are there compared with situation where 100 machine are there (Bhavesh case))
#TIME_TO_START_DAY=0
#NUM_TRIAL=100
################################################################
#Workload_duration=24.5#workload3
#TIME_UNIT=60 #60 for minute and 3600 for second
#NUM_TASKS=1295 # to generate 1000 tasks during 24 hours 
#TIME_TO_START_DAY=0
#NUM_TRIAL=100
################################################################
# Workload_duration=168.5#workload4 for 1 week
Workload_duration=24.5 # 24.5 JUST FOR PLOTTING
#reduce down time unit and num_task by 5 times
TIME_UNIT=720 #720 down from 3600
NUM_TASKS=2000 # 10k=2000,15k=3000, 4000,5000,6000,7000 (=35k)
#NUM_TASKS=3000 # to generate 2000 useful tasks (in fact 2200 tasks)
# NUM_TASKS=2370 # to generate 1500 tasks during 1 week 
# NUM_TASKS=1600 # to generate 1000 tasks during 1 week 
#NUM_TASKS=2000 # JUST FOR PLOTTING 
# NUM_TASKS=1000 # to generate 500 tasks (of course it has to be at least 700 that becomes 500 after warmup and cooldown
TIME_TO_START_DAY=0
NUM_TRIAL=1 #30
################################################################
DO_PLOTTING=1

def genArrivalsOfGeneralTaskTypes(numTasks, numGenTaskT, numSplTaskT, classes, priAndPrecFreq, numPriority, numPrecedence, duration, doPlotting):
    """ Generate the arrivals of general purpose task types
    
    n -- the number of tasks
    numGenTaskT -- the number of general task execution types
    numSplTaskT -- the number of special task execution types
    teTypes -- the number of task execution types
    classes -- the number of utility characteristic classes
    priAndPrecFreq -- cumulative distribution of pairs of priority and precedence
    numPriority -- the number of priority levels
    numPrecedence -- the number of precedence levels
    
    returns
    -- a list of lines representing general purpose tasks with the following format:
    Task Number, Task Class, Arrival time, task priority, task precedence, task type
    -- another list with the number of tasks in each of the general task types
    
    @author: Bhavesh Khemka    
    """
    
    sinRateListGrand = []
    timeListGrand = []
    meanRateListGrand = []
    
    taskDataAll = []
    numTasksInTaskT = []
    dayDuration = 24 * TIME_UNIT  #24 hours times 60 minutes = 1440 minutes
    meanNumTasksForTaskT = numTasks / (numGenTaskT + numSplTaskT)
    varNumTasksForTaskT  = meanNumTasksForTaskT / 10    #Setting the variance to be 10% around the mean
    
    for i in range(numGenTaskT):    
        time = 0
        numExpectedTasksHere = random.gauss(meanNumTasksForTaskT, varNumTasksForTaskT)  #NOOOTTTTEEEE: this is unlikely to be an integer!!!
        meanRate = numExpectedTasksHere/duration
        t = 1
        
        sinRateList = []
        timeList = []
        meanRateOfCurrent = 0
        
        numbHalfSin = random.randrange(2, 48, 2)    #governs the frequency, the steps of two is done so that the curve repeats after the 24 hour period
        startOffset = random.uniform(0, 2*pi)       #governs the phase shift
        sizeOfSin   = random.uniform(0.25, 0.90)    #governs the amplitude
        
        if i==0:
            numbHalfSin = 24
            startOffset = 0
            sizeOfSin   = 0.9            
        elif i==1:
            numbHalfSin = 48
            startOffset = pi/4
            sizeOfSin   = 0.5
        elif i==2:
            numbHalfSin = 2
            startOffset = pi/2
            sizeOfSin   = 0.666667
                      
        
            
        while (time < duration):            
            sinRate = sin( (numbHalfSin*pi)*time/dayDuration - startOffset)*meanRate*sizeOfSin + meanRate
            #if (i<10): #bkhemka: Note the arrival rate of for the first general task type for plotting
            sinRateList.append(sinRate)
            timeList.append(time)
            meanRateOfCurrent = meanRate
            #nextArrivalStep = random.expovariate(sinRate)
            #nextArrivalStep = random.gauss(1/sinRate, 1/(10*sinRate))
            nextArrivalStep = random.expovariate(sinRate)#, 1/(10*sinRate))
            
            #print "time = ", time, " sinRate = ", sinRate, " step = ", nextArrivalStep
            if (nextArrivalStep > dayDuration/50):
                nextArrivalStep = dayDuration/50
            time += nextArrivalStep
            if time > duration:
                break
            taskClass = random.randint(1,classes) # rfriese: decide task class
            priority,precedence = generatePriorityAndPrecedence(priAndPrecFreq,numPriority,numPrecedence)
            taskType = i + 1 + numSplTaskT  #bkhemka: add 1 because indexing starts at zero, whereas the task types are numbered starting from 1
                                            #         add numSplTaskT because initial numSplTaskT number of task types are special-purpose and only after 
                                            #    those does the count for the general-purpose task types start
            task = [t,taskClass,time,priority,precedence,taskType] # rfriese: basically a row in the arrival file
            taskDataAll.append(task)
            t += 1
        
        numTasksInTaskT.append(t-1)
                
        sinRateListGrand.append(sinRateList)
        timeListGrand.append(timeList)
        meanRateListGrand.append(meanRateOfCurrent)
        
        #New code for graphing...
        if (doPlotting):
            if (i<8):
                gTime = 0 #graph time
                gTimeList = []
                gSinRateList = []
                while(gTime < duration):
                    gSinRateList.append(  sin( (numbHalfSin*pi)*gTime/dayDuration - startOffset)*meanRate*sizeOfSin + meanRate  )
                    gTimeList.append(gTime)
                    gTime = gTime +1
                
                plt.plot (gTimeList, gSinRateList)
                plt.axhline(y = meanRate, linewidth = 1, linestyle = '--', label = 'mean rate')
                #plt.title('Arrival Pattern for a General Task Type')
                plt.xlabel('number of time-units')
                plt.ylabel('arrival rate (in number of tasks per minute)')         
                params = {#'backend': 'ps',
                  'font.size' : 19,
                  'axes.labelsize': 17,
                  'font.family' : 'sans-serif',     #'sans-serif' implies Helvetica. 'font.family' does not have arial
                  #'text.fontsize': 10,
                  #'title.fontsize' : 25,
                  'legend.fontsize': 15,
                  'xtick.labelsize': 15,
                  'ytick.labelsize': 15,
                  'text.usetex': True,
                  #'figure.figsize': fig_size,
                  #'legend.linewidth': 2
                  }
                plot.rcParams.update(params)
            
        '''
        #Plot arrival rate of the first general task type
        if (i==0):
            plt.plot (timeListGrand[i], sinRateListGrand[i], color = 'r')
            plt.axhline(y = meanRateListGrand[i], linewidth = 1, linestyle = '--', label = 'mean rate')
            #plt.title('Arrival Pattern for a General Task Type')
            plt.xlabel('time (in minutes)')
            plt.ylabel('arrival rate (in number of tasks per minute)')            
            params = {#'backend': 'ps',
              'font.size' : 19,
              'axes.labelsize': 17,
              #'text.fontsize': 10,
              #'title.fontsize' : 25,
              'legend.fontsize': 13,
              'xtick.labelsize': 15,
              'ytick.labelsize': 15,
              'text.usetex': True,
              #'figure.figsize': fig_size,
              #'legend.linewidth': 2
              }
            plot.rcParams.update(params)
            plt.show()
        
        
        if (i<5):
            print "Type", i
            print "numbHalfSin",numbHalfSin
            print "startOffset",startOffset
            print "sizeOfSin",sizeOfSin
            #An overlay plot of the arrival rate for all the Task Types
            plt.plot (timeListGrand[i], sinRateListGrand[i])
            plt.axhline(y = meanRateListGrand[i], linewidth = 1, linestyle = '--', label = 'mean rate')
            #plt.title('Arrival Pattern for a General Task Type')
            plt.xlabel('time (in minutes)')
            plt.ylabel('arrival rate (in number of tasks per minute)')            
            params = {#'backend': 'ps',
              'font.size' : 19,
              'axes.labelsize': 17,
              #'text.fontsize': 10,
              #'title.fontsize' : 25,
              'legend.fontsize': 13,
              'xtick.labelsize': 15,
              'ytick.labelsize': 15,
              'text.usetex': True,
              #'figure.figsize': fig_size,
              #'legend.linewidth': 2
              }
            plot.rcParams.update(params)
            #plt.Figure(3)
        '''        
    
    if (doPlotting):
        plt.show()
    return (taskDataAll, numTasksInTaskT)


def genArrivalsOfSpecialTaskTypes(numTasks, numGenTaskT, numSplTaskT, classes, priAndPrecFreq, numPriority, numPrecedence, timeToStartDay, duration, baseRateRange, highRateRange, baseInterval, highInterval, doPlotting):
    """ Generate the arrivals of special purpose task types
    
    n -- the number of tasks
    numGenTaskT -- the number of general task execution types
    numSplTaskT -- the number of special task execution types
    teTypes -- the number of task execution types
    classes -- the number of utility characteristic classes
    priAndPrecFreq -- cumulative distribution of pairs of priority and precedence
    numPriority -- the number of priority levels
    numPrecedence -- the number of precedence levels
    baseRateRange -- factor with respect to the mean rate of baseline arrival for special task types
    highRateRange -- factor with respect to the mean rate of higher arrival for special task types
    baseInterval -- tuple containing the baseline interval i.e. (3*60,5*60) 3 - 5 hours (in minutes)
    highInterval -- tuple containing the higher interval i.e. (.5*60,1.5*60) .5 - 1.5 hours (in minutes)
    
    returns
    -- a list of lines representing a special puporse tasks with the following format:
    Task Number, Task Class, Arrival time, task priority, task precedence, task type
    -- another list with the number of tasks in each of the special task types
    
    @author: Bhavesh Khemka    
    """

    rateListGrand = []
    timeListGrand = []
    meanRateListGrand = []
    
    taskDataAll = []
    numTasksInTaskT = []
    meanNumTasksForTaskT = numTasks / (numGenTaskT + numSplTaskT)
    varNumTasksForTaskT  = meanNumTasksForTaskT / 10    #Setting the variance to be 10% around the mean
    
    for i in range(numSplTaskT):
        rateList = []
        timeList = []
        meanRateOfCurrent = 0
        time = 0
        timeBegin = 0 # rfriese : beginning time of each interval
        intervalLen = 1 # rfriese : used to signify length of current interval
        
        if (random.randrange(0, 2, 1)):
            mode = "baseline" 
        else:
            mode = "higher"
        
        dayBoundaryMode = copy.deepcopy(mode)
        dayBoundaryInterval = 0
        dayBoundaryRate = 0
        startFound = 0
        endPerformed = 0
        timeToEndDay = timeToStartDay + (24*TIME_UNIT)#????mohsen
        
        numExpectedTasksHere = random.gauss(meanNumTasksForTaskT, varNumTasksForTaskT)  #NOOOTTTTEEEE: this is unlikely to be an integer!!!
#        print 'numExpectedTasksHere=',numExpectedTasksHere
        meanRate = numExpectedTasksHere/duration
     
        t = 1
        while time < duration:
            if mode is "baseline":
                intervalLen = random.randint(baseInterval[0],baseInterval[1])
                rate = random.uniform(baseRateRange[0]*meanRate,baseRateRange[1]*meanRate)        #bkhemka: definition: generates a random float in range [a,b]
                mode = "higher"
            else:
                intervalLen = random.randint(highInterval[0],highInterval[1])
                rate = random.uniform(highRateRange[0]*meanRate,highRateRange[1]*meanRate)        #bkhemka: definition: generates a random float in range [a,b]              
                mode = "baseline"
            while (intervalLen + timeBegin) > time:
########################I THNIK THIS PART IS FOR REPLICATING END OF WORKLOAD (I.E. CONSIDERING WARM UP PERIOD############
#                if (startFound == 0) and (time > timeToStartDay):
#                    startFound = 1
#                    dayBoundaryMode = copy.deepcopy(mode)
#                    dayBoundaryInterval = time - timeBegin
#                    #print "time = ", time, "timeBegin = ", timeBegin, "difference = ", (time - timeBegin)
#                    #print "dayBoundaryInterval = ", dayBoundaryInterval
#                    dayBoundaryRate = copy.deepcopy(rate)
#                    #if (i==0):
#                    #    print "dayBoundaryMode = ", dayBoundaryMode
#                    #    print "dayBoundaryInterval = ", dayBoundaryInterval
#                    #    print "dayBoundaryRate = ", dayBoundaryRate  
#                if (startFound == 1) and (time > (timeToEndDay - dayBoundaryInterval)) and (endPerformed == 0):
#                    endPerformed = 1
#                    mode        = copy.deepcopy(dayBoundaryMode)
#                    intervalLen = copy.deepcopy(dayBoundaryInterval)
#                    intervalLen = intervalLen - (time - (timeToEndDay - dayBoundaryInterval))
#                    rate        = copy.deepcopy(dayBoundaryRate)
#                    timeBegin   = time
#                    #if (i==0):
#                    #    print "mode = ", mode
#                    #    print "intervalLen = ", intervalLen
#                    #    print "rate = ", rate
####################################UP TO HERE################################
                time += random.expovariate(rate)
                if time > duration:
                    break                    
                rateList.append(rate)
                timeList.append(time)
#                print time
                meanRateOfCurrent = meanRate
                taskClass = random.randint(1,classes) # rfriese: decide task class
                priority,precedence = generatePriorityAndPrecedence(priAndPrecFreq,numPriority,numPrecedence)
                taskType = i+1 #bkhemka: because indexing starts at zero, whereas the task types are numbered starting from 1
                taskType = taskType-1 #bkhemka: because indexing starts at zero, whereas the task types are numbered starting from 1
                task = [t,taskClass,time,priority,precedence,taskType] # rfriese: basically a row in the arrival file
                taskDataAll.append(task)
                t += 1
            timeBegin = time

        numTasksInTaskT.append(t-1)
#         if(timeList[0]<2000):
        rateListGrand.append(rateList)
        timeListGrand.append(timeList)
        meanRateListGrand.append(meanRateOfCurrent)
        
        #Plot arrival rate of the first special task type 
        if (doPlotting):        
            if (i<4):
                clr=['darkgreen','royalblue','forestgreen','mediumblue','lightblue','limegreen','magenta','orange','red']
                sty=['-', '-' , '-.' , ':' , '--','--','-', '-' , '-.' , ':' , '--','--' ]
                plt.plot (timeListGrand[i], rateListGrand[i],linewidth = 3,linestyle = sty[i],color=clr[i])
#                 print timeListGrand[i],'----',rateListGrand[i]
                #plt.axhline(y = meanRateListGrand[i], linewidth = 2, linestyle = '--',color=clr[i])
                #plt.title('Arrival Pattern for a Special Task Type')
                plt.xlabel('number of time-units')
                plt.ylabel('arrival rate (in number of tasks per time-unit)')            
                params = {#'backend': 'ps',
                  'font.size' : 35,
                  'axes.labelsize': 38,
                  'font.family' : 'sans-serif',     #'sans-serif' implies Helvetica. 'font.family' does not have arial
                  #'text.fontsize': 38,
                  #'title.fontsize' : 30,
                  'legend.fontsize': 25,
                  'xtick.labelsize': 38,
                  'ytick.labelsize': 38,
                  'text.usetex': True,
                  #'figure.figsize': fig_size,
                  #'legend.linewidth': 1
                  }
                plot.rcParams.update(params)
        #the "if(doPlotting)" statement  ends at this indentation level
    
    #the "for i in range(numSplTaskT)" loop ends at this indentation level

    if (doPlotting):         
        plt.xlim(0,Workload_duration*TIME_UNIT)
#         plt.xlim(0,1500)
        plt.show()            
    return (taskDataAll, numTasksInTaskT)
    
    
    
def genSimpsonArrivals (numTasks, numGenTaskT, numSplTaskT, classes, priAndPrecFreq, numPriority, numPrecedence, baseRateRange, highRateRange, baseInterval, highInterval, timeToStartDay, duration, doPlotting):
    """ Generate the arrivals of special purpose task types
    
    n -- the number of tasks
    numGenTaskT -- the number of general task execution types
    numSplTaskT -- the number of special task execution types
    classes -- the number of utility characteristic classes
    priAndPrecFreq -- cumulative distribution of pairs of priority and precedence
    numPriority -- the number of priority levels
    numPrecedence -- the number of precedence levels
    baseRateRange -- factor with respect to the mean rate of baseline arrival for special task types
    highRateRange -- factor with respect to the mean rate of higher arrival for special task types
    baseInterval -- tuple containing the baseline interval i.e. (3*60,5*60) 3 - 5 hours (in minutes)
    highInterval -- tuple containing the higher interval i.e. (.5*60,1.5*60) .5 - 1.5 hours (in minutes)
    
    returns
    -- a list of lines representing a task with the following format:
    Task Number, Task Class, Arrival time, task priority, task precedence, task type
    
    @author: Bhavesh Khemka    
    """
    
    debug = 0
    taskDataAll = []
    
    
    #####################################################################
    ####################### General-Purpose Tasks #######################
    #####################################################################
    if (numGenTaskT != 0):
        (taskDataGenTasks, numGenTasksInTaskT) = genArrivalsOfGeneralTaskTypes(numTasks, numGenTaskT, numSplTaskT, classes, priAndPrecFreq, numPriority, numPrecedence, duration, doPlotting)
        
        taskDataGenTasksArray = np.array(taskDataGenTasks)
        taskDataGenTasksArraySorted = taskDataGenTasksArray[taskDataGenTasksArray[:,2].argsort()] #sort based on the arrival time    
        taskDataGenTasksFinalList = taskDataGenTasksArraySorted.tolist()    
        
        taskDataAll += taskDataGenTasks
        
        if(debug):
            print "len(taskDataGenTasks) = ", len(taskDataGenTasks), "sum(numGenTasksInTaskT) = ", sum(numGenTasksInTaskT)
        
        #Plot the arrival of the General-purpose Tasks
#        if (doPlotting):
#            arrivals = []
#            m = 0
#            cnt = [1]
#            for o in taskDataGenTasksFinalList:
#                if o[2] < m + 1: # rfriese: count number of arrivals per minute
#                    cnt[m]+=1
#                else:
#                    cnt.append(1)
#                    m += 1
#                    
#                arrivals.append(o[2])
#            #print out
#            #plt.plot(arrivals)
#            #plt.show()
#            plt.plot(cnt)
#            #plt.title('Arrival Pattern of all Tasks')
#            plt.xlabel('time (in minutes)')
#            plt.ylabel('number of tasks arrived per minute')
#            params = {#'backend': 'ps',
#              'font.size' : 19,
#              'axes.labelsize': 17,
#              'font.family' : 'sans-serif',     #'sans-serif' implies Helvetica. 'font.family' does not have arial
#              #'text.fontsize': 10,
#              #'title.fontsize' : 25,
#              'legend.fontsize': 15,
#              'xtick.labelsize': 15,
#              'ytick.labelsize': 15,
#              'text.usetex': True,
#              #'figure.figsize': fig_size,
#              #'legend.linewidth': 2
#              }
#            plot.rcParams.update(params)
#            #plt.Figure(1)
#            plt.show()    
    
    
    #####################################################################
    ####################### Special-Purpose Tasks #######################
    #####################################################################
    if (numSplTaskT != 0):
        (taskDataSplTasks, numSplTasksInTaskT) = genArrivalsOfSpecialTaskTypes(numTasks, numGenTaskT, numSplTaskT, classes, priAndPrecFreq, numPriority, numPrecedence, timeToStartDay, duration, baseRateRange, highRateRange, baseInterval, highInterval, doPlotting)
        
        taskDataSplTasksArray = np.array(taskDataSplTasks)
        taskDataSplTasksArraySorted = taskDataSplTasksArray[taskDataSplTasksArray[:,2].argsort()] #sort based on the arrival time    
        taskDataSplTasksFinalList = taskDataSplTasksArraySorted.tolist()    
        
        taskDataAll += taskDataSplTasks
        
        if(debug):
            print "len(taskDataSplTasks) = ", len(taskDataSplTasks), "sum(numSplTasksInTaskT) = ", sum(numSplTasksInTaskT)
        
        #Plot the arrival of the General-purpose Tasks
#COMMENTED BY MOHSEN
#        if (doPlotting):
#            arrivals = []
#            m = 0
#            cnt = [1]
#            for o in taskDataSplTasksFinalList:
#                if o[2] < m + 1: # rfriese: count number of arrivals per minute
#                    cnt[m]+=1
#                else:
#                    cnt.append(1)
#                    m += 1
#                    
#                arrivals.append(o[2])
#            #print out
#            #plt.plot(arrivals)
#            #plt.show()
#            plt.plot(cnt)
#            #plt.title('Arrival Pattern of all Tasks')
#            plt.xlabel('time (in minutes)')
#            plt.ylabel('number of tasks arrived per minute')
#            params = {#'backend': 'ps',
#              'font.size' : 19,
#              'axes.labelsize': 17,
#              'font.family' : 'sans-serif',     #'sans-serif' implies Helvetica. 'font.family' does not have arial
#              #'text.fontsize': 10,
#              #'title.fontsize' : 25,
#              'legend.fontsize': 15,
#              'xtick.labelsize': 15,
#              'ytick.labelsize': 15,
#              'text.usetex': True,
#              #'figure.figsize': fig_size,
#              #'legend.linewidth': 2
#              }
#            plot.rcParams.update(params)
#            #plt.Figure(1)
#            plt.show()    
           
    
    #####################################################################
    ######################### Merge Tasks Lists #########################
    #####################################################################
    '''bkhemka: merge the lists, drop their task_id values, sort them based on the arrival time of tasks and then create new values for the task_ids'''

    taskDataArray = np.array(taskDataAll)
    if(debug):
        print "taskDataArray.shape() before deleting = ", taskDataArray.shape
    
    taskDataArray = taskDataArray[:,1:taskDataArray.shape[1]]
    if(debug):
        print "taskDataArray.shape() after deleting = ", taskDataArray.shape
    
    taskDataArraySorted = taskDataArray[taskDataArray[:,1].argsort()] #sort based on the arrival time. Note that the arrival time information is now in the second column (imstead of third) because we have stripped of the first column
    
    taskId = np.arange(taskDataArraySorted.shape[0])
    taskId += 1
    taskId = taskId.reshape(-1,1)
    
    taskDataArrayRenew = np.hstack((taskId, taskDataArraySorted))
    if(debug):
        print "taskDataArrayRenew.shape() = ", taskDataArrayRenew.shape
        print "taskDataArrayRenew[0,0] = ", taskDataArrayRenew[0,0]
        print "taskDataArrayRenew[ taskDataArrayRenew.shape[0] -1 , 0] = ", taskDataArrayRenew[ taskDataArrayRenew.shape[0] -1 , 0]
    
    taskDataFinalList = taskDataArrayRenew.tolist()
    
    return taskDataFinalList   
    


def genArrivals(numTasks, teTypes, classes, priAndPrecFreq, numPriority, numPrecedence, baseRateRange, highRateRange, baseInterval, highInterval):
    """ Generate the arrivals that occur at time
    
    n -- the number of tasks
    teTypes -- the number of task execution types
    classes -- the number of utility characteristic classes
    priAndPrecFreq -- cumulative distribution of pairs of priority and precedence
    numPriority -- the number of priority levels
    numPrecedence -- the number of precedence levels
    baseRateRange -- arrival rate range of baseline
    highRateRange -- arrival rate range of higher
    baseInterval -- tuple containing the baseline interval i.e. (3*60,5*60) 3 - 5 hours (in minutes)
    highInterval -- tuple containing the higher interval i.e. (.5*60,1.5*60) .5 - 1.5 hours (in minutes)
    
    returns a list of lines representing a task with the following format:
    Task Number, Task Class, Arrival time, task priority, task precedence, task type
    
    @author: Ryan Friese
    
    """
    taskData = []
    time = 0
    timeBegin = 0 # rfriese : beginning time of each interval
    intervalLen = 1 # rfriese : used to signify length of current interval
    mode = "baseline" # mode = baseline, mode = higher
    rate = baseRateRange[0]
     
    t = 1
    while t < numTasks:
        if mode is "baseline":
            intervalLen = random.randint(baseInterval[0],baseInterval[1])
            rate = random.uniform(baseRateRange[0],baseRateRange[1])        #bkhemka: definition: generates a random float in range [a,b]
            mode = "higher"
        else:
            intervalLen = random.randint(highInterval[0],highInterval[1])
            rate = random.uniform(highRateRange[0],highRateRange[1])        #bkhemka: definition: generates a random float in range [a,b]
            mode = "baseline"
        while (intervalLen + timeBegin) > time:
            if t > numTasks:
                break
            time += random.expovariate(rate)
            taskClass = random.randint(1,classes) # rfriese: decide task class
            priority,precedence = generatePriorityAndPrecedence(priAndPrecFreq,numPriority,numPrecedence)
            taskType = random.randint(1,teTypes) # rfriese: decide task type
            task = [t,taskClass,time,priority,precedence,taskType] # rfriese: basically a row in the arrival file
            taskData.append(task)
            t += 1
        timeBegin = time
    return taskData

def gammaDist(M, V):
    """ Generate a sample from Gamma distribution
    M -- the mean
    V -- the coefficient of variation
    
    return sample
    @author: Ryan Friese    
    """
    shape = 1/float(V**2)
    scale = M/float(shape)
    return random.gammavariate(shape,scale)



def generatePriorityAndPrecedence( priAndPrecFreq, numPriority, numPrecedence):
    '''Generates a priority level and precedence level
    based on the cumulative distribution provided 
    by priAndPrecFreq
    
    priAndPrecFreq -- cumulative distribution of pairs of priority and precedence
    numPriority -- the number of priority levels
    numPrecedence -- the number of precedence levels
    
    return(priority,precedence) 
    
    @author: Ryan Friese
    
    '''
    assert(len(priAndPrecFreq) == numPriority*numPrecedence)
    
    prioritys = np.array(priAndPrecFreq) - random.uniform(0,1)
    #bkhemka: prioritys now has a series of negative numbers up to the point where all the numbers were less than r_temp(random.uniform(0,1), and all positive numbs above that 
    
    prioritys = np.ceil((prioritys + np.abs(prioritys))/2)
    #bkhemka: prioritys now has a series of 0s instead of the negative numbs and a series of 1s instead of the positive numbs

    index = len(priAndPrecFreq) - sum(prioritys)
    #bkhemka: this gives the index position of the first '1' that was present in the list, possible values for index are in the range 0:length(priority_freq)-1
    
    priority = int(index/numPrecedence) + 1
    #rfriese: priority has the values 1 - numPriority, for the values of 1:numPrecedence, numPrecedence+1:2*numPrecedence, (2*numPrecedence)+1:3*numPrecedence, etc,. +1 is to make it 1 indexed instead of 0 indexed

    precedence = int((index)%numPrecedence) + 1
    #rfriese: precedence has values 1 - numPrecedence. + 1 at end to make it 1 index for precedence value instead of 0 indexed
    
    return (priority,precedence)
    
    
    
def generateCOVETC(numSplMachT, numGenMachT, numSplTaskT, numGenTaskT, splTaskToMach, VSplTask, VGenTask, VSplMach, VGenMach, MSplTask, MGenTask):
    """ Generates an inconsistent ETC matrix using coefficent of variation method
    numSplMachT -- number of special machine types
    numGenMachT -- number of general purpose machine types
    numSplTaskT --number of special task execution types
    numGenTaskT -- number of general task execution types
    SplTaskToMach -- assignment of number of special tasks to machines
    VSplTask -- coefficient of variation for task variation on special machines
    VGenTask -- coefficient of variation for task variation on general machines
    VSplMach -- coefficient of variation for special machine variation
    VGenMach -- coefficient of variation for general machine variation
    MSplTask -- mean machine time execution on special machines
    MGenTask -- mean machine time execution on general machines   
    """
    if(splTaskToMach is not None and numSplTaskT is not 0 and numSplMachT is not 0):
        assert sum(splTaskToMach) is numSplTaskT and len(splTaskToMach) is numSplMachT
    
    totalMachT = numSplMachT + numGenMachT
    totalTaskT = numSplTaskT + numGenTaskT
    
    splTaskI = range(numSplTaskT) # indices of special tasks
    genTaskI = range(numSplTaskT,totalTaskT) # indices of general tasks
    assert (len(splTaskI)+len(genTaskI)) is totalTaskT
    
    splMachI = range(numSplMachT) # indices of special machines
    genMachI = range(numSplMachT,totalMachT) # indices of general machines
    assert (len(splMachI)+len(genMachI)) is totalMachT
    
    etc = np.zeros((totalTaskT,totalMachT)) # initialize etc matrix to 0
    
    
    
    #===========================================================================
    # Handle special purpose machines and tasks first
    #===========================================================================
    
    ot = 0 # keep track of last modified task
    om = 0 # keep track of which machine we're filling values in for
    
    if splTaskToMach is not None:
        for ttm in splTaskToMach: # ttm is the number of special tasks a special machine gets
            for t in range(ot,ot+ttm): # t is the overall task number
                q = gammaDist(MSplTask,VSplTask) 
                for m in splMachI: # m is the special machine
                    if om is m: # om is the current special machine we are worried about
                        etc[t,m]=gammaDist(q,VSplMach)
                    else: # the machine can not run the task
                        etc[t,m]=float('99999')
                ot = t
            ot += 1
            om += 1
        
    for t in range(ot,totalTaskT): # general tasks can not execute on special machines
        for m in splMachI:
            etc[t,m]=float('99999')
            
    # End Handling special purpose machines and tasks===========================
    
    #===========================================================================
    # Now fill in the rest of the ETC matrix
    #===========================================================================
    
    for t in range(totalTaskT):
        q = gammaDist(MGenTask,VGenTask)
        for m in genMachI:
            etc[t,m]=gammaDist(q,VGenMach)
            
    # End filling in rest of the matrix=========================================
           
    return etc


def generateCOVEPC(numSplMachT,numGenMachT,numSplTaskT,numGenTaskT,splTaskToMach,VSplTask,VGenTask,VSplMach,VGenMach,MSplTask,MGenTask):
    """ Generates an inconsistent ETC matrix using coefficent of variation method
    numSplMachT -- number of special machine types
    numGenMachT -- number of general purpose machine types
    numSplTaskT --number of special task execution types
    numGenTaskT -- number of general task execution types
    SplTaskToMach -- assignment of number of special tasks to machines
    VSplTask -- coefficient of variation for task variation on special machines
    VGenTask -- coefficient of variation for task variation on general machines
    VSplMach -- coefficient of variation for special machine variation
    VGenMach -- coefficient of variation for general machine variation
    MSplTask -- mean machine time execution on special machines
    MGenTask -- mean machine time execution on general machines
    
    
    """
    if(splTaskToMach is not None and numSplTaskT is not 0 and numSplMachT is not 0):
        assert sum(splTaskToMach) is numSplTaskT and len(splTaskToMach) is numSplMachT
    
    totalMachT = numSplMachT + numGenMachT
    totalTaskT = numSplTaskT + numGenTaskT
    
    splTaskI = range(numSplTaskT) # indices of special tasks
    genTaskI = range(numSplTaskT,totalTaskT) # indices of general tasks
    assert (len(splTaskI)+len(genTaskI)) is totalTaskT
    
    splMachI = range(numSplMachT) # indices of special machines
    genMachI = range(numSplMachT,totalMachT) # indices of general machines
    assert (len(splMachI)+len(genMachI)) is totalMachT
    
    epc = np.zeros((totalTaskT,totalMachT)) # initialize etc matrix to 0
    
    
    
    #===========================================================================
    # Handle special purpose machines and tasks first
    #===========================================================================
    
    ot = 0 # keep track of last modified task
    om = 0 # keep track of which machine were filling values in for
    
    if splTaskToMach is not None:
        for ttm in splTaskToMach: # ttm is the number of special tasks a special machine gets
            for t in range(ot,ot+ttm): # t is the overall task number
                q = gammaDist(MSplTask,VSplTask) 
                for m in splMachI: # m is the special machine
                    if om is m: # om is the current special machine we are worried about
                        epc[t,m]=gammaDist(q,VSplMach)
                    else: # the machine can not run the task
                        epc[t,m]=float('99999')
                ot = t
            ot += 1
            om += 1
        
    for t in range(ot,totalTaskT): # general tasks can not execute on special machines
        for m in splMachI:
            epc[t,m]=float('99999')
            
    # End Handling special purpose machines and tasks===========================
    
    #===========================================================================
    # Now fill in the rest of the EPC matrix
    #===========================================================================
    
    for t in range(totalTaskT):
        q = gammaDist(MGenTask,VGenTask)
        for m in genMachI:
            epc[t,m]=gammaDist(q,VGenMach)
            
    # End filling in rest of the matrix=========================================       
     
    return epc

def generateBaseEPC(numMachT,VMachPower,MMachPower):
    baseEPC = np.zeros(numMachT)
    for m in range(numMachT):
        baseEPC[m]=gammaDist(MMachPower,VMachPower)
    return [baseEPC]

def generateCOVPStates(numPStates,numSplMachT,numGenMachT,numSplTaskT,numGenTaskT,splTaskToMach,VSplTask,VGenTask,VSplT,VSplP,VGenT,VGenP,MSplTask,MGenTask):
    """ Generates an inconsistent ETC matrix using coefficent of variation method
    numSplMachT -- number of special machine types
    numGenMachT -- number of general purpose machine types
    numSplTaskT --number of special task execution types
    numGenTaskT -- number of general task execution types
    SplTaskToMach -- assignment of number of special tasks to machines
    VSplTask -- coefficient of variation for task variation on special machines
    VGenTask -- coefficient of variation for task variation on general machines
    VSplMach -- coefficient of variation for special machine variation
    VGenMach -- coefficient of variation for general machine variation
    MSplTask -- mean machine time execution on special machines
    MGenTask -- mean machine time execution on general machines
    
    
    """
    if(splTaskToMach is not None and numSplTaskT is not 0 and numSplMachT is not 0):
        assert sum(splTaskToMach) is numSplTaskT and len(splTaskToMach) is numSplMachT
    
    totalMachT = numSplMachT + numGenMachT
    totalTaskT = numSplTaskT + numGenTaskT
    
    splTaskI = range(numSplTaskT) # indices of special tasks
    genTaskI = range(numSplTaskT,totalTaskT) # indices of general tasks
    assert (len(splTaskI)+len(genTaskI)) is totalTaskT
    
    splMachI = range(numSplMachT) # indices of special machines
    genMachI = range(numSplMachT,totalMachT) # indices of general machines
    assert (len(splMachI)+len(genMachI)) is totalMachT
    
    etcPstates = np.zeros((totalTaskT,totalMachT),dtype=object) # initialize etc matrix to 0
    epcPstates = np.zeros((totalTaskT,totalMachT),dtype=object)
    
    
    pstateAdv = False
    #===========================================================================
    # Handle special purpose machines and tasks first
    #===========================================================================
    
    ot = 0 # keep track of last modified task
    om = 0 # keep track of which machine were filling values in for
    
    if splTaskToMach is not None:
        for ttm in splTaskToMach: # ttm is the number of special tasks a special machine gets
            for t in range(ot,ot+ttm): # t is the overall task number
                q=gammaDist(1,VSplTask)
                for m in splMachI: # m is the special machine
                    if om is m: # om is the current special machine we are worried about
                        tpstates =[]
                        tpstates.append(MSplTask[0])
                        ppstates = []
                        ppstates.append(MSplTask[0])
                        for p in range(1,numPStates):
                            tps = 1.0/gammaDist(math.sqrt(q*MSplTask[p]),VSplT)
                            while tps < 1:
                                tps = 1.0/gammaDist(math.sqrt(q*MSplTask[p]),VSplT)
                            if pstateAdv:
                                tps = 1.0
                            tpstates.append(tps)
                            ppstates.append(gammaDist(MSplTask[p],VSplP))
                        etcPstates[t,m] = tpstates
                        epcPstates[t,m] = ppstates
                    else: # the machine can not run the task
                        pstates=[]
                        for p in range(0,numPStates):
                            pstates.append(float('99999'))
                        etcPstates[t,m]=pstates
                        epcPstates[t,m]=pstates
                ot = t
            ot += 1
            om += 1
        
    for t in range(ot,totalTaskT): # general tasks can not execute on special machines
        for m in splMachI:
            pstates=[]
            for p in range(0,numPStates):
                pstates.append(float('99999'))
            etcPstates[t,m]=pstates
            epcPstates[t,m]=pstates
            
    # End Handling special purpose machines and tasks===========================
    
    #===========================================================================
    # Now fill in the rest of the ETC matrix
    #===========================================================================
    
    for t in range(totalTaskT):
        q=gammaDist(1,VGenTask)
        for m in genMachI:
            tpstates =[]
            tpstates.append(MSplTask[0])
            ppstates = []
            ppstates.append(MSplTask[0])
            for p in range(1,numPStates):
                if pstateAdv:
                    tpstates.append(1.0)
                else:
                    tpstates.append(1.0/gammaDist(math.sqrt(q*MGenTask[p]),VGenT))
                #print MGenTask[p],GenTask[p]
                ppstates.append(gammaDist(MGenTask[p],VGenP))
            etcPstates[t,m]=tpstates
            epcPstates[t,m]=ppstates
    # End filling in rest of the matrix=========================================       
     
    return (etcPstates,epcPstates)

def writePstates(file,pstates):
    f = open(file,'w')
    for t in range(len(pstates)):
        h=''
        for m in range(len(pstates[0])):
            o=''
            for p in range(len(pstates[0][0])):
                #print t,m,p
                o=o+str(pstates[t][m][p])+','
                #print o
            o=o[:-1]
            h=h+o+';'
            #print h
        f.write(h+"\n")
    #print len(pstates),len(pstates[0]),len(pstates[0][0])

def generateUtilityEtcFiles(directory,numSims,ETCParams,EPCParams,arrivalParams,BPParams,PSParams):
    """Used to generate the simulation files for the utility research
    directory -- specifies the file structure where you want to place the sim files (without the cwd)
    numSims -- the number of simulations to create files for
    ETCParams -- the parameters used to create a ETC matrix:
        numSplMachT -- number of special machine types
        numGenMachT -- number of general purpose machine types
        numSplTaskT --number of special task execution types
        numGenTaskT -- number of general task execution types
        SplTaskToMach -- assignment of number of special tasks to machines
        VSplTask -- coefficient of variation for task variation on special machines
        VGenTask -- coefficient of variation for task variation on general machines
        VSplMach -- coefficient of variation for special machine variation
        VGenMach -- coefficient of variation for general machine variation
        MSplTask -- mean machine time execution on special machines
        MGenTask -- mean machine time execution on general machines
    arrivalParams -- the parameters used to generate the task arrivals
        numSplMachT -- number of special machine types
        numGenMachT -- number of general purpose machine types
        numSplTaskT --number of special task execution types
        numGenTaskT -- number of general task execution types
        SplTaskToMach -- assignment of number of special tasks to machines
        VSplTask -- coefficient of variation for task variation on special machines
        VGenTask -- coefficient of variation for task variation on general machines
        VSplMach -- coefficient of variation for special machine variation
        VGenMach -- coefficient of variation for general machine variation
        MSplTask -- mean machine time execution on special machines
        MGenTask -- mean machine time execution on general machines
        
        @author: Ryan Friese
    
    """
    min_no_tasks=100000 # a very big value
    totalArrival=0
    for i in range(numSims):
        etcFile = os.path.join(os.getcwd(),directory,"sim"+str(i+1))
        epcFile = os.path.join(os.getcwd(),directory,"sim"+str(i+1))
        mptFile = os.path.join(os.getcwd(),directory,"sim"+str(i+1))
        basePFile = os.path.join(os.getcwd(),directory,"sim"+str(i+1))
        tpStateFile = os.path.join(os.getcwd(),directory,"sim"+str(i+1))
        ppStateFile = os.path.join(os.getcwd(),directory,"sim"+str(i+1))
        if not os.path.exists(etcFile):
            os.makedirs(etcFile)
        etcFile = os.path.join(etcFile,"node_ETC"+str(i+1)+".etc")
        epcFile = os.path.join(epcFile,"node_EPC"+str(i+1)+".epc")
        mptFile = os.path.join(mptFile,"node_MPT"+str(i+1)+".mpt")
        basePFile = os.path.join(basePFile,"node_BP"+str(i+1)+".bp")
        tpStateFile = os.path.join(tpStateFile,"node_TPS"+str(i+1)+".tps")
        ppStateFile = os.path.join(ppStateFile,"node_PPS"+str(i+1)+".pps")
        etc = generateCOVETC(ETCParams[0],ETCParams[1],ETCParams[3],ETCParams[4],ETCParams[5],ETCParams[6],ETCParams[7],ETCParams[8],ETCParams[9],ETCParams[10],ETCParams[11])
        np.savetxt(etcFile, etc, fmt='%.2f', delimiter=',')
        epc = generateCOVEPC(EPCParams[0],EPCParams[1],EPCParams[3],EPCParams[4],EPCParams[5],EPCParams[6],EPCParams[7],EPCParams[8],EPCParams[9],EPCParams[10],EPCParams[11])
        np.savetxt(epcFile, epc, fmt='%.2f', delimiter=',')
        if len(ETCParams[2]) > 1:
            np.savetxt(mptFile,ETCParams[2],fmt='%d',delimiter=',')
        bp = generateBaseEPC(BPParams[0],BPParams[1],BPParams[2])
        #print bp
        np.savetxt(basePFile,bp,fmt='%.2f',delimiter=',')
#        ps = generateCOVPStates(PSParams[0],PSParams[1],PSParams[2],PSParams[4],PSParams[5],PSParams[6],PSParams[7],PSParams[8],PSParams[9],PSParams[10],PSParams[11],PSParams[12],PSParams[13],PSParams[14])
#        #np.savetxt(pStateFile,ps,dtype=object,delimiter=',')
#        #print ps[0]
#        #print ps[1]
#        writePstates(tpStateFile,ps[0])
#        writePstates(ppStateFile,ps[1])
#        print etcFile
#        print epcFile
        
        arrivalFile = os.path.join(os.getcwd(),directory,"sim"+str(i+1))
        if not os.path.exists(arrivalFile):
            os.makedirs(arrivalFile)
        arrivalFile = os.path.join(arrivalFile,"arrival"+str(i+1)+".dat")
        #arrivals = genArrivals(arrivalParams[0],arrivalParams[1],arrivalParams[2],arrivalParams[3],arrivalParams[4],arrivalParams[5],arrivalParams[6],arrivalParams[7],arrivalParams[8],arrivalParams[9])
        arrivals = genSimpsonArrivals (arrivalParams[0],arrivalParams[1],arrivalParams[2],arrivalParams[3],arrivalParams[4],arrivalParams[5],arrivalParams[6],arrivalParams[7],arrivalParams[8],arrivalParams[9], arrivalParams[10], arrivalParams[11], arrivalParams[12], arrivalParams[13])
        totalArrival+= len(arrivals)
        if len(arrivals)<min_no_tasks:
            min_no_tasks=len(arrivals)
        np.savetxt(arrivalFile,arrivals,fmt=( '%d', '%d', '%.2f', '%d', '%d', '%d'),delimiter=',')
        etc = None
        epc= None
        bp = None
        ps = None
        gc.collect()
    print 'Average number of tasks in generated arrival files: ',float(totalArrival/numSims), ' min arrival: ',min_no_tasks
        

if __name__ == "__main__":
    
    random.seed(420)
    numSplM = 8
    numGenM = 0
    nmpt = (2, 2, 3, 3, 5, 5, 5, 10, 10, 10, 10, 15, 20)
    #nmpt = (2, 2, 4, 4, 8, 8, 8, 12, 12, 12, 16, 16, 20)
    numSplT = 12
    numGenT = 0
    sttm = (1,2,1,2,1,2,1,2) # must sum to numSplT and len must be numSplM
    #sttm = (5,4,5,3)
#PIECE OF CODE FOR GENERATING HETEROGENEOUS LOAD RATE    
#    for i in range(0,10):
#        print "%.2f"%gammaDist(1250, 0.1)
      
    ETCParams = (numSplM, # numSplMachT
                 numGenM, # numGenMachT
                 nmpt, # number machines per type
                 numSplT, # numSplTaskT
                 numGenT, # numGenTaskT
                 sttm, # splTaskToMach
                 .1, # VSplTask
                 .1, # VGenTask
                 .1, # VSplMach
                 .25, # VGenMach
                 1, # MSplTask
                 10) # MGenTask
    
    EPCParams = (numSplM, # numSplMachT
                 numGenM, # numGenMachT
                 nmpt, #number machines per type
                 numSplT, # numSplTaskT
                 numGenT, # numGenTaskT
                 sttm, # splTaskToMach
                 .1, # VSplTask
                 .1, # VGenTask
                 .1, # VSplMach
                 .2, # VGenMach
                 133, # MSplTask
                 133) # MGenTask
    
    arrivalParams = (NUM_TASKS, # numTasks for ~26.5 hours
                     #for generating 33k during the 24 hour period, we use 38,000 as the value here
                     #for generating 50k during the 24 hour period, we use 58,000 as the value here
                     numGenT, # numGenTaskT
                     numSplT, # numSplTaskT
                     12, # numClasses
                     [0.02,0.04,0.0405,0.04050001, #-------
                      0.075,0.125,0.14,0.17,       #priority and
                      0.170001,0.27,0.37,0.47,     #precendence
                      0.4700001,0.4700002,0.67,1], #-------
                     4, # numPriority
                     4, # numPrecedence
                     (0.7,0.75), # baseRateRange for the special-purpose tasks
                     (2.1,2.25), # highRateRange for the special-purpose tasks                            
                     (0.5*TIME_UNIT,0.6*TIME_UNIT), # base interval for the special-purpose tasks #CVT, edit base interval here
                     #(16*TIME_UNIT,19*TIME_UNIT),
                     (0.125*TIME_UNIT,0.15*TIME_UNIT), # high interval for the special-purpose tasks #CVT, edit high interval here
                     #(5*TIME_UNIT,8*TIME_UNIT),
                     TIME_TO_START_DAY*TIME_UNIT,  #time to start the day (used by special-purpose tasks)
                     Workload_duration*TIME_UNIT, # total duration
                     DO_PLOTTING      # Plotting? 0 implies don't plot, 1 implies do the plotting
                     )
    
    basePParams = (numSplM+numGenM, # number of machine types
                   .2, #
                   66)
    
    psParams = (3, #number of p-states
                 numSplM, # numSplMachT
                 numGenM, # numGenMachT
                 nmpt, #number machines per type
                 numSplT, # numSplTaskT
                 numGenT, # numGenTaskT
                 sttm, # splTaskToMach
                 .2, # VSplTask
                 .2, # VGenTask
                 .02, # VSplT
                 .01, # VSplP
                 .01, # VGenT
                 .01, # VGenP
                 (1.0,.75,.5), # MSplTask
                 (1.0,.75,.5)) # MGenTask
    
    #generateUtilityEtcFiles(os.path.join("homer_refurb_33k","inconsistent"), 100, ETCParams, arrivalParams)  
    generateUtilityEtcFiles(os.path.join("final_en_tests_50k","inconsistent"),NUM_TRIAL,ETCParams,EPCParams,arrivalParams,basePParams,psParams)
#    convert()

    
    
    
"""
    bkhemka:
    NOTE: some of the below comments are now out of date <--- (written on 06/30/2012)
    
    Notes from the document "as_of_10_14_2011_ORNL_Machine_and_task_model.docx"
    
    1. For our future simulations we will assume 100 machines, 13 machine types, 10,000 tasks, and 100 task types.
        a. The ETC matrix will be of dimensions: (# of task types) X (# of machine types).
    2. Proposed allotment of machines to machine type where the association of machines to machine types would be fixed across simulation trials 
        a. 4 special purpose machine types comprising of 10 machines in all. The spread of the 10 machines into the 4 special purpose machine types will be (2,2,3,3).
        b. The remaining 90 machines will be divided amongst the remaining 9 machine types: (5, 5, 5, 10, 10, 10, 10, 15, 20). This is just an initial combination of machines into machine types. We should discuss these to finalize on our combination.
    3. 5 special purpose task types, 95 regular task types.
        a. The execution time for regular task types across regular machines will be generated using the "COV" method and will not be able to execute on special purpose machines.
        b. Special purpose task types will have execution times generated by the "COV" method for general machine and will have 1/10th the average regular machine  execution time on its special purpose machine. It will not be able to execute on the other special purpose machines.
    4. We randomly assign task types to the incoming tasks to assume an approximately equal number of tasks in each task type. 
        a. Should the number of tasks for each special purpose machine be smaller?
            a.i. No. Just keep it random.
    5. We would have around 3-5 task types for each special purpose machine type.    
""" 
    
"""
    bkhemka: 
    Notes:
    - We have 17 special purpose task types in all (as opposed to the 5 mentioned in the discussions)
    - We have 17500 tasks in all (as opposed to 10,000 mentioned in the discussions)
"""
    
    
    
    
