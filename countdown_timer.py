import math
import time
import datetime
from datetime import date
import tkinter
from tkinter import *

clock_ = None


class Countdown_Timer:
    def __init__(self):
        self.d_time_curr = datetime.datetime.now()
        self.d_time_curr_fmtt = self.d_time_curr.strftime("%d %B %y, %A")
        self.d_time = None
        self.update_timer_text_year = False

        self.date_line = None
        self.date_year = None
        self.date_month = None
        self.date_day = None
        self.seconds_remaining = 0

        self.seconds_day = 24 * 60 * 60
        self.ave_days_p_mth = 30.437
        self.years = 0
        self.months = 0
        self.weeks = 0
        self.days = 0
        self.hours = 0
        self.minutes = 0
        self.seconds_remaining_5 = 0


    def time_left(self):
        print(self.d_time_curr.strftime("%d %B %y, %A"))
        self.d_time = date(self.d_time_curr.year, self.d_time_curr.month, self.d_time_curr.day)
        self.d_2022_1 = date(2022, 1, 1)
        print(self.date_line)
        print(self.d_time)

        difference_year = self.date_line - self.d_2022_1
        days_year = difference_year.days
        difference = self.date_line - self.d_time
        days_remaining = difference.days
        print(f"{days_remaining} days remaining| {days_year} days")

        if days_remaining > 0:
            self.seconds_remaining = days_remaining * 24 * 60 * 60
            hour_value = int(datetime.datetime.now().strftime("%H"))
            print(f"Hour of day: {hour_value}")
            min_value = int(datetime.datetime.now().strftime("%M"))
            print(f"Minute of day: {min_value}")
            sec_value = int(datetime.datetime.now().strftime("%S"))

            # OBTAIN THE HOUR/MIN/SECONDS VALUE THROUGH datetime.now IF DAY <=1
            # THEN REASSIGN seconds_remaining accordingly
            if self.seconds_remaining <= (24 * 60 * 60):
                self.seconds_remaining = (24 - hour_value) * 60 * 60 - min_value * 60 - sec_value
                print(self.seconds_remaining)
            else:
                self.seconds_remaining -= ((hour_value) * 60 * 60 + min_value * 60 + sec_value)
        else:
            print("PLEASE ENTER VALID DATE")


    # Want the count down function to proc every second and update a timer object on the webpage
    # ASSIGN COUNTDOWN OUTPUT TO HTML TO DISPLAY ON WEBPAGE
    def count_down(self):
        global clock_

        # Floor everything bcos the remainder goes to the next iterable
        # (year/month/week/day/hour/minute/second)
        # (365/12/7/24/60/60/1)

        self.years = math.floor(self.seconds_remaining / (self.seconds_day * 30 * 12))
        print(f" {self.years} years")
        seconds_remaining_0 = self.seconds_remaining - math.floor(
            self.years * (self.seconds_day * 30 * 12))

        self.months = math.floor(seconds_remaining_0 / (self.seconds_day * 30))
        print(f" {self.months} months")
        seconds_remaining_1 = seconds_remaining_0 - math.floor(self.months * (self.seconds_day * 30))

        self.weeks = math.floor(seconds_remaining_1 / (7 * self.seconds_day))
        print(f" {self.weeks} weeks")
        seconds_remaining_2 = seconds_remaining_1 - math.floor(self.weeks * (self.seconds_day * 7))

        self.days = math.floor(seconds_remaining_2 / self.seconds_day)
        print(f" {self.days} days")
        seconds_remaining_3 = seconds_remaining_2 - math.floor(self.days * (self.seconds_day))

        self.hours = math.floor(seconds_remaining_3 / (60 * 60))
        print(f" {self.hours} hours")
        seconds_remaining_4 = seconds_remaining_3 - math.floor(self.hours * (60 * 60))

        self.minutes = math.floor(seconds_remaining_4 / (60))
        print(f" {self.minutes} minutes")

        self.seconds_remaining_5 = round(seconds_remaining_4 - self.minutes * (60))
        print(f" {self.seconds_remaining_5} seconds\n")

        if self.seconds_remaining > 0:
            time.sleep(1)
            self.seconds_remaining-=1


    def start_cd(self):
        stop_cd = False
        self.time_left()
        while not stop_cd:
            self.count_down()
            if self.seconds_remaining == 0:
                stop_cd = True
        return self.seconds_remaining


