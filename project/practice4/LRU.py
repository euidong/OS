import random

file = open("input.txt", "r", encoding="utf-8")
frameNum = int(file.readline().strip())

referenceType = 3 * frameNum
referenceNum = 5 * frameNum

pageFaultCount = 0

frame = [0] * frameNum
currentSize = 0

reference = [random.randrange(1, referenceType +1) for i in range(referenceNum)]
currentLoc = 0

print ("frame size:"+ str(frameNum))
print ("reference:" +str(reference))

while currentLoc < referenceNum:
    # 1. 안에 존재하면 아무것도 안함
    isExist = False
    for alloc in range(currentSize):
        if frame[alloc] == reference[currentLoc]:
            isExist = True
            break
    if not isExist:
        # 2. 안에 빈공간이 존재하면 할당
        if currentSize < frameNum:
            frame[currentSize] = reference[currentLoc]
            currentSize += 1
            continue
        # 3. 안에 존재하지 않다면, 과거 목록을 다 뒤져서 값을 제거
        pageFaultCount +=1
        print("page fault가 발생했습니다.")
        tempF = frame.copy()
        tempSize = currentSize
        for i in range(currentLoc-1, -1, -1):
            if tempSize == 1:
                changeLoc = frame.index(tempF[0]) 
                frame[changeLoc] = reference[currentLoc]
                break
            for j in range(tempSize):
                if tempF[j] == reference[i]:
                    tempF.pop(j)
                    tempSize -= 1
                    break
    
    currentLoc += 1
    print(str(currentLoc) + "차시 :" + str(frame))

print("page fault 횟수 : " +str(pageFaultCount))