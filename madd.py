#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import sys

PAN = None
IN = None 
OUT = None
DATE = None

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
    
def main():    
    if len(sys.argv) > 5 or len(sys.argv) < 4:
        print('Неправильное количество аргументов')
        exit (1)
    global PAN,IN,OUT, DATE
    PAN = sys.argv[1]
    IN = sys.argv[2]
    OUT = sys.argv[3]
    if len(sys.argv) > 4:
        DATE = sys.argv[4]
        
    check_arguments()
    
if __name__ == '__main__':
    main()