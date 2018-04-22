'''
CS5250 Assignment 4, Scheduling policies simulator
Sample skeleton program
Author: Minh Ho
Input file:
    input.txt
Output files:
    FCFS.txt
    RR.txt
    SRTF.txt
    SJF.txt

Apr 10th Revision 1:
    Update FCFS implementation, fixed the bug when there are idle time slices between processes
    Thanks Huang Lung-Chen for pointing out
Revision 2:
    Change requirement for future_prediction SRTF => future_prediction shortest job first(SJF), the simpler non-preemptive version.
    Let initial guess = 5 time units.
    Thanks Lee Wei Ping for trying and pointing out the difficulty & ambiguity with future_prediction SRTF.
'''
import sys
import heapq # priority queue

input_file = 'input.txt'

class Process:
    last_scheduled_time = 0
    def __init__(self, id, arrive_time, burst_time):
        self.id = id
        self.arrive_time = arrive_time
        self.burst_time = burst_time
    #for printing purpose
    def __repr__(self):
        return ('[id %d : arrive_time %d,  burst_time %d]'%(self.id, self.arrive_time, self.burst_time))

def FCFS_scheduling(process_list):
    #store the (switching time, process_id) pair
    schedule = []
    current_time = 0
    waiting_time = 0
    for process in process_list:
        if (current_time < process.arrive_time):
            current_time = process.arrive_time
        schedule.append((current_time,process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        current_time = current_time + process.burst_time
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

#Input: process_list, time_quantum (Positive Integer)
#Output_1 : Schedule list contains pairs of (time_stamp, process_id) indicating the time switching to that process_id
#Output_2 : Average Waiting Time
def RR_scheduling(process_list, time_quantum ):
    schedule = []
    ready_queue = []
    current_time = 0
    total_waiting_time = 0
    last_scheduled_id = -1
    for process in process_list:
        if (current_time < process.arrive_time):
            time_to_go = process.arrive_time - current_time
            while (time_to_go > 0):
                if len(ready_queue) == 0:
                    current_time = process.arrive_time
                    break
                process_id, quantum, burst = ready_queue[0]
                if (process_id != last_scheduled_id):
                    schedule.append((current_time,process_id))
                    last_scheduled_id = process_id
                while True:
                    ready_queue[0][1] = quantum = quantum - 1
                    ready_queue[0][2] = burst = burst - 1
                    time_to_go = time_to_go - 1
                    current_time = current_time + 1
                    total_waiting_time = total_waiting_time + len(ready_queue) - 1
                    if burst == 0:
                        ready_queue.pop(0)
                        break
                    if quantum == 0:
                        ready_queue.pop(0)
                        ready_queue.append([process_id, time_quantum, burst])
                        break
                    if time_to_go == 0:
                        break
        new_process = True
        for index, element in enumerate(ready_queue):
            process_id, quantum, burst = element
            if (process.id == process_id):
                new_process = False
                burst = burst + process.burst_time
                break
        if new_process:
            ready_queue.append([process.id, time_quantum, process.burst_time])
    # code easier now that only two values left
    while (len(ready_queue) > 0):
        process_id, quantum, burst = ready_queue[0]
        if (process_id != last_scheduled_id):
            schedule.append((current_time,process_id))
            last_scheduled_id = process_id
        jump_time = min(quantum, burst)
        current_time = current_time + jump_time
        total_waiting_time = total_waiting_time + (len(ready_queue) - 1) * jump_time
        ready_queue.pop(0)
        if burst > jump_time:
            ready_queue.append([process_id, time_quantum, burst - jump_time])
    average_waiting_time = total_waiting_time/float(len(process_list))
    return schedule, average_waiting_time

def SRTF_scheduling(process_list):
    #store the (switching time, process_id) pair
    schedule = []
    ready_queue = []
    current_time = 0
    total_waiting_time = 0
    last_scheduled_id = -1
    for process in process_list:
        if (current_time < process.arrive_time):
            time_to_go = process.arrive_time - current_time
            print "time to go: %s" % time_to_go
            while (time_to_go > 0):
                if len(ready_queue) == 0:
                    current_time = process.arrive_time
                    break
                burst, process_id = heapq.heappop(ready_queue)
                if (process_id != last_scheduled_id):
                    schedule.append((current_time,process_id))
                    print "Scheduling process %d at time %d" % (process_id, current_time)
                    last_scheduled_id = process_id
                if (time_to_go < burst):
                    print "Process %d runs for %d time" % (process_id, time_to_go)
                    burst = burst - time_to_go
                    heapq.heappush(ready_queue, [burst, process_id])
                    print "Process %d has %d time left" % (process_id, burst)
                    print ready_queue
                    current_time = current_time + time_to_go
                    total_waiting_time = total_waiting_time + (len(ready_queue) - 1) * time_to_go
                    time_to_go = 0
                    break
                print "Process %d runs for %d time" % (process_id, burst)
                time_to_go = time_to_go - burst
                current_time = current_time + burst
                total_waiting_time = total_waiting_time + len(ready_queue) * burst
        heapq.heappush(ready_queue, [process.burst_time, process.id])
        print "Inserting process %d with time %d" % (process.id, process.burst_time)
        print ready_queue
    # code easier now
    while (len(ready_queue) > 0):
        burst, process_id = heapq.heappop(ready_queue)
        if (process_id != last_scheduled_id):
            schedule.append((current_time,process_id))
            last_scheduled_id = process_id
        current_time = current_time + burst
        total_waiting_time = total_waiting_time + len(ready_queue) * burst
        
    average_waiting_time = total_waiting_time/float(len(process_list))
    return schedule, average_waiting_time

def SJF_scheduling(process_list, alpha):
    return (["to be completed, scheduling SJF without using information from process.burst_time"],0.0)


def read_input():
    result = []
    with open(input_file) as f:
        for line in f:
            array = line.split()
            if (len(array)!= 3):
                print ("wrong input format")
                exit()
            result.append(Process(int(array[0]),int(array[1]),int(array[2])))
    return result
def write_output(file_name, schedule, avg_waiting_time):
    with open(file_name,'w') as f:
        for item in schedule:
            f.write(str(item) + '\n')
        f.write('average waiting time %.2f \n'%(avg_waiting_time))


def main(argv):
    process_list = read_input()
    print ("printing input ----")
    for process in process_list:
        print (process)
    print ("simulating FCFS ----")
    FCFS_schedule, FCFS_avg_waiting_time =  FCFS_scheduling(process_list)
    write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )
    print ("simulating RR ----")
    RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = 2)
    write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
    print ("simulating SRTF ----")
    SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
    write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )
    print ("simulating SJF ----")
    SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
    write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )

if __name__ == '__main__':
    main(sys.argv[1:])
