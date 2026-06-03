from pathlib import Path
import pandas as pd
import requests

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"

funds = {
    "sbi_bluechip": 119551,
    "icici_bluechip": 120503,
    "nippon_largecap": 118632,
    "axis_bluechip": 119092,
    "kotak_bluechip": 120841
}

for fund_name, scheme_code in funds.items():
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    response = requests.get(url)
    data = response.json()
    nav_df = pd.DataFrame(data["data"])
    output_file = RAW_DIR / f"{fund_name}_nav.csv"
    nav_df.to_csv(output_file, index=False)
    print(f"Saved: {output_file}")