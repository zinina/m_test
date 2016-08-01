#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import cx_Oracle

ADD_QUERY_TEMPLATE = """
                      SELECT * FROM
                           ap2.I_CRMS_SUBSCRIPTION_STATUS
                           WHERE status = 1 and pan = '{}'
                     """
LOGIN = "a"
PSW = "a"
DNS = "10"
def parse_arguments():
    if len(sys.argv) > 2:
        print('Неправильное количество аргументов')
        exit (1)    
    return sys.argv[1]
    
def check_arguments(pan):    
    if len(pan) != 19:
        print("Неверный PAN")
        exit(2)
    try:
        return int(pan)
    except:
        print("Неверный PAN")
        exit(2)
    
def mb(pan):
    query = ADD_QUERY_TEMPLATE.format(pan)
    ap2_connection = None
    ap2_cursor = None
    
    try:
        ap2_connection = cx_Oracle.connect(LOGIN, PSW, DNS)
        ap2_cursor = ap2_connection.cursor()
        ap2_cursor.execute(query)
        result = ap2_cursor.fetchall()
        if len(result) == 0:
            print("Записей не найдено")
        for row in result:
           print("Бокировка: ", row)
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(error.message)
        
    if ap2_cursor:
        ap2_cursor.close()
    if ap2_connection:
        ap2_connection.close()

def main():
    pan = parse_arguments()
    pan = check_arguments(pan)
    mb(pan)
    
if __name__ == '__main__':
    main()    
    
    