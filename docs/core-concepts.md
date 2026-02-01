# Core Concepts

PORTER is an extensible data integration platform designed to facilitate the seamless movement and transformation of data across various systems. 
Below are the core components that make up the PORTER architecture.

## Core Components
- [Pipeline](#pipeline)
- [Connections](#connections)
- [Metadata](#metadata)
- [Source](#source)
- [Target](#target)
- [Dataset](#dataset)
  - [Database Table](#table-as-a-dataset)
  - [Database Query](#query-as-a-dataset)
  - [File](#file-as-a-dataset)
  - [API](#api-response-as-a-dataset)
  - [Stream](#streaming-as-a-dataset)
- [Transformation](#transformation)
  - [Pre Transformations](#pre-transformations)
  - [Post Transformations](#pre-transformations)
- [Validation](#validation)
  - [Pre Validations](#pre-validations)
  - [Post Validations](#post-validations)
- [Governance](#governance)
  - [Audit](#audit)
  - [Data Quality](#data-quality)
  - [Data Lineage](#data-lineage)
  - [Notifications](#notifications)
- [Others](#others)

### Pipeline <a name="pipeline"></a>
A Pipeline is the central component of PORTER that allows users to define the data flow from source to target. 
It allows users to define the list of operations that are performed as part of this pipeline including extraction, transformation, loading, and validation.
Pipelines can be configured using YAML or JSON files, providing flexibility and ease of use.

In PORTER users can define the entire pipeline in one config and run it with a single command. Or if you wish to run individual steps with your own orchestrator of choice you can do that as well, while still keeping all the steps in singe config.

Example: `sample_pipeline.yaml`
```yaml 
name: sample_pipeline
description: A sample data pipeline

# Define all the Connections (sources and targets) used in this pipeline
connections:
  - name: postgres_dev
    secrets: dev/postgres/creds
    secrets_source: aws_sm
  - name: redshift_dev
    secrets: dev/redshift/creds
    secrets_source: aws_sm
    load_all: true

# Define the source for the pipeline, datasets to be extracted for here
source: postgres_dev

# Define the Datasets to be extracted from the source. It can be API/Table/Query/File based on the source type
datasets:
    - name: users
      table: public.users
    - name: departments
      table: public.departments

# Define any pre-validations to be applied on the data after extraction and pre-transformations
pre_validations:
    - name: null_column_check
      exception: 'Null values found in email column'
      args: 
        column: email
        
    - name: integrety check
      sql_query: SELECT COUNT(*) FROM users WHERE department_id NOT IN (SELECT id FROM departments)
      expectation: "source_result == 0"

# Once the extraction is done you can define any pre-transformations to be applied on the extracted data
# you can only applied these pre-transformations on the data that was extracted in this batch. 
pre_transformations:
    - name: add_audit_columns
      sql_query: SELECT *, :audit_id as audit_id, current_localtimestamp() as row_process_dt FROM users

# if you wish to add more validations after pre-transformations you can define them here


# Define the target where the data has to be loaded. You can define multiple targets as well.
# You can also specify if you want to load all datasets or only specific datasets to each target
targets:
    - name: redshift_dev
      load_all: true
    - name: s3_dev
      load_only: 
       - users

# Define any post-transformations to be applied on the data after loading into the target.
# These run on the specified target.
post_transformations:
    - name: finalize_data
      source: redshift_dev
      sql_path: finalize_data.sql
      

# Define any Post validations after loading the data into the target
post_validations:
    - name: row_count_check
      source: redshift_dev
      sql_query: SELECT COUNT(*) FROM users
      expectation: "source_result > 0"     
  
# Define any governance features like audit, data quality, lineage, notifications etc.   
```
With this sample PORTER config users can define a pipeline that extracts data from a Postgres source, applies a pre-transformation to add audit columns, performs a validation to check for null values in the email column, loads the data into a Redshift target, and finally applies a post-transformation to finalize the data.
You can call below command to run all the steps defined in the pipeline config, they will run in the same order that you define in the config. 
```shell
PORTER run --config sample_pipeline.yaml
```
- Or you can also run parts of the config like below
```shell
PORTER run --config sample_pipeline.yaml --steps pre_transformations,pre_validations
```
Obviously extraction will run by default in this case as you have not extracted the data yet. If you specify any `pre_` steps the extraction will be ran by default before running the specified steps.

- If you wish to run only post transformations and post validations you can do that as well.
```shell
PORTER run --config sample_pipeline.yaml --steps post_transformations,post_validations
```
If you specify ONLY `post_` steps, PORTER will assume that the data is already extracted and loaded into the target and will skip extraction and loading steps and run only the transformations or validations.
This is helpful if you have your own orchestrator and want to run only specific steps defined in the PORTER config.

> NOTE: Don`t worry we will cover each of these sections in detail in the following chapters.


### Connections <a name="connections"></a>

Connections in PORTER define the configuration details required to connect to various data sources and targets.
- Connection details should be stored in secure secret management systems like AWS Secrets Manager, HashiCorp Vault etc.
- All details regarding the connection should be set in the secrets, and provide the details of the secret and secret source in the PORTER config.
- You can also create separate configs for connections and pass the config file names in the pipeline config. This is helpful if you reuse this connection details in another pipeline

Examples:
- Assuming you have a secret in Secrets Manager like below with the name `dev/postgres/sales`
```json
{
  "host": "postgres.dev.company.com",
  "port": 5432,
  "database": "sales_db",
  "username": "db_user",
  "password": "secure_password"
}
```
you can define the connection in the PORTER config as below
```yaml
connections:
  - name: postgres_dev
    secrets: dev/postgres/sales
    secrets_source: aws_sm
```
- If you wish to create a separate config for connections you can create a file named `postgres_dev.yaml` like below.
```yaml
- name: postgres_dev
  secrets: dev/postgres/sales
  secrets_source: aws_sm
```
You can also have multiple connections defined in this config file like below
```yaml
- name: postgres_dev
  secrets: dev/postgres/sales
  secrets_source: aws_sm
- name: redshift_dev
  secrets: dev/redshift/creds
  secrets_source: aws_sm
```
Then in the pipeline config you can reference this connection config file as below

```yaml
# PORTER_pipeline.yaml
...
connections_config_files:
  - postgres_dev.yaml
...  
```
This allows you to use the same connection config file `postgres_dev.yaml` in multiple pipeline configs without having to redefine the connection details each time.
This is helpful if you have large number of pipelines dealing with same connections, also if you want to organize these config files separately.

A Complex team folder structure could look like 
```
pipelines/
  ├── sales_pipeline.yaml
  └── marketing_pipeline.yaml
connections/
  ├── dev/
  │   ├── postgres_dev_sales.yaml
  │   ├── postgres_dev_hr.yaml
  │   ├── redshift_dev.yaml
  │   ├── s3_dev.yaml
  │   ├── s3_marketing_dev.yaml
  │   └── s3_quant_dev.yaml
  ├── qa/
  │    ├── postgres_qa.yaml
  │    ├── redshift_qa.yaml
  │    └── s3_qa.yaml
  └── prod/
      ├── postgres_prod.yaml
      ├── redshift_prod.yaml
      └── s3_prod.yaml
```

- You can organize them based on the type of source, like all s3 , postgres etc.
- You can organize them based on the teams, like sales team, marketing team etc. 
- You can organize them based on the environments, like all dev, qa, prod etc.
- YOu can also mix and match

> If you wish to implement your own secrets source lets collaborate!


### Metadata 
- Metadata in PORTER refers to the information about the data being processed, including details about the source, target, datasets, transformations, and validations.
- You can choose supported metadata databases like Postgres, MySQL, SQLite (ONLY for local testing) etc. to store the metadata.
- Connection details for the metadata database can leverage the same connection mechanism as other sources and targets in PORTER.
- User should have access to create/update tables in the metadata database as PORTER will create necessary tables to store the metadata information.
- PORTER will not delete any data in the metadata database so it is individual user`s responsibility to manage the archival and size of the metadata database.

### Source

Source is the origin from where the data is extracted. PORTER supports a wide range of data sources including databases, APIs, file systems, and cloud storage services.
- Any connection from which you can extract data is defined as `Source`
- Only one source can be defined in one PORTER pipeline config.
- Multiple datasets can be extracted from the same source. Look at [Dataset](#dataset) section for more details.
- You can write custom extractors for any source that is not natively supported by PORTER. If you think its useful for the community please contribute it back!


### Target

Target is the destination where the data is loaded after extraction and transformation. PORTER supports various target systems including databases, data warehouses, data lakes, and cloud storage services.
- Any connection to which you can load data is defined as `Target`
- Multiple targets can be defined in one PORTER pipeline config.
- You can choose to load all datasets extracted from the source to the target or only specific datasets. Look at [Dataset](#dataset) section for more details.
- You can write custom loaders for any target that is not natively supported by PORTER. If you think its useful for the community please contribute it back!

### Dataset

Dataset is a logical representation of the data being moved. It can be a table in a database, a file in a file system, or an API response from an endpoint.
- Define one or more datasets to be extracted from the source.
- All datasets defined in the config will be extracted from the source during the extraction phase, and loaded into an engine like Duckdb/Spark so that you can perform any pre-transformations or validations on the extracted data.
- Define a name for each dataset so that you can reference it in the transformations or validations. The name should be unique with in the pipeline config.
- Define the schema for each dataset if you wish to override the schema detected during extraction. This leaves less room for errors due to schema assumptions.
- Get notified if the incoming data doesnt match your expected schema. And you can choose the fail the pipeline or just log a warning (this might have effects downstream if not handled properly).
- All extracted dataset details, and counts are logged in the metadata DB. 
- If the source is of database then you can choose to extract data parallelly based on the number of workers defined in the connection config.
  - This requires a column to be defined for parallel extraction. This column should be numeric or date/time type.
  - PORTER will automatically determine the min and max values for the column and create ranges based on the number of workers defined in the connection config.


Below example are only sample, you can pass many more arguments for each dataset based on the source type. Look at the specific source documentation for more details. 

```yaml
datasets:
  - name: users
    table: public.users
    args:
        num_executors: 4
        split-by: employee_id
```
You can also define a derived `split-by` like below, but the derived column should be able run on the source. 
```yaml
datasets:
  - name: users
    table: public.users
    args:
        num_executors: 4
        split-by: MOD(employee_id, 4)
```


#### Table as a Dataset
- To define a table as a dataset you can specify the table name in the dataset config.
- You can define the type of extraction, if its full refresh or incremental load based on a column.
- Last captured value for the incremental column can be stored in the metadata DB. 


#### Query as a Dataset
- To define a query as a dataset you can specify the sql query in the dataset config.
- This is useful if you want to extract a subset of data from a table or join multiple tables during extraction.
- Multiple ways of passing parameters to the query
  - Static values using `values_to_bind`
  - Dynamic values using `dynamic_input_queries` that run a query on the source or another source to get the value to be passed to the main query.
  - Environment variables using `ENV` as source in `dynamic_input_queries`

Some Examples:

```yaml
datasets:
  
  # Simple query without any parameters
  - name: active_users
    sql_query: SELECT * FROM public.users WHERE status = 'active'
  
  # Query with static parameters  
  - name: sales_data
    sql_query: SELECT * FROM public.sales WHERE sale_date >= :start_date AND sale_date < :end_date
    values_to_bind:
      start_date: '2024-01-01'
      end_date: '2024-02-01'
 
  # Query with dynamic parameters from the same source
  - name: marketing_data
    sql_query: SELECT * FROM public.marketing WHERE extraction_date > :campaigns_max_extraction_date
    dynamic_input_queries:
      - name: campaigns_max_extraction_date
        source: postgres_dev
        sql_query: 'SELECT max(extraction_date) FROM campaigns'
  
  # Query with dynamic parameters from environment variables
  - name: marketing_data
    sql_query: SELECT * FROM public.marketing WHERE extraction_date > :campaigns_max_extraction_date
    dynamic_input_queries:
      - name: campaigns_max_extraction_date
        source: ENV
```


#### File as a Dataset
- Define a file as a dataset, file can be of any type like CSV, JSON, Parquet, Avro etc.
- File can be in any of the supported file systems like local file system, S3, GCS, Azure Blob Storage etc.
- Additional args can be passed to define the file format options like delimiter, header, schema etc.
- All files will be downloaded to local and loaded into the engine like Duckdb/Spark for any pre-transformations or pre-validations.
- Define a file path pattern to load multiple files as a single dataset. Follow glob patterns for defining the file path pattern.

Example
```yaml
datasets:
  - name: sales_data
    file_pattern: /tmp/data/sales/2024/*.csv
    args:
      header: true
      delimiter: ","
```
Incase of S3 you can define the file path as below
```yaml
connections:
  - name: s3_dev
    secrets: dev/s3/creds
    secrets_source: aws_sm
datasets:
  - name: sales_data
    file_prefix: /sales/2024/
    file_suffix: csv
    args:
      header: true
      delimiter: ","
```

#### API response as a Dataset
- Define an API endpoint as a dataset to extract data from RESTful APIs.
- As every API is different you can pass additional args to define the request method, headers, authentication, pagination etc.

#### Streaming as a Dataset
- Define a streaming source like Kafka, Kinesis etc. as a dataset to extract real-time data.
- You can pass additional args to define the topic/stream name, consumer group, offset management etc.
- You can also leverage PORTER`s metadata to store the last processed offset for each partition to ensure exactly-once processing.

### Transformation

Transformations in PORTER allow users to modify and manipulate the data as it moves from source to target.
There are 2 types of transformations that can be defined in PORTER pipeline config depending on what kind of transformations you are running.
PORTER supports only `SQL` based transformations. For anything complex users can use engines of their choice like Spark post loading into the target.

#### Pre Transformations
- These are the transformations that are run right after extracting before loading into the target. 
- These transformations run on the extracted data that is loaded into an engine like Duckdb/Spark.
- You can only use the data that is extracted in this batch for pre-transformations.
- These transformations are useful for data cleansing, data enrichment, data aggregation, adding audit columns etc. before loading into the target.

#### Post Transformations
- These are the transformations that are run right after loading into the target.
- You need to defined the target on which the post transformation has to run.
- Any transformations that requires historical data that is already in the target should be run as post transformations.


If you are using something like [DBT](https://docs.getdbt.com/), can also use along with PORTER for any transformations post loading into the target (Ideally this would be a stage/bronze/temp).

### Validation
These are your DATA QUALITY checks!
- Like transformations PORTER supports 2 types of validations that can be defined in the pipeline config. 
- Validations are SQL based checks that run on the data to ensure data quality and integrity.
- If any validation fails you can choose what action to be taken.

#### Pre Validations
- These are the validations that are run right after extracting and pre-transformations before loading into the target.
- These validations run on the extracted data that is loaded into an engine like Duckdb/Spark.
- You can only use the data that is extracted in this batch for pre-validations.
- These validations are useful for checking null values, data types, referential integrity, uniqueness etc. before loading into the target.

#### Post Validations
- These are the validations that are run right after loading into the target.
- You need to defined the target on which the post validation has to run.
- Any validations that requires historical data that is already in the target should be run as post validations.
- These validations are useful for checking row counts, data consistency, data accuracy etc. after loading into the target.


### Governance
#### Audit
- PORTER maintains an audit trail of below in the metadata
  - Pipeline runs with start time, end time, status etc.
  - Dataset extraction details with row counts etc.
  - Transformation details with status etc.
  - Validation details with status etc.
  - Target load details with row counts etc.

- Logs will not be stored in the metadata DB, they will be printed to console and can be redirected to a file or log management system of your choice using standard output redirection mechanisms.

#### Data Lineage
- PORTER uses open libraries like 
  - [SQL Lineage](https://sqllineage.readthedocs.io/en/latest/) to derive the lineage
  - [OpenLineage](https://openlineage.io/) to emit or visualize the lineage

#### Notifications
- PORTER has a strong opinion about orchestration, it stays out of it. If your orchestrator already have integrations to send notifications of your companies choice you should leverage that.
If you dont have anything already in place you can use PORTER`s notification system to send notifications on things like pipeline success/failure or validation failures/summary via email/Slack etc.
- Leverage PORTER`s connection mechanism to define the authentication or details related to the notification channels.


> If you do not see a notification channel of your choice please collaborate with us to add it!


### Others

1. a
2. b
