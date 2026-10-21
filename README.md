# Pinteresty Outfits Business Desk

A Flask and SQLite app for a clothing and accessories shop. It can run locally on Windows or be deployed as a password-protected web app on Render. Local data stays in the project’s `instance/data` folder; the Render deployment stores data on its persistent disk.

## Windows setup

1. Install Python 3.11–3.13 from python.org and enable the Python launcher.
2. Double-click `run.bat`. The first run creates `.venv`, installs Flask, Pillow, and openpyxl, then starts the app.
3. Open http://127.0.0.1:5000. Close the command window to stop the server.
4. Data is stored in `instance/data`: `business.sqlite3`, `product_images`, and `backups`.

Manual PowerShell setup:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run.py
```

## Main workflows

Add products and customers from their pages. Product photos are validated and converted to local JPEGs. Search products by name or SKU and filter by category. Edit product or customer records from their lists. A customer can have a purchase history and outstanding balance; guest sales are supported.

Use New Sale to add multiple products, quantities and per-sale unit prices. The app checks stock and saves the sale, price/cost/category snapshots, and stock changes in one transaction. Discounts and paid amounts are validated. Open Sales History to filter by date or customer/name/phone/ID, record later payments, update sale contact details, or void a sale. Voiding restores stock and retains the sale record; it does not erase payment or refund history.

## Financial definitions

Gross sales are sum of quantity × saved item selling price before discounts. Net sales equal gross sales less order discounts. COGS equals quantity × saved item cost. Gross profit equals net sales less COGS. Payments received are the payments dated in the selected period, separate from revenue. Monthly outstanding is the current unpaid balance on active orders created in that month. These figures exclude overhead and operating expenses.

The dashboard shows today’s sales and date-range totals. Monthly Reports shows gross sales, discounts, net sales, COGS, gross profit, cash received by payment date, current outstanding on that month’s orders, order count, units, average order value, daily totals, category sales, payment-method receipts, and best sellers. Monthly Excel exports include summary, sales detail, category, and payment-method sheets. Sales and detailed-item exports accept a date range; inventory, customer, and outstanding exports contain current database records.

## Backup and restore

Use Backup & Restore to make a ZIP of the database and product images. Copy ZIPs to a separate drive. Restore checks archive paths and SQLite integrity, then creates a safety backup of the current files before replacing the database and images. Stop any other running copy of the app before restoring, and restart the app afterward.

## Testing

After installing requirements, run:

```powershell
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Tests cover multiple line totals and discounts, historical price/cost snapshots, stock checks and restoration, payments, product search and photo handling, monthly reporting, valid `.xlsx` output, and backup/restore. Python compilation and SQLite schema initialization were checked during implementation. The application tests pass in the project virtual environment.

## Deploy from GitHub to Render

GitHub stores the source code; it does not run this Flask app. The included `render.yaml` configures a Render web service with a persistent disk and HTTP Basic Authentication. The service plan with a persistent disk is paid. Render free web services have temporary local storage, which would lose the SQLite database and uploaded images when the service restarts.

1. Push the project to a GitHub repository.
2. In Render, create a Blueprint and connect that GitHub repository. Render reads `render.yaml` and prompts for `APP_USERNAME` and `APP_PASSWORD`; set both to strong values and keep them private.
3. Wait for the first deploy to finish. Render provides an `onrender.com` web address. Open it and sign in with the username and password you configured.
4. To move your existing local data, create a ZIP from **Backup & Restore** in the local app. After signing in to the deployed app, upload that ZIP on its **Backup & Restore** page, then restart the service from Render.
5. Later, push commits to the connected GitHub branch; Render will deploy them automatically.

Keep the GitHub repository private if it contains business code you do not want to share. Do not commit the local SQLite database, customer information, product photos, or backup ZIPs. Keep Render credentials private. The hosted database and uploaded photos persist on Render’s disk; download backups regularly and store them somewhere separate.

Sale line items and discounts cannot be edited in place. Void a mistaken order and create a corrected one so its audit trail and inventory remain understandable. The app does not handle refunds as separate transactions; enter any refund outside the app and retain the appropriate records.


