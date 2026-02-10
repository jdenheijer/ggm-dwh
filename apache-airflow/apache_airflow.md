## Apache Airflow
Apache Airflow is an open-source platform used for programmatically authoring, scheduling, and monitoring workflows, particularly in data engineering

## Installatie airflow
Volg de instructies op de airflow website om een docker image te draaien: https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

# Login
http://localhost:8080
airflow
airflow

# Voeg de verbindings parameters naar de RXM api op
1. Voeg de api credentials toe in een Airflow connection:
    Admin->Connections->Add connection
        Connection ID: rxm_api
        Connection type: http
        Description: rxm_api_details
        Login: {Het gebruikersnaam van de API}
        Password: {Het wachtwoord van de API}

2. Voeg de api URL toe in een Airflow variabele:
    Admin->Variables->Add Variable
        Key: rxm_api_biexport_url
        Value: {Het url van de endpoint van de bi-export}
