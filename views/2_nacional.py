import streamlit as st
import folium
from streamlit_folium import st_folium


df = st.session_state['data']

st.title('Dados do Brasil')
st.divider()
anos = [2017, 2018, 2019, 2020, 2021, 2022, 2023]
ano = st.sidebar.selectbox('Ano', anos,)

estados = df['uf'].sort_values().unique().tolist()
estado = st.sidebar.selectbox('Estado', estados)

base_map = folium.Map(
        width='100%',
        height='100%',
        location = [-14.32639, -51.54889],
        zoom_start=4,
    )

style_func = lambda x: {'color':'black',
                    'fillOpacity': 0,
                    'weight':1}
folium.GeoJson('assets/br.geojson', style_function=style_func, name='Estados Brasil').add_to(base_map)

st_data = st_folium(base_map, width=2500, height=500)

st.dataframe(df.query('ano == @ano and uf==@estado'))