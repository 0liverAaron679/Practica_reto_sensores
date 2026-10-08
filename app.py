import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
 
st.set_page_config(
    page_title="Reto Semanal - Monitoreo Industrial",
    layout="wide"
)
 
@st.cache_data
def cargar_datos():
    # Reemplazar por el nombre de su archivo descargado
    df = pd.read_csv("datos_sensores.csv")
    return df
 
df = cargar_datos()
 
st.title("📊 Panel de Depuración y Visualización de Sensores")
 
# Panel de Métricas (KPIs)
c1, c2, c3 = st.columns(3)
c1.metric("Total de Registros", len(df))
c2.metric("Promedio Variable X", f"{df.iloc[:, 0].mean():.2f}")
c3.metric("Máximo Variable Y", f"{df.iloc[:, 1].max():.2f}")
 
# Pestañas con visualizaciones interactivas
tab1, tab2 = st.tabs(["📈 Gráfico 2D/3D Plotly", "🔥 Matriz de Correlación"])
 
with tab1:
    st.subheader("Gráfico Interactivo de Dispersión")
    fig_scatter = px.scatter(df, x=df.columns[0], y=df.columns[1], color=df.columns[2])
    st.plotly_chart(fig_scatter, use_container_width=True)
 
with tab2:
    st.subheader("Mapa de Calor Seaborn")
    fig_sns, ax = plt.subplots()
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig_sns)
