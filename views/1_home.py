import streamlit as st

st.title('ACIDENTES RODOVIÁRIOS NO BRASIL (2017-2023) :collision::car:')
st.divider()
st.markdown("""
### Sobre o Conjunto de Dados
            
O dataset **Car Accidents in Brazil (2017-2023)**, disponível no Kaggle, contém informações detalhadas sobre acidentes de trânsito 
ocorridos no Brasil nesse período. Ele inclui dados como localização, causas dos acidentes, número de veículos envolvidos, e 
informações sobre vítimas, permitindo análises diversas, como tendências temporais e espaciais. 

Mais detalhes podem ser encontrados [aqui](https://www.kaggle.com/datasets/mlippo/car-accidents-in-brazil-2017-2023).

### Sobre o dashboard

Este dashboard foi feito como parte do trabalho final da disciplina de **Organização de Dados (ICP142)** do semestre 2024.2 do curso 
de Ciência da Computação da Universidade Federal do Rio de Janeiro.         
            
""")
st.image('images/logo_dcc.png', width=150)

# Centralizando a imagem
col1, col2, col3 = st.columns([1,3,1])

with col2:
    st.image('images/acidente_carro.jpg', 
            caption='📷️: Marcelo Ferreira/Correio Braziliense',
            width=850)