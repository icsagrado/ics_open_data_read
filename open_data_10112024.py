
# coding: utf-8

# ### CNMC OPEN DATA. Example of use:  'bono social' dataset
# #### CNMC API|Data https://data.cnmc.es/
# 
#     El Portal de datos abiertos CNMC|Data proporciona el punto de partida centralizado de datos sobre mercados en formatos abiertos y reutilizables que se ponen a disposición pública para que puedan ser utilizados y redistribuidos libremente de acuerdo con las condiciones de uso.
# 
#     La Comisión Nacional de los Mercados y la Competencia opta por la modalidad de puesta a disposición de los datos con sujeción a condiciones establecidas según la licencia de Creative Commons Atribución – Compartir-Igual (CC BY-SA 4.0)1.licencias-tipo (artículo 8.2 del Real Decreto 1495/2011, de 24 de octubre).
#     
# Origen de los datos: Comisión Nacional de los Mercados y la Competencia
# 
# Estadística bono social Última actualización: 18 Sep 2024 
# https://data.cnmc.es/energia/energia-electrica/bono-social

# In[1]:


import requests


# In[2]:


# CNMC API URL: catalog
url = "https://catalogodatos.cnmc.es/api/3/action/package_search"

# resquest
try:
    response = requests.get(url)# Obtención de los resultados

    # status
    if response.status_code == 200:
        data = response.json()  # Convierte la respuesta a JSON
        print("Data successfully obtained:")
        print(data)  # Muestra los datos
    else:
        print(f"Error in request: {response.status_code} - {response.text}")

except Exception as e:
    print(f"An error occurred: {e}")


# In[3]:


# catalog info
# data['result']
data['result'].keys()
# available number of datasets
data['result']['count']


# ## 'bono social' dataset

# In[4]:


bono_social ="Estadística bono social"
url = 'https://catalogodatos.cnmc.es/api/3/action/package_search?q=' + bono_social

header = {"User-Agent": "Application"}   
r = requests.get(url, headers=header)

# get dataset identifier
bono_social = r.json()
id_resource = bono_social['result']['results'][0]['resources'][0]['id'];
print(f"Dataset identifier: {id_resource}")


# In[ ]:


# LLamada API para obtener todos los datos del recurso del dataset
url = 'https://catalogodatos.cnmc.es/api/3/action/datastore_search?' +    'limit=32000&' +    'resource_id='+ id_resource
r = requests.get(url, headers=header)
bono_social_dataset = r.json()['result']['records']
print(f"Los datos del dataset son: {bono_social_dataset}")


# In[ ]:


#bono_social_dataset
bono_social_dataset[0].keys()


# ## Analysis

# In[ ]:


import json
import pandas as pd


# In[ ]:


import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
sns.set(color_codes=True)
sns.set(font_scale = 1.5)
sns.set_style("darkgrid")


# In[ ]:


json_string = json.dumps(bono_social_dataset) # Convert dictionary to JSON string
df = pd.read_json(json_string) # Convert JSON string to Pandas DataFrame


# In[ ]:


# explore dataset
df.describe
#df.head()
#df.info()
#df.columns


# In[ ]:


# get year and month from mes_consumo
df['anio']=df['mes_consumo'].str.slice(stop=4)
# get mes from mes_consumo
df['mes']=df['mes_consumo'].str.slice(start=5, stop=7)


# In[ ]:


# explore
df['anio'].unique()
#df['mes']


# In[ ]:


# explore
df['denominacion_por_categorias_de_beneficiarios_de_bono_social'].unique()


# In[ ]:


# Rename columns to make analysis easier
df.rename(columns={"denominacion_por_categorias_de_beneficiarios_de_bono_social": "tipo_beneficiario"},inplace=True)


# In[ ]:


df.head()


# ### Evolución del número de usuarios acogidos a bono social

# In[ ]:


# annual evolution of the monthly average
df_anio=df[(df.tipo_beneficiario=='Total')].groupby(['anio']).mean()
df_anio.drop(['_id'],axis=1,inplace=True)
df_anio


# #### Historical series plot

# In[ ]:


df_plot=df_anio

fig1, ax = plt.subplots(figsize=(10,7))
ax=sns.barplot(data=df_plot, y=df_plot['numero_clientes'],x=df_plot.index, color='b',orient='v')

