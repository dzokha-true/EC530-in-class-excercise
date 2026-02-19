
import requests

URL = "https://api.fda.gov/drug/drugsfda.json"
params = {"search": 'openfda.generic_name.exact:"TERBINAFINE"', "limit": 1}

r = requests.get(URL, params=params, timeout=20)
if r.status_code == 404:
    print("No matches found.")
else:
    r.raise_for_status()
    rec = r.json()["results"][0]
    active = rec["products"][0].get("active_ingredients", [])
    for ing in active:
        print(f"{ing.get('name')} — {ing.get('strength')}")


