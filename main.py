
import matplotlib.pyplot as plot
import numpy as np
import math
import datetime
import time
import sys
from shutil import copyfile
from prettytable import PrettyTable

export_dir = "C:/Users/timur/repo/hw/hw-LTspiceSimulations/FM/pwl_to_sin/sinsin.pwl"

Pi = math.pi

class SinSignal:
    """Sinuse Signal Class containing all attributes and methods.

    Example:
        signal = SinSignal(100,128)

    Args:
        frequenzy (int): Frequenzy of Signal to be sampled.
        sample_points (int): Resolution per period.

    """

    # Class Attribute
    typ = 'sinus'

    # Initializer / Instance Attributes
    def __init__(self, frequenzy, sample_points):
        #Frequenzy of Sinus Signal to be Digitalized
        self.frequenzy = int(frequenzy)
        #Amount of Sample Points for one Period
        self.sample_points = int(sample_points)
        #Sample Points in Degrees
        self.sp_degree = np.arange(0, sample_points, 1)
        #Sample Points Radian
        self.sp_radian = np.arange(0, sample_points, 1)
        #Y Achses Value for Sample Points before Normalzing
        self.sp_sin_rad = np.arange(0, sample_points, 1)
        #Normalized Y Values
        self.sp_normalized = np.arange(0, sample_points, 1)
        #Y Values in Percent
        self.sp_percent = np.arange(0, sample_points, 1)
        #On time of a single pulse
        self.sp_on_time  = np.arange(0, sample_points, 1)
        #Off time of single pulse
        self.sp_off_time  = np.arange(0, sample_points, 1)
        #the time of one pulse equals to duty cycle 100%
        self.period = 1/self.frequenzy
        #Total pulse time of single pulse
        self.pulse_time = self.period / self.sample_points
        #X Axes value for Sample Point
        self.sp_sample_time = np.arange(0, sample_points, 1)
        #Time when pulse goes high
        self.sp_high_on  = np.arange(0, sample_points, 1)
        #Time when pulse goes low
        self.sp_high_off = np.arange(0, sample_points, 1)

    #Calculates the Sample Points
    def calculate_sample_points(self):
        print("Sample Points calculated: ", str(self.sample_points))
        #Rad per Step
        angle_rad = 2*Pi/self.sample_points
        print("Angle between Sample Points in Rad ", "{0:.4f}".format(angle_rad))
        #Degree per Step
        angle_deg = 360/self.sample_points
        print("Angle between Sample Points in Degree ", "{0:.2f}".format(angle_deg))

        print("Calculating Sample Points in Degree")
        self.sp_degree = np.arange(0, int(math.degrees(2*Pi)), angle_deg)
        print("Calculating Sample Points in Rad")
        self.sp_radian = np.arange(0, 2*Pi, angle_rad)

        if self.sp_radian.size != self.sp_degree.size:
            print('You fucked up stupid np.arrange failed')
            #Don't know yet to solve that in better way, happens to rounding issues
            #when doing angle_deg = 360/self.sample_points
            exit()

        #Calculate Y Axis Values
        self.sp_sin_rad = np.sin(self.sp_radian)
        print("Calculating Normalized Sample Points")
        #Don't want to have negative values therefore lift the sinwave by 1
        self.sp_normalized = 1 + self.sp_sin_rad
        print("Calculating Sample Points in %")
        self.sp_percent = self.sp_normalized / 2
        print("Calculating On Time for Pulses")
        self.sp_on_time  = self.pulse_time * self.sp_percent
        print("Calculating Off Time for Pulses")
        self.sp_off_time = self.pulse_time - self.sp_on_time 

        self.sp_sample_time = (self.sp_radian/2*Pi)*self.period
        self.sp_high_on = self.sp_sample_time - (self.sp_on_time/2)
        self.sp_high_off = self.sp_sample_time +(self.sp_on_time/2)

    def plot_sample_points(self):

        print("Ploting Pretty Table: ")

        #Doing some logic here to have prettier prints
        time_unit_multiplier = 1
        period_unit_multiplier = 1
        TimeUnitPeriod = "s"
        TimeUnitPulse  = "s"

        if self.frequenzy <= 1000:
                #Frequenzy Below 1KHz
                time_unit_multiplier = 1000
                period_unit_multiplier = 1000
                TimeUnitPeriod = "ms"
                TimeUnitPulse  = "us"

        index = 0

        x = PrettyTable()
        x.field_names = ["Sample Points", str(self.sample_points)]
        x.add_row(["Period in "+ TimeUnitPeriod, " {0:.2f}" .format(self.period*period_unit_multiplier )])
        x.add_row(["Pulse time in "+ TimeUnitPeriod, " {0:.2f}" .format(self.pulse_time*time_unit_multiplier )])
        print(x)

        OnTimeHeader = "On Time in " + TimeUnitPulse
        OffTimeHeader = "Off Time in " + TimeUnitPulse
        index = 0
        y = PrettyTable()
        y.field_names = ["Degree", "Radian", "sine(Radian)", "Normalized", "Percent", OnTimeHeader, OffTimeHeader]

        for x in np.nditer(self.sp_degree):
            y.add_row(["{0:.2f}".format(self.sp_degree[index]),
            "{0:.2f}".format(self.sp_degree[index]),
            "{0:.2f}".format(self.sp_radian[index]),
            "{0:.2f}".format(self.sp_normalized[index]),
            "{0:.1f}".format((self.sp_percent[index])*100),
            "{0:.8f}".format(self.sp_on_time[index]* time_unit_multiplier),
            "{0:.8f}".format(self.sp_off_time[index]* time_unit_multiplier)])

            index += 1

        print('Calculated at - ' + datetime.datetime.now().strftime("%d-%m-%Y  %H:%M"))
        print(y)

    def plot_OnTime(self):

        print("Plot OnTime")

        #Doing some logic here to have prettier prints
        time_unit_multiplier = 1
        period_unit_multiplier = 1
        TimeUnitPeriod = "s"
        TimeUnitPulse  = "s"

        if self.frequenzy <= 1000:
                #Frequenzy Below 1KHz
                time_unit_multiplier = 1000
                period_unit_multiplier = 1000
                TimeUnitPeriod = "ms"
                TimeUnitPulse  = "us"

        index = 0

        x = PrettyTable()
        x.field_names = ["Sample Points", str(self.sample_points)]
        x.add_row(["Period in "+ TimeUnitPeriod, " {0:.2f}" .format(self.period*period_unit_multiplier )])
        x.add_row(["Pulse time in "+ TimeUnitPeriod, " {0:.2f}" .format(self.pulse_time*time_unit_multiplier )])
        x.add_row(["Frequenzy ", str(self.frequenzy)])

        print(x)

        OnTimeHeader = "On Time in " + TimeUnitPulse
        OffTimeHeader = "Off Time in " + TimeUnitPulse
        index = 0
        y = PrettyTable()
        y.field_names = ["Degree", "Radian", "sine(Radian)", "Normalized", "Percent", 'Sample Time', 'High Time On', 'High Time Off', OnTimeHeader, OffTimeHeader]

        for x in np.nditer(self.sp_degree):
            y.add_row(["{0:.2f}".format(self.sp_degree[index]),
            "{0:.2f}".format(self.sp_radian[index]),
            "{0:.2f}".format(self.sp_sin_rad[index]),
            "{0:.2f}".format(self.sp_normalized[index]),
            "{0:.1f}".format((self.sp_percent[index])*100),
            "{0:.2f}".format((self.sp_sample_time[index])*1000),
            "{0:.2f}".format((self.sp_high_on[index])*1000),
            "{0:.2f}".format((self.sp_high_off[index])*1000),
            "{0:.8f}".format(self.sp_on_time[index]* time_unit_multiplier),
            "{0:.8f}".format(self.sp_off_time[index]* time_unit_multiplier)])

            index += 1

        print('Calculated at - ' + datetime.datetime.now().strftime("%d-%m-%Y  %H:%M"))
        print(y)

        FileName = 'Frequenzy_'+ str(self.frequenzy) + 'Hz'+'.txt'
        print("Creating File: " + FileName)
        with open(FileName,'w') as pwl:
            pwl.write(str(y))

        t =(self.sp_on_time*1000)
        s = self.sp_degree
        plot.bar(s, t)

        plot.xlabel('Degree')
        plot.ylabel('OnTime')
        plot.title('OnTime')
        plot.grid(True)
        plot.show()

    def plot_PWL_File(self, gpio_volt):

        print("Plot PWL Output File")

        sample_point_buff = []

        index = 0
        rise_time = 0.00001
        fall_time = rise_time

        for x in np.nditer(self.sp_degree):
            #Calculate sample points on x axes
            #1st calculate the high plateau
            p2 = [float(self.sp_sample_time[index])-(float(self.sp_on_time[index]/2)), gpio_volt]
            p3 = [p2[0] + float(self.sp_on_time[index]), gpio_volt]
            p1 = [(p2[0] - rise_time), 0]
            p4 = [(p3[0] + fall_time), 0]

            sample_point_buff.append(p1)
            sample_point_buff.append(p2)
            sample_point_buff.append(p3)
            sample_point_buff.append(p4)

            print("{0:.6f} {1:.1f}".format(p1[0], p1[1]))
            print("{0:.6f} {1:.1f}".format(p2[0], p1[1]))
            print("{0:.6f} {1:.1f}".format(p3[0], p1[1]))
            print("{0:.6f} {1:.1f}".format(p4[0], p1[1]))

            index += 1

        print('Calculated at - ' + datetime.datetime.now().strftime("%d-%m-%Y  %H:%M"))

        FileName = 'PWL_Frequenzy_'+ str(self.frequenzy) + 'Hz'+'.pwl'
        t=[]
        s=[]
        print("Creating File: " + FileName)
        with open(FileName,'w') as pwl:
            for p in sample_point_buff:
                pwl.write("{0} {1}\n".format(p[0], p[1]))
                t.append(p[0])
                s.append(p[1])

        copyfile(FileName, export_dir)

        plot.scatter(t, s)
        plot.plot(t, s)

        plot.xlabel('t')
        plot.ylabel('gpio')
        plot.title('PWL')
        plot.grid(True)
        plot.show()

def main():
    print("Starting main()")
    signal = SinSignal(100, 8)
    signal.calculate_sample_points()
    signal.plot_sample_points()
    signal.plot_OnTime()
    signal.plot_PWL_File(3.3)
    sys.exit()

main()
