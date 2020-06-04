import csv

class Flower(object):
    def __init__(self,flowerName ,redGene, yellowGene, whiteGene, blueGene = 0 ):
        self.flowerName = flowerName
        self.GeneNumbers = [redGene, yellowGene, whiteGene, blueGene]
        self.GeneCode = geneCodeTranslator(self.GeneNumbers[0],self.GeneNumbers[1],self.GeneNumbers[2],self.GeneNumbers[3])
        self.colour = FlowerGeneColour[self.flowerName][self.GeneCode]

def geneCodeTranslator(red,yellow,white,blue):
    output = ""
    for R in range(2):
        if R < red:
            output +="R"
        else:
            output += "r"
    for Y in range(2):
        if Y < yellow:
            output += "Y"
        else:
            output += "y"
    for W in range(2):
        if W < white:
            output += "W"
        else:
            output += "w"
    for B in range(2):
        if B < blue:
            output += "B"
        else:
            output += "b"
    return output

def unique(inList):
    outList = []
    for item in inList:
        if item not in outList:
            outList.append(item)
    return outList

def breed(flower_1, flower_2):
    childflowers = {}
    if flower_1.flowerName == flower_2.flowerName:
        newFlowerGenes = []
        ListtoAppend = []
        for i in range(4):
            ListtoAppend.append(punnettSquare(flower_1.GeneNumbers[i],flower_2.GeneNumbers[i]))
        for REntry in ListtoAppend[0]:
            for YEntry in ListtoAppend[1]:
                for WEntry in ListtoAppend[2]:
                    for BEntry in ListtoAppend[3]:
                        newFlowerGenes.append([REntry, YEntry, WEntry, BEntry])
        #print(newFlowerGenes)
        uniqueFlowerGenes = unique(newFlowerGenes)
        #print(uniqueFlowerGenes)
        #print(uniqueFlowerGenes)
        probabilityList = {}
        for genes in uniqueFlowerGenes:
            ProbabilityIndex = geneCodeTranslator(genes[0], genes[1], genes[2], genes[3])
            probabilityList[ProbabilityIndex] = float(newFlowerGenes.count(genes))/float(len(newFlowerGenes))
        for genes in uniqueFlowerGenes:
            ProbabilityIndex = geneCodeTranslator(genes[0], genes[1], genes[2], genes[3])
            child = Flower(flower_1.flowerName,genes[0],genes[1],genes[2],genes[3])
            childflowers[child] = {}
            childflowers[child]["Probability"] = probabilityList[ProbabilityIndex]
            childflowers[child]["Parents"] = [flower_1, flower_2]

    return childflowers

def punnettSquare(GeneNumber_1, GeneNumber_2):
    output = []
    if GeneNumber_1 == 0:
        if GeneNumber_2 == 0:
            output = [0,0,0,0]
        elif GeneNumber_2 == 1:
            output = [0,0,1,1]
        elif GeneNumber_2 == 2:
            output = [1,1,1,1]
    elif GeneNumber_1 == 1:
        if GeneNumber_2 == 0:
            output = [0, 0, 1, 1]
        elif GeneNumber_2 == 1:
            output = [0, 1, 1, 2]
        elif GeneNumber_2 == 2:
            output = [1,1,2,2]
    elif GeneNumber_1 == 2:
        if GeneNumber_2 == 0:
            output = [1,1,1,1]
        elif GeneNumber_2 == 1:
            output = [1,1,2,2]
        elif GeneNumber_1 == 2:
            output = [2,2,2,2]

    return output

def IdentifyFlowersFromBreed(breed_list):
    output = []
    successList = []
    allfails = []
    failedOutput = []
    if len(breed_list) < 2:
        successList.append(list(breed_list)[0])
    else:
        for flowerE in list(breed_list):
            failedList = []
            Efailed = False
            testColour = flowerE.colour
            for flowerF in list(breed_list)[list(breed_list).index(flowerE)+1:]:
                if flowerF.colour == testColour and flowerF not in allfails:
                    Efailed = True
                    failedList.append(flowerF)
                    allfails.append(flowerF)
            if Efailed:
                allfails.append(flowerE)
                failedList.append(flowerE)
            if len(failedList) > 0:
                failedOutput.append([failedList, testColour])
        for flowerG in breed_list:
            if flowerG not in allfails:
                successList.append(flowerG)
    output = [successList, failedOutput]
    return output

