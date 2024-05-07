from shiny import App, ui, render
from shinywidgets import render_widget, output_widget, render_plotly
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd

from netCDF4 import Dataset
import xarray as xr
import netCDF4 as nc
import matplotlib.pyplot as plt
import scipy.io
import h5py
import plotly.figure_factory as ff
import geopandas as gpd
from shapely.geometry import LineString
import random


# 从 CSV 文件中读取数据
data = pd.read_csv('saying_data.csv')

# 定义页面布局
page1 = ui.page_fluid(  
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_select("file_1", "Select file:", {"file1": "saying_data"}),
            ui.input_select("type_1", "Select saying type:", {"var1": "人生／幸福", "var2": "人際關係", "var3": "逆境／痛苦", "var4": "自我實現", "var5": "自我認識／省察", "var6": "Not specify"}),
            ui.input_select("people","Select who? ",{"var1":"齊克果","var2":"沙特","var3":"尼采","var4":"柏拉圖","var5":"蘇格拉底","var6":"亞里斯多德","var7":"馬可・奧理略","var8":"康德","var9":"笛卡兒","var10":"黑格爾","var11":"伊比鳩魯",
                                                     "var12":"洛克","var13":"西蒙波娃","var14":"斯賓諾莎","var15":"杜斯妥也夫斯基","var16":"Not specify"}),
            ui.input_slider("saying_num1", "How many answers?", 1, 10, 1),

        ),
        ui.output_text_verbatim("random_sentence1")
    ),
)  

# 服务器函数
# 服务器函数
def server(input, output, session):
    @render.text 
    def random_sentence1():
        type_1, people, saying_num1 = input.type_1(), input.people(), input.saying_num1()
        type_dict = {
            "var1": "人生／幸福",
            "var2": "人際關係",
            "var3": "逆境／痛苦",
            "var4": "自我實現",
            "var5": "自我認識／省察",
            "var6": "Not specify"
        }

        people_dict = {
            "var1": "齊克果",
            "var2": "沙特",
            "var3": "尼采",
            "var4": "柏拉圖",
            "var5": "蘇格拉底",
            "var6": "亞里斯多德",
            "var7": "馬可・奧理略",
            "var8": "康德",
            "var9": "笛卡兒",
            "var10": "黑格爾",
            "var11": "培根",
            "var12": "伊比鳩魯",
            "var13": "洛克",
            "var14": "西蒙波娃",
            "var15": "斯賓諾莎",
            "var16": "杜斯妥也夫斯基",
            "var17": "Not specify"
        }
        selected_sayings = random.sample(data["saying"].tolist(),saying_num1)
        saying_ans=""

        for i in range(saying_num1):
            saying_type = selected_sayings[i]  # 默认情况下，假设选中的内容是一个字符串

            if type_1 != "var6":
                type_key = type_dict.get(type_1)
                if isinstance(selected_sayings[0], dict) and type_key in selected_sayings[0]:
                    saying_type = selected_sayings[0][type_key]

            if people != "var17" and isinstance(saying_type, dict):
                saying_type = saying_type.get(people_dict.get(people))
            
            saying_ans=saying_ans+str(i+1)+". "+saying_type+"\n"+"\n"

        return str(saying_ans)  # 将结果转换为字符串




# 定义应用程序 UI
app_ui = ui.page_navbar(
    ui.nav_panel("Page 1", page1),
    title="Page title"
)

# 创建应用程序
app = App(app_ui, server)
