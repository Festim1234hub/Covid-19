"""Konfigurimet globale: paths, konstantet."""

from pathlib import Path

# Rrugët e folderëve
ROOT_DIR = Path(__file__).parent.parent
DATA_RAW       = ROOT_DIR / "data" / "raw" / "covid_data.csv"
DATA_PROCESSED = ROOT_DIR / "data" / "processed" / "covid_clean.csv"
OUTPUT_FIGURES = ROOT_DIR / "outputs" / "figures"
OUTPUT_TABLES  = ROOT_DIR / "outputs" / "tables"

# 20 vendet e analizës
COUNTRIES = [
    "Albania", "Kosovo", "North Macedonia", "Bosnia and Herzegovina",
    "Montenegro", "Croatia", "Slovenia", "Bulgaria", "Romania",
    "Hungary", "Austria", "Italy", "Greece", "Germany",
    "France", "Spain", "Portugal", "Poland", "Czechia", "Switzerland"
]

# Kolonat që ngarkohen nga CSV
COLUMNS = [
    "location", "date", "total_cases", "total_deaths",
    "total_vaccinations_per_hundred", "gdp_per_capita", "population"
]
