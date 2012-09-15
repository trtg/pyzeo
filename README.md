#pyzeo
This library provides a lightweight python wrapper for the fitbit API with the goal of making it easier to visualize the data retrieved from the API. The methods provided by the API and their current state of support within this wrapper are indicated below:
 
##Overall Average Functions:
###getOverallAverageZQScore - Returns the average ZQ score for the user.
###getOverallAverageDayFeelScore - Returns the average score for how the user felt during the day.
###getOverallAverageMorningFeelScore - Returns the average score for how the user felt in the morning.
###getOverallAverageSleepStealerScore - Returns the average sleep stealer score for the user.

##Date Functions:
###getAllDatesWithSleepData - Returns an array of ZeoDate objects representing dates for which sleep data is available.
###getDatesWithSleepDataInRange - Returns an array of ZeoDate objects for which sleep data is available inclusive in dates.
###getSleepStatsForDate - Returns the SleepStats for the specified date.
###getSleepRecordForDate - Returns the SleepRecord for the specified date.

##Paging Functions:
##getPreviousSleepStats - Returns the SleepStats (grouped by day) for the latest date prior to the specified date.
##getPreviousSleepRecord - Returns the SleepRecord for the latest date prior to the specified date.
##getNextSleepStats - Returns the SleepStats (grouped by day) for the earliest date after the specified date.
##getNextSleepRecord -	Returns the SleepStats for the earliest date after the specified date.
##getEarliestSleepStats - Returns the SleepStats (grouped by day) with the earliest date on record for the current user.
##getEarliestSleepRecord - Returns the SleepRecord with the earliest date on record for the current user.
##getLatestSleepStats - Returns the SleepStats (grouped by day) with the latest date on record for the current user.
##getLatestSleepRecord -	Returns the SleepRecord with the latest date on record for the current user.

##Miscellaneous Functions:
###logout - Logs the user out of the API and closes the session.
