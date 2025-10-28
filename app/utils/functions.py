import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import seaborn as sns
import pandas as pd
import streamlit as st
import geopandas as gpd
from utils.bigquery import query_data
import utils.queries as q

# Cargamos los mapas de México una sola vez
@st.cache_data
def get_world_map():
    """Carga y cachea el mapa mundial de baja resolución."""
    url = "https://naturalearth.s3.amazonaws.com/10m_cultural/ne_10m_admin_0_countries.zip"
    world_countries = gpd.read_file(url)
    return world_countries[world_countries['CONTINENT'] == 'North America']

@st.cache_data
def get_mexico_states_map():
    """Carga y cachea las fronteras de los estados de México."""
    url = "https://naturalearth.s3.amazonaws.com/10m_cultural/ne_10m_admin_1_states_provinces.zip"
    world_states = gpd.read_file(url)
    mexico_states = world_states[world_states['admin'] == 'Mexico']
    return mexico_states

# FUNCIÓN PARA CARGAR LOS KPIs

@st.cache_data(ttl=3600) # Cachea los KPIs por 1 hora 
def load_all_kpis():
    """
    Carga todos los datos de los KPIs desde BigQuery en una sola función
    y los devuelve en un diccionario formateado.
    """
    try:
        # 1. Pico Ocupación
        df1 = query_data(q.KPI_1_PICO_OCUPACION)
        kpi1 = f"~{df1['kpi_value'].iloc[0]:,.0f}"

        # 2. Rango Ingresos
        df2 = query_data(q.KPI_2_RANGO_INGRESOS)
        kpi2 = f"{df2['kpi_min'].iloc[0]}-{df2['kpi_max'].iloc[0]}"

        # 3. Mediana Estancia
        df3 = query_data(q.KPI_3_MEDIANA_ESTANCIA)
        kpi3 = f"{df3['kpi_value'].iloc[0]} Días"

        # 4. Carga Tercer Nivel
        df4 = query_data(q.KPI_4_CARGA_TERCER_NIVEL)
        kpi4 = f"~{df4['kpi_value'].iloc[0]} Ingresos/Día"

        return {
            "pico_ocupacion": kpi1,
            "rango_ingresos": kpi2,
            "mediana_estancia": kpi3,
            "carga_tercer_nivel": kpi4
        }
        
    except Exception as e:
        print(f"Error al cargar KPIs: {e}")
        # En caso de error, devuelve los valores placeholder
        return { 
            "pico_ocupacion": "~3,600",
            "rango_ingresos": "400-800",
            "mediana_estancia": "5 Días",
            "carga_tercer_nivel": "~20 Ingresos/Día"
        }

# FUNCIONES ANALISIS
def plot_analisis_1():
    try:
        sql_query = q.OCUPACION_REAL_CAMAS
        df = query_data(sql_query)
        
        df['fecha'] = pd.to_datetime(df['fecha'])

    except Exception as e:
        print(f"Error al cargar datos para Análisis 1: {e}")
        fig, ax = plt.subplots(figsize=(16, 8))
        ax.text(0.5, 0.5, 'Error al cargar datos desde BigQuery',
                ha='center', va='center', fontsize=14, color='red')
        ax.set_axis_off()
        return fig

    # Gráfico de líneas
    fig, ax = plt.subplots(figsize=(16, 8))
    
    sns.lineplot(
        data=df,
        x='fecha',
        y='camas_ocupadas', 
        ax=ax,
        color='coral' 
    )
    
    ax.set_title('Análisis #1: Ocupación Real de Camas por Día', fontsize=16)
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Número de Camas Ocupadas')
    ax.grid(True)
    
    return fig

