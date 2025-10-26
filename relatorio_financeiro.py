import pandas as pd
from datetime import datetime
import glob
import os


def obter_ultimo_ficheiro_movimentos(prefixo="movimentos"):
    """
    Procura ficheiros que começam por 'movimentos' e terminam em .csv
    Ex.: movimentos.csv, movimentos_2025-10-27.csv, etc.
    Escolhe o MAIS RECENTE (pelo timestamp de modificação no repo checkout).
    """
    candidatos = glob.glob(f"{prefixo}*.csv")
    if not candidatos:
        raise FileNotFoundError("Nenhum ficheiro de movimentos encontrado (movimentos*.csv).")

    # ordenar por data de modificação (mais recente primeiro)
    candidatos.sort(key=os.path.getmtime, reverse=True)
    return candidatos[0]


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

    # nome dinâmico para o relatório
    nome_relatorio = f"relatorio_financeiro_{timestamp_para_nome}.txt"

    with open(nome_relatorio, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))

    print("✅ Relatório gerado:", nome_relatorio)

    # devolve o nome criado para que o workflow saiba o que subir
    return nome_relatorio


if __name__ == "__main__":
    gerar_relatorio_financeiro()
