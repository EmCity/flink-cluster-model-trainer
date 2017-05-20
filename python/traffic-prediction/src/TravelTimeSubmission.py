"""
Created on Wed May 19 20:40:00 2017

@author: Christian
"""
import os
import numpy as np
import pandas as pd
from datetime import timedelta
from datetime import time
from datetime import date
from datetime import datetime


class TravelTimeSubmission:
    """
    Input:
        A structure of lists
        Example: 
            [days[time_window_sets[time_window_set[routes[route[time_avg]]]]]]
    
            days
            -day
            --time_window_sets
            ---time_window_set
            ----routes
            -----route
            ------time_avg
        Or a DataFrame with ['intersection_id', 'tollgate_id', 'time_window', 'avg_travel_time'] as columns
    
    """

    table_columns = ['intersection_id', 'tollgate_id', 'time_window', 'avg_travel_time']

    # list of routes with tuple (intersection_id, tollgate_id)
    routes = [('A', '2'), ('A', '3'), ('B', '1'), ('B', '3'), ('C', '1'), ('C', '3')]

    time_windows_sets = [[(time(8, 0, 0), time(8, 20, 0)),
                          (time(8, 20, 0), time(8, 40, 0)),
                          (time(8, 40, 0), time(9, 0, 0)),
                          (time(9, 0, 0), time(9, 20, 0)),
                          (time(9, 20, 0), time(9, 40, 0)),
                          (time(9, 40, 0), time(10, 0, 0))]
        ,
                         [(time(17, 0, 0), time(17, 20, 0)),
                          (time(17, 20, 0), time(17, 40, 0)),
                          (time(17, 40, 0), time(18, 0, 0)),
                          (time(18, 0, 0), time(18, 20, 0)),
                          (time(18, 20, 0), time(18, 40, 0)),
                          (time(18, 40, 0), time(19, 0, 0)),
                          ]
                         ]

    def save_df_travel_time_submission(self, travel_time_df, filepath='..\\dataset',
                                       file_name='submission_travelTime.csv'):
        """
        Creates the submission file for task1: "estimated travel time average"

        The generated File:
            the file has the format:
            intersection_id,tollgate_id,time_window,avg_travel_time
            datatypes are:
            string, string, string, float(s)
            time_window with a touple of start_time and end_time with ISO 8601 "yyyy-MM-dd HH:mm:ss" enclosed by "[)"(right half-open interval) and seperated by ","
            example row:
            "A","2","[2016-10-18 08:00:00,2016-10-18 08:20:00)",681.3
            the file should have 504 datapoints

        Args:
            travel_time_df (pandas dataframe): the function takes a pandas dataframe with the following columns:
                intersection_id, tollgate_id, time_window, avg_travel_time
                    time_window ([timestamp, timestamp]): is a tuple of start_time and end_time as datetime.timestamp
            filepath (string, optional): 

            file_name (string, optional):

        """
        df = travel_time_df

        file = '.' + os.sep + filepath + os.sep + file_name
        print(file)

        # round to two decimals
        decimals = pd.Series([2])
        df['avg_travel_time'] = df['avg_travel_time'].round(decimals)

        # sort it like the sample
        df['start_tw'] = pd.to_datetime(df['time_window'].str[1:20])
        df['end_tw'] = pd.to_datetime(df['time_window'].str[21:-1])
        df['time_window_set_evening'] = (df['time_window'].str[12:14].astype(int) > 13)
        df = df.sort_values(['time_window_set_evening', 'intersection_id', 'tollgate_id', 'time_window'])
        df = df[['intersection_id', 'tollgate_id', 'time_window', 'avg_travel_time']]

        # write file
        df.to_csv(file, index=False)

        return True

    def by_time_window_set(self, date, time_windows_set, data_time_window_set):

        routes_tws = []
        for index_tw, route in enumerate(data_time_window_set):
            tws = []

            for index_r, avg_time in enumerate(route):
                time_window_str = '['
                time_window_str += str(datetime.combine(date, time_windows_set[index_tw][0]))
                time_window_str += ','
                time_window_str += str(datetime.combine(date, time_windows_set[index_tw][1]))
                time_window_str += ')'

                entry = [self.routes[index_r][0],
                         self.routes[index_r][1],
                         time_window_str,
                         avg_time]

                #print(entry)
                tws.append(entry)

            for tws_entry in tws:
                routes_tws.append(tws_entry)

        df = pd.DataFrame(routes_tws, columns=self.table_columns)
        return df

    def by_time_window_sets(self, date, data_time_window_sets):
        # there are two time_window_sets for each day. First is for morning, second is for evening.

        df1 = self.by_time_window_set(date, self.time_windows_sets[0], data_time_window_sets[0])
        df2 = self.by_time_window_set(date, self.time_windows_sets[1], data_time_window_sets[1])

        df = pd.concat([df1, df2])
        # print(df)

        return df

    def by_days(self, day_list, first_day=date(2016, 10, 18)):
        date_day = first_day
        df = self.by_time_window_sets(date_day, day_list[0])
        for day_index, day_entry in enumerate(day_list[1:]):
            date_day = date_day + timedelta(days=1)  # next date
            df2 = self.by_time_window_sets(date_day, day_entry)
            df = pd.concat([df, df2])

        return df

    def travel_time_submission(self, data_days_list, first_day=date(2016, 10, 18), filepath='..\\dataset',
                               file_name='submission_travelTime.csv', save_csv=True):
        """
        Use this method to safe a submission csv file with a structure of lists.
        The structure is maybe a bit complicated. I hope it makes sense.
        
        Level 1: list of days
        Level 2: the day entry has a time_window_sets_list (there are two sets. First for the time_windows in the morning 8-10 and Second for the time_windows in theevening 17-19)
        Level 3: the time_window_set havs 6 time_windows
        Level 4: a time_window contains the 6 routes_lists
        Level 5: one route contains 6 avg_time_values sorted like [('A', '2'), ('A', '3'), ('B', '1'), ('B', '3'), ('C', '1'), ('C', '3')]  
        
        
        
        Args:
            days_list: look above
            first_day (datetime.date, optional): the first day in list. datetime(2016,10,18) or datetime(2016,10,25) (def:2016,10,18)
        
        """
        df = self.by_days(data_days_list, first_day)

        if (save_csv):
            self.save_df_travel_time_submission(df, filepath, file_name)

        return df
