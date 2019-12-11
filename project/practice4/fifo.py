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
        frame[pageFaultCount % len(frame)] = reference[currentLoc]

        pageFaultCount +=1
        print("page fault가 발생했습니다.")
        
    
    currentLoc += 1
    print(str(currentLoc) + "차시 :" + str(frame))

print("page fault 횟수 : " +str(pageFaultCount))