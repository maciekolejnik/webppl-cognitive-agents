params = []

for i in range(10):
    filename = "examples/tipping/data/generatedData15r/simulation" + str(i) + ".txt" 
    with open(filename,"r") as f:
        content = f.readlines()
        # need to get goal coeffs (line 1), tipping norm + gasp score (line 4)
        firstLine = content[0]
        a = firstLine.find("[")
        b = firstLine.find(",")
        moneyCoeff = float(firstLine[a+1:b])
        tippingNorm = int(content[3].split(";")[0])
        gaspScore = int(content[3].split(";")[2])
        params.append([moneyCoeff, tippingNorm, gaspScore])

# now we should have all the params in a list
# print(params)
# print("\n\n\n")

posterior = []
with open("examples/tipping/results/generatedInfer15r.txt", "r") as f:
    content = f.readlines()
    lineNo = 3
    simNo = 0
    while lineNo < len(content):
        # process next simulation
        while not content[lineNo].startswith("abi"):
            lineNo += 1
        lineNo += 1
        # now we are at goal coeffs
        goalCoeffProbs = []
        while not content[lineNo].startswith("tipping"):
            line = content[lineNo]
            indexOfFirstComma = line.find(",")
            indexOfSecondComma = line.rfind(",")
            indexOfLastChar = line.find(")")
            moneyCoeff = float(line[2:indexOfFirstComma])
            prob = float(line[indexOfSecondComma+1:indexOfLastChar])
            goalCoeffProbs.append([moneyCoeff, 1/6])
            # goalCoeffProbs.append([moneyCoeff, prob])
            lineNo += 1
        lineNo += 1
        # now we are at tipping norm
        normProbs = []
        while not content[lineNo].startswith("gasp"):
            line = content[lineNo]
            pair = line.rstrip()[1:-1].split(",")
            norm = int(pair[0])
            prob = float(pair[1])
            normProbs.append([norm,1/5])
            # normProbs.append([norm,prob])
            lineNo += 1
        lineNo += 1
        # now we are at gasp score
        gaspProbs = []
        while not content[lineNo].startswith("undefined"):
            line = content[lineNo]
            pair = line.rstrip()[1:-1].split(",")
            gasp = int(pair[0])
            prob = float(pair[1])
            # gaspProbs.append([gasp, prob])
            gaspProbs.append([gasp, 1/4])
            lineNo += 1
        lineNo += 1
        simNo += 1
        posterior.append([goalCoeffProbs, normProbs, gaspProbs])

# print(posterior)

print("should be equal:")
print(len(params))
print(len(posterior))

pmses = []
tops = []

for (values, predictions) in zip(params, posterior):
    l = []
    t = []
    for (value, prediction) in zip(values, predictions):
        topPrediction = prediction[0][0]
        t.append(int(abs(topPrediction - value) <= 0.1))
        # if abs(topPrediction - value) <= 0.1:
        #     t.append(1)
        # else:
        #     t.append(0)
        pmse = 0
        for pair in prediction:
            prob = pair[1]
            predVal = pair[0]
            pmse += prob * pow(value - predVal, 2)
        l.append(pmse)
    pmses.append(l)
    tops.append(t)

# print(pmses)
# print(tops)

# pmses holds all the... pmses, as a list of 3 element lists
# tops has the same format but holds 1 or 0

def sumElementWise(arrayOfArrays):
    result = [0,0,0]
    for array in arrayOfArrays:
        result = [sum(x) for x in zip(result, array)]
    return result

# pmsesSum = [0,0,0]
# for pmse in pmses:
#     pmsesSum = [sum(x) for x in zip(pmsesSum, pmse)]

pmsesSum = sumElementWise(pmses)
n = len(pmses)
averagePmses = [x / n for x in pmsesSum]
print("mean averages:")
print(averagePmses)

# compute mean pmses
l = [[],[],[]]
for pmse in pmses:
    for i in range(len(pmse)):
        l[i].append(pmse[i])

from statistics import median
def computeMedian(list):
    return median(list)

medians = list(map(median, l))
# medians = list(map(computeMedian, l))

print("medians:")
print(medians)


topsSums = sumElementWise(tops)
print("binary:")
print(topsSums)

