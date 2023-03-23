# Some functions like tokenize are based on functions in
# https://github.com/joelhil/Topmost-Words
# large and small letters combined at start!

from random import random,uniform,randint

def tokenize(lines,seqLength,stopChars):
    sequences = []
    for line in lines:
        line = ''.join(c for c in line if c not in stopChars)

        for n in range(1,seqLength+1):
            start = 0
            end = 0
            line = line + " "
            # if start is shorter than the length of line
            while start < len(line) and end < len(line):
                sequences.append(line[start:start+n])
                start+=1
                #end = start+n
    return sequences

def randSeq(line,seqLength):
    text = ''

    start = randint(0,len(line)-seqLength)
    text= line[start:start+seqLength].lower()

    return text



def countSeq(sequences):
    seqAmount = {}
    for seq in sequences:
        #if character.isupper():
        seq = seq.lower()
        if seq != '\n':
            if seq not in seqAmount:
                seqAmount[seq] = 1
            elif seq in seqAmount:
                seqAmount[seq] = int(seqAmount[seq])+1

    return seqAmount


def printTopMost(frequencies, n):
    count = 0
    for word, freq in sorted(frequencies.items(), key=lambda x: -x[1]):
        if count < n:
            print(word.ljust(20)+str(freq).rjust(5))
            count = count + 1

# Calculate probability of each sequence
def calcProbabilities(wordDict):
    probabilities = {}
    sum = 0
    for word, freq in sorted(wordDict.items(), key=lambda x: -x[1]):
        sum += freq
    for word, freq in sorted(wordDict.items(), key=lambda x: -x[1]):
        probabilities[word] = freq/sum
    return probabilities

# Generate a string based on probabilties of characters
# like roulette-wheel selection
def genString(probabilities,length):
    text = ""
    for i in range(length):
        pSum = 0
        p = random()
        for character in probabilities:
            pSum += probabilities[character]
            if p < pSum:
                text += character
                break
    return text


# Generate a character given a distribution
# if sum of probabilties in distribution is not 1
# it is normalised
def randCharacter(probabilities):
    char = ''
    pSum = 0
    sum=0
    for character in probabilities:
        sum += probabilities[character]
    p = uniform(0,sum)
    for character in probabilities:
        pSum += probabilities[character]
        if p < pSum:
            char = character
            break
    # if char == '':
    #     print(p, '\t', pSum)
    return char


# Generate a string based on probabilties of characters given a character
def genStringCondLong(probabilities,length,lcorr,startWord):
    text = startWord
    for i in range(len(text)-lcorr+1, length):
        # Generate the conditional probability distribution
        alfaProb = {}
        alfa = text[i:i+lcorr-1]
        for key in probabilities:
            if key[0:lcorr-1] == alfa and len(key) > lcorr-1:
                # Should add stopsigns
                #print(alfa,'\t',key)
                
                if key[lcorr-1]!='\n' and key[lcorr-1] != '"' and key[lcorr-1] != ';' and key[lcorr-1] != '-' and key[lcorr-1] != ':':
                    #print('alfa: "',alfa,'"\tkey: "',key,'"\tstartWord "',startWord,'"')
                    alfaProb[key[lcorr-1]] = probabilities[key]/probabilities[alfa]
        #print(alfa, '\n',alfaProb)
        text+=randCharacter(alfaProb)

    return text

