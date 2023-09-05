#!pip install geopandas -q
#!pip install pandas -q
#!pip install matplotlib -q              #permite personalizar opões de design
#!pip install matplotlib.scalebar -q     #módulo da matplot específico para escala
#!pip install contextily -q              #Importação de mapa base externo
#!pip install mapclassify -q

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
from mpl_toolkits.axes_grid1 import make_axes_locatable #da escala
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, TransformedBbox #da escala
from matplotlib_scalebar.scalebar import ScaleBar #da escala
from sqlalchemy import true                         #
from pandas.core.reshape.tile import Categorical    #categorização ao inves de classificação

## caso ambiente seja colab, conecta este ambiente automaticamente com a conta do google (deve ter login da Polo@gmail para funcionar)
#from google.colab import drive
#drive.mount('/content/drive')

#selecionando a cidade e parâmetro desejado
idade = "Marituba"          #coloque com acento se houver, não esqueça das aspas
parametro_censo = "densidade habitacional"

cidade = cidade.title()                             #transforma em letras maiusculas as primeiras das palavras
parametro_censo = parametro_censo.upper()           #transforma em letras maiusculas

#tabela rascunho interna para verificação do estado ao qual a cidade pertence
tabela1 = pd.read_csv('/content/drive/MyDrive/Tabelas/Estados.csv', sep=",", decimal=".", encoding="UTF-8")
cid_estado = tabela1[tabela1.NM_MUN == cidade]
cid_estado = cid_estado[["SIGLA_UF"]]

indice_resetado = cid_estado.reset_index()         #como a tabela é grande, após encontrar, precisa-se resetar a fim de se pegar o registro com nome da cidade que agora sempre estara no [0]
estado = indice_resetado.loc[0, 'SIGLA_UF']  #caso o nome da cidade seja compartilhado por outra em outro estado trocar o número 0 por 1 ou 2, ou 3....

#Se o Estado for SP verificar aqui se é da RMSP

caminho_cidades = "/content/drive/MyDrive/Camadas/" + estado + "_mun.shp"
caminho_setores = "/content/drive/MyDrive/Camadas/" + estado + "_setores.shp"
caminho_tabela_setores = "/content/drive/MyDrive/Tabelas/" + estado + "_tab_setores.csv"
caminho_tabela_raca = "/content/drive/MyDrive/Tabelas/Pessoa03_" + estado + ".csv"

shape_estado_mun = gpd.read_file(caminho_cidades)
shape_setores = gpd.read_file(caminho_setores)
tabela_setores = pd.read_csv(caminho_tabela_setores, sep=";", decimal=",", encoding="UTF-8")
tabela_raca = pd.read_csv(caminho_tabela_raca, sep=";", decimal=",", encoding="UTF-8")

#adequação ao crs correto das camadas obtidas
shape_estado_mun =shape_estado_mun.to_crs(epsg=31983)
shape_setores = shape_setores.to_crs(epsg=31983)

#camadas base comuns a todos os mapas independente da cidade
oceano =gpd.read_file('/content/drive/MyDrive/Camadas/Fundo_oceano.shp')
oceano=oceano.to_crs(epsg=31983)
br=gpd.read_file('/content/drive/MyDrive/Camadas/BRUFE250GC_SIR.shp')
br=br.to_crs(epsg=31983)

#importação e transformação do csv no formato padrão para fazer a união de tabelas
tabela_setores = tabela_setores[["Cod_setor", "V001","V002","V005"]]
tabela_setores['dens_hab'] = tabela_setores['V002'] / tabela_setores['V001']

#construindo situação Rural ou Urbana

tabela_setores['Situacao_urb'] = ''
#tabela_setores.insert(column= "Situacao_urb")

# Classificando entre rural e urbano
for i, row in tabela_setores.iterrows():
    if row['Situacao_setor'] < 4:
      tabela_setores.loc[i,'Situacao_urb'] = "Urbano"
    else:
      tabela_setores.loc[i,'Situacao_urb'] = "Rural"


#verificação do tipo da variável 
tabela_setores.Cod_setor.dtype
shape_setores.CD_GEOCODI.dtype

#tranformação da coluna do shape setores que contem os codigos unitários para números inteiros
shape_setores.CD_GEOCODI= shape_setores.CD_GEOCODI.astype(int)
#mescla da tabela com shape
dados= shape_setores.merge(tabela_setores, left_on="CD_GEOCODI", right_on="Cod_setor")

#definição de variáveis em acordo com tipo de MAPA pretendido
if parametro_censo == "RENDA":
    variavel_censo = "V005"
    titulo_mapa = "Rendimento Nominal\médio mensal"
    cor_mapa = "Greens"
elif parametro_censo == "DENSIDADE HABITACIONAL":
    variavel_censo = "dens_hab"
    titulo_mapa = "Densidade Habitacional"
    cor_mapa = "Oranges"
elif parametro_censo == "RAÇA":
    variavel_censo = "dens_hab"
    titulo_mapa = "Densidade Habitacional"
    cor_mapa = "Oranges"
elif parametro_censo == "SITUAÇÃO URBANA":
    variavel_censo = "Situacao_urb"
    titulo_mapa = "Situação Urbana"
    cor_mapa = "Wistia"
else:
    print("Variavel não válida ou ainda não atendida.")



