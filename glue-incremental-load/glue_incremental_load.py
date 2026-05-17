import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F

## @params: [JOB_NAME, SOURCE_TYPE, JDBC_CONNECTION_NAME, SOURCE_QUERY, S3_SOURCE_PATH, S3_SOURCE_FORMAT,
##          TARGET_REDSHIFT_JDBC_URL, TARGET_TABLE, WATERMARK_COLUMN, TEMP_S3_DIR, IAM_ROLE_FOR_REDSHIFT, DELETE_TEMP_FILES]

args = getResolvedOptions(sys.argv, [
    'JOB_NAME',
    'SOURCE_TYPE',
    'JDBC_CONNECTION_NAME',
    'SOURCE_QUERY',
    'S3_SOURCE_PATH',
    'S3_SOURCE_FORMAT',
    'TARGET_REDSHIFT_JDBC_URL',
    'TARGET_TABLE',
    'WATERMARK_COLUMN',
    'TEMP_S3_DIR',
    'IAM_ROLE_FOR_REDSHIFT',
    'DELETE_TEMP_FILES'
])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

def get_max_watermark(jdbc_url, table, watermark_col):
    # Query to get max watermark; we assume the JDBC URL contains user/password or uses IAM.
    query = f"(SELECT COALESCE(MAX({watermark_col}), CAST('1900-01-01' AS TIMESTAMP)) AS max_wm FROM {table}) AS wm"
    df = spark.read.format("jdbc") \
        .option("url", jdbc_url) \
        .option("dbtable", query) \
        .load()
    row = df.collect()[0]
    return row['max_wm']

# Read source
if args['SOURCE_TYPE'] == 'jdbc':
    # For demo, we assume the source query is a table name or a subquery.
    # In practice, you would retrieve connection details from Glue connection.
    source_df = spark.read.format("jdbc") \
        .option("url", args['JDBC_CONNECTION_NAME']) \
        .option("dbtable", f"({args['SOURCE_QUERY']}) AS src") \
        .load()
elif args['SOURCE_TYPE'] == 's3':
    if args['S3_SOURCE_FORMAT'] == 'csv':
        source_df = spark.read.option("header", "true").csv(args['S3_SOURCE_PATH'])
    elif args['S3_SOURCE_FORMAT'] == 'parquet':
        source_df = spark.read.parquet(args['S3_SOURCE_PATH'])
    else:
        raise ValueError("Unsupported S3 source format: " + args['S3_SOURCE_FORMAT'])
else:
    raise ValueError("SOURCE_TYPE must be 'jdbc' or 's3'")

# Get watermark from target
max_watermark = get_max_watermark(args['TARGET_REDSHIFT_JDBC_URL'], args['TARGET_TABLE'], args['WATERMARK_COLUMN'])
print(f"Maximum watermark in target: {max_watermark}")

# Filter incremental
incremental_df = source_df.where(F.col(args['WATERMARK_COLUMN']) > F.lit(max_watermark))
count = incremental_df.count()
print(f"New/updated records to load: {count}")

if count > 0:
    # Write to temporary S3 location in Parquet format
    incremental_df.write.mode("overwrite").parquet(args['TEMP_S3_DIR'])
    
    # Use Redshift COPY from S3 via JDBC statement.
    # Build the COPY command. Assuming IAM role is provided via jdbc URL or separate.
    copy_sql = f"""
        COPY {args['TARGET_TABLE']}
        FROM '{args['TEMP_S3_DIR']}'
        IAM_ROLE '{args['IAM_ROLE_FOR_REDSHIFT']}'
        FORMAT AS PARQUET;
    """
    # Execute the COPY statement via JDBC
    spark.read.format("jdbc") \
        .option("url", args['TARGET_REDSHIFT_JDBC_URL']) \
        .option("dbtable", f"({copy_sql}) AS copy_result") \
        .load()
    print("COPY command executed.")
else:
    print("No new records to process.")

job.commit()