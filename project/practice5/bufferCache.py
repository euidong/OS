import random
import time


class freeBlock():
    def __init__(self, next, back, data, state):
        self.next = next
        self.back = back
        self.data = data
        self.state = state
    
    def getSize(self):
        header =self.next
        count = 0
        while header != self:
            count+=1
            header = header.next
        return count

def setInit(modNumber, blockNum, busyList):
    hashQueue = [[] for i in range(modNumber)]
    freeHeader = freeBlock(None, None, "header", 'Free')

    for i in range(blockNum):
        block = random.randrange(0,100)
        isExist = False
        for hBlock in hashQueue[block % modNumber]:
            if hBlock[0] == block:
                isExist = True
        if not isExist:
            if i % 5 == 0:
                if freeHeader.back != None:
                    newFree = freeBlock(freeHeader, freeHeader.back, block, 'Free')
                    freeHeader.back.next = newFree
                    freeHeader.back = newFree
                else:
                    newFree = freeBlock(freeHeader, freeHeader, block, 'Free')
                    freeHeader.next = newFree
                    freeHeader.back = newFree
                hashQueue[block % modNumber].append([block,'Free'])
            else:        
                hashQueue[block % modNumber].append([block,'Busy'])
                busyList.append([block, random.randrange(1,10)])
    return hashQueue, freeHeader

def makeDelay(freeHeader):
    size = freeHeader.getSize()
    if size != 0:
        randFree = random.randrange(0,size)
        block = freeHeader.next
        for i in range(randFree):
            block = block.next     
         
        if block.state == 'Free':
            block.state = 'Delay'

def makeBusy(hashQueue, FreeHeader, busyList):
    size = FreeHeader.getSize()
    if size > 0:
        randNum =random.randrange(0, size)
        target = FreeHeader.next
        for i in range(randNum):
            target = target.next
        target.back.next = target.next
        target.next.back = target.back
        hashIndex = target.data % len(hashQueue)
        busyList.append([target.data, random.randrange(1, 10)])
        for i in range(len(hashQueue[hashIndex])):
            if hashQueue[hashIndex][i][0] == target.data:
                hashQueue[hashIndex][i][1] = 'Busy'
        
    

def makeFree(hashQueue, FreeHeader, busyList):
    allDeleted = False
    while not allDeleted:
        for busyBlock in busyList:
            if busyBlock[1] <= 0:
                hashIndex = busyBlock[0] % len(hashQueue)
                for i in range(len(hashQueue[hashIndex])):
                    if hashQueue[hashIndex][i][0] == busyBlock[0]:
                        hashQueue[hashIndex][i][1] = 'Free'
                        busyList.remove(busyBlock)
                        if freeHeader.back != None:
                            newFree = freeBlock(freeHeader, freeHeader.back, hashQueue[hashIndex][i][0], 'Free')
                            freeHeader.back.next = newFree
                            freeHeader.back = newFree
                        else:
                            newFree = freeBlock(freeHeader, freeHeader, hashQueue[hashIndex][i][0], 'Free')
                            freeHeader.next = newFree
                            freeHeader.back = newFree
                        break
        allDeleted = True
        for busyBlock in busyList:
            if busyBlock[1] <= 0:
                allDeleted = False     

def getBlock(requestBlock, hashQueue, freeHeader, busyList):
    hashIndex = requestBlock % len(hashQueue)
    isExist = False
    for i in range(len(hashQueue[hashIndex])):
        if hashQueue[hashIndex][i][0] == requestBlock:
            isExist = True
            if hashQueue[hashIndex][i][1] == 'Busy':
                print("Senario 5 : request block(" +str(requestBlock) + ") is Busy", end=' ')
                for busyBlock in busyList:
                    if busyBlock[0] == requestBlock:
                        print("wait " + str(busyBlock[1]) +"s")
                return 'Senario_5'
            else:
                free = freeHeader.next
                while free.data != hashQueue[hashIndex][i][0]:
                    free = free.next
                free.back.next = free.next
                free.next.back = free.back
                hashQueue[hashIndex][i][1] = 'Busy'
                busyList.append([requestBlock, random.randrange(1,10)])
                print("Senario 1 : make Free block(" +str(requestBlock) + ") Busy") 
                return 'Senario_1'
    if not isExist:
        if freeHeader.next == freeHeader:
            print("Senario 4 : free Block(" +str(requestBlock) + ") is not exist")
            return 'Senario_4'
        else:
            free = freeHeader.next
            freeHeader.next = free.next
            free.next.back = freeHeader

            hashIndex = free.data % len(hashQueue)
            
            if free.state == 'Delay':
                for i in range(len(hashQueue[hashIndex])):
                    if hashQueue[hashIndex][i][0] == free.data:
                        hashQueue[hashIndex][i][1] = 'Busy'
                        busyList.append([free.data, random.randrange(1, 10)])
                print("Senario 3 : delay data(" +str(requestBlock) + ") writing")            
                return 'Senario_3'
            else :
                hashQueue[hashIndex].remove([free.data, 'Free'])
                hashIndex = requestBlock % len(hashQueue)
                hashQueue[hashIndex].append([requestBlock, 'Busy'])
                busyList.append([requestBlock, random.randrange(1, 10)])
                print("Senario 2 : allocate new block(" +str(requestBlock) + ")")
                return 'Senario_2'

busyList = []
hashQueue, freeHeader = setInit(10, 30, busyList)

senarioList = [False] * 5

complete = False
Execute = True

counter = 0
while not complete:
    freeSize = freeHeader.getSize()
    if senarioList[0] and senarioList[1] and senarioList[2] and senarioList[4] and Execute:
        print("\nTo show senario 4 I make " + str(freeSize) +" buffer busy")
        for i in range(freeSize):
            makeBusy(hashQueue, freeHeader, busyList)

    hashValue = len(hashQueue)
    print("Hash Queue state-----------------")
    for i in range(hashValue):
        print("x mod " + str(hashValue) + "= " + str(i), end='')
        print(hashQueue[i])
    freeSize = freeHeader.getSize()
    print("\nFree List state------------------",end='\n-')
    if freeSize == 0:
        print("Empty")

    while(freeHeader.next.data != "header"):
        freeHeader = freeHeader.next
        print('['+str(freeHeader.data)+ ' ' +freeHeader.state,end=']-')
    freeHeader = freeHeader.next
    print()
    counter +=1


    complete = True
    if Execute:
        rand = random.randint(0, 100) 
    
    print("\nDo allocate " + str(rand) + "-------------------")
    result = getBlock(rand, hashQueue, freeHeader, busyList) 
    
    if result == 'Senario_1':
        senarioList[0] = True
        Execute = True
    
    if result == 'Senario_2':
        senarioList[1] = True
        Execute = True
        
    if result == 'Senario_3':
        senarioList[2] = True
        Execute = False
    
    if result == 'Senario_4':
        senarioList[3] = True
        Execute = False
        
    if result == 'Senario_5':
        senarioList[4] = True
        Execute = False       

    for senario in senarioList:
        if not senario:
            complete = False
            break
    if counter % 5 == 0:
        makeBusy(hashQueue, freeHeader, busyList)
        makeDelay(freeHeader)
    for busy in busyList:
        busy[1] -= 1
    
    makeFree(hashQueue, freeHeader, busyList)
    makeBusy(hashQueue, freeHeader, busyList)
    print("\n")
    time.sleep(1)
print("총 할당 횟수 :" + str(counter))