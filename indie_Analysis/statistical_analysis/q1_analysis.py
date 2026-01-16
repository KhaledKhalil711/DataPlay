# analysis/q1_analysis_static.py

import pandas as pd
import plotly.graph_objects as go
from .data_loader import load_games_data
from util.chart_config import COLORS
import os

OUTPUT_DIR = "static/Images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def prepare_q1_data():
    """
    Prépare les données pour l'analyse de l'engagement et des genres/tags.
    
    Returns:
        df_games (pd.DataFrame): DataFrame complet avec les colonnes nécessaires.
    """
    df_games = load_games_data()
    
    # Engagement moyen par genre
    genre_engagement = df_games.groupby('genre')['average_playtime_hours'].mean().sort_values(ascending=False)
    
    # Nombre de jeux par genre
    genre_count = df_games['genre'].value_counts().sort_values(ascending=False)
    
    # Top tags
    # On suppose que df_games['tags'] est une liste ou chaîne séparée par ;
    all_tags = df_games['tags'].dropna().str.split(';').explode()
    top_tags = all_tags.value_counts().head(10)
    
    return df_games, genre_engagement, genre_count, top_tags

def create_genre_engagement_png():
    """Graphique en barres de l'engagement moyen par genre."""
    _, genre_engagement, _, _ = prepare_q1_data()
    
    fig = go.Figure(go.Bar(
        x=genre_engagement.index,
        y=genre_engagement.values,
        marker=dict(color=COLORS['accent_blue'], line=dict(color=COLORS['primary_blue'], width=1.5)),
        text=[f"{v:.1f}h" for v in genre_engagement.values],
        textposition='outside'
    ))
    
    fig.update_layout(
        title="Engagement moyen par genre (heures de jeu)",
        xaxis_title="Genre",
        yaxis_title="Heures moyennes de jeu",
        xaxis_tickangle=-45,
        margin=dict(b=100)
    )
    
    path = os.path.join(OUTPUT_DIR, "q1_genre_engagement.png")
    fig.write_image(path, scale=2)
    return path

def create_genre_count_png():
    """Graphique en barres du nombre de jeux par genre."""
    _, _, genre_count, _ = prepare_q1_data()
    
    fig = go.Figure(go.Bar(
        x=genre_count.index,
        y=genre_count.values,
        marker=dict(color=COLORS['primary_blue'], line=dict(color=COLORS['accent_blue'], width=1.5)),
        text=[f"{v}" for v in genre_count.values],
        textposition='outside'
    ))
    
    fig.update_layout(
        title="Nombre de jeux par genre",
        xaxis_title="Genre",
        yaxis_title="Nombre de jeux",
        xaxis_tickangle=-45,
        margin=dict(b=100)
    )
    
    path = os.path.join(OUTPUT_DIR, "q1_genre_count.png")
    fig.write_image(path, scale=2)
    return path

def create_top_tags_png():
    """Graphique en barres des 10 tags les plus populaires."""
    _, _, _, top_tags = prepare_q1_data()
    
    fig = go.Figure(go.Bar(
        x=top_tags.index,
        y=top_tags.values,
        marker=dict(color=COLORS['light_blue'], line=dict(color=COLORS['primary_blue'], width=1.5)),
        text=[f"{v}" for v in top_tags.values],
        textposition='outside'
    ))
    
    fig.update_layout(
        title="Top 10 des tags les plus populaires",
        xaxis_title="Tag",
        yaxis_title="Nombre de jeux",
        xaxis_tickangle=-45,
        margin=dict(b=100)
    )
    
    path = os.path.join(OUTPUT_DIR, "q1_top_tags.png")
    fig.write_image(path, scale=2)
    return path

def get_q1_insights():
    """Retourne quelques statistiques clés pour Q1."""
    df_games, genre_engagement, genre_count, top_tags = prepare_q1_data()
    return {
        'total_games': len(df_games),
        'top_genre_engagement': genre_engagement.idxmax(),
        'top_genre_count': genre_count.idxmax(),
        'top_tag': top_tags.idxmax()
    }
