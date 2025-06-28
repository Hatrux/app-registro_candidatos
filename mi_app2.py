# -*- coding: utf-8 -*-
"""
Created on Fri Jun 20 19:52:21 2025

@author: 167676-1
"""

import streamlit as st
import pandas as pd

# Botón
boton1 = st.button('Haz click aquí')
if boton1:
    st.success('¡Botón presionado!')

# Botón de formulario
with st.form('formulario'):
    nombre = st.text_input('Nombre: ')
    boton2 = st.form_submit_button('Enviar formulario')
if boton2:
    st.success('Formulario enviado')

# Botón descarga
data = 'Éste es un ejemplo de descarga de archivo'
boton3 = st.download_button('Descargar texto', data, file_name='archivo.txt')
if boton3:
    st.success('Archivo descargado')
#csv = df.to_csv()

archivo = st.file_uploader('Subir un archivo', type=['csv'])


valores = {
        'Nombre' : ['Ana', 'Luis', 'María'],
        'Edad': [25, 30, 35],
        'Salario' : [10000, 20000, 30000]
    }
df = pd.DataFrame(valores)

st.header('Mostrar datos tabulares')
st.write('Mostrar datos con write')
st.write(df)

st.write('Mostrar datos con dataframe')
st.dataframe(df)

st.write('Mostrar datos con tabla')
st.table(df)