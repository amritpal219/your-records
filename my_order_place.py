import json
import os
from datetime import datetime

CONFIG_FILE = "config.json"
ITEM_FILE = "items.json"
RECORD_FILE = "records.json"

# ---------- AUTO SETUP ----------
def setup_files():
    if not os.path.exists(CONFIG_FILE):
        print("=== FIRST TIME SETUP ===")
        shop_name = input("Enter shop name: ")
        currency = input("Enter currency (₹, $, PKR etc): ")
        start_year = int(input("Enter shop start year: "))

        config = {
            "shop_name": shop_name,
            "currency": currency,
            "start_year": start_year
        }

        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)

        print("✔ Setup completed\n")

    if not os.path.exists(ITEM_FILE):
        with open(ITEM_FILE, "w") as f:
            json.dump([], f)

    if not os.path.exists(RECORD_FILE):
        with open(RECORD_FILE, "w") as f:
            json.dump([], f)

# ---------- LOAD CONFIG ----------
def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

# ---------- FILE HELPERS ----------
def load_data(file):
    with open(file, "r") as f:
        return json.load(f)

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# ---------- ADD ITEM ----------
def add_item():
    items = load_data(ITEM_FILE)
    name = input("Item name: ")
    price = float(input("Item price: "))
    items.append({"name": name, "price": price})
    save_data(ITEM_FILE, items)
    print("✔ Item added\n")

# ---------- ADD RECORD ----------
def add_record(currency):
    items = load_data(ITEM_FILE)
    if not items:
        print("❌ Add items first\n")
        return

    record_items = []
    grand_total = 0

    while True:
        print("\nItems List:")
        for i, item in enumerate(items):
            print(f"{i+1}. {item['name']} - {currency}{item['price']}")

        choice = int(input("Choose item number: ")) - 1
        qty = int(input("Quantity: "))

        selected = items[choice]
        total = selected["price"] * qty

        record_items.append({
            "item": selected["name"],
            "qty": qty,
            "total": total
        })

        grand_total += total

        print("Add more items?")
        print("1. Yes")
        print("2. No")
        if input("Choose: ") == "2":
            break

    now = datetime.now()
    record = {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "items": record_items,
        "grand_total": grand_total
    }

    records = load_data(RECORD_FILE)
    records.append(record)
    save_data(RECORD_FILE, records)
    print("✔ Record saved\n")

# ---------- VIEW RECORDS ----------
def view_records(currency):
    records = load_data(RECORD_FILE)
    if not records:
        print("❌ No records\n")
        return

    print("""
1. Day
2. Week
3. Month
4. Year
5. Back
""")
    ch = input("Choose: ")
    today = datetime.now()

    if ch == "1":
        days = min(int(input("Number of days (max 1095): ")), 1095)
    elif ch == "2":
        weeks = min(int(input("Number of weeks (max 156): ")), 156)
    elif ch == "3":
        months = min(int(input("Number of months (max 36): ")), 36)
    elif ch == "4":
        years = min(int(input("Number of years (max 3): ")), 3)
    else:
        return

    filtered = []
    for r in records:
        r_date = datetime.strptime(r["date"], "%Y-%m-%d")
        delta = today - r_date

        if ch == "1" and delta.days <= days:
            filtered.append(r)
        elif ch == "2" and delta.days <= weeks * 7:
            filtered.append(r)
        elif ch == "3" and (today.year - r_date.year) * 12 + (today.month - r_date.month) < months:
            filtered.append(r)
        elif ch == "4" and (today.year - r_date.year) < years:
            filtered.append(r)

    if not filtered:
        print("❌ No records in this period\n")
        return

    for r in filtered:
        print("\n----------------")
        print("Date:", r["date"], "Time:", r["time"])
        for it in r["items"]:
            print(f"{it['item']} | Qty {it['qty']} | {currency}{it['total']}")
        print("Grand Total:", currency, r["grand_total"])
        print("----------------")

    print("""
What you want to do?
1. Total Money
2. Save to Text File
3. Nothing
""")
    op = input("Choose: ")

    if op == "1":
        total = sum(r["grand_total"] for r in filtered)
        print("TOTAL:", currency, total)

    elif op == "2":
        filename = f"records_{today.strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w") as f:
            for r in filtered:
                f.write(f"{r['date']} {r['time']}\n")
                for it in r["items"]:
                    f.write(f"{it['item']} x{it['qty']} = {currency}{it['total']}\n")
                f.write(f"Grand Total: {currency}{r['grand_total']}\n")
                f.write("-----------------\n")
        print("✔ Saved as", filename)

# ---------- MAIN ----------
def main():
    setup_files()
    config = load_config()

    print(f"\n=== {config['shop_name']} ===")
    print(f"Shop started in {config['start_year']}\n")

    while True:
        print("""
1. Add New Record
2. View Records
3. Add Item
4. Exit
""")
        choice = input("Choose: ")
        if choice == "1":
            add_record(config["currency"])
        elif choice == "2":
            view_records(config["currency"])
        elif choice == "3":
            add_item()
        elif choice == "4":
            print("Goodbye 👋")
            break
        else:
            print("Invalid option\n")

main()
