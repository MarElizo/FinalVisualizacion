import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

st.set_page_config(layout="wide")
@st.cache_data
def load_data(file, sheet_name):
    return pd.read_excel(file, sheet_name=sheet_name)

# cargar datos
aire = load_data("fin.xlsx", sheet_name="aire")
asma = load_data("fin.xlsx", sheet_name="asma")
cancer = load_data("fin.xlsx", sheet_name="cancer")
aire_2 = pd.read_excel("fin2.xlsx", sheet_name="calidad_asma")
aire_3 = pd.read_excel("fin2.xlsx", sheet_name="calidad_cancer")

st.title("Visualización a través de Gráficos")

st.write("## Estudio general de los datos")

sns.set_style("whitegrid")
asma_sum = asma.groupby('Year')['DataValue'].sum()
cancer_sum = cancer.groupby('Year')['DataValue'].sum()
aire_avg = aire.groupby('Year')['DataValue'].mean()
asma_sum.index = asma_sum.index.astype(int)
cancer_sum.index = cancer_sum.index.astype(int)
fig_gen, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

ax1.plot(asma_sum.index.astype(int), asma_sum.values, color='blue', marker='o', label='Asma')
ax1.plot(cancer_sum.index.astype(int), cancer_sum.values, color='orange', marker='o', label='Cáncer')
ax2.plot(aire_avg.index.astype(int), aire_avg.values, color='green', marker='o', label='Aire')

ax1.set_xticks(asma_sum.index[::1])
ax2.set_xticks(aire_avg.index[::1])

ax1.set_title("Evolución por año de: casos de cáncer, visitas a emergencia por asma y concentración de PM2.5")
ax2.set_xlabel('Año')
ax1.set_ylabel('Número de personas')
ax2.set_ylabel('Concentración de PM2.5')

ax1.legend()
ax2.legend()

plt.tight_layout()

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.pyplot(fig_gen)

st.subheader("Distribución de los datos")


fig_box, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

sns.boxplot(x='Year', y='DataValue', data=cancer, ax=axes[0])
axes[0].set_title('Casos de cáncer por año')
axes[0].set_xlabel('Año')
axes[0].set_ylabel('Número de casos')
plt.setp(axes[0].xaxis.get_majorticklabels(), rotation=45)

sns.boxplot(x='Year', y='DataValue', data=asma, ax=axes[1])
axes[1].set_title('Visitas a emergencia por asma por año')
axes[1].set_xlabel('Año')
axes[1].set_ylabel('Visitas a emergencia')
plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=45)

sns.boxplot(x='Year', y='DataValue', data=aire, ax=axes[2])
axes[2].set_title('Concentración de PM2.5 por año')
axes[2].set_xlabel('Año')
axes[2].set_ylabel('Concentración de PM2.5')
plt.setp(axes[2].xaxis.get_majorticklabels(), rotation=45)


plt.tight_layout()

st.pyplot(fig_box)


fig_kde, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 4))

sns.kdeplot(x='Year', y='DataValue', data=cancer, ax=axes[0], cmap='Oranges')
axes[0].set_title('Distribución de casos de cáncer')
axes[0].set_xlabel('Año')
axes[0].set_ylabel('Número de casos')


sns.kdeplot(x='Year', y='DataValue', data=asma, ax=axes[1], cmap='Blues')
axes[1].set_title('Distribución de visitas a emergencia por asma')
axes[1].set_xlabel('Año')
axes[1].set_ylabel('Visitas a emergencia')


sns.kdeplot(x='Year', y='DataValue', data=aire, ax=axes[2], cmap='Greens')
axes[2].set_title('Distribución de concentración de PM2.5')
axes[2].set_xlabel('Año')
axes[2].set_ylabel('Concentración de PM2.5')


plt.tight_layout()
st.pyplot(fig_kde)


st.write("## Estudio sobre asma")


data = pd.merge(aire_2, asma, on=['Year', 'State'], how='outer')

g_as = sns.jointplot(x="DataValue", y='DataValue2', data=data, hue='State', palette='husl')
g_as.ax_joint.legend(title='Estados')
g_as.fig.suptitle('Relación entre visitas a emergencia por asma y concentración de PM2.5', y=1.03)
g_as.set_axis_labels('Visitas a emergencia', 'Concentración PM2.5')


plt.tight_layout()

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.pyplot(g_as)
    
st.subheader("Estudio personalizado")


# seleccionar estados

select1_key = "select1"
select2_key = "select2"

asma_cleaned = asma.drop_duplicates(['Year', 'State'])
pivot_df = asma_cleaned.pivot(index='Year', columns='State', values='DataValue')

colormap = plt.get_cmap("tab20")
num_colors = len(pivot_df.columns)
colores = colormap.colors[:num_colors]

all_states = pivot_df.columns.tolist()
all_states.insert(0, "Seleccionar todo")

selected_states1 = st.multiselect("Selecciona los estados a incluir en la visualización:", all_states, default=[], key="select1_key")

if "Seleccionar todo" in selected_states1:
    selected_states1 = all_states[1:]  
sns.set_style("whitegrid")
fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12), sharex=True)

for estado in selected_states1:
    data_estado = asma[asma['State'] == estado].sort_values('Year')
    ax1.plot(data_estado['Year'], data_estado['DataValue'], marker="o", label=estado)

for estado in selected_states1:
    data_estado = aire[aire['State'] == estado].sort_values('Year')
    ax2.plot(data_estado['Year'], data_estado['DataValue'], marker="o", label=estado)

