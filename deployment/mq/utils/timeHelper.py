# -*- coding: utf-8 -*-
'''
Created on 2012-11-29

@author: JD
'''
import time

class DateTime:
    @staticmethod
    def now():
        return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    
    @staticmethod
    def addSeconds(seconds):
        now_seconds = time.time()
        new_seconds = now_seconds + seconds
        return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(new_seconds))
    
    @staticmethod
    def addMinutes(minutes):
        return DateTime.addSeconds(minutes * 60)
    
    @staticmethod
    def addHours(hours):
        return DateTime.addMinutes(hours * 60)
    
    @staticmethod
    def addDays(days):
        return DateTime.addHours(days * 24)
