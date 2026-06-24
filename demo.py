import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Dashboard de Residuos Municipales",
    layout="wide"
)

df = pd.read_excel("Dataset.xlsx")



tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📖 Introducción",
    "📊 Gráficos",
    "📅 Análisis por Año",
    "👤 Residuos Per Cápita",
    "📋 Datos"
])



with tab1:

    st.title("♻️ Dashboard de Residuos Municipales del Perú")

    st.image(
        "https://images.unsplash.com/photo-1532996122724-e3c354a0b15b",
        use_container_width=True
    )

    st.markdown("""
    ## Introducción

    La adecuada gestión de residuos sólidos es uno de los principales retos
    ambientales en las ciudades del Perú. El crecimiento poblacional,
    la urbanización y el incremento del consumo generan cada año una mayor
    cantidad de residuos que deben ser recolectados y tratados de forma eficiente.

    Este dashboard utiliza información oficial sobre residuos municipales
    para analizar el comportamiento de los diferentes departamentos,
    provincias y distritos del país.

    ### Objetivos del proyecto

    - Analizar la generación de residuos municipales.
    - Comparar la producción de residuos entre departamentos.
    - Evaluar la evolución de los residuos a lo largo de los años.
    - Estudiar la distribución entre residuos domiciliarios y no domiciliarios.
    - Analizar la generación per cápita de residuos.

    ### Variables Analizadas

    - Población total.
    - Población urbana.
    - Población rural.
    - Residuos domiciliarios.
    - Residuos no domiciliarios.
    - Residuos municipales totales.
    - Generación per cápita (GPC).

    ### Fuente de Datos

    Datos de generación de residuos municipales del Perú
correspondientes al periodo 2014-2024.
    """)



