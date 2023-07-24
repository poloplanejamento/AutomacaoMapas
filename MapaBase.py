
""""
#esta parte do código é de instalação de pacotes, 
#permitem chamar funções específicas para além das básicas de python
#para funcionar, deve-se copiar o trecho abaixo e colar no "TERMINAL"
#você só precisa instalar uma vez na sua máquina, nas próximas vezes é só importar 
   
pip install geopandas
pip install pandas
pip install geobr
pip install matplotlib
pip install matplotlib.scalebar
pip install contextily

"""

#sempre é necessário importar no começo de um código


import pandas as pd
import geopandas as gpd
import geobr
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable #da escala
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, TransformedBbox #da escala
from matplotlib_scalebar.scalebar import ScaleBar #da escala

geobr.list_geobr() #lista todas as funções desta bibliotaca, é possível baixar dados já prontos

#Importa dados do Censo2010 do estado de São Paulo, para outros Estados, substituir sigla
geobr.read_census_tract(code_tract="SP", year=2010)
censo_sp_2010 = geobr.read_census_tract(code_tract="SP", year=2010) 
censo_sp_2010.plot()  #imprime o resultado na tela

#Importa os setores censitarios do Censo2010 da cidade de São Paulo, para outras, substituir código do IBGE
censo_sp_2010 = geobr.read_census_tract(code_tract=3550308, year=2010)
censo_sp_2010.plot() #imprime o resultado na tela

#Inicio da montagem do mapa
areaUrbana = geobr.read_urban_area(year=2015)   # a variável criada 'areaUrbana' está recebendo os dados de area urbana do ano de 2015 (ano é o parâmetro aceito)
areaUrbana.plot() #imprime o resultado na tela

urbano_sp = areaUrbana[areaUrbana.code_muni==3550308] # a variável criada 'urbano_sp' está recebendo os dados filtrados pelo código da area urbana de São Paulo
urbano_sp.plot() #imprime o resultado na tela

urbano_sp=urbano_sp.to_crs(epsg=31983) #muda o epsg para o padrão para a cidade de São Paulo 31983 - Sirgas 2000 23 sul
urbano_sp.plot() #imprime o resultado na tela

municipio = geobr.read_municipality(code_muni=3550308, year=2010) # a variável criada 'municipio' recebe a feição do município de São Paulo
municipio.plot()

municipio=municipio.to_crs(epsg=31983) #muda o epsg para o padrão para a cidade de São Paulo 31983 - Sirgas 2000 23 sul
municipio.plot()

#Primeira versão com as camadas sobrepostas
base = municipio.plot() # a variavel criada "base" recebe uma plotagem que é usada como base no plot da linha abaixo
urbano_sp.plot(ax=base, color='red') 


fig, ax = plt.subplots()
ax = municipio.plot(ax=ax, color='dimgrey')
#ax.set_axis_off();
ax = urbano_sp.plot(ax=ax, color='salmon')
ax.set_axis_off()
#cx.add_basemap(ax, crs=municipio.crs.to_string(), source=cx.providers.CartoDB.Positron)
plt.show()

#Criação do buffer do municipio de SP
buffer_mun=municipio.buffer(10000)
buffer_mun.plot(alpha=0.5)

#Versão com buffer com transparencia
fig, ax = plt.subplots()
ax = municipio.plot(ax=ax, color='dimgrey',zorder=0)
#ax.set_axis_off();
ax = buffer_mun.plot(ax=ax,color='C1', alpha=0.5, zorder=3)
ax = urbano_sp.plot(ax=ax, color='salmon',zorder=2)
ax.set_axis_off()
#cx.add_basemap(ax, crs=municipio.crs.to_string(), source=cx.providers.CartoDB.Positron)
plt.show()

#Transformação do buffer em DataFrame que permite a utilização da ferramenta de "diferença"
buffer_mun=municipio.buffer(100000)
#buffer_mun.plot(alpha=0.5)
type(buffer_mun)
df_buffer = buffer_mun.to_frame()

#Aplicação da ferramenta "diferença"
resultado = gpd.overlay( df_buffer, municipio, how='difference')
resultado.plot()

#Adição do limite da extensão da figura
fig, ax = plt.subplots(figsize=(9,9))
ax.set_xlim(250000,420000)
ax.set_ylim(7330000,7440000)
#Rotação da grade "Y"
ax.tick_params(axis="y",labelrotation=90)
ax.set_box_aspect(1)
ax = municipio.plot(ax=ax, color='dimgrey',zorder=0)
#ax = hidro.plot(ax=ax,zorder=1)
ax = resultado.plot(ax=ax,color='white', alpha=0.7, zorder=3)
ax = urbano_sp.plot(ax=ax, color='salmon',zorder=2)
ax.set_axis_on()
#cx.add_basemap(ax, crs=municipio.crs.to_string(), source=cx.providers.CartoDB.Positron)
plt.show()

#Versão do mapa com legenda e escala
fig, ax = plt.subplots(figsize=(8,8))
ax = municipio.plot(ax=ax, color='dimgrey',zorder=0)
#ax = hidro.plot(ax=ax,zorder=1)
ax = resultado.plot(ax=ax,color='white', alpha=0.7, zorder=3)
ax = urbano_sp.plot(ax=ax, color='salmon',zorder=2)
#Inserção da legenda
ax.legend(loc='lower left')
ax.set_xlim(250000,420000)
ax.set_ylim(7320000,7440000)
ax.tick_params(axis="y",labelrotation=90)
ax.set_box_aspect(1)
ax.set_axis_on()
#Inserção da escala
ax.add_artist(ScaleBar(dx=1, location='lower right'))
#cx.add_basemap(ax, crs=municipio.crs.to_string(), source=cx.providers.CartoDB.Positron)
plt.show()