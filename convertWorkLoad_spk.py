'''
Created on Nov 6, 2012

@author: amini

Chavit update: spiky workload somehow start their tasktype index at 0 instead of 1, so +1 on task type to shift range to 1-12 rather than 0-11
'''


import os
import random
import math
import numpy

DUR_TASK=[159,172,158,161,164,155,189,462,225,145,139,132]

SEED=420

#DEADLINE_GEN='tight' #this variable determines the way deadline is generated. Values can be "tight" (batch mode paper) and "urgency" (Grag's paper) and "prop" based on Hj idea
DEADLINE_GEN='prop'
#DEADLINE_GEN='urgency'
##########PROPERTIES OF URGENCY DEADLINE##########
LOW_URGENCY_RATE=0.5 #Percentage of low urgency tasks
Avg_Low_Urgency=2
Var_Low_Urgency=0.5

Avg_High_Urgency=1.3
Var_High_Urgency=0.5
##################################################
#####PROPERTIES OF PROPORTIONAL DEADLINE##########
ALPHA=1.0 # Coefficient
NO_MACHINES=8
NO_TASKTYPES=12
ETC = numpy.empty((NO_TASKTYPES, NO_MACHINES)) #row: task type; column: machine type
##################################################
MEANFILESIZE=64
VARIANCEFILESIZE=6.4    #one tenth of meamfilesize
NUM_TRIAL=30

def getDataSize(MEANFILESIZE,VARIANCEFILESIZE):
    datasize=random.normalvariate(MEANFILESIZE,math.sqrt(VARIANCEFILESIZE))
    return round(datasize,2) 
def tight_deadline(taskType,parts):
        """
        This function generates deadlines based on what is discussed in Batch mode paper. 
        """
        deadline=float(parts[2].lstrip().rstrip())+DUR_TASK[taskType]
        return deadline
    
def urgency_deadline(taskType,parts):
    """
    this function generates deadline based on low and high urgency. For more information look at Grag's paper in JPDC and Amini's paper in AINA12. 
    """
    p=random.random()
    if p<=LOW_URGENCY_RATE:
        deadline=float(parts[2].lstrip().rstrip())+(random.normalvariate(Avg_Low_Urgency,math.sqrt(Var_Low_Urgency))*DUR_TASK[taskType])
    else:
        deadline=float(parts[2].lstrip().rstrip())+(random.normalvariate(Avg_High_Urgency,math.sqrt(Var_High_Urgency))*DUR_TASK[taskType])
    return round(deadline,2)

def proportional_deadline(taskType,parts):
    """
    this function generates deadline for task type "i" based on average of task execution time on all machines + (alpha * average execution time of all tasks on all machines)
    """
    sumTaskOnAllMachines=0.0
    for i in range(0,NO_MACHINES):
        sumTaskOnAllMachines+=ETC[taskType][i]
    avgTaskOnAllMachines=sumTaskOnAllMachines/NO_MACHINES
#    print 'avgTaskOnAllMachines=',avgTaskOnAllMachines
    overall_sum=0.0
    for i in range(0,NO_TASKTYPES):
        partial_avg=0.0
        partial_sum=0.0
        for j in range(0,NO_MACHINES):
            partial_sum+=ETC[i][j]
        partial_avg=partial_sum/NO_MACHINES
        overall_sum+=partial_avg
    overall_avg=overall_sum/NO_TASKTYPES
#    print 'overall_avg=',overall_avg
    deadline=avgTaskOnAllMachines+(ALPHA*overall_avg)
#    print deadline
    deadline=float(parts[2].lstrip().rstrip())+deadline #just add it to the task arrival time
    deadline=round(deadline,2)#round the deadline to avoid big numbers after decimal
    return deadline

def intialize():
    nominator=0.0
    denominator=0.0
    prevTaskType=0
    prevMachine=0
#    tt=1 #temporary task type (just for checking)
    fd = open('../trials/classes_2.etc', 'r')
    ETC.fill(0)
    for line in fd:
        if line.find("machine=") != -1:
            infoLine = line.split(";")
            machine=infoLine[0].split("=")
            taskType=infoLine[1].split("=")
            if line.find("machine=0;task=0")==-1: # if not the first row of the classes file
                avg=nominator/denominator
                ETC[prevTaskType,prevMachine]=avg
                nominator=0.0
                denominator=0.0
                avg=0
            prevTaskType=int(taskType[1])
            prevMachine=int(machine[1])
        else:
            if line.find("machineCount=8;taskCount=12") !=-1: #if it is the first line
                continue
            probLine=line.split("\t")
            nominator+=float(probLine[1].lstrip().rstrip())*float(probLine[0].lstrip().rstrip())
            denominator+=float(probLine[1])
    avg=nominator/denominator #just for the very last item in the ETC
    ETC[prevTaskType,prevMachine]=avg
#    print ETC
    
        
#TODO: be AWARE THAT ALL DATA SIZES FOR DIFFERENT ALPHAS(NOT TRIALS!) ARE THE SMAE. 
#IF YOU WANT DIFFEREMT CODE SHOULD
#BE CHANGED TO A LOOP THAT GENERATES ALL DIRECTIRIES (ALL ALPHAS) ARE GENERATED AT THE SAME TIME.
if __name__ == '__main__':
    intialize()
    random.seed(SEED)
    workload_name="trials_"+DEADLINE_GEN+str(ALPHA)
    os.makedirs(workload_name)
    #intialize()# this is just for prop deadline
    for i in range(1,NUM_TRIAL+1):
        path='final_en_tests_50k/inconsistent/sim'+str(i)+'/arrival'+str(i)+'.dat'
        fd = open(path, 'r')
        newFileName='trial_'+str(i)+'.dat'
        trialFile = os.path.join(os.getcwd(),workload_name,newFileName)
        newFile = open(trialFile, 'w')
        newFile.write('taskCount=2000;');
        lineCnt=0
        for line in fd:
            lineCnt=lineCnt+1
            stripped = line.lstrip()
            parts = stripped.split(",")
            taskType=int(parts[5].lstrip().rstrip()) - 1
        
            if DEADLINE_GEN=="tight":
                deadline=tight_deadline(taskType, parts)
            elif DEADLINE_GEN=="urgency":
                deadline=urgency_deadline(taskType, parts)
            elif DEADLINE_GEN=="prop":
                deadline=proportional_deadline(taskType,parts)
#generating data size
            #dataSize=getDataSize(MEANFILESIZE,VARIANCEFILESIZE)
            #print str(dataSize)
            assmbledLine = parts[2].lstrip().rstrip() + ' ' + str(taskType+1) +' '+str(deadline) +';\n'
            newFile.write(assmbledLine)
        firstLine='taskCount='+str(lineCnt)+';\n'
        newFile.seek(0)
        newFile.write(firstLine);
        fd.close()
        newFile.close()
        print 'all done'
