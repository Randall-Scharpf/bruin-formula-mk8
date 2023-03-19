import globalfonts
import datetime
from datetime import datetime as dt


MS_PER_UPDATE = 100
ELAPSED_MSG_TOLERANCE = 1
ELAPSED_MSG_MAX = 99
FPS_UPDATE_TIME = 1

USE_SYS_TIME = False
TIME_DISPLAY_FORMAT = '%m/%d/%y %I:%M:%S %p %a'
# FPSLabel to MPSLabel


class UpdateTimer():
    __timestamp = dt.now().timestamp()
    __prev_timer_seconds = -1
    __prev_disconnection = -2
    __prev_msg_timestamp = (dt.now() - datetime.timedelta(seconds=1)).timestamp()
    __prev_fps_update = dt.now()
    __elapsed_num_messages = 0

    def __init__(self, main_win):
        self.main_win = main_win

    def on_update_labels(self):
        sys_dt_object = dt.now()

        # update Time Label if changes should be made
        if self.__prev_timer_seconds != sys_dt_object.second:
            if USE_SYS_TIME:
                time_display = sys_dt_object.strftime('(ST) ' + TIME_DISPLAY_FORMAT)
            else:
                time_display = dt.fromtimestamp(self.__timestamp).strftime(TIME_DISPLAY_FORMAT)
            self.__prev_timer_seconds = sys_dt_object.second
            self.main_win.TimeLabel.setText(time_display)

        # update CAN Hat Status
        disconnection_time = int((sys_dt_object - dt.fromtimestamp(self.__prev_msg_timestamp)).total_seconds())
        if disconnection_time >= ELAPSED_MSG_TOLERANCE and self.__prev_disconnection != disconnection_time:
            self.main_win.CANConnectionLabel.setText('No Connection (' + str(min(ELAPSED_MSG_MAX, disconnection_time)) + ')')
            self.main_win.CANStatusLabel.setStyleSheet(globalfonts.FONT_CSS + 'color: red;' + globalfonts.TRANSPARENT_CSS + globalfonts.scaled_css_size(25))
            self.__prev_disconnection = disconnection_time
        elif disconnection_time < ELAPSED_MSG_TOLERANCE and self.__prev_disconnection != -1:
            self.main_win.CANConnectionLabel.setText('Connected')
            self.main_win.CANStatusLabel.setStyleSheet(globalfonts.FONT_CSS + 'color: green;' + globalfonts.TRANSPARENT_CSS + globalfonts.scaled_css_size(25))
            self.__prev_disconnection = -1

        # update FPS label
        global FPS_UPDATE_TIME
        if (sys_dt_object - self.__prev_fps_update).total_seconds() > FPS_UPDATE_TIME:
            self.main_win.FPSLabel.setText("FPS: " + str(min(999, int(self.__elapsed_num_messages / FPS_UPDATE_TIME))))
            self.__elapsed_num_messages = 0
            self.__prev_fps_update = sys_dt_object

    # if you want to add @pyqtSlot(int) before the function, you have to make this class inherit QObject
    # and initialize the QObject by calling super's __init__, too much work, I'll just not leave this line here
    def on_receive_data(self, timestamp):
        self.__timestamp = timestamp
        self.__prev_msg_timestamp = dt.now().timestamp()
        self.__elapsed_num_messages += 1
