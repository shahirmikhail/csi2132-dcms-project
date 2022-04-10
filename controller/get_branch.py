import os
import psycopg2
from flask import Flask, render_template
import json

def get_db_connection():
    # conn = psycopg2.connect(host='ec2-34-231-63-30.compute-1.amazonaws.com',
    #                         database=os.environ['DB_NAME'],
    #                         user=os.environ['DB_USERNAME'],
    #                         password=os.environ['DB_PASSWORD'])
    conn = psycopg2.connect(host='ec2-34-231-63-30.compute-1.amazonaws.com',
                            database="dfkjl7dui72stg",
                            user="pmhsdddzxbeguh",
                            password="e3abc65ef611b4bdfea7b4ff8d41b2dd3073c9db00049b3d07f9058045537869")
    return conn

def get_all_branches():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM "DBclinic".branch;')
    branches = cur.fetchall()
    cur.close()
    conn.close()
    main_json_str = "[" #open bracket
    for item in branches:
        json_str = "{\"branch_id\": "+str(item[0])+", \"branch_location\": \""+item[1]+"\"},"
        main_json_str = main_json_str + json_str
    main_json_str = main_json_str[:-1] #remove last comma
    main_json_str = main_json_str + "]" #add closing bracket
    print(main_json_str)
    branches_json = json.loads(main_json_str)
    #     item = [1, "Ottawa"]
    # print("branches")
    # print(branches)
    return branches_json


def get_all_dentists_from_branch(branch_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM "DBclinic".employee WHERE branch_id = '+str(branch_id)+'AND employee_type = '
                                                                                      '\'Dentist\';')
    dentists = cur.fetchall()
    cur.close()
    conn.close()
    main_json_str = "[" #open bracket
    for item in dentists:
        json_str = "{\"employee_id\": "+str(item[0])+", " \
                        "\"employee_type\": \""+item[1]+"\", " \
                        "\"ssn\": "+str(item[2])+"," \
                        "\"role\": \"" + item[3] + "\", " \
                        "\"salary\": \"" + str(item[4]) + "\", " \
                        "\"firstname\": \"" + item[5] + "\", " \
                        "\"lastname\": \"" + item[6] + "\", "\
                        "\"gender\": \"" + item[7] + "\", " \
                        "\"streetname\": \"" + item[8] + "\", " \
                        "\"streetnum\": \"" + str(item[9]) + "\", " \
                        "\"apartment\": \"" + str(item[10]) + "\", " \
                        "\"city\": \"" + item[11] + "\", " \
                        "\"province\": \"" + item[12] + "\", " \
                        "\"zipcode\": \"" + item[13] + "\", " \
                        "\"phonenum\": \"" + item[14] + "\", " \
                        "\"dateofbirth\": \"" + str(item[15]) + "\", " \
                        "\"branch_id\": \"" + str(item[16]) + "\", " \
                        "\"user_id\": \"" + str(item[17]) + "\"},"
        main_json_str = main_json_str + json_str
    main_json_str = main_json_str[:-1] #remove last comma
    main_json_str = main_json_str + "]" #add closing bracket
    print(main_json_str)
    dentists_json = json.loads(main_json_str)
    #     item = [1, "Ottawa"]
    # print("branches")
    # print(branches)
    return dentists_json

