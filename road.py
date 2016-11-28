#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import datetime
import os
import random
import sys
import traceback

PATH = '643:1:1:'

road51 = [[51,0,True,False,False],
          [53,2500,True,False,False],
          [2,2500,False,True,False],
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
    
def make_routes(settings):
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
    
def calc_times(allroutes, settings):
    for route in allroutes:
        for i in range(len(route)):
            # формирую точку вьезда вида 643:1:1:узел
            plaza = PATH + str(route[i][0])
            
            # рассчет времени до этой точки в минутах
            mins = round(route[i][1]*3.6/50/60)
            
            # прибавление полученного интервала к указанной дате
            route_dt = settings.date + datetime.timedelta(minutes=mins)
            if i > 0 and (route_dt - route[i-1][1]).seconds == 0:
                route_dt += datetime.timedelta(minutes=1)
            
            route[i] = [settings.tag, route_dt, plaza]

        settings.date = route[-1][1] + datetime.timedelta(minutes=1)
          
def make_csv(allroutes):
    # открываю файл на запись
    file = open('/home/user/Projects/test.csv', 'w')
    for route in allroutes:
        random.shuffle(route)
        for point in route:
            file.write('{};{};{};\n'.format(point[0], point[1].strftime('%d.%m.%Y %X'), point[2]))
    file.close()
    

def prime():
    try:
        settings = parse_arguments()
        check_arguments(settings)
    except Exception as e:
        print('Неверные параметры: ' + str(e))
        return
    # print(settings)
    # print(make_routs(settings))
    routes = make_routes(settings)
    calc_times(routes, settings)
    make_csv(routes)    

def main():
    prime()  
    
if __name__ == '__main__':
    main()