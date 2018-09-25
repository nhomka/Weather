import urllib2
import datetime

now = datetime.datetime.now()

my_url = urllib2.urlopen("http://www.weather.com/weather/tenday/Buffalo+NY+USNY0181:1:US").read()

my_file = open('Weather10Day_'+str(now)[:-7].replace(' ', '_').replace(':', '-')+'.txt', 'w')

for line in my_url:
    my_file.write(line)
