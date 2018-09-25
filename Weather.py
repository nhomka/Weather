import re
import pylab as pl
from numpy import *

'''Essentially this extracts the high and low temperatures from weather pages in the Buffalo area
over the course of about 2 months, and then finds out statistics from the information, such as the 
average error from day to day, the average error in the forecast 1 day in the future vs 10 days in 
the future, and so on.  The subplots (the red bar is the actual temperature for each day, and the 
blue line is the temperature in the days prior to when the actual measurement was taken, going back 
up to 10 days) and outputs from the script are provided, as it was implausible to try and make a 
dummy document given how it had been coded.'''

num_files = 137
num_rows = 10
num_cols = 13

weather_dict_hi = {}
weather_dict_low = {}
weather_dict_hi_avg = {}
weather_dict_low_avg = {}
weather_dict_hi_yest = {}
weather_dict_low_yest = {}

for a in range(1, num_files):
    filename = "Text_Files\BuffaloWeather10Day_"+str(a)+".txt"
    whole_thing = open(filename).read()

    hi_temp_re = re.compile('"wx-temp"> (.*)<sup>')
    hi_temps = re.findall(hi_temp_re, whole_thing)

    low_temp_re = re.compile('"wx-temp-alt"> (.*)<sup>')
    low_temps = re.findall(low_temp_re, whole_thing)

    date_re = re.compile('"wx-label">(... .*)</span>')
    dates = re.findall(date_re, whole_thing)

    # print dates
    # print hi_temps
    # print low_temps

    for dates, hi, low in zip(dates, hi_temps, low_temps):
        if dates not in weather_dict_hi:
            weather_dict_hi[dates] = [int(hi)]
        if dates in weather_dict_hi:
            weather_dict_hi[dates] += [int(hi)]
        if dates not in weather_dict_low:
            weather_dict_low[dates] = [int(low)]
        if dates in weather_dict_low:
            weather_dict_low[dates] += [int(low)]

for key in weather_dict_hi.iterkeys():
    weather_dict_hi_avg[key] = mean(weather_dict_hi[key])
for key in weather_dict_low.iterkeys():
    weather_dict_low_avg[key] = mean(weather_dict_low[key])

for b in range(1, num_files):
    filename = "Text_Files\BuffaloWeatherYesterday_"+str(b)+".txt"
    whole_thing = open(filename).read()

    hi_temp_re = re.compile('"wx-temp">\n(.*)<sup>')
    hi_temps = re.findall(hi_temp_re, whole_thing)

    low_temp_re = re.compile('wx-temp-low">\n(.*)<sup>')
    low_temps = re.findall(low_temp_re, whole_thing)

    date_re = re.compile('<div class="wx-12hr-titlewrap">\n<h3>\n(... .*)\n</h3>\n<div class="wx-label wx-day-label">')
    dates = re.findall(date_re, whole_thing)

# print dates
# print hi_temps
# print low_temps, '\n'

    for dates, hi, low in zip(dates, hi_temps, low_temps):
        if dates not in weather_dict_hi_yest:
            weather_dict_hi_yest[dates] = [int(hi)]
        if dates not in weather_dict_low_yest:
            weather_dict_low_yest[dates] = [int(low)]

# print weather_dict_hi_yest
# print weather_dict_low_yest

count = 0
sum_his = 0
sum_his_abs = 0
for dates in weather_dict_hi_yest:
    if dates != 'Feb 10':
        count += 1
        sum_his_abs = sum_his_abs + abs(float(weather_dict_hi_yest[dates] - weather_dict_hi_avg[dates]))
        sum_his = sum_his + (float(weather_dict_hi_yest[dates] - weather_dict_hi_avg[dates]))

print 'average error in high temp = ', sum_his_abs / count
print 'average difference between predicted and actual high temp = ', sum_his / count, '\n'

count = 0
sum_lows = 0
sum_lows_abs = 0
for dates in weather_dict_low_yest:
    if dates != 'Feb 10':
        count += 1
        sum_lows_abs = sum_lows_abs + abs(float(weather_dict_low_yest[dates] - weather_dict_low_avg[dates]))
        sum_lows = sum_lows + (float(weather_dict_low_yest[dates] - weather_dict_low_avg[dates]))

print "Average error in low temp = ", sum_lows_abs / count
print "Average difference between predicted and actual low temp = ", sum_lows / count


measurements = 20
for x in range(1, (measurements+1)):
    sum_x = 0
    count = 0
    for dates in weather_dict_hi_yest:
        if dates != 'Feb 10':
            if len(weather_dict_hi[dates]) >= measurements:
                count += 1
                sum_x = sum_x + abs(float(weather_dict_hi[dates][-x] - weather_dict_hi_yest[dates][0]))
    print "Average error in high temp ", x, " measurement(s) before actual day is ", sum_x / count, " degrees"
print "Number of days used for this sample = ", count

for x in range(1, (measurements+1)):
    sum_x = 0
    count = 0
    for dates in weather_dict_low_yest:
        if dates != 'Feb 10':
            if len(weather_dict_low[dates]) >= measurements:
                count += 1
                sum_x = sum_x + abs(float(weather_dict_low[dates][-x] - weather_dict_low_yest[dates][0]))
                # print 'predicted ', x, ' days before', weather_dict_low[dates][-x]
                # print 'actual ', weather_dict_low_yest[dates][0]
    print "Average error in low temp ", x, " measurement(s) before actual day is ", sum_x / count, " degrees"
print "Number of days used for this sample = ", count

# print weather_dict_hi
# print weather_dict_low

num_plots = 49
num_cols = 1
num_rows = int(math.ceil(math.sqrt(num_plots)))
while num_cols*num_rows < num_plots:
    num_cols += 1
x = 1
for dates in weather_dict_hi_yest:
    if dates != 'Feb 10':
        if len(weather_dict_hi[dates]) >= measurements:
            pl.subplot(num_rows, num_cols, x)
            x += 1
            pl.plot(linspace(0., 20., len(weather_dict_hi[dates])), weather_dict_hi[dates], alpha=1)
            pl.xticks([])   # pl.tick_params(axis='x', bottom = 'off', labelsize = 7)
            pl.tick_params(axis='y', left='on', labelsize=7)
            pl.axhline(y=weather_dict_hi_yest[dates], xmin=0, xmax=20, c='r', linewidth=.5)
            pl.title(dates, fontsize=7)
pl.show()

num_plots = 49
num_cols = 1
num_rows = int(math.ceil(math.sqrt(num_plots)))
while num_cols*num_rows < num_plots:
    num_cols += 1
x = 1
for dates in weather_dict_hi_yest:
    if dates != 'Feb 10':
        if len(weather_dict_low[dates]) >= measurements:
            pl.subplot(num_rows, num_cols, x)
            x += 1
            pl.plot(linspace(0., 20., len(weather_dict_low[dates])), weather_dict_low[dates], alpha=1)
            pl.xticks([])   # pl.tick_params(axis='x', bottom = 'off', labelsize = 7)
            pl.tick_params(axis='y', left='on', labelsize=7)
            pl.axhline(y=weather_dict_low_yest[dates], xmin=0, xmax=20, c='r', linewidth=.5)
            pl.title(dates, fontsize=7)
pl.show()
