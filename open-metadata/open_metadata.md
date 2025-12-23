## Open Metadata (OM)
Open Metadata is een open source tool waarmee je verschillende vormen van metadata kan beheren. 

### Installatie OM
Volg de instructie van de volgende link. Voor de demo omgeving is het volgende image geinstalleerd: https://github.com/open-metadata/OpenMetadata/releases/download/1.11.3-release/docker-compose-postgres.yml

### Configuratie OM
Navigeer naar http://localhost:8585 en login

  username: admin@open-metadata.org
  password: admin

Ga naar Instellingen, Services, Databases, Nieuwe Service toevoegen, selecteer Postgres en druk op Volgende. 

  Servicenaam: ggm-dwh

Druk op Volgende.

  Username: youruser
  Auth config type: Basic Auth
  Password: yourpassword
  Host and Port: postgres:5432
  Database: ggm_dwh
  Ingest All Databses: toelichting_resultaat

Klik op Volgende, en daarna Save. Er wordt nu een ingestion-agent gestart. Als deze klaar is dan is de database inzichtelijk in Open Metadata.

### dbt ingestie
#### Python requirements
Voor de ingestie van dbt zijn er twee python packages nodig:
```bash
pip install --upgrade mashumaro #
pip install collate-dbt-artifacts-parser
pip install openmetadata-ingestion

```

Hernoem het .env.example naar .env
Pas vervolgens de paden aan, naar de paden op jouw locale omgeving. 
Haal ook jouw jwt token op uit open metadata
1. Login in Open Metadata
2. Ga naar Settings
3. Ga naar Bots
4. Open de IngestionBot
5. Kopieer het JWT token, en plaats dat in de .env file

in de rootfolder van dit project, draai in je console het command
```bash
python run_ingestion.py
```

### Next steps
- Ingestie van dbt relics : https://docs.open-metadata.org/latest/connectors/ingestion/workflows/dbt/run-dbt-workflow-externally#4.-local-storage
- Opzetten structurele ingest
- Integratie airflow/postgres met onze eigen airflow/postgres?
- Alles verder uitwerken.. wie gaan met OM aan de slag? Welke rechten hebben ze (niet), beter inrichtingen van alles.. etc.



