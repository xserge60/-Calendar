#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import datetime
import time
import calendar
import csv
import configparser
import sys
import codecs
import logging
import winsound
duration = 100  # millisecond
freq = 440  # Hz
winsound.Beep(freq, duration) 

#print (help(logging.basicConfig))
logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'Calendar.log')
#logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.DEBUG)
# расчет даты пасхи
def calc_easter(year):
    "Returns Easter as a date object."
    f = ((19 * (year % 19) + 15) % 30) + ((2 * (year % 4) + 4 * (year % 7) + 6 * ((19 * (year % 19) + 15) % 30) + 6) % 7)
    if f < 10:
        month = 3
        day = f + 22
    else:
        month = 4
        day = f - 9
    return datetime.date(year, month, day) + datetime.timedelta(days=13)

# чтение настроек из секции конфига
def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1
    
def dlit(l):
    return str(((int(l[1].split(':')[0])*60+int(l[1].split(':')[1])) - (int(l[0].split(':')[0])*60+int(l[0].split(':')[1])))//60) + ':' +  str(((int(l[1].split(':')[0])*60+int(l[1].split(':')[1])) - (int(l[0].split(':')[0])*60+int(l[0].split(':')[1]))) % 60)

# вычисление фазы луны по дате
def luna(dat):
    # Продолжительность синодического месяца в среднем составляет 29,53059 суток. 
    # 2.01.2018 5:25 - полнолуние
    # 1.10.2016 2:12 - новолуние
    d = round((int(str(dat - datetime.date(2016, 10, 1)).split(' ')[0]) % 29.53059 - ( 29.53059 / 16)) / ( 29.53059 / 8) )
    return d
    
print(sys.version)
v_god = 2017
v_mes = ('Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень', 'Липень', 'Серпень', 'Вересень', 'Жовтень', 'Листопад', 'Грудень')
v_day = ('понеділок', 'вівторок', 'середа', 'четвер', 'п\'ятниця', 'субота', 'неділя')
v_text = 'This is a text'
v_dat = datetime.date(v_god, 1, 1)
v_dat = datetime.date.today()
dict1 = {v_dat:22, v_dat + datetime.timedelta(days=1):12}
dict1[v_dat] += 100
print(dict1)

print(dlit(('11:36','15:06')))
print(str(luna(datetime.date(2018, 1, 2))))

for i in range(28):
    d = i+1
    n = (27-d)+(((d-1)&2)<<1)
    print(d,n,(((d-1)&2)<<1))

sys.exit()

print(int(v_dat.strftime("%m")),int(v_dat.strftime("%d")),v_dat.weekday())
print(calc_easter(v_god))

Config = configparser.ConfigParser()
Config.read('Calendar_page.config')
print(Config.sections())

attrib_start = ConfigSectionMap("1")["attrib_start"]
attrib_end = ConfigSectionMap("1")["attrib_end"]
print ("Атрибут начала %s. Атрибут конца %s" % (attrib_start, attrib_end))

res = codecs.open('test.txt','w','utf-8')
infile = codecs.open('Calendar_page_bottom.csv', 'r', 'utf8')


with infile as csvfile:

#with codecs.open('Calendar_page_bottom.csv', 'r', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile, quotechar='\"')
    langs = next(csv_reader)[1:]
    res.write(str(langs)+'\n')
    for row in csv_reader:
        res.write(str(row)+'\n')
#for row in reader:
#    print(row)
#    res.write(str(row)+'\n')

res.write("English text"+'\n')
res.write("Русский текст"+'\n')
res.write("Український текст"+'\n')
res.close()


# Сообщение отладочное
logging.debug( "Отладочное сообщение".encode('utf-8').decode('utf-8') )
# Сообщение информационное
logging.info( "Информационное  сообщение" )
# Сообщение предупреждение
logging.warning( "Предупреждение" )
# Сообщение ошибки
logging.error( "Сообщение об ошибе" )
# Сообщение критическое
logging.critical( "Чи є щось гірше?" )

freq = 330  # Hz
winsound.Beep(freq, duration)
