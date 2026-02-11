# dashboard_defjam_records.py
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import re
from datetime import datetime
import warnings
import base64
import io
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="ANALYSE STRATÉGIQUE - DEF JAM RECORDINGS",
    page_icon="🎶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé avec thème Def Jam (noir, rouge, urban)
st.markdown("""
<style>
    .main {
        color: #ffffff !important;
        background-color: #000000 !important;
    }
    
    .stApp {
        background-color: #000000 !important;
        color: #ffffff !important;
    }
    
    .main-header {
        font-size: 3rem;
        color: #FF0000 !important;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        border-bottom: 3px solid #FF0000;
        padding-bottom: 1rem;
        text-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
        background: linear-gradient(90deg, #000000, #330000, #000000);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Franklin Gothic Heavy', 'Arial Black', sans-serif;
        letter-spacing: 1px;
    }
    
    .academic-card {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
        border: 1px solid #444444;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(255, 0, 0, 0.1);
        color: #ffffff !important;
        transition: all 0.3s ease;
    }
    
    .academic-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 0, 0, 0.3);
        border-color: #FF0000;
    }
    
    .simmons-card { 
        border-left: 5px solid #FF0000; 
        background: linear-gradient(135deg, #1a0a0a 0%, #2d1a1a 100%);
    }
    .llcoolj-card { 
        border-left: 5px solid #4169E1; 
        background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2d 100%);
    }
    .jayz-card { 
        border-left: 5px solid #FFD700; 
        background: linear-gradient(135deg, #1a1a0a 0%, #2d2d1a 100%);
    }
    .kanye-card { 
        border-left: 5px solid #800080; 
        background: linear-gradient(135deg, #1a0a1a 0%, #2d1a2d 100%);
    }
    .rza-card { 
        border-left: 5px solid #C0C0C0; 
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
    }
    .methodman-card { 
        border-left: 5px solid #00FF00; 
        background: linear-gradient(135deg, #0a1a0a 0%, #1a2d1a 100%);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #FF0000 !important;
        margin: 0.5rem 0;
        text-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
        font-family: 'Franklin Gothic Heavy', 'Arial Black', sans-serif;
        letter-spacing: 1px;
    }
    
    .section-title {
        color: #ffffff !important;
        border-bottom: 2px solid #FF0000;
        padding-bottom: 0.5rem;
        margin: 2rem 0 1rem 0;
        font-size: 1.6rem;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(255, 0, 0, 0.2);
        font-family: 'Franklin Gothic Heavy', 'Arial Black', sans-serif;
        letter-spacing: 1px;
    }
    
    .subsection-title {
        color: #ffffff !important;
        border-left: 4px solid #FF0000;
        padding-left: 1rem;
        margin: 1.5rem 0 1rem 0;
        font-size: 1.3rem;
        font-weight: 600;
        font-family: 'Arial', sans-serif;
    }
    
    .stMarkdown {
        color: #ffffff !important;
    }
    
    p, div, span, h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    .secondary-text {
        color: #cccccc !important;
    }
    
    .light-text {
        color: #999999 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #0a0a0a;
        border-radius: 8px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1a1a1a;
        border-radius: 5px;
        color: #ffffff !important;
        font-weight: 500;
        border: 1px solid #444444;
        transition: all 0.3s ease;
        font-family: 'Arial', sans-serif;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #2d2d2d;
        border-color: #FF0000;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #FF0000 !important;
        color: #000000 !important;
        font-weight: 600;
        border-color: #FF0000;
    }
    
    .card-content {
        color: #ffffff !important;
    }
    
    .card-secondary {
        color: #cccccc !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #FF0000 0%, #CC0000 100%);
        color: #ffffff;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 0, 0, 0.3);
        font-family: 'Arial', sans-serif;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #FF3333 0%, #FF0000 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 0, 0, 0.5);
    }
    
    .stDataFrame {
        background-color: #0a0a0a;
        color: #ffffff;
    }
    
    .stSelectbox > div > div {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    .stSlider > div > div > div {
        background-color: #FF0000;
    }
    
    /* Style pour les graphiques Plotly */
    .js-plotly-plot .plotly .modebar {
        background-color: rgba(10, 10, 10, 0.8) !important;
    }
    
    .js-plotly-plot .plotly .modebar-btn {
        background-color: transparent !important;
        color: #ffffff !important;
    }
    
    /* Def Jam Badge */
    .defjam-badge {
        display: inline-block;
        background: #000000;
        color: #FF0000;
        padding: 5px 15px;
        border-radius: 20px;
        border: 2px solid #FF0000;
        font-weight: bold;
        font-size: 0.9rem;
        margin: 0 5px 10px 0;
        font-family: 'Arial', sans-serif;
        text-transform: uppercase;
    }
    
    /* Urban Style Elements */
    .urban-glow {
        position: relative;
    }
    
    .urban-glow::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #FF0000, #000000, #FF0000);
        z-index: -1;
        border-radius: 12px;
        opacity: 0.3;
    }
    
    /* Record Label Effect */
    .record-icon {
        display: inline-block;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: linear-gradient(45deg, #FF0000, #000000);
        margin-right: 5px;
        border: 2px solid #FF0000;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0a0a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #444444;
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #555555;
    }
    
    /* Street Style */
    .street-text {
        font-family: 'Arial Black', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

class DefJamAnalyzer:
    def __init__(self):
        # Définition de la palette de couleurs pour Def Jam
        self.color_palette = {
            'RICK RUBIN': '#FF0000',        # Rouge Def Jam
            'RUSSELL SIMMONS': '#4169E1',   # Bleu
            'LL COOL J': '#FFD700',         # Or
            'JAY-Z': '#000000',             # Noir premium
            'KANYE WEST': '#800080',        # Pourpre
            'RZA': '#C0C0C0',               # Argent
            'METHOD MAN': '#00FF00',        # Vert
            'BEASTIE BOYS': '#FF4500',      # Orange rouge
            'PUBLIC ENEMY': '#000080',      # Bleu marine
            'Période 80s': '#FF0000',
            'Période 90s': '#4169E1',
            'Période 2000s': '#FFD700'
        }
        
        # Couleurs pour les types de données
        self.data_colors = {
            'Ventes': '#FF0000',
            'Albums': '#4169E1',
            'Artistes': '#FFD700',
            'Revenus': '#00FF00',
            'Influence': '#800080'
        }
        
        self.initialize_data()
        
    def initialize_data(self):
        """Initialise les données complètes sur Def Jam Recordings"""
        
        # Données principales sur le label
        self.label_data = {
            'fondation': 1984,
            'fondateur': 'Rick Rubin, Russell Simmons',
            'statut': 'Label major (Universal Music Group)',
            'siege': 'New York City, New York, USA',
            'specialisation': 'Hip-hop, R&B, Urban music',
            'philosophie': "Original, authentic, street music",
            'distribution': 'Universal Music Group (monde entier)'
        }

        # Données des artistes principaux
        self.artists_data = {
            'RICK RUBIN': {
                'debut': 1984,
                'genre': 'Hip-hop, Rock, Production',
                'albums_defjam': 30,
                'ventes_totales': 50000000,
                'succes_principal': 'Co-fondateur, producteur légendaire',
                'statut': 'Co-fondateur et producteur',
                'impact': 'Visionnaire, pont hip-hop/rock',
                'annees_activite': '1984-1988 (en tant que co-fondateur)',
                'albums_principaux': ['Licensed to Ill (Beastie Boys)', 'Raising Hell (Run-DMC)'],
                'chiffre_affaires_estime': 200000000,
                'public_cible': 'Tous genres, innovateurs',
                'tournees': 'Production uniquement'
            },
            'RUSSELL SIMMONS': {
                'debut': 1984,
                'genre': 'Hip-hop, Business',
                'albums_defjam': 40,
                'ventes_totales': 60000000,
                'succes_principal': 'Visionnaire commercial',
                'statut': 'Co-fondateur et businessman',
                'impact': 'Commercialisation du hip-hop',
                'annees_activite': '1984-1999',
                'albums_principaux': ['Business ventures', 'Label development'],
                'chiffre_affaires_estime': 300000000,
                'public_cible': 'Mainstream, entreprise',
                'tournees': 'Business development'
            },
            'LL COOL J': {
                'debut': 1985,
                'genre': 'Hip-hop, R&B',
                'albums_defjam': 13,
                'ventes_totales': 15000000,
                'succes_principal': 'Radio (1985)',
                'statut': 'Première superstar du label',
                'impact': 'Pionnier rap romantique',
                'annees_activite': '1985-2013',
                'albums_principaux': ['Radio', 'Mama Said Knock You Out', 'Mr. Smith'],
                'chiffre_affaires_estime': 80000000,
                'public_cible': 'Mainstream, femmes',
                'tournees': 'Mondiales'
            },
            'JAY-Z': {
                'debut': 1996,
                'genre': 'Hip-hop, Business',
                'albums_defjam': 11,
                'ventes_totales': 50000000,
                'succes_principal': 'Reasonable Doubt (1996)',
                'statut': 'CEO et légende',
                'impact': 'Businessman, icône culturelle',
                'annees_activite': '1996-2017 (CEO 2004-2007)',
                'albums_principaux': ['Reasonable Doubt', 'The Blueprint', 'The Black Album'],
                'chiffre_affaires_estime': 1000000000,
                'public_cible': 'Global, luxe, business',
                'tournees': 'Mondiales'
            },
            'KANYE WEST': {
                'debut': 2004,
                'genre': 'Hip-hop, Pop, Experimental',
                'albums_defjam': 6,
                'ventes_totales': 35000000,
                'succes_principal': 'The College Dropout (2004)',
                'statut': 'Artiste innovateur',
                'impact': 'Fusion hip-hop/fashion/art',
                'annees_activite': '2004-2016',
                'albums_principaux': ['The College Dropout', 'Late Registration', 'My Beautiful Dark Twisted Fantasy'],
                'chiffre_affaires_estime': 250000000,
                'public_cible': 'Fashion, art, mainstream',
                'tournees': 'Mondiales innovantes'
            },
            'RZA': {
                'debut': 1993,
                'genre': 'Hip-hop, Production',
                'albums_defjam': 5,
                'ventes_totales': 8000000,
                'succes_principal': 'Enter the Wu-Tang (36 Chambers)',
                'statut': 'Leader Wu-Tang Clan',
                'impact': 'Production innovante, philosophie',
                'annees_activite': '1993-2005',
                'albums_principaux': ['Enter the Wu-Tang', 'Liquid Swords (production)'],
                'chiffre_affaires_estime': 40000000,
                'public_cible': 'Underground, philosophie',
                'tournees': 'Internationales'
            },
            'METHOD MAN': {
                'debut': 1994,
                'genre': 'Hip-hop, Hardcore rap',
                'albums_defjam': 4,
                'ventes_totales': 6000000,
                'succes_principal': 'Tical (1994)',
                'statut': 'Membre Wu-Tang, star solo',
                'impact': 'Charisme, voix distinctive',
                'annees_activite': '1994-2006',
                'albums_principaux': ['Tical', 'Tical 2000: Judgement Day'],
                'chiffre_affaires_estime': 30000000,
                'public_cible': 'Hardcore, mainstream',
                'tournees': 'Nationales'
            },
            'BEASTIE BOYS': {
                'debut': 1986,
                'genre': 'Hip-hop, Rock',
                'albums_defjam': 1,
                'ventes_totales': 10000000,
                'succes_principal': 'Licensed to Ill (1986)',
                'statut': 'Premier groupe blanc de hip-hop',
                'impact': 'Croisement hip-hop/rock',
                'annees_activite': '1986-1987',
                'albums_principaux': ['Licensed to Ill'],
                'chiffre_affaires_estime': 50000000,
                'public_cible': 'Rock, hip-hop, alternative',
                'tournees': 'Mondiales'
            },
            'PUBLIC ENEMY': {
                'debut': 1987,
                'genre': 'Hip-hop, Politique',
                'albums_defjam': 3,
                'ventes_totales': 5000000,
                'succes_principal': 'It Takes a Nation of Millions to Hold Us Back (1988)',
                'statut': 'Groupe politique légendaire',
                'impact': 'Hip-hop politique, conscience sociale',
                'annees_activite': '1987-1991',
                'albums_principaux': ['Yo! Bum Rush the Show', 'It Takes a Nation...', 'Fear of a Black Planet'],
                'chiffre_affaires_estime': 25000000,
                'public_cible': 'Politique, activistes',
                'tournees': 'Internationales politiques'
            }
        }

        # Données chronologiques détaillées
        self.timeline_data = [
            {'annee': 1984, 'evenement': 'Fondation par Rick Rubin dans son dortoir', 'type': 'Structure', 'importance': 10},
            {'annee': 1985, 'evenement': 'Signature de LL Cool J - premier album solo', 'type': 'Artiste', 'importance': 9},
            {'annee': 1986, 'evenement': 'Licensed to Ill (Beastie Boys) - premier #1 hip-hop', 'type': 'Album', 'importance': 10},
            {'annee': 1987, 'evenement': 'Signature de Public Enemy', 'type': 'Artiste', 'importance': 9},
            {'annee': 1988, 'evenement': 'It Takes a Nation... (Public Enemy)', 'type': 'Album', 'importance': 10},
            {'annee': 1988, 'evenement': 'Départ de Rick Rubin', 'type': 'Structure', 'importance': 8},
            {'annee': 1990, 'evenement': 'Mama Said Knock You Out (LL Cool J)', 'type': 'Album', 'importance': 9},
            {'annee': 1993, 'evenement': 'Enter the Wu-Tang (36 Chambers)', 'type': 'Album', 'importance': 10},
            {'annee': 1996, 'evenement': 'Signature de Jay-Z', 'type': 'Artiste', 'importance': 10},
            {'annee': 1999, 'evenement': 'Vente à Universal Music Group', 'type': 'Business', 'importance': 9},
            {'annee': 2004, 'evenement': 'The College Dropout (Kanye West)', 'type': 'Album', 'importance': 10},
            {'annee': 2004, 'evenement': 'Jay-Z devient CEO', 'type': 'Structure', 'importance': 9},
            {'annee': 2007, 'evenement': 'Jay-Z quitte le poste de CEO', 'type': 'Structure', 'importance': 8},
            {'annee': 2010, 'evenement': 'My Beautiful Dark Twisted Fantasy (Kanye)', 'type': 'Album', 'importance': 9},
            {'annee': 2017, 'evenement': '40 ans d\'anniversaire', 'type': 'Événement', 'importance': 7},
            {'annee': 2021, 'evenement': 'Vente des masters à Sony', 'type': 'Business', 'importance': 8}
        ]

        # Données financières et commerciales
        self.financial_data = {
            'RICK RUBIN': {
                'ventes_albums': 50000000,
                'chiffre_affaires': 200000000,
                'rentabilite': 85,
                'cout_production_moyen': 500000,
                'budget_marketing_moyen': 2000000,
                'roi': 800,
                'influence_culturelle': 10
            },
            'RUSSELL SIMMONS': {
                'ventes_albums': 60000000,
                'chiffre_affaires': 300000000,
                'rentabilite': 80,
                'cout_production_moyen': 400000,
                'budget_marketing_moyen': 3000000,
                'roi': 750,
                'influence_culturelle': 9
            },
            'LL COOL J': {
                'ventes_albums': 15000000,
                'chiffre_affaires': 80000000,
                'rentabilite': 75,
                'cout_production_moyen': 300000,
                'budget_marketing_moyen': 1500000,
                'roi': 600,
                'influence_culturelle': 8
            },
            'JAY-Z': {
                'ventes_albums': 50000000,
                'chiffre_affaires': 1000000000,
                'rentabilite': 90,
                'cout_production_moyen': 1000000,
                'budget_marketing_moyen': 5000000,
                'roi': 1000,
                'influence_culturelle': 10
            },
            'KANYE WEST': {
                'ventes_albums': 35000000,
                'chiffre_affaires': 250000000,
                'rentabilite': 85,
                'cout_production_moyen': 800000,
                'budget_marketing_moyen': 3000000,
                'roi': 900,
                'influence_culturelle': 10
            },
            'RZA': {
                'ventes_albums': 8000000,
                'chiffre_affaires': 40000000,
                'rentabilite': 70,
                'cout_production_moyen': 200000,
                'budget_marketing_moyen': 800000,
                'roi': 500,
                'influence_culturelle': 9
            },
            'METHOD MAN': {
                'ventes_albums': 6000000,
                'chiffre_affaires': 30000000,
                'rentabilite': 68,
                'cout_production_moyen': 150000,
                'budget_marketing_moyen': 600000,
                'roi': 450,
                'influence_culturelle': 8
            },
            'BEASTIE BOYS': {
                'ventes_albums': 10000000,
                'chiffre_affaires': 50000000,
                'rentabilite': 78,
                'cout_production_moyen': 250000,
                'budget_marketing_moyen': 1000000,
                'roi': 550,
                'influence_culturelle': 9
            },
            'PUBLIC ENEMY': {
                'ventes_albums': 5000000,
                'chiffre_affaires': 25000000,
                'rentabilite': 65,
                'cout_production_moyen': 100000,
                'budget_marketing_moyen': 500000,
                'roi': 400,
                'influence_culturelle': 10
            }
        }

        # Données de stratégie marketing
        self.marketing_data = {
            'RICK RUBIN': {
                'strategie': 'Authenticité brute, minimalisme, fusion genres',
                'cibles': 'Puristes, innovateurs, cross-genre',
                'canaux': ['Radio college', 'Clubs underground', 'Presse spécialisée'],
                'budget_ratio': 20,
                'succes': 'Visionnaire',
                'innovations': 'Production minimaliste, fusion hip-hop/rock'
            },
            'RUSSELL SIMMONS': {
                'strategie': 'Commercialisation mainstream, branding',
                'cibles': 'Mainstream, entreprises, médias',
                'canaux': ['MTV', 'Radio commerciale', 'Fashion', 'TV'],
                'budget_ratio': 30,
                'succes': 'Business genius',
                'innovations': 'Commercialisation du hip-hop'
            },
            'LL COOL J': {
                'strategie': 'Charisme, accessibilité, romance',
                'cibles': 'Femmes, mainstream, jeunes',
                'canaux': ['MTV', 'Radio pop', 'Cinéma', 'TV'],
                'budget_ratio': 25,
                'succes': 'Superstar',
                'innovations': 'Rap romantique mainstream'
            },
            'JAY-Z': {
                'strategie': 'Luxe, business, exclusivité',
                'cibles': 'Luxe, business, global',
                'canaux': ['Événements VIP', 'Marques luxe', 'Business media'],
                'budget_ratio': 35,
                'succes': 'Icône business',
                'innovations': 'Hip-hop comme business empire'
            },
            'KANYE WEST': {
                'strategie': 'Art, fashion, controverse maîtrisée',
                'cibles': 'Fashion, art, avant-garde',
                'canaux': ['Fashion shows', 'Art galleries', 'Social media viral'],
                'budget_ratio': 40,
                'succes': 'Innovateur',
                'innovations': 'Hip-hop comme art total'
            },
            'RZA': {
                'strategie': 'Philosophie, mysticisme, underground',
                'cibles': 'Intellectuels, underground, philosophie',
                'canaux': ['Cinéma', 'Conférences', 'Presse underground'],
                'budget_ratio': 18,
                'succes': 'Cult',
                'innovations': 'Hip-hop philosophique'
            },
            'METHOD MAN': {
                'strategie': 'Charisme naturel, humour, street',
                'cibles': 'Street, humour, mainstream',
                'canaux': ['Cinéma', 'TV shows', 'Features'],
                'budget_ratio': 22,
                'succes': 'Personnalité',
                'innovations': 'Marketing par personnalité'
            },
            'BEASTIE BOYS': {
                'strategie': 'Humoristique, rock attitude, rebellion',
                'cibles': 'Rock fans, alternative, humour',
                'canaux': ['Radio rock', 'MTV', 'Festivals'],
                'budget_ratio': 28,
                'succes': 'Crossover',
                'innovations': 'Hip-hop blanc accessible'
            },
            'PUBLIC ENEMY': {
                'strategie': 'Politique, militant, intellectuel',
                'cibles': 'Activistes, intellectuels, politique',
                'canaux': ['Conférences', 'Presse politique', 'Universités'],
                'budget_ratio': 20,
                'succes': 'Conscience',
                'innovations': 'Hip-hop comme arme politique'
            }
        }

        # Données de production
        self.production_data = {
            'RICK RUBIN': {
                'albums_produits': 30,
                'duree_contrat': 4,
                'rythme_sorties': 0.5,
                'qualite_production': 10,
                'autonomie_artistique': 10,
                'support_label': 9,
                'style_production': 'Minimaliste, samples bruts, fusion'
            },
            'RUSSELL SIMMONS': {
                'albums_produits': 40,
                'duree_contrat': 15,
                'rythme_sorties': 0.75,
                'qualite_production': 8,
                'autonomie_artistique': 9,
                'support_label': 10,
                'style_production': 'Commercial, accessible, mainstream'
            },
            'LL COOL J': {
                'albums_produits': 13,
                'duree_contrat': 28,
                'rythme_sorties': 2.15,
                'qualite_production': 8,
                'autonomie_artistique': 7,
                'support_label': 9,
                'style_production': 'Romantique, pop, accessible'
            },
            'JAY-Z': {
                'albums_produits': 11,
                'duree_contrat': 21,
                'rythme_sorties': 1.9,
                'qualite_production': 9,
                'autonomie_artistique': 9,
                'support_label': 10,
                'style_production': 'Luxe, business, storytelling'
            },
            'KANYE WEST': {
                'albums_produits': 6,
                'duree_contrat': 12,
                'rythme_sorties': 2.0,
                'qualite_production': 10,
                'autonomie_artistique': 10,
                'support_label': 9,
                'style_production': 'Expérimental, orchestral, innovant'
            },
            'RZA': {
                'albums_produits': 5,
                'duree_contrat': 12,
                'rythme_sorties': 2.4,
                'qualite_production': 9,
                'autonomie_artistique': 8,
                'support_label': 8,
                'style_production': 'Samples kung-fu, minimaliste, philosophique'
            },
            'METHOD MAN': {
                'albums_produits': 4,
                'duree_contrat': 12,
                'rythme_sorties': 3.0,
                'qualite_production': 8,
                'autonomie_artistique': 7,
                'support_label': 8,
                'style_production': 'Hardcore, humoristique, charismatique'
            },
            'BEASTIE BOYS': {
                'albums_produits': 1,
                'duree_contrat': 1,
                'rythme_sorties': 1.0,
                'qualite_production': 9,
                'autonomie_artistique': 8,
                'support_label': 9,
                'style_production': 'Rock/Hip-hop fusion, humoristique'
            },
            'PUBLIC ENEMY': {
                'albums_produits': 3,
                'duree_contrat': 4,
                'rythme_sorties': 1.33,
                'qualite_production': 9,
                'autonomie_artistique': 9,
                'support_label': 8,
                'style_production': 'Politique, samples denses, messages'
            }
        }

        # Données de gestion et management
        self.management_data = {
            'structure': {
                'type': 'Label major avec indépendance créative',
                'effectif': 120,
                'departements': ['A&R', 'Production', 'Marketing', 'Commercial', 'Legal', 'International'],
                'processus_decision': 'Mixte (créatif/commercial)',
                'culture_entreprise': 'Street credibility meets corporate'
            },
            'ressources_humaines': {
                'turnover': 'Moyen',
                'expertise': 'Hip-hop tradition et innovation',
                'reseautage': 'Global, multi-industries',
                'formation': 'Professionnelle et street'
            },
            'finances': {
                'model_economique': 'Major label avec catalogue historique',
                'marge_nette': '25-30%',
                'investissement_artistes': 'Mixte (stars et développement)',
                'risque': 'Contrôlé'
            },
            'relations_artistes': {
                'approche': 'Partnership, long-term development',
                'contrats': 'Standards major avec flexibilité',
                'communication': 'Professionnelle, directe',
                'loyaute': 'Variable selon époque'
            }
        }

    def display_header(self):
        """Affiche l'en-tête du dashboard"""
        st.markdown('<h1 class="main-header">🎶 DEF JAM RECORDINGS - DASHBOARD STRATÉGIQUE</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #cccccc; font-size: 1.2rem; margin-bottom: 2rem; font-family: Arial, sans-serif;">Label légendaire de hip-hop - Analyse complète 1984-2024</p>', unsafe_allow_html=True)
        
        # Métriques principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_ventes = sum(self.financial_data[artist]['ventes_albums'] for artist in self.financial_data)
            st.markdown(f"""
            <div class="academic-card simmons-card">
                <div style="color: {self.color_palette['RICK RUBIN']}; font-size: 1rem; font-weight: 600; text-align: center;">💿 VENTES TOTALES</div>
                <div class="metric-value" style="color: {self.color_palette['RICK RUBIN']}; text-align: center;">{total_ventes/1000000:.0f}M</div>
                <div style="color: #cccccc; text-align: center;">Albums vendus mondialement</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_artistes = len(self.artists_data)
            st.markdown(f"""
            <div class="academic-card llcoolj-card">
                <div style="color: {self.color_palette['LL COOL J']}; font-size: 1rem; font-weight: 600; text-align: center;">👑 LÉGENDES</div>
                <div class="metric-value" style="color: {self.color_palette['LL COOL J']}; text-align: center;">{total_artistes}</div>
                <div style="color: #cccccc; text-align: center;">Artistes iconiques</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_albums = sum(self.artists_data[artist]['albums_defjam'] for artist in self.artists_data)
            st.markdown(f"""
            <div class="academic-card jayz-card">
                <div style="color: {self.color_palette['JAY-Z']}; font-size: 1rem; font-weight: 600; text-align: center;">🎵 ALBUMS</div>
                <div class="metric-value" style="color: {self.color_palette['JAY-Z']}; text-align: center;">{total_albums}</div>
                <div style="color: #cccccc; text-align: center;">Classiques du label</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            influence_totale = sum(self.financial_data[artist]['influence_culturelle'] for artist in self.financial_data)
            st.markdown(f"""
            <div class="academic-card kanye-card">
                <div style="color: {self.color_palette['KANYE WEST']}; font-size: 1rem; font-weight: 600; text-align: center;">🌟 INFLUENCE</div>
                <div class="metric-value" style="color: {self.color_palette['KANYE WEST']}; text-align: center;">{influence_totale}/90</div>
                <div style="color: #cccccc; text-align: center;">Score culturel</div>
            </div>
            """, unsafe_allow_html=True)

    def create_artist_analysis(self):
        """Analyse complète des artistes"""
        st.markdown('<h3 class="section-title">👑 PANTHÉON DES LÉGENDES</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">📊 Influence Culturelle vs Ventes</div>', unsafe_allow_html=True)
            self.create_influence_sales_chart()
        
        with col2:
            st.markdown('<div class="subsection-title">📈 ROI Culturel</div>', unsafe_allow_html=True)
            self.create_cultural_roi_chart()
        
        # Analyse détaillée par artiste
        st.markdown('<div class="subsection-title">🔍 Profils Légendaires</div>', unsafe_allow_html=True)
        self.create_detailed_artist_analysis()

    def create_influence_sales_chart(self):
        """Graphique influence vs ventes"""
        artists = list(self.artists_data.keys())
        influence = [self.financial_data[artist]['influence_culturelle'] for artist in artists]
        ventes_normalisees = [min(10, self.financial_data[artist]['ventes_albums'] / 5000000) for artist in artists]
        
        fig = go.Figure()
        
        for i, artist in enumerate(artists):
            fig.add_trace(go.Scatter(
                x=[influence[i]],
                y=[ventes_normalisees[i]],
                mode='markers+text',
                marker=dict(
                    size=80, 
                    color=self.color_palette[artist], 
                    opacity=0.9,
                    line=dict(width=3, color='#ffffff')
                ),
                text=[artist],
                textposition="middle center",
                textfont=dict(color='white', size=12, weight='bold'),
                name=artist,
                showlegend=True
            ))
        
        fig.update_layout(
            title='Influence Culturelle vs Ventes Commerciales',
            xaxis_title='Influence Culturelle (1-10)',
            yaxis_title='Ventes Normalisées (1-10)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#FF0000',
                borderwidth=1,
                font=dict(color='white', size=10)
            ),
            xaxis=dict(range=[6, 10.5], tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(range=[0, 10.5], tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_cultural_roi_chart(self):
        """Graphique ROI culturel"""
        artists = list(self.financial_data.keys())
        roi = [self.financial_data[artist]['roi'] for artist in artists]
        influence = [self.financial_data[artist]['influence_culturelle'] for artist in artists]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=artists,
            y=roi,
            mode='lines+markers',
            line=dict(color='#FF0000', width=3),
            marker=dict(
                size=12,
                color=[self.color_palette[artist] for artist in artists]
            ),
            name='ROI (%)'
        ))
        
        fig.add_trace(go.Scatter(
            x=artists,
            y=[i * 100 for i in influence],  # Multiplier pour échelle similaire
            mode='lines+markers',
            line=dict(color='#4169E1', width=3, dash='dash'),
            marker=dict(
                size=12,
                color=[self.color_palette[artist] for artist in artists]
            ),
            name='Influence (x100)'
        ))
        
        fig.update_layout(
            title='ROI vs Influence Culturelle',
            xaxis_title='Artistes',
            yaxis_title='Valeurs',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#FF0000',
                borderwidth=1,
                font=dict(color='white', size=12)
            ),
            xaxis=dict(tickfont=dict(size=10), gridcolor='#333333'),
            yaxis=dict(tickfont=dict(size=10), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_detailed_artist_analysis(self):
        """Analyse détaillée par artiste"""
        artists = list(self.artists_data.keys())
        tabs = st.tabs(artists)
        
        for i, artist in enumerate(artists):
            with tabs[i]:
                couleur = self.color_palette[artist]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Informations générales
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {couleur}20 0%, {couleur}05 100%); padding: 1rem; border-radius: 8px; border-left: 5px solid {couleur}; margin-bottom: 1rem;">
                        <div style="color: {couleur}; font-weight: bold; font-size: 1.5rem; margin-bottom: 0.5rem;">{artist}</div>
                        <div style="color: #cccccc; font-size: 1.1rem; font-weight: 500;">{self.artists_data[artist]['genre']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Métriques clés
                    st.metric("Albums Def Jam", self.artists_data[artist]['albums_defjam'])
                    st.metric("Ventes totales", f"{self.financial_data[artist]['ventes_albums']/1000000:.1f}M")
                    st.metric("Influence culturelle", f"{self.financial_data[artist]['influence_culturelle']}/10")
                    
                    # Style production
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; margin-top: 1rem; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Style:</div>
                        <div style="color: #ffffff; font-style: italic; font-size: 1.1rem;">{self.production_data[artist]['style_production']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Caractéristiques commerciales
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Performance:</div>
                        <ul style="color: #ffffff; font-weight: 500;">
                            <li>Rentabilité: {self.financial_data[artist]['rentabilite']}%</li>
                            <li>ROI: {self.financial_data[artist]['roi']}%</li>
                            <li>Coût production: ${self.financial_data[artist]['cout_production_moyen']/1000:.0f}k</li>
                            <li>Budget marketing: ${self.financial_data[artist]['budget_marketing_moyen']/1000:.0f}k</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Graphique radar des caractéristiques
                    categories = ['Influence', 'Qualité', 'ROI', 'Innovation']
                    valeurs = [
                        self.financial_data[artist]['influence_culturelle'] * 10,
                        self.production_data[artist]['qualite_production'] * 10,
                        min(100, self.financial_data[artist]['roi'] / 10),
                        100 if self.marketing_data[artist]['innovations'] in ['Production minimaliste', 'Commercialisation du hip-hop'] else
                        90 if self.marketing_data[artist]['innovations'] in ['Hip-hop comme business', 'Hip-hop comme art'] else
                        80
                    ]
                    
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatterpolar(
                        r=valeurs + [valeurs[0]],
                        theta=categories + [categories[0]],
                        fill='toself',
                        line=dict(color=couleur, width=3),
                        marker=dict(size=8, color=couleur),
                        name=artist
                    ))
                    
                    fig.update_layout(
                        polar=dict(
                            bgcolor='#1a1a1a',
                            radialaxis=dict(
                                visible=True, 
                                range=[0, 100],
                                gridcolor='#333333',
                                tickfont=dict(color='#ffffff', size=12),
                                linecolor='#444444'
                            ),
                            angularaxis=dict(
                                gridcolor='#333333',
                                tickfont=dict(color='#ffffff', size=12),
                                linecolor='#444444'
                            )
                        ),
                        paper_bgcolor='#0a0a0a',
                        font=dict(color='#ffffff', size=14),
                        showlegend=False,
                        height=300,
                        title=f"Profil Légendaire - {artist}"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)

    def create_production_analysis(self):
        """Analyse de la production"""
        st.markdown('<h3 class="section-title">🎛️ ÉVOLUTION DE LA PRODUCTION</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">⏳ Rythme de Production par Époque</div>', unsafe_allow_html=True)
            self.create_production_pace_chart()
        
        with col2:
            st.markdown('<div class="subsection-title">⚗️ Qualité vs Autonomie</div>', unsafe_allow_html=True)
            self.create_quality_autonomy_chart()
        
        # Analyse des styles
        st.markdown('<div class="subsection-title">🎨 Évolution des Styles</div>', unsafe_allow_html=True)
        self.create_production_evolution_analysis()

    def create_production_pace_chart(self):
        """Graphique rythme de production"""
        artists = list(self.production_data.keys())
        rythme = [self.production_data[artist]['rythme_sorties'] for artist in artists]
        albums = [self.production_data[artist]['albums_produits'] for artist in artists]
        
        fig = go.Figure()
        
        for i, artist in enumerate(artists):
            fig.add_trace(go.Scatter(
                x=[rythme[i]],
                y=[albums[i]],
                mode='markers+text',
                marker=dict(
                    size=60, 
                    color=self.color_palette[artist], 
                    opacity=0.9,
                    line=dict(width=2, color='#ffffff')
                ),
                text=[artist],
                textposition="middle center",
                textfont=dict(color='white', size=10, weight='bold'),
                name=artist
            ))
        
        fig.update_layout(
            title='Rythme de Production vs Nombre d\'Albums',
            xaxis_title='Rythme (années entre albums)',
            yaxis_title="Nombre d'albums produits",
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            showlegend=False,
            xaxis=dict(tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_quality_autonomy_chart(self):
        """Graphique qualité vs autonomie"""
        artists = list(self.production_data.keys())
        qualite = [self.production_data[artist]['qualite_production'] for artist in artists]
        autonomie = [self.production_data[artist]['autonomie_artistique'] for artist in artists]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=qualite,
            y=autonomie,
            mode='markers+text',
            marker=dict(
                size=60,
                color=[self.color_palette[artist] for artist in artists],
                opacity=0.9
            ),
            text=artists,
            textposition="top center",
            textfont=dict(color='white', size=10, weight='bold')
        ))
        
        fig.update_layout(
            title='Qualité de Production vs Autonomie Artistique',
            xaxis_title='Qualité de Production (1-10)',
            yaxis_title='Autonomie Artistique (1-10)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            showlegend=False,
            xaxis=dict(range=[7, 10.5], tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(range=[6, 10.5], tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

        def create_quality_autonomy_chart(self):
        """Graphique qualité vs autonomie"""
        artists = list(self.production_data.keys())
        qualite = [self.production_data[artist]['qualite_production'] for artist in artists]
        autonomie = [self.production_data[artist]['autonomie_artistique'] for artist in artists]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=qualite,
            y=autonomie,
            mode='markers+text',
            marker=dict(
                size=60,
                color=[self.color_palette[artist] for artist in artists],
                opacity=0.9
            ),
            text=artists,
            textposition="top center",
            textfont=dict(color='white', size=10, weight='bold')
        ))
        
        fig.update_layout(
            title='Qualité de Production vs Autonomie Artistique',
            xaxis_title='Qualité de Production (1-10)',
            yaxis_title='Autonomie Artistique (1-10)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            showlegend=False,
            xaxis=dict(range=[7, 10.5], tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(range=[6, 10.5], tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_production_evolution_analysis(self):  # <-- CETTE LIGNE DOIT AVOIR 4 ESPACES
        """Analyse de l'évolution des styles"""
        # Groupes par décennies
        decennies = {
            '1980s': ['RICK RUBIN', 'RUSSELL SIMMONS', 'LL COOL J', 'BEASTIE BOYS', 'PUBLIC ENEMY'],
            '1990s': ['RZA', 'METHOD MAN'],
            '2000s+': ['JAY-Z', 'KANYE WEST']
        }
        
        # Définir les couleurs pour chaque décennie
        couleurs = {
            '1980s': '#FF0000',  # Rouge
            '1990s': '#4169E1',  # Bleu
            '2000s+': '#FFD700'  # Or
        }
        
        fig = go.Figure()
        
        for decennie, artistes in decennies.items():
            if artistes:
                # Calculer la moyenne de qualité pour la décennie
                qualite_moyenne = np.mean([self.production_data[a]['qualite_production'] for a in artistes if a in self.production_data])
                autonomie_moyenne = np.mean([self.production_data[a]['autonomie_artistique'] for a in artistes if a in self.production_data])
                
                # Vérifier que les valeurs sont valides
                if not np.isnan(qualite_moyenne) and not np.isnan(autonomie_moyenne):
                    fig.add_trace(go.Scatter(
                        x=[qualite_moyenne],
                        y=[autonomie_moyenne],
                        mode='markers',
                        marker=dict(
                            size=120,
                            color=couleurs.get(decennie, '#FFFFFF'),
                            opacity=0.8,
                            line=dict(width=3, color='#ffffff')
                        ),
                        text=[decennie],
                        textposition="middle center",
                        textfont=dict(color='white', size=14, weight='bold'),
                        name=decennie,
                        showlegend=True
                    ))
        
        fig.update_layout(
            title='Évolution des Styles par Décennie',
            xaxis_title='Qualité Moyenne (1-10)',
            yaxis_title='Autonomie Moyenne (1-10)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#FF0000',
                borderwidth=1,
                font=dict(color='white', size=12)
            ),
            xaxis=dict(range=[7, 9.5], tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(range=[7, 9.5], tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_marketing_analysis(self):  # <-- Cette méthode doit aussi avoir 4 espaces
        """Analyse des stratégies marketing"""
        st.markdown('<h3 class="section-title">🎯 STRATÉGIES MARKETING ÉVOLUTIVES</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">📈 Budgets vs Innovation</div>', unsafe_allow_html=True)
            self.create_marketing_innovation_chart()
        
        with col2:
            st.markdown('<div class="subsection-title">🎪 Canaux par Époque</div>', unsafe_allow_html=True)
            self.create_marketing_channels_evolution()
        
        # Analyse des innovations
        st.markdown('<div class="subsection-title">✨ Révolution Marketing</div>', unsafe_allow_html=True)
        self.create_marketing_revolution_analysis()

    def create_marketing_analysis(self):
        """Analyse des stratégies marketing"""
        st.markdown('<h3 class="section-title">🎯 STRATÉGIES MARKETING ÉVOLUTIVES</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">📈 Budgets vs Innovation</div>', unsafe_allow_html=True)
            self.create_marketing_innovation_chart()
        
        with col2:
            st.markdown('<div class="subsection-title">🎪 Canaux par Époque</div>', unsafe_allow_html=True)
            self.create_marketing_channels_evolution()
        
        # Analyse des innovations
        st.markdown('<div class="subsection-title">✨ Révolution Marketing</div>', unsafe_allow_html=True)
        self.create_marketing_revolution_analysis()

    def create_marketing_innovation_chart(self):
        """Graphique marketing vs innovation"""
        artists = list(self.marketing_data.keys())
        budget_ratios = [self.marketing_data[artist]['budget_ratio'] for artist in artists]
        succes = [10 if self.marketing_data[artist]['succes'] == 'Visionnaire' else 
                 9 if self.marketing_data[artist]['succes'] == 'Business genius' else
                 8 if self.marketing_data[artist]['succes'] in ['Superstar', 'Icône business', 'Innovateur'] else
                 7 for artist in artists]
        
        fig = go.Figure()
        
        for i, artist in enumerate(artists):
            fig.add_trace(go.Scatter(
                x=[budget_ratios[i]],
                y=[succes[i]],
                mode='markers+text',
                marker=dict(
                    size=80, 
                    color=self.color_palette[artist], 
                    opacity=0.9,
                    line=dict(width=3, color='#ffffff')
                ),
                text=[artist],
                textposition="middle center",
                textfont=dict(color='white', size=10, weight='bold'),
                name=artist
            ))
        
        fig.update_layout(
            title='Budget Marketing vs Innovation Stratégique',
            xaxis_title='Ratio Budget Marketing (%)',
            yaxis_title='Innovation Stratégique (1-10)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            showlegend=False,
            xaxis=dict(range=[15, 45], tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(range=[6, 11], tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_marketing_channels_evolution(self):
        """Analyse de l'évolution des canaux marketing"""
        # Canaux par décennie
        canaux_par_decennie = {
            '1980s': ['Radio college', 'Clubs underground', 'Presse spécialisée', 'MTV'],
            '1990s': ['MTV', 'Radio commerciale', 'Cinéma', 'TV'],
            '2000s+': ['Événements VIP', 'Marques luxe', 'Business media', 'Fashion shows', 'Social media']
        }
        
        # Créer un graphique à barres groupées
        fig = go.Figure()
        
        decennies = list(canaux_par_decennie.keys())
        for i, decennie in enumerate(decennies):
            canaux = canaux_par_decennie[decennie]
            fig.add_trace(go.Bar(
                name=decennie,
                x=[decennie] * len(canaux),
                y=[1] * len(canaux),
                text=canaux,
                textposition='auto',
                marker_color=['#FF0000', '#4169E1', '#FFD700'][i],
                opacity=0.8
            ))
        
        fig.update_layout(
            title='Évolution des Canaux Marketing par Décennie',
            xaxis_title='Décennie',
            yaxis_title='Nombre de Canaux',
            barmode='group',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_marketing_revolution_analysis(self):
        """Analyse de la révolution marketing"""
        innovations_par_decennie = {
            '1980s': ['Production minimaliste', 'Fusion hip-hop/rock', 'Commercialisation du hip-hop'],
            '1990s': ['Rap romantique mainstream', 'Hip-hop philosophique'],
            '2000s+': ['Hip-hop comme business empire', 'Hip-hop comme art total']
        }
        
        # Afficher les innovations par décennie
        cols = st.columns(3)
        
        for i, (decennie, innovations) in enumerate(innovations_par_decennie.items()):
            with cols[i]:
                couleur = {'1980s': '#FF0000', '1990s': '#4169E1', '2000s+': '#FFD700'}[decennie]
                st.markdown(f"""
                <div class="academic-card urban-glow">
                    <div style="text-align: center;">
                        <h4 style="color: {couleur}; font-weight: bold; margin: 10px 0;">{decennie}</h4>
                        <div style="margin-top: 10px;">
                """, unsafe_allow_html=True)
                
                for innovation in innovations:
                    st.markdown(f"""
                    <div style="background: {couleur}20; padding: 8px; margin: 5px 0; border-radius: 5px; border-left: 3px solid {couleur};">
                        <span style="color: #ffffff; font-weight: 500;">{innovation}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div></div>", unsafe_allow_html=True)

    def create_management_analysis(self):
        """Analyse de la gestion et management"""
        st.markdown('<h3 class="section-title">🏢 ÉVOLUTION DU MANAGEMENT</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">📊 Modèles de Gestion</div>', unsafe_allow_html=True)
            self.create_management_models_chart()
        
        with col2:
            st.markdown('<div class="subsection-title">💼 Économie du Label</div>', unsafe_allow_html=True)
            self.create_label_economics()
        
        # Analyse SWOT
        st.markdown('<div class="subsection-title">🔍 Analyse SWOT Historique</div>', unsafe_allow_html=True)
        self.create_swot_analysis()

    def create_management_models_chart(self):
        """Graphique des modèles de gestion"""
        # Modèles par période
        periodes = ['Fondation (1984-1988)', 'Expansion (1989-1999)', 'Major Label (2000-2010)', 'Moderne (2011-présent)']
        creativite = [10, 8, 7, 6]
        commercial = [5, 8, 9, 8]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=periodes,
            y=creativite,
            mode='lines+markers',
            name='Créativité',
            line=dict(color='#FF0000', width=3),
            marker=dict(size=10, color='#FF0000')
        ))
        
        fig.add_trace(go.Scatter(
            x=periodes,
            y=commercial,
            mode='lines+markers',
            name='Commercial',
            line=dict(color='#4169E1', width=3),
            marker=dict(size=10, color='#4169E1')
        ))
        
        fig.update_layout(
            title='Évolution: Créativité vs Commercial',
            xaxis_title='Période',
            yaxis_title='Score (1-10)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#FF0000',
                borderwidth=1,
                font=dict(color='white', size=12)
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_label_economics(self):
        """Économie du label"""
        # Créer un graphique d'évolution des revenus
        annees = ['1985', '1990', '1995', '2000', '2005', '2010', '2015', '2020']
        revenus = [10, 50, 100, 200, 300, 250, 200, 180]  # En millions
        marges = [15, 20, 25, 30, 28, 25, 22, 20]  # En pourcentage
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(x=annees, y=revenus, name="Revenus (M$)", line=dict(color='#FF0000', width=3)),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Scatter(x=annees, y=marges, name="Marge (%)", line=dict(color='#FFD700', width=3, dash='dash')),
            secondary_y=True,
        )
        
        fig.update_layout(
            title='Évolution des Revenus et Marges',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#FF0000',
                borderwidth=1,
                font=dict(color='white', size=12)
            )
        )
        
        fig.update_xaxes(title_text="Année", gridcolor='#333333')
        fig.update_yaxes(title_text="Revenus (M$)", secondary_y=False, gridcolor='#333333')
        fig.update_yaxes(title_text="Marge (%)", secondary_y=True, gridcolor='#333333')
        
        st.plotly_chart(fig, use_container_width=True)

    def create_swot_analysis(self):
        """Analyse SWOT"""
        # Créer un graphique radar pour l'analyse SWOT
        categories = ['Forces', 'Faiblesses', 'Opportunités', 'Menaces']
        valeurs = [9, 4, 8, 6]  # Scores sur 10
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=valeurs + [valeurs[0]],
            theta=categories + [categories[0]],
            fill='toself',
            line=dict(color='#FF0000', width=3),
            marker=dict(size=8, color='#FF0000'),
            name='Analyse SWOT'
        ))
        
        fig.update_layout(
            polar=dict(
                bgcolor='#1a1a1a',
                radialaxis=dict(
                    visible=True, 
                    range=[0, 10],
                    gridcolor='#333333',
                    tickfont=dict(color='#ffffff', size=12),
                    linecolor='#444444'
                ),
                angularaxis=dict(
                    gridcolor='#333333',
                    tickfont=dict(color='#ffffff', size=12),
                    linecolor='#444444'
                )
            ),
            paper_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            showlegend=False,
            height=400,
            title="Analyse SWOT - Label Historique"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Afficher les détails de l'analyse SWOT
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="academic-card simmons-card">
                <h4 style="color: #FF0000; text-align: center; font-weight: bold;">FORCES</h4>
                <ul style="color: #ffffff; font-weight: 500; font-size: 0.9rem;">
                    <li>Catalogue historique inégalé</li>
                    <li>Brand recognition mondiale</li>
                    <li>Légendes multiples générations</li>
                    <li>Réseau Universal Music</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="academic-card llcoolj-card">
                <h4 style="color: #4169E1; text-align: center; font-weight: bold;">FAIBLESSES</h4>
                <ul style="color: #ffffff; font-weight: 500; font-size: 0.9rem;">
                    <li>Dépendance au catalogue ancien</li>
                    <li>Difficulté à lancer nouveaux talents</li>
                    <li>Structure bureaucratique</li>
                    <li>Coûts fixes élevés</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="academic-card jayz-card">
                <h4 style="color: #FFD700; text-align: center; font-weight: bold;">OPPORTUNITÉS</h4>
                <ul style="color: #ffffff; font-weight: 500; font-size: 0.9rem;">
                    <li>Streaming du catalogue historique</li>
                    <li>Documentaires et biopics</li>
                    <li>Collaborations intergénérationnelles</li>
                    <li>Brand extensions (fashion, etc.)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="academic-card kanye-card">
                <h4 style="color: #800080; text-align: center; font-weight: bold;">MENACES</h4>
                <ul style="color: #ffffff; font-weight: 500; font-size: 0.9rem;">
                    <li>Concurrence des labels indépendants</li>
                    <li>Changement des habitudes d'écoute</li>
                    <li>Vieillissement du catalogue</li>
                    <li>Érosion de la marque</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    def create_timeline_analysis(self):
        """Analyse chronologique"""
        st.markdown('<h3 class="section-title">📜 CHRONOLOGIE HISTORIQUE</h3>', unsafe_allow_html=True)
        
        # Créer un DataFrame pour la timeline
        df_timeline = pd.DataFrame(self.timeline_data)
        
        fig = go.Figure()
        
        # Ajouter les événements par type
        types_couleurs = {
            'Structure': '#FF0000',
            'Artiste': '#4169E1',
            'Album': '#FFD700',
            'Business': '#00FF00',
            'Événement': '#800080'
        }
        
        for event_type in df_timeline['type'].unique():
            df_type = df_timeline[df_timeline['type'] == event_type]
            fig.add_trace(go.Scatter(
                x=df_type['annee'],
                y=[1] * len(df_type),
                mode='markers',
                marker=dict(
                    size=df_type['importance'] * 12,
                    color=types_couleurs[event_type],
                    opacity=0.8,
                    line=dict(width=2, color='#ffffff')
                ),
                text=[f"{row['evenement']}<br>Importance: {row['importance']}/10" 
                      for _, row in df_type.iterrows()],
                hoverinfo='text',
                name=event_type
            ))
        
        # Ajouter une ligne de temps
        fig.add_trace(go.Scatter(
            x=df_timeline['annee'],
            y=[1] * len(df_timeline),
            mode='lines',
            line=dict(color='#555555', width=2, dash='dash'),
            showlegend=False
        ))
        
        fig.update_layout(
            title='Timeline Historique Def Jam Recordings',
            xaxis_title='Année',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=500,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#FF0000',
                borderwidth=1,
                font=dict(color='white', size=12)
            ),
            yaxis=dict(
                showticklabels=False,
                range=[0.8, 1.2]
            ),
            hovermode='closest'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Analyse par décennies
        st.markdown('<div class="subsection-title">📊 Impact par Décennie</div>', unsafe_allow_html=True)
        self.create_decade_analysis()

    def create_decade_analysis(self):
        """Analyse de l'impact par décennie"""
        decades = {
            '1984-1989': ['RICK RUBIN', 'RUSSELL SIMMONS', 'LL COOL J', 'BEASTIE BOYS', 'PUBLIC ENEMY'],
            '1990-1999': ['RZA', 'METHOD MAN'],
            '2000-2009': ['JAY-Z', 'KANYE WEST'],
            '2010-2024': []  # Période moderne
        }
        
        # Calcul des métriques par décennie
        decades_stats = {}
        for decade, artists in decades.items():
            if artists:
                total_sales = sum(self.financial_data[a]['ventes_albums'] for a in artists)
                total_influence = sum(self.financial_data[a]['influence_culturelle'] for a in artists)
                avg_roi = np.mean([self.financial_data[a]['roi'] for a in artists])
                decades_stats[decade] = {
                    'ventes': total_sales / 1000000,  # En millions
                    'influence': total_influence / len(artists),
                    'roi': avg_roi,
                    'artistes': len(artists)
                }
            else:
                decades_stats[decade] = {'ventes': 50, 'influence': 6, 'roi': 300, 'artistes': 0}  # Estimations pour période moderne
        
        # Créer un graphique à barres groupées
        decades_list = list(decades_stats.keys())
        ventes = [decades_stats[d]['ventes'] for d in decades_list]
        influence = [decades_stats[d]['influence'] * 10 for d in decades_list]  # Multiplier pour échelle
        artistes = [decades_stats[d]['artistes'] for d in decades_list]
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Bar(
                name='Ventes (M$)',
                x=decades_list,
                y=ventes,
                marker_color='#FF0000',
                opacity=0.8
            ),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Scatter(
                name='Influence (x10)',
                x=decades_list,
                y=influence,
                mode='lines+markers',
                line=dict(color='#4169E1', width=3),
                marker=dict(size=10, color='#4169E1')
            ),
            secondary_y=True,
        )
        
        fig.update_layout(
            title='Performance par Décennie',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            barmode='group',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#FF0000',
                borderwidth=1,
                font=dict(color='white', size=12)
            )
        )
        
        fig.update_xaxes(title_text="Décennie", gridcolor='#333333')
        fig.update_yaxes(title_text="Ventes (M$)", secondary_y=False, gridcolor='#333333')
        fig.update_yaxes(title_text="Influence (score)", secondary_y=True, gridcolor='#333333')
        
        st.plotly_chart(fig, use_container_width=True)

    def create_financial_analysis(self):
        """Analyse financière complète"""
        st.markdown('<h3 class="section-title">💰 ANALYSE FINANCIÈRE</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">📈 ROI par Artiste</div>', unsafe_allow_html=True)
            self.create_roi_analysis()
        
        with col2:
            st.markdown('<div class="subsection-title">💸 Structure des Coûts</div>', unsafe_allow_html=True)
            self.create_cost_structure_analysis()
        
        # Analyse de rentabilité
        st.markdown('<div class="subsection-title">📊 Rentabilité Comparative</div>', unsafe_allow_html=True)
        self.create_profitability_analysis()

    def create_roi_analysis(self):
        """Analyse du ROI par artiste"""
        artists = list(self.financial_data.keys())
        roi_values = [self.financial_data[artist]['roi'] for artist in artists]
        ventes = [self.financial_data[artist]['ventes_albums'] / 1000000 for artist in artists]  # En millions
        
        # Créer un graphique bubble
        fig = go.Figure()
        
        for i, artist in enumerate(artists):
            fig.add_trace(go.Scatter(
                x=[roi_values[i]],
                y=[ventes[i]],
                mode='markers',
                marker=dict(
                    size=ventes[i] * 2,
                    color=self.color_palette[artist],
                    opacity=0.8,
                    line=dict(width=2, color='#ffffff')
                ),
                text=[f"{artist}<br>ROI: {roi_values[i]}%<br>Ventes: {ventes[i]:.1f}M"],
                hoverinfo='text',
                name=artist
            ))
        
        fig.update_layout(
            title='ROI vs Ventes par Artiste',
            xaxis_title='ROI (%)',
            yaxis_title='Ventes (Millions)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            showlegend=False,
            xaxis=dict(gridcolor='#333333'),
            yaxis=dict(gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_cost_structure_analysis(self):
        """Analyse de la structure des coûts"""
        artists = list(self.financial_data.keys())[:5]  # Prendre les 5 premiers pour lisibilité
        
        production_costs = [self.financial_data[artist]['cout_production_moyen'] / 1000 for artist in artists]
        marketing_costs = [self.financial_data[artist]['budget_marketing_moyen'] / 1000 for artist in artists]
        
        fig = go.Figure(data=[
            go.Bar(
                name='Coût Production (k$)',
                x=artists,
                y=production_costs,
                marker_color='#FF0000',
                text=production_costs,
                textposition='auto'
            ),
            go.Bar(
                name='Budget Marketing (k$)',
                x=artists,
                y=marketing_costs,
                marker_color='#4169E1',
                text=marketing_costs,
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title='Structure des Coûts par Artiste',
            xaxis_title='Artistes',
            yaxis_title='Coûts (k$)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            barmode='group',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#FF0000',
                borderwidth=1,
                font=dict(color='white', size=12)
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_profitability_analysis(self):
        """Analyse de rentabilité comparative"""
        # Calculer plusieurs métriques de rentabilité
        metrics_data = []
        for artist in self.financial_data:
            metrics_data.append({
                'Artiste': artist,
                'Rentabilité (%)': self.financial_data[artist]['rentabilite'],
                'ROI (%)': self.financial_data[artist]['roi'],
                'Ventes (M)': self.financial_data[artist]['ventes_albums'] / 1000000,
                'CA (M$)': self.financial_data[artist]['chiffre_affaires'] / 1000000
            })
        
        df_metrics = pd.DataFrame(metrics_data)
        
        # Normaliser les données pour le radar chart
        df_normalized = df_metrics.copy()
        for col in ['Rentabilité (%)', 'ROI (%)', 'Ventes (M)', 'CA (M$)']:
            df_normalized[col] = (df_metrics[col] - df_metrics[col].min()) / (df_metrics[col].max() - df_metrics[col].min()) * 100
        
        # Sélectionner quelques artistes pour le radar
        selected_artists = ['JAY-Z', 'KANYE WEST', 'RICK RUBIN', 'LL COOL J']
        
        fig = go.Figure()
        
        for artist in selected_artists:
            row = df_normalized[df_normalized['Artiste'] == artist].iloc[0]
            values = [
                row['Rentabilité (%)'],
                row['ROI (%)'],
                row['Ventes (M)'],
                row['CA (M$)']
            ]
            
            fig.add_trace(go.Scatterpolar(
                r=values + [values[0]],
                theta=['Rentabilité', 'ROI', 'Ventes', 'CA'] + ['Rentabilité'],
                fill='toself',
                name=artist,
                line=dict(color=self.color_palette[artist], width=2),
                opacity=0.7
            ))
        
        fig.update_layout(
            polar=dict(
                bgcolor='#1a1a1a',
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    gridcolor='#333333',
                    tickfont=dict(color='#ffffff', size=12)
                ),
                angularaxis=dict(
                    gridcolor='#333333',
                    tickfont=dict(color='#ffffff', size=12)
                )
            ),
            paper_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=500,
            title="Rentabilité Comparative",
            legend=dict(
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#FF0000',
                borderwidth=1,
                font=dict(color='white', size=12)
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_cultural_impact_analysis(self):
        """Analyse de l'impact culturel"""
        st.markdown('<h3 class="section-title">🌍 IMPACT CULTUREL</h3>', unsafe_allow_html=True)
        
        # Impact par domaine
        impact_domains = {
            'Musique': 9.5,
            'Mode': 8.0,
            'Business': 9.0,
            'Politique': 7.5,
            'Langage': 8.5,
            'Social': 8.0
        }
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(impact_domains.keys()),
                y=list(impact_domains.values()),
                marker_color=['#FF0000', '#4169E1', '#FFD700', '#00FF00', '#800080', '#C0C0C0'],
                text=list(impact_domains.values()),
                textposition='auto',
                texttemplate='%{y:.1f}'
            )
        ])
        
        fig.update_layout(
            title='Impact Culturel par Domaine (1-10)',
            xaxis_title='Domaines',
            yaxis_title='Score d\'Impact',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            yaxis=dict(range=[0, 10])
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Citations et légendes
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="academic-card simmons-card">
                <h4 style="color: #FF0000; text-align: center; font-weight: bold;">LEGACY</h4>
                <p style="color: #ffffff; font-style: italic; text-align: center; font-size: 1.1rem;">
                    "Def Jam n'est pas juste un label, c'est une culture"
                </p>
                <p style="color: #cccccc; text-align: center; font-size: 0.9rem;">
                    - Russell Simmons
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="academic-card jayz-card">
                <h4 style="color: #FFD700; text-align: center; font-weight: bold;">INNOVATION</h4>
                <p style="color: #ffffff; font-style: italic; text-align: center; font-size: 1.1rem;">
                    "Le hip-hop a fait plus pour le dialogue racial que la politique"
                </p>
                <p style="color: #cccccc; text-align: center; font-size: 0.9rem;">
                    - Jay-Z
                </p>
            </div>
            """, unsafe_allow_html=True)

    def create_strategic_recommendations(self):
        """Recommandations stratégiques"""
        st.markdown('<h3 class="section-title">🎯 RECOMMANDATIONS STRATÉGIQUES</h3>', unsafe_allow_html=True)
        
        # Catégories de recommandations
        recommendations = {
            'Catalogue Historique': [
                'Digitaliser et remasteriser le catalogue complet',
                'Créer des box sets thématiques par décennie',
                'Développer des partenariats streaming exclusifs'
            ],
            'Nouveaux Talents': [
                'Créer un incubateur pour jeunes artistes',
                'Système de mentorat avec les légendes',
                'Label indépendant sous marque Def Jam'
            ],
            'Brand Extension': [
                'Ligne de vêtements "Def Jam Classics"',
                'Documentaires et séries sur l\'histoire du label',
                'Expériences live immersives (concerts VR)'
            ],
            'Innovation Digitale': [
                'NFTs des albums historiques',
                'Plateforme de contenu exclusif',
                'Intelligence artificielle pour découverte artistique'
            ]
        }
        
        # Afficher les recommandations sous forme de cartes
        cols = st.columns(4)
        
        for i, (categorie, recommandations_list) in enumerate(recommendations.items()):
            with cols[i]:
                couleurs = ['#FF0000', '#4169E1', '#FFD700', '#00FF00']
                st.markdown(f"""
                <div class="academic-card urban-glow">
                    <div style="text-align: center;">
                        <h4 style="color: {couleurs[i]}; font-weight: bold; margin: 10px 0;">{categorie}</h4>
                        <div style="margin-top: 10px;">
                """, unsafe_allow_html=True)
                
                for rec in recommandations_list:
                    st.markdown(f"""
                    <div style="background: {couleurs[i]}20; padding: 8px; margin: 5px 0; border-radius: 5px; border-left: 3px solid {couleurs[i]};">
                        <span style="color: #ffffff; font-weight: 500; font-size: 0.9rem;">{rec}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Plan d'action
        st.markdown('<div class="subsection-title">📅 Plan d\'Action Prioritaire</div>', unsafe_allow_html=True)
        
        timeline_data = [
            {'Phase': 'Court terme (0-6 mois)', 'Actions': ['Audit du catalogue numérique', 'Lancement incubateur', 'Premiers partenariats NFT']},
            {'Phase': 'Moyen terme (6-18 mois)', 'Actions': ['Série documentaire', 'Ligne merchandise', 'Plateforme contenu exclusif']},
            {'Phase': 'Long terme (18-36 mois)', 'Actions': ['Acquisitions stratégiques', 'Expansion internationale', 'Écosystème complet']}
        ]
        
        for phase in timeline_data:
            st.markdown(f"""
            <div class="academic-card" style="margin: 10px 0; padding: 15px;">
                <h5 style="color: #FF0000; margin-bottom: 10px;">{phase['Phase']}</h5>
                <ul style="color: #ffffff; font-weight: 500;">
            """, unsafe_allow_html=True)
            
            for action in phase['Actions']:
                st.markdown(f"<li>{action}</li>", unsafe_allow_html=True)
            
            st.markdown("</ul></div>", unsafe_allow_html=True)

    def create_conclusion(self):
        """Section de conclusion"""
        st.markdown('<h3 class="section-title">🏁 CONCLUSION STRATÉGIQUE</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="academic-card simmons-card">
                <h4 style="color: #FF0000; text-align: center; font-weight: bold;">HERITAGE</h4>
                <p style="color: #ffffff; text-align: justify; font-size: 1rem;">
                    Def Jam Recordings représente l'un des chapitres les plus importants de l'histoire 
                    culturelle moderne. De son humble début dans un dortoir universitaire à son statut 
                    d'empire musical, le label a démontré une capacité unique à identifier et développer 
                    des talents visionnaires.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="academic-card jayz-card">
                <h4 style="color: #FFD700; text-align: center; font-weight: bold;">FUTURE</h4>
                <p style="color: #ffffff; text-align: justify; font-size: 1rem;">
                    Pour les 40 prochaines années, Def Jam doit équilibrer la préservation de son 
                    héritage avec l'innovation nécessaire pour rester pertinent. La marque possède 
                    un capital culturel inestimable qui peut être activé de multiples façons dans 
                    l'économie numérique moderne.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Score final
        st.markdown('<div class="subsection-title">🏆 Score Stratégique Final</div>', unsafe_allow_html=True)
        
        scores = {
            'Héritage Culturel': 95,
            'Potentiel Innovation': 75,
            'Résilience Business': 80,
            'Capital Marque': 90,
            'Adaptabilité': 70
        }
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=list(scores.values()) + [list(scores.values())[0]],
            theta=list(scores.keys()) + [list(scores.keys())[0]],
            fill='toself',
            line=dict(color='#FF0000', width=3),
            marker=dict(size=8, color='#FF0000'),
            name='Def Jam 2024'
        ))
        
        fig.update_layout(
            polar=dict(
                bgcolor='#1a1a1a',
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    gridcolor='#333333',
                    tickfont=dict(color='#ffffff', size=12)
                ),
                angularaxis=dict(
                    gridcolor='#333333',
                    tickfont=dict(color='#ffffff', size=12)
                )
            ),
            paper_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            title="Profil Stratégique du Label",
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def run_dashboard(self):
        """Exécute le dashboard complet"""
        self.display_header()
        
        # Créer les onglets principaux
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "👑 ARTISTES", 
            "🎛️ PRODUCTION", 
            "🎯 MARKETING", 
            "🏢 MANAGEMENT", 
            "📜 HISTORIQUE", 
            "💰 FINANCES", 
            "🎯 STRATÉGIE"
        ])
        
        with tab1:
            self.create_artist_analysis()
        
        with tab2:
            self.create_production_analysis()
        
        with tab3:
            self.create_marketing_analysis()
        
        with tab4:
            self.create_management_analysis()
        
        with tab5:
            self.create_timeline_analysis()
            st.markdown("---")
            self.create_cultural_impact_analysis()
        
        with tab6:
            self.create_financial_analysis()
        
        with tab7:
            self.create_strategic_recommendations()
            st.markdown("---")
            self.create_conclusion()
        
        # Footer
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="text-align: center; color: #cccccc; font-size: 0.9rem;">
                <p>Dashboard Stratégique Def Jam Recordings - Analyse 1984-2024</p>
                <p>© 2024 - Tous droits réservés - À des fins éducatives uniquement</p>
            </div>
            """, unsafe_allow_html=True)

# Exécution principale
if __name__ == "__main__":
    analyzer = DefJamAnalyzer()
    analyzer.run_dashboard()
