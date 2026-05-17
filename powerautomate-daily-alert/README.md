# Power Automate Daily Alert Flow

This folder contains a sample Power Automate cloud flow that runs on a schedule (e.g., each morning), queries an Amazon Redshift table for a key metric, evaluates a threshold, and sends a notification (email, Teams, etc.) if the condition is met.

## What the flow does

1. **Trigger** – Recurrence (e.g., every day at 08:00 AM).
2. **Action** – Execute a SQL query against Amazon Redshift using the Premium connector.
   - Example query:  
     ```sql
     SELECT SUM(sales_amount) AS daily_sales
     FROM analytics.fact_sales
     WHERE order_date = CURRENT_DATE;
     ```
3. **Action** – Parse the query result (single value).
4. **Condition** – Check if the metric is below/above a defined threshold (or matches a business rule).
5. **If yes** – Send an notification:
   - Send an email (Outlook, Gmail)  
   - Post a message to a Microsoft Teams channel  
   - Send a mobile push notification  
   - (Optional) Call an approval process or create a Planner task.
6. **If no** – (Optional) log that everything is OK or do nothing.

## Files

- `README.md` – this file.
- `sample_flow.json` – an exported flow definition (you can import this into Power Automate and then adjust connections/parameters).
- `connection-guide.md` – short steps to create the Redshift Premium connector and configure the flow.

## How to use the sample

1. Import `sample_flow.json` into Power Automate:
   - In Power Automate, click **Import** → **Upload** → select the file.
   - During import, you will be prompted to create or select connections:
     - **Amazon Redshift** (Premium connector) – provide your cluster endpoint, port, database, username/password or use Azure AD/IAM.
     - **Outlook** (or whichever email/messaging connector you choose for notifications).
   - Complete the import.
2. Open the flow for editing:
   - Review the recurrence trigger time‑zone and frequency.
   - Edit the SQL query in the **Redshift – Execute a query** action to match your table and metric.
   - Adjust the threshold in the condition.
   - Choose your preferred notification action and fill in the details (recipient, subject, message body).
3. Save and test the flow using the **Test** button (manually or with sample data).
4. Once satisfied, turn the flow on.

## Extending / Customizing

- Use multiple queries in parallel (e.g., sales, returns, inventory) and combine results in a single message.
- Add approval steps before sending notifications.
- Write the result to a SharePoint list or Power BI dataset for historical tracking.
- Use the **HTTP** action to call a custom API if you need to integrate with other systems.
- Add error handling (configure run after) to notify on failures.

## Sample flow definition (json) – overview

The exported JSON contains the following high‑level structure:
- **definition.triggers**: recurrence.
- **definition.actions**:
  - `Redshift.ExecuteQuery`: runs the SQL.
  - `ParseJSON`: extracts the scalar result.
  - `Condition`: compares the result to a threshold.
  - If true: `Office365Outlook.SendEmail` (or Teams.PostMessage).
  - If false: optionally a `Compose` action logging “All good”.

You can view the detailed actions after import.

## License
Feel free to reuse and adapt this flow for your own projects.
