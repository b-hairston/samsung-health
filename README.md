# samsung-health

#### Components
- Python + Prefect (ETL) [In Progress 1/19/25]
- Postgres (DB) [Local Testing Complete 1/19/25]
- ~~DBT (Optional)~~
- Metabase (BI) [In Progress 1/19/25]

#### Data Requirements

Available Data:
- Step Data
- Exercise Data - [Complete 1/19/25]
- Sleep Data
- Heart Rate Data
- Calorie Burn Data 
- Skin Temp Data

##### Questions to Answer
- Can improvement be shown in heart rate over time during exercise?
- Can it be established that better sleep is had based on consistent exercise periods?
- Can calorie burn and exercise frequency/difficulty show longer rest periods?


#### Further Development Ideas
- Create an application to transfer data from Samsung Health to S3
    - currently SH doesn't have an open API to request against, though it has an SDK
    - https://developer.samsung.com/codelab#Health
    - datatypes and units will come from this sorta data dictionary:
        - https://developer.samsung.com/health/android/data/api-reference/com/samsung/android/sdk/healthdata/HealthConstants.Exercise.html#DURATION
x
