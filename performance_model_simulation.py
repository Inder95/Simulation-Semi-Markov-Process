"""This program tries to simulate the task arrival which is Poisson ditributed which constitutes the
Performance model of the paper I am doing under the Professor Nagpal Fellowship"""

import simpy
import math
import random
import pylab as pl

def initialize(l,m,state3,state2,state1,check_interval_2):
    global lamda,mu,k1,k2,k3,t2
    lamda=l
    mu=m
    k3=state3
    k2=state2
    k1=state1
    t2=check_interval_2
    
def check_state(task): #This function checks the number of tasks in the system
    if task==0:
        return 4
    if (task>0 and task<=k3):
        return 3
    if task>k3 and task<=k2:
        return 2
    if task>k2 and task<=k1:
        return 1
    if task>k1:
        return 0
def minimal_repair(env,tasks):
    if tasks>=(k2):
        for i in range (tasks-k3): #This condition does not halt the other processes while repairing
            #cpu.release()
            #a.interrupt("Minimal repair performed")
            yield env.timeout(1)#Use interrupts 
            print("Minimal repair performed")
    else:
        yield env.timeout(0.1)
        print("Check finished at: ",env.now)
            
        
def task_generator(env):
    
    task_ctr=0 # Counts the number of task generated
    
    while True:
        yield env.timeout(-1*math.log(1-random.random())/lamda)
        task_ctr=task_ctr+1
        #print("Task ", task_ctr," generated at ", env.now)
        env.process(computer(env,task_ctr))
                    
def computer(env,name):
    prev_time=0
    with cpu.request() as req:
        state=check_state(cpu.count)
        #print("State :",state,"at time: ",env.now)
        if state==2 and (env.now-prev_time)>=t2:
            print("Check invoked after: ",(prev_time-env.now))
            print("Check started at: ",env.now)
            prev_time=env.now
            env.process(minimal_repair(env,cpu.count))
            
        yield req
        #print("Task ", name," got resource at: ",env.now)
        #print("Number of task: ",cpu.count)
        yield env.timeout(-1*math.log(1-random.random())/mu)
        #print("Task ",name, "leaves at ", env.now)
        
                    

initialize(4,2,2,5,7,0.4)

env1=simpy.Environment();
cpu=simpy.Resource(env1, capacity=5);
#The resource name is CPU and its capacity is 1000 (tasks it can process)
a=env1.process(task_generator(env1))
env1.run(until=30)

