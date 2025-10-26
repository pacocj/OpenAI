import pandas as pd
from datetime import datetime
import glob
import os
import matplotlib.pyplot as plt


def obter_ultimo_ficheiro_movimentos(prefixo="movimentos"):
    """
    Procura ficheiros que começam por 'movimentos' e terminam em .csv
    Ex.: movimentos.csv, movimentos_2025-10-27.csv, etc.
    Escolhe o MAIS RECENTE (pelo timestamp de modificação no repo checkout).
    """
    candidatos = glob.glob(f"{prefixo}*.csv")
    if not candidatos:
        raise FileNotFoundError("Nenhum ficheiro de movimentos encontrado (movimentos*.csv).")

    candidatos.sort(key=os.path.getmtime, reverse=True)
    return candidatos[0]


def gerar_grafico_despesas_por_categoria(df, nome_png):
    """
    Gera um gráfico de barras com o total de despesas por categoria
    e guarda-o como imagem PNG.
    """
    despesas_cat = (
        df[df["Tipo"].str.capitalize() == "Despesa"]
        .groupby(df["Categoria"].str.capitalize())["Valor"]
        .sum()
        .sort_values(ascending=False)
    )

    if despesas_cat.empty:
        # Se por acaso não houver despesas, ainda assim criamos um gráfico vazio
        plt.figure(figsize=(6,4))
        plt.text(0.5, 0.5, "Sem despesas registadas", ha="center", va="center")
        plt.title("Despesas por Categoria (€)")
        plt.axis("off")
    else:
        plt.figure(figsize=(6,4))
        plt.bar(despesas_cat.index, despesas_cat.values)
        plt.title("Despesas por Categoria (€)")
        plt.ylabel("€")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()

    plt.savefig(nome_png)
    plt.close()


def gerar_relatorio_financeiro():
    # 1. descobrir qual csv usar
    caminho_csv = obter_ultimo_ficheiro_movimentos()

    df = pd.read_csv(caminho_csv)

    # limpeza básica
    df["Tipo"] = df["Tipo"].str.strip().str.capitalize()
    df["Categoria"] = df["Categoria"].str.strip().str.capitalize()

    total_receitas = df[df["Tipo"] == "Receita"]["Valor"].sum()
    total_despesas = df[df["Tipo"] == "Despesa"]["Valor"].sum()
    saldo = total_receitas - total_despesas

    if total_receitas > 0:
        perc_despesas = (total_despesas / total_receitas) * 100
    else:
        perc_despesas = 0

    categorias_despesa = (
        df[df["Tipo"] == "Despesa"]
        .groupby("Categoria")["Valor"]
        .sum()
        .sort_values(ascending=False)
        .head(3)
    )

    # Observação automática
    if saldo > 0:
        observacao = "Resultado POSITIVO — as receitas superam as despesas."
    elif saldo < 0:
        observacao = "Resultado NEGATIVO — despesas acima das receitas."
    else:
        observacao = "Saldo neutro — receitas e despesas equilibradas."

    agora = datetime.now()
    timestamp_humano = agora.strftime("%Y-%m-%d %H:%M:%S")
    timestamp_para_nome = agora.strftime("%Y-%m-%d_%H-%M-%S")

    # ----- 1) gerar relatório texto -----
    linhas = []
    linhas.append("RELATÓRIO FINANCEIRO AUTOMÁTICO")
    linhas.append(f"Data: {timestamp_humano}")
    linhas.append("-" * 60)
    linhas.append("")
    linhas.append(f"Ficheiro analisado: {caminho_csv}")
    linhas.append("")
    linhas.append(f"Total de Receitas: €{total_receitas:,.2f}")
    linhas.append(f"Total de Despesas: €{total_despesas:,.2f}")
    linhas.append(f"Saldo: €{saldo:,.2f}")
    linhas.append(f"Percentagem de despesas vs receitas: {perc_despesas:.1f}%")
    linhas.append("")
    linhas.append("Top 3 Categorias de Despesa:")
    for categoria, valor in categorias_despesa.items():
        linhas.append(f"  - {categoria}: €{valor:,.2f}")
    linhas.append("")
    linhas.append("Observação:")
    linhas.append(f"- {observacao}")

    nome_relatorio = f"relatorio_financeiro_{timestamp_para_nome}.txt"
    with open(nome_relatorio, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))

    # ----- 2) gerar gráfico PNG -----
    nome_grafico = f"grafico_despesas_{timestamp_para_nome}.png"
    gerar_grafico_despesas_por_categoria(df, nome_grafico)

    print("Relatório gerado:", nome_relatorio)
    print("Gráfico gerado:", nome_grafico)

    # devolvemos os nomes para o workflow apanhar e fazer upload
    return nome_relatorio, nome_grafico


if __name__ == "__main__":
    gerar_relatorio_financeiro()
