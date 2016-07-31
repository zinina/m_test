#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import cx_Oracle

APCORE_QUERY_TEMPLATE = """
                          SELECT 'AP' host, alitem FROM ap2.AUTH_LIST_ITEM
                          WHERE alitem LIKE '{}%'
                          AND (end_dt IS NULL OR end_dt > CURRENT_DATE)
                          UNION ALL
                          SELECT 'CORE' host, alitem FROM o_auth.AUTH_LIST_ITEM
                          WHERE alitem LIKE '{}%'
                          AND (end_dt IS NULL OR end_dt > CURRENT_DATE)
                          ORDER BY 2,1
                        """
LOGIN = "login"
PSW = "psw"
DNS = "dns"
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
    
def apcore(pan):
    query = APCORE_QUERY_TEMPLATE.format(pan)
    sys_connection = None
    sys_cursor = None
    
    try:
        sys_connection = cx_Oracle.connect(LOGIN, PSW, DNS)
        sys_cursor = sys_connection.cursor()        
        sys_cursor.execute(query)        
        result = sys_cursor.fetchall()        
        if len(result) == 0:
            print("Записей не найдено")
        for row in result:
           print(row)
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(error.message)
        
    if sys_cursor:
        sys_cursor.close()
    if sys_connection:
        sys_connection.close()
        

def main():
    pan = parse_arguments()
    pan = check_arguments(pan)
    apcore(pan)
    
if __name__ == '__main__':
    main()    
    
    