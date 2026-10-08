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
        converted = pd.to_numeric(df[col], errors='coerce')
        if not converted.isna().all():
            df[col] = converted
            
    return df

df = cargar_datos()

st.title("📊 Panel de Depuración y Visualización de Sensores")

# Seleccionar columnas numéricas explícitamente para las métricas y gráficos
num_cols = df.select_dtypes(include=[np.number]).columns.tolist()

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
    
    if len(num_cols) >= 2:
        # Selector de dimensiones (2D vs 3D)
        tipo_grafico = st.radio(
            "Selecciona la dimensión del gráfico:",
            ["2D", "3D"],
            horizontal=True
        )
        
        # Selección de ejes
        col_controls = st.columns(4 if tipo_grafico == "3D" else 3)
        
        with col_controls[0]:
            eje_x = st.selectbox("Eje X", options=num_cols, index=0)
        with col_controls[1]:
            eje_y = st.selectbox("Eje Y", options=num_cols, index=min(1, len(num_cols)-1))
            
        if tipo_grafico == "3D":
            with col_controls[2]:
                eje_z = st.selectbox("Eje Z", options=num_cols, index=min(2, len(num_cols)-1))
            with col_controls[3]:
                eje_color = st.selectbox("Color (Opcional)", options=["Ninguno"] + list(df.columns), index=0)
        else:
            with col_controls[2]:
                eje_color = st.selectbox("Color (Opcional)", options=["Ninguno"] + list(df.columns), index=0)

        color_var = None if eje_color == "Ninguno" else eje_color

        # Generación del gráfico según la selección
        if tipo_grafico == "2D":
            fig = px.scatter(
                df, 
                x=eje_x, 
                y=eje_y, 
                color=color_var,
                title=f"Dispersión 2D: {eje_x} vs {eje_y}"
            )
        else:
            fig = px.scatter_3d(
                df, 
                x=eje_x, 
                y=eje_y, 
                z=eje_z, 
                color=color_var,
                title=f"Dispersión 3D: {eje_x} vs {eje_y} vs {eje_z}"
            )
            
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Se necesitan al menos 2 columnas numéricas para generar las visualizaciones.")

with tab2:
    st.subheader("Mapa de Calor Seaborn")
    df_corr = df.corr(numeric_only=True)
    if not df_corr.empty:
        fig_sns, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(df_corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
        st.pyplot(fig_sns)
    else:
        st.info("No hay columnas numéricas suficientes para calcular la matriz de correlación.")