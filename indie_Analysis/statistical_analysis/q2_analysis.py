# analysis/q2_analysis.py

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from .data_loader import load_games_data
from util.chart_config import COLORS, get_base_layout, get_axis_style

def prepare_q2_data():
    """Prepare data for Q2 price analysis"""
    df_games = load_games_data()
    
    # Create price buckets
    df_games.loc[df_games["is_free"] == True, "price_bucket"] = "Free"
    
    paid_mask = (df_games["is_free"] == False) & (df_games["price_eur"] > 0)
    bins = [0, 5, 10, 15, 20, 30, np.inf]
    labels = ["€0–4.99", "€5–9.99", "€10–14.99", "€15–19.99", "€20–29.99", "€30+"]
    
    df_games.loc[paid_mask, "price_bucket"] = pd.cut(
        df_games.loc[paid_mask, "price_eur"],
        bins=bins,
        labels=labels,
        right=False
    )
    
    return df_games, paid_mask

def create_histogram():
    """Create histogram of paid game prices"""
    df_games, paid_mask = prepare_q2_data()
    paid_prices = df_games.loc[paid_mask, "price_eur"]
    
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=paid_prices,
        nbinsx=150,
        marker=dict(
            color=COLORS['accent_blue'],
            line=dict(color=COLORS['primary_blue'], width=0.5)
        ),
        hovertemplate='<b>Prix:</b> €%{x:.2f}<br>' +
                      '<b>Nombre de jeux:</b> %{y}<br>' +
                      '<extra></extra>',
        name='Jeux'
    ))
    
    layout = get_base_layout('Distribution des Prix des Jeux Indés Payants (EUR)')
    layout['xaxis'] = get_axis_style('Prix (EUR)')
    layout['xaxis']['range'] = [0, 60]
    layout['xaxis']['dtick'] = 5
    layout['yaxis'] = get_axis_style('Nombre de jeux')
    
    fig.update_layout(**layout)
    
    return fig.to_html(include_plotlyjs='cdn', div_id='histogram-chart')

def create_price_buckets():
    """Create bar chart of price range buckets"""
    df_games, _ = prepare_q2_data()
    
    bucket_order = ["Free", "€0–4.99", "€5–9.99", "€10–14.99", "€15–19.99", "€20–29.99", "€30+"]
    bucket_counts = df_games["price_bucket"].value_counts().reindex(bucket_order)
    
    bar_colors = [
        COLORS['accent_blue'], COLORS['primary_blue'], COLORS['light_blue'],
        COLORS['primary_blue'], COLORS['light_blue'], COLORS['primary_blue'], COLORS['light_blue']
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=bucket_order,
        y=bucket_counts,
        marker=dict(color=bar_colors, line=dict(color=COLORS['accent_blue'], width=1.5)),
        text=[f'{int(val):,}' if not pd.isna(val) else '0' for val in bucket_counts],
        textposition='outside',
        textfont=dict(size=12, color=COLORS['text_white']),
        hovertemplate='<b>Tranche:</b> %{x}<br><b>Nombre:</b> %{y:,}<br><extra></extra>',
    ))
    
    layout = get_base_layout('Jeux Indés par Tranche de Prix')
    layout['xaxis'] = get_axis_style('Tranche de prix (EUR)', grid=False)
    layout['xaxis']['tickangle'] = -45
    layout['yaxis'] = get_axis_style('Nombre de jeux indés')
    layout['margin']['b'] = 100
    layout['showlegend'] = False
    
    fig.update_layout(**layout)
    
    return fig.to_html(include_plotlyjs='cdn', div_id='buckets-chart')

def get_statistics():
    """Calculate price statistics"""
    df_games, paid_mask = prepare_q2_data()
    paid_prices = df_games.loc[paid_mask, "price_eur"]
    
    return {
        'total_games': len(df_games),
        'free_games': int((df_games['is_free'] == True).sum()),
        'paid_games': int(paid_mask.sum()),
        'median_price': float(paid_prices.median()),
        'average_price': float(paid_prices.mean()),
        'under_10': int(((paid_prices > 0) & (paid_prices < 10)).sum()),
        'percent_under_10': float((((paid_prices > 0) & (paid_prices < 10)).sum() / paid_mask.sum() * 100) if paid_mask.sum() > 0 else 0)
    }