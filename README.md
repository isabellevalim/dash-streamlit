# Dashboard de Vendas
Dashboard para monitoramento de vendas (desenvolvido no Streamlit) que coleta dados de uma API pública

## Objetivos do projeto

Primeiro, é necessário fazer a configuração do ambiente para que você possa utilizar a ferramenta. 
Depois, vamos fazer a leitura dos dados a partir da consulta à uma API. Na sequência, vamos construir os gráficos e os inserir no dashboard.
Ao final, faremos o deploy. Assim, todas as pessoas conseguirão acessar a aplicação a partir de um link.

Para acessar o dashboard: https://dash-app-machineisa.streamlit.app/

## Como executar o código na sua máquina

Assista as aulas do módulo bônus de Git para saber como clonar esse projeto para a sua máquina local

Com o projeto aberto, crie um ambiente virtual: python -m venv venv

Ative o ambiente virtual: .\venv\Scripts\activate

Dentro do ambiente virtual venv, instale os pacotes necessários: streamlit, requests, pandas e plotly

Para executar a aplicação web, o comando é: streamlit run app.py

## Obtendo os dados a partir de uma API pública

A url de chamada da API é: https://labdados.com/produtos
A API fornece os dados filtrados por região e ano pela seguinte url: https://labdados.com/produtos?regiao=norte&ano=2022
