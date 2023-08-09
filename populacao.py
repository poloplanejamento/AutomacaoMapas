pip install geopandas -q
pip install pandas -q
pip install matplotlib -q              #permite personalizar opões de design
pip install matplotlib.scalebar -q     #módulo da matplot específico para escala
pip install contextily -q
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable #da escala
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, TransformedBbox #da escala
from matplotlib_scalebar.scalebar import ScaleBar #da escala

#sp= gpd.read_file('/content/drive/MyDrive/Camadas/35MUE250GC_SIR.shp')
#sp.plot()

#br= gpd.read_file('/content/drive/MyDrive/Camadas/BRUFE250GC_SIR.shp')
#br.plot()

#setores = gpd.read_file('/content/drive/MyDrive/Camadas/35SEE250GC_SIR.shp')
#setores.plot()

#setores.head()

#tabela = pd.read_csv('/content/drive/MyDrive/Camadas/Basico_SP2.csv', sep=";", decimal=",", encoding="LATIN-1")
#tabela.head()

#dados= setores.merge(tabela, left_on="code_tract", right_on="Cod_setor")
#dados.head()