##tentativa mudança de fonte, não funcionou no ambiente colab
#matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
#plt.rcParams['font.family']
#matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')

#font_dirs = ['/content/drive/MyDrive/Fonte/']
#font_files = font_manager.findSystemFonts (fontpaths = font_dirs)

#for font_file in font_files:
#    font_manager.fontManager.addfont(font_file)

## set font
#plt.rcParams['font.family'] = 'Jost-Regular'


#Plotagem do mapa
cidade2 = cidade.upper()   ###########consertar
cidade1 = cidade.title()

fig,ax = plt.subplots()    #cria uma plotagem

lim_ext = shape_estado_mun[shape_estado_mun.NM_MUN == cidade1]              #coloca um fundo branco no município
lim_ext.plot(zorder=3, color= 'white', ax=ax)  #define a ordem e carcteristicas desse fundo
cidade_setores= dados[dados.NM_MUNICIP == cidade2]          #seleciona todos os setores censitários que têm essa cidade no nome

if titulo_mapa == "Situação Urbana": #mapa categorizado
    cidade_setores.plot(zorder=4,column= variavel_censo, ax=ax, categorical=True, cmap= cor_mapa, alpha=0.6 , edgecolor='white', linewidth=0.1, legend=True, legend_kwds={
        'loc': "lower right",
        "title": titulo_mapa,
        "fontsize":"xx-small",
        "labelcolor":'#4d4d4d',
        "title_fontsize": "x-small"
        })
else: #mapa classificado
    cidade_setores.plot(zorder=4,column= variavel_censo, ax=ax, scheme="natural_breaks", k=5, cmap= cor_mapa, alpha=0.8 , edgecolor='white', linewidth=0.1, legend=True, legend_kwds={
          'loc': "lower right",
          "title": titulo_mapa,
          "fontsize":"xx-small",
          "labelcolor":'#4d4d4d',
          "title_fontsize": "x-small"
          })

    #column é a coluna selecionada da tabela (no caso, renda)
    #ax=ax é a posição do plot (preciso entender melhor)
    #scheme é a simbologia por categorização (quantiles, equal_interval, natural_breaks)
    #k é o número de classes da categorização
    #cmap é a definição das cores do mapa. (https://matplotlib.org/stable/gallery/index.html#color)
    #edgecolor é definição de cor da borda das feições. Para retirar as bordas, usar edgecolor='nome'
    #legend é a opção para inserir ou não a legenda

ax = oceano.plot(ax=ax, color='#dee6ef',zorder=0, linewidth=0.6, edgecolor='white')
ax = br.plot(ax=ax, color='#f1f1f1',zorder=1, linewidth=0.6, edgecolor='#b7b7b7')
ax = shape_estado_mun.plot(ax=ax, color='lightgrey',zorder=2, linewidth=0.6, edgecolor='white')        #plota uma camada com as outras cidades do estado
lim_ext.plot(ax=ax, zorder= 5, color='none', edgecolor= 'dimgray', linewidth=1.5)           #plota uma camada com a borda do municipio

ax.set_box_aspect(0.47058)                                   #define a proporção do frame (mapa)
minx, miny, maxx, maxy = cidade_setores.geometry.total_bounds        #pega a proporção da camada só com os setores e ajusta

ax.set_xlim(minx - 500, maxx + 7000)                         #ajusta posição de plot
ax.set_ylim(miny - 2000, maxy + 2000)

#usar rótulos
#for idx, row in sp.iterrows():
#    ax.annotate(text=row['NM_MUNICIP'], xy=(row['geometry'].centroid.x, row['geometry'].centroid.y),
#               xytext=(3, 3), textcoords='offset points', fontsize=8, color='#4d4d4d')

#título
#titulo = "Mapa de "+ variavel_censo + " de " + cidade
#plt.title (titulo.title(), fontsize=10, loc='center',color='#4d4d4d')

#definindo os eixos
ax.spines['bottom'].set_color('lightgrey')
ax.spines['top'].set_color('lightgrey')
ax.spines['right'].set_color('lightgrey')
ax.spines['left'].set_color('lightgrey')
ax.tick_params( colors='lightgrey')

#plt.rcParams['font.family'] = 'Jost-Regular'
plt.xlabel( "Longitude" ,color='lightgrey', fontsize=5)
plt.ylabel( "Latitude", color='lightgrey',fontsize=5)
plt.xticks(fontname="Jost", fontsize=4, color='lightgrey')
plt.yticks(fontname="Jost", fontsize=4, color='lightgrey')
ax.ticklabel_format(useOffset=False, style='plain')        #remove a notação científica
ax.add_artist(ScaleBar(dx=1, box_color= 'none',color = '#7a7a7a', location='lower left')) #Barra de escala


#gdf = gpd.read_file(gpd.datasets.get_path('nybb'))
#gdf.plot(ax=ax)

##inserção de norte
#x, y, arrow_length = 0.5, 0.5, 0.1
#ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
#            arrowprops=dict(facecolor='black', width=5, headwidth=15),
#            ha='center', va='center', fontsize=20,
#            xycoords=ax.transAxes)


fig.tight_layout()
plt.plot()

#caminho="/content/drive/MyDrive/Mapas_imersao/"+i.replace(" ", "_")+".jpeg"
#fig.savefig((caminho), dpi=300)
