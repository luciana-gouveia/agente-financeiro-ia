import streamlit as st
import pandas as pd
import plotly.express as px
import os
from llm_agent import responder

st.set_page_config(page_title="Finanças", page_icon="💰", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Montserrat', sans-serif !important;
    }

    [data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.1) !important;
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
        padding: 15px !important;
        border-radius: 10px !important;
    }

    [data-testid="stMetricValue"] {
        color: #2e7d32 !important; 
        font-weight: 700 !important;
    }

    @media (prefers-color-scheme: dark) {
        [data-testid="stMetricValue"] {
            color: #00ffa3 !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def formatar_br(valor):
    try:
        return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0,00"

@st.cache_data
def carregar_dados():
    arquivo = "dados_exemplo.csv"
    if not os.path.exists(arquivo):
        arquivo = os.path.join("..", "dados_exemplo.csv")
        if not os.path.exists(arquivo): 
            return None

    try:
        df = pd.read_csv(arquivo, sep=None, engine='python', encoding='utf-8-sig')
        df = df.rename(columns={df.columns[0]: 'Categoria', df.columns[1]: 'Valor'})
        
        def limpar(v):
            v = str(v).replace('R$', '').replace(' ', '').strip()
            if ',' in v and '.' in v: 
                v = v.replace(',', '')
            elif ',' in v: 
                v = v.replace('.', '').replace(',', '.')
            try: 
                return float(v)
            except: 
                return 0.0

        df['Valor'] = df['Valor'].apply(limpar)
        return df
    except:
        return None

df = carregar_dados()

with st.sidebar:
    st.title("💰 Finanças")
    menu = st.radio("Ir para:", ["Resumo", "Assistente"])
    st.divider()
    st.caption("v1.0")

if df is None:
    st.error("Arquivo 'dados_exemplo.csv' não encontrado.")
else:
    if menu == "Resumo":
        st.header("Resumo de Gastos")
        
        c1, c2, c3 = st.columns(3)
        with c1: 
            st.metric("Total", formatar_br(df['Valor'].sum()))
        with c2: 
            st.metric("Maior", formatar_br(df['Valor'].max()))
        with c3: 
            st.metric("Itens", len(df))

        st.markdown("---")

        g1, g2 = st.columns(2)
        with g1:
            fig_pie = px.pie(
                df, values='Valor', names='Categoria', hole=0.5,
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_pie.update_layout(
                margin=dict(t=0, b=0, l=0, r=0),
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with g2:
            fig_bar = px.bar(
                df, x='Categoria', y='Valor', color='Categoria',
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_bar.update_layout(
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_bar, use_container_width=True)

    elif menu == "Assistente":
        st.header("Assistente")
        pergunta = st.chat_input("Como posso ajudar?")
        if pergunta:
            with st.chat_message("user"): 
                st.write(pergunta)
            with st.chat_message("assistant"):
                resumo = f"Total gasto: {formatar_br(df['Valor'].sum())}. Categorias: {list(df['Categoria'].unique())}"
                st.write(responder(pergunta, resumo))