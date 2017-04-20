import itertools

def findFItem(recipeTrans, w4herblist, sup):
    itemDict = {}
    fitems = {}
    for i in range(0, len(recipeTrans)):
        recipe = recipeTrans[i]
        for item in recipe:
            if item in itemDict:
                w4herb = w4herblist[i]
                if int(w4herb[recipe.index(item)])==1:
                    itemDict[item]+=1
                else:
                    itemDict[item]+=2
            else:
                w4herb = w4herblist[i]
                if int(w4herb[recipe.index(item)])==1:
                    itemDict[item]=1
                else:
                    itemDict[item]=2
    for item in itemDict.keys():
        if itemDict[item]>=sup:
            fitems[item]=itemDict[item]
    return fitems

def findFSet(recipeTrans, items, w4herblist, size, sup):
    setDict = {}
    fset = {}
    flag=True
    candiSet = list(getCandidate(items,size))
    for i in range(0, len(candiSet)):
        setDict[candiSet[i]]=0
    for i in range(0, len(recipeTrans)):
        recipe=recipeTrans[i]
        for j in range(0,len(candiSet)):
            candidate=candiSet[j]
            if set(candidate)<=set(recipe):
                w4herb=w4herblist[i]
                for item in candidate:
                    if int(w4herb[recipe.index(item)])==1:
                        setDict[candidate]+=1
                        flag=False
                        break
                if flag:
                    setDict[candidate]+=2
            flag=True
    for herbset in setDict:
        if setDict[herbset]>=sup:
            fset[herbset]=setDict[herbset]
    return fset

def countset_w(recipeTrans, w4herblist, fset):
    count = 0
    flag = True
    for i in range(0, len(recipeTrans)):
        recipe = recipeTrans[i]
        if set(fset)<=set(recipe):
            w4herb = w4herblist[i]
            for item in fset:
                if int(w4herb[recipe.index(item)]) == 1:
                    count += 1
                    flag = False
                    break
            if flag:
                count += 2
        flag=True
    return count

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
