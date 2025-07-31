import pandas as pd


df1 = pd.DataFrame({
    'invoice_id': [1, 2, 3, 4, 5],
    'invoice_amt': [200, 300, 500, 700, 1000]
})

#print(df1)

df2 = pd.DataFrame({
    'invoice_id': [3, 4, 6, 7],
    'invoice_amt': [400, 100, 600, 800]
})
#print(df2)

merged = pd.merge(df1,df2, on="invoice_id", how="outer")
# print(merged)

merged['maximum'] = merged[["invoice_amt_x", "invoice_amt_y"]].max(axis=1)
print(merged)