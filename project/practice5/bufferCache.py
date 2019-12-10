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

def makeBusy(hashQueue, busyList):
    randHash = random.randrange(0, len(hashQueue))
    if hashQueue[randHash]:
        randData = random.randrange(0, len(hashQueue[randHash]))
        if hashQueue[randHash][randData][1] == 'Free':
            hashQueue[randHash][randData][1] = 'Busy'
            busyList.append([hashQueue[randHash][randData][0] , random.randrange(1,10)])

def notBusy(hashQueue, busyList):
    delete = True
    while delete:
        delete =False
        for busyBlock in busyList:
            if busyBlock[1] == 0:
                hashIndex = busyBlock[0] % len(hashQueue)
                for block in hashQueue[hashIndex]:
                    if block[0] == busyBlock[0]:
                        block[1] = 'Busy'
                        busyList.remove(busyBlock)
                        delete = True
                        break

def ReleaseBlock(hashQueue, freeHeader):
    randHash = random.randrange(0, len(hashQueue))
    if hashQueue[randHash]:
        randData = random.randrange(0, len(hashQueue[randHash]))
        state = hashQueue[randHash][randData][1]
        if state == 'Busy':
            hashQueue[randHash][randData][1] = 'Free'
            block = hashQueue[randHash][randData][0]
            for busy in busyList:
                if busy[0] == block:
                   busyList.remove(busy)
                   break  
            if freeHeader.back != None:
                newFree = freeBlock(freeHeader, freeHeader.back, block, 'Free')
                freeHeader.back.next = newFree
                freeHeader.back = newFree
            else:
                newFree = freeBlock(freeHeader, freeHeader, block, 'Free')
                freeHeader.next = newFree
                freeHeader.back = newFree
           

def getBlock(requestBlock, hashQueue, freeHeader, busyList):
    hashIndex = requestBlock % len(hashQueue)
    isExist = False
    for block in hashQueue[hashIndex]:
        if block[0] == requestBlock:
            isExist = True
            if block[1] == 'Busy':
                print("Senario 5 : request block(" +str(requestBlock) + ") is busy")
                return 'Senario_5'
            else:
                free = freeHeader.next
                while free.data != block[0]:
                    free = free.next
                free.back.next = free.next
                free.next.back = free.back
                block[1] = 'Busy'
                busyList.append([block[0], random.randrange(1,10)])
                print("Senario 1 : make free block(" +str(requestBlock) + ") to not free") 
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
                for hBlock in hashQueue[hashIndex]:
                    if hBlock[0] == free.data:
                        hBlock[1] = 'Busy'
                print("Senario 3 : delay data(" +str(requestBlock) + ") writing")            
                return 'Senario_3'
            else :
                hashQueue[hashIndex].remove([free.data, 'Free'])
                hashIndex = requestBlock % len(hashQueue)
                hashQueue[hashIndex].append([requestBlock, 'Busy'])
                print("Senario 2 : allocate new block(" +str(requestBlock) + ")")
                return 'Senario_2'

busyList = []
hashQueue, freeHeader = setInit(10, 30, busyList)


while(freeHeader.next.data != "header"):
    freeHeader = freeHeader.next
    print(str(freeHeader.data) + ' ' +freeHeader.state)
freeHeader = freeHeader.next

ReleaseBlock(hashQueue, freeHeader)
print(hashQueue)
print(busyList)
print()


while(freeHeader.next.data != "header"):
    freeHeader = freeHeader.next
    print(str(freeHeader.data)+ ' ' +freeHeader.state)
freeHeader = freeHeader.next

senarioList = [False] * 5

complete = False
Execute = True

counter = 0
while not complete:
    counter +=1
    if counter == 5:
        counter = 0
        makeBusy(hashQueue,busyList)
        makeBusy(hashQueue,busyList)
        makeDelay(freeHeader)
    for busy in busyList:
        busy[1] -= 1
    notBusy(hashQueue, busyList)
    complete = True
    if Execute:
        rand = random.randint(0, 100) 
    result = getBlock(rand, hashQueue, freeHeader, busyList) 
    
    if result == 'Senario_1':
        senarioList[0] = True
        Execute = True
    
    if result == 'Senario_2':
        senarioList[1] = True
        Execute = True
        while(freeHeader.next.data != "header"):
            freeHeader = freeHeader.next
            print(str(freeHeader.data)+ ' ' +freeHeader.state)
        freeHeader = freeHeader.next
        
    if result == 'Senario_3':
        senarioList[2] = True
        Execute = False
    
    if result == 'Senario_4':
        senarioList[3] = True
        Execute = False
        ReleaseBlock(hashQueue, freeHeader)
        
        
    if result == 'Senario_5':
        senarioList[4] = True
        Execute = False
    
    if result == 'Senario_0':
        Execute = True
    
    for senario in senarioList:
        if not senario:
            complete = False
            break
    if senarioList[0] == False:
        ReleaseBlock(hashQueue, freeHeader)
        ReleaseBlock(hashQueue, freeHeader)
    

    print(hashQueue)
    time.sleep(1)
