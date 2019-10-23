import random
from matplotlib import pyplot as plt
import numpy as np

class task :
    def __init__(self,c,t,arrival,is_poll,name):
        self.c = c
        self.t = t
        self.u = c/t
        self.arrival = arrival
        self.is_poll = is_poll
        self.name = name

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

def make_gantt_chart():    
    label = "Scheduling"
    index = np.arange(1)
    a = 3
    b = 5
    c = 100
    plt.title("Poll Scheduling")
    plt.xlabel("time")
    plt.rcParams["figure.figsize"] = (20,2)
    plt.rcParams['axes.grid'] = True
    plt.barh(1, a, height = 0.1, color='b')
    plt.barh(1, b, height = 0.1, color ='r', left = a )
    plt.barh(1, c, height = 0.1, color ='g', left = a + b )
    plt.title("Poll Scheduling")
    plt.xlabel('time')
    plt.xticks(np.arange(0,110, step = 5))
    plt.yticks([])
    plt.show()

def polling(tasks, poll, aperiodic_num):
    util = 0
    for task in tasks:
        util += task.u
    util += poll.u
    
    n = len(tasks) + 1
    
    max_util = n * ( 2 ** (1/n) -1 )

    # scheduling이 가능한 경우
    if (util <= max_util):
        poll_buffer = 0
        put_count = 0
        aperiodic_count = 0
        current = 0
        hyperPeriod = hyper_period(tasks, poll)
        aperiodic_tasks = make_aperiodic_tasks(aperiodic_num, hyperPeriod)
        schedule = [0 for i in range(hyperPeriod + 1)]

        # for i in range(0,hyperPeriod, poll.t):
        #     if aperiodic_count < aperiodic_num:
        #         if aperiodic_tasks[aperiodic_count].arrival < i:
        #             poll_buffer+= aperiodic_tasks[aperiodic_count]
        #             aperiodic_count+=1
        #     while poll_buffer > 0:
        #         if poll.c - put_count > 0:
        #             schedule[i + put_count] = "AP"
        #             put_count += 1
        #         else:
        #             put_count = 0
        #             break

        if task.is_poll == True:
                while current < hyper_period:
                    while current >= aperiodic_tasks[aperiodic_count].arrival and aperiodic_count < aperiodic_num:
                        poll_buffer += aperiodic_tasks[aperiodic_count].c
                        aperiodic_count += 1

                    while put_count < task.c and poll_buffer > 0:
                        schedule[current + put_count] = task.name
                        put_count += 1
                    put_count = 0
                    current += task.t
        tasks = sorted(tasks, key=lambda task: task.t)

        for task in tasks:
            while current < hyper_period: 
                while put_count < task.c:
                    schedule[current + put_count] = task.name
                    put_count += 1
                put_count = 0
                current += task.t
            current = 0
                    





    # scheduling이 불가능한 경우
    else :
        print("I can't schedule tasks")
        print("Because : max_util(" +str(max_util) +') < util(' + str(util) + ')')
    


# task(execution time, cycle time, arrival time, is_poll)
tasks = [task(4,20,0,False,"a"), task(2,10,0,False, "b"), task(5,25,0,False, "c")]
poll = task(1,15,0,True,"poll")

# tasks, poll, aperiodicTask_num
polling(tasks,poll, 3)

