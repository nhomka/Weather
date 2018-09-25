from numpy import *
import re
import urllib2

s = open('weatherpages.txt','r')

file_name = 'weatherpages.txt'
whole_thing = open(file_name).read()


file_strip_re = re.compile('href="(.*)">2014')
file_names = re.findall(file_strip_re, whole_thing)
# print file_names

count = 0

for a in file_names:
    if 'weather_tenday_Buffalo_NY_14222' in a:
        link = 'http://blue.math.buffalo.edu/463/weatherpages/'+a
        count += 1
        print link
        myurl = urllib2.urlopen(link).read()
        myfile = open('BuffaloWeather10day_'+str(count)+'.txt', 'w')
        for line in myurl:
            myfile.write(line)

count = 0

for a in file_names:
    if 'weather_yesterday_Buffalo_NY_14222' in a:
        link = 'http://blue.math.buffalo.edu/463/weatherpages/'+a
        count += 1
        print link
        myurl = urllib2.urlopen(link).read()
        myfile = open('BuffaloWeatherYesterday_'+str(count)+'.txt', 'w')
        for line in myurl:
            myfile.write(line)

print count



