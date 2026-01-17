# FileDataset 

Dataset model for file-based datasets.
Files in the path matching the prefix and suffix will be included in the dataset.
Example: /path/to/data/prefix_*.csv

### Required Fields


- name

- file_path


### Parameters:

| Name | Type | Required | Description |
|-----|------|----------|-------------|
| name | string | Yes | The name of the dataset </br></br> Examples :</br> <pre>- employee_data<br>- sales_data_2023<br></pre>  | 
| columns | array | No | If you want to specify the schema of the incoming dataset do so or else it will be inferred for you based on the engine you use.Also remember to use the datatype that the engine you use understands.Example: Use 'str' if you are using pandas, 'STRING' if you are using DuckDB/Spark, etc. </br></br> Examples :</br> <pre>- datatype: INTEGER<br>  name: id<br>- datatype: STRING<br>  name: name<br>- datatype: STRING<br>  name: email<br>- datatype: DATE<br>  name: start_date<br>- datatype: DATE<br>  name: end_date<br>- datatype: STRING<br>  name: department<br>- datatype: DECIMAL(20,2)<br>  name: salary<br></pre>  | 
| metadata | object | No | Metadata for the dataset. By default includes the name of the dataset you dont have to pass it </br></br> Examples :</br> <pre>- owner: John Doe<br>  project: sales_analysis<br></pre>  | 
| file_path | string | Yes | The file path of the dataset.  | 
| file_prefix |  | No | The file prefix of the dataset.  | 
| file_suffix |  | No | The file suffix of the dataset.  | 
| is_partitioned |  | No | Indicates if the dataset is partitioned with subdirectories.  | 
| args |  | No | N/A  | 
