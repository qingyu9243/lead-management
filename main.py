import uvicorn
import uuid
import mysql.connector
from fastapi import FastAPI
from pydantic import BaseModel

import lead_utils

class Payload(BaseModel):
    first_name: str
    last_name: str
    email:str
    resume: str

app = FastAPI()

@app.post("/lead")
def create_lead(payload: Payload):
    lead_id = str(uuid.uuid4())
    mydb = None
    try:
        mydb = mysql.connector.connect(
            host = "127.0.0.1",
            port = 3306,
            user = "root",
            password = "password",
            database = "lead_data"
        )

        # create table if not exist: lead if not exist
        sql_create_table = "CREATE TABLE IF NOT EXISTS lead_data.applications \
            (id VARCHAR(36) PRIMARY KEY, \
            first_name VARCHAR(255) NOT NULL, \
            last_name VARCHAR(255) NOT NULL, \
            email VARCHAR(100) NOT NULL, \
            resume VARCHAR(255) NOT NULL,\
            status VARCHAR(36) NOT NULL)"
        
        # insert the row with values
        sql_insert_value = "INSERT INTO lead_data.applications (id, first_name, last_name, email, resume, status) \
                            VALUES (%s, %s, %s, %s, %s, %s)"
        status = str(lead_utils.Status.PENDING)
        values = (lead_id, payload.first_name, payload.last_name, payload.email, payload.resume, status)

        mycursor = mydb.cursor()
        mycursor.execute(sql_create_table)
        mycursor.execute(sql_insert_value, values)
        mydb.commit()
        print(mycursor.rowcount, "Lead record insert into leads table.")
        mycursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into MySQL table. {}".format(error))

    finally:
        if mydb and mydb.is_connected():
            mydb.close()
            print("MySql connection is closed")
    
    return {
        "lead_id":lead_id,
        "first_name": payload.first_name,
        "last_name": payload.last_name,
        "email": payload.email,
        "resume": payload.resume,
        "status": lead_utils.Status.PENDING
        }

@app.get("/lead/{lead_id}")
def get_lead(lead_id: str):
    mydb = None
    try:
        mydb = mysql.connector.connect(
            host = "127.0.0.1",
            port = 3306,
            user = "root",
            password = "password",
            database = "lead_data"
        )

        # get application/lead info by id
        #sql_select_by_id = "SELECT * FROM lead_data.applications WHERE id = %s", lead_id

        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute("SELECT * FROM lead_data.applications WHERE id = %s", (lead_id,))
        application_record = mycursor.fetchone()
        if application_record:
            #print(application_record)
            return {
                "lead_id":application_record["id"],
                "first_name": application_record["first_name"],
                "last_name": application_record["last_name"],
                "email": application_record["email"],
                "resume": application_record["resume"],
                "status": application_record["status"]
                }

    except mysql.connector.Error as error:
        print("Failed to retrieve record into MySQL table. {}".format(error))

    finally:
        if mydb and mydb.is_connected():
            mycursor.close()
            mydb.close()
            print("MySql connection is closed")    


@app.put("/lead/{lead_id}")
def update_lead(lead_id, new_status):
    return {"lead_id":"12389793"}
# curl -X PUT  http://127.0.0.1:5000/lead/xxxxxxx --data '{"status":1}'

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")

