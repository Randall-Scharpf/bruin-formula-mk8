import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from os import listdir
from os.path import isfile, join


# data class to help keep track of different types of data
class Data:
    def __init__(self, title, units):
        self.title = title
        self.units = units
        # parameters that will be passed to matplotlib
        self.x = []  # x is usually time
        self.y = []  # y is the value of the data


# all the data that we want to keep track of
# acc data
acc_magnitude = Data("Acceleration Magnitude", "g")
# can data with message id = 01F0A000
engine_speed = Data("Engine Speed", "RPM")
throttle = Data("Throttle", "%")
intake_air_temp = Data("Intake Air Temp", "F")
coolant_temp = Data("Coolant Temp", "F")
# can data with message id = 0x01F0A003
lambda1 = Data("Lambda #1", "Lambda")
ign_timing = Data("Ignite Timing", "Deg")
battery_volts = Data("Battery Volts", "Volts")
# can data with message id = 0x01F0A004
ve = Data("Volumetric Efficiency", "%")
fuel_pressure = Data("Fuel Pressure", "PSIg")
lambda_target = Data("Lambda Target", "Lambda")
fuel_pump = Data("Fuel Pump", "bool")
fan1 = Data("Fan 1", "bool")
# can data with message id = 0x01F0A005
launch_ramp_time = Data("Launch Ramp Time", "ms")
mass_airflow = Data("Mass Airflow", "gms/s")
# gyr data
rotation_x = Data("Rotation X", "deg/s")
rotation_y = Data("Rotation Y", "deg/s")
rotation_z = Data("Rotation Z", "deg/s")

# data frame containing all data imported from files
data_df = None
# is the maximum number of samples acc() will average over, cannot be 0
acc_average_times = 5

# a list of color chars, can change this to add more colors
colors = list("bgrcmy")
# below are parameters that user can set to fits specific needs, will reset to default values after plt.show()
# specifies a range in which data will be plotted
graph_within_range = False
x_range_lower = 25
x_range_upper = 26
y_range_lower = 0.3
y_range_upper = 0.4
# have a legend or not
have_legend = True
# have a grid or not
have_grid = True
# label of the y-axis, empty string means use self-generated label, overwrites only when there is one y label
y_label = ""
# title of the graph, empty string means use self-generated title
graph_title = ""


def main():
    load_data("files/1234")
    acc()
    can_01F0A000()
    can_01F0A003()
    can_01F0A004()
    can_01F0A005()
    gyr()

    plot_data([coolant_temp])
    # plot_data_multi_axes([coolant_temp, intake_air_temp, throttle])


# read all files under directory, concatenates them, store them in data_df
# files will be read in lexicographic order
def load_data(directory):
    global data_df
    # get all files under directory, excluding folders
    filenames = [f for f in listdir(directory) if isfile(join(directory, f))]
    # sort the file names lexicographically
    filenames.sort()
    df_list = []
    for file in filenames:
        # skip files whose names start with a dot (to avoid reading .DS_Store files and alike)
        if file[0] == ".":
            continue
        filepath = directory + "/" + file
        print("Reading", filepath, "...")
        df_list.append(pd.read_csv(filepath, index_col=0, names=["Message Type", "Time(ms)", "Data1", "Data2", "Data3"],
                                   dtype=str))
    data_df = pd.concat(df_list, axis=0, ignore_index=False)
    '''
    another way to structure data_df: message type will become its own column instead of being the index column
    for file in filenames:
        df_list.append(pd.read_csv(filepath, index_col=False, names=["Message Type", "Time(ms)", "Data1", "Data2",
                                   "Data3"]))
    data_df = pd.concat(df_list, axis=0, ignore_index=True)
    '''
    print("Imported data frame:")
    print(data_df)


'''
The following functions process data_df and store data in corresponding global Data variables

Warning: the functions below will crash if there is only one line of data of interest (i.e. only one acc data). this is
due to that when dataframes have only 1 row, df[col] will return a string instead of a list. it will cause
df[col].to_numpy().astype(float) to throw an error. but since this rarely happens, i am leaving it as it be.

Some useful pandas functions:
data_df[str] returns the column with column name str
data_df.loc[str] returns rows whose index = str
data_df.loc[bool1 & bool2] returns rows that satisfy bool1 and bool2
'''


