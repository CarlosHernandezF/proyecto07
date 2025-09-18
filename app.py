import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------
# Función para cargar datos
# -------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("vehicles_us.csv")
        return df
    except FileNotFoundError:
        st.error("⚠️ No se encontró el archivo 'vehicles_us.csv'.")
        return None

# -------------------
# Función para graficar
# -------------------
def plot_histogram(df, column, title):
    fig = px.histogram(df, x=column, nbins=30, title=title)
    st.plotly_chart(fig)

def plot_scatter(df, x_col, y_col, title):
    fig = px.scatter(df, x=x_col, y=y_col, title=title)
    st.plotly_chart(fig)

# -------------------
# Interfaz Streamlit
# -------------------
st.title("Análisis de Vehículos - Proyecto 07")

df = load_data()

if df is not None and "odometer" in df.columns and "price" in df.columns:
    
    # Filtros
    st.sidebar.header("Filtros")
    odometer_range = st.sidebar.slider(
        "Selecciona rango de kilometraje",
        int(df["odometer"].min()), int(df["odometer"].max()),
        (int(df["odometer"].min()), int(df["odometer"].max()))
    )
    price_range = st.sidebar.slider(
        "Selecciona rango de precio",
        int(df["price"].min()), int(df["price"].max()),
        (int(df["price"].min()), int(df["price"].max()))
    )
    
    # Aplicar filtros
    filtered_df = df[
        (df["odometer"].between(*odometer_range)) &
        (df["price"].between(*price_range))
    ]

    st.subheader("📊 Histograma: Odómetro")
    plot_histogram(filtered_df, "odometer", "Distribución de Kilometraje")

    st.subheader("📈 Scatterplot: Odómetro vs Precio")
    plot_scatter(filtered_df, "odometer", "price", "Relación Kilometraje vs Precio")

else:
    st.warning("El dataset no tiene las columnas necesarias para graficar.")
