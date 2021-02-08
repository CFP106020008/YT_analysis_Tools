import time
import threading
import multiprocessing as mp

T0 = time.time()
P = []


def main(Name, Num):
    P.append(Num)
    #print(Name, Num)
    #print(time.time())
    #print('Done')

Names = ['A','B','C','D','E']
Nums = [0,1,2,3,4,5]

N = 5

t_list = []

for i in range(N):
    t_list.append(mp.Process(target=main, args=(Names[i], Nums[i])))

for t in t_list:
    t.start()

for t in t_list:
    t.join()

print(P)

T1 = time.time()
print(T1-T0)

