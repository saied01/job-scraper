import streamlit as st
import plotly.express as px
import sqlite3
import pandas as pd
import os


# CONNECT DASHBOARD TO DB

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "database.db")

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM data_table", conn)
conn.close()


# GET DATA FROM COMPANIES
empresas = df['empresa'].unique()
seleccion_empresas = st.multiselect("Seleccionar empresas", empresas, default=empresas)

filtered_df = df[df['empresa'].isin(seleccion_empresas)]

def parse_salario(s):
    if pd.isna(s): return 0
    s = s.replace("$","").replace(".","").replace(",",".").split()[0]
    try:
        return float(s)
    except:
        return 0

filtered_df['salario_num'] = filtered_df['salario'].apply(parse_salario)


# DISPLAY DATA
st.bar_chart(filtered_df.groupby('ubicacion')['salario_num'].mean())


fig = px.box(filtered_df, x='modalidad', y='salario_num')
st.plotly_chart(fig)

st.dataframe(filtered_df)
