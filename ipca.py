import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from statsmodels.tsa.holtwinters import ExponentialSmoothing

st.set_page_config(layout="wide")

url = "https://servicodados.ibge.gov.br/api/v3/agregados/1737/periodos/200001-202512/variaveis/63?localidades=N1[all]"

def parse_ibge_data(data):
    """Função para converter dados JSON da API do IBGE para um DataFrame"""
    registros = []
    for item in data[0]['resultados'][0]['series']:
        for mes, valor in item['serie'].items():
            registros.append({'Data': mes, 'IPCA': float(valor)})
    df = pd.DataFrame(registros)
    df['Data'] = pd.to_datetime(df['Data'], format='%Y%m')
    return df

try:
    data = requests.get(url).json()
    df = parse_ibge_data(data)
except Exception as e:
    st.error("Erro ao obter ou processar os dados da API do IBGE.")
    st.stop()

df['Ano'] = df['Data'].dt.year
df['Mês'] = df['Data'].dt.month

modelo = ExponentialSmoothing(df['IPCA'], trend='add', seasonal='add', seasonal_periods=12)
modelo_fit = modelo.fit()

futuro = pd.date_range(start=df['Data'].max(), periods=24, freq='ME')
previsoes = modelo_fit.forecast(len(futuro))

df_previsao = pd.DataFrame({'Data': futuro, 'IPCA': previsoes})

variacao_ipca = {
    'Categoria': [
        'Índice Geral', 'Alimentação e Bebidas', 'Habitação', 'Artigos de Residência', 'Vestuário',
        'Transportes', 'Saúde e Cuidados Pessoais', 'Despesas Pessoais', 'Educação', 'Comunicação'
    ],
    'Variação Mensal (%)': [0.5, 0.6, 4.2, 0.3, 0.1, 0.8, 0.5, 0.2, 4.5, 0.3],
    'Variação Acumulada (%)': [2.1, 3.5, 2.8, 2.3, 3.9, 4.1, 3.0, 2.9, 4.9, 4.7]
}
df_variacao = pd.DataFrame(variacao_ipca)

st.sidebar.header("Filtros Interativos")

anos_selecionados = st.sidebar.slider(
    "Selecione o intervalo de anos",
    int(df['Ano'].min()),
    int(df['Ano'].max()),
    (2000, 2025) 
)

df = df[(df['Ano'] >= anos_selecionados[0]) & (df['Ano'] <= anos_selecionados[1])]

categorias_selecionadas = st.sidebar.multiselect(
    "Selecione as categorias",
    options=df_variacao['Categoria'].unique(),
    default=df_variacao['Categoria'].unique()  
)

df_variacao_filtrado = df_variacao[df_variacao['Categoria'].isin(categorias_selecionadas)]

media_ipca_2025 = df[df['Ano'] == 2025]['IPCA'].mean()
variacao_acumulada_total = df['IPCA'].sum()
previsao_acumulada_2026 = df_previsao['IPCA'].sum()

st.title("Dashboard IPCA")
st.subheader("Principais Métricas do IPCA")

col1, col2, col3 = st.columns(3)

col1.metric(
    label="Média do IPCA em 2025",
    value=f"{media_ipca_2025:.2f}",
    delta=None
)

col2.metric(
    label=f"Variação Acumulada ({anos_selecionados[0]}-{anos_selecionados[1]})",
    value=f"{variacao_acumulada_total:.2f}",
    delta=None
)

col3.metric(
    label="Previsão Acumulada para 2026",
    value=f"{previsao_acumulada_2026:.2f}",
    delta=None
)

st.markdown("---")

col1, col2, col3 = st.columns([3, 3, 3])
col4, col5, col6 = st.columns([3, 3, 3])

with col1:

    fig_coluna = px.bar(
        df,
        x=df['Data'].dt.strftime('%Y-%m'),  #
        y='IPCA',  
        title="Evolução de 2000 à 2025",
        labels={'Data': 'Ano-Mês', 'IPCA': 'Valor do IPCA'}, 
        color='Ano',
    )

    fig_coluna.update_layout(
        title = {
            'text': "Evolução de 2000 à 2025",
            'x': 0.5,
            'xanchor': 'center', 
            'yanchor': 'top'  
        }
    )

    fig_coluna.update_layout(
        xaxis_title="Ano-Mês",
        yaxis_title="IPCA",
        width=800, 
        height=450,  
    )

    st.plotly_chart(fig_coluna, use_container_width=True)  

with col2:
    fig_pie = px.pie(df_variacao, values='Variação Acumulada (%)', names='Categoria',
        title='Distribuição Porcentual - Variação Acumulada',
        labels={'Categoria': 'Grupo', 'Variação Acumulada (%)': 'Variação (%)'}
    )
    fig_pie.update_layout(width=900, height=450)
    st.plotly_chart(fig_pie, use_container_width=True)

    fig_coluna.update_layout(
        title = {
            'text': "Distribuição Porcentual - Variação Acumulada",
            'x': 0.5,
            'xanchor': 'center', 
            'yanchor': 'top'  
        }
    )

with col3:
    df_clusterizado = df_variacao.melt(
        id_vars='Categoria', 
        value_vars=['Variação Mensal (%)', 'Variação Acumulada (%)'],
        var_name='Tipo de Variação', 
        value_name='Valor'
    )

    fig_bar = px.bar(
        df_clusterizado, 
        x='Valor', 
        y='Categoria', 
        color='Tipo de Variação', 
        barmode='group', 
        title='Variação Mensal e Acumulada - Fevereiro 2025',
        labels={'Valor': 'Variação (%)', 'Categoria': 'Grupo'},
        color_discrete_map={
            'Variação Mensal (%)': '#1E90FF',  
            'Variação Acumulada (%)': '#FF4500' 
        }
    )

    fig_coluna.update_layout(
        title = {
            'text': "Variação Mensal e Acumulada - Fevereiro 2025",
            'x': 0.5,
            'xanchor': 'center', 
            'yanchor': 'top'  
        }
    )

    fig_bar.update_layout(
        width=900,  
        height=450, 
    )

    st.plotly_chart(fig_bar, use_container_width=True)

