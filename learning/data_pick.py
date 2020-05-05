import matplotlib.pyplot as plt
from utils import data_extraction
import numpy as np

# This file is for data checking and pick
def vis(Data1, Data2=None, Data3=None, ss1=0, ee1=-1, ss2=0, ee2=-1, ss3=0, ee3=-1):
    if Data3 is None:
        plt.figure(figsize=(12,4))
        plt.subplot(1, 3, 1)
        line1, = plt.plot(Data1['time'][ss1:ee1], Data1['pos'][ss1:ee1, 0])
        line2, = plt.plot(Data1['time'][ss1:ee1], Data1['pos'][ss1:ee1, 1])
        line3, = plt.plot(Data1['time'][ss1:ee1], Data1['pos'][ss1:ee1, 2])
        plt.legend([line1, line2, line3], ['x', 'y', 'z'])
        plt.grid()
        plt.title('traj (agent a)')
        plt.subplot(1, 3, 2)
        if Data2 is not None:
            line1, = plt.plot(Data2['time'][ss2:ee2], Data2['pos'][ss2:ee2, 0])
            line2, = plt.plot(Data2['time'][ss2:ee2], Data2['pos'][ss2:ee2, 1])
            line3, = plt.plot(Data2['time'][ss2:ee2], Data2['pos'][ss2:ee2, 2])
            plt.legend([line1, line2, line3], ['x', 'y', 'z'])
            plt.grid()
        plt.title('traj (agent b)')
        plt.subplot(1, 3, 3)
        plt.scatter(Data1['pos'][ss1:ee1, 1], Data1['pos'][ss1:ee1, 2])
        if Data2 is not None:
            plt.scatter(Data2['pos'][ss2:ee2, 1], Data2['pos'][ss2:ee2, 2])
        plt.legend(['a', 'b'])
        plt.show()
        print("a: t0, t1 = " + str(Data1['time'][ss1]) + ', ' + str(Data1['time'][ee1]))
        if Data2 is not None:
            print("b: t0, t1 = " + str(Data2['time'][ss2]) + ', ' + str(Data2['time'][ee2]))
        else:
            print('Ground effect data!')
    else:
        plt.figure(figsize=(16,4))
        plt.subplot(1, 4, 1)
        line1, = plt.plot(Data1['time'][ss1:ee1], Data1['pos'][ss1:ee1, 0])
        line2, = plt.plot(Data1['time'][ss1:ee1], Data1['pos'][ss1:ee1, 1])
        line3, = plt.plot(Data1['time'][ss1:ee1], Data1['pos'][ss1:ee1, 2])
        plt.legend([line1, line2, line3], ['x', 'y', 'z'])
        plt.grid()
        plt.title('traj (agent a)')
        plt.subplot(1, 4, 2)
        line1, = plt.plot(Data2['time'][ss2:ee2], Data2['pos'][ss2:ee2, 0])
        line2, = plt.plot(Data2['time'][ss2:ee2], Data2['pos'][ss2:ee2, 1])
        line3, = plt.plot(Data2['time'][ss2:ee2], Data2['pos'][ss2:ee2, 2])
        plt.legend([line1, line2, line3], ['x', 'y', 'z'])
        plt.grid()
        plt.title('traj (agent b)')
        plt.subplot(1, 4, 3)
        line1, = plt.plot(Data3['time'][ss3:ee3], Data3['pos'][ss3:ee3, 0])
        line2, = plt.plot(Data3['time'][ss3:ee3], Data3['pos'][ss3:ee3, 1])
        line3, = plt.plot(Data3['time'][ss3:ee3], Data3['pos'][ss3:ee3, 2])
        plt.legend([line1, line2, line3], ['x', 'y', 'z'])
        plt.grid()
        plt.title('traj (agent c)')
        plt.subplot(1, 4, 4)
        plt.scatter(Data1['pos'][ss1:ee1, 1], Data1['pos'][ss1:ee1, 2])
        plt.scatter(Data2['pos'][ss2:ee2, 1], Data2['pos'][ss2:ee2, 2])
        plt.scatter(Data3['pos'][ss3:ee3, 1], Data3['pos'][ss3:ee3, 2])
        plt.legend(['a', 'b', 'c'])
        plt.show()
        print("a: t0, t1 = " + str(Data1['time'][ss1]) + ', ' + str(Data1['time'][ee1]))
        print("b: t0, t1 = " + str(Data2['time'][ss2]) + ', ' + str(Data2['time'][ee2]))
        print("c: t0, t1 = " + str(Data3['time'][ss3]) + ', ' + str(Data3['time'][ee3]))

Data_a = data_extraction('../../datacollection20_12_20_2019/swap_sss/cf50_00.csv')
Data_b = data_extraction('../../datacollection20_12_20_2019/swap_sss/cf51_00.csv')
Data_c = data_extraction('../../datacollection20_12_20_2019/swap_sss/cf52_00.csv')
vis(Data_a, Data_b, Data_c, 0, -1, 0, -1, 0, -1)