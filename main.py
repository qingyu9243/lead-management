import uvicorn
import uuid
import mysql.connector
from fastapi import FastAPI

import lead_utils

app = FastAPI()

@app.post("/lead")
def create_lead(first_name: str, last_name: str, email: str, resume_file: str):
    lead_id = f'{uuid.uuid4()}
    
    try:
        mydb = mysql.connector.connect(
            host = "127.0.0.1:3306",
            user = "my-sql",
            password = "password",
            database = "lead_data"
        )

        # create table: lead if not exist
        sql_create_table = "CREATE TABLE IF NOT EXISTS leads (id, first_name, last_name, email, resume_file) VALUES (%s, %s, %s, %s, %s)"
        # insert the row with values
        sql_insert_value = "INSERT INTO leads ()"
        values = (lead_id, first_name, last_name, email, resume_file)

        mycursor = mydb.cursor()
        mycursor.execute(sql_create_table, values)
        mydb.commit()
        print(mycursor.rowcount, "Lead record insert into leads table.")
        mycursor.close()

    except mysql.connector.Error as error:
        print("".format(error))

    finally:
        if mydb.is_connected():
            mydb.close()
            print("MySql connection is closed")

    return {
        "lead_id":lead_id,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "status": lead_utils.Status.PENDING}
        
## curl -X POST -F 'username=your_username' -F 'email=your_email@example.com' -F 'file=@/path/to/your/file' http://127.0.0.1:5000/lead

@app.get("/lead/{lead_id}")
def get_lead(lead_id: str):
    
    return {
        "lead_id":"12389793",
        "first_name": first_name,
        "last_name": last_name,
        "email": email}

@app.put("/lead/{lead_id}")
def update_lead(lead_id: uuid, new_status: lead_utils.Status.REACHED_OUT):


    return {"lead_id":"12389793"}
# curl -X PUT  http://127.0.0.1:5000/lead/xxxxxxx --data '{"status":1}'

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")