with col4:
 
    df['IPCA_positivo'] = df['IPCA'].apply(lambda x: x if x > 0 else 0)
    df['IPCA_negativo'] = df['IPCA'].apply(lambda x: x if x < 0 else 0)

    fig_area = go.Figure()

    fig_area.add_trace(go.Scatter(
        x=df['Data'],
        y=df['IPCA_positivo'],
        fill='tozeroy',
        mode='none',
        name='Positivo',
        fillcolor='DodgerBlue'
    ))

    fig_area.add_trace(go.Scatter(
        x=df['Data'],
        y=df['IPCA_negativo'],
        fill='tozeroy',
        mode='none',  
        name='Negativo',
        fillcolor='darkorange'
    ))

    fig_coluna.update_layout(
        title = {
            'text': "Variação Mensal com Destaque por Ano",
            'x': 0.5,
            'xanchor': 'center', 
            'yanchor': 'top'  
        }
    )

    anos = df['Data'].dt.year.unique()  
    for ano in anos:
        fig_area.add_shape(
            type="line",
            x0=f"{ano}-01-01",  
            x1=f"{ano}-01-01",  
            y0=min(df['IPCA'].min(), 0),  
            y1=max(df['IPCA'].max(), 0),  
            line=dict(color="gray", width=1, dash="dash")  
        )

    max_valor = df['IPCA_positivo'].max()
    data_max = df[df['IPCA_positivo'] == max_valor]['Data'].values[0]

    min_valor = df['IPCA_negativo'].min()
    data_min = df[df['IPCA_negativo'] == min_valor]['Data'].values[0]

    fig_area.add_annotation(
        x=data_max,
        y=max_valor,
        text=f"Máx: {max_valor:.2f}",
        showarrow=True,
        arrowhead=2,
        font=dict(size=12, color="black"),
        bgcolor="#C7E9FF" 
    )

    fig_area.add_annotation(
        x=data_min,
        y=min_valor,
        text=f"Mín: {min_valor:.2f}",
        showarrow=True,
        arrowhead=2,
        font=dict(size=12, color="black"),
        bgcolor="#FFC7C7" 
    )

    fig_area.add_shape(
        type="line",
        x0=min(df['Data']),
        x1=max(df['Data']),
        y0=0,
        y1=0,
        line=dict(color="gray", width=1, dash="dash") 
    )


    fig_area.update_layout(
        title="Variação Mensal com Destaque por Ano",
        xaxis_title="Data",
        yaxis_title="IPCA",
        width=900,  
        height=450,  
        showlegend=True 
    )


    st.plotly_chart(fig_area, use_container_width=True)



with col5:
 
    fig_boxplot = px.box(
        df,
        x='Ano',
        y='IPCA',
        title='Distribuição por Ano',
        color='Ano'  
    )

    fig_boxplot.update_layout(
        title = {
            'text': "Distribuição por Ano",
            'x': 0.5,
            'xanchor': 'center', 
            'yanchor': 'top'  
        }
    )

    fig_boxplot.update_layout(
        width=800,  
        height=450  
    )

    st.plotly_chart(fig_boxplot, use_container_width=True)



with col6:
    df_previsao['Cenário Otimista'] = df_previsao['IPCA'] * 0.9  
    df_previsao['Cenário Pessimista'] = df_previsao['IPCA'] * 1.1  
    df_previsao['Cenário Esperado'] = df_previsao['IPCA']  

    fig_cenarios = go.Figure()

    fig_cenarios.add_trace(go.Scatter(
        x=df_previsao['Data'],
        y=df_previsao['Cenário Esperado'],
        name='Cenário Esperado',
        mode='lines',
        line=dict(color='orange', width=2)  
    ))

    fig_cenarios.add_trace(go.Scatter(
        x=df_previsao['Data'],
        y=df_previsao['Cenário Otimista'],
        name='Cenário Otimista',
        mode='lines',
        line=dict(color='green', dash='dash')  
    ))

    fig_cenarios.add_trace(go.Scatter(
        x=df_previsao['Data'],
        y=df_previsao['Cenário Pessimista'],
        name='Cenário Pessimista',
        mode='lines',
        line=dict(color='red', dash='dash') 
    ))

    fig_cenarios.add_trace(go.Bar(
        x=df_previsao['Data'],
        y=df_previsao['Cenário Esperado'],
        name='',
        marker=dict(color='#FBE4B9') 
    ))

    fig_cenarios.update_layout(
        title={
            'text': "Previsão do IPCA até 2026 (Análise de Cenários)",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Data",
        yaxis_title="IPCA",
        width=900,   
        height=450,  
        barmode='group' 
    )

    st.plotly_chart(fig_cenarios, use_container_width=True)

st.markdown("---")

resumo_estatistico = df.groupby('Ano')['IPCA'].agg(['mean', 'median', 'min', 'max']).reset_index()
resumo_estatistico.columns = ['Ano', 'Média', 'Mediana', 'Mínimo', 'Máximo']  

st.write("##### Resumo Estatístico por Ano")
st.dataframe(resumo_estatistico.style.format({
    'Média': "{:.2f}",
    'Mediana': "{:.2f}",
    'Mínimo': "{:.2f}",
    'Máximo': "{:.2f}"
}))