def calculateTest(test):
    AllColours = []
    TestOutputs = {}
    for testChild in test:
        UniqueChildColours = []
        OutsideColourList = []
        testChildColourList = []
        for colour in test[testChild]:
            testChildColourList.append(colour) #gets all colours this test combo can produce
            AllColours.append(colour) #gives all colours to system
        for otherChild in test:
            if otherChild != testChild:
                for colour in test[otherChild]:
                    OutsideColourList.append(colour)
        for colour in testChildColourList:
            if colour not in OutsideColourList:
                UniqueChildColours.append(colour)
        TestOutputs[testChild] = {}
        for colour in UniqueChildColours:
            TestOutputs[testChild][colour] = {}
        for colour in UniqueChildColours:
            TestOutputs[testChild][colour] = test[testChild][colour]
    return TestOutputs #rewrite to take a dictionary input and prodce a dictionary of successful result colours

def IsFlowerNotDiscovered(testFlower, knownFlowerList):
    output = True
    for flowerX in knownFlowerList:
        if (testFlower.GeneCode == flowerX.GeneCode) and (testFlower.flowerName == flowerX.flowerName):
            output = False

    return output

def IsGroupingBreedAndNotGenomed(testGroup, UnGeneFlowerPool):
    output = False
    for grouping in UnGeneFlowerPool:
        if ((testGroup[2].flowerName == grouping[2].flowerName) and
            (grouping[2].GeneCode == testGroup[2].GeneCode) and (grouping[3].GeneCode == testGroup[3].GeneCode)):
            output = True

    return output

def IdentifyUngenedFlowers(ungenedFlowers, IdentifiedFlowers):
    for unidentifiedPool in ungenedFlowers:
        testResults = {}
        for flowerB in UpdatedFlowerPool:
            test = {}
            for flowerA in unidentifiedPool["Flowers"]:
                if flowerB.flowerName == flowerA.flowerName:
                    #print("--")
                    #print("New Test Flower")
                    potentialColours = {}
                    newFlowerPool = breed(flowerA, flowerB)
                    if len(newFlowerPool) > 0:
                        for flower in newFlowerPool:
                            potentialColours[flower.colour] = {}
                            potentialColours[flower.colour]["Flowers"] = []
                            potentialColours[flower.colour]["Probability"] = 0.0
                        for flower in newFlowerPool:
                            potentialColours[flower.colour]["Flowers"].append(flower)
                            potentialColours[flower.colour]["Probability"] += newFlowerPool[flower]["Probability"]
                        test[flowerA] = potentialColours
            if len(test) > 0:
                testResults[flowerB] = {}
                testResults[flowerB] = test
        for test in testResults:
            #print(test)
            interpretResults = calculateTest(testResults[test])
            #print(interpretResults)
            """print(
                interpretResults[1][0][0].colour + " children, of "
               + interpretResults[3].colour + " " +  interpretResults[3].flowerName + "s (" + interpretResults[3].GeneCode + ") and "
               + interpretResults[4].colour + " " +  interpretResults[4].flowerName + "s (" + interpretResults[4].GeneCode + ")"
               + ", when breed with " + interpretResults[0].colour + " " +  interpretResults[0].flowerName + " (" + interpretResults[0].GeneCode + ") "
                + "will themselves produce the following colours of children: " + ", ".join(map(str,interpretResults[2]))
            )"""
            for geneTest in interpretResults:
                #print(geneTest)
                if len(interpretResults[geneTest]) > 0:
                    """print(geneTest[0].colour + " " + geneTest[0].flowerName + " (" + geneTest[0].GeneCode
                    + ") children of "
               + interpretResults[3].colour + " " +  interpretResults[3].flowerName + "s (" + interpretResults[3].GeneCode + ") and "
               + interpretResults[4].colour + " " +  interpretResults[4].flowerName + "s (" + interpretResults[4].GeneCode
               + ") can be identified by having "+ ", ".join(map(str,geneTest[1])) + " children with "
                    + interpretResults[0].colour + " " +  interpretResults[0].flowerName + " (" + interpretResults[0].GeneCode + ") "
                    + "out of a colour pool of " + ", ".join(map(str,interpretResults[2])))"""

                    TestSuccessProbability = 0.0
                    for colour in interpretResults[geneTest]:
                        TestSuccessProbability += interpretResults[geneTest][colour]["Probability"]
                    IdentifiedFlowers[geneTest.flowerName][geneTest.GeneCode] = {}
                    IdentifiedFlowers[geneTest.flowerName][geneTest.GeneCode][geneTest] = {}
                    IdentifiedFlowers[geneTest.flowerName][geneTest.GeneCode][geneTest]["Probability"] = \
                    unidentifiedPool["Flowers"][geneTest]
                    IdentifiedFlowers[geneTest.flowerName][geneTest.GeneCode][geneTest]["Parents"] = unidentifiedPool["Parents"]
                    IdentifiedFlowers[geneTest.flowerName][geneTest.GeneCode][geneTest]["ID"] = IdentificationReasons[2]
                    IdentifiedFlowers[geneTest.flowerName][geneTest.GeneCode][geneTest]["Test Flower"] = {}
                    IdentifiedFlowers[geneTest.flowerName][geneTest.GeneCode][geneTest]["Test Flower"][test] = {}
                    IdentifiedFlowers[geneTest.flowerName][geneTest.GeneCode][geneTest]["Test Flower"][test]["Probability"] = TestSuccessProbability
                    IdentifiedFlowers[geneTest.flowerName][geneTest.GeneCode][geneTest]["Test Flower"][test]["Colours"] = [colour for colour in interpretResults[geneTest]]

