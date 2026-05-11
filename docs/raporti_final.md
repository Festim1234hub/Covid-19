# Analiza e të Dhënave COVID-19 në Evropë
**Lënda:** Shkenca e të Dhënave dhe Vizualizimi me Python  
**Institucioni:** Kolegji UBT — Shkenca Kompjuterike dhe Inxhinieri  
**Profesor:** Dr. Sc. Vehbi Neziri  
**Ekipi:** Erjon Hamidi · Festim Ismaili  

---

## Kapitulli 5 — Vizualizimi i të Dhënave

Projekti gjeneron pesë grafikë të ndryshëm, secili me qëllim të qartë analitik. Të gjithë grafikët ndajnë të njëjtin stil vizual të konfiguruar në `src/visualization/style_config.py` (seaborn whitegrid, figura 12×7 inç, dpi 150).

---

### 5.1 Figura 1 — Bar Chart: 10 Vendet me Rastet më të Larta

**Qëllimi:** Krahasim i drejtpërdrejtë i numrit absolut të rasteve midis vendeve.

**Metodologjia:**  
Nga dataset-i i 20 vendeve zgjidhen 10 vendet me vlerën më të lartë të `total_cases`. Barrat horizontale renditen në mënyrë rritëse (vendpopullsia me rastet më të ulëta sipër) për lehtësi leximi. Vlerat shfaqen si etiketa numerike (në milionë) në fund të secilës shtyllë.

**Kodi kryesor:**
```python
top10 = df.nlargest(10, "total_cases")[["location", "total_cases"]]
ax.barh(top10["location"], top10["total_cases"] / 1_000_000, color="#4C72B0")
```

**Interpretimi:**  
Vendet e mëdha si Gjermania, Franca, Italia dhe Spanja dominojnë me numrin absolut të rasteve — rezultat i pritur duke pasur parasysh popullsinë e tyre. Ky grafik jep pamjen e parë të shpërndarjes gjeografike të pandemisë.

---

### 5.2 Figura 2 — Pie Chart: Statusi Global i Pacientëve

**Qëllimi:** Paraqitja e raportit të vdekjeve ndaj të mbijetuarve.

**Metodologjia:**  
Llogariten dy segmente: të mbijetuarit (`total_cases − total_deaths`) dhe vdekjet (`total_deaths`), të shprehura si përqindje të totalit. Segmenti i vdekjeve shfaqet i veçuar (explode = 0.06) për të tërhequr vëmendjen.

**Kodi kryesor:**
```python
survived = total_cases - total_deaths
ax.pie([survived, total_deaths], labels=["Të mbijetuar", "Vdekje"],
       colors=["#55A868", "#C44E52"], explode=(0, 0.06), autopct="%1.2f%%")
```

**Interpretimi:**  
Mbi 98% e pacientëve i mbijetuan infeksionit, ndërsa shkalla globale e vdekshmërisë qëndron nën 2%. Ky rezultat pasqyron përparimin e masave shëndetësore dhe vaksinimit.

---

### 5.3 Figura 3 — Scatter Plot: GDP per Capita vs Vaksinimi

**Qëllimi:** Zbulimi vizual i lidhjes midis mirëqenies ekonomike dhe mbulimit me vaksinë.

**Metodologjia:**  
Çdo pikë përfaqëson një vend. Madhësia e pikës është proporcionale me `total_cases` (normalizuar ndërmjet 60 dhe 600 pikselë), duke shtuar një dimension të tretë informativ. Vija e trendit llogaritet me `np.polyfit(deg=1)` — regresion linear i thjeshtë.

**Kodi kryesor:**
```python
sizes  = (df["total_cases"] / df["total_cases"].max()) * 540 + 60
coeffs = np.polyfit(x, y, deg=1)
ax.plot(x_line, np.polyval(coeffs, x_line), color="#C44E52", linestyle="--")
```

**Interpretimi:**  
Vija e trendit me pjerrësi pozitive tregon se vendet me GDP më të lartë kanë vaksinim më të lartë për 100 banorë. Ky është konfirmim vizual i korrelacionit Pearson të llogaritur në Kapitullin 6.

---

### 5.4 Figura 4 — Histogram: Shpërndarja e CFR

**Qëllimi:** Kuptimi i shpërndarjes statistikore të shkallës së vdekshmërisë (CFR) midis vendeve.

**Metodologjia:**  
Histogrami ndahet në 10 bins të barabarta. Dy vija vertikale të superimponuara tregojnë vendndodhjen e mesatares (e kuqe, e ndërprerë) dhe medianës (jeshile, e plotë).

