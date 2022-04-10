import os
import psycopg2
from flask import Flask, render_template
import json
from controller.uuid import *

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

def post_appointment(payload):
    appointment_id = str(generate_appointment_id())
    employee_id = payload["employee_id"]
    patient_id = payload["patient_id"]
    appointment_date = payload["appointment_date"]
    start_time = payload["start_time"]
    end_time = payload["end_time"]
    status = payload["status"]
    room = payload["room"]

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO "DBclinic".appointment (appointment_id, employee_id, patient_id, appointment_date, start_time, end_time, status, room) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (appointment_id, employee_id, patient_id, appointment_date, start_time, end_time, status, room)
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        message = "Record inserted successfully into DBclinic.appointment table"
        status_code = 201

    except (Exception, psycopg2.Error) as error:
        message = "Failed to insert record into DBclinic.appointment table" + str(error)
        status_code = 400

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return {"message": message, "status_code": status_code}


def generate_appointment_id():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM "DBclinic".appointment ORDER BY appointment_id DESC;')
    appointments = cur.fetchall()
    cur.close()
    conn.close()
    largest_appointment_id = (appointments[0])[0]
    new_appointment_id = largest_appointment_id+1
    return new_appointment_id

