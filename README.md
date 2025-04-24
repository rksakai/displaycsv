# Alertas Urbanos – Simulação DevOps

Este projeto simula uma aplicação de visualização de dados urbanos (em formato CSV), com foco na aplicação prática de técnicas de **DevOps**, como:

- Integração Contínua (CI)
- Entrega Contínua (CD)
- Containerização com Docker
- Orquestração de serviços
- Deploy automatizado (Azure)

## 🔍 Objetivo

Este repositório foi adaptado a partir do projeto [displaycsv](https://github.com/rksakai/displaycsv), com o intuito de representar uma aplicação de **Cidade Inteligente**, como o sistema de **Alertas Urbanos**. A ideia é simular visualização de ocorrências urbanas com base em arquivos CSV.

## ⚙️ Tecnologias Utilizadas

- Python (Flask)
- GitHub Actions (CI/CD)
- Docker
- Azure App Service (para simulação de produção)
- GitHub + Azure DevOps

## 🚀 Como Executar Localmente

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar aplicação
python app.py
