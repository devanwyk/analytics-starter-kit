# Redshift Schema Generator

A small Python utility that converts a simple YAML schema definition into ready-to-run Amazon Redshift DDL (CREATE SCHEMA, CREATE TABLE, ALTER TABLE … ADD CONSTRAINT).

## What it does

- Reads `schema_def.yaml` describing tables, columns, data types, nullable, primary keys, foreign keys, and sort/dist styles.
- Uses a Jinja2 template to produce `generated_schema.sql`.
- Supports basic data type mapping (e.g., `string` → `VARCHAR(255)`, `integer` → `INTEGER`, `decimal(p,s)` → `DECIMAL(p,s)`, `date` → `DATE`, `timestamp` → `TIMESTAMP`).
- Can be extended to include Redshift-specific options like `DISTSTYLE`, `SORTKEY`, `ENCODE`.

## Files

- `schema_def.yaml` – example schema definition (sales star schema).
- `generate_schema.py` – main script.
- `templates/create_table.sql.j2` – Jinja2 template for a single table.
- `generated_schema.sql` – example output produced from the sample definition.
- `requirements.txt` – Python dependencies (Jinja2, PyYAML).

## How to use

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Edit `schema_def.yaml` to match your source model.
3. Run the generator:
   ```bash
   python generate_schema.py
   ```
4. Review `generated_schema.sql` and execute it against your Redshift cluster (via psql, AWS Data API, or any SQL client).

## Extending

- Add more Jinja2 blocks for distribution style, sort keys, column encoding.
- Add support for `VIEW` or `MATERIALIZED VIEW` generation.
- Integrate into a CI/CD pipeline to keep schema in sync with a model repository.
