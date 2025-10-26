import pandas as pd
from datetime import datetime


def gerar_relatorio_financeiro(caminho_csv="movimentos.csv", saida="relatorio_financeiro.txt"):
    df = pd.read_csv(caminho_csv)

    # Garantir que os dados estão limpos
    df["Tipo"] = df["Tipo"].str.strip().str.capitalize()
    df["Categoria"] = df["Categoria"].str.strip().str.capitalize()

    # Totais básicos
    total_receitas = df[df["Tipo"] == "Receita"]["Valor"].sum()
    total_despesas = df[df["Tipo"] == "Despesa"]["Valor"].sum()
    saldo = total_receitas - total_despesas

    # Top 3 categorias de despesa
    categorias_despesa = (
        df[df["Tipo"] == "Despesa"]
        .groupby("Categoria")["Valor"]
        .sum()
        .sort_values(ascending=False)
        .head(3)
    )

    # Percentagem de despesas vs receitas
    if total_receitas > 0:
        perc_despesas = (total_despesas / total_receitas) * 100
    else:
        perc_despesas = 0

    # Observação automática
    if saldo > 0:
        observacao = "Resultado POSITIVO — as receitas superam as despesas."
    elif saldo < 0:
        observacao = "Resultado NEGATIVO — despesas acima das receitas."
    else:
        observacao = "Saldo neutro — receitas e despesas equilibradas."

    # Montar relatório
    linhas = []
    linhas.append("RELATÓRIO FINANCEIRO AUTOMÁTICO")
    linhas.append(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    linhas.append("-" * 60)
    linhas.append(f"\nTotal de Receitas: €{total_receitas:,.2f}")
    linhas.append(f"Total de Despesas: €{total_despesas:,.2f}")
    linhas.append(f"Saldo: €{saldo:,.2f}")
    linhas.append(f"Percentagem de despesas vs receitas: {perc_despesas:.1f}%")

    linhas.append("\nTop 3 Categorias de Despesa:")
    for categoria, valor in categorias_despesa.items():
        linhas.append(f"  - {categoria}: €{valor:,.2f}")

    linhas.append("\nObservação:")
    linhas.append(f"- {observacao}")

    # Guardar relatório
    with open(saida, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))

    print("✅ Relatório gerado com sucesso:", saida)


if __name__ == "__main__":
    gerar_relatorio_financeiro()