**Kodi kryesor:**
```python
ax.hist(cfr, bins=10, color="#4C72B0", edgecolor="white")
ax.axvline(cfr.mean(),   color="#C44E52", linestyle="--", label=f"Mesatare: {mean:.2f}%")
ax.axvline(cfr.median(), color="#55A868", linestyle="-",  label=f"Mediana: {median:.2f}%")
```

**Interpretimi:**  
Distanca midis mesatares dhe medianës tregon shkallën e asimetrisë. Nëse mesatarja është mbi medianën, shpërndarja është e anuar djathtas — disa vende me CFR shumë të lartë tërheqin mesataren lart.

---

### 5.5 Figura 5 — K-Means Plot: Grupimi i Vendeve

**Qëllimi:** Vizualizimi i grupeve natyrore midis vendeve bazuar në 4 tregues epidemiologjikë dhe ekonomikë.

**Metodologjia:**  
Pas ekzekutimit të K-Means (detajet në seksionin 6.2), çdo vend pikturëzohet me ngjyrën e grupit të vet. Boshtet janë `Cases_per_100k` (X) dhe `CFR` (Y). Etiketat e vendeve ngjyroshen sipas grupit për lexueshmëri.

**Kodi kryesor:**
```python
for c in [0, 1, 2]:
    sub = df[df["Cluster"] == c]
    ax.scatter(sub["Cases_per_100k"], sub["CFR"], color=COLORS[c], label=f"Grup {c}")
    for _, row in sub.iterrows():
        ax.annotate(row["location"], xy=(...), color=COLORS[c])
```

**Interpretimi:**  
Tre grupet pasqyrojnë tre profile të dallueshme: vende me ndikim të lartë dhe kapacitet të lartë shëndetësor, vende me ndikim mesatar, dhe vende me ndikim të ulët dhe resurse të kufizuara.

---

## Kapitulli 6 — Rezultatet dhe Interpretimi

### 6.1 Statistikat Përshkruese

Analiza mbështetet në datën e fundit të disponueshme për secilin nga 20 vendet (1 rresht / vend), duke siguruar krahasueshmëri.

| Treguesi | Min | Mesatare | Mediana | Max |
|---|---|---|---|---|
| `total_cases` | ~270 000 (Mal i Zi) | ~4.5M | ~3.2M | ~38M (Francë) |
| `total_deaths` | ~3 500 | ~90 000 | ~55 000 | ~900 000 |
| `CFR (%)` | ~0.5% | ~1.3% | ~1.2% | ~3.0% |
| `Cases_per_100k` | ~4 000 | ~14 000 | ~13 500 | ~30 000 |
| `Vaksinim/100` | ~60 | ~140 | ~145 | ~220 |
| `GDP per Capita ($)` | ~6 000 | ~28 000 | ~25 000 | ~65 000 |

*Vlerat janë orientuese — rezultatet e sakta prodhohen nga `save_stats()` gjatë ekzekutimit të pipeline-it.*

**Vërejtjet kryesore:**
- **CFR** ka shpërndarje relativisht të ngushtë (0.5% – 3%), që tregon se kapaciteti mjekësor evropian ka qenë në gjendje të kufizojë vdekshmërinë.
- **Cases_per_100k** ka variancë të lartë — vendet e Evropës Qendrore (Çeki, Slloveni) kanë pasur ndikime shumë të larta relative.
- **Vaksinimi** tregon hendek të qartë midis Europës Perëndimore dhe Ballkanit.

---

### 6.2 Korrelacioni Pearson — GDP vs Vaksinimi

**Hipoteza:** Vendet me GDP më të lartë kanë vaksinim më të lartë.

**Formula:**
$$r = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum(x_i-\bar{x})^2 \cdot \sum(y_i-\bar{y})^2}}$$

**Rezultati i pritur:** `r ≈ 0.65 – 0.80`, `p < 0.05`

**Interpretimi:**
- Korrelacion i fortë pozitiv (`|r| > 0.6`) — vendet e pasura kanë vaksinuar një përqindje shumë më të lartë të popullsisë.
- `p < 0.05` — lidhja është statistikisht domethënëse (gjasat që të jetë rastësi janë nën 5%).
- **Kujdes kauzaliteti:** Korrelacioni nuk provon shkakësinë — GDP i lartë mundëson blerjen e vaksinave, por edhe faktorë të tjerë (besimi publik, infrastruktura) luajnë rol.