# inputs hex string, returns 8-bit signed int value of it
def hex_to_signed_int8(hexadecimal):
    int_val = int(hexadecimal, 16)
    if int_val >= 128:
        int_val -= 128
    return int_val


# process can data with message id 01F0A000
def can_01F0A000():
    df = data_df.loc[(data_df.index == "CAN") & (data_df["Data2"] == "01F0A000")]
    if df.empty:
        print("Warning: No CAN data with message id 01F0A000")
        return
    time_stamps = df["Time(ms)"].to_numpy().astype(float) / 1e6  # to make timestamps in seconds
    messages = df["Data3"].to_list()

    global engine_speed, throttle, intake_air_temp, coolant_temp
    engine_speed.x = throttle.x = intake_air_temp.x = coolant_temp.x = time_stamps
    for msg in messages:
        engine_speed.y.append(int(msg[0: 4], 16) * 0.39063)
        throttle.y.append(int(msg[8: 12], 16) * 0.0015259)
        intake_air_temp.y.append(9.0 / 5 * hex_to_signed_int8(msg[12: 14]) + 32)
        coolant_temp.y.append(9.0 / 5 * hex_to_signed_int8(msg[14: 16]) + 32)


# process can data with message id 01F0A003
def can_01F0A003():
    df = data_df.loc[(data_df.index == "CAN") & (data_df["Data2"] == "01F0A003")]
    if df.empty:
        print("Warning: No CAN data with message id 01F0A003")
        return
    time_stamps = df["Time(ms)"].to_numpy().astype(float) / 1e6
    messages = df["Data3"].to_list()

    global ve, fuel_pressure, lambda_target, fuel_pump, fan1
    lambda1.x = ign_timing.x = battery_volts.x = time_stamps
    for msg in messages:
        lambda1.y.append(int(msg[0: 2], 16) * 0.00390625 + 0.5)
        ign_timing.y.append(int(msg[10: 12], 16) * 0.35156 - 17)
        battery_volts.y.append(int(msg[12: 16], 16) * 0.0002455)


# process can data with message id 0x01F0A004
def can_01F0A004():
    df = data_df.loc[(data_df.index == "CAN") & (data_df["Data2"] == "01F0A004")]
    if df.empty:
        print("Warning: No CAN data with message id 01F0A004")
        return
    time_stamps = df["Time(ms)"].to_numpy().astype(float) / 1e6
    messages = df["Data3"].to_list()

    global ve, fuel_pressure, lambda_target, fuel_pump, fan1
    ve.x = fuel_pressure.x = lambda_target.x = fuel_pump.x = fan1.x = time_stamps
    for msg in messages:
        ve.y.append(int(msg[4: 6], 16))
        fuel_pressure.y.append(int(msg[6: 8], 16) * 0.580151)
        lambda_target.y.append(int(msg[10: 12], 16) * 0.00390625)
        # the [2:] removes the unnecessary '0b' from string, zfill(8) pads the string with leading zeros
        byte7_bin = bin(int(msg[12: 14], 16))[2:].zfill(8)
        fuel_pump.y.append(int(byte7_bin[-1]))
        fan1.y.append(int(byte7_bin[-2]))


# process can data with message id 0x01F0A005
def can_01F0A005():
    df = data_df.loc[(data_df.index == "CAN") & (data_df["Data2"] == "01F0A005")]
    if df.empty:
        print("Warning: No CAN data with message id 01F0A005")
        return
    time_stamps = df["Time(ms)"].to_numpy().astype(float) / 1e6
    messages = df["Data3"].to_list()

    global launch_ramp_time, mass_airflow
    launch_ramp_time.x = mass_airflow.x = time_stamps
    for msg in messages:
        launch_ramp_time.y.append(int(msg[0: 4], 16) * 10)
        mass_airflow.y.append(int(msg[4: 8], 16) * 0.05)