def plot_analisis_2():
    try:
        sql_query = q.FLUJO_DEMANDA_DIARIA
        df = query_data(sql_query)
        
        df['fecha'] = pd.to_datetime(df['fecha'])
        
        # --- [NUEVO] CALCULAR PERCENTILES ---
        # 1. Replicamos la lógica del KPI: filtramos el "ruido" de 2023
        #    para obtener solo el rango operativo real.
        df_operativo = df[df['ingresos_diarios'] > 100] 
        
        # 2. Calculamos los percentiles 5 y 95 en Pandas
        p05 = df_operativo['ingresos_diarios'].quantile(0.05)
        p95 = df_operativo['ingresos_diarios'].quantile(0.95)
        # --- [FIN DEL CÓDIGO NUEVO] ---

    except Exception as e:
        print(f"Error al cargar datos para Análisis 2: {e}")
        # (Tu manejo de errores va aquí...)
        fig, ax = plt.subplots(figsize=(16, 8))
        ax.text(0.5, 0.5, 'Error al cargar datos desde BigQuery',
                ha='center', va='center', fontsize=14, color='red')
        ax.set_axis_off()
        return fig

    # --- Gráfico de líneas (igual que antes) ---
    fig, ax = plt.subplots(figsize=(16, 8))
    
    sns.lineplot(
        data=df,
        x='fecha',
        y='ingresos_diarios',   
        ax=ax,
        color='dodgerblue' 
    )
    
    # --- [NUEVO] AÑADIR LÍNEAS DE PERCENTIL ---
    # Añadimos las líneas horizontales (axhline)
    ax.axhline(
        p95, 
        color='firebrick',  # Un color que contraste
        linestyle='--', 
        linewidth=1.5,
        alpha=0.8
    )
    ax.axhline(
        p05, 
        color='firebrick', 
        linestyle='--', 
        linewidth=1.5,
        alpha=0.8
    )
    
    # --- [NUEVO] AÑADIR ETIQUETAS A LAS LÍNEAS ---
    # Colocamos las etiquetas al final del eje X para una UI limpia
    fecha_max_label = df['fecha'].max() 
    
    ax.text(fecha_max_label, p95, f'             ({p95:,.0f})', 
            color='firebrick', ha='left', va='center', fontsize=10, weight='bold')
            
    ax.text(fecha_max_label, p05, f'             ({p05:,.0f})', 
            color='firebrick', ha='left', va='center', fontsize=10, weight='bold')
    
    # --- Configuración del gráfico (igual que antes) ---
    ax.set_title('Análisis #2: Flujo de Nuevas Admisiones por Día', fontsize=16)
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Número de Pacientes Ingresados')
    ax.grid(True) # Mantenemos tu grid
    
    # Hacemos un pequeño margen a la derecha para que quepan las etiquetas
    ax.margins(x=0.05) 
    
    return fig

def plot_analisis_3():
    try:
        sql_query = q.CARGA_PACIENTES_NIVEL_ATENCION
        df = query_data(sql_query)
        
        print("Datos del Análisis 3 cargados:")
        print(df)

    except Exception as e:
        print(f"Error al cargar datos para Análisis 3: {e}")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, 'Error al cargar datos desde BigQuery',
                ha='center', va='center', fontsize=12, color='red')
        ax.set_axis_off()
        return fig

    # Grafico de barras
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sns.barplot(
        data=df,
        x='nivel_atencion',
        y='carga_promedio_por_nivel',
        palette=['purple', 'blue', 'grey'],
        alpha=0.8,
        ax=ax
    )
    
    ax.set_title('Carga Promedio de Pacientes Diarios por Nivel de Atención', fontsize=16)
    ax.set_xlabel('Nivel de Atención')
    ax.set_ylabel('Promedio de Ingresos Diarios')
    ax.tick_params(axis='x', rotation=0)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    return fig

def plot_analisis_4():
    try:
        sql_query = q.COMPOSICION_DEMANDA_POR_SERVICIO
        df = query_data(sql_query)
        
        df['week_date'] = pd.to_datetime(df['week_date'])
        
        df = df.set_index('week_date')
        df = df.sort_index()

    except Exception as e:
        print(f"Error al cargar datos para Análisis 4: {e}")
        fig, ax = plt.subplots(figsize=(16, 9))
        ax.text(0.5, 0.5, 'Error al cargar datos desde BigQuery',
                ha='center', va='center', fontsize=14, color='red')
        ax.set_axis_off()
        return fig

    # Gráfico 
    fig, ax = plt.subplots(figsize=(16, 9))
    
    df.plot(
        kind='area', 
        stacked=True, 
        ax=ax, 
        figsize=(16, 9),
        alpha=0.8
    )
    
    ax.set_title('Composición Semanal de la Demanda por Servicio', fontsize=16)
    ax.set_ylabel('Número de Ingresos Semanales')
    ax.set_xlabel('Fecha')
    ax.legend(title='Servicio Troncal', loc='upper left')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.set_ylim(bottom=0) 
    
    return fig

