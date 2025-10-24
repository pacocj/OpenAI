# Automação Comercial Assistida por IA

Este repositório mostra um exemplo prático de como usar automação + análise de dados para dar poder a equipas comerciais, usando Python e IA.

## O que este projeto faz

1. Lê uma lista de leads/prospects de um ficheiro Excel ou CSV.
2. Conta quantos leads existem por estado (por exemplo: Quente, Morno, Frio).
3. Gera um mini-relatório com prioridades comerciais (quem atacar primeiro).
4. Guarda esse relatório pronto para enviar à direção comercial.

Isto é útil para equipas de vendas B2B (leasing, renting de camiões, financiamento de máquinas, etc.) e pode ser adaptado a qualquer pipeline comercial.

## Ficheiros principais

- `lead_report.py`  
  Gera automaticamente um relatório de leads e cria o ficheiro `relatorio_leads.txt`.

- `requirements.txt`  
  Lista as dependências necessárias para correr o script.

- `leads_exemplo.csv`  
  Pequeno exemplo de leads para testar.

## Como correr

1. Instalar dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Atualizar o ficheiro `leads_exemplo.csv` com os seus leads reais.

3. Correr:
   ```bash
   python lead_report.py
   ```

4. Abrir o ficheiro `relatorio_leads.txt` que foi gerado automaticamente.

## Porque isto interessa

- Dá visão imediata de prioridades comerciais sem precisar de CRM complexo/caro.
- Funciona com um simples Excel/CSV da equipa.
- Pode ser automatizado para correr todos os dias às 08h e enviar relatório por e-mail / WhatsApp.

## Próximo passo

Automatizar o envio diário deste relatório e ligar a dashboards visuais.
