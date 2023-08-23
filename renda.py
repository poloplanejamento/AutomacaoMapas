!pip install geopandas -q
!pip install pandas -q
!pip install matplotlib -q              #permite personalizar opões de design
!pip install matplotlib.scalebar -q     #módulo da matplot específico para escala
!pip install contextily -q              #Importação de mapa base externo
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable #da escala
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, TransformedBbox #da escala
from matplotlib_scalebar.scalebar import ScaleBar #da escala
sp= gpd.read_file('/content/drive/MyDrive/Camadas/35MUE250GC_SIR.shp')
sp.plot()
sp=sp.to_crs(epsg=31983)
br= gpd.read_file('/content/drive/MyDrive/Camadas/BRUFE250GC_SIR.shp')
br.plot()
br=br.to_crs(epsg=31983)
setores = gpd.read_file('/content/drive/MyDrive/Camadas/35SEE250GC_SIR.shp')
setores.plot()
setores=setores.to_crs(epsg=31983)
setores.head()
tabela = pd.read_csv('/content/drive/MyDrive/Camadas/Basico_SP2.csv', sep=";", decimal=",", encoding="UTF-8")
tabela.head()
tabela = tabela[["Cod_setor", "V005"]]
tabela.head()
tabela.Cod_setor.dtype
setores.CD_GEOCODI.dtype
setores.CD_GEOCODI= setores.CD_GEOCODI.astype(int)
setores.CD_GEOCODI.dtype
dados= setores.merge(tabela, left_on="CD_GEOCODI", right_on="Cod_setor")
dados.head()
dados.plot()
!pip install geopandas
!pip install mapclassify -q

#para exportar todos os mapas do estado de uma única vez
# import matplotlib.pyplot as plt

# for i in pd.unique(dados.NM_MUNICIP):
#   fig,ax= plt.subplots(figsize=(10,10))
#   selec= dados[dados.NM_MUNICIP ==i]
#   selec.plot(column="V005", ax=ax, scheme="quantiles", k=3, cmap="OrRd", edgecolor="k", legend=True, legend_kwds={'loc': "center left", "bbox_to_anchor": (1,0.5), "title": "Rendimento Nominal\nmédio mensal"})
#   ax.set_title(i, x=0.5, y=1.25, va="center")
#   fig.subplots_adjust(top=0.75)
#   fig.tight_layout()
#   caminho="/content/drive/MyDrive/Exportados/"+i.replace(" ", "_")+".jpeg"
#   fig.savefig((caminho), dpi=300)

#exporta os mapas zipados para o drive
#  !zip -r /content/drive/MyDrive/Exportados.zip /content/drive/MyDrive/Exportados


#Código atualizado em 22/08/23

cidade = "CERQUILHO"

fig, ax = plt.subplots(figsize=(8,8))

ax = sp.plot(ax=ax, color='grey', zorder=0)

selec= dados[dados.NM_MUNICIP == cidade]
selec.plot(column="V005", ax=ax, scheme="natural_breaks", k=5, cmap="OrRd", edgecolor='#eeeeee', legend=True, legend_kwds={
  'loc': "lower right",
  "title": "Rendimento Nominal\nmédio mensal",
  "fontsize":"xx-small",
  "title_fontsize":"x-small" })
#column é a coluna selecionada da tabela (no caso, renda)
#ax=ax é a posição do plot (preciso entender melhor)
#scheme é a simbologia por categorização (quantiles, equal_interval, natural_breaks)
#k é o número de classes da categorização
#cmap é a definição das cores do mapa. (https://matplotlib.org/stable/gallery/index.html#color)
#edgecolor é definição de cor da borda das feições. Para retirar as bordas, usar edgecolor='nome'
#legend é a opção para inserir ou não a legenda

ax.set_box_aspect(0.4067)
pos1 = ax.get_position()
ax.set_position(pos1)
#ax.set_box_aspect determina a proporção da area de impressão

minx, miny, maxx, maxy = selec.geometry.total_bounds
ax.set_xlim(minx - 100, maxx + 100) # added/substracted value is to give some margin around total bounds
ax.set_ylim(miny - 400, maxy + 400)

titulo = "Mapa de renda de " + cidade
plt.title (titulo.title(), fontsize=12, loc='center',color='#4d4d4d')
plt.xlabel("Longitude", color='#4d4d4d')
plt.ylabel("Latitude", color='#4d4d4d')
plt.xticks(color='#4d4d4d')
plt.yticks(color='#4d4d4d')


fig.tight_layout()
plt.plot()
