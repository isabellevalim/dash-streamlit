import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Comando para garantir que os componentes do dashboard sejam apresentados numa resolução widescreen
st.set_page_config(layout = 'wide')

# Função auxiliar para formatar as métricas com 2 casas decimais
def formataNumero (valor, prefixo = ''):
    for unidade in ['', 'mil']:
        if valor < 1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor:.2f} milhões'

# Inserindo o título do dashboard
st.title("Dashboard de vendas")

# Essa é a url da API de onde vamos pegar os dados
url = 'https://labdados.com/produtos'
regioes = ['Brasil', 'Centro-Oeste', 'Nordeste', 'Norte', 'Sudeste', 'Sul']

# Quero inserir no dashboard a opção do usuário filtrar os dados por regiao e ano das vendas. Pra isso, vou inserir os componentes
## selectbox, checkbox e slider no sidebar da aplicação
st.sidebar.title('Filtros')
regiao = st.sidebar.selectbox('Região', regioes)
if regiao == 'Brasil':
    regiao = ''

todosAnos = st.sidebar.checkbox('Dados de todo o período', value = True)
if todosAnos:
    ano = ''
else:
    ano = st.sidebar.slider('Ano', 2020, 2023)

# Posso incrementar a url da API e já pegar as informaçoes filtradas por ano e regiao. Pra isso preciso passar esses parametros
## Criei uma variavel queryString do tipo dicionário onde eu passo o nome da regiao e o ano
queryString = {'regiao': regiao.lower(), 'ano':ano}

# Usando a biblioteca requests para pegar as informações da API
response = requests.get(url, params = queryString) # Se eu nao quiser pegar as informacoes filtradas por regiao e ano, é só não passar params como atributo do get()
dados = pd.DataFrame.from_dict(response.json()) # Transformei o json que recebo da API em um dataframe Pandas
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format = '%d/%m/%Y') # formatei o tipo dessa coluna para datetime

# Criando um filtro de vendedores
filtroVendedores = st.sidebar.multiselect('Vendedores', dados['Vendedor'].unique())
if filtroVendedores:
    dados = dados[dados['Vendedor'].isin(filtroVendedores)]

############# Tabelas
# Manipulando o dataframe com todas as informações para gerar a informações que eu quero
receitaEstados = dados.groupby('Local da compra')[['Preço']].sum()
receitaEstados = dados.drop_duplicates(subset = 'Local da compra')[['Local da compra', 'lat', 'lon']].merge(receitaEstados, left_on =  'Local da compra', right_index = True).sort_values('Preço', ascending = False)

receitaMensal = dados.set_index('Data da Compra').groupby(pd.Grouper(freq = 'M'))[ 'Preço'].sum().reset_index()
receitaMensal['Ano'] = receitaMensal['Data da Compra'].dt.year
receitaMensal['Mes'] = receitaMensal['Data da Compra'].dt.month_name()

receitaCategorias = dados.groupby('Categoria do Produto')[['Preço']].sum().sort_values('Preço', ascending = False)

vendedores = pd.DataFrame(dados.groupby('Vendedor')['Preço'].agg(['sum', 'count']))


############# Gráficos
# Criando os gráficos com o pacote Plotly usando as tabelas que eu criei no step anterior
figMapaReceita = px.scatter_geo(receitaEstados,
                                lat = 'lat',
                                lon = 'lon',
                                scope = 'south america',
                                size = 'Preço',
                                template = 'seaborn',
                                hover_name = 'Local da compra',
                                hover_data = {'lat': False, 'lon':False},
                                title = 'Receita por estado')


figReceitaMensal = px.line(receitaMensal,
                            x = 'Mes',
                            y = 'Preço',
                            markers = True,
                            range_y = (0,receitaMensal.max()),
                            color = 'Ano',
                            line_dash = 'Ano',
                            title = 'Receita mensal')

figReceitaMensal.update_layout(yaxis_title = 'Receita')

figReceitaEstados = px.bar(receitaEstados.head(),
                            x = 'Local da compra',
                            y = 'Preço',
                            text_auto = True,
                            title = 'Top estados (receita)')

figReceitaEstados.update_layout(yaxis_title = 'Receita')

figReceitaCategorias = px.bar(receitaCategorias,
                            text_auto = True,
                            title = 'Receita por categoria')

figReceitaCategorias.update_layout(yaxis_title = 'Receita')


############# Visualização da aplicação -> dashboard

aba1, aba2 = st.tabs(['Receita', 'Vendedores']) # Dividi a aplicação em 2 abas para separar melhor as informações

with aba1:
    coluna1, coluna2 = st.columns(2) # Dividi as informações que eu quero mostrar na primeira aba em 2 colunas
    with coluna1: # Inseri o que eu quero na primeira coluna
        st.metric('Receita', formataNumero(dados['Preço'].sum(), 'R$'))
        st.plotly_chart(figMapaReceita, use_container_width = True)
        st.plotly_chart(figReceitaEstados, use_container_width = True)
    with coluna2: # Inseri o que eu quero na segunda coluna
        st.metric('Quantidade de vendas', formataNumero(dados.shape[0]))
        st.plotly_chart(figReceitaMensal, use_container_width = True)
        st.plotly_chart(figReceitaCategorias, use_container_width = True)

with aba2: # Aqui vou inserir o que eu quero na segunda aba
    qtd_vendedores = st.number_input('Quantidade de vendedores', 2, 10, 5) # Recurso interativo onde o usuário pode escolher o numero de vendedores que ele quer ver
    coluna1, coluna2 = st.columns(2) # Tambem dividi a segunda aba em 2 colunas
    with coluna1: # Inseri o que eu quero na primeira coluna
        st.metric('Receita', formataNumero(dados['Preço'].sum(), 'R$'))

        figReceitaVendedores = px.bar(vendedores[['sum']].sort_values('sum', ascending = False).head(qtd_vendedores),
                                        x = 'sum',
                                        y = vendedores[['sum']].sort_values('sum', ascending = False).head(qtd_vendedores).index,
                                        text_auto = True,
                                        title = f'Top {qtd_vendedores} vendedores (receita')
        st.plotly_chart(figReceitaVendedores)

    with coluna2:# Inseri o que eu quero na segunda coluna
        st.metric('Quantidade de vendas', formataNumero(dados.shape[0]))
        figVendaVendedores = px.bar(vendedores[['count']].sort_values('count', ascending = False).head(qtd_vendedores),
                                        x = 'count',
                                        y = vendedores[['count']].sort_values('count', ascending = False).head(qtd_vendedores).index,
                                        text_auto = True,
                                        title = f'Top {qtd_vendedores} vendedores (qtd de vendas')
        st.plotly_chart(figVendaVendedores)
