#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import os, fnmatch
import csv
import codecs
import winsound

duration = 100  # millisecond
freq = 440  # Hz
winsound.Beep(freq, duration)

path = 'source'
v_pref = '<font face="Times New Roman" color=#2F0000>'
v_suf  = '</tr>'
v_max_len = 100

res = codecs.open('Calendar_back.txt','w','utf-8')
for filename in os.listdir(path):
    if fnmatch.fnmatch(filename, '0*.msg'):
        print(filename)
        infile = codecs.open(os.path.join(path, filename), 'r', 'utf8')
        v_text = False
        v_end_str = True
        for line in infile:
            if line.find('Если, глядя утром в зеркало')>=0:
                pass
            if not v_text and line.find(v_pref)>=0:
                v_text = True
            elif v_text and len(line)>v_max_len:
                v_text = False
            elif v_text and line.find(v_suf)<0 and line[0]!='<' and len(line)>2:
                if v_end_str:   # предыдущая строка была с окончанием
                    v_end_str = (line[-6:-2] == '<br>')
                    if v_end_str:   # текущая строка с окончанием
                        res.write(line.replace(' / ','').replace('- ','— ').replace('— ','<br>— ').replace(' <br>— ',' — ').replace('<br><br>','<br>'))
                    else:
                        res.write(line.replace(' / ','').replace('- ','— ').replace('— ','<br>— ').replace(' <br>— ',' — ').replace('<br><br>','<br>')[:-2])      # убираем \n
                else:   # предыдущая строка была без окончания
                    v_end_str = (line[-6:-2] == '<br>')
                    if v_end_str:   # текущая строка с окончанием
                        res.write(line.replace(' / ','<br>').replace('- ','— ').replace('— ','<br>— ').replace(' <br>— ',' — ').replace('<br><br>','<br>'))
                    else:
                        res.write(line.replace(' / ','<br>').replace('- ','— ').replace('— ','<br>— ').replace(' <br>— ',' — ').replace('<br><br>','<br>')[:-2])
            elif v_text and line.find(v_suf)>=0:
                v_text = False
        infile.close()

res.close()



freq = 330  # Hz
winsound.Beep(freq, duration)
