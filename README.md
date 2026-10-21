# Pinteresty Outfits Business Desk

A local Flask and SQLite app for a clothing and accessories shop. It uses no external APIs or cloud services and binds to `127.0.0.1` only. Product photos, the database, and backups stay in the project’s local data folder.

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

Sale line items and discounts cannot be edited in place. Void a mistaken order and create a corrected one so its audit trail and inventory remain understandable. The app does not handle refunds as separate transactions; enter any refund outside the app and retain the appropriate records.


