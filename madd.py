#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import cx_Oracle
import datetime
import os
import sys
import traceback



PAN = None
IN = None 
OUT = None
DATE = None
TS = 1 # по умолчанию первый
COUNT = 1 # по умолчанию одна
ADD_QUERY_TEMPLATE = """
BEGIN
   onm_api_crms.api_emul.create_passage_trx(
     p_plaza_out => '643:00042:01:{}', 
     p_plaza_in => '643:00042:01:{}',
     p_pan => '{}',
     p_class => '{}',
     p_cnt => {},
     p_dt => to_date('{}', 'yyyy-mm-dd hh24:mi:ss'));
END;
"""
LOGIN = "o"
PSW = "o"
DNS = "10"

def parse_arguments():
    parser = argparse.ArgumentParser(description='Все писать сюды')
    parser.add_argument("--pan", type=int, required = True)
    parser.add_argument("--in", type=int, default = 11, choices = [11,12,15,16,17,18], dest = "inn")
    parser.add_argument("--out", type=int, required = True, choices = [11,12,15,16,17,18])
    parser.add_argument("--date", type=str, default = datetime.datetime.now().strftime('%Y-%m-%d %X'))
    parser.add_argument("--ts", type=int, default = 1, choices = [1,2,3,4])
    parser.add_argument("--count", type=int, default = 1)
    return parser.parse_args()

def check_arguments(settings):
    if len(str(settings.pan)) != 19:
        raise Exception("Неверный PAN")

    if settings.inn not in [11,12,15,16,17,18]:
        raise Exception("Неверная точка въезда")
    if settings.out not in [11,12,15,16,17,18]:
        raise Exception("Неверная точка выезда")
    if settings.inn == settings.out:
        raise Exception("Точки въезда и выезда не могут совпадать!")
     
    if settings.date == 'now':
        settings.date = datetime.datetime.now()
    else:    
        try:
            settings.date = datetime.datetime.strptime(settings.date, '%Y-%m-%d %X')
        except:
            raise Exception("Неверный формат даты")
        if abs(settings.date.year - datetime.datetime.now().year) > 1:
            raise Exception('Слишком отдаленный период времени')
            
    if settings.count < 1:
        raise Exception("Неверное число проездов")
        
    if settings.ts not in [1, 2, 3, 4]:
        raise Exception("Неверный класс ТС")

    #в single_madd сделать try и ловить исключение

def do_madd(settings):
    crms_connection = None
    crms_cursor = None
    date = settings.date.strftime('%Y-%m-%d %X')
    query = ADD_QUERY_TEMPLATE.format(settings.inn, settings.out, settings.pan, settings.ts, settings.count, date)
    # print(query)
    #exit_code = os.system('echo "{}" | ./dummy_sqlplus.sh'.format(query))
    #print("exit code: {}".format(exit_code))
    query_api_login = "BEGIN :k := onm.ac.login('l', 's', 'C'); onm.ac.init(:k); onm.ac.set_position(31); END;"
    try:
        crms_connection = cx_Oracle.connect(LOGIN, PSW, DNS)
        crms_cursor = crms_connection.cursor()    
        key = crms_cursor.var(cx_Oracle.STRING)
        crms_cursor.execute(query_api_login, k = key)
        crms_cursor.execute(query)
        print(query)
        crms_connection.commit()
        print("commited")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(error.message)
    if crms_cursor:
        crms_cursor.close()
    if crms_connection:
        crms_connection.close()
    
def single_madd():
    try:
        settings = parse_arguments()
        check_arguments(settings)
    except Exception as e:
        print('Неверные параметры: ' + str(e))
        return
    print(settings)
    do_madd(settings)

def parse_line(line):
    class s:
        pass
       
    tokens = line.split(',')
    settings = s()
    settings.pan = int(tokens[0].strip())
    settings.inn = int(tokens[1].strip())
    settings.out = int(tokens[2].strip())
    settings.date = tokens[3].strip()
    settings.ts = int(tokens[4].strip())
    settings.count = int(tokens[5].strip())
    check_arguments(settings)
    return settings

def butch_madd():
    file = open(sys.argv[1])
    for line in file:
        try:
            settings = parse_line(line)
        except Exception as e:
            print('Плохая строка: ' + line[:-1] + ': ' + str(e))
            # print(traceback.format_exc())
            continue
        do_madd(settings)
    file.close()    
    
def main():
    if len(sys.argv) == 2:
        butch_madd()
    else:
        single_madd()
    
if __name__ == '__main__':
    main()