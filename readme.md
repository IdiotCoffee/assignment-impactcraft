These are the scripts I have implemented:

Data Generation
    • Generates invoice entries with fields: date, amount, tags
    • Two modes for generation:
        - By date range (we can also specify the number of transactions per day if we want to)
        - By total number of invoices spread randomly across the last 90 days (the number of days can be adjusted)
Analysis
    • Takes a percentile value as input and runs in four modes:
        - Mode 1: Groups invoices by week and calculates the selected percentile of invoice amounts per week.
        - Mode 2: Calculates the percentile of invoice amounts for every possible tag individually (e.g., cash, upi, etc.).
        - Mode 3: Filters data for invoices that contain ANY of the given tags, then computes the overall percentile for that subset.
        - Mode 4: Filters data for invoices that contain ALL of the selected tags (strict match), and calculates the percentile on that subset. This differs from Mode 3 which uses an OR-style match.