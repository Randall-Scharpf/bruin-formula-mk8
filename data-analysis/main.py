import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from os import listdir
from os.path import isfile, join


class Data:
    def __init__(self, title, units):
        self.title = title
        self.units = units
        # the parameters that will be passed to matplotlib
        self.x = []
        self.y = []


data_df = None  # data frame of all data from files
acc_magnitude = Data("Acc Magnitude", "g")
engine_speed = Data("Engine Speed", "RPM")
throttle = Data("Throttle", "%")
intake_air_temp = Data("Intake Air Temp", "C")
coolant_temp = Data("Coolant Temp", "C")
lambda1 = Data("Lambda #1", "Lambda")
ign_timing = Data("Ignite Timing", "Deg")
battery_volts = Data("Battery Volts", "Volts")
ve = Data("Volumetric Efficiency", "%")
fuel_pressure = Data("Fuel Pressure", "PSIg")
lambda_target = Data("Lambda Target", "Lambda")
fuel_pump = Data("Fuel Pump", "bool")
fan1 = Data("Fan 1", "bool")
launch_ramp_time = Data("Launch Ramp Time", "ms")
mass_airflow = Data("Mass Airflow", "gms/s")
rotation_x = Data("Rotation X", "deg/s")
rotation_y = Data("Rotation Y", "deg/s")
rotation_z = Data("Rotation Z", "deg/s")

# changes the scaling of the graph
graph_all = True
x_range_lower = 25
x_range_upper = 26
y_range_lower = 0.3
y_range_upper = 0.4


def main():
    load_data("files/0007")
    acc()
    can_01F0A000()
    can_0x01F0A003()
    can_0x01F0A004()
    can_0x01F0A005()

    '''
    figure, axis = plt.subplots(1, 1)
    plot_data(axis, [intake_air_temp, coolant_temp])
    if not graph_all:
        axis.set_xlim([x_range_lower, x_range_upper])
        axis.set_ylim([y_range_lower, y_range_upper])
    '''

    fig = plt.figure()
    ax = fig.add_subplot(111)

    lns1 = ax.plot(engine_speed.x, engine_speed.y, '', label='Engine Speed', color='r')
    ax2 = ax.twinx()
    lns2 = ax.plot(intake_air_temp.x, intake_air_temp.y, '', label='Intake Air Temp', color='b')
    lns3 = ax2.plot(coolant_temp.x, coolant_temp.y, '', label='Coolant Temp', color='g')

    # added these three lines
    lns = lns1 + lns2 + lns3
    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, loc=0)

    ax.grid()
    ax.set_xlabel("Time (s)")
    ax.set_ylabel(r"some speed units")
    ax2.set_ylabel(r"Temp (C)")
    ax2.set_ylim(0, 35)
    fig.tight_layout()
    # figure.tight_layout()


# read all files under directory, concatenates them, store them in data_df
def load_data(directory):
    global data_df
    filenames = [f for f in listdir(directory) if isfile(join(directory, f))]
    filenames.sort()
    df_list = []
    for file in filenames:
        df_list.append(pd.read_csv(directory + "/" + file, index_col=0, names=["Message Type", "Time/ms", "Data1", "Data2", "Data3"]))
    data_df = pd.concat(df_list, axis=0, ignore_index=False)
    '''
    Another way to structure data_df: no col index
    for file in filenames:
        df_list.append(pd.read_csv(directory + "/" + file, index_col=False, names=["Message Type", "Time/ms", "Data1", "Data2", "Data3"]))
    data_df = pd.concat(df_list, axis=0, ignore_index=True)
    '''
    print(data_df)


# inputs hex string, returns 8-bit signed int value of it
def hex_to_signed_int8(hexadecimal):
    int_val = int(hexadecimal, 16)
    if int_val >= 128:
        int_val -= 128
    return int_val


def can_01F0A000():
    if "CAN" not in data_df.index:
        print("No CAN Data")
        return
    df = data_df.loc[(data_df.index == "CAN") & (data_df["Data2"] == "01F0A000")]
    time_stamps = df["Time/ms"].to_numpy().astype(float)
    messages = df["Data3"].to_list()

    global engine_speed, throttle, intake_air_temp, coolant_temp
    engine_speed.x = throttle.x = intake_air_temp.x = coolant_temp.x = time_stamps
    for msg in messages:
        engine_speed.y.append(int(msg[0: 4], 16) * 0.39063)
        throttle.y.append(int(msg[8: 12], 16) * 0.0015259)
        intake_air_temp.y.append(hex_to_signed_int8(msg[12: 14]))
        coolant_temp.y.append(hex_to_signed_int8(msg[14: 16]))