def BreedNewFlowers(UpdatedFlowerPool, IdentifiedFlowers):
    for flowerA in UpdatedFlowerPool:
        for flowerB in UpdatedFlowerPool[UpdatedFlowerPool.index(flowerA):]:
            newFlowerPool = breed(flowerA, flowerB)
            if len(newFlowerPool) > 0:
                IdentifyedVector = IdentifyFlowersFromBreed(newFlowerPool)
                reason = ""
                isThisAnUpdate = ""
                if len(newFlowerPool) < 2:
                   reason = IdentificationReasons[0]
                else:
                   reason = IdentificationReasons[1]
                for flower in IdentifyedVector[0]:
                    if IsFlowerNotDiscovered(flower, UpdatedFlowerPool):
                        #ColourProbabilities = CalculateColourProbabilities(newFlowerPool)
                        IdentifiedFlowers[flower.flowerName][flower.GeneCode] = {}
                        IdentifiedFlowers[flower.flowerName][flower.GeneCode][flower] = {}
                        IdentifiedFlowers[flower.flowerName][flower.GeneCode][flower]["Probability"] =  newFlowerPool[flower]["Probability"]
                        IdentifiedFlowers[flower.flowerName][flower.GeneCode][flower]["Parents"] = [flowerA, flowerB]
                        IdentifiedFlowers[flower.flowerName][flower.GeneCode][flower]["ID"] = reason
                        """print("A " + flower.colour + " " + flower.flowerName +
                              " (" + flower.GeneCode + ") was the child of a "
                              + flowerA.colour + " " + flowerA.flowerName + " ("+ flowerA.GeneCode + ") and a "
                              + flowerB.colour + " " + flowerB.flowerName +" ("+ flowerB.GeneCode +
                              ") and was identified by " + reason + ". " + str(newFlowerPool[flower]["Probability"]))"""

                for failedGrouping in IdentifyedVector[1]:
                    failedDictionary = {}
                    failedDictionary["Flowers"] = {}
                    for flower in failedGrouping[0]:
                        failedDictionary["Flowers"][flower] = newFlowerPool[flower]["Probability"]
                    failedDictionary["Colour"] = failedGrouping[1]
                    failedDictionary["Parents"] = newFlowerPool[flower]["Parents"]
                    UngenedflowerPool.append(failedDictionary)

