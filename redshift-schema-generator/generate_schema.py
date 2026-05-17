#!/usr/bin/env python3
"""
Redshift Schema Generator
Reads schema_def.yaml and emits Redshift DDL using Jinja2 template.
"""

import yaml
from jinja2 import Environment, FileSystemLoader
import os
import sys

def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def render_template(template_dir, template_name, context):
    env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(template_name)
    return template.render(**context)

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(base_dir, 'schema_def.yaml')
    template_dir = os.path.join(base_dir, 'templates')
    output_path = os.path.join(base_dir, 'generated_schema.sql')

    if not os.path.exists(schema_path):
        print(f"Schema definition not found: {schema_path}")
        sys.exit(1)

    schema_data = load_yaml(schema_path)

    # Ensure required top-level keys
    if 'name' not in schema_data or 'tables' not in schema_data:
        print("schema_def.yaml must contain 'name' (schema name) and 'tables' list.")
        sys.exit(1)

    schema_name = schema_data['name']
    tables = schema_data['tables']

    # Render each table
    table_sqls = []
    for table in tables:
        table_ctx = {
            'schema_name': schema_name,
            'table_name': table['name'],
            'columns': table['columns'],
            'diststyle': table.get('diststyle', 'EVEN'),
            'sortkey': table.get('sortkey', []),
        }
        table_sql = render_template(template_dir, 'create_table.sql.j2', table_ctx)
        table_sqls.append(table_sql)

    # Compose full DDL
    ddl_parts = [
        f"-- Generated Redshift schema for schema: {schema_name}",
        f"CREATE SCHEMA IF NOT EXISTS {schema_name};",
        ""
    ]
    ddl_parts.extend(table_sqls)

    final_sql = "\n\n".join(ddl_parts)

    with open(output_path, 'w') as f:
        f.write(final_sql)

    print(f"Generated DDL written to: {output_path}")

if __name__ == '__main__':
    main()