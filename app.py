import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import bcrypt
st.set_page_config(page_title="Dashboard de Ventas", layout="wide")

# -------------------------
# 👤 USUARIOS
# -------------------------
users = {
    "migueesaz": bcrypt.hashpw("Yeezy21*".encode('utf-8'), bcrypt.gensalt()),
    "admin": bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
}
# -------------------------
# SESSION STATE
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# -------------------------
# LOGIN
# -------------------------
def login():
    st.title("🔒 Iniciar Sesión")

    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Entrar"):
        if username in users and bcrypt.checkpw(password.encode('utf-8'), users[username]):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")
# -------------------------
# DASHBOARD
# -------------------------
def dashboard():
    st.sidebar.title(f"Bienvenido, {st.session_state.username} 👋")

    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    st.title("📊 Dashboard de Ventas")
    st.write("Análisis de ventas por ciudad y persona")

    df = pd.read_csv("data.csv")
    st.sidebar.subheader("Filtros")
    #CIUDAD
    ciudad = st.sidebar.multiselect(
        "Ciudad",
        options=df["ciudad"].unique(),
        default=df["ciudad"].unique()
    )
    #VENTAS
    min_ventas, max_ventas = st.sidebar.slider(
        "Rango de Ventas",
        min_value=int(df["ventas"].min()),
        max_value=int(df["ventas"].max()),
        value=(int(df["ventas"].min()), int(df["ventas"].max()))
    )
    # EDAD
    min_edad, max_edad = st.sidebar.slider(
        "Rango de Edad",
        min_value=int(df["edad"].min()),
        max_value=int(df["edad"].max()),
        value=(int(df["edad"].min()), int(df["edad"].max()))
    )
    #NOMBRE
    busqueda_nombre = st.sidebar.text_input("Buscar por Nombre")
    df_filtrado = df[
        df["ciudad"].isin(ciudad) & 
        (df["ventas"] >= min_ventas) & 
        (df["ventas"] <= max_ventas) & 
        (df["edad"] >= min_edad) & (df["edad"] <= max_edad)
    ]
    if busqueda_nombre:
        df_filtrado = df_filtrado[
            df_filtrado["nombre"].str.contains(busqueda_nombre, case=False)
         ]
    st.sidebar.write(f"Total registros: {len(df_filtrado)}")
    if st.sidebar.button("Limpiar Filtros"):
        st.rerun()
    # 📊 Métricas
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Personas", len(df_filtrado))
    col2.metric("Edad Promedio", round(df_filtrado["edad"].mean(), 2))
    col3.metric("Ventas Totales", f"${df_filtrado['ventas'].sum():,.2f}")

    # 📈 Gráfico
    st.subheader("Ventas por persona")

    fig, ax = plt.subplots()
    ax.bar(df_filtrado["nombre"], df_filtrado["ventas"])
    plt.xticks(rotation=45)

    st.pyplot(fig)
    # 📋 Tabla
    st.subheader("Datos")
    st.dataframe(df_filtrado)
# -------------------------
# 🚀 CONTROL PRINCIPAL (ÚNICO)
# -------------------------
if st.session_state.logged_in:
    dashboard()
else:
    login()