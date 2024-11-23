import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import plotly.graph_objects as go
import pandas as pd



df = st.session_state['data']

# Sidebar
anos = [2020, 2021, 2022, 2023]
ano = st.sidebar.selectbox('Ano', anos)

meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
mes = st.sidebar.selectbox('Mês', meses)

df_filtered = df.query('ano == @ano and mes == @mes')

# Conteúdo da pagina 
st.title('DADOS NACIONAIS 🇧🇷')
st.subheader(f'Dados de {mes}/{ano}')

# Primeira linha 
col11, col12, col13, col14 = st.columns(4)

with col11:
    with st.container(border=True):
        st.metric('Acidentes :construction:', df_filtered.shape[0])

with col12:
    with st.container(border=True):
        st.metric('Feridos leves 🤕', df_filtered['feridos_leves'].sum())
    
with col13:
    with st.container(border=True):
        st.metric('Feridos graves 🚑️', df_filtered['feridos_graves'].sum())
    
with col14:
    with st.container(border=True):
        st.metric('Mortos ☠️', df_filtered['mortos'].sum())
    

# Segunda linha
col21, col22 = st.columns(2)

with col21:
    with st.container(border=True):
        st.markdown(f'**Acidentes em {mes}/{ano}**')
        st.line_chart(data=df_filtered['data_inversa'].value_counts(), height=250, color='#FF79C6')
        
with col22:
    with st.container(border=True, height=333):
        st.markdown('**Causa mais frequentes de acidente**')
        
        causa_acidentes = df_filtered['causa_acidente'].value_counts().sort_values(ascending=False).head(5).reset_index().rename(columns={'causa_acidente':'Causa',
                                                                                                                                   'count':'Registros'})
        st.dataframe(
            causa_acidentes, 
            column_config={
            'Registros':st.column_config.ProgressColumn('Registros',
                                                    format='%d',
                                                    min_value=0,
                                                    max_value=int(causa_acidentes['Registros'].max()))
        })
                    



# Terceira linha
col31, col32, col33 = st.columns(3)

with col31:
    with st.container(border=True, height=383):
        st.markdown('**Distribuição por fase do dia**')
        labels = df_filtered['fase_dia'].value_counts().index
        values = df_filtered['fase_dia'].value_counts()
        fig = go.Figure(data=[go.Pie(labels=labels, 
                                        values=values, 
                                        hole=.3,
                                        textinfo='label+percent',
                                        title='Fases do dia')],
                        layout=go.Layout(height=300,
                                        width=300))
        fig.update(layout_showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
    
    
with col32:
    with st.container(border=True):
        st.markdown('**Acidentes por estado**')
        st.bar_chart(df_filtered.groupby('uf').count()['data_inversa'].sort_values(ascending=False),
                    height=300,
                    color='#FF79C6')
    
with col33:
    with st.container(border=True, height=383):
        st.map(df_filtered, height=300, size='pessoas', color='color')
        st.markdown('🔵 Ilesos  🟠 Feridos  🔴 Mortos') 


categorias = df_filtered['classificacao_acidente'].unique()

categoria = st.selectbox('Classificação do acidente', categorias)

st.markdown('**Tabela de contingência Traçado da Via x Condição Meteorológica**')
st.table(pd.crosstab(df_filtered.query('classificacao_acidente == @categoria')['tracado_via'], 
                     df_filtered.query('classificacao_acidente == @categoria')['condicao_metereologica'],
                     margins=True,
                     margins_name='Total'))