if not selected_states1:
    ax1.text(0.5, 0.5, 'Selecciona estados para visualizar los datos', ha='center', va='center', fontsize=20, transform=ax1.transAxes)
    ax2.text(0.5, 0.5, 'Selecciona estados para visualizar los datos', ha='center', va='center', fontsize=20, transform=ax2.transAxes)

ax1.set_xticks(asma['Year'].unique())
ax2.set_xticks(aire['Year'].unique())

ax1.set_title("Evolución de visitas a emergencia por asma y de concentración de PM2.5",  fontsize=22)
ax2.set_xlabel('Año',  fontsize=20)
ax1.set_ylabel('Visitas a emergencia',  fontsize=20)
ax2.set_ylabel('Concentración de PM2.5',  fontsize=20)

ax1.legend()
ax2.legend()

plt.tight_layout()

#barras
fig2, ax = plt.subplots(figsize=(14, 12))

filtered_pivot_df = pivot_df[selected_states1] if selected_states1 else pivot_df[[]]

if not filtered_pivot_df.empty:
    filtered_pivot_df.plot(kind='bar', stacked=True, color=colores[:len(selected_states1)], width=0.8, legend=len(selected_states1) <= 10, ax=ax)
    ax.set_ylim(0, filtered_pivot_df.sum(axis=1).max())
else:
    ax.text(0.5, 0.5, 'Selecciona estados para visualizar los datos', ha='center', va='center', fontsize=20)
    ax.set_xlim(-0.5, 0.5)
    ax.set_ylim(0, 1)

plt.title('Visitas a emergencia por asma por año diferenciando por estados', fontsize=22)
plt.xlabel('Año',  fontsize=20)
plt.ylabel('Visitas a emergencia',  fontsize=20)

plt.tight_layout()
col1, col2 = st.columns([1, 1])
with col1:
    st.pyplot(fig1)
with col2:
    st.pyplot(fig2)



st.write("## Estudio sobre cáncer")



data = pd.merge(aire_3, cancer, on=['Year', 'State'], how='outer')

g_c=sns.jointplot(x="DataValue", y='DataValue2', data=data, hue='State', palette='husl', legend=False)
g_c.fig.suptitle('Relación entre casos de cáncer y concentración de PM2.5')
g_c.set_axis_labels('Número de casos', 'Concentración PM2.5')


plt.tight_layout()

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.pyplot(g_c)


st.subheader("Estudio personalizado")

cancer_cleaned = cancer.drop_duplicates(['Year', 'State'])
pivot_df = cancer_cleaned.pivot(index='Year', columns='State', values='DataValue')

colormap = plt.get_cmap("tab20")
num_colors = len(pivot_df.columns)
colores = colormap.colors[:num_colors]
# seleccionar estados
all_states = pivot_df.columns.tolist()
all_states.insert(0, "Seleccionar todo")

selected_states2 = st.multiselect("Selecciona los estados a incluir en la visualización:", all_states, default=[],key=select2_key)


if "Seleccionar todo" in selected_states2:
    selected_states2 = all_states[1:]  


sns.set_style("whitegrid")

fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12), sharex=True)

for estado in selected_states2:
    data_estado = cancer[cancer['State'] == estado].sort_values('Year')
    ax1.plot(data_estado['Year'], data_estado['DataValue'], marker="o", label=estado)

for estado in selected_states2:
    data_estado = aire[aire['State'] == estado].sort_values('Year')
    ax2.plot(data_estado['Year'], data_estado['DataValue'], marker="o", label=estado)

if not selected_states2:
    ax1.text(0.5, 0.5, 'Selecciona estados para visualizar los datos', ha='center', va='center', fontsize=20, transform=ax1.transAxes)
    ax2.text(0.5, 0.5, 'Selecciona estados para visualizar los datos', ha='center', va='center', fontsize=20, transform=ax2.transAxes)

ax1.set_xticks(cancer['Year'].unique())
ax2.set_xticks(aire['Year'].unique())

ax1.set_title("Evolución de casos de cáncer y de concentración de PM2.5",  fontsize=22)
ax2.set_xlabel('Año', fontsize=20)
ax1.set_ylabel('Número de casos', fontsize=20)
ax2.set_ylabel('Concentración de PM2.5',  fontsize=20)
if len(selected_states2) <= 10:
    ax1.legend()
    ax2.legend()

plt.tight_layout()

# grafico de barras
fig2, ax = plt.subplots(figsize=(14, 12))

filtered_pivot_df = pivot_df[selected_states2] if selected_states2 else pivot_df[[]]

if not filtered_pivot_df.empty:
    filtered_pivot_df.plot(kind='bar', stacked=True, color=colores[:len(selected_states2)], width=0.8, legend=len(selected_states2) <= 10, ax=ax)
    ax.set_ylim(0, filtered_pivot_df.sum(axis=1).max())
else:
    ax.text(0.5, 0.5, 'Selecciona estados para visualizar los datos', ha='center', va='center', fontsize=20)
    ax.set_xlim(-0.5, 0.5)
    ax.set_ylim(0, 1)


plt.title('Casos de cáncer por año diferenciando por estados', fontsize=22)
plt.xlabel('Año',  fontsize=20)
plt.ylabel('Número de casos',  fontsize=20)

plt.tight_layout()

col1, col2 = st.columns([1, 1])
with col1:
    st.pyplot(fig1)
with col2:
    st.pyplot(fig2)

