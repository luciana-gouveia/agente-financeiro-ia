import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import os
from data_loader import carregar_dados, resumo_financeiro
from llm_agent import responder

# Configuração da página
st.set_page_config(
    page_title="Dashboard Financeiro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título
st.title("📊 Dashboard Financeiro")
st.markdown("Análise simples e visual dos seus gastos.")

# Sidebar
st.sidebar.title("Menu")
opcao = st.sidebar.selectbox("Escolha uma opção", ["Dashboard", "Análise com IA"])

# Upload
st.info("Você pode enviar um arquivo CSV ou usar os dados de exemplo.")
arquivo = st.file_uploader("Envie seu CSV", type=["csv"])

# Caminho seguro do CSV
caminho_padrao = os.path.join(os.path.dirname(__file__), "..", "data", "dados_exemplo.csv")

# Carregar dados
if arquivo:
    df = carregar_dados(arquivo)
else:
    df = carregar_dados(caminho_padrao)

# Validação do CSV
if "categoria" not in df.columns or "valor" not in df.columns:
    st.error("O CSV deve conter as colunas: categoria e valor")
    st.stop()

# Resumo
resumo = resumo_financeiro(df)

# =========================
# DASHBOARD
# =========================
if opcao == "Dashboard":

    st.markdown("## 📊 Visão Geral")

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Total gasto", f"R$ {resumo['total']:.2f}")
    col2.metric("📊 Média por gasto", f"R$ {resumo['media']:.2f}")
    col3.metric("🏆 Maior categoria", resumo["maior_categoria"])

    st.markdown("## 📈 Gastos por categoria")

    fig, ax = plt.subplots()
    ax.bar(df["categoria"], df["valor"])

    ax.set_title("Gastos por Categoria")
    ax.set_xlabel("Categoria")
    ax.set_ylabel("Valor (R$)")

    plt.xticks(rotation=30)
    plt.tight_layout()

    st.pyplot(fig)

    st.markdown("## 🥧 Distribuição dos gastos")

    fig2, ax2 = plt.subplots()
    ax2.pie(df["valor"], labels=df["categoria"], autopct="%1.1f%%")

    st.pyplot(fig2)

    st.markdown("## 📋 Dados detalhados")
    st.dataframe(df, use_container_width=True)

# =========================
# IA
# =========================
elif opcao == "Análise com IA":

    st.markdown("## 🤖 Pergunte sobre suas finanças")

    pergunta = st.text_input("Digite sua pergunta:")

    if pergunta:
        contexto = f"Dados financeiros: {df.to_dict()}"
        resposta = responder(pergunta, contexto)
        st.write(resposta)