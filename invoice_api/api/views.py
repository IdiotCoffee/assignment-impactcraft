from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def generate_invoices(mode, count=None, start_date=None, end_date=None, per_day=5):
    tag1 = ["UPI", "cash", "card"]
    tag2 = ["taxes", "notaxes"]
    tag3 = ["discount", "nodiscount"]

    data = []

    if mode == 1:
        current = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        while current <= end:
            for _ in range(per_day):
                amount = round(random.uniform(100, 1000), 2)
                tags = [random.choice(tag1), random.choice(tag2), random.choice(tag3)]
                data.append({"date": current.strftime("%Y-%m-%d"), "amount": amount, "tags": tags})
            current += timedelta(days=1)

    elif mode == 2:
        for _ in range(count):
            random_day = datetime.now() - timedelta(days=random.randint(0, 89))
            amount = round(random.uniform(100, 1000), 2)
            tags = [random.choice(tag1), random.choice(tag2), random.choice(tag3)]
            data.append({"date": random_day.strftime("%Y-%m-%d"), "amount": amount, "tags": tags})

    return data


def analyze_data(df, percentile, mode, tag_input=None):
    df["date"] = pd.to_datetime(df["date"])
    df["amount"] = df["amount"].astype(float)

    if mode == 1:
        df['week'] = df['date'].dt.to_period('W').apply(lambda r: r.start_time)
        grouped = df.groupby("week")["amount"].apply(lambda x: np.percentile(x, percentile)).reset_index()
        return grouped.to_dict(orient="records")

    elif mode == 2:
        exploded = df.explode("tags")
        grouped = exploded.groupby("tags")["amount"].apply(lambda x: np.percentile(x, percentile)).reset_index()
        return grouped.to_dict(orient="records")

    elif mode == 3:
        selected_tags = [tag.strip() for tag in tag_input]
        exploded = df.explode("tags")
        f_tags = exploded[exploded["tags"].isin(selected_tags)].drop_duplicates(subset=["date", "amount"])
        if len(f_tags) <= 0:
            return {"message": "No records"}
        result = np.percentile(f_tags["amount"], percentile)
        return {"tags": selected_tags, f"{percentile}th": result}

    elif mode == 4:
        selected_tags = [tag.strip() for tag in tag_input]
        df["tag_str"] = df["tags"].apply(lambda x: ",".join(x))
        f_df = df[~df["tag_str"].str.contains("|".join(selected_tags))]
        if len(f_df) <= 0:
            return {"message": "No records"}
        result = np.percentile(f_df["amount"], percentile)
        return {"excluded_tags": selected_tags, f"{percentile}th": result}

    else:
        return {"error": "Invalid mode"}


class GenerateInvoiceView(APIView):
    def post(self, request):
        try:
            mode = int(request.data.get("mode"))

            if mode == 1:
                start_date = request.data.get("start_date")
                end_date = request.data.get("end_date")
                per_day = int(request.data.get("per_day", 5))
                data = generate_invoices(mode, start_date=start_date, end_date=end_date, per_day=per_day)
            elif mode == 2:
                count = int(request.data.get("count"))
                data = generate_invoices(mode, count=count)
            else:
                return Response({"error": "Invalid mode"}, status=400)

            return Response(data, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=400)


class AnalyzeInvoiceView(APIView):
    def post(self, request):
        try:
            invoices = request.data.get("data")
            percentile = float(request.data.get("percentile"))
            mode = int(request.data.get("mode"))

            # Sanitize tags
            raw_tags = request.data.get("tags", [])
            if isinstance(raw_tags, str):
                tag_input = [t.strip() for t in raw_tags.split(",")]
            else:
                tag_input = raw_tags

            df = pd.DataFrame(invoices)
            result = analyze_data(df, percentile, mode, tag_input)
            return Response(result)

        except Exception as e:
            return Response({"error": str(e)}, status=400)
