import streamlit as st
import pandas as pd

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

homepage = st.Page(page='views/1_home.py', 
                title='Dashboard', 
                icon='📊',
                default=True
)
page2 = st.Page(page='views/2_nacional.py', 
                title='Dados Nacionais',
                icon='🇧🇷'
)
page3 = st.Page(page='views/3_estado.py',
                title='Dados Estaduais',
                icon='🏛️')

pages = {
    "Páginas":[homepage, page2, page3]
}

if 'data' not in st.session_state:
    df = pd.read_csv('acidentes_brasil.csv')
    
    df['data_inversa'] = pd.to_datetime(df['data_inversa'])
    # Criando a coluna de mês e ano
    df['ano'] = df['data_inversa'].dt.year
    df['mes'] = df['data_inversa'].dt.month
    # Selecionando os dados que não serão utilizados
    
    st.session_state['data'] = df


st.logo('images/logo_ufrj.png', size='large')
    
pg = st.navigation(pages)
pg.run()