def SaveFlowers(UpdatedFlowerPool, IdentifiedFlowers):
    #for flower in IdentifiedFlowers:
        #if IsFlowerNotDiscovered(flower, UpdatedFlowerPool):
        #    UpdatedFlowerPool.append(flower)
            #print(flower.colour + " " + flower.flowerName + " " + flower.GeneCode)
     newFlowers = False
     for flowerName in IdentifiedFlowers:
         for Gene in IdentifiedFlowers[flowerName]:
             flowerToSave = None
             NeedsIDed = True
             maxProb = 0.0
             maxIDProb = 0.0
             IDFlower = None
             AdditionalReason = ""
             output = False
             for flower in IdentifiedFlowers[flowerName][Gene]:
                if IsFlowerNotDiscovered(flower, UpdatedFlowerPool):
                    output = True
                    if NeedsIDed and IdentifiedFlowers[flowerName][Gene][flower]["ID"] == IdentificationReasons[2]:
                        maxIDProbThisFlower = 0.0 #assigns a new target flow amoung flowers that MUST be identified through gene tests
                        MaxProbIDFlower = None
                        for testFlower in IdentifiedFlowers[flowerName][Gene][flower]["Test Flower"]: #Gets MaxID chance & associated flower
                            if IdentifiedFlowers[flowerName][Gene][flower]["Test Flower"][testFlower]["Probability"] > maxIDProbThisFlower:
                                maxIDProbThisFlower = IdentifiedFlowers[flowerName][Gene][flower]["Test Flower"][testFlower]["Probability"]
                                MaxProbIDFlower = testFlower
                        if IdentifiedFlowers[flowerName][Gene][flower]["Probability"] > maxProb: #If the new flower is easier to breed, the new flower will be our target
                            maxProb = IdentifiedFlowers[flowerName][Gene][flower]["Probability"]
                            flowerToSave = flower
                            maxIDProb = maxIDProbThisFlower
                            IDFlower = MaxProbIDFlower
                        elif(IdentifiedFlowers[flowerName][Gene][flower]["Probability"] == maxProb and maxIDProbThisFlower > maxIDProb):
                            flowerToSave = flower #If the new flower is easier to Identify, this new flower will be our target
                            maxIDProb = maxIDProbThisFlower
                            IDFlower = MaxProbIDFlower
                    else:
                        if NeedsIDed: #When we can avoid gene tests, we no long check gene test flowers
                            NeedsIDed = False
                            maxProb = 0.0
                        if IdentifiedFlowers[flowerName][Gene][flower]["Probability"] > maxProb: #If the new flower is easier to breed, the new flower is our new target
                            maxProb = IdentifiedFlowers[flowerName][Gene][flower]["Probability"]
                            flowerToSave = flower
             if(output):
                 if NeedsIDed:
                     AdditionalReason = "This flower is successfully Identified by breeding it with a " + IDFlower.colour + " "\
                     + IDFlower.flowerName + " (" + IDFlower.GeneCode + ") and getting children of the following colours: "\
                     + ", ".join(map(str,IdentifiedFlowers[flowerName][Gene][flowerToSave]["Test Flower"][IDFlower]["Colours"])) \
                     + ". These occur with a chance of " + str(maxIDProb)
                 print("A " + flowerToSave.colour + " " + flowerToSave.flowerName + " (" + flowerToSave.GeneCode + ") should be bred from a "
                 + IdentifiedFlowers[flowerName][Gene][flowerToSave]["Parents"][0].colour
                 + " " + IdentifiedFlowers[flowerName][Gene][flowerToSave]["Parents"][0].flowerName
                 + " (" + IdentifiedFlowers[flowerName][Gene][flowerToSave]["Parents"][0].GeneCode + ") and a "
                 + IdentifiedFlowers[flowerName][Gene][flowerToSave]["Parents"][1].colour
                 + " " + IdentifiedFlowers[flowerName][Gene][flowerToSave]["Parents"][1].flowerName
                 + " (" + IdentifiedFlowers[flowerName][Gene][flowerToSave]["Parents"][1].GeneCode + "). It has a " + str(maxProb)
                 + " chance of being bred. It can be identified by "
                 +   IdentifiedFlowers[flowerName][Gene][flowerToSave]["ID"] + ". " + AdditionalReason   )
                 UpdatedFlowerPool.append(flowerToSave)
     return output




