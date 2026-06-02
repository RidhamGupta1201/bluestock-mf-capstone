import requests
import pandas as pd
from pathlib import Path
import time
import logging
from datetime import datetime

# Setup paths
BASE = Path(__file__).resolve().parent.parent
LOG_DIR = BASE / "reports"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Setup logging
logging.basicConfig(
    filename=str(LOG_DIR / "nav_fetch_log.txt"),
    level=logging.INFO,
    format="%(asctime)s — %(message)s"
)

def fetch_and_save(scheme_code, name):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    save_dir = BASE / "data" / "raw"
    
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                print(f"Bad status {response.status_code} for {scheme_code}, retrying...")
                time.sleep(2)
                continue
            
            if not response.text.strip():
                print(f"Empty response for {scheme_code}, retrying...")
                time.sleep(2)
                continue
            
            data = response.json()
            nav_df = pd.DataFrame(data["data"])
            nav_df["amfi_code"] = scheme_code
            nav_df["scheme_name"] = data["meta"]["scheme_name"]
            
            nav_df.to_csv(save_dir / f"{name}_nav.csv", index=False)
            
            msg = f"Saved {name}_nav.csv — {len(nav_df)} rows"
            print(f"✓ {msg}")
            logging.info(msg)
            return nav_df
        
        except requests.exceptions.JSONDecodeError:
            print(f"JSON error for {scheme_code} (attempt {attempt+1}/3)")
            time.sleep(3)
        except requests.exceptions.ConnectionError:
            print("No internet connection.")
            logging.error("No internet connection")
            break
        except requests.exceptions.Timeout:
            print(f"Timeout for {scheme_code}, retrying...")
            time.sleep(3)
    
    logging.error(f"Failed to fetch {scheme_code} after 3 attempts")
    print(f"✗ Failed: {scheme_code}")
    return None


if __name__ == "__main__":
    schemes = {
        125497: "hdfc_top100",
        119551: "sbi_bluechip",
        120503: "icici_bluechip",
        118632: "nippon_largecap",
        119092: "axis_bluechip",
        120841: "kotak_bluechip"
    }
    
    logging.info("===== Scheduled NAV fetch started =====")
    print(f"\n{'='*40}")
    print(f"Scheduled NAV Fetch — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*40}\n")
    
    success, failed = 0, 0
    for code, name in schemes.items():
        print(f"Fetching {name}...")
        result = fetch_and_save(code, name)
        if result is not None:
            success += 1
        else:
            failed += 1
        time.sleep(1)
    
    summary = f"Job complete — {success} succeeded, {failed} failed"
    print(f"\n{summary}")
    logging.info(summary)
    logging.info("===== Scheduled NAV fetch ended =====\n")