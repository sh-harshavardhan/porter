# FileDataset

Dataset model for file-based datasets.
Files in the path matching the prefix and suffix will be included in the dataset.
Example: /path/to/data/prefix_*.csv

### Required Fields


- name

- file_path

- file_type


### Parameters:

| Name | Type | Required | Description |
|-----|------|----------|-------------|
| name | string | Yes | The name of the dataset </br></br> Examples :</br> <pre>- employee_data<br>- sales_data_2023<br></pre>  |
| columns | array | No | If you want to specify the schema of the incoming dataset do so or else it will be inferred for you based on the engine you use.Also remember to use the datatype that the engine you use understands.Example: Use 'str' if you are using pandas, 'STRING' if you are using DuckDB/Spark, etc. </br></br> Examples :</br> <pre>- datatype: INTEGER<br>  name: id<br>- datatype: STRING<br>  name: name<br>- datatype: STRING<br>  name: email<br>- datatype: DATE<br>  name: start_date<br>- datatype: DATE<br>  name: end_date<br>- datatype: STRING<br>  name: department<br>- datatype: DECIMAL(20,2)<br>  name: salary<br></pre>  |
| on_dataset_missing |  | No | Action to take when the dataset is missing.  |
| metadata | object | No | Metadata for the dataset. By default includes the name of the dataset you dont have to pass it </br></br> Examples :</br> <pre>- owner: John Doe<br>  project: sales_analysis<br></pre>  |
| args | object | No | Additional arguments for fetching the dataset. These are source specific arguments. Read th documentation for each source to know the list of arguments that it accepts  |
| file_path | string | Yes | The file path of the dataset.  |
| file_type |  | Yes | Type of the file. </br></br> Examples :</br> <pre>- csv<br>- json<br>- parquet<br>- excel<br>- xml<br>- fixed_width<br>- avro<br>- orc<br>- custom<br></pre>  |
| engine |  | No | Which Engine to use to read the file, By default PANDAS is used </br></br> Examples :</br> <pre>- duckdb<br>- spark<br>- pandas<br>- pyarrow<br></pre>  |
| file_pattern |  | No | The file pattern, Uses glob patterning.
                    By default all the files under `file_path` will be processed.
                    Also if either `file_prefix` or `file_suffix` they take precedence.
                     </br></br> Examples :</br> <pre>- DB_FILE_*.csv<br>- sales_data_*.json<br>- EMP_REC_*_PART_*_.parquet<br></pre>  |
| file_prefix |  | No | The file prefix of the dataset, use this if the source cannot handle glob patterns. </br></br> Examples :</br> <pre>- /source_data/DB_FILE_<br>- sales_data_<br>- EMP_REC_<br></pre>  |
| file_suffix |  | No | The file suffix of the dataset, this will be added at the end of the file pattern. Use this if the source cannot handle glob patterns. </br></br> Examples :</br> <pre>- .csv<br>- .json<br>- .parquet<br></pre>  |
| is_partitioned |  | No | Indicates if the dataset is partitioned with subdirectories.  |
