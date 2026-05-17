# App Recreation Instructions

These instructions assume you have already created an Amazon Redshift Premium connector in Power Apps.

## Step 1: Create the Connection (if not already done)
1. In Power Apps Studio, select **Data** from the left pane.
2. Click **+ Add data source**.
3. Click **+ New connection**.
4. Search for **Amazon Redshift** and select the Premium connector.
5. Enter your Redshift connection details:
   - **Server**: `<your-cluster>.abc123.us-east-1.redshift.amazonaws.com`
   - **Port**: `5439`
   - **Database**: `<your_database>`
   - **Username**: `<your_username>`
   - **Password**: `<your_password>`
   - (Optional) Use Azure AD or IAM authentication if configured.
6. Click **Create**.

## Step 2: Add the Target Table as a Data Source
1. After the connection appears under Data, click it to expand.
2. Select the table you want to expose (e.g., `analytics.fact_sales`).
3. Click **Connect**. The table will now appear as a data source.

## Step 3: Build the User Interface
### 3.1 Gallery for Listing Records
1. From the **Insert** tab, choose **Gallery** → **Vertical**.
2. Set the gallery's **Items** property to:
   ```
   RedshiftTable   // replace with your actual table name
   ```
3. Inside the gallery, insert **Label** controls to display fields.
   - For each label, set the **Text** property to the corresponding field, e.g.:
     - `ThisItem.sale_id`
     - `ThisItem.order_date`
     - `ThisItem.sales_amount`
   - Arrange the labels as desired (e.g., three columns).

### 3.2 Form for Adding/Editing Records
1. From the **Insert** tab, choose **Forms** → **Edit form**.
2. With the form selected, set the **DataSource** property to your Redshift table (e.g., `RedshiftTable`).
3. The form will automatically generate fields based on the table's columns.
   - You can remove fields you don't want editable by selecting the field card and pressing Delete.
   - To reorder, drag the field cards within the form.
4. Position the form to the right of or below the gallery, depending on your layout preference.

### 3.3 Action Buttons
1. Insert a **Button** below the form (or wherever you prefer).
   - Set the **Text** property to `Save`.
   - Set the **OnSelect** property to:
     ```
     SubmitForm(EditForm1);
     Refresh(RedshiftTable);
     Notify("Record saved.", NotificationType.Success);
     ```
2. Insert another button for creating a new record.
   - Set **Text** to `New`.
   - Set **OnSelect** to:
     ```
     NewForm(EditForm1);
     // Optional: navigate to a blank screen or reset the form
     ```
3. (Optional) Add a **Delete** button inside the gallery:
   - Insert a button inside the gallery (e.g., at the end of each row).
   - Set **Text** to `Del`.
   - Set **OnSelect** to:
     ```
     Remove(RedshiftTable, ThisItem);
     Notify("Record deleted.", NotificationType.Warning);
     ```

## Step 4: Save, Publish, and Share
1. Click **File** → **Save** to save your app to the cloud.
2. Give the app a descriptive name (e.g., `Sales Data Entry`).
3. Click **File** → **Publish** to publish the latest version.
4. Click **Share** to share the app with users or groups in your organization.
   - Set permissions as needed (User can use, Co‑owner, etc.).

## Step 5: Testing
1. Open the app in Power Apps Mobile or in a browser.
2. Verify that the gallery shows existing records from Redshift.
3. Click **New** to create a record, fill in the form, and click **Save**.
4. Confirm the new record appears in the gallery and that the underlying Redshift table has been updated (you can query Redshift directly).

## Troubleshooting
- **Connection errors**: Double-check the Redshift connection credentials and ensure the connector has network access to your cluster (security groups, VPC, etc.).
- **Permission issues**: The Redshift user must have INSERT/UPDATE/DELETE permissions on the target table.
- **Delegation warnings**: If you notice a delegation warning on the gallery, consider reducing the data volume or using views to limit the rows returned, as Power Apps may not delegate certain functions to Redshift.
- **Performance**: For large tables, consider adding a search box or filters to limit the gallery's initial load.

## License
Feel free to reuse and adapt these instructions for your own projects.
