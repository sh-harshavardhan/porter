# ApiDataset

Dataset model for api-based datasets.

### Required Fields


- name


### Parameters:

| Name | Type | Required | Description |
|-----|------|----------|-------------|
| name | string | Yes | The name of the dataset </br></br> Examples :</br> <pre>- employee_data<br>- sales_data_2023<br></pre>  |
| columns | array | No | If you want to specify the schema of the incoming dataset do so or else it will be inferred for you based on the engine you use.Also remember to use the datatype that the engine you use understands.Example: Use 'str' if you are using pandas, 'STRING' if you are using DuckDB/Spark, etc. </br></br> Examples :</br> <pre>- datatype: INTEGER<br>  name: id<br>- datatype: STRING<br>  name: name<br>- datatype: STRING<br>  name: email<br>- datatype: DATE<br>  name: start_date<br>- datatype: DATE<br>  name: end_date<br>- datatype: STRING<br>  name: department<br>- datatype: DECIMAL(20,2)<br>  name: salary<br></pre>  |
| on_dataset_missing |  | No | Action to take when the dataset is missing.  |
| metadata | object | No | Metadata for the dataset. By default includes the name of the dataset you dont have to pass it </br></br> Examples :</br> <pre>- owner: John Doe<br>  project: sales_analysis<br></pre>  |
| args | object | No | Additional arguments for fetching the dataset. These are source specific arguments. Read th documentation for each source to know the list of arguments that it accepts  |
| url | string | No | API endpoint to fetch data from source, which becomes a dataset  |
| auth_url |  | No | Authentication URL to get access token if required  |
