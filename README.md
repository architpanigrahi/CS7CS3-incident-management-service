# CS7CS3-incident-management-service
One of the backends for final code made in submission for CS7CS3 at TCD 202425.

## Start docker compose file - 
1. DynamoDB -- 8000
2. Prometheus -- 9090
3. Grafana -- 3000

Execute the below from the root folder.
`cd docker
docker-compose up -d`

## Create "Incidents" Table
1. Install AWS NoSQL Workbench
2. Create a file ~/.aws/credentials with the following contents
`
[default]
aws_access_key_id = fakeAccessKey
aws_secret_access_key = fakeSecretKey
`

3. Create a file ~/.aws/config with the following contents
`
[default]
region = us-west-1
`

4. Connect to localhost:8000 and create Incidents table with "incident_id" as primary key (partition key).


## Start App
Run the below code in the root folder.
`
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
`
