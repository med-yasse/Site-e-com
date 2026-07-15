from flask import Flask, render_template
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # backend non-interactif (pas d'affichage fenêtre)
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)
path = 'vis_project/'

# Palette commune pour tous les graphiques
PALETTE = ['#00d4aa', '#7c6fff', '#ff6b6b', '#ffd166', '#06d6a0',
           '#118ab2', '#ef476f', '#ffd60a', '#80b918', '#f4a261']

def apply_dark_style(ax, fig):
    #Applique un style sombre cohérent à tous les graphiques.
    fig.patch.set_facecolor('#0f1117')
    ax.set_facecolor('#1a1d2e')
    ax.tick_params(colors='#a0aec0', labelsize=10)
    ax.xaxis.label.set_color('#a0aec0')
    ax.yaxis.label.set_color('#a0aec0')
    ax.title.set_color('#e2e8f0')
    ax.title.set_fontsize(14)
    ax.title.set_fontweight('bold')
    for spine in ax.spines.values():
        spine.set_edgecolor('#2d3748')
    ax.grid(color='#2d3748', linestyle='--', linewidth=0.5, alpha=0.7)

@app.route('/')
def home():
    df = pd.read_csv(path + 'Sales_Transaction.csv')
    df['Total'] = df['Price'] * df['Quantity'] # S'assurer que la colonne Total est bien calculée

    # ── GRAPHE 1 : Distribution des ventes (histogramme log) ──────────────────
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.histplot(df['Total'], bins=50, log_scale=True, ax=ax, color='#00d4aa', edgecolor='#0f1117', alpha=0.85)

    ax.set_title('Sales Distribution (Log Scale)')
    ax.set_xlabel('Total Sale (€)')
    ax.set_ylabel('Frequency')
    apply_dark_style(ax, fig)

    plt.tight_layout()
    plt.savefig(path + 'static/sales_hist.png', dpi=120)
    plt.close()

    # ── GRAPHE 2 : Top 10 Produits par revenu ─────────────────────────────────
    top_products = (
        df.groupby('ProductName')['Total'].sum().sort_values(ascending=False).head(10)
    )
    fig, ax = plt.subplots(figsize=(11, 6))

    bars = ax.barh(top_products.index[::-1], top_products.values[::-1],
            color=PALETTE[:len(top_products)], edgecolor='none', height=0.65)
    # Valeurs au bout des barres
    for bar in bars:
        w = bar.get_width()
        ax.text(w * 1.01, bar.get_y() + bar.get_height() / 2,
                f'€{w:,.0f}', va='center', ha='left',
                color='#a0aec0', fontsize=9)
    ax.set_title('Top 10 Products by Revenue')
    ax.set_xlabel('Revenue (€)')
    ax.set_ylabel('')
    apply_dark_style(ax, fig)
    ax.margins(x=0.18)
    
    plt.tight_layout()
    plt.savefig(path + 'static/top_products.png', dpi=120)
    plt.close()

    # ── GRAPHE 3 : Top 10 Produits par volume de transactions ─────────────────
    top_qty = (
        df.groupby('ProductName')['Quantity'].sum()
        .sort_values(ascending=False).head(10)
    )

    fig, ax = plt.subplots(figsize=(11, 6))
    sns.barplot(x=top_qty.index, y=top_qty.values, ax=ax,
                palette=PALETTE[:len(top_qty)], edgecolor='none')
    ax.set_title('Top 10 Products by Quantity Sold')
    ax.set_xlabel('Product')
    ax.set_ylabel('Total Quantity')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=35, ha='right', fontsize=9)
    apply_dark_style(ax, fig)

    plt.tight_layout()
    plt.savefig(path + 'static/top_qty.png', dpi=120)
    plt.close()

    # ── GRAPHE 4 : Relation Prix vs Total (scatter) ───────────────────────────
    sample = df.sample(min(2000, len(df)), random_state=42)
    fig, ax = plt.subplots(figsize=(9, 5))

    ax.scatter(sample['Price'], sample['Total'], alpha=0.35, s=18, color='#7c6fff', edgecolors='none')
    # Ligne de tendance
    m, b = pd.np.polyfit(sample['Price'], sample['Total'], 1) if hasattr(pd, 'np') \
        else (__import__('numpy').polyfit(sample['Price'], sample['Total'], 1))
    
    xs = np.linspace(sample['Price'].min(), sample['Price'].max(), 200)
    ax.plot(xs, m * xs + b, color='#00d4aa', linewidth=1.8, label='Trend')
    ax.set_title('Price vs Total Sale')
    ax.set_xlabel('Unit Price (€)')
    ax.set_ylabel('Total Sale (€)')
    ax.legend(facecolor='#1a1d2e', labelcolor='#a0aec0', edgecolor='#2d3748')
    apply_dark_style(ax, fig)

    plt.tight_layout()
    plt.savefig(path + 'static/price_vs_total.png', dpi=120)
    plt.close()

    # ── GRAPHE 5 : Distribution des quantités achetées (boxplot) ──────────────
    fig, ax = plt.subplots(figsize=(9, 4))

    bp = ax.boxplot(df['Quantity'].dropna(), vert=False, patch_artist=True,
                    boxprops=dict(facecolor='#7c6fff', color='#a0aec0'),
                    medianprops=dict(color='#00d4aa', linewidth=2),
                    whiskerprops=dict(color='#a0aec0'),
                    capprops=dict(color='#a0aec0'),
                    flierprops=dict(marker='o', color='#ff6b6b',alpha=0.4, markersize=4))
    
    ax.set_title('Quantity per Transaction — Distribution')
    ax.set_xlabel('Quantity')
    ax.set_yticks([])
    apply_dark_style(ax, fig)

    plt.tight_layout()
    plt.savefig(path + 'static/qty_boxplot.png', dpi=120)
    plt.close()

    # ── Statistiques globales ─────────────────────────────────────────────────
    total_revenue    = round(df['Total'].sum(), 2)
    total_transactions = len(df)
    avg_order        = round(df['Total'].mean(), 2)
    avg_price        = round(df['Price'].mean(), 2)
    top_product_name = top_products.index[0]
    top_product_rev  = round(top_products.iloc[0], 2)
    unique_products  = df['ProductName'].nunique()

    stats = df[['Price', 'Quantity', 'Total']].describe().round(2).to_html(classes='stats-table', border=0)

    return render_template(
        'index.html',
        tables=stats,
        revenue=total_revenue,
        transactions=total_transactions,
        avg_order=avg_order,
        avg_price=avg_price,
        top_product_name=top_product_name,
        top_product_rev=top_product_rev,
        unique_products=unique_products,
    )

if __name__ == '__main__':
    app.run(debug=True)