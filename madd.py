#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import sys

PAN = None
IN = None 
OUT = None
DATE = None
TS = 1 # по умолчанию первый
COUNT = 1 # по умолчанию одна
ADD_QUERY_TEMPLATE = """
begin
   onm_api_crms.api_emul.create_passage_trx(
     p_plaza_out => '643:00042:01:{}', 
     p_plaza_in => '643:00042:01:{}',
     p_pan => '{}',
     p_class => '{}',
     p_cnt => {},
     p_dt => to_date('{}', 'yyyy-mm-dd hh24:mi:ss'));
commit;
end;
"""

def parse_arguments():
    if len(sys.argv) > 5 or len(sys.argv) < 4:
        print('Неправильное количество аргументов')
        exit (1)
    global PAN,IN,OUT,DATE,TS
    PAN = sys.argv[1]
    IN = sys.argv[2]
    OUT = sys.argv[3]
    if len(sys.argv) > 4:
        DATE = sys.argv[4]  

def check_arguments():
    global PAN,IN,OUT,DATE
    if len(PAN) != 19:
        print("Неверный PAN")
        exit(2)
    try:
        PAN = int(PAN)
    except:
        print("Неверный PAN")
        exit(2)
    
    if IN not in ('11','12','15','16','17','18'):
        print('Неверная точка входа')
        exit(3)
    
    if OUT not in ('11','12','15','16','17','18'):
        print('Неверная точка выхода')
        exit(4)
        
    if DATE == None:
        DATE = datetime.datetime.now()
    else:
        try:
            DATE = datetime.datetime.strptime(DATE, '%Y-%m-%d %X')
        except:
            print('Неверная дата')
            exit(5)
    if abs(DATE.year - datetime.datetime.now().year) > 1:
        print('Слишком отдаленный период времени')
        exit(5)
    # TODO доделать проверку TS и COUNT
    # переделать exit на raise
    #в single_madd сделать try и ловить исключение

def do_madd(pan, in_plaza, out_plaza, moment, ts_class, count):
    moment_str = moment.strftime('%Y-%m-%d %X')
    query = ADD_QUERY_TEMPLATE.format(in_plaza, out_plaza, pan, ts_class, count, moment_str)
    # print(query)
    exit_code = os.system('echo "{}" | ./dummy_sqlplus.sh'.format(query))
    print("exit code: {}".format(exit_code))
    
def single_madd():    
    parse_arguments()
    check_arguments()
    do_madd(PAN, IN, OUT, DATE, TS, COUNT)

def parse_line(line):
    tokens = line.split(',')
    global PAN,IN,OUT,DATE,TS,COUNT
    PAN = tokens[0].trim()
    IN = tokens[1].trim()
    OUT = tokens[2].trim()
    DATE = tokens[3].trim()
    TS = tokens[4].trim()
    COUNT = tokens[5].trim()
    check_arguments()

def butch_madd():
    file = sys.argv[1]
    for line in file:
        try:
            parse_line(line)
        except:
            print('Плохая строка: ' + line)
            continue
        do_madd(PAN, IN, OUT, DATE, TS, COUNT)
        
    
def main():
    if len(sys.argv) == 2:
        butch_madd()
    else:
        single_madd()
    
if __name__ == '__main__':
    main()