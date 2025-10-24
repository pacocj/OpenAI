import pandas as pd
from datetime import datetime
import os


FASES_ABERTAS = ["Proposta enviada", "A negociar"]
FASE_GANHO = "Fechado ganho"
FASE_PERDIDO = "Fechado perdido"


def carregar_dados(caminho_csv: str = "negocios.csv") -> pd.DataFrame:
    """
    Lê o CSV de pipeline comercial.
    Espera colunas:
    - Oportunidade
    - Valor_Estimado
    - Fase
    - Responsavel
    - Data_Prevista_Fecho
    """
    if not os.path.exists(caminho_csv):
        raise FileNotFoundError(f"Ficheiro não encontrado: {caminho_csv}")

    df = pd.read_csv(caminho_csv)

    # Normaliza nomes de colunas
    df.columns = [c.strip() for c in df.columns]

    obrigatorias = [
        "Oportunidade",
        "Valor_Estimado",
        "Fase",
        "Responsavel",
        "Data_Prevista_Fecho",
    ]
    for col in obrigatorias:
        if col not in df.columns:
            raise ValueError(f"Coluna obrigatória em falta: {col}")

    # Converter valor para numérico (caso esteja tipo string)
    df["Valor_Estimado"] = pd.to_numeric(df["Valor_Estimado"], errors="coerce").fillna(0)

    # Converter data prevista para datetime se der
    df["Data_Prevista_Fecho"] = pd.to_datetime(
        df["Data_Prevista_Fecho"], errors="coerce", format="%Y-%m-%d"
    )

    return df


def analisar_pipeline(df: pd.DataFrame) -> str:
    agora = datetime.now()

    # Valores por categoria
    total_aberto = df[df["Fase"].isin(FASES_ABERTAS)]["Valor_Estimado"].sum()
    total_ganho = df[df["Fase"] == FASE_GANHO]["Valor_Estimado"].sum()
    total_perdido = df[df["Fase"] == FASE_PERDIDO]["Valor_Estimado"].sum()

    # Taxa de sucesso comercial
    base_sucesso = total_ganho + total_perdido
    if base_sucesso > 0:
        taxa_sucesso = (total_ganho / base_sucesso) * 100
    else:
        taxa_sucesso = 0.0

    # Quem está a segurar mais dinheiro em aberto
    por_resp = (
        df[df["Fase"].isin(FASES_ABERTAS)]
        .groupby("Responsavel")["Valor_Estimado"]
        .sum()
        .sort_values(ascending=False)
    )
    if not por_resp.empty:
        top_resp = por_resp.index[0]
        top_resp_valor = por_resp.iloc[0]
    else:
        top_resp = "n/a"
        top_resp_valor = 0

    # Próximas oportunidades com fecho previsto (só das fases abertas)
    proximos = (
        df[df["Fase"].isin(FASES_ABERTAS)]
        .dropna(subset=["Data_Prevista_Fecho"])
        .sort_values("Data_Prevista_Fecho")
        .head(3)
    )

    linhas = []
    linhas.append("RELATÓRIO DE PIPELINE COMERCIAL")
    linhas.append(f"Data: {agora.strftime('%Y-%m-%d %H:%M')}")
    linhas.append("-" * 70)

    linhas.append(f"\nTotal em aberto (potencial ainda negociável): €{total_aberto:,.2f}")
    linhas.append(f"Total ganho (já fechado):                     €{total_ganho:,.2f}")
    linhas.append(f"Total perdido:                                 €{total_perdido:,.2f}")
    linhas.append(f"Taxa de sucesso (ganho / ganho+perdido):       {taxa_sucesso:.1f}%")

    linhas.append(
        f"\nMaior responsável pelo pipeline em aberto: {top_resp} "
        f"(€{top_resp_valor:,.2f} em negociação)"
    )

    # Secção de próximos fechos
    linhas.append("\nPróximas oportunidades com fecho previsto:")
    if proximos.empty:
        linhas.append("  - (Sem datas previstas nas negociações atuais)")
    else:
        for _, row in proximos.iterrows():
            data_prev = (
                row["Data_Prevista_Fecho"].strftime("%Y-%m-%d")
                if not pd.isna(row["Data_Prevista_Fecho"])
                else "data n/d"
            )
            linhas.append(
                f"  - {row['Oportunidade']} | {row['Responsavel']} | "
                f"€{row['Valor_Estimado']:,.2f} | Previsto: {data_prev}"
            )

    # Pequena leitura consultiva
    linhas.append("\nObservação estratégica:")
    avisos = []

    # Muito dinheiro aberto mas pouco ganho -> risco de arrastar negociação
    if total_aberto > (total_ganho * 2) and total_ganho < 1.5 * total_perdido:
        avisos.append(
            "Muito valor em aberto mas pouco convertido. "
            "Rever objeções e pricing nas propostas enviadas."
        )

    # Taxa de sucesso baixa
    if taxa_sucesso < 30 and base_sucesso > 0:
        avisos.append(
            "Taxa de sucesso abaixo de 30%. "
            "Sugere muita perda após proposta. Analisar razões de perda."
        )

    # Sem oportunidades abertas
    if total_aberto == 0:
        avisos.append(
            "Não há pipeline ativo em negociação. "
            "Urgente gerar novas oportunidades."
        )

    # Caso não haja avisos "críticos", damos orientação positiva
    if not avisos:
        avisos.append(
            "Pipeline equilibrado. Continuar follow-up nas oportunidades com fecho mais próximo."
        )

    for a in avisos:
        linhas.append(f"- {a}")

    return "\n".join(linhas)


def guardar_relatorio(texto: str, caminho_saida: str = "relatorio_pipeline.txt"):
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(texto)


def executar(caminho_csv: str = "negocios.csv"):
    df = carregar_dados(caminho_csv)
    resumo = analisar_pipeline(df)
    guardar_relatorio(resumo)
    print("Relatório gerado: relatorio_pipeline.txt")
    print("")
    print(resumo)


if __name__ == "__main__":
    executar("negocios.csv")
