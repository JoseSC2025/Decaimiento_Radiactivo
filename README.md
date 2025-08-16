# requirements.txt
streamlit
numpy
pandas
matplotlib

# README.md
# 🧪 Simulador de Decaimiento Radiactivo

Este proyecto es una aplicación interactiva desarrollada en **Streamlit** que permite visualizar el **decaimiento radiactivo** de distintos isótopos.

## 🚀 Características
- Gráfica del decaimiento \(N(t)=N_0 e^{-\lambda t}\).
- Selección de isótopo desde un menú desplegable.
- Control de parámetros: número inicial de núcleos, unidad de tiempo, escala logarítmica.
- Cálculo y despliegue de parámetros físicos: semivida, constante de decaimiento, vida media y modo de decaimiento.
- Caja de texto con aplicaciones prácticas del isótopo.
- Descarga de datos en formato CSV.

## 📦 Instalación local
Clona este repositorio e instala dependencias:
```bash
pip install -r requirements.txt
```

Ejecuta la app:
```bash
streamlit run app.py
```

## ☁️ Despliegue en Streamlit Cloud
1. Sube este repositorio a GitHub.
2. Crea un nuevo proyecto en [Streamlit Community Cloud](https://share.streamlit.io).
3. Selecciona el repositorio y archivo `app.py`.

## 📚 Autores
- José Santa Cruz Delgado (y colaboradores)

## 📖 Nota
Los valores y datos son **aproximados** y se incluyen con fines **educativos**.
