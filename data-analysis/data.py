import pandas as pd
import matplotlib
import matplotlib.backends.backend_tkagg
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

matplotlib.use('tkagg')

# is the maximum number of samples acc() will average over, cannot be 0
acc_average_times = 5
# a list of color chars, can change this to add more colors
colors = list("bgrcmy")
'''
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
'''


# data class to help keep track of different types of data
class Data:
    def __init__(self, title, units):
        self.title = title
        self.units = units
        # parameters that will be passed to matplotlib
        self.x = []  # x is usually time
        self.y = []  # y is the value of the data


# all the data that we want to keep track of
all_data = ["Acceleration Magnitude", "Battery Voltage", "Coolant Temperature", "Engine Speed",
            "Exhaust Gas Temperature", "Fan on/off", "Fuel Pressure","Fuel Pump on/off", "Ignition Timing",
            "Injector Duty Cycle","Intake Air Temperature", "Lambda", "Lambda Feedback", "Lambda Target", 
            "Lin Pot FR", "Lin Pot FL", "Lin Pot RL", "Lin Pot RR", 
            "Mass Airflow", "Manifold Absolute Pressure", "RPM Limit", 
            "Rotation X", "Rotation Y", "Rotation Z", "Throttle %",
            "FL Wheel Speed", "FR Wheel Speed", "RL Wheel Speed", "RR Wheel Speed",
            "Volumetric Efficiency", "Gear", "Shifter"]
# acc data
acc_magnitude = Data("Acceleration Magnitude", "g")
# egt data
egt = Data("Exhaust Gas Temp", "F")
# can data with message id = 01F0A000
engine_speed = Data("Engine Speed", "RPM")
throttle = Data("Throttle", "%")
intake_air_temp = Data("Intake Air Temp", "F")
coolant_temp = Data("Coolant Temp", "F")
# can data with message id = 0x01F0A003
lambda1 = Data("Lambda #1", "Lambda")
ign_timing = Data("Ignite Timing", "Deg")
battery_volts = Data("Battery Volts", "Volts")
gear = Data("Gear", "Gear #")
# can data with message id = 0x01F0A004
manifold_pressure = Data("Manifold Absolute Pressure", "kPa")
ve = Data("Volumetric Efficiency", "%")
fuel_pressure = Data("Fuel Pressure", "PSIg")
lambda_target = Data("Lambda Target", "Lambda")
lambda_feedback = Data("Lambda Feedback", "%")
fuel_pump = Data("Fuel Pump", "bool")
fan1 = Data("Fan 1", "bool")
# can data with message id = 0x01F0A005
launch_ramp_time = Data("Launch Ramp Time", "ms")
mass_airflow = Data("Mass Airflow", "gms/s")
# can data with message id = 0x01F0A006
inj_duty = Data("Injector Duty Cycle", "%")
#can data with message id = 0x01F0A008
rpm_limit = Data("RPM Limit", "RPM")
#can data with message id = 0x01F0A011
fl_wheel_speed = Data("FL Wheel Speed", "mph")
fr_wheel_speed = Data("FR Wheel Speed", "mph")
rl_wheel_speed = Data("RL Wheel Speed", "mph")
rr_wheel_speed = Data("RR Wheel Speed", "mph")
# gyr data
rotation_x = Data("Rotation X", "deg/s")
rotation_y = Data("Rotation Y", "deg/s")
rotation_z = Data("Rotation Z", "deg/s")
shifting = Data("Shifter", "up/down")
# can data with message id = 0xC?01000 where ? is 0, 1, 2, 3 for FR, FL, RL, RR
lin_pot_fr = Data("Lin Pot FR", "mm")
lin_pot_fl = Data("Lin Pot FL", "mm")
lin_pot_rl = Data("Lin Pot RL", "mm")
lin_pot_rr = Data("Lin Pot RR", "mm")

# data frame containing all data imported from files
data_df = None


def load(csv):
    load_data(csv)
    acc()
    can_01F0A000()
    can_01F0A003()
    can_01F0A004()
    can_01F0A005()
    can_01F0A006()
    can_01F0A008()
    can_01F0A011()
    load_lin_pots()
    load_egt()
    gyr()
    shf()


