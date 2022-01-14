import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
import openpyxl

data = pd.read_excel("for_dashboard_edited2.xlsx", engine="openpyxl")
#print(df_pd.head)
print(data.columns.values.tolist())


total_infection = data['total_infection'].replace(999, np.NaN)
severe_infection = data['severe_infection'].replace(999, np.NaN)
data['total_infection'] = total_infection
data['severe_infection'] = severe_infection

data["p"] = data["total_infection"]/data["n"]
data["p_severe"] = data["severe_infection"]/data["n"]

xs = ['severe_infection', 'total_infection', 'sex_ratio', 'Age_mean', 'BMI_kg_m2_mean', 
'Caucasian_pct', 'CRP_mg_L_mean', 'RA_duration_mean_yrs', 'Rheumatoid_factor_positive_pct', 
'MTX_pct', 'MTX_dose_mg_week_mean', 'Corticosteroids_pct', 'Cort_dose_mg_day_mean', 
'No_of_prior_DMARDS_mean', 'previous_bDMARD_use_pct', 'Previous_bDMARD_mean', 'ESR_mm_h_mean',
 'CRP_mg_L_mean.1']

data_xs = data[xs]

followup_group_design = data.followup_group_design.unique()
#data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
#data.sort_values("Date", inplace=True)

#wb = openpyxl.load_workbook(filename='example.xlsx', data_only=True)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Scatterplots: identify outliers"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Exploring type of relationship between moderator and proportions ", className="header-title"
                ),
                html.P(
                    #children="Select s"
                    #" and the number of avocados sold in the US"
                    #" between 2015 and 2018",
                    #className="header-description",
                ),
            ],
            className="header",
        ),
           html.Div( 
            children=[
                html.Div(
                    children=[
                        html.Div(children="Design_F_U", className="menu-title"),
                        dcc.Dropdown(
                            id="design_f_u-filter",
                            options=[
                                {"label": f_design, "value": f_design}
                                for f_design in np.sort(data.followup_group_design.unique())
                            ],
                            value="RCTBelow 18 weeks",
                            clearable=False,
                            className="dropdown",
                        style={"width":300,'display': 'inline-block'})
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Type", className="menu-title"),
                        dcc.Dropdown(
                            id="xs-filter",
                            options=[
                                {"label": x, "value": x}
                                for x in xs
                            ],
                            value="sex_ratio",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        style={"width":300, 'display': 'inline-block'}),
                    ],
                ),
                # html.Div(
                #     children=[
                #         html.Div(
                #             children="Date Range",
                #             className="menu-title"
                #             ),
                #         dcc.DatePickerRange(
                #             id="date-range",
                #             min_date_allowed=data.Date.min().date(),
                #             max_date_allowed=data.Date.max().date(),
                #             start_date=data.Date.min().date(),
                #             end_date=data.Date.max().date(),
                #         ),
                #     ]
                # ),
     #       ],
    #        className="menu",
    #    ),

    #   html.Div([
    #     html.Div(
    #       dcc.Graph(id='price-chart', 
    #                 className="six columns",
    #                 style={"width":500, "margin": 0, 'display': 'inline-block'}
    #             ),
    #     html.Div(
    #       dcc.Graph(id='volume-chart', 
    #                 className="six columns",
    #                 style={"width":500, "margin": 0, 'display': 'inline-block'}
    #             ))]
    #     ]), className="row")
        # html.Div(className="row",
        #    children=[
        #          html.Div(
        #              children=[dcc.Graph(
        #                  id="price-chart", style={'display': 'inline-block'},
        #              ), dcc.Graph(id="volume-chart", style={'display': 'inline-block'})],
        #              className="row",
        #          ),
        #      #],
        #      #className="wrapper",
  
        #      #children=[
        #         html.Div(
        #              children=dcc.Graph(
        #                  id="volume-chart2", style={'display': 'inline-block'},
        #              ),
        #              className="card",
        #          ),
        #      ],
        #      #className="wrapper",
        #  ),
     #]
      html.Div(children=[
         dcc.Graph(id="price-chart", style={"width":620, "margin": 5,'display': 'inline-block'}),
         dcc.Graph(id="volume-chart", style={"width":620, "margin": 5,'display': 'inline-block'}),
      ],className="card",)])
            ], )


@app.callback(
    [Output("price-chart", "figure"), Output("volume-chart", "figure")],
    [
        Input("design_f_u-filter", "value"),
        Input("xs-filter", "value"),
    ],
)
def update_charts(f_design, x):
    mask = (
        (data.followup_group_design == f_design)
    )
    filtered_data = data.loc[mask, :]
    filtered_data["x"] = filtered_data[x]

    price_chart_figure = px.scatter(
        filtered_data, x=x, y="p", 
        #color="species", size='petal_length', 
        hover_data=['PMID','followup_group_design'])

    volume_chart_figure = px.scatter(
        filtered_data, x=x, y="p_severe", 
        #color="species", size='petal_length', 
        hover_data=['PMID','followup_group_design'])
    # volume_chart_figure = {
    #     "data": [
    #         {
    #             "x": filtered_data["p_severe"],
    #             "y": filtered_data[xs],
    #             "type": "scatter",
    #         },
    #     ],
    #     "layout": {
    #         "title": {"text": "Avocados Sold", "x": 0.05, "xanchor": "left"},
    #         "xaxis": {"fixedrange": True},
    #         "yaxis": {"fixedrange": True},
    #         "colorway": ["#E12D39"],
    #     },
    #}
    return price_chart_figure, volume_chart_figure

if __name__ == "__main__":
    app.run_server(debug=False)