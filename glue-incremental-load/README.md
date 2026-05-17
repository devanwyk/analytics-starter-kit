# Glue Incremental Load Template

A reusable AWS Glue PySpark script that performs an incremental load from a source (e.g., an S3 folder of CSV files or a SQL Server table via JDBC) into an Amazon Redshift target table using a watermark column (e.g., `last_updated_ts`).

## What it does

- Reads job parameters: source connection info, source query or path, target table, watermark column, IAM role for Redshift, temporary S3 path for Redshift COPY/UNLOAD.
- Reads the maximum watermark value from the target table (if any) to determine the starting point.
- Extracts new/changed records from the source where the watermark column > last watermark.
- Writes the increment to a temporary S3 location in Parquet/CSV format.
- Uses the Redshift JDBC connector (or Spark-Redshift connector via spark-redshift package) to COPY the data into the target table.
- Updates the watermark table (or could rely on target's MAX) for the next run.

## Files

- `glue_incremental_load.py` – main PySpark script.
- `job_parameters.json` – example of parameters you would pass when creating the Glue job.
- `README.md` – this file.
- `requirements.txt` – optional Python packages (if you want to test locally with `pyspark`).

## How to use (AWS Glue)

1. Upload the script to S3 or provide directly when creating the Glue job.
2. Set up the following parameters (key-value pairs) in the Glue job configuration:
   - `SOURCE_TYPE`: `jdbc` or `s3`
   - For JDBC:
     - `JDBC_CONNECTION_NAME`: name of the Glue connection configured for your SQL Server (or other source).
     - `SOURCE_TABLE` or `SOURCE_QUERY`: the table or SQL query to extract data.
   - For S3:
     - `S3_SOURCE_PATH`: s3://bucket/path/
     - `S3_SOURCE_FORMAT`: `csv` or `parquet`
   - `TARGET_REDSHIFT_JDBC_URL`: JDBC URL for Redshift (include IAM authentication if used).
   - `TARGET_TABLE`: fully qualified target table (e.g., `analytics.fact_sales`).
   - `WATERMARK_COLUMN`: column name used for incremental detection (e.g., `last_updated_ts`).
   - `TEMP_S3_DIR`: S3 path for temporary data (must be writable by the Glue role).
   - `IAM_ROLE_FOR_REDSHIFT`: (optional) if using IAM authentication for Redshift.
   - `DELETE_TEMP_FILES`: `true` or `false` (default true).
3. Ensure the Glue role has permissions to:
   - Read from the source (S3 or JDBC).
   - Write to the temporary S3 directory.
   - Access Redshift via JDBC/IAM.
   - Access Glue catalog, CloudWatch logs.
4. Create a trigger (on-demand, schedule, or event-based) to run the job as needed.
5. After each run, check the job output for the number of records processed and the new watermark value.

## Extending / Customizing

- Add support for multiple watermark columns (composite key).
- Add data quality checks (e.g., row counts, null checks) before writing to Redshift.
- Use Spark-Redshift package (`com.databricks:spark-redshift`) for more robust unload/load.
- Implement slowly changing dimension (SCD) type 2 logic if needed.

## Sample job_parameters.json

```json
{
  "SOURCE_TYPE": "jdbc",
  "JDBC_CONNECTION_NAME": "sqlserver-prod",
  "SOURCE_QUERY": "SELECT SaleID, OrderDate, ProductKey, CustomerKey, Quantity, SalesAmount, DiscountAmount, LastUpdatedTS FROM dbo.FactSales",
  "TARGET_REDSHIFT_JDBC_URL": "jdbc:redshift://mycluster.abc123.us-east-1.redshift.amazonaws.com:5439/dev?user=etl_user&password=******",
  "TARGET_TABLE": "analytics.fact_sales",
  "WATERMARK_COLUMN": "LastUpdatedTS",
  "TEMP_S3_DIR": "s3://my-analytics-bucket/temp/glue_incremental/",
  "IAM_ROLE_FOR_REDSHIFT": "arn:aws:iam::123456789012:role/GlueRedshiftAccess",
  "DELETE_TEMP_FILES": "true"
}
```

## Local testing (optional)

If you have a local Spark setup, you can install the dependencies in `requirements.txt` and run the script with `spark-submit` after adjusting the parameters to point to local test data.
