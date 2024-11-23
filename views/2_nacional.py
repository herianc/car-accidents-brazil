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
st.title('Dados dos Nacionais 🇧🇷')
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
        st.line_chart(data=df_filtered['data_inversa'].value_counts(), height=250)
        
with col22:
    with st.container(border=True, height=333):
        st.markdown('**Distribuição por fase do dia**')
        labels = df_filtered['fase_dia'].value_counts().index
        values = df_filtered['fase_dia'].value_counts()
        fig = go.Figure(data=[go.Pie(labels=labels, 
                                        values=values, 
                                        hole=.3,
                                        textinfo='label+percent',
                                        title='Fases do dia')],
                        layout=go.Layout(height=400,
                                        width=400))
        fig.update(layout_showlegend=False)
        st.plotly_chart(fig, use_container_width=True)



# Terceira linha
col31, col32, col33 = st.columns(3)

with col31:
    with st.container(border=True):
        st.markdown('**Causa mais frequentes de acidente**')
        st.bar_chart(df_filtered['causa_acidente'].value_counts().sort_values(ascending=False).head(5),
                    horizontal=True,
                    height=300, width=700)
    
    
with col32:
    with st.container(border=True):
        st.markdown('**Acidentes por estado**')
        st.bar_chart(df_filtered.groupby('uf').count()['data_inversa'].sort_values(ascending=False),
                    height=300)
    
    
with col33:
    with st.container(border=True, height=383):
        st.map(df_filtered, height=300, size='pessoas', color='color')
        st.markdown('🔵 Ilesos  🟠 Feridos  🔴 Mortos') 
    

st.markdown('**Tabela de contingência Traçado da Via x Condição Meteorológica**')
st.table(pd.crosstab(df_filtered['tracado_via'], df_filtered['condicao_metereologica']))