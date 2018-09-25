import re

for x in range(1, 9):
    file_name = "Hi_Low_Temps\Weather10Day"+str(x)+".html"
    whole_thing = open(file_name).read()

    hi_temp_re = re.compile('"wx-temp"> (.*)<sup>')
    hi_temps = re.findall(hi_temp_re, whole_thing)

    low_temp_re = re.compile('"wx-temp-alt"> (.*)<sup>')
    low_temps = re.findall(low_temp_re, whole_thing)

    date_re = re.compile('"wx-label">(.* .*)</span>')
    dates = re.findall(date_re, whole_thing)

    # print dates
    # print hi_temps
    # print low_temps

    for dates, hi, low in zip(dates, hi_temps, low_temps):
        print dates, hi, low
    print "\n"
