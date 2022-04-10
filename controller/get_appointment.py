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


def get_upcoming_appointment(employee_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM "DBclinic".appointment WHERE employee_id = '+str(employee_id)+'AND status = \'upcoming\' ORDER BY appointment_date ASC;')
    appointments = cur.fetchall()
    cur.close()
    conn.close()
    print(appointments)
    main_json_str = "{\"appointment_id\": "+str((appointments[0])[0])+", " \
                        "\"employee_id\": \""+str((appointments[0])[1])+"\", " \
                        "\"patient_id\": "+str((appointments[0])[2])+"," \
                        "\"appointment_date\": \"" + str((appointments[0])[3]) + "\", " \
                        "\"start_time\": \"" + str((appointments[0])[4]) + "\", " \
                        "\"end_time\": \"" + str((appointments[0])[5]) + "\", " \
                        "\"status\": \"" + (appointments[0])[6] + "\", "\
                        "\"room\": \"" + str((appointments[0])[7]) + "\"}"

    appointment_json = json.loads(main_json_str)
    #     item = [1, "Ottawa"]
    # print("branches")
    # print(branches)
    return appointment_json

