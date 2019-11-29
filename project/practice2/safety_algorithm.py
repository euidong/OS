import random
import copy


# 1. get input
# (process number   , type      , max   , total)
# (n<100            , 2<=n<100  , n<=100,      )
f = open("task_input.txt", "r", encoding="utf-8")
tasks = []

lines = f.readlines()
pNum = int(lines[0].strip())
rNum = int(lines[1].strip())
maxResource = []
for i in range(pNum):
    split = list(map(int, lines[i+2].strip().split(' ')))
    maxResource.append(split)
totalResource = list(map(int,lines[pNum+2].strip().split(' ')))

# 2. get snap shot with random allocation.
# sum of allocate <= total
# allocate <= Max 
tempTotal = totalResource.copy()
allocate = [[0 for i in range(rNum)] for i in range(pNum)]

for i in range(rNum):
    for j in range(pNum):
        if tempTotal[i] > maxResource[j][i]:
            allocate[j][i] = random.randrange(0, maxResource[j][i] + 1)
            tempTotal[i] -= allocate[j][i]

# 3. calculate need available
available = totalResource.copy()
for i in range(rNum):
    for j in range(pNum):
        available[i] -= allocate[j][i]

need = copy.deepcopy(maxResource)

for i in range(rNum):
    for j in range(pNum):
        need[j][i] -= allocate[j][i]

print("---------------------------------------------------------")
print("total")
print(totalResource)
print("---------------------------------------------------------")
print("max")
print(maxResource)
print("---------------------------------------------------------")
print("allocate")
print(allocate)
print("---------------------------------------------------------")
print("available")
print(available)
print("---------------------------------------------------------")
print("need")
print(need)

# 4. judge request.
canRequest = []
for i in range(pNum):
    for j in range(rNum):
        if need[i][j] <= available[j]:
            if j == rNum -1:
                canRequest.append(i)
        else :
            break
print("---------------------------------------------------------")
print("\nThis list is that can allocate request :" , end=' ')
for canReq in canRequest:
    print("P" +str(canReq), end=" ")
print("\n")

request = []
if len(canRequest) > 0:
    ran = random.randrange(0, len(canRequest))
    for j in range(rNum):
        if need[canRequest[ran]][j] != 0:
            request.append(random.randrange(1, need[canRequest[ran]][j] + 1))
        else :
            request.append(0)
        allocate[canRequest[ran]][j] += request[j]
        need[canRequest[ran]][j] -= request[j]
        available[j] -= request[j]
    print("request frome process" + str(canRequest[ran]))
    print(request)
    

print("allocate")
print(allocate)
print("need")
print(need)
print("available")
print(available)

# 5. make safe sequency
def canWork(need, available):
    canRequest = []
    for i in range(len(need)):
        if need[i][0] != -1:
            for j in range(len(need[i])):
                if need[i][j] <= available[j]:
                    if j == rNum -1:
                        canRequest.append(i)
                else :
                    break
    if len(canRequest) == 0:
        return -1
    else:
        return canRequest[0]




print("\n---------------------------------------------------------")
print("output\n")

safety_sequence = []
for n in range(pNum):
    can = canWork(need, available)
    if  can >= 0:
        for i in range(rNum):
            available[i] += allocate[can][i]
        allocate[can][0] = -1
        need[can][0] = -1
        print("P"+ str(can) +"할당됨 ", end='')
        print("available : ", end='')
        print(available)
        safety_sequence.append(can)
    else :
        print("can't allocate")
        break

        