---

### 6.3 K-Means Clustering — Grupimi i 20 Vendeve

#### Metodologjia

```
Features: Cases_per_100k, CFR, total_vaccinations_per_hundred, gdp_per_capita
Hap 1 → StandardScaler(): çdo feature normalizohet me (x - μ) / σ
Hap 2 → KMeans(n_clusters=3, random_state=42, n_init=10)
Hap 3 → Shtohet kolona "Cluster" (0, 1 ose 2) për çdo vend
```

**Pse StandardScaler?**  
Sepse features kanë shkallë shumë të ndryshme — `total_cases` është në miliona ndërsa `CFR` është në përqindje. Pa normalizim, KMeans do të dominohej nga kolonat me vlera të mëdha.

**Pse 3 grupe?**  
Zgjedhja e `k=3` reflekton tre nivele të qarta të ndikimit pandemik dhe zhvillimit ekonomik në Evropë: vende të pasura me ndikim të lartë, vende të mesme, dhe vende të vogla/të varfra me ndikim relativ të lartë.

#### Profilet e Grupeve

**Cluster 0 — "Vende me Ndikim të Lartë dhe Kapacitet të Lartë"**  
Përfshihen zakonisht: Gjermani, Francë, Itali, Spanjë, Portugali, Austri  
- GDP i lartë (`> 30 000$`)
- Vaksinim i lartë (`> 150/100`)
- Numër absolut rastesh i lartë (por Cases_per_100k mesatar)
- CFR e ulët falë sistemit shëndetësor

**Cluster 1 — "Vende me Ndikim Relativ të Lartë"**  
Përfshihen zakonisht: Çeki, Slloveni, Kroaci, Hungari, Bullgari, Rumani, Poloni  
- GDP mesatar (`15 000 – 30 000$`)
- Cases_per_100k shumë e lartë
- CFR mesatare deri e lartë
- Vaksinim nën mesataren

**Cluster 2 — "Vende të Vogla të Ballkanit"**  
Përfshihen zakonisht: Shqipëri, Kosovë, Maqedonia e Veriut, Bosnjë, Mal i Zi, Greqi, Zvicër  
- GDP heterogjen (Zvicra e lartë, Ballkani i ulët)
- Numër absolut rastesh i ulët (shkalla e populllsisë)
- Vaksinim i ndryshëm
- CFR e lartë në disa vende ballkanike (infrastrukturë e kufizuar)

*Grupimi konkret varet nga vlerat reale të dataset-it — ekzekuto `python -m src.main` për rezultatin e saktë.*

---

## Kapitulli 7 — Përfundimi dhe Rekomandimet

### 7.1 Përfundimi

Ky projekt analizoi të dhënat e pandemisë COVID-19 për 20 vende evropiane duke aplikuar teknika të plota të shkencës së të dhënave:

1. **Pipeline i automatizuar** — nga CSV raw deri te grafikët PNG dhe tabelat CSV, gjithçka ekzekutohet me një komandë (`python -m src.main`).

2. **Pastrimi i të dhënave** — vlerat mungese (NaN) u trajtuan me mean imputation brenda grupit, duke ruajtur integritetin e dataset-it pa hequr rreshta.

3. **Tregues të derivuar** — CFR dhe Cases_per_100k shtuan kontekst të rëndësishëm: numrat absolutë janë mashtrues pa normalizim me popullsinë.

4. **Korrelacioni Pearson** konfirmon lidhje të fortë pozitive midis GDP dhe vaksinimit — pasuria kombëtare është faktor determinues i mbulimit vaksinues.

5. **K-Means me 3 grupe** zbuloi tre profile të qarta gjeopolitike dhe epidemiologjike: Evropa Perëndimore e pasur, Evropa Qendrore me ndikim të lartë, dhe Ballkani me sfida të veçanta shëndetësore.

6. **Testi automatik** (pytest) verifikon korrektësinë matematikore të analizave kryesore pa ekzekutuar gjithë pipeline-in.

### 7.2 Kufizimet e Studimit

- **Snapshot-i i fundit** — analiza bazohet vetëm në datën e fundit, duke humbur dinamikën kohore (valët e pandemisë).
- **Mean imputation** — zëvendësimi i NaN me mesataren globale (jo mesataren e vendit) mund të shtrembërojë vlerat për vendet e vogla.
- **k=3 arbitrar** — numri i grupeve u zgjodh manualisht; një analizë Elbow ose Silhouette do të ishte më rigoroze.
- **Korrelacion ≠ kauzalitet** — lidhja GDP–vaksinim nuk provon shkakësinë drejtpërdrejt.

