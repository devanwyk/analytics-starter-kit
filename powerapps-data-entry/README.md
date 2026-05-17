# Power Apps Data Entry App

This folder contains guidance and a placeholder for a Power Apps canvas app that enables users to enter or edit data which is written directly to an Amazon Redshift table via the Premium connector.

## What the app does

- Connects to a Redshift table (e.g., `analytics.fact_sales`) using the Amazon Redshift Premium connector.
- Displays a gallery of recent records.
- Provides a form to add a new record or edit an existing one.
- On submit, writes the data back to Redshift.
- Optionally, can trigger a Power Automate flow for post-processing.

## Files

- `README.md` – this file.
- `SampleApp/` – folder that would contain the exported `.msapp` file (not included to keep the repo lightweight; you can export from Power Apps and add it here).
- `app-instructions.md` – step‑by‑step instructions to recreate the app from scratch.

## How to create the app (quick steps)

1. **Create a connection to Redshift**
   - In Power Apps Studio, go to **Data** → **Add data source** → **New connection**.
   - Search for **Amazon Redshift** and select the Premium connector.
   - Fill in the cluster endpoint, port, database name, username, and password (or use Azure AD/IAM if configured).
   - Click **Create**.

2. **Add the target table as a data source**
   - After the connection is created, select it and choose the table you wish to expose (e.g., `analytics.fact_sales`).
   - The table will appear under the Data pane.

3. **Build the screen**
   - Insert a **Vertical Gallery** control.
   - Set its `Items` property to `RedshiftTable` (replace with your table name).
   - Inside the gallery, add labels to show fields like `sale_id`, `order_date`, `sales_amount`.
   - Insert a **Form** control (Edit form) and set its `DataSource` to `RedshiftTable`.
   - Add the fields you want editable to the form.
   - Insert a **Button** labeled "Save".
   - Set the button's `OnSelect` property to:
     ```
     SubmitForm(EditForm1);
     Refresh(RedshiftTable);
     ```
   - Optionally, add a "New" button that calls `NewForm(EditForm1)` and navigates to a blank form.

4. **Save, publish, and share**
   - Give the app a meaningful name (e.g., "Sales Data Entry").
   - Publish to your environment and share with the intended users or security groups.

5. **Optional: Add Power Automate trigger**
   - You can add a flow that runs on item submission (using Power Apps trigger) to perform additional logic such as sending notifications or updating a data warehouse.

## Extending the app

- Add multiple screens for master‑detail (e.g., select a customer then see their orders).
- Use variables or collections to cache data for offline‑friendly experiences.
- Implement business rules with `If`, `Patch`, or `Collect` functions.
- Use the Power Apps Component Framework (PCF) for custom controls if needed.

## Sample data

If you wish to test with dummy data before connecting to Redshift, you can create a local collection:

```powerapps
ClearCollect(
    LocalSales,
    {
        sale_id: 1,
        order_date: Today(),
        product_key: 101,
        customer_key: 2001,
        quantity: 2,
        sales_amount: 150.00,
        discount_amount: 0.00
    }
)
```

Then set the gallery's `Items` to `LocalSales` for testing, and switch back to `RedshiftTable` when ready.

## License

Feel free to reuse and adapt this guidance for your own projects.
