import pandas as pd
from datetime import datetime
import os

def carregar_dados(caminho_ficheiro: str) -> pd.DataFrame:
    """
    Lê um ficheiro .csv com leads.
    O ficheiro deve ter pelo menos uma coluna chamada 'Status'
    (ex: 'Quente', 'Morno', 'Frio').
    """
    if not os.path.exists(caminho_ficheiro):
        raise FileNotFoundError(f"Ficheiro não encontrado: {caminho_ficheiro}")

    if caminho_ficheiro.lower().endswith(".csv"):
        df = pd.read_csv(caminho_ficheiro)
    else:
        raise ValueError("Formato não suportado. Usa .csv")

    # Normaliza nomes de colunas (tira espaços, põe em minúsculas)
    df.columns = [c.strip().lower() for c in df.columns]

    if "status" not in df.columns:
        raise ValueError(
            "O ficheiro precisa de uma coluna chamada 'Status' (ex: Quente / Morno / Frio)."
        )

    return df


def analisar_leads(df: pd.DataFrame) -> str:
    """
    Faz o resumo das oportunidades por estado e devolve texto pronto a usar.
    """
    total = len(df)

    # Contar por status
    contagem_status = df["status"].value_counts(dropna=False)

    linhas_relatorio = []
    linhas_relatorio.append("RELATÓRIO DE LEADS")
    linhas_relatorio.append(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    linhas_relatorio.append("-" * 40)
    linhas_relatorio.append(f"Total de leads: {total}")
    linhas_relatorio.append("")

    linhas_relatorio.append("Leads por estado:")
    for estado, qtd in contagem_status.items():
        linhas_relatorio.append(f"  - {estado}: {qtd}")

    # Heurística simples de leitura comercial
    quente = 0
    for estado, qtd in contagem_status.items():
        if str(estado).strip().lower() == "quente":
            quente = qtd
            break

    linhas_relatorio.append("")
    linhas_relatorio.append("Observação rápida:")
    if quente == 0:
        linhas_relatorio.append("⚠ Não há leads \"Quente\". Urgente reativar pipeline.")
    elif quente < 3:
        linhas_relatorio.append("Há poucos leads \"Quente\". Focar follow-up imediato.")
    else:
        linhas_relatorio.append("Bom nível de leads \"Quente\". Priorizar estes nomes já hoje.")

    return "\n".join(linhas_relatorio)


def guardar_relatorio(texto: str, caminho_saida: str = "relatorio_leads.txt"):
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(texto)


def executar(caminho_ficheiro: str = "leads_exemplo.csv"):
    """
    Fluxo completo:
    1. Carrega dados
    2. Analisa
    3. Gera relatorio_leads.txt
    """
    df = carregar_dados(caminho_ficheiro)
    resumo = analisar_leads(df)
    guardar_relatorio(resumo)
    print("Relatório gerado: relatorio_leads.txt")
    print("")
    print(resumo)


if __name__ == "__main__":
    executar("leads_exemplo.csv")
