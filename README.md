# Analytics Modernisation Starter Kit

This repository contains a reusable set of assets to help you quickly deliver analytics solutions that combine:

- **AWS Redshift** (data warehousing)
- **Microsoft Power Platform** (Power Apps, Power Automate, Power BI)
- **Optional ETL/ELT** (AWS Glue, AWS DMS, dbt, etc.)

## Folder structure

```
redshift/
├── glue_scripts/          # AWS Glue PySpark/SQL scripts for ETL
└── dms/                   # AWS DMS task definitions & CSV mapping (if using DMS)

powerbi/
└── reports/               # Sample .pbix files or PBITS templates

powerapps/
└─ SampleApp/              # Power Apps canvas app source (MSApp files) or instructions

powerautomate/
   # Sample flows (JSON definitions) or export .zip
```

## How to use

1. Clone this repo to your workstation.
2. Customize the Redshift target schema (see `redshift/glue_scripts/create_target_schema.sql`).
3. Run the Glue jobs to migrate/transform your source data into Redshift.
4. Connect Power BI to the Redshift tables using the Amazon Redshift connector.
5. Build or import the Power Apps canvas app to enable manual data entry or record updates.
6. Use Power Automate to trigger data refreshes, send alerts, or orchestrate complex workflows.
7. Document any custom connectors or gateway setups required for on-prem data sources.

## Typical deliverables (for a freelance pilot)

- Redshift target schema + validated data load (Glue/DMS scripts)
- Power BI dataset + 2‑3 core reports (.pbix)
- Power Apps canvas app (MSApp) + optional custom connector
- Power Automate flow(s) for refresh/alert
- 2‑hour knowledge‑transfer session (recording + slides)

## License

MIT – feel free to adapt and reuse for client work.
