# tagsinclusive user inputs the tag or tags, only those tag/tags are seperated - even if there are multiple tags, you can still seperate that tag.
# tagsexclusive - user will input the tag/tags, and only those rows will be filtered. If a row has multiple tags, it will not be filtered.
# tags - group all different types of tags together, count the number of instances of these tags, then percentile 
# no tags - only take transactions with no tags

import pandas as pd
import numpy as np
import ast
# import json

df = pd.read_csv("invoices.csv")
df["date"] = pd.to_datetime(df["date"])
# df["tags"] = df["tags"].apply(json.loads)
df["tags"] = df["tags"].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) and x != '[]' else [])
print(type(df["tags"].iloc[0]))


percentile = float(input("Enter the percentile: "))

mode = int(input("1. Group by week, then percentile\n2. A percentile score for all types of tags.\n3. Tag-based filtering\n4. Tag-based, both included"))

if mode == 1:

    df.set_index('date', inplace=True)
    weekly = df.resample('W')['amount'].apply(lambda x: np.percentile(x, percentile)).reset_index()
    weekly.columns = ['week-start', f"{percentile}th"]
    weekly.to_csv("weekly.csv", index=False)
    print("done.")
    # print(weekly.head())

if mode == 2:
    seperated_tags = df.explode('tags')
    tagwise = seperated_tags.groupby('tags')['amount'].apply(lambda x: np.percentile(x, percentile)).reset_index()
    tagwise.columns = ['tag', f'{percentile}th']
    tagwise.to_csv("option2.csv", index=False)
    print(tagwise.head())

if mode == 3:
    tag_ip = input("Enter the tag/tags: ")
    selected_tags = [tag.strip() for tag in tag_ip.split(",")]
    exploded = df.explode("tags")
    f_tags = exploded[exploded["tags"].isin(selected_tags)]

    ''' Do I have to drop duplicates ?'''
    f_tags = f_tags.drop_duplicates(subset=["date","amount"])

    if len(f_tags) <= 0:
        print("No records")
    else:
        result = np.percentile(f_tags["amount"], percentile)
        print(f"{percentile}th percentile value for {tag_ip} is: {result: .2f}")
        # df = pd.DataFrame(
        #     {
        #         "tags": [",".join(selected_tags)],
        #         f"{percentile}th" : [result]
        #     }
        # )
        # df.to_csv("option3.csv", index=False)

if mode == 4:
    tag_ip = input("Enter the tag/tags: ")
    selected_tags = [tag.strip() for tag in tag_ip.split(",")]
    filtered = df[df["tags"].apply(lambda x: all(tag in x for tag in selected_tags))]   
    if len(filtered) == 0:
        print("No such solo combinations of tags")
    else:
        result = np.percentile(filtered["amount"], percentile)
        print(f"{percentile}th score for {tag_ip} is {result: .2f}")
        # pd.DataFrame({
        #     "tags": [",".join(selected_tags)],
        #     "percentile amount": [result]
        # }).to_csv("option4.csv",index=False)