pos_y=0
pos_x=0
for a in df_plot['numero_clientes']:
    color='white'           
    ax.text(pos_x,a-a*0.2, str(round(a/1E6,2))+'\nMillones', color=color,size='16', ha="center",fontweight='bold')   
    pos_x=pos_x+1    

#ax.set(ylabel='VI declarado (M€)')
ax.set(ylabel=None)
ax.set(yticks=[])
ax.set(xlabel='Año')
  
ax.set(title='Evolución del número de usuarios acogidos a bono social\n(promedio mensual para cada año)')
plt.savefig("bono_social.png", bbox_inches='tight')
plt.show()


# ### Analysis by categories

# In[ ]:


# Analysis of the different types of beneficiaries
df_cat=df[['numero_clientes','anio','mes','tipo_beneficiario']][df['tipo_beneficiario']!='Total'].groupby(['anio','mes','tipo_beneficiario']).mean()
df_cat.reset_index(inplace=True)
df_cat


# In[ ]:


# 2023
df_cat_2023=df_cat[df_cat.anio=='2023']
# vulnerable/severely vulnerable disaggregation
df_cat_2023['categoria']=df_cat_2023['tipo_beneficiario'].str.slice(stop=2) # 
df_cat_2023[['mes','categoria','tipo_beneficiario']].groupby(['mes','categoria']).count()


# In[ ]:


# explore
df_cat_2023[df_cat_2023.categoria=='V '].groupby('mes').count()
mes=df_cat_2023['mes'].unique()
#print (mes)
for m in mes:
    cat=df_cat_2023['tipo_beneficiario'][df_cat_2023.mes==m].unique()
    print(m, len(cat) )
for c in cat:
    print (c)


# In[ ]:


# explore
tipo_ben_01=df_cat_2023['tipo_beneficiario'][df_cat_2023.mes=='01']
tipo_ben_12=df_cat_2023['tipo_beneficiario'][df_cat_2023.mes=='12']

# Convert lists to sets
set1 = set(tipo_ben_01)
set2 = set(tipo_ben_12)

# Intersection (common elements)
intersection = set1 & set2
#print(len(intersection),list(intersection))  

# Union (all unique elements)
union = set1 | set2
#print(len(union),list(union))  

# Difference (elements in set1 not in set2)
difference = set1 - set2
print(list(difference))  # Output: [1, 2]
df_cat_2023[df_cat_2023.tipo_beneficiario=='V Desempleados y ERTE'].groupby('mes').sum()


# In[ ]:


df_cat_2023[df_cat_2023.tipo_beneficiario=='V Desempleados y ERTE']


# In[ ]:


df_cat_2023.groupby(['categoria','mes']).sum()


# In[ ]:


df_cat_2023.groupby(['mes']).sum()/1000000


# In[ ]:


df_cat_2023.groupby(['categoria']).mean()


# ### plot by categories in the last available month: June 2024

# In[ ]:


df_cat_2023[['numero_clientes','categoria', 'tipo_beneficiario']][df_cat_2023.mes=='06'].groupby(['categoria','tipo_beneficiario']).sum()


# In[ ]:


df_plot=df_cat_2023[['numero_clientes','categoria']][df_cat_2023.mes=='06'].groupby('categoria').sum()
df_plot


# #### Plot 

# In[ ]:


fig, ax = plt.subplots(figsize=(12, 8))
plt.pie(df_plot,labels=['Vulnerable','Vulnerable\nSevero'],
        autopct='%.0f%%',pctdistance=0.8,labeldistance=1.21,
        startangle=-90,textprops=dict(color="k",ha='center',size='14',fontweight='bold'))#horizontalalignment='right'
# donut plot
my_circle=plt.Circle( (0,0), 0.5, color='white')
p=plt.gcf()
p.gca().add_artist(my_circle)

total=df_plot['numero_clientes'].sum()
ax.text(0,0.,''+str('{:.2f}'.format(total/1E6))+ ' Millones', color='k',size='18', ha="center",fontweight='bold')
ax.set(title='Usuarios acogidos a bono social en junio de 2024')
plt.savefig("bono_social_cat_junio_2024.png", bbox_inches='tight')
plt.show()

