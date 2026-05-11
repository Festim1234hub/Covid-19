# Analiza e të Dhënave COVID-19 në Evropë

> Projekt për lëndën **Shkenca e të Dhënave dhe Vizualizimi me Python**
> Kolegji UBT — Shkenca Kompjuterike dhe Inxhinieri
> Profesor: Dr. Sc. Vehbi Neziri

## 📋 Përshkrimi

Ky projekt analizon të dhënat e pandemisë COVID-19 për 20 vende evropiane duke aplikuar teknikat e shkencës së të dhënave dhe vizualizimit me Python. Përfshin pastrimin e të dhënave, analizën statistikore, korrelacionin Pearson, 5 vizualizime të ndryshme dhe algoritmin K-Means Clustering.

## 🎯 Qëllimet

1. Pastrimi dhe përpunimi i të dhënave me vlera mungese
2. Llogaritja e treguesve statistikorë (CFR, Cases per 100k)
3. Vizualizimi me 5 grafikë (Bar, Pie, Scatter, Histogram, K-Means)
4. Grupimi i vendeve me K-Means Clustering

## 👥 Ekipi

- **Erjon Hamidi** Të dhënat, Analiza statistikore, Bar/Pie charts, Style config
- **Festim Ismaili** — Scatter, Histogram, K-Means Clustering, Utils, Main pipeline

## 📁 Struktura e Projektit

```
covid19-analysis/
├── data/                   # Dataset-et origjinale dhe të përpunuara
│   ├── raw/                # Të dhënat origjinale CSV
│   ├── processed/          # Të dhënat e pastruara dhe të transformuara
│   └── external/           # Burime të jashtme (popullsia, GDP)
├── notebooks/              # Jupyter Notebooks për eksplorim dhe analizë
│   ├── 01_exploratory.ipynb
│   ├── 02_cleaning.ipynb
│   ├── 03_analysis.ipynb
│   └── 04_visualization.ipynb
├── src/                    # Kodi kryesor i projektit
│   ├── config.py           # Konfigurimet globale dhe paths
│   ├── main.py             # Pipeline kryesor i ekzekutimit
│   ├── data/               # Ngarkimi, pastrimi dhe transformimi
│   │   ├── loader.py
│   │   ├── cleaner.py
│   │   └── transformer.py
│   ├── analysis/           # Analiza statistikore dhe clustering
│   │   ├── descriptive.py
│   │   ├── correlation.py
│   │   └── clustering.py
│   ├── visualization/      # Gjenerimi i 5 grafikëve
│   │   ├── bar_chart.py
│   │   ├── pie_chart.py
│   │   ├── scatter_plot.py
│   │   ├── histogram.py
│   │   ├── kmeans_plot.py
│   │   └── style_config.py
│   └── utils/              # Funksione dhe konstante ndihmëse
│       ├── helpers.py
│       └── constants.py
├── outputs/                # Rezultatet e gjeneruar automatikisht
│   ├── figures/            # Grafikët e eksportuar (PNG)
│   ├── tables/             # Tabelat statistikore (CSV)
│   └── reports/            # Raportet e gjeneruar
├── tests/                  # Unit tests për modulet kryesore
├── docs/                   # Dokumentacioni dhe imazhet
├── app.py                  # Dashboard interaktiv Streamlit
├── .gitignore
├── requirements.txt
└── LICENSE
```

## 🚀 Si të ekzekutohet

```bash
# 1. Klono repozitorinë
git clone https://github.com/USERNAME/covid19-analysis.git
cd covid19-analysis

# 2. Krijo virtual environment
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows

# 3. Instalo varësitë
pip install -r requirements.txt

# 4. Ekzekuto pipeline-in (gjeneron figurat dhe tabelat)
python -m src.main

# 5. Hap dashboard-in interaktiv
streamlit run app.py
```

## 🔧 Libraritë e Përdorura

- **pandas** — manipulim i të dhënave
- **numpy** — llogaritje numerike
- **matplotlib** & **seaborn** — vizualizim
- **scikit-learn** — K-Means Clustering, StandardScaler
- **scipy** — korrelacioni Pearson
- **streamlit** — dashboard interaktiv

## 📊 Outputs

Pas ekzekutimit gjenerohen:

- 5 grafikë në `outputs/figures/`
- Tabela statistikore në `outputs/tables/`
- Dataset i pastruar në `data/processed/`

## 📝 Raporti

Dokumentimi i plotë i projektit ndodhet në `docs/`.

## 📜 Licenca

MIT License — shih file-in [LICENSE](LICENSE).
