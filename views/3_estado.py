import streamlit as st
import plotly.graph_objects as go

# Cor padrão para os gráficos
COLOR = '#BD93F9'

# Recuperando os dados carregados
df = st.session_state['data']

# Botões laterais para filtragem 
estados = df['uf'].sort_values().unique()
estado = st.sidebar.selectbox('Estado', estados)

df_filtered = df.query('uf == @estado')

anos = [2017, 2018, 2019, 2020, 2021, 2022]
ano = st.sidebar.selectbox('Ano', anos)

df_filtered = df_filtered.query('uf == @estado and ano == @ano')

st.image(df_filtered.iloc[0]["uf_img"])

# Primeira linha
col11, col12, col13 = st.columns([1,3,1])

with col11:
    with st.container(border=True, height=155):
        st.metric('**Acidentes** :construction:', df_filtered.shape[0])
    with st.container(border=True, height=155):
        st.metric('**Feridos leves** 🤕', df_filtered['feridos_leves'].sum())

with col12:
    with st.container(border=True):
        st.markdown(f'**Acidentes em {ano}**')
        st.line_chart(data=df_filtered['data_inversa'].value_counts(), height=250, color=COLOR)
        
with col13:
    with st.container(border=True, height=155):
        st.metric('**Feridos graves** 🚑️', df_filtered['feridos_graves'].sum())
    with st.container(border=True, height=155):
        st.metric('**Mortos** ☠️', df_filtered['mortos'].sum())


# Segunda linha        
col21, col22 = st.columns(2)

with col21:
    with st.container(border=True, height=383):
        st.map(df_filtered, height=300, size='pessoas', color='color')
        st.markdown('🔵 Ilesos  🟠 Feridos  🔴 Mortos')
              
with col22:
    with st.container(border=True, height=383):
        st.subheader('Acidentes por município')
        st.table(df_filtered['municipio'].value_counts().rename('Acidentes'))


# Terceira linha
col31, col32 = st.columns(2)

with col31:
    with st.container(border=True):
        st.markdown('**Causa mais frequentes de acidente**')
        
        causa_acidentes = df_filtered['causa_acidente'].value_counts().sort_values(ascending=False).head(6).reset_index().rename(columns={'causa_acidente':'Causa',
                                                                                                                                   'count':'Registros'})
        st.dataframe(
            causa_acidentes, 
            column_config={
            'Registros':st.column_config.ProgressColumn('Registros',
                                                    format='%d',
                                                    min_value=0,
                                                    max_value=int(causa_acidentes['Registros'].max()),
                                                    width='medium')
        }, 
        hide_index=True)
        
with col32:
    with st.container(border=True, height=327):
        labels = df_filtered['fase_dia'].value_counts().index
        values = df_filtered['fase_dia'].value_counts()
        fig = go.Figure(data=[go.Pie(labels=labels, 
                                        values=values, 
                                        hole=.7,
                                        textinfo='label+percent',
                                        title='Fases do dia')],
                        layout=go.Layout(height=300,
                                        width=300))
        fig.update(layout_showlegend=False)
        fig.update_layout(title={'text':'Distribuição das fases do dia'})
        st.plotly_chart(fig, use_container_width=True)
