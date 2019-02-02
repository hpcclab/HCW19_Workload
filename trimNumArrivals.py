import os
import sys
NUM_TRIAL=30

if len(sys.argv) > 2:
    baseFilename = sys.argv[1]
    numTasks = int(sys.argv[2])
else:
    print("Please run script with 2 arguments.")
    print("1st arg is base directory and filename beginning e.g. ./trials/trial_")
    print("2nd arg is number of trials to leave")


if __name__ == '__main__':
    for i in range(1,NUM_TRIAL+1):
        toWrite=""
        path=baseFilename + str(i)+'.dat'
        fd = open(path, 'r')
        line = fd.readline()
        line = toWrite + "taskCount="+str(numTasks)+";\n"
        counter = -1 #because first line is not a trial
        while line:
            counter += 1
            if counter <= numTasks:
                print(counter)
                toWrite = toWrite + line
            line = fd.readline()

        fd.close()
        fd = open(path, 'w')
        for line in toWrite:
            fd.write(line)
        fd.close()
        print 'all done'
