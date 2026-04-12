import pandas as pd

def carregar_dados(caminho):
    return pd.read_csv(caminho)

def resumo_financeiro(df):
    total = df["valor"].sum()
    media = df["valor"].mean()
    maior = df.loc[df["valor"].idxmax()]

    return {
        "total": total,
        "media": media,
        "maior_categoria": maior["categoria"],
        "maior_valor": maior["valor"]
    }