with tab2:

    st.header("Filtros")

    col1, col2, col3 = st.columns(3)

    departamentos = ["Todos"] + sorted(
        df["DEPARTAMENTO"].dropna().unique()
    )

    with col1:
        departamento = st.selectbox(
            "Departamento",
            departamentos
        )

    df_filtrado = df.copy()

    if departamento != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado["DEPARTAMENTO"] == departamento
        ]

    provincias = ["Todos"] + sorted(
        df_filtrado["PROVINCIA"].dropna().unique()
    )

    with col2:
        provincia = st.selectbox(
            "Provincia",
            provincias
        )

    if provincia != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado["PROVINCIA"] == provincia
        ]

    distritos = ["Todos"] + sorted(
        df_filtrado["DISTRITO"].dropna().unique()
    )

    with col3:
        distrito = st.selectbox(
            "Distrito",
            distritos
        )

    if distrito != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado["DISTRITO"] == distrito
        ]

    st.success(
        f"Mostrando información de: {departamento} | {provincia} | {distrito}"
    )

    st.markdown("---")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total de Registros",
        len(df_filtrado)
    )

    c2.metric(
        "Residuos Municipales",
        f"{df_filtrado['QRESIDUOS_MUN'].sum():,.2f}"
    )

    c3.metric(
        "Distritos Analizados",
        df_filtrado["DISTRITO"].nunique()
    )

    st.markdown("---")

    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:

        st.subheader("Evolución de Residuos Municipales")

        residuos_anio = (
            df_filtrado
            .groupby("PERIODO")["QRESIDUOS_MUN"]
            .sum()
        )

        fig1, ax1 = plt.subplots(figsize=(8,4))

        ax1.plot(
            residuos_anio.index,
            residuos_anio.values,
            marker="o"
        )

        ax1.set_title("Evolución por Año")
        ax1.set_xlabel("Periodo")
        ax1.set_ylabel("Residuos Municipales")
        ax1.grid(True)

        st.pyplot(fig1)

    with col_graf2:

        st.subheader("Distribución de Residuos")

        residuos_dom = df_filtrado["QRESIDUOS_DOM"].sum()
        residuos_no_dom = df_filtrado["QRESIDUOS_NO_DOM"].sum()

        fig2, ax2 = plt.subplots(figsize=(6,6))

        ax2.pie(
            [residuos_dom, residuos_no_dom],
            labels=[
                "Domiciliarios",
                "No domiciliarios"
            ],
            autopct="%1.1f%%"
        )

        ax2.set_title("Distribución de Residuos")

        st.pyplot(fig2)

    st.markdown("---")

    st.subheader(
        "Top 10 Distritos con Mayor Generación de Residuos"
    )

    top_distritos = (
        df_filtrado
        .groupby("DISTRITO")["QRESIDUOS_MUN"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig3, ax3 = plt.subplots(figsize=(10,5))

    ax3.bar(
        top_distritos.index,
        top_distritos.values
    )

    ax3.set_title("Top 10 Distritos")
    ax3.set_xlabel("Distrito")
    ax3.set_ylabel("Residuos Municipales")

    plt.xticks(rotation=45)

    st.pyplot(fig3)

    st.markdown("---")

    st.subheader("Población Urbana vs Rural")

    urbana = df_filtrado["POB_URBANA"].sum()
    rural = df_filtrado["POB_RURAL"].sum()

    fig4, ax4 = plt.subplots(figsize=(8,4))

    ax4.bar(
        ["Población Urbana", "Población Rural"],
        [urbana, rural]
    )

    ax4.set_title("Distribución de la Población")
    ax4.set_ylabel("Habitantes")

    st.pyplot(fig4)


with tab3:

    st.subheader("Análisis por Año")

    anios = sorted(df["PERIODO"].unique())

    anio = st.selectbox(
        "Seleccione un Año",
        anios
    )

    st.markdown(f"## 📅 Análisis del Año {anio}")

    df_anio = df[
        df["PERIODO"] == anio
    ]

    residuos_dep = (
        df_anio
        .groupby("DEPARTAMENTO")["QRESIDUOS_DOM"]
        .sum()
        .sort_values(ascending=False)
    )

    fig5, ax5 = plt.subplots(figsize=(10,5))

    ax5.bar(
        residuos_dep.index,
        residuos_dep.values
    )

    ax5.set_title(
        f"Residuos Domiciliarios por Departamento - {anio}"
    )

    ax5.set_xlabel("Departamentos")
    ax5.set_ylabel("Cantidad")

    plt.xticks(rotation=90)

    st.pyplot(fig5)



with tab4:

    st.header("👤 Análisis de Residuos Per Cápita")

    st.write("""
    La generación per cápita representa la cantidad promedio de residuos
    generados por habitante por día.
    """)

    percapita_dep = (
        df.groupby("DEPARTAMENTO")["GPC_DOM"]
        .mean()
        .sort_values(ascending=False)
    )

    fig6, ax6 = plt.subplots(figsize=(12,5))

    ax6.bar(
        percapita_dep.index,
        percapita_dep.values
    )

    ax6.set_title(
        "Generación Per Cápita por Departamento"
    )

    ax6.set_xlabel("Departamento")
    ax6.set_ylabel("kg/hab/día")

    plt.xticks(rotation=90)

    st.pyplot(fig6)

    st.metric(
        "Promedio Nacional",
        f"{df['GPC_DOM'].mean():.2f} kg/hab/día"
    )

    st.markdown("---")

    st.subheader(
        "Top 10 Distritos con Mayor Generación Per Cápita"
    )

    top_pc = (
        df.groupby("DISTRITO")["GPC_DOM"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    fig7, ax7 = plt.subplots(figsize=(10,5))

    ax7.bar(
        top_pc.index,
        top_pc.values
    )

    ax7.set_title(
        "Top 10 Distritos por Generación Per Cápita"
    )

    plt.xticks(rotation=45)

    st.pyplot(fig7)



with tab5:

    st.subheader("Datos Filtrados")

    st.dataframe(df)
