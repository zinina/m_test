#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
# import cx_Oracle
import datetime
import os
import sys
import traceback

#ADD_QUERY_TEMPLATE = """
#BEGIN
#   onm_api_crms.api_emul.create_passage_trx(
#     p_plaza_out => '643:00042:01:{}', 
#     p_plaza_in => '643:00042:01:{}',
#     p_pan => '{}',
#     p_class => '{}',
#     p_cnt => {},
#     p_dt => to_date('{}', 'yyyy-mm-dd hh24:mi:ss'));
#END;
#"""
#LOGIN = "o"
#PSW = "o"
#DNS = "10"

road51 = [[51,0,True,False],
          [53,2500,True,False],
          [2,2500,False,True],
          [1,2550,True,False],
          [4,4750,False,True],
          [5,4750,False,False],
          [8,4750,True,False],
          [55,8650,False,True],
          [9,8650,True,False],
          [61,17450,False,True],
          [63,17450,True,False],
          [65,19650,True,False],
          [11,22550,False,True],
          [67,22550,True,False],
          [17,31050,False,True],
          [77,39550,True,False],
          [78,39550,True,False],
          [19,53750,False,True]]

def parse_arguments():
    parser = argparse.ArgumentParser(description='tag date road')
    parser.add_argument("--tag", type=str, default = '01')
    parser.add_argument("--date", type=str, default = datetime.datetime.now().strftime('%Y-%m-%d %X'))
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
            settings.date = datetime.datetime.strptime(settings.date, '%Y-%m-%d %X')
        except:
            raise Exception("Неверный формат даты")
        if abs(settings.date.year - datetime.datetime.now().year) > 1:
            raise Exception('Слишком отдаленный период времени')
    

def pp(settings):
    date = settings.date.strftime('%Y-%m-%d %X')
    if settings.road == 51:
        r = road51
    else:
        r = road52
    for i in r:
        if not i[2]:
            continue
        route = [i]
        for l in r:
            if l[1] < i[1] or l[2]:
                continue
            if not l[3]:
                route.append(l)
            if l[3]:
                print(route + [l])
    

# def pp2(settings):
#     crms_connection = None
#     crms_cursor = None
#     date = settings.date.strftime('%Y-%m-%d %X')
#     query = ADD_QUERY_TEMPLATE.format(settings.inn, settings.out, settings.pan, settings.ts, settings.count, date)
    # print(query)
    #exit_code = os.system('echo "{}" | ./dummy_sqlplus.sh'.format(query))
    #print("exit code: {}".format(exit_code))
#     query_api_login = "BEGIN :k := onm.ac.login('l', 's', 'C'); onm.ac.init(:k); onm.ac.set_position(31); END;"
#     try:
#         crms_connection = cx_Oracle.connect(LOGIN, PSW, DNS)
#         crms_cursor = crms_connection.cursor()    
#         key = crms_cursor.var(cx_Oracle.STRING)
#         crms_cursor.execute(query_api_login, k = key)
#         crms_cursor.execute(query)
#         print(query)
#         crms_connection.commit()
#         print("commited")
#     except cx_Oracle.DatabaseError as e:
#         error, = e.args
#         print(error.message)
#     if crms_cursor:
#         crms_cursor.close()
#     if crms_connection:
# crms_connection.close()

def p():
    try:
        settings = parse_arguments()
        check_arguments(settings)
    except Exception as e:
        print('Неверные параметры: ' + str(e))
        return
    print(settings)
    pp(settings)    

def main():
    p()  
    
if __name__ == '__main__':
    main()