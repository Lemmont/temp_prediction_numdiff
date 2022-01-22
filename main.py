from asyncore import read
from cProfile import label
from cgitb import reset
import numpy as np
from matplotlib import pyplot as plt

def df5(x, h, i):
    if (i - 2*h) >= 0 and (i + 2*h) < len(x):
        return (x[i-2*h] - 8*x[i-h] + 8*x[i+h] - x[i+2*h])/(12*h)
    else:
        return (x[i] - 8*x[i] + 8*x[i] - x[i])/(12*h)

'''
def ddf5(x, h, i):
    if (i - 2*h) >= 0 and (i + 2*h) < len(x):
        return (-x[i -2*h] + 16*x[i - h] - 30*x[i] + 16*x[i + h] - x[i + 2*h])/(12*pow(h, 2))
    else:
        return (-x[i] + 16*x[i] - 30*x[i] + 16*x[i] - x[i])/(12*pow(h, 2))
'''

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

def read_data(filename):
    dag = []
    temp = []
    fp = open(filename, "r")
    for line in fp:
        _, temp_dag, temp_x = line.split(',')
        temp_x = int(temp_x)
        dag_x = str(temp_dag[0:4]) + "-" + str(temp_dag[4:6]) + "-" + str(temp_dag[6:8])
        temp_x /= 10
        dag.append(dag_x)
        temp.append(temp_x)
    return temp

def df_year(year, temp, h):
    df_data = []
    for i in range(len(temp[:365])):
        df_data.append(df5(temp, h, i))
    return df_data
    
def avg_temp(year, temp):
    avg_temp_data = []
    for r in range(len(temp[:365])):
        avg_temp_data.append(vgem(25, r, temp[:365]))
    return avg_temp_data

def avg_incr_temp(year, df_data):
    avg_temp_incr_data = []
    for j in range(len(df_data)):
        avg_temp_incr_data.append(vgem(25, j, df_data))
    return avg_temp_incr_data

def predict(temps, acc):
    res = []
    for i in range(len(temps)):
        j = i
        while j >= 365:
            j -= 365
        res.append(temps[i]*((acc[j]/10)+1))
    return res    

def make_avg_acc(temps):
    data = []
    for i in range(len(temps)):
        data.append(df5(temps, 1, i))
    res = [0 for _ in range(365)]
    for k in range(365):
        for j in range(int(len(data)/365)):
            res[k] += data[(j*365)+k]
    for g in range(len(res)):
        res[g] /= (len(data)/365)
    return res

def plot_data(year, temp, avg_temp_data, df_data, avg_incr_temp_data):
    avg_acc_total = make_avg_acc(temp)
    _, axis = plt.subplots(2, 1)
    axis[0].plot(temp[:1000], label=f'Tempature')
    axis[0].plot(avg_temp_data, label=f'Average temparature')
    axis[0].plot(predict(temp[:1000], avg_acc_total), label=f'Temparature prediction')
    axis[1].plot(df_data, label=f'Increase in temparature')
    axis[1].plot(avg_incr_temp_data, label=f'Average increase in temparature')
    axis[1].plot(avg_acc_total, label=f'Predicted increase in temparature')
    axis[0].set_title(f'Tempature stats in {year}')
    axis[1].set_title(f'Tempature increase stats in {year}')
    axis[0].legend()
    axis[1].legend()
    plt.show()

temp = read_data("result.txt")
df_data = df_year(0, temp, 1)
avg_temp_data = avg_temp(0, temp)
avg_incr_temp_data = avg_incr_temp(0, df_data)
plot_data(0, temp, avg_temp_data, df_data, avg_incr_temp_data)
'''
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
'''
