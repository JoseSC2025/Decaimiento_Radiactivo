import streamlit as st
import numpy as np
import pandas as pd
import math

# ------------------------------------------------------------
# APP: Gráfica interactiva de decaimiento radiactivo
# Autor: (tu nombre)
# Despliegue: Coloca este archivo como app.py en tu repo de GitHub
# Requisitos sugeridos (requirements.txt):
#   streamlit
#   numpy
#   pandas
#   matplotlib
# ------------------------------------------------------------

st.set_page_config(
    page_title="Decaimiento radiactivo",
    page_icon="🧪",
    layout="centered"
)

st.title("🧪 Decaimiento radiactivo — simulador interactivo")
st.write(
    """
    Explora el modelo de **decaimiento radiactivo** \(N(t)=N_0 e^{-\lambda t}\). 
    Elige un isótopo, ajusta el tiempo y el número inicial de núcleos, y observa la curva de decaimiento.
    """
)

# ----------------------------
# Datos de isótopos (valores aproximados y de uso educativo)
# t_1/2 en segundos
# ----------------------------
AÑO = 365.25*24*3600
DIA = 24*3600
HORA = 3600
MIN = 60

isotopos = {
    "Carbono-14 (C-14)": {
        "t12_s": 5730 * AÑO,
        "modo": "β⁻",
        "nota_t12": "5730 años",
        "aplicacion": "Datación radiocarbónica en arqueología y geología."
    },
    "Uranio-238 (U-238)": {
        "t12_s": 4.468e9 * AÑO,
        "modo": "α",
        "nota_t12": "4.47 × 10⁹ años",
        "aplicacion": "Relojes geológicos y fuente de calor interno terrestre."
    },
    "Iodo-131 (I-131)": {
        "t12_s": 8.02 * DIA,
        "modo": "β⁻, γ",
        "nota_t12": "≈ 8 días",
        "aplicacion": "Diagnóstico y tratamiento de trastornos tiroideos."
    },
    "Cobalto-60 (Co-60)": {
        "t12_s": 5.27 * AÑO,
        "modo": "β⁻, γ",
        "nota_t12": "5.27 años",
        "aplicacion": "Radioterapia y gammagrafía industrial."
    },
    "Tecnecio-99m (Tc-99m)": {
        "t12_s": 6 * HORA,
        "modo": "isómero → γ",
        "nota_t12": "6 horas",
        "aplicacion": "Imagenología médica (medicina nuclear)."
    },
    "Cesio-137 (Cs-137)": {
        "t12_s": 30.17 * AÑO,
        "modo": "β⁻, γ",
        "nota_t12": "30.17 años",
        "aplicacion": "Calibración de detectores y rastreo ambiental."
    },
    "Radón-222 (Rn-222)": {
        "t12_s": 3.8235 * DIA,
        "modo": "α",
        "nota_t12": "≈ 3.82 días",
        "aplicacion": "Trazador en estudios de ventilación y geofísica."
    },
    "Plutonio-239 (Pu-239)": {
        "t12_s": 24100 * AÑO,
        "modo": "α",
        "nota_t12": "24 100 años",
        "aplicacion": "Combustible en reactores y fuentes de neutrones."
    }
}

# ----------------------------
# Barra lateral — controles
# ----------------------------
st.sidebar.header("Controles")
iso_nombre = st.sidebar.selectbox("Isótopo", list(isotopos.keys()))
info = isotopos[iso_nombre]

N0 = st.sidebar.number_input(
    "Núcleos iniciales N₀",
    min_value=1.0,
    value=1e6,
    step=1e5,
    format="%.0f"
)

unidades = {
    "segundos": 1.0,
    "minutos": MIN,
    "horas": HORA,
    "días": DIA,
    "años": AÑO,
}
unidad_sel = st.sidebar.selectbox("Unidad de tiempo", list(unidades.keys()), index=4)