def can_0x01F0A003():
    if "CAN" not in data_df.index:
        print("No CAN Data")
        return
    df = data_df.loc[(data_df.index == "CAN") & (data_df["Data2"] == "0x01F0A003")]
    time_stamps = df["Time/ms"].to_numpy().astype(float)
    messages = df["Data3"].to_list()

    global ve, fuel_pressure, lambda_target, fuel_pump, fan1
    lambda1.x = ign_timing.x = battery_volts.x = time_stamps
    for msg in messages:
        lambda1.y.append(int(msg[0: 2], 16) * 0.00390625 + 0.5)
        ign_timing.y.append(int(msg[10: 12], 16) * 0.35156 - 17)
        battery_volts.y.append(int(msg[12: 16], 16) * 0.0002455)


def can_0x01F0A004():
    if "CAN" not in data_df.index:
        print("No CAN Data")
        return
    df = data_df.loc[(data_df.index == "CAN") & (data_df["Data2"] == "0x01F0A004")]
    time_stamps = df["Time/ms"].to_numpy().astype(float)
    messages = df["Data3"].to_list()

    global ve, fuel_pressure, lambda_target, fuel_pump, fan1
    ve.x = fuel_pressure.x = lambda_target.x = fuel_pump.x = fan1.x = time_stamps
    for msg in messages:
        ve.y.append(int(msg[4: 6], 16))
        fuel_pressure.y.append(int(msg[6: 8], 16) * 0.580151)
        lambda_target.y.append(int(msg[10: 12], 16) * 0.00390625)
        byte7_binary = bin(int(msg[12: 14], 16))
        fuel_pump.y.append(int(byte7_binary[-1]))
        fan1.y.append(int(byte7_binary[-2]))


def can_0x01F0A005():
    if "CAN" not in data_df.index:
        print("No CAN Data")
        return
    df = data_df.loc[(data_df.index == "CAN") & (data_df["Data2"] == "0x01F0A005")]
    time_stamps = df["Time/ms"].to_numpy().astype(float)
    messages = df["Data3"].to_list()

    global launch_ramp_time, mass_airflow
    launch_ramp_time.x = mass_airflow.x = time_stamps
    for msg in messages:
        launch_ramp_time.y.append(int(msg[0, 4], 16) * 10)
        mass_airflow.y.append(int(msg[4, 8], 16) * 0.05)


def acc():
    if "ACC" not in data_df.index:
        print("No ACC Data")
        return
    global acc_magnitude
    df = data_df.loc["ACC"]

    x_list = df["Data1"].to_numpy().astype(float) / 1e6
    y_list = df["Data2"].to_numpy().astype(float) / 1e6
    z_list = df["Data3"].to_numpy().astype(float) / 1e6
    MAX_AVG_TIMES = 5
    avg_times = min(MAX_AVG_TIMES, len(x_list))
    x_avg = np.sum(x_list[0: avg_times], axis=0) / avg_times
    y_avg = np.sum(y_list[0: avg_times], axis=0) / avg_times
    z_avg = np.sum(z_list[0: avg_times], axis=0) / avg_times

    acc_magnitude.x = df["Time/ms"].to_numpy().astype(float)
    acc_magnitude.y = list(np.sqrt(np.square(x_list - x_avg) + np.square(y_list - y_avg) + np.square(z_list - z_avg)))


def gyro():
    if "GYR" not in data_df.index:
        print("No GYR Data")
        return
    global rotation_x, rotation_y, rotation_z
    df = data_df.loc["GYR"]

    x_list = df["Data1"].to_numpy().astype(float)
    y_list = df["Data2"].to_numpy().astype(float)
    z_list = df["Data3"].to_numpy().astype(float)

    rotation_x.x = rotation_y.x = rotation_z.x = df["Time/ms"].to_numpy().astype(float)
    rotation_x.y = x_list
    rotation_y.y = y_list
    rotation_z.y = z_list


def plot_data(axis, data):
    if type(data) == Data:
        axis.plot(np.array(data.x) / 1e6, np.array(data.y))
        axis.set_title(data.title)
        axis.set_xlabel("Time (s)")
        axis.set_ylabel(data.title + " (" + data.units + ")")
    else:
        colors = ["r", "g", "b"]
        color_index = 0
        concatenated_title = ""
        for d in data:
            axis.plot(d.x / 1e6, d.y, color=colors[color_index % len(colors)], label=d.title)
            concatenated_title += d.title + ", "
            color_index += 1
        axis.set_title(concatenated_title[0: -2])
        axis.set_xlabel("Time (s)")
        axis.set_ylabel("Magnitude (units)")


if __name__ == '__main__':
    import timeit
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print("Runtime:", stop - start, "s")
    plt.show()
