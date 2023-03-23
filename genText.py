# Joel h 4/07-2020
import random
from functions import tokenize, countSeq, printTopMost, genStringCondLong, calcProbabilities, randSeq, randCharacter
import numpy as np
import matplotlib.pyplot as plt

def plotFailure():
    fileName = 'thetrial.txt'
    fileNameStopSigns = 'stopSign.txt'

    with open(fileNameStopSigns, 'r') as f:
        stopChars = set(f.read().split())

    correlationMax = 10
    failures = np.zeros(correlationMax-1)
    corrLength = []
    textLength = 100
    nTrials = 200
    inp_file = open(fileName, "r", encoding="utf-8")
    #correlation=3

    for correlation in range(2,correlationMax+1):
        corrLength.append(str(correlation))
        print(correlation)
        inp_file = open(fileName, "r", encoding="utf-8")
        words = (tokenize(inp_file,correlation,stopChars))
        # perform counting and sorting
        dic = countSeq(words)
        prob = calcProbabilities(dic)

        inp_file.close()
        for i in range(nTrials):
            #Pick a random line and make sure length is longer than correlation (there are blank rows)
            line = random.choice(open(fileName).readlines())
            line = ''.join(c for c in line if c not in stopChars)
            while len(line) < correlation:
                line = random.choice(open(fileName).readlines())
                line = ''.join(c for c in line if c not in stopChars)
            line = line[:-1]
            #print('"',line,'"')
            startWord = randSeq(line,correlation)

            test = genStringCondLong(prob,textLength,correlation,startWord)
            if len(test) != (textLength+correlation-1):
                #print(len(test),'\t',textLength+correlation-1)
                failures[correlation-2]+=1
        failures[correlation-2]=failures[correlation-2]/nTrials
        print(failures)
        print(corrLength)
    fig = plt.figure()
    ax = fig.add_subplot(111)    
    ax.bar(corrLength,failures)
    plt.ylabel('Fraction of failed text generation')
    plt.xlabel('Correlation length')
    plt.show()


def main():
    correlation = 7
    fileName = 'thetrial.txt'
    fileNameStopSigns = 'stopSign.txt'

    with open(fileNameStopSigns, 'r') as f:
        stopChars = set(f.read().split())

    inp_file = open(fileName, "r", encoding="utf-8")
    words = (tokenize(inp_file,correlation,stopChars))
    

    # perform counting and sorting
    dic = countSeq(words)
    #print(dic)
    #printTopMost(dic,10)
    prob = calcProbabilities(dic)
    #print(prob)


    # FOr case correlation 1 (random signs based on individual characters)
    # corr1 = ''
    # for i in range(50):
    #     new = randCharacter(prob)
    #     while new == '\n' or new == '\t':
    #         new = randCharacter(prob)
    #     corr1+=new
    # print('start\n',corr1,'\nend')
    # print(len(corr1))
    


    #Pick a random line and make sure length is longer than correlation (there are blank rows)
    line = random.choice(open(fileName).readlines())
    line = ''.join(c for c in line if c not in stopChars)
    while len(line) < correlation:
        line = random.choice(open(fileName).readlines())
        line = ''.join(c for c in line if c not in stopChars)
    startWord = randSeq(line,correlation)
    #print(test)
    inp_file.close()

    test = genStringCondLong(prob,50,correlation,startWord)
    print('start\n\n',len(test),test,'\n\nend')

    

#main()
plotFailure()
