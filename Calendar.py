#!/usr/bin/python3
# -*- coding: utf-8 -*-

# программа формирования HTML-файла для печати календаря
# исходные файлы (шаблоны
version = '1.1'
import sys
from color_output import print
print('Python version #15 '+sys.version.split(' ')[0])
v_debug = True  # поставить False при окончательной печати для резки
v_pages = 365//4+1  #  28//4 #
#from ctypes import *
import datetime
import configparser
import csv
import codecs

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

# очистка от кавычек
def del_q(s):
    "Deletes quoters."
    if (s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'"):
        return s[1:-1]
    return s

# проверка дня недели на соответствие
def true_day(dat, tip):
    if tip == '0' and dat.strftime("%m") != (dat + datetime.timedelta(days=7)).strftime("%m"):
        return True
    elif dat.strftime("%m") != (dat - datetime.timedelta(days=int(tip)*7)).strftime("%m") and dat.strftime("%m") == (dat - datetime.timedelta(days=(int(tip)-1)*7)).strftime("%m"):
        return True
    return False

# вычисление длительности дня по кортежу из строк восхода и захода
def dlit(l):
    return str(((int(l[1].split(':')[0])*60+int(l[1].split(':')[1])) - (int(l[0].split(':')[0])*60+int(l[0].split(':')[1])))//60) + ':' +  (str(((int(l[1].split(':')[0])*60+int(l[1].split(':')[1])) - (int(l[0].split(':')[0])*60+int(l[0].split(':')[1]))) % 60)).zfill(2)

# вычисление фазы луны по дате
def luna(dat):
    return str(round((((int(str(dat - datetime.date(2016, 10, 1)).split(' ')[0])+1.7) % 29.53059 ) - ( 29.53059 / 16)) / ( 29.53059 / 8) ))

# слово после числа лет
def gram_case(n):
    if 10 < (abs(n) % 100 ) < 20:
        return list_let[0]
    return list_let[abs(n) % 10]

# кол-во строк под фрагмент текста
def kol_br(txt):
    v = 0
    for c in txt.split('<br>'):
        v += 1 + len(c) // 43
    return v

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
            print("#12 exception on %s!" % option)
            dict1[option] = None
    return dict1

# ищем среди праздников соответствующий этому дню
def form_holiday_text():
    for row in Calendar_text[fname]:
        # ищем праздник по дню недели
        if len(row)>3 and (row[0] == '8' or row[0] == '9') and (int(row[2]) == 0 or int(row[2]) == var_mesnom) and int(row[1]) == v_dat.weekday()+1 and true_day(v_dat, row[3]):
            attrib_start = del_q(ConfigSectionMap(row[0])["attrib_start"])
            attrib_end = del_q(ConfigSectionMap(row[0])["attrib_end"])
            f_result.write(attrib_start + del_q(row[4])+attrib_end+'\n')
            v_dat_count[v_dat][v_part] += 1
        if len(row)>1 and row[0] == 'easter' and v_dat == v_dat_easter + datetime.timedelta(days=int(row[1])):
            attrib_start = del_q(ConfigSectionMap(row[0])["attrib_start"])
            attrib_end = del_q(ConfigSectionMap(row[0])["attrib_end"])
            f_result.write(attrib_start + del_q(row[2])+attrib_end+'\n')
            v_dat_count[v_dat][v_part] += 1
        # тот ли месяц (совпадает или равен 0)
        if len(row)>3 and '0' <= row[0] < '8' and (row[2] == '0' or int(row[2]) == var_mesnom):
            # тот ли день
            if v_dat == datetime.date(v_god, 11, 23) and v_part == 1:
                attrib_start = del_q(ConfigSectionMap('1')["attrib_start"])
                attrib_end = del_q(ConfigSectionMap('1')["attrib_end"])
                f_result.write(attrib_start + '<img src="img\\tort.jpg" width=90 hight=70></img><font size=+3>' + 'Мне ' + str(v_god - 1960) + '</font>' + attrib_end + '\n')
                v_dat_count[v_dat][v_part] += 1
                break
            elif v_dat == datetime.date(v_god, 9, 23) and v_part == 1:
                attrib_start = del_q(ConfigSectionMap('1')["attrib_start"])
                attrib_end = del_q(ConfigSectionMap('1')["attrib_end"])
                f_result.write('<img src="img\\tost.jpg" width=170 hight=70></img>\n')
                v_dat_count[v_dat][v_part] += 1
                break
            elif row[3] == var_dat:
                # вывод строки праздника с нужными атрибутами
                attrib_start = del_q(ConfigSectionMap(row[0])["attrib_start"])
                attrib_end = del_q(ConfigSectionMap(row[0])["attrib_end"])
                # указан ли год
                if row[1] == '0':
                    f_result.write(attrib_start + del_q(row[4])+attrib_end+'\n')
                else:
                    if row[0] == '3':
                        f_result.write(attrib_start + row[1] + ' ' + del_q(row[4]) + ' (' + (str(int(v_dat.strftime("%Y")) - int(row[1])) if int(v_dat.strftime("%Y")) >= int(row[1]) else ("через " + str(int(row[1])-int(v_dat.strftime("%Y"))))) + ' ' + gram_case(int(v_dat.strftime("%Y")) - int(row[1])) + ')' + attrib_end + '\n')
                    elif row[0] == '4':
                        f_result.write(attrib_start + '<i>' + row[1] + '</i> ' + del_q(row[4]) + attrib_end + '\n')
                    else:
                        f_result.write(attrib_start + '<i>' + row[1] + '</i> ' + del_q(row[4]) + ('&nbsp;(' + list_day0[(datetime.date(int(row[1]), int(row[2]), int(row[3]))).weekday()] + ')' if isint(row[1]) else '') + attrib_end + '\n')
                v_dat_count[v_dat][v_part] += 1
    return

# формирование обратной стороны листка при печати "вверх ногами" обратной стороны
def form_back_side_new():
    for n in range(v_pages):
        if v_debug:
            back_page(v_pages*4-1-n*4)
            back_page(v_pages*4-0-n*4)
            back_page(v_pages*4-3-n*4)
            back_page(v_pages*4-2-n*4)
        else:
            back_page(Calendar_back[4*n % 4])
            back_page(Calendar_back[(4*n+1) % 4])
            Calendar_back[4*n % 4] -= 1
            Calendar_back[(4*n+1) % 4] -= 1
            back_page(Calendar_back[(4*n+2) % 4])
            back_page(Calendar_back[(4*n+3) % 4])
            Calendar_back[(4*n+2) % 4] -= 1
            Calendar_back[(4*n+3) % 4] -= 1
    return

# вывод текста обратной стороны для n-го дня года
def back_page(n):
    dat = datetime.date(v_god, 1, 1) + datetime.timedelta(days=n-1)
#    print(n, str(dat))

    # ищем обратную сторону для этой даты в Calendar_back.csv
    # если не находим, то берем строки после v_pos_in_back из файла Calendar_back.txt

# проверка на целое число в строке
def isint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

if len(sys.argv)>1 and sys.argv[1].isdigit() and (1900<int(sys.argv[1])<3000):
    v_god = int(sys.argv[1])
else:
    v_god = (datetime.date.today()+datetime.timedelta(days=30)).year    # в декабре уже по умолчанию берем следующий год
v_dat_easter = calc_easter(v_god)
v_counter_per_page = 0
list_mes = ('Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень', 'Липень', 'Серпень', 'Вересень', 'Жовтень', 'Листопад', 'Грудень')
list_day = ('понеділок', 'вівторок', 'середа', 'четвер', 'п\'ятниця', 'субота', 'неділя')
list_day0 = ('пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'нд')
list_let = ('років', 'рік', 'роки', 'роки', 'роки', 'років', 'років', 'років', 'років', 'років')
#print('Формирование HTML-файла для печати календаря ' + str(v_god) + ' года.')
f_html = codecs.open('Calendar.html', 'r','utf-8')
f_result = codecs.open('Calendar_'+str(v_god)+'.html', 'w','utf-8')
f_log = codecs.open('Calendar.log', 'w','utf-8')
f_log.write( str(datetime.datetime.today()).split('.')[0] + '\n' )
f_log.write( 'Формирование календаря на ' + str(v_god) + ' год.\n' )
for line in f_html:
    line = line.replace('##var_god',str(v_god))
    line = line.replace('##title','')
    line = line.replace('##bcolor','black')
    if line[0:6] == '##loop':
        print('File #15 Calendar_'+str(v_god)+'.html #7 started.')
        break
    f_result.write(line)
var_loop = []
for line in f_html:
    if line[0:9] == '##endloop':
        print('File #15 Calendar_'+str(v_god)+'.html #7 looped.')
        break
    if line[0:9] == '##include':
        f_page = codecs.open(line[10:-2], 'r', 'utf-8')
        v_counter_per_page += 1
        for pline in f_page:
            var_loop.append(pline)
        f_page.close()
    else:
        var_loop.append(line)

# считываем в словарь настройки
Config = configparser.ConfigParser()
Config.read('Calendar_page.config',encoding='utf-8')

# считываем восходы-заходы солнца
# 9,14,06:16,18:57 (всё по летнему времени)
ft = codecs.open('Calendar_sun.csv', 'r','utf-8')
with ft as csvfile:
    csv_reader = csv.reader(csvfile, quotechar='\"')
    Calendar_sun = {(row[0],row[1]):[row[2],row[3]] for row in csv_reader}

# меняем час для зимнего времени
d = 7-(datetime.date(v_god, 10, 1)).weekday()
d1 = d+28 if (d<4) else d+21   # день перехода в октябре
d = 7-(datetime.date(v_god,  3, 1)).weekday()
d2 = d+28 if (d<4) else d+21   # день возрата в марте

for d in Calendar_sun:
    if int(d[0])==10 and int(d[1])>=d1 or int(d[0])>10 or int(d[0])<3 or int(d[0])==3 and int(d[1])<d2:
        Calendar_sun[(d[0],d[1])][0] = str(int(Calendar_sun[(d[0],d[1])][0][:2])-1)+Calendar_sun[(d[0],d[1])][0][2:]
        Calendar_sun[(d[0],d[1])][1] = str(int(Calendar_sun[(d[0],d[1])][1][:2])-1)+Calendar_sun[(d[0],d[1])][1][2:]
    else:
        Calendar_sun[(d[0],d[1])][0] = str(int(Calendar_sun[(d[0],d[1])][0][:2]))+Calendar_sun[(d[0],d[1])][0][2:]
        Calendar_sun[(d[0],d[1])][1] = str(int(Calendar_sun[(d[0],d[1])][1][:2]))+Calendar_sun[(d[0],d[1])][1][2:]

v_dat = datetime.date(v_god, 1, 1) - datetime.timedelta(days=1)
Calendar_text = {}
Calendar_back = {0:v_pages*3,1:v_pages*4,2:v_pages*1,3:v_pages*2}   # счетчики дней для обратной стороны
Calendar_red = [v_dat_easter, v_dat_easter + datetime.timedelta(days=49)]
v_part = 0
v_dat_count = {}
v_c = 0

for v_paper in range(v_pages):  #при окончательной печати для резки
    v_page = 0
    for line in var_loop:
        var_day = list_day[v_dat.weekday()]
        var_dat = str(int(v_dat.strftime("%d")))
        var_mes = list_mes[int(v_dat.strftime("%m"))-1]
        var_mesnom = int(v_dat.strftime("%m"))
        var_god = str(int(v_dat.strftime("%Y")))
        if (v_dat.weekday() == 5 and v_dat not in Calendar_red) or (v_dat.weekday() == 0 and ((v_dat - datetime.timedelta(days=1)) in Calendar_red or (v_dat - datetime.timedelta(days=2)) in Calendar_red)):
            line = line.replace('##var_col','Violet')
        elif v_dat.weekday() == 6 or v_dat in Calendar_red:
            line = line.replace('##var_col','red')
        else:
            line = line.replace('##var_col','black')
        if line.find('##id')>=0:
            line = line.replace('##id',str(v_dat))
        if line.find('##file')>=0:
            line = line.replace('##file',str(v_paper)+'-'+str(v_page)+' '+str(v_dat))+'<br>.......................................................................<br>'
            v_page +=1

        line = line.replace('##var_day',var_day)
        line = line.replace('##var_mes',var_mes)
        line = line.replace('##var_god',var_god)
        if var_dat == '8' and var_mesnom == 3:
            line = line.replace('##var_dat','<img src="img\8marta.jpg" width=60></img>')
        else:
            line = line.replace('##var_dat',var_dat)
       #['12', '24', '9:31', '17:50']
        line = line.replace('##var_sun1',Calendar_sun[(str(int(v_dat.strftime("%m"))),var_dat)][0])
        line = line.replace('##var_sun2',Calendar_sun[(str(int(v_dat.strftime("%m"))),var_dat)][1])
        line = line.replace('##var_sun3',dlit(Calendar_sun[(str(int(v_dat.strftime("%m"))),var_dat)]))
        line = line.replace('##var_luna',luna(v_dat))

        # нужны ли подстановки из файла праздников в этом месте?
        if line.find('.csv')>=0:
            # файл с праздниками должен называться Calendar??????.csv и быть в кодировке UTF-8
            fname = line[(line.find('##Calendar')+2):(line.find('.csv')+4)]
            # проверим, считаны ли уже строки этого файла
            if fname not in Calendar_text:
                ft = codecs.open(fname, 'r','utf-8')
            # считываем строки календаря событий
                with ft as csvfile:
                    csv_reader = csv.reader(csvfile, quotechar='\"')
                    Calendar_text[fname] = [row for row in csv_reader]
                    Calendar_red += [ datetime.date(v_god, int(row[2]), int(row[3])) for row in Calendar_text[fname] if len(row)>3 and row[0] == '1' ]
                ft.close()
                Calendar_red += [ datetime.date(v_god+1, 1, 1) ]
            if line.find('##'+fname) == 0:
                line = ''
            else:
                line = line.replace('##'+fname,'')
                if line.find('##easter')>=0:
                    v_part = 0
                    v_dat_count[v_dat] = [0,0]
#                    v_c += 1
#                    print(v_c, v_paper, v_page, str(v_dat))
                    line = line.replace('##easter','')

                if line.find('##prof')>=0:
                    v_part = 1
                    line = line.replace('##prof','')

                # определяем, не тот ли это день недели для профессионального праздника
                if v_part == 1 and v_dat == datetime.date(v_god, 1, 1) + datetime.timedelta(days=255):
                    attrib_start = del_q(ConfigSectionMap('1')["attrib_start"])
                    attrib_end = del_q(ConfigSectionMap('1')["attrib_end"])
                    f_result.write(attrib_start + "День компьютерщика"+attrib_end+'\n')
                    v_dat_count[v_dat][v_part] += 1

                form_holiday_text()

        if line.find('##endpage')>=0:
            line = line.replace('##endpage','')
            v_dat += datetime.timedelta(days=v_pages if not v_debug else 1)
#            print(v_dat)
        f_result.write(line)
    v_dat -= datetime.timedelta(days=(v_pages*4-1) if not v_debug else 0)

for line in f_html:
    f_result.write(line)

f_html.close()
f_result.close()

f_log.write( 'Обработаны входные файлы событий:\n' )
for c in Calendar_text.keys():
    f_log.write( str(c) + '\n' )
f_log.write( '\nОбнаружены выходные дни:\n' )
for c in sorted(Calendar_red):
    f_log.write( str(c) + '\n' )
f_log.write( '\nКоличество событий по датам:' )
for c in sorted(v_dat_count):
    if int(c.strftime("%d")) == 1:
        f_log.write( '\n' + list_mes[int(c.strftime("%m"))-1] )
    if int(c.strftime("%d")) % 7 == 1:
        f_log.write( '\n' )
    f_log.write( str(c) + '-' + str(v_dat_count[c][0]) + '+' + str(v_dat_count[c][1]) + '  ' )
print('File #15 Calendar_'+str(v_god)+'.html #7 created.')

f_log.write( '\nСоздание календаря закончено ' + str(datetime.datetime.today()).split('.')[0] + '\n' )

#####################################################################################
# формирование обратной стороны
Calendar_back = {0:v_pages*3,1:v_pages*4,2:v_pages*1,3:v_pages*2}   # счетчики дней для обратной стороны
Calendar_text = {}

for n in range(v_pages*2):
    if v_debug:
        back_page(v_pages*4-1-n*2)
        back_page(v_pages*4-n*2)
    else:
        back_page(Calendar_back[2*n % 4])
        back_page(Calendar_back[(2*n+1) % 4])
        Calendar_back[2*n % 4] -= 1
        Calendar_back[(2*n+1) % 4] -= 1

f_html = codecs.open('Calendar.html', 'r','utf-8')
f_result = codecs.open('Calendar_'+str(v_god)+'_back.html', 'w','utf-8')
f_page = codecs.open('Calendar_back.txt', 'r', 'utf-8')
for line in f_html:
    line = line.replace('##var_god',str(v_god))
    line = line.replace('##title','(обратная сторона)')
    line = line.replace('##bcolor','white')
    if line[0:6] == '##loop':
        print('File #15 Calendar_'+str(v_god)+'_back.html #7 started.')
        break
    f_result.write(line)
var_loop = []
for line in f_html:
    if line[0:9] == '##endloop':
        print('File #15 Calendar_'+str(v_god)+'_back.html #7 looped.')
        break
    if line[0:9] == '##include':
        f_page = codecs.open('Calendar_back.page', 'r', 'utf-8')
        for pline in f_page:
            var_loop.append(pline)
        f_page.close()
    else:
        var_loop.append(line)

f_txt = codecs.open('Calendar_back.txt', 'r', 'utf-8')
var_txt = []
for line in f_txt:
    var_txt.append(line)
f_txt.close()

f_stih1 = codecs.open('Calendar_back_stih-1.txt', 'r', 'utf-8')
var_stih1 = []
for line in f_stih1:
    var_stih1.append(line)
f_stih1.close()

f_stih2 = codecs.open('Calendar_back_stih-2.txt', 'r', 'utf-8')
var_stih2 = []
for line in f_stih2:
    var_stih2.append(line)
f_stih2.close()

v_dat = datetime.date(v_god, 1, 1)
v_part = 0
v_c = 0
v_high = 390
v_kol = v_high // 15
pos_stih1 = 0
pos_stih2 = 0
pos_txt = 0

for v_paper in range(v_pages):  #при окончательной печати для резки
    v_page = 0
    for line in var_loop:
        var_day = list_day[v_dat.weekday()]
        var_dat = str(int(v_dat.strftime("%d")))
        var_mes = list_mes[int(v_dat.strftime("%m"))-1]
        var_mesnom = int(v_dat.strftime("%m"))
        var_god = str(int(v_dat.strftime("%Y")))

        if line.find('##id')>=0:
            line = line.replace('##id',str(v_dat))

        if line.find('##file')>=0:
            line = '<font color=white>....................................................................</font><br>'+line.replace('##file',str(v_paper)+'-'+str(v_page)+' '+str(v_dat))
            v_page +=1
            v_part = 0
            v_dat_count[v_dat] = [0,0]

        if line.find('##high')>=0:
            line = line.replace('##high',str(v_high))
            v_page +=1
            v_part = 0
            v_dat_count[v_dat] = [0,0]

        # нужны ли подстановки из файла праздников в этом месте?
        if line.find('.csv')>=0:
            # файл с праздниками должен называться Calendar??????.csv и быть в кодировке UTF-8
            fname = line[(line.find('##Calendar')+2):(line.find('.csv')+4)]
            # проверим, считаны ли уже строки этого файла
            if fname not in Calendar_text:
                ft = codecs.open(fname, 'r','utf-8')
            # считываем строки календаря событий
                with ft as csvfile:
                    csv_reader = csv.reader(csvfile, quotechar='\"')
                    Calendar_text[fname] = [row for row in csv_reader]
                ft.close()
            if line.find('##'+fname) == 0:
                line = ''
            else:
                line = line.replace('##'+fname,'')

                # ищем среди праздников соответствующий этому дню
                form_holiday_text()

                # дополнение обратной стороны листка текстом из Calendar_back_stih-1.txt
                attrib_start = "<font color=black><b>"
                attrib_end   = "</b></font><br>"
                while len(var_stih1[pos_stih1])>3:
                    f_result.write(attrib_start + var_stih1[pos_stih1] + attrib_end+'\n')
                    v_dat_count[v_dat][0] += kol_br(var_stih1[pos_stih1])
                    pos_stih1 = (pos_stih1+1) % len(var_stih1)
                pos_stih1 = (pos_stih1+1) % len(var_stih1)
                f_result.write('<p ALIGN=CENTER>')
                v_dat_count[v_dat][0] += 1
                # дополнение обратной стороны листка текстом из Calendar_back_stih-2.txt
                attrib_start = "<font color=blue>"
                attrib_end   = "</font><br>"
                while len(var_stih2[pos_stih2])>3:
                    f_result.write(attrib_start + var_stih2[pos_stih2] + attrib_end+'\n')
                    v_dat_count[v_dat][0] += kol_br(var_stih2[pos_stih2])
                    pos_stih2 = (pos_stih2+1) % len(var_stih2)
                pos_stih2 = (pos_stih2+1) % len(var_stih2)
                f_result.write('<p>')
                v_dat_count[v_dat][0] += 1
                # дополнение обратной стороны листка текстом из Calendar_back.txt
                attrib_start = "<font color=black>"
                attrib_end   = "</font><p>"
                while v_dat_count[v_dat][0] + kol_br(var_txt[pos_txt]) <= v_kol:
                    f_result.write(attrib_start + var_txt[pos_txt] + attrib_end+'\n')
                    v_dat_count[v_dat][0] += kol_br(var_txt[pos_txt]) + 1
                    pos_txt = (pos_txt+1) % len(var_txt)
                    while kol_br(var_txt[pos_txt]) > v_kol/2:
                        pos_txt = (pos_txt+1) % len(var_txt)

                v_dat += datetime.timedelta(days=v_pages if not v_debug else 1)

        if line.find('##endpage')>=0:
            line = line.replace('##endpage','')
#            print(v_dat)
        f_result.write(line)
    v_dat -= datetime.timedelta(days=(v_pages*4-1) if not v_debug else 0)

for line in f_html:
    f_result.write(line)
f_html.close()
f_result.close()


print('File #15 Calendar_'+str(v_god)+'_back.html #7 created.')

f_log.close()