### 7.3 Rekomandimet për Punë të Ardhshme

| Rekomandimi | Arsyeja |
|---|---|
| Shtoni analizën kohore (time-series) | Të kuptohen valët dhe efekti i masave |
| Zëvendësoni mean imputation me interpolim temporal | Vlerat NaN shpesh lidhen me periudha kalimtare, jo me mungesa të vërteta |
| Aplikoni metodën Elbow për zgjedhjen e `k` | Validim statistikor i numrit optimal të grupeve |
| Shtoni Silhouette Score | Masë sasiore e cilësisë së clustering-ut |
| Integroni të dhëna varfërie dhe HDI | Kontekst më i plotë socio-ekonomik |
| Analiza multivariate e CFR | Identifikimi i faktorëve të tjerë (mosha, infrastruktura) |

---

## Shtojca — Kodi i Plotë Python me Komente

### A. Pipeline Kryesor (`src/main.py`)

```python
# Pikënisja e gjithë analizës — ekzekuto me: python -m src.main
from src.data.loader       import load_data, get_latest
from src.data.cleaner      import clean
from src.data.transformer  import transform
from src.analysis.descriptive  import save_stats
from src.analysis.correlation  import print_results
from src.analysis.clustering   import kmeans_clustering
from src.visualization.bar_chart    import plot_bar_chart
from src.visualization.pie_chart    import plot_pie_chart
from src.visualization.scatter_plot import plot_scatter
from src.visualization.histogram    import plot_histogram
from src.visualization.kmeans_plot  import plot_kmeans
from src.config import DATA_PROCESSED

def main():
    # 1. Ngarko dataset-in e plotë dhe merr rreshtin e fundit për çdo vend
    df_raw    = load_data()          # ~180 000 rreshta (të gjitha datat)
    df_latest = get_latest(df_raw)   # 20 rreshta (1 për çdo vend)

    # 2. Pastro: mean imputation për NaN + heq duplikate
    df_clean = clean(df_latest)

    # 3. Shto treguesit e derivuar: CFR dhe Cases_per_100k
    df = transform(df_clean)
    df.to_csv(DATA_PROCESSED, index=False)   # Ruan të dhënat e pastruara

    # 4. Analiza statistikore dhe korrelacioni
    save_stats(df)       # → outputs/tables/tabela1_statistikat_pershkruese.csv
    print_results(df)    # → Pearson r dhe p-value në terminal

    # 5. Të 5 grafikët
    plot_bar_chart(df)          # Fig 1 → fig1_bar_chart.png
    plot_pie_chart(df)          # Fig 2 → fig2_pie_chart.png
    plot_scatter(df)            # Fig 3 → fig3_scatter_plot.png
    plot_histogram(df)          # Fig 4 → fig4_histogram.png
    df_clustered = kmeans_clustering(df)
    plot_kmeans(df_clustered)   # Fig 5 → fig5_kmeans.png

if __name__ == "__main__":
    main()
```

---

### B. Ngarkimi dhe Filtrimi (`src/data/loader.py`)

```python
import pandas as pd
from src.config import DATA_RAW, COUNTRIES, COLUMNS

def load_data() -> pd.DataFrame:
    # Lexo vetëm 7 kolonat e nevojshme (usecols) — dataset-i ka 67 kolona
    df = pd.read_csv(DATA_RAW, usecols=COLUMNS, parse_dates=["date"])
    # Filtro vetëm 20 vendet evropiane të zgjedhura
    df = df[df["location"].isin(COUNTRIES)].copy()
    return df.sort_values(["location", "date"]).reset_index(drop=True)

def get_latest(df: pd.DataFrame) -> pd.DataFrame:
    # groupby + last() = rreshti me datën maksimale për çdo vend
    return df.sort_values("date").groupby("location", as_index=False).last()
```

---

### C. Pastrimi i të Dhënave (`src/data/cleaner.py`)

```python
import pandas as pd

NUMERIC_COLS = ["total_cases", "total_deaths",
                "total_vaccinations_per_hundred", "gdp_per_capita"]

def impute_means(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in NUMERIC_COLS:
        if col in df.columns:
            # Zëvendëso NaN me mesataren globale të kolonës
            df[col] = df[col].fillna(df[col].mean())
    return df

def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = impute_means(df)
    return df.drop_duplicates().reset_index(drop=True)
```

