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

def get_all_procedures():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM "DBclinic".procedure;')
    procedures = cur.fetchall()
    cur.close()
    conn.close()
    print(procedures)
    main_json_str = "[" #open bracket
    for item in procedures:
        json_str = "{\"procedure_id\": "+str(item[0])+", \"patient_id\": "+str(item[1])+", \"appointment_id\": "+str(item[2])+", \"procedure_code\": \""+str(item[3])+"\", \"procedure_type\": \""+str(item[4])+"\", \"description\": \""+str(item[5])+"\"},"
        main_json_str = main_json_str + json_str
    main_json_str = main_json_str[:-1] #remove last comma
    main_json_str = main_json_str + "]" #add closing bracket
    print(main_json_str)
    procedures_json = json.loads(main_json_str)
    #     item = [1, "Ottawa"]
    # print("branches")
    # print(branches)
    return procedures_json

