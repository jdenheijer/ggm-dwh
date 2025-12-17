## ggm-dbt-postgres-pgadmin
Dit project is een simpel voorbeeld dat een schets geeft van hoe het GGM gemodelleerd zou kunnen worden aan de hand van dbt. 

Let op! Dit project is nog niet af en bevat ongeverifieerde door AI gegenereerde code!

Dit project gebruikt docker voor een locale Postgresql database, en pgadmin om de database te benaderen.
Het bevat een dbt model waarmee rauwe data (gebaseerd op een zaak-applicatie) vertaald wordt naar de GGM tabel "zaken", onderdeel van .
De rauwe data zijn in dit voorbeeld een drietal simpele csv bestanden in de dbt/seeds map.

### Benodigde tools
python, git, docker

### Setup postgres, pgadmin
Open Konsole, powershell of iets anders en navigeer naar de map waar je het  project wilt downloaden.

```bash
git clone 
#Takes between 30 seconds and several minutes to download and build the images
docker-compose up --build -d
```

Test pgadmin door in je browser te navigeren naar:
http://localhost:5050
username: your@email.com
wachtwoord: yourpassword

Als je ingelogd bent, klap de Servers open en vervolgens het ggm_dwh. 
Voer het wachtwoord in: yourpassword

### Setup dbt
Maak eerst een virtual environment van Python aan, en installeer de requirements
```bash
pip install dbt-core dbt-postgres
```
of

```bash
pip install -r requirements.txt
```

Open de dbt directory, installeer de dependencies, en check de database verbinding:
```bash
cd dbt
dbt deps #<- voor nu niet nodig (idem packages.yml)>
dbt debug
```

'Seed' het model. dit vult het dwh_raw schema met data uit de csv's.
```bash
dbt seed
```
Optioneel: Bekijk het nieuwe dwh_raw schema in pgadmin. Deze bevat nu een aantal tabellen met data.

Draai nu het stg model
```bash
dbt run --select stg
```
Optioneel: Bekijk de views van het dwh_stg schema.

Draai nu het ggm model
```bash
dbt run --select ggm
```
Optioneel: Bekijk de tabellen in het dwh_ggm schema.

Genereer en bekijk de documentatie. dbt docs serve opent een webbrowser met het model.
```bash
dbt docs generate
dbt docs serve
```

### Next steps
- toevoegen metadata vanuit het GGM, bv https://github.com/Gemeente-Delft/Gemeentelijk-Gegevensmodel/blob/f7957cc9baceeaa54b3837aa79aceeae32c30166/docs/definities/definitie_Model%20Kern%20RGBZ.md#zaak of een betere bron.
- "Echt" het dbt model maken van Zaken, ipv deze ai schmuck. Check ook of het niet Zaak zou moeten zijn ipv zaken?
- Simpele datamart toevoegen
- implementeer open metadata https://docs.open-metadata.org/latest/quick-start/local-docker-deployment
- implementeer cdc (waarschijnlijk met dbt snapshots) en breidt dataset uit
- query naar sql-server ipv postgres ivm pilot omgeving?
- tbd...