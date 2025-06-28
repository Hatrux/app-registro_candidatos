# -*- coding: utf-8 -*-
"""
Created on Fri Jun 20 19:01:07 2025

@author: 167676-1
"""

# formulario_entrevista.py

import streamlit as st
import pandas as pd
import datetime as dt
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title='Registro', page_icon=':pineapple:', layout='wide', initial_sidebar_state='auto')

class AppCandidatos:
    def __init__(self):
        path = os.path.join(os.getcwd(), 'resultados/candidatos.csv')

        try:
            df = pd.read_csv(path)
            st.session_state.df = df
            if 'candidatos' not in st.session_state:
                st.session_state.candidatos = df.to_dict(orient='records')
        except FileNotFoundError:
            st.session_state.candidatos = []
            st.session_state.df = pd.DataFrame()
    
    def vista_registro_candidatos(self):
        st.title('Registro de candidatos')
        st.write('Por favor, rellene los siguientes campos:')
        
        with st.form('formulario_candidatos'):
            col1, col2 = st.columns(2)
            with col1:
                nombre = st.text_input('Nombre completo', placeholder='Escribe tu nombre', label_visibility='visible')
                edad = st.slider('Edad: ', value=30, min_value=18, max_value=99)
                genero = st.radio('Género: ', ['Masculino', 'Femenino', 'Otro'])
            with col2:
                nivel_estudios = st.selectbox('Nivel de estudios: ', ['Licenciatura', 'Maestría', 'Doctorado'])
                idiomas = st.multiselect('Idiomas: ', ['Inglés', 'Frances', 'Alemán', 'Español', 'Chino'])
                salario = st.number_input('Salario actual (MXN)', min_value=0, step=500)
                experiencia = st.checkbox('¿Tienes experiencia?')
            with st.expander('Más opciones'):
                fecha = st.date_input('Fecha de entrevista: ')
                hora = st.time_input('Hora de entrevista: ', step=dt.timedelta(minutes=30))
            cv = st.file_uploader('Subir curriculum (PDF)', type=['pdf'], accept_multiple_files=False)
            enviado = st.form_submit_button("Registrar")

            if enviado:
                nuevo = {
                    'Nombre': nombre,
                    'Edad': edad,
                    'Salario': salario,
                    'Experiencia': experiencia,
                    'Genero': genero,
                    'Nivel_estudios': nivel_estudios,
                    'Idiomas': ', '.join(idiomas),
                    'Entrevista': f'{fecha} {hora}',
                    'CV subido': 'SI' if cv else 'NO'
                }
                st.session_state.candidatos.append(nuevo)
                st.success('Candidato registrado')
                # Replace DataFrame and save
                st.session_state.df = pd.DataFrame(st.session_state.candidatos)
                path = os.path.join(os.getcwd(), 'resultados/candidatos.csv')
                st.session_state.df.to_csv(path, index=False)
    
    def vista_consulta_candidatos(self):
        if not st.session_state.df.empty:
            st.success('Candidatos recuperados exitosamente del archivo')
            st.subheader("Consulta de candidatos")
            st.dataframe(st.session_state.df)
            csv = st.session_state.df.to_csv(index=False).encode('utf-8')
            st.download_button('Descargar csv', csv, file_name='candidatos.csv', mime='text/csv')
        else:
            st.info("No hay candidatos registrados aún.")
    
    def vista_visualizar_grafica(self):
        df = st.session_state.df
        if not df.empty:
            # Opción 1
            niveles = ['Licenciatura', 'Maestría', 'Doctorado']
            seleccion = st.multiselect('Selecciona los niveles', niveles, default = niveles)
            condicion = df['Nivel_estudios'].isin(seleccion)
            df_filtrado = df[condicion]
            fig, ax = plt.subplots()
            sns.boxplot(df_filtrado, x = 'Nivel_estudios', y = 'Salario', hue = 'Nivel_estudios', ax = ax)            
            ax.set_title('Distribución de salarios por nivel de estudios')
            st.pyplot(fig)
            # Opción 2
            fig_plotly = px.box(
                df_filtrado, 
                x = 'Nivel_estudios',
                y = 'Salario',
                color = 'Nivel_estudios',
                title = 'Distribución de salarios por nivel de estudios',
                #category_orders = ('Estudios': niveles)
                )
            st.plotly_chart(fig_plotly)
        else:
            st.info('No hay candidatos registrados')
    
    def run(self):
        st.sidebar.title('Menú')
        opcion = st.sidebar.selectbox('Ir a:', ['Registro', 'Consulta', 'Gráficas'])
        if opcion == 'Registro':
            self.vista_registro_candidatos()
        elif opcion == 'Consulta':
            self.vista_consulta_candidatos()
        elif opcion == 'Gráficas':
            self.vista_visualizar_grafica()
    
app = AppCandidatos()
app.run()