import itertools

def findFItem(recipeTrans, sup):
    itemDict = {}
    fitems = {}
    for recipe in recipeTrans:
        for herb in recipe:
            if herb in itemDict.keys():
               itemDict[herb]+=1
            else:
                itemDict[herb]=1
    for item in itemDict.keys():
        if itemDict[item]>=sup:
            fitems[item]=itemDict[item]
    return fitems

def findFSet(recipeTrans, items, len, sup):
    setDict = {}
    fset = {}
    candiSet = list(getCandidate(items,len))
    for recipe in recipeTrans:
        for candidate in candiSet:
            if set(candidate)<=set(recipe):
                if candidate in setDict.keys():
                    setDict[candidate]+=1
                else:
                    setDict[candidate]=1
    for herbset in setDict:
        if setDict[herbset]>=sup:
            fset[herbset]=setDict[herbset]
    return fset

def getCandidate(items, len):
    candiSet = itertools.combinations(items, len)
    return candiSet

def getItemInSet(frequentSet):
    items = []
    for fset in frequentSet:
        for item in fset:
            if item not in items:
               items.append(item)
    return items