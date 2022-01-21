import numpy as np
from matplotlib import pyplot as plt

def df5(x, h, i):
    if (i - 2*h) >= 0 and (i + 2*h) < len(x):
        return (x[i-2*h] - 8*x[i-h] + 8*x[i+h] - x[i+2*h])/(12*h)
    else:
        return (x[i] - 8*x[i] + 8*x[i] - x[i])/(12*h)

def ddf5(x, h, i):
    if (i - 2*h) >= 0 and (i + 2*h) < len(x):
        return (-x[i -2*h] + 16*x[i - h] - 30*x[i] + 16*x[i + h] - x[i + 2*h])/(12*pow(h, 2))
    else:
        return (-x[i] + 16*x[i] - 30*x[i] + 16*x[i] - x[i])/(12*pow(h, 2))

def vrts_gem(q, n, x):
    som = 0
    for i in range(-q, q+1):
        try:
            som += abs(x[n+i])
        except IndexError:
            continue
    return (1/2*q+1) * som

def vgem(q, n, x):
    som = 0
    for i in range(0, q+1):
        try:
            som += x[n-i]
        except IndexError:
            continue
    return som/q

dag = []
temp = []
fp = open("result.txt", "r")
for line in fp:
    _, temp_dag, temp_x = line.split(',')
    temp_x = int(temp_x)
    dag_x = str(temp_dag[0:4]) + "-" + str(temp_dag[4:6]) + "-" + str(temp_dag[6:8])
    temp_x /= 10
    dag.append(dag_x)
    temp.append(temp_x)
h = 1
afgeleide = []
for i in range(len(temp[:365])):
    afgeleide.append(df5(temp, h, i))
smooth = []
for r in range(len(temp[:365])):
    smooth.append(vgem(25, r, temp[:365]))
smooth_af = []
for j in range(len(afgeleide)):
    smooth_af.append(vgem(25, j, afgeleide))

k = 0
avg_acc_2_jan_list = []
avg_temp_1_jan_list = []
while k < len(temp):
    try:
        avg_acc_2_jan_list.append(afgeleide[k+1])
    except IndexError:
        pass
    avg_temp_1_jan_list.append(temp[k])
    k += 365
avg_temp_1_jan = sum(avg_temp_1_jan_list)/len(avg_temp_1_jan_list)
avg_acc_2_jan = sum(avg_acc_2_jan_list)/len(avg_acc_2_jan_list)
print(avg_temp_1_jan)
print(avg_acc_2_jan)
print((1 + avg_acc_2_jan)*avg_temp_1_jan)

figure, axis = plt.subplots(3, 1)
axis[0].plot(temp[:365])
axis[0].plot(smooth)
axis[1].plot(afgeleide)
axis[1].plot(smooth_af)
plt.show()