# Connecting Power Automate to Amazon Redshift

This guide shows how to set up the Amazon Redshift Premium connector in Power Automate and use it in a flow.

## Prerequisites

- An active Power Automate license that includes access to premium connectors.
- Access to an Amazon Redshift cluster with network access allowed from the Power Automate service (you may need to add the Power Automate IP ranges to your cluster's security group/firewall).
- A Redshift user with at least SELECT permissions on the tables/views you intend to query.

## Step‑by‑step

1. **Open Power Automate**
   - Go to https://flow.microsoft.com and sign in with your work or school account.

2. **Create a new connection to Redshift**
   - In the left navigation pane, select **Data** → **Connections** → **+ New connection**.
   - Search for **Amazon Redshift** and select the connector labeled **(Premium)**.
   - Fill in the connection details:
     - **Connection name**: a friendly name, e.g., `Redshift-Prod`.
     - **Server**: the Redshift cluster endpoint (e.g., `mycluster.abc123.us-east-1.redshift.amazonaws.com`).
     - **Port**: `5439` (default).
     - **Database**: the database name.
     - **Username**: your Redshift username.
     - **Password**: the corresponding password.
     - (Optional) If you use Azure AD or IAM authentication, choose the appropriate option and provide the required details (e.g., IAM role ARN).
   - Click **Create**. The connector should show as **Connected**.

3. **Use the connector in a flow**
   - When creating or editing a flow, add a new step and search for **Amazon Redshift**.
   - Choose the action **Execute a query** (or **Stored procedure** if you prefer).
   - In the action, select the connection you just created from the dropdown.
   - Enter your SQL statement in the **Query** box. You can use dynamic content from previous steps.
   - Note: The connector returns a result set; you may need to use **Parse JSON** to extract scalar values or rows.

4. **Handling the result**
   - The output of **Execute a query** is an object with a `resultSets` array.
   - Example to get a single scalar value:
     - Add a **Parse JSON** action.
     - Set **Content** to the output of the Redshift action.
     - Use a schema like:
       ```json
       {
         "type": "object",
         "properties": {
           "resultSets": {
             "type": "array",
             "items": {
               "type": "object",
               "properties": {
                 "rows": {
                   "type": "array",
                   "items": {
                     "type": "array"
                   }
                 }
               }
             }
           }
         }
       }
       ```
     - Then reference `body('Parse_JSON')?['resultSets']?[0]?['rows']?[0]?[0]` to get the first cell.
   - For returning multiple rows, you can use **Create CSV table** or **Select** to shape the data.

5. **Testing the connection**
   - Use a simple query like `SELECT 1 AS test;` to verify the connection works.
   - Check the run history for any errors; common issues are network/security group mismatches or incorrect credentials.

6. **Best practices**
   - Keep queries as efficient as possible; Redshift charges for data scanned.
   - Consider using views or materialized views to simplify complex logic.
   - Avoid using `SELECT *`; list only the columns you need.
   - If you need to write data back to Redshift, you can use the same connector with an `INSERT`, `UPDATE`, or `DELETE` statement, or use the **Redshift Bulk Copy** via COPY from S3 (more efficient for large loads).

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `Unable to connect to the server` | Network blockage (security group, NACL, VPC) | Add the Power Automate outbound IP ranges (published by Microsoft) to your Redshift security group. |
| `Authentication failed` | Wrong username/password or missing IAM role | Double‑check credentials; if using IAM, ensure the role has `redshift:GetClusterCredentials` and the JDBC URL is formed correctly. |
| `Query exceeded timeout` | Query too long or returning too many rows | Add `LIMIT` or tighten WHERE clauses; consider using UNLOAD to S3 for large result sets. |
| `Premium connector not available` | License does not include premium | Verify your plan or ask your admin to assign a license with Power Automate per‑user plan that includes premium connectors. |

## Reference
- Official docs: https://powerautomate.microsoft.com/en-us/connectors/details/shared_amazonredshift/
- Microsoft IP ranges: https://www.microsoft.com/en-us/download/details.aspx?id=56519

Feel free to adapt these steps for your own environment.