def plot_analisis_5():
    try:
        sql_query = q.PATRONES_TEMPORALES_DEMANDA
        df = query_data(sql_query)
        
        df['fecha'] = pd.to_datetime(df['fecha'])
        
        # Crear las columnas para graficar
        df['day_name'] = df['fecha'].dt.day_name()
        df['month_number'] = df['fecha'].dt.month

    except Exception as e:
        print(f"Error al cargar datos para Análisis 5: {e}")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
        ax1.text(0.5, 0.5, 'Error al cargar datos (Día)', ha='center', va='center', color='red')
        ax2.text(0.5, 0.5, 'Error al cargar datos (Mes)', ha='center', va='center', color='red')
        ax1.set_axis_off()
        ax2.set_axis_off()
        return fig

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
    
    # Ordenar los días de la semana
    dias_ordenados = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Gráfico 1: Día de la Semana
    sns.boxplot(
        data=df, 
        x='day_name',         
        y='ingresos_ese_dia', 
        ax=ax1, 
        order=dias_ordenados
    )
    ax1.set_title('Distribución de Ingresos por Día de la Semana', fontsize=14)
    ax1.set_xlabel('Día de la Semana')
    ax1.set_ylabel('Ingresos Diarios')
    ax1.tick_params(axis='x', rotation=45) # Rotamos un poco para que no se solapen

    # Gráfico 2: Mes del Año
    sns.boxplot(
        data=df, 
        x='month_number',     
        y='ingresos_ese_dia', 
        ax=ax2
    )
    ax2.set_title('Distribución de Ingresos por Mes', fontsize=14)
    ax2.set_xlabel('Mes del Año')
    ax2.set_ylabel('Ingresos Diarios')
    
    plt.tight_layout() 
    
    return fig
    return fig

def plot_analisis_6_contexto():
    try:
        sql_query = q.DURACION_ESTANCIA_POR_SERVICIO
        df = query_data(sql_query)
        
    except Exception as e:
        print(f"Error al cargar datos para Análisis 6 (Contexto): {e}")
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.text(0.5, 0.5, 'Error al cargar datos desde BigQuery',
                ha='center', va='center', fontsize=12, color='red')
        ax.set_axis_off()
        return fig

    # Gráfico Boxplot
    fig, ax = plt.subplots(figsize=(14, 8))
    
    sns.boxplot(
        data=df,
        x='duracion_estancia',
        y='servicio_troncal', 
        palette='plasma',
        ax=ax,
        fliersize=2
    )
    
    ax.set_title('Distribución de la Duración de Estancia por Servicio (Contexto)', fontsize=16)
    ax.set_xlabel('Días de Estancia')
    ax.set_ylabel('Servicio Troncal')
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    
    return fig

def plot_analisis_6_outliers():
    try:
        sql_query = q.DIAGNOSTICOS_OUTLIER_POR_SERVICIO
        df_outliers = query_data(sql_query)
        
        top_4_servicios = df_outliers['servicio_troncal'].unique()
        
        if len(top_4_servicios) > 4:
            top_4_servicios = top_4_servicios[:4]
            
    except Exception as e:
        print(f"Error al cargar datos para Análisis 6 (Outliers): {e}")
        fig, axes = plt.subplots(2, 2, figsize=(20, 16))
        for ax in axes.flatten():
            ax.text(0.5, 0.5, 'Error al cargar datos', ha='center', color='red')
            ax.set_axis_off()
        return fig

    fig, axes = plt.subplots(2, 2, figsize=(20, 16))
    axes = axes.flatten() # Convierte la cuadrícula 2x2 en una lista de 4 ejes
    
    colors = ['firebrick', 'darkorange', 'darkgoldenrod', 'darkgreen']

    # Iterar y graficar
    for i, servicio in enumerate(top_4_servicios):
        ax = axes[i]
        
        df_servicio = df_outliers[df_outliers['servicio_troncal'] == servicio]
        
        # Graficar
        sns.barplot(
            data=df_servicio,
            x='conteo_casos_outlier',
            y='descripcion_diagnostico',
            ax=ax,
            color=colors[i % len(colors)],
            alpha=0.8
        )
        
        ax.set_title(f'Diagnósticos Outlier en "{servicio}"', fontsize=14)
        ax.set_xlabel('Número de Casos de Larga Estancia')
        ax.set_ylabel('')
        ax.invert_yaxis()
        
 
    for j in range(i + 1, len(axes)):
        axes[j].set_axis_off()

    plt.tight_layout(pad=3.0)
    return fig
    
