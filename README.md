## Project Overview
The project aims to create a robust data pipeline for obtaining economic data from EconDB.com, transforming it, storing it, and making it available for dashboarding and analysis.
![System](https://github.com/john-ml-dev/econdb_project/assets/78201996/b2e36f97-54a9-4bf1-8d68-799b0eee5b08)
~ **By _John Tamakloe_**
### Data Gathering

- **Source**: Data is gathered from [econdb.com]([https://www.econdb.com/home]). Econdb is a leading data service for economic indicators and the shipping industry.
### Scheduling

- **Tool**: Airflow is used to schedule the data fetching process.
- Apache Airflow is used for orchestrating the workflow, managing task dependencies, scheduling, and monitoring the data pipeline.
- Airflow handles the execution of each step in the pipeline, ensuring tasks are run in the correct order and handling retries and failures.
- **Frequency**: The project is scheduled to run daily.

### Containerization
- **Tool**: Docker is used to containerize the project.
- **Reason for Choosing Docker**: Docker simplifies the setup and ensures replicability of the project across different operating systems.
-------------

This document outlines the setup and usage instructions for the **econdb_project** project. Follow the steps below to clone the repository, set up the environment, and run the project.

# Setup Instructions

Create an account with econdb by visiting https://www.econdb.com/home
After creating your account locate your `API_TOKEN` by visiting https://www.econdb.com/account/keys/

## Directory Structure

```plaintext
econdb_project/
│
├── airflow/
│
├── Docs/
│
├── images/
│
├── PowerBI/  
│
└── README.md
```

## 1. Clone the Repository
Clone the repository to your local machine using the following command:
```sh
git clone github.com/john-ml-dev/econdb_project.git
```
## 2. Change Directory to airflow
Navigate to the airflow directory:
```sh
cd airflow
```
The folder structure should look like this
```plaintext
airflow/
│
├── dags/
│
├── input/
│
├── logs/
│
├── output/
│
├── pg-init-scripts/
│
├── plugins/
│
├── sql/
│
├── test/
│
├── .env
│
├── .ignore
│
├── docker-compose.yml
│
├── Dockerfile
│
└── requirements.txt
```
### Essential Folders

`dags/`
Description: Contains Directed Acyclic Graphs (DAGs) which define the workflows and tasks to be executed by Airflow.
Purpose: Essential for orchestrating the sequence and dependency of tasks in data processing pipelines. 
`main.py` serves as the heart of the project all dag tasks are implemented here

`plugins/`
Description: Directory for custom plugins to extend Airflow’s functionality.
Functions for various tasks are implemented here in a dedicated .py file and imported in `main.py`
`output/`
Purpose: Directory for saving output files
`input/`
Purpose: Contains countries dataset as `countries.csv`

## 3. Build the Docker Image
Build the Docker image with the tag `pandas_airflow:latest`: by running the command
```sh
docker compose build --tag pandas_airflow:latest .
```
This allows docker to install pandas in airflow since airflow does not comes with pandas by default. 
To use any other package or library, locate the `requirements.txt` and add package name to the list or run 
```bash
echo "package_name" > requirements.txt
```
The above command adds the package with the package name `package_name` to the bottom of the list of packages in the requirements.txt file
## 4. Update `.env` with S3 Credentials and API_TOKEN
Update the `.env` file with your AWS S3 credentials. This file should contain the necessary environment variables for accessing your S3 bucket and econdb

## 5. Start the Docker Containers
Whiles your docker desktop is running in the background, start the Docker containers in detached mode:
```sh
docker compose up -d
```
## 6. Access the Airflow UI
Open your web browser and go to http://localhost:8080 to access the Airflow UI.

## 7. Connect to PostgreSQL
Use a SQL tool such as DBeaver or Valentina Studio to connect to the PostgreSQL database. Enter the connection details as specified above.

## 8. Verify S3 Upload
Verify that the fils have been successfully uploaded to s3 bucket.

## 9. Terminate program gracefully
Run the code in your terminal to gracefully end the program
```sh
docker compose down
```
