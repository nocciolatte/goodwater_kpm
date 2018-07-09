#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
from datetime import datetime


class AppData(object):

    def __init__(self, datafile, **kwargs):
        assert datafile
        self._raw = datafile

        # read data format specifier; if none, default to csv
        if "data_format" in kwargs.keys():
            if kwargs["data_format"] == "csv":
                self.__read_csv()
            elif kwargs["data_format"] == "xslt":
                self.__read_xslt()
            elif kwargs["data_format"] == "json":
                self.__read_json()
        else:
            self.__read_csv()

    def __read_csv(self):
        assert self._raw

        app_data = pd.read_csv(self._raw, sep="\s+", header=[0])
        # convert the column date strings to dt objects
        conversion = dict(zip(app_data.columns[1:], pd.to_datetime(app_data.columns[1:])))
        self.df = app_data.rename(columns=conversion)
        self.df.set_index('AppName', inplace=True)


    def __read_xslt(self):
        pass


    def __read_json(self):
        pass


    def get_leaderboard_by_date(self, dt):
        assert dt
        try:
            dl_data = self.df[dt].copy().sort_values(ascending=False)
        except KeyError:
            print("Data doesn't exist for the date %s provided" % dt)
            return pd.DataFrame()
        return dl_data



    def get_sums_by_date_range(self, dt_start, dt_end):
        df = self.__get_data_by_date_range(dt_start, dt_end)
        return df.sum(axis=1)

    def get_means_by_date_range(self, dt_start, dt_end):
        df = self.__get_data_by_date_range(dt_start, dt_end)
        return df.mean(axis=1)

    def get_mins_by_date_range(self, dt_start, dt_end):
        df = self.__get_data_by_date_range(dt_start, dt_end)
        return df.min(axis=1)

    def get_maxs_by_date_range(self, dt_start, dt_end):
        df = self.__get_data_by_date_range(dt_start, dt_end)
        return df.max(axis=1)


    def get_app_ranking_by_date(self, appName, dt):
        df = self.__get_data_by_date_range(dt, dt)
        return pd.Series.rank(df, ascending=False).loc[appName]

    def get_max_within_date_range(self, dt_start, dt_end):
        assert dt_start
        assert dt_end
        assert datetime.strptime(dt_end, "%m/%d/%Y") >= datetime.strptime(dt_start, "%m/%d/%Y")
        df = self.__get_data_by_date_range(dt_start, dt_end)
        if df.empty:
            return pd.DataFrame()
        sums = df.sum(axis=1)
        return sums[sums==sums.max(axis=0)]


    def plot_app_data_in_date_range(self, appName, dt_start, dt_end):
        df = self.__get_app_data_by_date_range(appName, dt_start, dt_end)
        return df.T.plot()


    def plot_data_in_date_range(self, dt_start, dt_end):
        df = self.__get_data_by_date_range(dt_start, dt_end)
        return df.T.plot()

    def __get_data_by_date_range(self, start, end):
        assert start
        assert end
        assert datetime.strptime(end, "%m/%d/%Y") >= datetime.strptime(start, "%m/%d/%Y")

        dt_range = pd.date_range(start, end)

        try:
            dl_data = self.df[dt_range].copy()
        except KeyError:
            print("Data doesn't exist for the dates %s-%s provided" % (start, end))
            return pd.DataFrame()
        return dl_data

    def __get_app_data_by_date_range(self, appName, start, end):
        assert appName
        assert start
        assert end
        assert datetime.strptime(end, "%m/%d/%Y") >= datetime.strptime(start, "%m/%d/%Y")
        dt_range = pd.date_range(start, end)

        try:
            df = self.df[dt_range].loc[appName].copy()
        except KeyError:
            print("Data doesn't exist for the app during the date range provided" , appName, dt_range)
            return pd.DataFrame()
        return df