def plot_analisis_7():
    try:
        sql_query = q.DISTRIBUCION_GEOGRAFICA_DEMANDA_HOSPITALARIA
        df_mapa_filtrado = query_data(sql_query)
        
        # Cargar los mapas cacheados
        north_america_map = get_world_map()
        mexico_states_map = get_mexico_states_map()
        
    except Exception as e:
        print(f"Error al cargar datos para Análisis 7: {e}")
        fig, ax = plt.subplots(figsize=(18, 12))
        ax.text(0.5, 0.5, f'Error al cargar datos geo:\n{e}',
                ha='center', va='center', fontsize=12, color='red')
        ax.set_axis_off()
        return fig

    # Gráfico
    fig, ax = plt.subplots(figsize=(18, 12))

    # Fondo: países de Norteamérica 
    north_america_map.plot(
        ax=ax, color='lightgrey', edgecolor='black', linewidth=0.5
    )

    # SUPERPONER FRONTERAS DE ESTADOS DE MÉXICO
    mexico_states_map.plot(
        ax=ax,
        facecolor='none',
        edgecolor='#555588',
        linewidth=0.9,
        alpha=0.7
    )
    
    # AGREGAR ETIQUETAS DE ESTADOS
    estados_a_mostrar = [
    'México', 'Jalisco', 'Nuevo León', 'Veracruz', 'Puebla',
    'Guanajuato', 'Michoacán', 'Chiapas', 'Sonora', 'Baja California',
    'Quintana Roo', 'Yucatán', 'Tabasco', 'Campeche', 'Oaxaca','Chihuahua', 'Tamaulipas'
    ]

    for idx, row in mexico_states_map.iterrows():
        if row['name'] not in estados_a_mostrar:
            continue

        centroid = row.geometry.centroid
        x, y = centroid.x, centroid.y
    
        if not (-118 < x < -82 and 16 < y < 32):
            continue
        
        nombre = row['name']
    
        ax.text(
            x, y, nombre,
            fontsize=6,
            ha='center', va='center',
            color='black',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.7, edgecolor='none'),
            zorder=10
        )

    # Recortar al área de interés (México)
    ax.set_xlim((-120, -80))
    ax.set_ylim((14, 34))

    # Graficar los puntos
    sns.scatterplot(
        data=df_mapa_filtrado,
        x='lon_decimal',
        y='lat_decimal',
        size='total_ingresos',
        sizes=(50, 1500),
        alpha=0.7,
        hue='nombre_entidad',
        palette='tab20',
        ax=ax,
        legend=False
    )

    # Leyenda Manual: Tamaño (Total de Ingresos)
    size_legend_values = [100, 1000, 5000, 10000]
    size_legend_marker_sizes = [100, 180, 260, 340]

    size_handles_manual = []
    for s_val, s_marker in zip(size_legend_values, size_legend_marker_sizes):
        size_handles_manual.append(
            Line2D([0], [0], marker='o', color='gray',
                   markersize=s_marker / 15,
                   label=f'{s_val:,.0f}',
                   linestyle='None')
        )

    legend_tamano = ax.legend(
        handles=size_handles_manual,
        title='Total de Ingresos',
        bbox_to_anchor=(1.02, 0.70),
        loc='upper left',
        frameon=False,
        fontsize='medium',
        labelspacing=1.5
    )
    ax.add_artist(legend_tamano)

    # Leyenda Manual: Entidad
    unique_entidades = df_mapa_filtrado.drop_duplicates(subset=['nombre_entidad'])
    
    colors = sns.color_palette('tab20', n_colors=len(unique_entidades))
    hue_handles = [
        Line2D([0], [0], marker='o', color='w', 
               markerfacecolor=color, markersize=12, label=entidad)
        for color, entidad in zip(colors, unique_entidades['nombre_entidad'])
    ]
    
    ax.legend(
        handles=hue_handles,
        title='Entidad (Top 5)',
        bbox_to_anchor=(1.02, 1.0),
        loc='upper left',
        frameon=False
    )

    ax.set_title('Distribución Geográfica de la Demanda Hospitalaria por Entidad', fontsize=18)
    ax.axis('off')
    fig.tight_layout(rect=(0, 0, 0.82, 1)) 

    return fig