def CalculateColourProbabilities(BreedList):
    colours = []
    totals = []
    output = {}
    for flower in BreedList:
        output[flower.colour] = 0.0
    for flower in BreedList:
        output[flower.colour] += BreedList[flower]["Probability"]
    for entryIndex in range(len(totals)):
        totals[entryIndex] = float(totals[entryIndex])/float(len(BreedList))
    #print(totals)
    for entryIndex in range(len(totals)):
        output[colours[entryIndex]] = totals[entryIndex]
    return output

GeneList = []

for b in range(3):
    for r in range(3):
        for y in range(3):
           for w in range(3):
               GeneList.append(geneCodeTranslator(r,y,w,b))

flowerList = ["Cosmo", "Hyacinth", "Lilly", "Mum", "Pansie", "Rose", "Tulip", "Windflower"]

Colours = ["White", "Pink", "Red", "Orange", "Yellow", "Green", "Blue",  "Purple", "Black"]

FlowerGeneColour = {flowerList[0]: {GeneList[0]: Colours[0],
                                     GeneList[1]: Colours[0],
                                     GeneList[2]: Colours[0],
                                     GeneList[3]: Colours[4],
                                     GeneList[4]: Colours[4],
                                     GeneList[5]: Colours[0],
                                     GeneList[6]: Colours[4],
                                     GeneList[7]: Colours[4],
                                     GeneList[8]: Colours[4],
                                     GeneList[9]: Colours[1],
                                     GeneList[10]: Colours[1],
                                     GeneList[11]: Colours[1],
                                     GeneList[12]: Colours[3],
                                     GeneList[13]: Colours[3],
                                     GeneList[14]: Colours[1],
                                     GeneList[15]: Colours[3],
                                     GeneList[16]: Colours[3],
                                     GeneList[17]: Colours[3],
                                     GeneList[18]: Colours[2],
                                     GeneList[19]: Colours[2],
                                     GeneList[20]: Colours[2],
                                     GeneList[21]: Colours[3],
                                     GeneList[22]: Colours[3],
                                     GeneList[23]: Colours[2],
                                     GeneList[24]: Colours[8],
                                     GeneList[25]: Colours[8],
                                     GeneList[26]: Colours[2]},
                    flowerList[1]: {GeneList[0]: Colours[0],
                                    GeneList[1]: Colours[0],
                                    GeneList[2]: Colours[6],
                                    GeneList[3]: Colours[4],
                                    GeneList[4]: Colours[4],
                                    GeneList[5]: Colours[0],
                                    GeneList[6]: Colours[4],
                                    GeneList[7]: Colours[4],
                                    GeneList[8]: Colours[4],
                                    GeneList[9]: Colours[2],
                                    GeneList[10]: Colours[1],
                                    GeneList[11]: Colours[0],
                                    GeneList[12]: Colours[3],
                                    GeneList[13]: Colours[4],
                                    GeneList[14]: Colours[4],
                                    GeneList[15]: Colours[3],
                                    GeneList[16]: Colours[4],
                                    GeneList[17]: Colours[4],
                                    GeneList[18]: Colours[2],
                                    GeneList[19]: Colours[2],
                                    GeneList[20]: Colours[2],
                                    GeneList[21]: Colours[6],
                                    GeneList[22]: Colours[6],
                                    GeneList[23]: Colours[2],
                                    GeneList[24]: Colours[7],
                                    GeneList[25]: Colours[7],
                                    GeneList[26]: Colours[7]},
                    flowerList[2]: {GeneList[0]: Colours[0],
                                    GeneList[1]: Colours[0],
                                    GeneList[2]: Colours[0],
                                    GeneList[3]: Colours[4],
                                    GeneList[4]: Colours[0],
                                    GeneList[5]: Colours[0],
                                    GeneList[6]: Colours[4],
                                    GeneList[7]: Colours[4],
                                    GeneList[8]: Colours[0],
                                    GeneList[9]: Colours[2],
                                    GeneList[10]: Colours[1],
                                    GeneList[11]: Colours[0],
                                    GeneList[12]: Colours[3],
                                    GeneList[13]: Colours[4],
                                    GeneList[14]: Colours[4],
                                    GeneList[15]: Colours[3],
                                    GeneList[16]: Colours[4],
                                    GeneList[17]: Colours[4],
                                    GeneList[18]: Colours[8],
                                    GeneList[19]: Colours[2],
                                    GeneList[20]: Colours[1],
                                    GeneList[21]: Colours[8],
                                    GeneList[22]: Colours[2],
                                    GeneList[23]: Colours[1],
                                    GeneList[24]: Colours[3],
                                    GeneList[25]: Colours[3],
                                    GeneList[26]: Colours[0]},
                    flowerList[3]: {GeneList[0]: Colours[0],
                                    GeneList[1]: Colours[0],
                                    GeneList[2]: Colours[7],
                                    GeneList[3]: Colours[4],
                                    GeneList[4]: Colours[4],
                                    GeneList[5]: Colours[0],
                                    GeneList[6]: Colours[4],
                                    GeneList[7]: Colours[4],
                                    GeneList[8]: Colours[4],
                                    GeneList[9]: Colours[1],
                                    GeneList[10]: Colours[1],
                                    GeneList[11]: Colours[1],
                                    GeneList[12]: Colours[4],
                                    GeneList[13]: Colours[2],
                                    GeneList[14]: Colours[1],
                                    GeneList[15]: Colours[7],
                                    GeneList[16]: Colours[7],
                                    GeneList[17]: Colours[7],
                                    GeneList[18]: Colours[2],
                                    GeneList[19]: Colours[2],
                                    GeneList[20]: Colours[2],
                                    GeneList[21]: Colours[7],
                                    GeneList[22]: Colours[7],
                                    GeneList[23]: Colours[2],
                                    GeneList[24]: Colours[5],
                                    GeneList[25]: Colours[5],
                                    GeneList[26]: Colours[2]},
                    flowerList[4]: {GeneList[0]: Colours[0],
                                    GeneList[1]: Colours[0],
                                    GeneList[2]: Colours[6],
                                    GeneList[3]: Colours[4],
                                    GeneList[4]: Colours[4],
                                    GeneList[5]: Colours[6],
                                    GeneList[6]: Colours[4],
                                    GeneList[7]: Colours[4],
                                    GeneList[8]: Colours[4],
                                    GeneList[9]: Colours[2],
                                    GeneList[10]: Colours[2],
                                    GeneList[11]: Colours[4],
                                    GeneList[12]: Colours[3],
                                    GeneList[13]: Colours[3],
                                    GeneList[14]: Colours[3],
                                    GeneList[15]: Colours[4],
                                    GeneList[16]: Colours[4],
                                    GeneList[17]: Colours[4],
                                    GeneList[18]: Colours[2],
                                    GeneList[19]: Colours[2],
                                    GeneList[20]: Colours[7],
                                    GeneList[21]: Colours[2],
                                    GeneList[22]: Colours[2],
                                    GeneList[23]: Colours[7],
                                    GeneList[24]: Colours[3],
                                    GeneList[25]: Colours[3],
                                    GeneList[26]: Colours[7]},
                    flowerList[5]: {GeneList[0]: Colours[0],
                                    GeneList[1]: Colours[0],
                                    GeneList[2]: Colours[7],
                                    GeneList[3]: Colours[4],
                                    GeneList[4]: Colours[0],
                                    GeneList[5]: Colours[7],
                                    GeneList[6]: Colours[4],
                                    GeneList[7]: Colours[4],
                                    GeneList[8]: Colours[0],
                                    GeneList[9]: Colours[2],
                                    GeneList[10]: Colours[2],
                                    GeneList[11]: Colours[2],
                                    GeneList[12]: Colours[3],
                                    GeneList[13]: Colours[2],
                                    GeneList[14]: Colours[2],
                                    GeneList[15]: Colours[3],
                                    GeneList[16]: Colours[3],
                                    GeneList[17]: Colours[2],
                                    GeneList[18]: Colours[8],
                                    GeneList[19]: Colours[8],
                                    GeneList[20]: Colours[8],
                                    GeneList[21]: Colours[3],
                                    GeneList[22]: Colours[2],
                                    GeneList[23]: Colours[8],
                                    GeneList[24]: Colours[3],
                                    GeneList[25]: Colours[3],
                                    GeneList[26]: Colours[6],
                                    GeneList[27]: Colours[0],
                                    GeneList[28]: Colours[0],
                                    GeneList[29]: Colours[7],
                                    GeneList[30]: Colours[4],
                                    GeneList[31]: Colours[0],
                                    GeneList[32]: Colours[7],
                                    GeneList[33]: Colours[4],
                                    GeneList[34]: Colours[4],
                                    GeneList[35]: Colours[0],
                                    GeneList[36]: Colours[1],
                                    GeneList[37]: Colours[1],
                                    GeneList[38]: Colours[1],
                                    GeneList[39]: Colours[4],
                                    GeneList[40]: Colours[1],
                                    GeneList[41]: Colours[1],
                                    GeneList[42]: Colours[4],
                                    GeneList[43]: Colours[4],
                                    GeneList[44]: Colours[1],
                                    GeneList[45]: Colours[2],
                                    GeneList[46]: Colours[2],
                                    GeneList[47]: Colours[2],
                                    GeneList[48]: Colours[3],
                                    GeneList[49]: Colours[2],
                                    GeneList[50]: Colours[2],
                                    GeneList[51]: Colours[3],
                                    GeneList[52]: Colours[3],
                                    GeneList[53]: Colours[2],
                                    GeneList[54]: Colours[0],
                                    GeneList[55]: Colours[0],
                                    GeneList[56]: Colours[7],
                                    GeneList[57]: Colours[4],
                                    GeneList[58]: Colours[0],
                                    GeneList[59]: Colours[7],
                                    GeneList[60]: Colours[4],
                                    GeneList[61]: Colours[4],
                                    GeneList[62]: Colours[0],
                                    GeneList[63]: Colours[0],
                                    GeneList[64]: Colours[0],
                                    GeneList[65]: Colours[7],
                                    GeneList[66]: Colours[4],
                                    GeneList[67]: Colours[0],
                                    GeneList[68]: Colours[7],
                                    GeneList[69]: Colours[4],
                                    GeneList[70]: Colours[4],
                                    GeneList[71]: Colours[0],
                                    GeneList[72]: Colours[1],
                                    GeneList[73]: Colours[1],
                                    GeneList[74]: Colours[1],
                                    GeneList[75]: Colours[4],
                                    GeneList[76]: Colours[0],
                                    GeneList[77]: Colours[7],
                                    GeneList[78]: Colours[4],
                                    GeneList[79]: Colours[4],
                                    GeneList[80]: Colours[0],
                                    },
                    flowerList[6]: {GeneList[0]: Colours[0],
                                    GeneList[1]: Colours[0],
                                    GeneList[2]: Colours[0],
                                    GeneList[3]: Colours[4],
                                    GeneList[4]: Colours[4],
                                    GeneList[5]: Colours[0],
                                    GeneList[6]: Colours[4],
                                    GeneList[7]: Colours[4],
                                    GeneList[8]: Colours[4],
                                    GeneList[9]: Colours[2],
                                    GeneList[10]: Colours[1],
                                    GeneList[11]: Colours[0],
                                    GeneList[12]: Colours[3],
                                    GeneList[13]: Colours[4],
                                    GeneList[14]: Colours[4],
                                    GeneList[15]: Colours[3],
                                    GeneList[16]: Colours[4],
                                    GeneList[17]: Colours[4],
                                    GeneList[18]: Colours[8],
                                    GeneList[19]: Colours[2],
                                    GeneList[20]: Colours[2],
                                    GeneList[21]: Colours[8],
                                    GeneList[22]: Colours[2],
                                    GeneList[23]: Colours[2],
                                    GeneList[24]: Colours[7],
                                    GeneList[25]: Colours[7],
                                    GeneList[26]: Colours[7]},
                    flowerList[7]: {GeneList[0]: Colours[0],
                                    GeneList[1]: Colours[0],
                                    GeneList[2]: Colours[6],
                                    GeneList[3]: Colours[3],
                                    GeneList[4]: Colours[3],
                                    GeneList[5]: Colours[6],
                                    GeneList[6]: Colours[3],
                                    GeneList[7]: Colours[3],
                                    GeneList[8]: Colours[3],
                                    GeneList[9]: Colours[2],
                                    GeneList[10]: Colours[2],
                                    GeneList[11]: Colours[6],
                                    GeneList[12]: Colours[1],
                                    GeneList[13]: Colours[1],
                                    GeneList[14]: Colours[1],
                                    GeneList[15]: Colours[3],
                                    GeneList[16]: Colours[3],
                                    GeneList[17]: Colours[3],
                                    GeneList[18]: Colours[2],
                                    GeneList[19]: Colours[2],
                                    GeneList[20]: Colours[7],
                                    GeneList[21]: Colours[2],
                                    GeneList[22]: Colours[2],
                                    GeneList[23]: Colours[7],
                                    GeneList[24]: Colours[1],
                                    GeneList[25]: Colours[1],
                                    GeneList[26]: Colours[7]},
                    }