def select_choices(choices):
    data_types = []
    if "Acceleration Magnitude" in choices:
        data_types.append(acc_magnitude)
    if "Battery Voltage" in choices:
        data_types.append(battery_volts)
    if "Coolant Temperature" in choices:
        data_types.append(coolant_temp)
    if "Engine Speed" in choices:
        data_types.append(engine_speed)
    if "Exhaust Gas Temperature" in choices:
        data_types.append(egt)
    if "Fan on/off" in choices:
        data_types.append(fan1)
    if "Fuel Pressure" in choices:
        data_types.append(fuel_pressure)
    if "Fuel Pump on/off" in choices:
        data_types.append(fuel_pump)
    if "Ignition Timing" in choices:
        data_types.append(ign_timing)
    if "Injector Duty Cycle" in choices:
        data_types.append(inj_duty)
    if "Intake Air Temperature" in choices:
        data_types.append(intake_air_temp)
    if "Lambda" in choices:
        data_types.append(lambda1)
    if "Lambda Target" in choices:
        data_types.append(lambda_target)
    if "Lambda Feedback" in choices:
        data_types.append(lambda_feedback)
    if "Lin Pot FR" in choices:
        data_types.append(lin_pot_fr)
    if "Lin Pot FL" in choices:
        data_types.append(lin_pot_fl)
    if "Lin Pot RL" in choices:
        data_types.append(lin_pot_rl)
    if "Lin Pot RR" in choices:
        data_types.append(lin_pot_rr)
    if "Mass Airflow" in choices:
        data_types.append(mass_airflow)
    if "Manifold Absolute Pressure" in choices:
        data_types.append(manifold_pressure)
    if "RPM Limit" in choices:
        data_types.append(rpm_limit)
    if "Rotation X" in choices:
        data_types.append(rotation_x)
    if "Rotation Y" in choices:
        data_types.append(rotation_y)
    if "Rotation Z" in choices:
        data_types.append(rotation_z)
    if "Throttle %" in choices:
        data_types.append(throttle)
    if "Volumetric Efficiency" in choices:
        data_types.append(ve)
    if "FL Wheel Speed" in choices:
        data_types.append(fl_wheel_speed)
    if "FR Wheel Speed" in choices:
        data_types.append(fr_wheel_speed)
    if "RL Wheel Speed" in choices:
        data_types.append(rl_wheel_speed)
    if "RR Wheel Speed" in choices:
        data_types.append(rr_wheel_speed)
    if "Gear" in choices:
        data_types.append(gear)
    if "Shifter" in choices:
        data_types.append(shifting)
    return data_types


# read all file and store them in data_df
def load_data(file):
    global data_df
    data_df = pd.read_csv(file, index_col=0, names=["Message Type", "Time(ms)", "Data1", "Data2", "Data3"],
                          dtype=str)
    '''
    another way to structure data_df: message type will become its own column instead of being the index column
    for file in filenames:
        df_list.append(pd.read_csv(filepath, index_col=False, names=["Message Type", "Time(ms)", "Data1", "Data2",
                                   "Data3"]))
    data_df = pd.concat(df_list, axis=0, ignore_index=True)
    '''
    print("Imported data frame:")
    print(data_df)


# save data into csv
def save_data1(file, data_selected):
    dictionary = {"time(ms)": [], "value(units)": []}
    for data_name in data_selected:
        data_type = select_choices([data_name])[0]
        dictionary["time(ms)"].append("")
        dictionary["value(units)"].append("")
        dictionary["time(ms)"].append(data_type.title + " (" + data_type.units + ")")
        dictionary["value(units)"].append("")
        dictionary["time(ms)"].extend(data_type.x)
        dictionary["value(units)"].extend(data_type.y)
    pd.DataFrame(dictionary).to_csv(file, header=False, index=False)


