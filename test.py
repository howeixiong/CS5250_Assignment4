from simulator import *

def multiple_runs():
    min_time = 999999999
    for i in range(100):
        SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
        if (SRTF_avg_waiting_time < min_time):
            min_time = SRTF_avg_waiting_time
    print "SRTF: average_waiting_time is %.2f" % min_time
    for i in range(100):
        SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
        if (SJF_avg_waiting_time < min_time):
            min_time = SJF_avg_waiting_time
    print "SJF: average_waiting_time is %.2f" % min_time
    

def test_RR():
    max_burst = max(map(lambda process: process.burst_time, process_list))
    print "Largest burst time is %d" % max_burst
    for Q in range(1, max_burst + 1):
        RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = Q)
        print "Quantum %d: average_waiting_time %.2f" % (Q, RR_avg_waiting_time)


def test_SJF():
    min_waiting_time = 999999999
    min_waiting_time_alpha = -1
    for alpha in map(lambda i: i/100.0, range(0, 100 + 1)):
        min_waiting_time_for_this_alpha = 999999999
        for i in range(1000):
            SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha)
            if (SJF_avg_waiting_time < min_waiting_time_for_this_alpha):
                min_waiting_time_for_this_alpha = SJF_avg_waiting_time
        print "alpha %.2f: average_waiting_time %.2f" % (alpha, min_waiting_time_for_this_alpha)
        if (min_waiting_time_for_this_alpha < min_waiting_time):
            min_waiting_time = min_waiting_time_for_this_alpha
            min_waiting_time_alpha = alpha
    print "Minimum average waiting time is %.2f for alpha of %.2f" % (min_waiting_time, min_waiting_time_alpha)

#testing different way in case non-determinism works funnily
def test_SJF_2():
    min_waiting_time_per_alpha = [999999999] * 101
    for i in range(1000):
        for alpha in range(0, 100 + 1):
            SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha/100.0)
            if (SJF_avg_waiting_time < min_waiting_time_per_alpha[alpha]):
                min_waiting_time_per_alpha[alpha] = SJF_avg_waiting_time
    min_waiting_time = 999999999
    min_waiting_time_i = -1
    for i in range(0, 100 + 1):
        print "alpha %.2f: average_waiting_time %.2f" % (i/100.0, min_waiting_time_per_alpha[i])
        if (min_waiting_time_per_alpha[i] < min_waiting_time):
            min_waiting_time = min_waiting_time_per_alpha[i]
            min_waiting_time_i = i
    print "Minimum average waiting time is %.2f for alpha of %.2f" % (min_waiting_time, min_waiting_time_i/100.0)

if __name__ == '__main__':
    process_list = read_input()
    multiple_runs()
    print ""
    test_RR()
    print ""
    test_SJF()
    #print ""
    #test_SJF_2()