initialflowerPool = [
    Flower(flowerList[0],0,0,1),
    Flower(flowerList[0],0,2,1),
    Flower(flowerList[0],2,0,0),
    Flower(flowerList[1],0,0,1),
    Flower(flowerList[1],0,2,0),
    Flower(flowerList[1],2,0,1),
    Flower(flowerList[2],0,0,2),
    Flower(flowerList[2],0,2,0),
    Flower(flowerList[2],2,0,1),
    Flower(flowerList[3],0,0,1),
    Flower(flowerList[3],0,2,0),
    Flower(flowerList[3],2,0,0),
    Flower(flowerList[4],0,0,1),
    Flower(flowerList[4],0,2,0),
    Flower(flowerList[4],2,0,0),
    Flower(flowerList[5],0,0,1,0),
    Flower(flowerList[5],0,1,0,0),
    Flower(flowerList[5],2,0,0,1),
    Flower(flowerList[6],0,0,1),
    Flower(flowerList[6],0,2,0),
    Flower(flowerList[6],2,0,1),
    Flower(flowerList[7],0,0,1),
    Flower(flowerList[7],0,2,0),
    Flower(flowerList[7],2,0,0)
]

IdentificationReasons = ["Uniqueness", "Colour", "Gene Test"]


newFlowers = True
UpdatedFlowerPool = initialflowerPool[:]
UngenedflowerPool = []
newFlowerPool = []
generation = 0
print(len(UpdatedFlowerPool))
while (newFlowers):
    print(generation)
    generation += 1
