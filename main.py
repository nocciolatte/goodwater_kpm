#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import tkinter as tk
from datetime import datetime
import matplotlib.pyplot as plt

from appdata import AppData
from kpm import KPM




if __name__ == "__main__":
    d = AppData("sample_data.csv")
    today = datetime(2017, 1, 1)
    print(d.df)
    print(d.get_leaderboard_by_date(today))
    print(d.get_sums_by_date_range('1/1/2017', '1/7/2017'))

    plt.figure()

    d.plot_app_data_in_date_range('Facebook', '1/1/2017', '1/6/2017')
    d.plot_data_in_date_range('1/1/2017', '1/6/2017')

    plt.show()


    dashboard = KPM(d, today)
    dashboard.mainloop()

    # print(d.get_means_by_date_range('1/1/2017', '1/4/2017'))
    # print(d.get_mins_by_date_range('1/1/2017', '1/4/2017'))
    # print(d.get_maxs_by_date_range('1/1/2017', '1/4/2017'))
    # print(d.get_app_ranking_by_date('Pinterest', '1/1/2017'))

    # print(d.get_max_within_range('1/1/2017', '1/4/2017'))
