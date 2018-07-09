#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import pandas as pd
from tkinter import ttk
from appdata import AppData
from datetime import datetime


class KPM(tk.Tk):

    def __init__(self, appdata, today_dt):
        tk.Tk.__init__(self)
        assert isinstance(appdata, AppData)
        self.appdata = appdata

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)


        self.frames = {}
        home_frame = HomePage(self.container, self, self.appdata)
        self.frames[HomePage] = home_frame
        table_frame = TodaysLeaderboard(self.container, self, self.appdata, today_dt)
        self.frames[TodaysLeaderboard] = table_frame
        table_frame = ADaysLeaderboard(self.container, self, self.appdata, today_dt)
        self.frames[ADaysLeaderboard] = table_frame

        for f in self.frames.values():
            f.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, controller):
        frame = self.frames[controller]
        frame.tkraise()

    def refresh_frame(self, controller, input):
        # if controller in self.frames:
        self.frames[controller].destroy()
        self.frames[controller] = ADaysLeaderboard(self.container, self, self.appdata, input)
        self.frames[controller].grid(row=0, column=0, sticky="nsew")
        self.frames[controller].tkraise()



class HomePage(tk.Frame):

    def __init__(self, parent, controller, appdata):

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="KPM Dashboard", font=("Arial", 15))
        label.grid(row=0, columnspan=3)

        b1 = ttk.Button(self, text="Today's Leaderboard",
                       command=lambda: controller.show_frame(TodaysLeaderboard))
        b1.grid(row=1, columnspan=3)

        ## dropdown to specify date
        date = tk.StringVar()
        dropdown_label = ttk.Label(self, text="Select date:", width=10, anchor='w')
        dates_in_df = [datetime.strftime(d, "%Y-%m-%d") for d in appdata.df.columns]
        dropdown = tk.OptionMenu(*(self, date) + tuple(dates_in_df))
        # dropdown_row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        dropdown_label.grid(row=2, column=0)
        dropdown.grid(row=2, column=1)

        b2 = ttk.Button(self, text="Get Leaderboard",
                       command=lambda: controller.refresh_frame(ADaysLeaderboard, datetime.strptime(date.get(), "%Y-%m-%d")))
        b2.grid(row=2, column=2)




class DailyLeaderboard(tk.Frame):

    def __init__(self, parent, controller, appdata, dt):
        tk.Frame.__init__(self, parent)
        self.dt = dt
        self._widgets = []

        df = appdata.get_leaderboard_by_date(dt)

        # get rows and column sizes of df, add 1 for headers and index
        rows = df.shape[0] + 1
        columns = 2

        for row in range(rows):
            current_row = []
            for column in range(columns):
                label = ttk.Label(self, text="",
                                 borderwidth=0, width=10)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)

        button = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))

        button.grid(row=rows, columnspan=columns)
        self.grid_rowconfigure(rows, weight=11)

        self.fill_table(df)

    def fill_table(self, df):

        self.__set(0, 1, self.dt)
        row_num = 1
        for ind in df.index:
            self.__set(row_num, 0, ind)
            self.__set(row_num, 1, df[ind])

            row_num += 1

    def __set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)


class TodaysLeaderboard(DailyLeaderboard):
    def __init__(self, parent, controller, appData, dt):
        DailyLeaderboard.__init__(self, parent, controller, appData, dt)

class ADaysLeaderboard(DailyLeaderboard):
    def __init__(self, parent, controller, appData, dt):
        DailyLeaderboard.__init__(self, parent, controller, appData, dt)




if __name__ == "__main__":


    d = AppData("sample_data.csv")
    print(d.df)

    dashboard = KPM(d, datetime(2017, 1, 1))
    dashboard.mainloop()
