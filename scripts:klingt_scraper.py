"""
klingt.org event scraper
extrae todos los eventos desde enero 2022 hasta abril 2026
guarda en klingt_events.csv con formato: datum;event_name;venue
"""

import requests
from bs4 import BeautifulSoup
import csv
import time

URL = "https://klingt.org/gro.tgnilk/events/index.html?sid=1429840101128926"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:149.0) Gecko/20100101 Firefox/149.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-AR,es;q=0.9,en-US;q=0.8",
    "Referer": URL,
    "Content-Type": "application/x-www-form-urlencoded",
}

# periodos a extraer: enero 2022 a abril 2026
PERIODS = []
for year in range(2022, 2027):
    for month in range(1, 13):
        if year == 2022 and month < 1:
            continue
        if year == 2026 and month > 4:
            break
        PERIODS.append((month, year))


def scrape_month(session, month, year):
    data = {
        "start_month": str(month),
        "start_year": str(year),
        "limit": "99999",
        "sortby": "when",
        "direction": "up",
        "submit": "submit",
    }
    try:
        r = session.post(URL, data=data, headers=HEADERS, timeout=30)
        if r.status_code != 200:
            print(f"  error {r.status_code} para {month}/{year}")
            return []

        soup = BeautifulSoup(r.text, "html.parser")
        rows = soup.find_all("tr")
        events = []

        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 3:
                datum = cells[0].get_text(strip=True)
                event_name = cells[1].get_text(strip=True)
                venue = cells[2].get_text(strip=True)
                if datum and event_name and venue:
                    # convertir fecha a formato YYYY-MM-DD
                    datum_clean = parse_date(datum)
                    events.append([datum_clean, event_name, venue])

        return events

    except Exception as e:
        print(f"  excepcion en {month}/{year}: {e}")
        return []


def parse_date(date_str):
    """convierte 'jan. 15 2022' a '2022-01-15'"""
    months = {
        "jan": "01", "feb": "02", "mar": "03", "apr": "04",
        "may": "05", "jun": "06", "jul": "07", "aug": "08",
        "sep": "09", "oct": "10", "nov": "11", "dec": "12"
    }
    try:
        parts = date_str.lower().replace(".", "").split()
        if len(parts) >= 3:
            month = months.get(parts[0][:3], "00")
            day = parts[1].zfill(2)
            year = parts[2]
            return f"{year}-{month}-{day}"
    except Exception:
        pass
    return date_str


def main():
    session = requests.Session()
    # establecer sesion con GET primero
    session.get(URL, headers={"User-Agent": HEADERS["User-Agent"]})

    all_events = []
    total_periods = len(PERIODS)

    for i, (month, year) in enumerate(PERIODS):
        print(f"extrayendo {month:02d}/{year} ({i+1}/{total_periods})...")
        events = scrape_month(session, month, year)
        print(f"  {len(events)} eventos encontrados")
        all_events.extend(events)
        time.sleep(1)  # pausa de 1 segundo entre requests

    # guardar CSV
    output_file = "klingt_events_raw.csv"
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["datum", "event_name", "venue"])
        writer.writerows(all_events)

    print(f"\nlisto. {len(all_events)} eventos extraidos.")
    print(f"guardado en: {output_file}")


if __name__ == "__main__":
    main()
