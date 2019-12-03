# 1. get input
# 1) total memory size
# 2) allocation & deallocation.
import copy
import datetime
import plotly.graph_objects as go

f = open("compaction_input.txt", "r", encoding="utf-8")
lines = f.readlines()

memory = []
totalMemory = int(lines[0].strip())
splits = list(map(int, lines[1].strip().split(' ')))
pair_pm = []
for i in range(0, len(splits), 2):
    pair_pm.append([splits[i], splits[i+1]])

print("\nMEMORY SIZE: " +str(totalMemory) + "K\n")


# 2. allocation in order.
# must check coalescing
# setting freeBlock & allocatedBlock
# they keep each block's startPoint, size, Pnumber
freeBlock = [[0,totalMemory,-1]]
allocatedBlock = []

def coalsing(freeBlock, happen):
    seperated = True
    while seperated:
        seperated = False
        for f in range(len(freeBlock) - 1):
            if freeBlock[f][0] + freeBlock[f][1] == freeBlock[f+1][0]:
                happen.append([f, freeBlock[f][0], freeBlock[f+1][0]])
                newFree = [freeBlock[f][0], freeBlock[f][1] + freeBlock[f + 1][1], -1]
                freeBlock.remove(freeBlock[f])
                freeBlock.remove(freeBlock[f])
                freeBlock.append(newFree)
                freeBlock = sorted(freeBlock)
                seperated = True 
                break
    return freeBlock

def replaceBlock(freeBlock, allocatedBlock):
    start = freeBlock[0][0]
    last = freeBlock[len(freeBlock) - 1][0] + freeBlock[len(freeBlock) - 1][1]
    # 같은 사이즈의 block이 존재하는 경우.
    for aBlock in allocatedBlock:
        if aBlock[0] > start and aBlock[0] < last:
            for fBlock in freeBlock:
                if aBlock[1] == fBlock[1]:
                    allocatedBlock.remove(aBlock)
                    freeBlock.remove(fBlock)
                    fBlock[2] = aBlock[2]
                    aBlock[2] = -1

                    allocatedBlock.append(fBlock)
                    allocatedBlock = sorted(allocatedBlock)
                    freeBlock.append(aBlock)
                    freeBlock = sorted(freeBlock)
                    freeBlock = coalsing(freeBlock, happen)      
                    return freeBlock, allocatedBlock, True     
    return freeBlock, allocatedBlock, False


# print Best fit of state
def printState(aBlock, request, happen, freeBlock):
    if request[1] != 0:
        print("REQUEST " + str(aBlock[2]) + ": " + str(aBlock[1]) + "K")
        print("Best Fit: Allocated at address " + str(aBlock[0]) +"K")    
        if len(happen) != 0:
                print("\tCompaction is happened ")
    else:
        print("FREE REQUEST" + str(aBlock[2]) + " (" + str(aBlock[1]) +"K)")
        print("Best Fit: Freed at address " + str(aBlock[0])+"K")
        while len(happen) != 0:
            print("\tCoalescing blocks at addresses " + str(happen[0][1]) +"K and " + str(happen[0][2]) +"K")
            happen.pop(0)
    totalFree = 0
    for fBlock in freeBlock:
        totalFree += fBlock[1]
    print("\t" + str(totalFree) + "K free, " + str(len(freeBlock)) + " block(s), average size = " + str(totalFree / len(freeBlock)) + "K")


# make totalBlock shape.
def getTotalBlock(allocatedBlock, freeBlock):
    for fBlock in freeBlock:
        fBlock[2] = "empty"
    totalBlock = copy.deepcopy(allocatedBlock)
    totalBlock.extend(copy.deepcopy(freeBlock))
    totalBlock = sorted(totalBlock)
    return totalBlock

def showGraph(totalBlocks):
    x = []
    colors= {}
    
    for i in range(len(totalBlocks)):
        x.append("REQUEST" +str(i+1))
    yBatch = []
    for num in range(len(totalBlocks)):
        for block in totalBlocks[num]:
            y = []
            for i in range(num):
                y.append(0)
            y.append(block[1])
            name = block[2]
            if name == 'empty':
                colors.update({name: 'grey'})
            else:
                colors.update({name : 'rgb({},{},{})'.format((name*10)%256, (name*100)%256, (name*50)%256)})
            for n in range(num+1, len(totalBlocks)):
                if len(totalBlocks[n]) != 0 and block[2] == totalBlocks[n][0][2]:
                    y.append(totalBlocks[n][0][1])
                    totalBlocks[n].pop(0)
                else:
                    y.append(0)
            yBatch.append([name, y])
    
    data = []
    for nameAndY in yBatch:
        data.append(go.Bar(name=nameAndY[0], x=x, y=nameAndY[1], marker={'color': colors[nameAndY[0]] }))
    flg = go.Figure(data=data)
    flg.update_layout(barmode='stack')
    flg.show()

totalBlocks = []
for request in pair_pm:
    happen=[]
    # deallocate
    # if deallocated space's start point is empty, combine 2 empty space
    if request[1] == 0:
        for aBlock in allocatedBlock:
            if aBlock[2] == request[0]:
                freeBlock.append(aBlock)
                freeBlock = sorted(freeBlock)

                # coalscing
                freeBlock = coalsing(freeBlock, happen)
                allocatedBlock.remove(aBlock)
                break

    # allocate
    # empty space check. if size is enough, allocate this space.
    # if not, do compaction.
    # if although program do compaction, memory is not enough, it mean that program can't allocate.
    else:
        i = 0
        if len(freeBlock) == 0:
            print("can't allocate, because memory is full")
            break
        else:
            same = False
            for i in range(len(freeBlock)):
                if freeBlock[i][1] == request[1]:
                    same = True
                    break
            if not same:
                canAllocate = False
                for i in range(len(freeBlock)):
                    if request[1] <= freeBlock[i][1]:
                        canAllocate = True
                        break          
                # need to do compaction
                # 1. find a block to move.
                # 2. if the blocks's size is same any free block, move to that free block location.
                # 3. if not, do compaction.   
                if not canAllocate:
                    if len(freeBlock) == 1:
                    # can't compaction
                        print("Can't allocation this memory.")
                        break
                    else :
                        flag = True
                        while flag:
                            freeBlock, allocatedBlock, flag = replaceBlock(freeBlock, allocatedBlock)
                        start = freeBlock[0][0]
                        last = freeBlock[len(freeBlock) - 1][0] + freeBlock[len(freeBlock) - 1][1]
                        for aBlock in allocatedBlock:
                            if aBlock[0] > start and aBlock[0] < last:
                                aBlock[0] = freeBlock[0][0]
                                freeBlock[0][0] = aBlock[0] + aBlock[1]
                                freeBlock = coalsing(freeBlock, happen)
                        canAllocate = False
                        for i in range(len(freeBlock)):
                            if request[1] <= freeBlock[i][1]:
                                canAllocate = True
                                break
                        if not canAllocate:
                            print("Can't allocation thismemory.")
                            break
            # case : don't need to do compaction.
            
            aBlock = [freeBlock[i][0], request[1], request[0]]
            allocatedBlock.append(aBlock)
            allocatedBlock = sorted(allocatedBlock)
            if request[1] == freeBlock[i][1]:
                freeBlock.pop(i)
            else:
                freeBlock[i][0] += request[1]
                freeBlock[i][1] -= request[1]
    printState(aBlock,request, happen, freeBlock)
    totalBlocks.append(getTotalBlock(allocatedBlock, freeBlock))
showGraph(totalBlocks)