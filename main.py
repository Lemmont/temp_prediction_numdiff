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
    for i in range(len(temp[(year-1)*365:year*365])):
        df_data.append(df5(temp, h, i))
    return df_data
    
def avg_temp(year, temp):
    avg_temp_data = []
    for r in range(len(temp[(year-1)*365:year*365])):
        avg_temp_data.append(vgem(25, r, temp[(year-1)*365:year*365]))
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

def plot_data(year, temp, avg_temp_data):
    avg_acc_total = make_avg_acc(temp)
    predicted = predict(temp[:365], avg_acc_total)
    accuracy = 0
    r = 0
    for i in range((year-1)*365,year*365):
        accuracy += abs(temp[i]-predicted[r])
        r += 1
    accuracy /= 365
    print(f'accuracy: {100-(10*accuracy)}%')
    plt.plot(temp[(year-1)*365:year*365], label=f'Tempature')
    plt.plot(avg_temp_data, label=f'Average temparature')
    plt.plot(predicted, label=f'Temparature prediction')
    plt.title(f'Tempature stats for {1979+year}')
    plt.xlabel(f'Time in days from 01-01-{1979+year} upwards')
    plt.legend()
    plt.show()

year = 4
temp = read_data("result.txt")
df_data = df_year(year, temp, 1)
avg_temp_data = avg_temp(year, temp)
avg_incr_temp_data = avg_incr_temp(year, df_data)
plot_data(year, temp, avg_temp_data)