'''
The following functions process data_df and store data in corresponding global Data variables
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


# receives a dataframe and a column name, returns a numpy array of the
# corresponding column in the dataframe in floats
# when there is only one value in the interested column, df[col_name]
# will return a string value as opposed to a Series
def df_to_float_numpy(df, col_name):
    col = df[col_name]
    if type(col) == str:
        return np.array([col], dtype=float)
    else:
        return col.to_numpy().astype(float)


# process can data with message id 01F0A000
def can_01F0A000():
    df = data_df.loc[(data_df.index == "CAN") & (data_df["Data2"] == "01F0A000")]
    if df.empty:
        print("Warning: No CAN data with message id 01F0A000")

    time_stamps = df_to_float_numpy(df, "Time(ms)") / 1e6  # to make timestamps in seconds
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

    time_stamps = df_to_float_numpy(df, "Time(ms)") / 1e6
    messages = df["Data3"].to_list()

    global ve, fuel_pressure, lambda_target, fuel_pump, fan1
    lambda1.x = ign_timing.x = battery_volts.x = time_stamps
    for msg in messages:
        lambda1.y.append(int(msg[0: 2], 16) * 0.00390625 + 0.5)
        ign_timing.y.append(int(msg[10: 12], 16) * 0.35156 - 17)
        battery_volts.y.append(int(msg[12: 16], 16) * 0.0002455)

    # we don't want to show neutral in logs (it just adds confusion)
    for i in range(1,len(messages)):
        if(int(messages[i][8: 10], 16) != 7):
            gear.x.append(time_stamps[i])
            gear.y.append(int(messages[i][8: 10], 16))


# process can data with message id 0x01F0A004
def can_01F0A004():
    df = data_df.loc[(data_df.index == "CAN") & (data_df["Data2"] == "01F0A004")]
    if df.empty:
        print("Warning: No CAN data with message id 01F0A004")

    time_stamps = df_to_float_numpy(df, "Time(ms)") / 1e6
    messages = df["Data3"].to_list()

    global ve, manifold_pressure, fuel_pressure, lambda_target, fuel_pump, fan1
    manifold_pressure.x = ve.x = fuel_pressure.x = lambda_target.x = fuel_pump.x = fan1.x = time_stamps
    for msg in messages:
        ve.y.append(int(msg[4: 6], 16))
        manifold_pressure.y.append(int(msg[0: 4], 16) * 0.1)
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

    time_stamps = df_to_float_numpy(df, "Time(ms)") / 1e6
    messages = df["Data3"].to_list()

    global launch_ramp_time, mass_airflow
    launch_ramp_time.x = mass_airflow.x = time_stamps
    for msg in messages:
        launch_ramp_time.y.append(int(msg[0: 4], 16) * 10)
        mass_airflow.y.append(int(msg[4: 8], 16) * 0.05)


# process can data with message id 0x01F0A006
def can_01F0A006():
    df = data_df.loc[(data_df.index == "CAN") & (data_df["Data2"] == "01F0A006")]
    if df.empty:
        print("Warning: No CAN data with message id 01F0A006")

    time_stamps = df_to_float_numpy(df, "Time(ms)") / 1e6
    messages = df["Data3"].to_list()

    global inj_duty, lambda_feedback
    inj_duty.x = time_stamps
    lambda_feedback.x = time_stamps
    for msg in messages:
        inj_duty.y.append(int(msg[6: 10], 16) * 0.392157)
        lambda_feedback.y.append(int(msg[2:4], 16) * 0.5 - 64)


# process can data with message id 0x01F0A008
def can_01F0A008():
    df = data_df.loc[(data_df.index == "CAN") & (data_df["Data2"] == "01F0A008")]
    if df.empty:
        print("Warning: No CAN data with message id 01F0A008")

    time_stamps = df_to_float_numpy(df, "Time(ms)") / 1e6
    messages = df["Data3"].to_list()

    global rpm_limit
    rpm_limit.x = time_stamps
    for msg in messages:
        rpm_limit.y.append(int(msg[6: 10], 16) * 0.39063)


# process can data with message id 0x01F0A011
def can_01F0A011():
    df = data_df.loc[(data_df.index == "CAN") & (data_df["Data2"] == "01F0A011")]
    if df.empty:
        print("Warning: No CAN data with message id 01F0A011")

    time_stamps = df_to_float_numpy(df, "Time(ms)") / 1e6
    messages = df["Data3"].to_list()

    global fl_wheel_speed, fr_wheel_speed, rl_wheel_speed, rr_wheel_speed
    fl_wheel_speed.x = time_stamps
    rl_wheel_speed.x = time_stamps
    fr_wheel_speed.x = time_stamps
    rr_wheel_speed.x = time_stamps
    for msg in messages:
        fl_wheel_speed.y.append(int(msg[0:4], 16) * 0.02 / 1.609)
        fr_wheel_speed.y.append(int(msg[4:8], 16) * 0.02 / 1.609)
        rl_wheel_speed.y.append(int(msg[8:12], 16) * 0.02 / 1.609)
        rr_wheel_speed.y.append(int(msg[12:16], 16) * 0.02 / 1.609)


def load_lin_pots():
    df_fr = data_df.loc[(data_df.index == "CAN") & (data_df["Data2"] == "0C001000")]
    df_fl = data_df.loc[(data_df.index == "CAN") & (data_df["Data2"] == "0C101000")]
    df_rl = data_df.loc[(data_df.index == "CAN") & (data_df["Data2"] == "0C201000")]
    df_rr = data_df.loc[(data_df.index == "CAN") & (data_df["Data2"] == "0C301000")]

    if df_fr.empty:
        print("Warning: No lin pot data from FR")
    if df_fl.empty:
        print("Warning: No lin pot data from FL")
    if df_rl.empty:
        print("Warning: No lin pot data from RL")
    if df_rr.empty:
        print("Warning: No lin pot data from RR")

    global lin_pot_fr, lin_pot_fl, lin_pot_rl, lin_pot_rr

    lin_pot_fr.x = df_to_float_numpy(df_fr, "Time(ms)") / 1e6
    lin_pot_fl.x = df_to_float_numpy(df_fl, "Time(ms)") / 1e6
    lin_pot_rl.x = df_to_float_numpy(df_rl, "Time(ms)") / 1e6
    lin_pot_rr.x = df_to_float_numpy(df_rr, "Time(ms)") / 1e6

    for msg in df_fr["Data3"].to_list():
        lin_pot_fr.y.append(int(msg[0:4], 16) * 75./1023.)

    for msg in df_fl["Data3"].to_list():
        lin_pot_fl.y.append(int(msg[0:4], 16) * 75./1023.)

    for msg in df_rl["Data3"].to_list():
        lin_pot_rl.y.append(int(msg[0:4], 16) * 75./1023.)

    for msg in df_rr["Data3"].to_list():
        lin_pot_rr.y.append(int(msg[0:4], 16) * 75./1023.)


# process can data with message id 00DA5401 (egt data)
def load_egt():
    df = data_df.loc[data_df.index == "EGT"]
    if df.empty:
        print("Warning: No EGT data")

    time_stamps = df_to_float_numpy(df, "Time(ms)") / 1e6
    messages = df_to_float_numpy(df, "Data1")

    global egt
    egt.x = time_stamps
    for msg in messages:
        egt.y.append(msg * 9/5 + 32)

# process acc data
def acc():
    if "ACC" not in data_df.index:
        print("Warning: No ACC Data")
        return

    global acc_magnitude
    df = data_df.loc[data_df.index == "ACC"]

    x_list = df_to_float_numpy(df, "Data1") / 1e6
    y_list = df_to_float_numpy(df, "Data2") / 1e6
    z_list = df_to_float_numpy(df, "Data3") / 1e6

    # calculate the averages of x, y, and z
    avg_times = min(acc_average_times, len(x_list))
    x_avg = np.sum(x_list[0: avg_times], axis=0) / avg_times
    y_avg = np.sum(y_list[0: avg_times], axis=0) / avg_times
    z_avg = np.sum(z_list[0: avg_times], axis=0) / avg_times

    acc_magnitude.x = df_to_float_numpy(df, "Time(ms)") / 1e6
    # subtract the average from x, y, z to filter out gravity
    acc_magnitude.y = list(np.sqrt(np.square(x_list - x_avg) + np.square(y_list - y_avg) + np.square(z_list - z_avg)))


# process gyr data
def gyr():
    if "GYR" not in data_df.index:
        print("Warning: No GYR Data")

    global rotation_x, rotation_y, rotation_z
    df = data_df.loc[data_df.index == "GYR"]

    x_list = df_to_float_numpy(df, "Data1")
    y_list = df_to_float_numpy(df, "Data2")
    z_list = df_to_float_numpy(df, "Data3")

    rotation_x.x = rotation_y.x = rotation_z.x = df_to_float_numpy(df, "Time(ms)") / 1e6
    rotation_x.y = x_list / 1e3
    rotation_y.y = y_list / 1e3
    rotation_z.y = z_list / 1e3

def shf():
    df = data_df.loc[data_df.index == "SHF"]
    if df.empty:
        print("Warning: No SHF Data")

    df = df.replace('UPSHIFT', 1, regex=True)
    df = df.replace('DOWNSHIFT', -1, regex=True)

    time_stamps = df_to_float_numpy(df, "Time(ms)") / 1e6
    messages = df_to_float_numpy(df, "Data1")

    global shifting
    for i in range(0,len(time_stamps)):
        shifting.x.append(time_stamps[i])
        if(i < len(time_stamps)-1):
            for j in range(time_stamps[i].astype(int)*100, time_stamps[i+1].astype(int)*100):
                shifting.x.append(j/100)
    for i in range(0, len(time_stamps)):
        shifting.y.append(messages[i])
        if(i < len(messages)-1):
            for j in range(time_stamps[i].astype(int)*100, time_stamps[i+1].astype(int)*100):
                shifting.y.append(0)

'''
if __name__ == '__main__':
    import timeit

    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print("Runtime:", stop - start, "s")
'''