import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd

from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt


st.set_page_config(layout="wide")

#carga de datos
@st.cache_data
def load_data(file, sheet_name):
    return pd.read_excel(file, sheet_name=sheet_name)

aire = load_data("fin.xlsx", sheet_name="aire")
asma = load_data("fin.xlsx", sheet_name="asma")
cancer = load_data("fin.xlsx", sheet_name="cancer")

#carga del mapa
us_states = gpd.read_file('tl_2023_us_state/tl_2023_us_state.shp')
st.title("Visualización a través de Mapas")

#seleccion
parametro = st.selectbox("Selecciona el parámetro a visualizar", ["aire", "asma", "cancer"])
medio = st.checkbox("Mostar el valor medio por año", value=False)
año = st.selectbox("Si no se aplica la media seleccione el año a visualizar", [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020])

#valor medio
if medio:
    if parametro == "aire":
        
        data_grouped = aire.groupby('State')['DataValue'].mean().reset_index()
        merged = us_states.merge(data_grouped, left_on='NAME', right_on='State', how='left')

        fig1, ax = plt.subplots(1, 1, figsize=(15, 15))
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.1)
        
        us_states.boundary.plot(ax=ax, color='black', linewidth=0.5)

        merged.plot(column="DataValue", ax=ax, legend=True, cax=cax,
                    legend_kwds={'label': "Concentración de PM2.5", 'orientation': "vertical"},
                    missing_kwds={"color": "white", "edgecolor": "lightgrey", "hatch": "/ /", "label": "Missing values"})
        ax.set_xlim(-130, -65)
        ax.set_ylim(24, 50)

        ax.set_title('Valores Medios de concentración de PM2.5 por estado en 2001-2020')
        ax.set_facecolor('lightblue')

        st.pyplot(fig1)
    elif parametro == "asma":
        
        data_grouped = asma.groupby('State')['DataValue'].sum().reset_index()
        merged = us_states.merge(data_grouped, left_on='NAME', right_on='State', how='left')

        fig1, ax = plt.subplots(1, 1, figsize=(15, 15))
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.1)
        
        us_states.boundary.plot(ax=ax, color='black', linewidth=0.5)

        merged.plot(column="DataValue", ax=ax, legend=True, cax=cax,
                    legend_kwds={'label': "visitas a emergencia por asmisitas a emergencia por asm", 'orientation': "vertical"},
                    missing_kwds={"color": "white", "edgecolor": "lightgrey", "hatch": "/ /", "label": "Missing values"})
        ax.set_xlim(-130, -65)
        ax.set_ylim(24, 50)

        ax.set_title('Valores Medios de visitas a emergencia por asma por estado en 2001-2020')
        ax.set_facecolor('lightblue')

        st.pyplot(fig1)
    else:
        
        data_grouped = cancer.groupby('State')['DataValue'].sum().reset_index()
        merged = us_states.merge(data_grouped, left_on='NAME', right_on='State', how='left')

        fig1, ax = plt.subplots(1, 1, figsize=(15, 15))
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.1)
        
        us_states.boundary.plot(ax=ax, color='black', linewidth=0.5)

        merged.plot(column="DataValue", ax=ax, legend=True, cax=cax,
                    legend_kwds={'label': "Casos de cáncer", 'orientation': "vertical"},
                    missing_kwds={"color": "white", "edgecolor": "lightgrey", "hatch": "/ /", "label": "Missing values"})
        ax.set_xlim(-130, -65)
        ax.set_ylim(24, 50)

        ax.set_title('Valores Medios de casos de cáncer por estado en 2001-2020')
        ax.set_facecolor('lightblue')

        st.pyplot(fig1)
#por año
else:
    if parametro == "aire":

        year_to_plot = año
        data_for_year = aire[aire['Year'] == year_to_plot]

        merged = us_states.merge(data_for_year, left_on='NAME', right_on='State', how='left')

        fig1, ax = plt.subplots(1, 1, figsize=(15, 15))
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.1)

        us_states.boundary.plot(ax=ax, color='black', linewidth=0.5)

        merged.plot(column="DataValue", ax=ax, legend=True, cax=cax,
                    legend_kwds={'label': "Concentración de PM2.5", 'orientation': "vertical"},
                    missing_kwds={"color": "white", "edgecolor": "lightgrey", "hatch": "/ /", "label": "Missing values"})
        ax.set_xlim(-130, -65)
        ax.set_ylim(24, 50)

        ax.set_title(f'Valores de concentración de PM2.5 por estado en {year_to_plot}')
        ax.set_facecolor('lightblue')

        st.pyplot(fig1)

    elif parametro == "asma":
        year_to_plot = año
        data_for_year = asma[asma['Year'] == year_to_plot]

        merged = us_states.merge(data_for_year, left_on='NAME', right_on='State', how='left')

        fig1, ax = plt.subplots(1, 1, figsize=(15, 15))
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.1)

        us_states.boundary.plot(ax=ax, color='black', linewidth=0.5)

        merged.plot(column="DataValue", ax=ax, legend=True, cax=cax,
                    legend_kwds={'label': "Visitas a emergencia por asma", 'orientation': "vertical"},
                    missing_kwds={"color": "white", "edgecolor": "lightgrey", "hatch": "/ /", "label": "Missing values"})
        ax.set_xlim(-130, -65)
        ax.set_ylim(24, 50)

        ax.set_title(f'Valores de visitas a emergencia por asma por estado en {year_to_plot}')
        ax.set_facecolor('lightblue')

        st.pyplot(fig1)
    else:
        
        year_to_plot = año
        data_for_year = cancer[cancer['Year'] == year_to_plot]

        merged = us_states.merge(data_for_year, left_on='NAME', right_on='State', how='left')

        fig1, ax = plt.subplots(1, 1, figsize=(15, 15))
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.1)

        us_states.boundary.plot(ax=ax, color='black', linewidth=0.5)

        merged.plot(column="DataValue", ax=ax, legend=True, cax=cax,
                    legend_kwds={'label': "Casos de cáncer", 'orientation': "vertical"},
                    missing_kwds={"color": "white", "edgecolor": "lightgrey", "hatch": "/ /", "label": "Missing values"})
        ax.set_xlim(-130, -65)
        ax.set_ylim(24, 50)

        ax.set_title(f'Valores de casos de cáncer por estado en {year_to_plot}')
        ax.set_facecolor('lightblue')

        st.pyplot(fig1)
