from shiny import App, ui, render
from shinywidgets import render_widget, output_widget, render_plotly
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import scipy.io
import plotly.figure_factory as ff
import geopandas as gpd

data=pd.read_csv('data.csv')
page1 = ui.page_fluid(  
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_select("file_1", "select file:", {"file1": "20220402_115000_7_0_19_046_DD", "file2": "20220402_115000_7_0_19_046_DD"}),
            ui.input_select("datetime_1", "select datetime:", {"var1": "2022-04-02 11:40:24", "var2": "2022-04-02 11:42:00", "var3": "2022-04-02 11:43:36", "var4": "2022-04-02 11:45:12", "var5": "2022-04-02 11:46:48", "var6": "2022-04-02 11:48:23", "var7": "2022-04-02 11:49:59"}),
            ui.input_select("WSWD_1", "WS/WD:", {"WS": "WS", "WD": "WD"}),
            ui.input_select("height_1", "height:", {"50": "50", "75": "75", "100": "100", "125": "125", "150": "150", "175": "175", "200": "200", "225": "225"}),
            ui.input_select("grid_1", "grid:", {"inner": "inner", "all": "all"}),
            ui.input_select("size_1", "size of the picture:", {"500": "500", "700": "700","900":"900"} , selected="700"),
            ui.input_slider("plotscale_1", "Plot scale:", 10, 50, 30),
            ui.input_slider("eastingrange_1", "easting range:", 264800.0, 285150.0, [264800.0, 285150.0]),
            ui.input_slider("WSrange_1", "WS range:", 10, 23, [10, 23]),
            ui.input_slider("WDrange_1", "WD range:", 0, 360, [0, 360]),
            ui.input_slider("WSscale_1", "WS scale:", 0, 100, 40),
            ui.input_select("vectorspacing_1", "vector spacing:", {"50": "50", "100": "100", "150": "150", "200": "200", "250": "250", "300": "300", "350": "350", "400": "400", "450": "450", "500": "500"}, selected="400"),
            ui.layout_columns(
                ui.input_action_button("plot_1", "plot"),
                ui.input_action_button("download_1", "download"),
            )
        ),
        ui.panel_main(
            output_widget("plot_raster"),
        ),
    ),
)  

page2 = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_select("file_2", "select file:", {"file1": "20220402_115000_7_0_19_046_DD", "file2": "20220402_115000_7_0_19_046_DD"}),
            ui.input_select("datetime_2", "select datetime:", {"var1": "2022-04-02 11:40:24", "var2": "2022-04-02 11:42:00", "var3": "2022-04-02 11:43:36", "var4": "2022-04-02 11:45:12", "var5": "2022-04-02 11:46:48", "var6": "2022-04-02 11:48:23", "var7": "2022-04-02 11:49:59"}),
            ui.input_select("WSWD_2", "WS/WD:", {"WS": "WS", "WD": "WD"}),
            ui.input_select("angle_2", "project angle", {"0": "0", "5": "5", "10": "10", "15": "15", "20": "20", "25": "25", "30": "30", "35": "35","40": "40","45": "45","50": "50","55": "55","60": "60","65": "65","70": "70","75": "75","80": "80","85": "85","90": "90",
                                                         "95": "95","100": "100","105": "105","110": "110","115": "115","120": "120","125": "125","130": "130","135": "135","140": "140","145": "145","150": "150","155": "155","160": "160","165": "165","170": "170","175": "175","180": "180",
                                                        "185": "185","190": "190","195": "195","200": "200","205": "205","210": "210","215": "215","220": "220","225": "225","230": "230","235": "235","240": "240","245": "245","250": "250","255": "255","260": "260","265": "265","270": "270",
                                                        "275": "275","280": "280","285": "285","290": "290","295": "295","300": "300","305": "305","310": "310","315": "315","320": "320","325": "325","330": "330","335": "335","340": "340","345": "345","350": "350","355": "355","360": "360"}),
            ui.input_slider("color_bar_range_2", "color bar range:", -20, 30, [-5, 30]),
            ui.input_radio_buttons("station_manual_2", "station or manual:", {"station": "station", 'manual': 'manual'}),
            ui.panel_conditional(
                "input.station_manual_2 == 'station'",
                ui.input_select("station_select_2", "Which station ?", {"var1": "280550,2734150 (met mast)", "var2": "280678.72,2736246.21 (station 1)", "var3": "280338.95,2736545.3 (station 2)", "var4": "279993.23,2736847.47 (station 3)", "var5": "280975.78,2734872.33 (station 4)", "var6": "280503.33,2735265.39 (station 5)", "var7": "280130.53,2735631.97 (station 6)","var8": "279320.24,2736319.08 (station 8)","var9": "278780.12,2735709.72 (station 13)",
                                    "var10": "280121.22,2733418.22 (station 14)","var11": "279713.58,2733728.3 (station 15)","var12": "279262.23,2734128.04 (station 16)","var13": "278812.1,2734542.78 (station 17)","var14": "279154.34,2733247.26 (station 19)","var15": "279143.53,2732742.3 (station 21)","var16": "277410.48,2734608.26 (station 24)","var17": "278131.93,2732973.06 (station 25)","var18": "277709.34,2733287.35 (station 26)"
                                    ,"var19": "277319.42,2733647.19 (station 27)","var20": "278089.11,2732507.73 (station 28)","var21": "277206.34,2732616.41(station 30)","var22": "276704.53,2733054.91(station 31)","var23": "276360.06,2733375.07(station 32)"})
            ),
            ui.panel_conditional(
                "input.station_manual_2 == 'manual'",
                ui.input_slider("manual_easting_2", "manual easting:", 256750, 288700, 275000),
                ui.input_slider("manual_northing_2", "manual northing:", 2723700, 2758900, 2734000),

            ),

        ui.layout_columns(
            ui.input_action_button("plot_", "plot"),
            ui.input_action_button("download_", "download"),
        )
        ),

        ui.panel_main(
            output_widget("plot_projection"),
            output_widget("plot_map")
        ),
    ),  
)


def server(input, output, session):
    @render_widget
    def plot_raster(): 
        file, datetime, wswd, height, grid, size,plot_scale,eastingrange, wsrange, wdrange, wsscale, vectorspacing = input.file_1(), input.datetime_1(), input.WSWD_1(), input.height_1(), input.grid_1(),input.size_1(),input.plotscale_1(), input.eastingrange_1(), input.WSrange_1(), input.WDrange_1(), input.WSscale_1(), input.vectorspacing_1()
        
        return scatterplot  
    
    @render_widget
    def plot_projection(): 
        file, datetime, wswd, angle, color_bar_range, station_manual,station_choose ,easting,northing= input.file_2(), input.datetime_2(), input.WSWD_2(), input.angle_2(), input.color_bar_range_2(), input.station_manual_2(),input.station_select_2(),input.manual_easting_2(),input.manual_northing_2()

        return projection  
    
    @render_widget
    def plot_map(): 
        file, datetime, wswd, angle, color_bar_range, station_manual,station_choose ,easting,northing= input.file_2(), input.datetime_2(), input.WSWD_2(), input.angle_2(), input.color_bar_range_2(), input.station_manual_2(),input.station_select_2(),input.manual_easting_2(),input.manual_northing_2()
        
        return plot_map

app_ui = ui.page_navbar(
    ui.nav_panel("Page 1", page1),
    ui.nav_panel("Page 2", page2),
    title="Page title"
)

app = App(app_ui, server)

