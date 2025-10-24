# Automação Comercial Assistida por IA

Este repositório mostra um exemplo real de como usar automação + análise de dados para dar poder a equipas comerciais, usando Python e IA.

## O que este projeto faz

1. Lê uma lista de leads/prospects de um ficheiro Excel ou CSV.
2. Conta quantos leads existem por estado (por ex.: Quente, Morno, Frio).
3. Gera um mini-relatório de apoio à decisão comercial (quantos leads quentes tenho hoje? onde investir primeiro?).
4. Guarda esse relatório pronto para enviar ao chefe / equipa.

Isto é útil para equipas de vendas B2B (leasing, renting de camiões, equipamentos industriais, financiamento de máquinas, etc.), mas pode ser adaptado a qualquer pipeline comercial.

## Ficheiros principais

- `lead_report.py`  
  Script que gera automaticamente um relatório de leads.

## Como usar

1. Instalar dependências (Python 3 + pandas + openpyxl):
   ```bash
   pip install pandas openpyxl