# Escala de tiempo: hasta k semividas
k_semividas = st.sidebar.slider("Rango de tiempo (en múltiplos de t₁/₂)", 0.5, 10.0, 5.0, 0.5)
logy = st.sidebar.checkbox("Escala logarítmica (eje y)", value=False)

# ----------------------------
# Cálculos
# ----------------------------
t12 = info["t12_s"]
lam = math.log(2) / t12  # constante de decaimiento λ [1/s]
tau = 1.0 / lam          # vida media τ [s]

# tiempo máximo en segundos y en la unidad elegida
Tmax_s = k_semividas * t12
factor = unidades[unidad_sel]
Tmax_u = Tmax_s / factor

# Resolución de la malla de tiempos
num_pts = 600

t_u = np.linspace(0, Tmax_u, num_pts)  # vector en unidades elegidas
t_s = t_u * factor                     # vector en segundos (para el modelo)

N_t = N0 * np.exp(-lam * t_s)
A_t = lam * N_t  # Actividad proporcional a λ N(t) (en unidades arbitrarias si no se dan desintegraciones/s)

# ----------------------------
# Gráfica
# ----------------------------
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(t_u, N_t, linewidth=2)
ax.set_xlabel(f"t [{unidad_sel}]")
ax.set_ylabel("N(t)")
ax.set_title(f"Decaimiento de {iso_nombre}")
if logy:
    ax.set_yscale('log')
ax.grid(True, alpha=0.3)
st.pyplot(fig, use_container_width=True)

# ----------------------------
# Datos y descarga
# ----------------------------
df = pd.DataFrame({
    f"t ({unidad_sel})": t_u,
    "N(t)": N_t,
    "Actividad ∝ λN(t)": A_t,
})

st.download_button(
    label="Descargar datos (CSV)",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name=f"decaimiento_{iso_nombre.replace(' ', '_')}.csv",
    mime="text/csv",
)

# Mostrar primeras filas de referencia
st.dataframe(df.head(10))

# ----------------------------
# Resumen de características físicas
# ----------------------------
col1, col2 = st.columns(2)
with col1:
    st.subheader("Parámetros del modelo")
    st.latex(r"N(t) = N_0\, e^{-\lambda t}")
    st.markdown(
        f"""
        - **Semivida** \(t_{{1/2}}\): **{info['nota_t12']}**  
        - **Constante de decaimiento** \(\lambda\): **{lam:.3e}\, s^{{-1}}**  
        - **Vida media** \(\tau = 1/\lambda\): **{tau:.3e}\, s**  
        - **Modo de decaimiento**: **{info['modo']}**
        """
    )

with col2:
    st.subheader("Actividad (proporcional)")
    st.markdown(
        f"""
        - **Actividad inicial** \(A_0 = \lambda N_0\): **{(lam*N0):.3e}** (u. arb.)  
        - **Actividad a t = t₁/₂**: **{(lam*N0*np.exp(-lam*t12)):.3e}** (u. arb.)  
        - **Fracción remanente a t = t₁/₂**: **50\%**
        """
    )

# ----------------------------
# Aplicación del isótopo (texto breve)
# ----------------------------
st.subheader("Aplicación del isótopo")
st.text_area(
    label="Uso típico (editable)",
    value=info["aplicacion"],
    height=90
)

# ----------------------------
# Notas
# ----------------------------
with st.expander("Notas y consideraciones"):
    st.markdown(
        """
        - Este simulador usa un **modelo de decaimiento exponencial simple** y valores aproximados, con fines educativos.  
        - La actividad mostrada es proporcional a \(\lambda N(t)\) y no está calibrada en Bq a menos que se indique el número real de núcleos y la tasa de desintegración en s⁻¹.  
        - La escala temporal se fija como múltiplos de la semivida para facilitar la visualización.  
        - Puedes **editar** la caja de texto de la aplicación para personalizarla.
        """
    )
