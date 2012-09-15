import zeo_api 
import matplotlib.pyplot as plt #for plotting data
from datetime import *
from pandas import * #for dataframe
import json #for manipulating API responses
from credentials import * #credentials.py defines consumer_secret, consumer_key, api_key,referer, and callback_url
#-----------------------------------
#get your own consumer key and secret by emailing zeo developer relations

myzeo = zeo_api.Zeo(consumer_key,consumer_secret,api_key,referer,callback_url,verbose=1)
zqscore = myzeo.getOverallAverageZQScore()
print zqscore
print myzeo.getOverallAverageDayFeelScore()
print myzeo.getOverallAverageMorningFeelScore()
print myzeo.getOverallAverageSleepStealerScore()
print myzeo.getAllDatesWithSleepData()

#note that dateFrom and dateTo are inclusive values
print myzeo.getDatesWithSleepDataInRange(dateFrom='2012-09-13')
print myzeo.getDatesWithSleepDataInRange(dateTo='2012-09-13')
print myzeo.getDatesWithSleepDataInRange(dateFrom='2012-09-12',dateTo='2012-09-13')

#if no date is specified, the current date will be used
print myzeo.getSleepStatsForDate()
print myzeo.getSleepStatsForDate('2012-09-12')

print myzeo.getSleepRecordForDate()

print myzeo.getPreviousSleepStats()

print myzeo.getPreviousSleepRecord()

print myzeo.getNextSleepStats('2012-09-01')

print myzeo.getNextSleepRecord('2012-09-01')

