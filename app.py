"""Dashboard interaktiv për analizën COVID-19 në Evropë."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
import pandas as pd

from src.data.loader import load_data, get_latest
from src.data.cleaner import clean
from src.data.transformer import transform
from src.analysis.clustering import kmeans_clustering
from src.analysis.correlation import pearson_gdp_vaccination
from src.visualization.bar_chart import plot_bar_chart
from src.visualization.pie_chart import plot_pie_chart
from src.visualization.scatter_plot import plot_scatter
from src.visualization.histogram import plot_histogram
from src.visualization.kmeans_plot import plot_kmeans

# ── Konfigurimi i faqes ──────────────────────────────────────────
st.set_page_config(
    page_title="COVID-19 Analiza — Evropë",
    page_icon="🦠",
    layout="wide"
)

# ── Ngarkimi i të dhënave ────────────────────────────────────────
@st.cache_data
def get_data():
    df = transform(clean(get_latest(load_data())))
    df = kmeans_clustering(df)
    return df

df = get_data()

# ── Header ───────────────────────────────────────────────────────
st.title("🦠 Analiza e COVID-19 në Evropë")
st.divider()

# ── KPI Metrics ──────────────────────────────────────────────────
st.subheader("📊 Treguesit Kryesorë")
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("🌍 Vende", "20")
col2.metric("🦠 Rastet Totale", f"{df['total_cases'].sum()/1_000_000:.1f}M")
col3.metric("💀 Vdekjet Totale", f"{df['total_deaths'].sum()/1_000:.0f}K")
col4.metric("📉 CFR Mesatar", f"{df['CFR'].mean():.2f}%")
col5.metric("💉 Vaksinim Mesatar", f"{df['total_vaccinations_per_hundred'].mean():.1f}%")

st.divider()

# ── Tabs ─────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Bar Chart",
    "🥧 Pie Chart",
    "📈 Scatter Plot",
    "📉 Histogram",
    "🤖 K-Means",
    "📋 Statistika"
])

# ── Tab 1: Bar Chart ─────────────────────────────────────────────
with tab1:
    st.subheader("Figura 1: 10 Vendet me Rastet më të Larta")
    plot_bar_chart(df)
    st.image("outputs/figures/fig1_bar_chart.png", width=900)
    st.info("Franca dhe Gjermania dominojnë me mbi 38 milionë raste secila.")

# ── Tab 2: Pie Chart ─────────────────────────────────────────────
with tab2:
    st.subheader("Figura 2: Statusi Global i Pacientëve")
    plot_pie_chart(df)
    st.image("outputs/figures/fig2_pie_chart.png", width=900)
    cfr = df['total_deaths'].sum() / df['total_cases'].sum() * 100
    st.info(f"Nga të gjithë rastet, **{cfr:.2f}%** përfunduan me vdekje.")

# ── Tab 3: Scatter Plot ──────────────────────────────────────────
with tab3:
    st.subheader("Figura 3: GDP per Capita vs Vaksinimi")
    plot_scatter(df)
    st.image("outputs/figures/fig3_scatter_plot.png", width=900)
    r, p = pearson_gdp_vaccination(df)
    col1, col2 = st.columns(2)
    col1.metric("Pearson r", r)
    col2.metric("p-value", p)
    st.success(f"Korrelacion **i fortë** (r={r}) — vendet më të pasura vaksinuan më shumë.")

# ── Tab 4: Histogram ─────────────────────────────────────────────
with tab4:
    st.subheader("Figura 4: Shpërndarja e CFR")
    plot_histogram(df)
    st.image("outputs/figures/fig4_histogram.png", width=900)
    col1, col2 = st.columns(2)
    col1.metric("CFR Mesatar", f"{df['CFR'].mean():.2f}%")
    col2.metric("CFR Medianë", f"{df['CFR'].median():.2f}%")

# ── Tab 5: K-Means ───────────────────────────────────────────────
with tab5:
    st.subheader("Figura 5: K-Means Clustering — 3 Grupe")
    plot_kmeans(df)
    st.image("outputs/figures/fig5_kmeans.png", width=900)

    st.markdown("#### Shpërndarja e vendeve sipas grupeve:")
    col1, col2, col3 = st.columns(3)
    colors = ["🔵", "🔴", "🟢"]
    for i, col in enumerate([col1, col2, col3]):
        vendet = df[df["Cluster"] == i]["location"].tolist()
        col.markdown(f"**{colors[i]} Grupi {i}**")
        for v in vendet:
            col.write(f"• {v}")

# ── Tab 6: Statistika ────────────────────────────────────────────
with tab6:
    st.subheader("Tabela 1: Statistikat Përshkruese")
    stats_cols = ["total_cases", "total_deaths", "CFR",
                  "Cases_per_100k", "total_vaccinations_per_hundred", "gdp_per_capita"]
    st.dataframe(df[stats_cols].describe().round(2), use_container_width=True)

    st.subheader("Të dhënat e plota — 20 Vendet")
    st.dataframe(
        df[["location", "total_cases", "total_deaths", "CFR",
            "Cases_per_100k", "total_vaccinations_per_hundred",
            "gdp_per_capita", "Cluster"]].set_index("location").round(2),
        use_container_width=True
    )