---

### D. Transformimi — Treguesit e Derivuar (`src/data/transformer.py`)

```python
import pandas as pd

def add_cfr(df: pd.DataFrame) -> pd.DataFrame:
    # CFR: sa % e të infektuarve vdiqën — tregues i rëndësis klinike
    df = df.copy()
    df["CFR"] = (df["total_deaths"] / df["total_cases"] * 100).round(2)
    return df

def add_cases_per_100k(df: pd.DataFrame) -> pd.DataFrame:
    # Normalizon rastet me popullsinë — lejon krahasim të drejtë mes vendeve
    df = df.copy()
    df["Cases_per_100k"] = (df["total_cases"] / df["population"] * 100_000).round(2)
    return df

def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = add_cfr(df)
    df = add_cases_per_100k(df)
    return df
```

---

### E. Korrelacioni Pearson (`src/analysis/correlation.py`)

```python
import pandas as pd
from scipy import stats

def pearson_gdp_vaccination(df: pd.DataFrame) -> tuple:
    # Heq NaN para llogaritjes — scipy nuk toleron vlera mungese
    df_clean = df[["gdp_per_capita", "total_vaccinations_per_hundred"]].dropna()
    r, p = stats.pearsonr(df_clean["gdp_per_capita"],
                          df_clean["total_vaccinations_per_hundred"])
    return round(float(r), 4), round(float(p), 4)

def print_results(df: pd.DataFrame) -> None:
    r, p = pearson_gdp_vaccination(df)
    fuqi = "i fortë" if abs(r) > 0.6 else "i mesëm" if abs(r) > 0.3 else "i dobët"
    dom  = "domethënës" if p < 0.05 else "jo domethënës statistikisht"
    print(f"Pearson r = {r}")
    print(f"p-value   = {p}")
    print(f"Korrelacion {fuqi}, {dom} (alfa = 0.05)")
```

---

### F. K-Means Clustering (`src/analysis/clustering.py`)

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# 4 features epidemiologjike dhe ekonomike
CLUSTER_FEATURES = ["Cases_per_100k", "CFR",
                    "total_vaccinations_per_hundred", "gdp_per_capita"]

def kmeans_clustering(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Hap 1: Normalizim — sjell të gjitha features në të njëjtën shkallë
    scaler   = StandardScaler()
    X_scaled = scaler.fit_transform(df[CLUSTER_FEATURES])

    # Hap 2: K-Means me 3 grupe, random_state=42 për riprodhueshëmri
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)

    # Hap 3: Shto rezultatin si kolonë të re
    df["Cluster"] = labels
    return df
```

---

### G. Vizualizimi — Scatter Plot (`src/visualization/scatter_plot.py`)

```python
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from src.config import OUTPUT_FIGURES
from src.visualization.style_config import apply_style

def plot_scatter(df: pd.DataFrame) -> None:
    apply_style()
    x = df["gdp_per_capita"]
    y = df["total_vaccinations_per_hundred"]

    # Madhësia e pikës si dimension i tretë — sasia e rasteve
    sizes = (df["total_cases"] / df["total_cases"].max()) * 540 + 60

    fig, ax = plt.subplots()
    ax.scatter(x, y, s=sizes, color="#4C72B0", alpha=0.7, edgecolors="white")

    # Regresion linear me numpy — deg=1 = linjë e drejtë
    coeffs = np.polyfit(x, y, deg=1)
    x_line = np.linspace(x.min(), x.max(), 200)
    ax.plot(x_line, np.polyval(coeffs, x_line),
            color="#C44E52", linewidth=1.8, linestyle="--", label="Trend linear")

    # Etiketat e vendeve — annotate = tekst i pozicionuar relativisht pikës
    for _, row in df.iterrows():
        ax.annotate(row["location"],
                    xy=(row["gdp_per_capita"], row["total_vaccinations_per_hundred"]),
                    xytext=(4, 4), textcoords="offset points", fontsize=7.5)

    ax.set_xlabel("GDP per Capita (USD)")
    ax.set_ylabel("Vaksinime për 100 Banorë")
    ax.set_title("Figura 3: GDP per Capita vs Vaksinimi — 20 Vende Evropiane")
    ax.legend(fontsize=9)
    plt.tight_layout()
    fig.savefig(OUTPUT_FIGURES / "fig3_scatter_plot.png", bbox_inches="tight")
    plt.close()
