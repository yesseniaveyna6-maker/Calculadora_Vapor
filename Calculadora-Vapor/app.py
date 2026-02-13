import streamlit as st
import pandas as pd
import numpy as np
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------
# ESTILO CORPORATIVO
# ---------------------------------------------------
st.markdown("""
<style>

/* Fondo degradado azul */
.stApp {
    background: linear-gradient(180deg, #0B1F3B 0%, #163A6B 40%, #FFFFFF 100%);
}

/* Línea dorada */
hr {
    border: none;
    height: 4px;
    background-color: #C8A951;
}

/* Titulos en blanco */
h1, h2, h3 {
    color: white;
}

/* Números de métricas */
[data-testid="stMetricValue"] {
    color: #0B1F3B;
    font-weight: bold;
}

/* Tarjetas blancas */
[data-testid="stMetric"] {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    border-left: 5px solid #C8A951;
}


            
[data-testid="stMetric"] {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    border-left: 5px solid #C8A951;
}

        
.stApp {
    background: linear-gradient(180deg, #0B1F3B 0%, #163A6B 40%, #FFFFFF 100%);
}

hr {
    border: none;
    height: 4px;
    background-color: #C8A951;
}

[data-testid="stMetricValue"] {
    color: #0B1F3B;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# CONFIGURACIÓN
# ---------------------------------------------------
st.set_page_config(
    page_title="Impacto por Fugas de Vapor",
    page_icon="🏭",
    layout="wide"
)

# ---------------------------------------------------
# LOGOS
# ---------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.image(os.path.join(BASE_DIR, "logo1.png"), width=140)

with col2:
    st.image(os.path.join(BASE_DIR, "logo2.png"), width=140)

with col3:
    st.image(os.path.join(BASE_DIR, "logo3.png"), width=140)

with col4:
    st.image(os.path.join(BASE_DIR, "logo4.png"), width=140)


st.divider()

# ---------------------------------------------------
# TITULOS
# ---------------------------------------------------
st.title("Impacto Energético por Fugas de Vapor")
st.markdown("### Conversión a energía y afectación del TPE")
st.divider()

# ---------------------------------------------------
# CONSTANTES
# ---------------------------------------------------
COSTO_MJ = 0.089
ENTALPIA = 2409 / 1000  # MJ/kg

# hectolitros reales
HL_DIA = 58333.33
HL_MES = 1750000
HL_ANIO = 21000000

# ---------------------------------------------------
# TABLA
# ---------------------------------------------------
df = pd.read_excel("fugas_vapor.xlsx")

diametros = df["diametro_mm"].values
flujos = df["kg_h"].values

# ---------------------------------------------------
# COLUMNAS PRINCIPALES
# ---------------------------------------------------
col1, col2 = st.columns([1, 1])

# ===================================================
# ENTRADAS
# ===================================================
with col1:
    st.header("Datos de entrada")

    metodo = st.radio(
        "Método de cálculo",
        ("Diámetro de orificio", "Vapor conocido (kg/h)")
    )

    if metodo == "Diámetro de orificio":
        diametro = st.number_input(
            "Diámetro (mm)",
            min_value=1,
            step=1,
            format="%d"
        )

        # interpolación + extrapolación
        kg_h = np.interp(diametro, diametros, flujos)

    else:
        kg_h = st.number_input("Vapor perdido (kg/h)", min_value=0.0)

    tiempo = st.number_input(
        "Tiempo",
        min_value=1,
        step=1,
        format="%d"
    )

    unidad = st.selectbox(
        "Unidad",
        ("Minutos", "Horas", "Días", "Meses")
    )

    if unidad == "Minutos":
        horas = tiempo / 60
    elif unidad == "Horas":
        horas = tiempo
    elif unidad == "Días":
        horas = tiempo * 24
    else:
        horas = tiempo * 24 * 30

# ===================================================
# CÁLCULOS
# ===================================================
calcular = st.button("Calcular impacto")

if calcular:
    kg_total = kg_h * horas
    energia = kg_total * ENTALPIA
    costo = energia * COSTO_MJ

    tpe_dia = energia / HL_DIA
    tpe_mes = energia / HL_MES
    tpe_anio = energia / HL_ANIO


# ===================================================
# RESULTADOS
# ===================================================
with col2:
    st.header("Resultados")

    if calcular:
        st.metric("Energía perdida (MJ)", f"{energia:,.2f}")
        st.metric("Costo estimado", f"${costo:,.2f}")

        st.divider()
        st.subheader("Impacto en TPE")
        st.metric("Día (MJ/hL)", f"{tpe_dia:,.4f}")
        st.metric("Mes (MJ/hL)", f"{tpe_mes:,.4f}")
        st.metric("Año (MJ/hL)", f"{tpe_anio:,.4f}")
    else:
        st.info("Ingrese los datos y presione **Calcular impacto**")

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.divider()
st.caption("Herramienta para evaluación de pérdidas energéticas | 2026")





