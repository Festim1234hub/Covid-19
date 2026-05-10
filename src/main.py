"""Pipeline kryesor i analizës COVID-19."""

from src.data.loader      import load_data, get_latest
from src.data.cleaner     import clean
from src.data.transformer import transform

from src.analysis.descriptive import save_stats
from src.analysis.correlation import print_results
from src.analysis.clustering  import kmeans_clustering

from src.visualization.bar_chart   import plot_bar_chart
from src.visualization.pie_chart   import plot_pie_chart
from src.visualization.scatter_plot import plot_scatter
from src.visualization.histogram   import plot_histogram
from src.visualization.kmeans_plot import plot_kmeans

from src.config import DATA_PROCESSED


def main() -> None:
    print("=" * 50)
    print("  COVID-19 European Data Analysis Pipeline")
    print("=" * 50)

    # 1. Ngarkimi i të dhënave
    print("\n[1/6] Duke ngarkuar të dhënat...")
    df_raw    = load_data()
    df_latest = get_latest(df_raw)
    print(f"      {len(df_latest)} vende të ngarkuara.")

    # 2. Pastrimi i të dhënave
    print("\n[2/6] Duke pastruar të dhënat (mean imputation)...")
    df_clean = clean(df_latest)

    # 3. Llogaritja e kolonave të reja (CFR, Cases_per_100k)
    print("\n[3/6] Duke llogaritur CFR dhe Cases_per_100k...")
    df = transform(df_clean)
    df.to_csv(DATA_PROCESSED, index=False)
    print(f"      Dataset i pastruar ruajtur: {DATA_PROCESSED}")

    # 4. Analiza statistikore
    print("\n[4/6] Duke kryer analizën statistikore...")
    save_stats(df)
    print_results(df)

    # 5. Të 5 grafikët
    print("\n[5/6] Duke gjeneruar grafikët...")
    plot_bar_chart(df)
    plot_pie_chart(df)
    plot_scatter(df)
    plot_histogram(df)

    df_clustered = kmeans_clustering(df)
    plot_kmeans(df_clustered)

    # 6. Përfundim
    print("\n[6/6] Pipeline përfundoi me sukses.")
    print("=" * 50)


if __name__ == "__main__":
    main()

