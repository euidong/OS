import random
import numpy as np
import plotly.figure_factory as ff
import datetime


class task :
    def __init__(self,c,t,arrival,is_poll,name):
        self.c = c
        self.t = t
        self.u = c/t
        self.arrival = arrival
        self.is_poll = is_poll
        self.name = name
        self.waiting_time = 0
        self.use = 0
        self.is_arrived = False

class defer :
    def __init__(self, capacity, t):
        self.capacity = capacity
        self.t = t
        self.u = capacity/t
        self.use = 0

def gcd (num1, num2):
    while num2:
        num1, num2 = num2, num1 % num2
    return num1

def lcm (num1, num2):
    return num1 * num2 // gcd(num1, num2)

def hyper_period(tasks, poll):
    n = poll.t
    for task in tasks :
        n = lcm(task.t,n)
    return n

def make_aperiodic_task(boundary):
    return task(random.randrange(1,3),-1,random.randrange(1,boundary), False, "AP")

def make_aperiodic_tasks(n, boundary):
    aperiodic_tasks = []
    for i in range(n):
        aperiodic_tasks.append(make_aperiodic_task(boundary))
    return aperiodic_tasks

def make_gantt_chart(schedule):
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y-%m-%d')
    df = []
    for job in schedule:
        tomorrow = (now + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        if job != "":
            df.append(dict(Task=job,Start=nowDate,Finish=tomorrow,Resource=job))
        now = now + datetime.timedelta(days=1)
        nowDate = tomorrow

    flg = ff.create_gantt(df,title="deferrable scheduling",index_col='Resource', show_colorbar=True, group_tasks=True,showgrid_x=True)
    flg.show()

def defering(tasks, deferer, aperiodic_num):
    util = 0
    for task in tasks:
        util += task.u
    util += deferer.u
    
    n = len(tasks) + 1
    
    max_util = n * ( 2 ** (1/n) -1 )

    # scheduling이 가능한 경우
    if (util <= max_util):
        poll_buffer = []
        current = 0
        hyperPeriod = hyper_period(tasks, deferer)
        aperiodic_tasks = make_aperiodic_tasks(aperiodic_num, hyperPeriod)
        schedule = ["" for i in range(hyperPeriod + 1)]

        tasks = sorted(tasks, key=lambda task: task.t)
        
        # scheduling 실시
        while current < hyperPeriod:
            # 1. poll_buffer에 쌓기
            for aperiodic_task in aperiodic_tasks:
                if aperiodic_task.arrival <= current and not aperiodic_task.is_arrived:
                    aperiodic_task.is_arrived = True
                    poll_buffer.append(aperiodic_task)
            
            # 2. defer의 주기 순환
            if current % deferer.t == 0:
                deferer.use = 0

            # 3. defer 실시.
            if deferer.capacity > deferer.use :
                if len(poll_buffer) > 0:
                    deferer.use += 1
                    poll_buffer[0].use += 1
                    schedule[current] = poll_buffer[0].name
                    if poll_buffer[0].c == poll_buffer[0].use:
                        poll_buffer.pop(0)
    

            # 4. task의 주기 순환(주기가 돌았으면 초기화).
            for task in tasks:
                if current % task.t == 0:
                    task.use = 0

            if schedule[current] != "AP": 
                # 5. task 할당.
                for task in tasks:
                    if task.use < task.c:
                        schedule[current] = task.name
                        task.use += 1
                        break

            # 6. aperiodic task의 waiting time 추가
            for arrived_AP in poll_buffer:
                if schedule[current] != "AP":
                    arrived_AP.waiting_time += 1
                
            current += 1
        
        sum_waiting_time = 0
        for aperiodic_task in aperiodic_tasks:
            sum_waiting_time += aperiodic_task.waiting_time
        
        for aperiodic_task in aperiodic_tasks:
            print("AP_arrival time : " + str(aperiodic_task.arrival) + ", AP_execution time : " + str(aperiodic_task.c), ",AP_waiting time : " + str(aperiodic_task.waiting_time),end='')
            if aperiodic_task.use != aperiodic_task.c :
                print(" This work not allocated (rest : {})".format(aperiodic_task.c - aperiodic_task.use), end='')
            print()
        i = 0
        for task in schedule:
            print(task +"(" + str(i) + ")", end='\t')
           
            i += 1
        make_gantt_chart(schedule)
        return sum_waiting_time /aperiodic_num
    

    # scheduling이 불가능한 경우
    else :
        print("I can't schedule tasks")
        print("Because : max_util(" +str(max_util) +') < util(' + str(util) + ')')
        return -1
    

f = open("task_input.txt","r")
tasks = []

lines = f.readlines()
for line in lines:
    split = line.strip().split(' ')
    tasks.append(task(int(split[0]), int(split[1]), 0, False, split[2]))

f.close()

# task(execution time, cycle time, arrival time, is_poll)
# tasks = [task(4,20,0,False,"a"), task(2,10,0,False, "b"), task(5,25,0,False, "c")]
deferer = defer(1,10)

# tasks, poll, aperiodicTask_num
print("Average waiting time of Aperiodic task : " + str(defering(tasks,deferer, 5)))