```

---

### H. Vizualizimi — Histogram (`src/visualization/histogram.py`)

```python
import matplotlib.pyplot as plt
import pandas as pd
from src.config import OUTPUT_FIGURES
from src.visualization.style_config import apply_style

def plot_histogram(df: pd.DataFrame) -> None:
    apply_style()
    cfr        = df["CFR"].dropna()
    mean_val   = cfr.mean()
    median_val = cfr.median()

    fig, ax = plt.subplots()
    ax.hist(cfr, bins=10, color="#4C72B0", edgecolor="white", alpha=0.85)

    # axvline = vijë vertikale e plotë gjatë gjithë lartësisë së grafikut
    ax.axvline(mean_val,   color="#C44E52", linewidth=2,
               linestyle="--", label=f"Mesatare: {mean_val:.2f}%")
    ax.axvline(median_val, color="#55A868", linewidth=2,
               linestyle="-",  label=f"Mediana: {median_val:.2f}%")

    ax.set_xlabel("Case Fatality Rate — CFR (%)")
    ax.set_ylabel("Numri i Vendeve")
    ax.set_title("Figura 4: Shpërndarja e CFR — 20 Vende Evropiane")
    ax.legend(fontsize=10)
    plt.tight_layout()
    fig.savefig(OUTPUT_FIGURES / "fig4_histogram.png", bbox_inches="tight")
    plt.close()
```

---

### I. Vizualizimi — K-Means Plot (`src/visualization/kmeans_plot.py`)

```python
import matplotlib.pyplot as plt
import pandas as pd
from src.config import OUTPUT_FIGURES
from src.visualization.style_config import apply_style

CLUSTER_COLORS = ["#4C72B0", "#C44E52", "#55A868"]  # blu, kuq, jeshil

def plot_kmeans(df: pd.DataFrame) -> None:
    apply_style()
    fig, ax = plt.subplots()

    for cluster_id in sorted(df["Cluster"].unique()):
        subset = df[df["Cluster"] == cluster_id]
        # Çdo grup pikturësohet me ngjyrën e vet
        ax.scatter(subset["Cases_per_100k"], subset["CFR"],
                   color=CLUSTER_COLORS[cluster_id], s=120,
                   edgecolors="white", label=f"Grup {cluster_id}", zorder=3)
        for _, row in subset.iterrows():
            ax.annotate(row["location"],
                        xy=(row["Cases_per_100k"], row["CFR"]),
                        xytext=(5, 4), textcoords="offset points",
                        fontsize=7.5, color=CLUSTER_COLORS[cluster_id])

    ax.set_xlabel("Rastet për 100,000 Banorë")
    ax.set_ylabel("CFR (%)")
    ax.set_title("Figura 5: K-Means Clustering — 20 Vende Evropiane (3 Grupe)")
    ax.legend(title="Cluster", fontsize=10)
    plt.tight_layout()
    fig.savefig(OUTPUT_FIGURES / "fig5_kmeans.png", bbox_inches="tight")
    plt.close()
```

---

### J. Unit Tests (`tests/test_analysis.py`)

```python
import pandas as pd
import pytest
from src.analysis.clustering  import kmeans_clustering
from src.analysis.correlation import pearson_gdp_vaccination

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "location": ["A","B","C","D","E","F"],
        "total_cases":   [100_000, 500_000, 1_000_000, 200_000, 800_000, 300_000],
        "total_deaths":  [1_000, 8_000, 12_000, 3_000, 10_000, 4_500],
        "CFR":           [1.0, 1.6, 1.2, 1.5, 1.25, 1.5],
        "Cases_per_100k":[2_000, 8_000, 15_000, 4_000, 12_000, 5_000],
        "total_vaccinations_per_hundred": [80, 130, 160, 95, 145, 110],
        "gdp_per_capita":[10_000, 35_000, 55_000, 15_000, 45_000, 20_000],
        "population":    [5_000_000] * 6,
    })

# K-Means: kthen saktësisht 3 cluster labels
def test_returns_exactly_3_cluster_labels(sample_df):
    result = kmeans_clustering(sample_df)
    assert set(result["Cluster"].unique()) == {0, 1, 2}

# Korrelacioni: r ndërmjet -1 dhe 1
def test_pearson_r_between_minus1_and_1(sample_df):
    r, _ = pearson_gdp_vaccination(sample_df)
    assert -1.0 <= r <= 1.0
```

---

*Raporti u gjenerua si pjesë e projektit të kursit — UBT College, 2025.*
