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
    
    # Intentar convertir las columnas a numérico de forma segura
    for col in df.columns:
        # Se intenta convertir; si no se puede, pd.to_numeric con coerce asigna NaN a textos inválidos
        converted = pd.to_numeric(df[col], errors='coerce')
        # Solo reemplazamos si la columna convertida tiene valores válidos
        if not converted.isna().all():
            df[col] = converted
        
    return df

df = cargar_datos()

st.title("📊 Panel de Depuración y Visualización de Sensores")

# Seleccionar columnas numéricas explícitamente para las métricas
num_cols = df.select_dtypes(include=[np.number]).columns

# Panel de Métricas (KPIs)
c1, c2, c3 = st.columns(3)
c1.metric("Total de Registros", len(df))

if len(num_cols) >= 1:
    col_x = num_cols[0]
    val_mean = df[col_x].mean()
    c2.metric(f"Promedio {col_x}", f"{val_mean:.2f}" if pd.notnull(val_mean) else "N/A")
else:
    c2.metric("Promedio Variable X", "N/A")

if len(num_cols) >= 2:
    col_y = num_cols[1]
    val_max = df[col_y].max()
    c3.metric(f"Máximo {col_y}", f"{val_max:.2f}" if pd.notnull(val_max) else "N/A")
else:
    c3.metric("Máximo Variable Y", "N/A")

# Pestañas con visualizaciones interactivas
tab1, tab2 = st.tabs(["📈 Gráfico 2D/3D Plotly", "🔥 Matriz de Correlación"])

with tab1:
    st.subheader("Gráfico Interactivo de Dispersión")
    if len(df.columns) >= 2:
        x_axis = df.columns[0]
        y_axis = df.columns[1]
        color_axis = df.columns[2] if len(df.columns) > 2 else None
        
        fig_scatter = px.scatter(df, x=x_axis, y=y_axis, color=color_axis)
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.warning("El dataset necesita al menos 2 columnas para el gráfico de dispersión.")

with tab2:
    st.subheader("Mapa de Calor Seaborn")
    df_corr = df.corr(numeric_only=True)
    if not df_corr.empty:
        fig_sns, ax = plt.subplots()
        sns.heatmap(df_corr, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig_sns)
    else:
        st.info("No hay columnas numéricas suficientes para calcular la matriz de correlación.")