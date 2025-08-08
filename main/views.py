import json
from datetime import datetime
from django.conf import settings
from django.shortcuts import render

def index(request):

    with open('output.json', 'r') as f:
        data = json.load(f)

    parsed_entries = []
    for entry in data:
        date_str = entry['date']
        try:
            date_clean = date_str.split('(')[0].strip()
            date_obj = datetime.strptime(date_clean, "%B %d, %Y")
        except ValueError:
            try:
                date_obj = datetime.strptime(date_str, "%B %d, %Y")
            except ValueError:
                continue

        parsed_entries.append((date_obj, entry['value'], date_str))

    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

    nearest = None
    min_diff = None
    for date_obj, value, original_str in parsed_entries:
        diff = (date_obj - today).days
        if diff >= 0:
            if min_diff is None or diff < min_diff:
                min_diff = diff
                nearest = (original_str, value)

    if nearest is None:
        context = {
            "error": "No upcoming dates found."
        }
    else:
        nearest_date_str, nearest_value = nearest
        context = {
            "nearest_date": nearest_date_str,
            "patch_version": nearest_value
        }

    return render(request, 'index.html', context)