# process acc data
def acc():
    if "ACC" not in data_df.index:
        print("Warning: No ACC Data")
        return
    global acc_magnitude
    df = data_df.loc["ACC"]

    x_list = df["Data1"].to_numpy().astype(float) / 1e6
    y_list = df["Data2"].to_numpy().astype(float) / 1e6
    z_list = df["Data3"].to_numpy().astype(float) / 1e6

    # calculate the averages of x, y, and z
    avg_times = min(acc_average_times, len(x_list))
    x_avg = np.sum(x_list[0: avg_times], axis=0) / avg_times
    y_avg = np.sum(y_list[0: avg_times], axis=0) / avg_times
    z_avg = np.sum(z_list[0: avg_times], axis=0) / avg_times

    acc_magnitude.x = df["Time(ms)"].to_numpy().astype(float) / 1e6
    # subtract the average from x, y, z to filter out gravity
    acc_magnitude.y = list(np.sqrt(np.square(x_list - x_avg) + np.square(y_list - y_avg) + np.square(z_list - z_avg)))


# process gyr data
def gyr():
    if "GYR" not in data_df.index:
        print("Warning: No GYR Data")
        return
    global rotation_x, rotation_y, rotation_z
    df = data_df.loc["GYR"]

    x_list = df["Data1"].to_numpy().astype(float)
    y_list = df["Data2"].to_numpy().astype(float)
    z_list = df["Data3"].to_numpy().astype(float)

    rotation_x.x = rotation_y.x = rotation_z.x = df["Time(ms)"].to_numpy().astype(float) / 1e6
    rotation_x.y = x_list / 1e3
    rotation_y.y = y_list / 1e3
    rotation_z.y = z_list / 1e3


'''
The following functions are for plotting and displaying graphs
'''


def reset_params():
    global graph_within_range, have_legend, have_grid, y_label, graph_title
    graph_within_range = False
    have_legend = True
    have_grid = True
    y_label = ""
    graph_title = ""


# data is a list of Data that will be plotted
# call this function if you want to have one or multiple datas under a single y-axis
def plot_data(data):
    figure, axis = plt.subplots(1, 1)
    color_index = 0  # which color the next data would be plotted in
    concatenated_title = ""
    for d in data:
        axis.plot(d.x, d.y, color=colors[color_index % len(colors)], label=d.title)
        concatenated_title += d.title + ", "
        color_index += 1

    # default stylistic choices
    axis.set_title(concatenated_title[0: -2])
    axis.set_xlabel("Time (s)")
    if len(data) == 1:
        axis.set_ylabel(data[0].units)
    else:
        axis.set_ylabel("Magnitude (units)")

    # user can overwrite these stylistic elements
    if graph_title != "":
        axis.set_title(graph_title)
    if y_label != "":
        axis.set_ylabel(y_label)
    if graph_within_range:
        axis.set_xlim([x_range_lower, x_range_upper])
        axis.set_ylim([y_range_lower, y_range_upper])
    if have_legend:
        axis.legend()
    if have_grid:
        axis.grid()
    figure.tight_layout()
    reset_params()
    plt.show()


# data is a list of Data that will be plotted
# call this function if you want to have multiple datas under multiple y-axes
def plot_data_multi_axes(data):
    # sort data into groups that share the same units, so that they can share the same y-axis
    data_groups = []
    while len(data) > 0:
        units = data[0].units
        group = []
        i = 0
        while i < len(data):
            if data[i].units == units:
                group.append(data[i])
                data.remove(data[i])
            else:
                i += 1
        data_groups.append(group)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel("Time (s)")

    # create new axes and lines
    lines = []
    color_index = 0
    for d in data:
        if len(lines) == 0:
            axis = ax
        else:
            axis = ax.twinx()
        for d in group:
            line = axis.plot(d.x, d.y, "", label=d.title, color=colors[color_index % len(colors)])
            lines += line  # note that line is a list itself
            color_index += 1
        axis.set_ylabel(group[0].units)
    labels = [l.get_label() for l in lines]

    # stylistic elements
    if graph_title != "":
        ax.set_title(graph_title)
    if graph_within_range:
        ax.set_xlim([x_range_lower, x_range_upper])
        ax.set_ylim([y_range_lower, y_range_upper])
    if have_legend:
        ax.legend(lines, labels, loc=0)
    if have_grid:
        ax.grid()
    fig.tight_layout()
    reset_params()
    plt.show()


if __name__ == '__main__':
    import timeit
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print("Runtime:", stop - start, "s")
