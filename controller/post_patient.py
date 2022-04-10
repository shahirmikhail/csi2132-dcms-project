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

def post_patient(payload):
    patient_id = str(generate_patient_id())
    ssn = payload["ssn"]
    firstname = payload["firstname"]
    lastname = payload["lastname"]
    insurance = payload["insurance"]
    gender = payload["gender"]
    streetname = payload["streetname"]
    streetnum = payload["streetnum"]
    apartment = payload["apartment"]
    city = payload["city"]
    province = payload["province"]
    zipcode = payload["zipcode"]
    phonenum = payload["phonenum"]
    dateofbirth = payload["dateofbirth"]
    branch_id = payload["branch_id"]
    user_id = payload["user_id"]
    #
    # sql_str = 'INSERT INTO "DBclinic".patient' \
    #           ' (patient_id, ssn, firstname, lastname, insurance, gender, streetname, streetnum, ' \
    #           'apartment, city, province, zipcode, phonenum, dateofbirth, branch_id, user_id) ' \
    #           'VALUES ('+patient_id+', ' \
    #                 + ssn + ', ' \
    #                 + '\'' + firstname + '\', ' \
    #                 + '\'' + lastname + '\', ' \
    #                 + '\'' + insurance + '\', ' \
    #                 + '\'' + gender + '\', ' \
    #                 + '\'' + streetname + '\', ' \
    #                 + streetnum + ', ' \
    #                 + apartment + ', ' \
    #                 + '\'' + city + '\', ' \
    #                 + '\'' + province + '\', ' \
    #                 + '\'' + zipcode + '\', ' \
    #                 + '\'' + phonenum + '\', ' \
    #                 + '\'' + dateofbirth + '\', ' \
    #                 + branch_id + ', ' \
    #                 + user_id + '); '
    # print(sql_str)
    # conn = get_db_connection()
    # cur = conn.cursor()
    # cur.execute(sql_str)
    # # branches = cur.fetchall()
    # cur.close()
    # conn.close()

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO "DBclinic".patient (patient_id, ssn, firstname, lastname, insurance, gender, streetname, streetnum, apartment, city, province, zipcode, phonenum, dateofbirth, branch_id, user_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (patient_id, ssn, firstname, lastname, insurance, gender, streetname, streetnum, apartment, city, province, zipcode, phonenum, dateofbirth, branch_id, user_id)
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        message = "Record inserted successfully into DBclinic.patient table"
        status_code = 201

    except (Exception, psycopg2.Error) as error:
        message = "Failed to insert record into DBclinic.patient table" + str(error)
        status_code = 400

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return {"message": message, "status_code": status_code}


def generate_patient_id():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM "DBclinic".patient ORDER BY patient_id DESC;')
    patients = cur.fetchall()
    cur.close()
    conn.close()
    largest_patient_id = (patients[0])[0]
    new_patient_id = largest_patient_id+1
    return new_patient_id

