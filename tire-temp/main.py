import numpy as np
import pandas as pd
import easygui

def main():
    data = pd.read_csv(easygui.fileopenbox(), index_col=3, names=["type", "time", "flags", "id", "msg"], dtype=str)
    can_data = data.loc[data["type"] == "CAN"]
    print(can_data.loc["id"])





if __name__ == '__main__':
    main()
