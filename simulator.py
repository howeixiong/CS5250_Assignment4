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
    process_index = 0
    current_time = 0
    ready_queue = []
    last_scheduled_id = -1
    schedule = []
    waiting_time = 0

    while (process_index < len(process_list)) or (len(ready_queue) > 0): # while there is something to do
        if process_index < len(process_list):
            new_process = process_list[process_index]
            
            # append process to queue if it has arrived
            if new_process.arrive_time == current_time:
                ready_queue.append( [new_process.id, new_process.burst, time_quantum, new_process.arrive_time + new_process.burst] )
                process_index += 1
          
        # what should I do at this current time?
        if len(ready_queue) == 0:
            # nothing to do -> move forward one time unit (for optimisation, can fast forward to next process' arrival time)
            current_time += 1
            last_scheduled_id = -1
        else:
            # do first process in the ready queue
            process_id, process_burst, process_quantum, process_earliest_end_time = ready_queue.pop(0)
            
            if last_scheduled_id != process.id:
              schedule.append( [current_time, process_id] )
              last_scheduled_id = process.id
            
            # increment time
            process.burst -= 1
            process.quantum -= 1
            current_time += 1
            
            if process.burst == 0:
                # done with this process
                waiting_time += current_time - process_earliest_end_time
            elif process.quantum == 0:
                # this process has used up its quantum -> move it to the back of the queue
                ready_queue.append( [process)id, process_burst, time_quantum, process_earliest_end_time] )
    
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

def SRTF_scheduling(process_list):
    #store the (switching time, process_id) pair
    schedule = []
    ready_queue = []
    current_time = 0
    waiting_time = 0
    last_scheduled_id = -1
    for process in process_list:
        if (current_time < process.arrive_time):
            time_to_go = process.arrive_time - current_time
            while (time_to_go > 0):
                if len(ready_queue) == 0:
                    current_time = process.arrive_time
                    last_scheduled_id = -1
                    break
                burst, process_id = heapq.heappop(ready_queue)
                if (process_id != last_scheduled_id):
                    schedule.append((current_time,process_id))
                    last_scheduled_id = process_id
                if (time_to_go < burst):
                    burst -= time_to_go
                    heapq.heappush(ready_queue, [burst, process_id])
                    current_time += time_to_go
                    waiting_time += (len(ready_queue) - 1) * time_to_go
                    time_to_go = 0
                    break
                time_to_go -= burst
                current_time += burst
                waiting_time += len(ready_queue) * burst
        # i think need to deal with the case where the process is there already
        heapq.heappush(ready_queue, [process.burst_time, process.id])
    # code easier now
    while (len(ready_queue) > 0):
        burst, process_id = heapq.heappop(ready_queue)
        if (process_id != last_scheduled_id):
            schedule.append((current_time,process_id))
            last_scheduled_id = process_id
        current_time += burst
        waiting_time += len(ready_queue) * burst
        
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

def SJF_scheduling(process_list, alpha):
    #store the (switching time, process_id) pair
    schedule = []
    ready_queue = []
    past_predicted_time = {}
    actual_time = {}
    current_time = 0
    waiting_time = 0
    last_scheduled_id = -1
    for process in process_list:
        while (current_time < process.arrive_time):
            if len(ready_queue) == 0:
                current_time = process.arrive_time
                last_scheduled_id = -1
                break
            predicted_time, process_id, burst = heapq.heappop(ready_queue)
            if (process_id != last_scheduled_id):
                schedule.append((current_time,process_id))
                last_scheduled_id = process_id
            
            current_time += burst
            waiting_time += len(ready_queue) * burst
        # i think need to deal with the case where the process is there already
        if process.id in past_predicted_time:
            predicted_time = alpha * actual_time[process.id] + (1 - alpha) * past_predicted_time[process.id]
        else:
            predicted_time = 5
        past_predicted_time[process.id] = predicted_time
        actual_time[process.id] = process.burst_time
        heapq.heappush(ready_queue, [predicted_time, process.id, process.burst_time])
        waiting_time += current_time - process.arrive_time
    # code easier now
    while (len(ready_queue) > 0):
        predicted_time, process_id, burst = heapq.heappop(ready_queue)
        if (process_id != last_scheduled_id):
            schedule.append((current_time,process_id))
            last_scheduled_id = process_id
        current_time += burst
        waiting_time += len(ready_queue) * burst
        
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time


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
