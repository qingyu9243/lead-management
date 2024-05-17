# lead-management System
Design Doc:
https://quip.com/ePFlAKh5CxFD/One-Page-Design-Lead-Management-System

Overview
The Lead Management System (LMS) is a FastAPI-based application designed to manage lead information effectively. It allows for the creation, retrieval, and updating of lead details within an organization. The system also automates the sending of notification emails when new leads are created.

Local Setup
Setting Up the MySQL Database
Start MySQL using Docker:
Run the following command to pull the MySQL image and start a MySQL container. Replace yourpassword with a secure password.

docker run --name mysql-lead-db -e MYSQL_ROOT_PASSWORD=yourpassword -e MYSQL_DATABASE=lead_data -p 3306:3306 -d mysql:latest
This command sets up a MySQL server running in a Docker container named mysql-lead-db and exposes port 3306. It also creates a database named lead_data.

Accessing MySQL:
Access the MySQL shell using Docker with the following command:

docker exec -it mysql-lead-db mysql -uroot -pyourpassword
Setting Up the FastAPI Application
Install Required Libraries:
Ensure you have the required Python libraries installed. You can install them using pip:

pip install fastapi uvicorn mysql-connector-python
Running the FastAPI Server:
Navigate to the directory containing your FastAPI application and start the server using Uvicorn:

uvicorn main:app --reload
Replace main with the name of your Python script if different.

Testing the Application Locally
Testing with curl
Create Lead:
Use the following curl command to create a lead:

curl -X POST http://127.0.0.1:8000/lead -H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "email": "johndoe@example.com", "resume": "resume.pdf"}'
Retrieve Lead:
Replace {lead_id} with the actual lead ID returned by the create API:

curl -X GET http://127.0.0.1:8000/lead/{lead_id}
Update Lead:
Replace {lead_id} with the lead ID:

curl -X PUT http://127.0.0.1:8000/lead/{lead_id} -H "Content-Type: application/json" -d '{"status":"reached_out"}'
Using API Testing Tools
Alternatively, you can use API testing tools like Postman or Insomnia for a more interactive way of testing the APIs.