#if (newFlowers):
    IdentifiedFlowers = {}
    for flower in flowerList:
        IdentifiedFlowers[flower] = {}



    BreedNewFlowers(UpdatedFlowerPool, IdentifiedFlowers)
    IdentifyUngenedFlowers(UngenedflowerPool, IdentifiedFlowers)

    newFlowers = SaveFlowers(UpdatedFlowerPool, IdentifiedFlowers)

print(len(UpdatedFlowerPool))

listOfAllFlowers = []

for flowerName in flowerList:
    if flowerName == "Rose":
        for b in range(3):
            for r in range(3):
                for y in range(3):
                    for w in range(3):
                        listOfAllFlowers.append(Flower(flowerName, r,y,w,b))
    else:
        for r in range(3):
            for y in range(3):
                for w in range(3):
                    listOfAllFlowers.append(Flower(flowerName, r,y,w))
"""listOfUnidentifiedFlowers = []
for flower in listOfAllFlowers:
    if IsFlowerNotDiscovered(flower, UpdatedFlowerPool):
        listOfUnidentifiedFlowers.append(flower)

listOfUnidentifiedFlowers = unique(listOfUnidentifiedFlowers)
for flower in listOfUnidentifiedFlowers:
    print(flower.colour + " " + flower.flowerName + " (" + flower.GeneCode + ")")"""







# Run through flower list (without repeats)
# Identify identifiable flowers
# Repeat
# Identify Flowers which need gene tested
# Run Needs-Gene-Tested flowers against known gened plants
# Identify identifiable flowers
# Identify Flowers which need gene tested
# Repeat until no new flowers are found
# Replace simple "flower" list with Gene dictionary
# The gene dictionary refers to a list: [flower, probability, parents?, generation?]
# When choosing the flower to add to the final flower list, we pick the flower with the highest probability of getting the desired flower

#Finish geneTesting output to append the correct stuff: parents of flower, test candidate, probability of appearing from parents, probability of being identified, etc.
#Move new flower announcements to when they get appended to the Known flowers list
#Generate code for adding gene tested flowers to flower pool.
#Think about further tests for unidentified flowers.

print("Compiled successfully!")



