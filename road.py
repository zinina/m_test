#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import datetime
import os
import sys
import traceback

PATH = '643:1:1:'

road51 = [[51,0,True,False,False],
          [53,2500,True,False,False],
          [2,2501,False,True,False],
          [1,2550,True,False,False],
          [4,4750,False,True,False],
          [5,4751,False,False,True],
          [8,4752,True,False,False],
          [55,8650,False,True,False],
          [9,8651,True,False,False],
          [61,17450,False,True,False],
          [63,17451,True,False,False],
          [65,19650,True,False,False],
          [11,22550,False,True,False],
          [67,22551,True,False,False],
          [17,31050,False,True,True],
          [77,39551,True,False,False],
          [78,39552,True,False,False],
          [19,53750,False,True,False]]

def parse_arguments():
    parser = argparse.ArgumentParser(description='tag date road')
    parser.add_argument("--tag", type=str, default = '01')
    parser.add_argument("--date", type=str, default = datetime.datetime.now().strftime('%d.%m.%Y %X'))
    parser.add_argument("--road", type=int, required = True, choices = [51,52])
    return parser.parse_args()

def check_arguments(settings):
    if len(settings.tag) > 6:
        raise Exception("Нетестовый TAG")
    if settings.road not in [51,52]:
        raise Exception("Неверное направление дороги")
    if settings.date == 'now':
        settings.date = datetime.datetime.now()
    else:    
        try:
            settings.date = datetime.datetime.strptime(settings.date, '%d.%m.%Y %X')
        except:
            raise Exception("Неверный формат даты")
        if abs(settings.date.year - datetime.datetime.now().year) > 1:
            raise Exception('Слишком отдаленный период времени')
    

def make_routs(settings):
    allrouts = []
    if settings.road == 51:
        road = road51
    else:
        road = road52
    for i in road:
        if not i[2]:
            continue
        route = [i]
        for l in road:
            if l[1] < i[1] or l[2]:
                continue
            if l[4]:
                route.append(l)
            if l[3]:
                #print(route + ([l] if not l[4] else []))
                allrouts.append(route + ([l] if not l[4] else []))
    return allrouts            
    
    
    
def make_csv(allrouts,settings):
    file = open('/home/zinina/routs/test.csv', 'w') #открываю файл на запись
    
    for i in allrouts:
        for l in i:
            print(l)
            plaza = PATH + str(l[0]) #формирую точку вьезда вида 643:1:1:узел
            p_time = round((l[1]/50000)*60) #рассчет времени до этой точки в минутах
            pt = 0
            pt = pt + p_time
            p_date = settings.date + datetime.timedelta(minutes=p_time) #прибавление полученного интервала к указанной дате
            file.write(settings.tag + ';' + p_date.strftime('%d.%m.%Y %X') + ';' + plaza + ';'  + '\n') #формирование строки csv файла
            #p_date = p_date + datetime.timedelta(minutes=15) #двигаю исходную дату для чистоты эксперимента
        settings.date = settings.date + datetime.timedelta(minutes=pt) + datetime.timedelta(minutes=1)
        
    file.close()            
                             


def prime():
    try:
        settings = parse_arguments()
        check_arguments(settings)
    except Exception as e:
        print('Неверные параметры: ' + str(e))
        return
    print(settings)
    print(make_routs(settings))
    make_csv(make_routs(settings),settings)    

def main():
    prime()  
    
if __name__ == '__main__':
    main()