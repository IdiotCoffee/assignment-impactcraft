# invoices_data:
# date    amount  tags
# tags1 can be: [ "UPI", "cash", "card"]
# tags2 can be: ["taxes", "notaxes"]
# tags3 can be: ["discount", "loyaltyCard"]
# percentile value input, then find data corresponding to that percentile.
# the tester should be able to choose how he wants to define the data.
# timedelta is used in count to have a start-date to begin the transactions, i have taken it to be days=90.

import pandas as pd
import random
from datetime import datetime, timedelta
# import json

payment_options = ["cash", "card", "upi"]
payment_info= ["discounted", "no-taxes", "with-tax"]
customer_info = ["loyaltyCard", "newCustomer", "guest"]

def generate_invoice(date):
    tags = [
        random.choice(payment_options),
        random.choice(payment_info),
        random.choice(customer_info)
    ]

    no_of_tags = random.randint(0, 3)
    chosen_tags = random.sample(tags, k=no_of_tags)
    
    single_invoice = {
        "date": date.isoformat(),
        "amount": round(random.uniform(300, 1000), 2),
        "tags": chosen_tags
    }
    return single_invoice

def dateRange(startdate, enddate, fixed=None):
    invoices = []
    for d in pd.date_range(start=startdate, end=enddate):
        count = fixed if fixed else random.randint(5, 10)
        for i in range(count):
            invoices.append(generate_invoice(d.date()))
    return invoices

def numberOfInvoices(count):
    invoices = []
    end = datetime.today()
    start = datetime.today() - timedelta(days=90)
    d_range = pd.date_range(start=start, end=end).tolist()
    chosen_dates = random.choices(d_range, k=count)
    for d in chosen_dates:
        invoices.append(generate_invoice(d.date()))
    return invoices



mode = int(input("1. Generate by date-range\n2. Generate by total_no of invoices\n"))

if mode == 1:
    start = input("enter start date: ")
    end = input("enter end date: ")
    fixed = input("do you want to fix the number of transactions: ").lower()

    start = pd.to_datetime(start).date()
    end = pd.to_datetime(end).date()

    if fixed == "y":
        daily = int(input("Enter the number of entries per day: "))
        invoices = dateRange(start, end, daily)
    else:
        invoices = dateRange(start,end)
    # print(invoices)
    
if mode == 2:
    count = int(input("how many invoices do you want in total: "))
    invoices = numberOfInvoices(count)
    # print(invoices)

df = pd.DataFrame(invoices)
# df["tags"] = df["tags"].apply(json.dumps)
df.to_csv("invoices.csv", index=False)
print(len(invoices))
print(df.head())