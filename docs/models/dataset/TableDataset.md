# TableDataset

Dataset model for Table-based datasets.

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
| query | string | No | Source query to fetch data from source, which becomes a dataset </br></br> Examples :</br> <pre>- SELECT * FROM employees WHERE department = :department<br>- SELECT id, name, sales_amount FROM sales_data_2023 WHERE region = :region<br></pre>  |
| table |  | No | Source table name to fetch data from source, which becomes a dataset </br></br> Examples :</br> <pre>- employees<br>- sales_data_2023<br></pre>  |
| values_to_bind |  | No | If the query has placeholders, this dictionary contains the values to bind to the placeholders </br></br> Examples :</br> <pre>- department: Engineering<br>- region: North America<br></pre>  |
| dynamic_input_queries |  | No | List of dynamic input query details, each dictionary should contain
        name: The name of the dynamic input parameter, this will be used as a placeholder in the main query.
        query: Query that returns the value for the dynamic input parameter.
        source: Name of the source on which the dynamic input query has to be executed,
                Note : make sure that this source is defined in the pipeline config. </br></br> Examples :</br> <pre>- - name: employee_extraction_date<br>    query: SELECT MAX(extraction_date) FROM employees<br>    source: hr_database<br>  - name: sales_extraction_date<br>    query: SELECT MAX(extraction_date) FROM sales_data_2023<br>    source: sales_database<br></pre>  |
