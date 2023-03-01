from dash import Dash, html, Output, Input, callback, dcc
import dash_mantine_components as dmc
from generate import Calls
import random
import pandas as pd
from dash_iconify import DashIconify
import plotly.express as px


app = Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

app.title = "Billings Dashboard"
server = app.server
# app.config["suppress_callback_exceptions"] = True

# say the number of calls can range from 67 to 124
company_logs = Calls().many_calls(random.randint(67, 124))

df = pd.DataFrame(data=company_logs["data"], columns=company_logs["columns"])

df.sort_values(by="day", inplace=True)

# print(company_logs)

fig1 = px.histogram(
    df,
    x="start_time",
    y="duration",
    color="status",
    barmode="group",
    title="call volume",
    width=550,
    height=400,
)

df_status = df.groupby(["status"]).sum().reset_index()
fig2 = px.pie(
    df_status, names="status", values="duration", hole=0.5, width=350, height=300
)

df_country = df.groupby(["dest"]).sum().reset_index()
fig3 = px.choropleth(
    df_country,
    locations="dest",
    color="duration",  # lifeExp is a column of gapminder
    hover_name="dest",
    locationmode="country names",
    color_continuous_scale="Reds",
    width=550,
    height=400,
    title="countries called",
)

df_days = df.groupby(["day"]).sum()
fig4 = px.line(
    df_days,
    y="down_time",
    labels={"down_time": "total down time in minutes"},
    width=550,
    height=400,
)

ans = 80
df2 = pd.DataFrame({"names": ["answered", " "], "values": [ans, 100 - ans]})

# plotly
fig5 = px.pie(
    df2,
    values="values",
    names="names",
    hole=0.5,
    color_discrete_sequence=["green", "rgba(0,0,0,0)"],
    width=550,
    height=400,
    title="",
)

fig4.data[0].textfont.color = "white"



app.layout = html.Div(
    [
        dmc.Group(
            [
                html.H1("VoIP Dashboard"),
                dmc.Avatar(
                    "DA",
                    color="yellow",
                    radius="xl",
                ),
            ]
        ),
        dmc.Divider(variant="solid"),
        dmc.Group(
            [
                html.H2("Calls"),
                dmc.SegmentedControl(
                    id="call-type-segmented",
                    value="all",
                    data=[
                        {"value": "all", "label": "All"},
                        {"value": "inbound", "label": "Inbound"},
                        {"value": "outbound", "label": "Outbound"},
                    ],
                ),
            ]
        ),
        dmc.Group(
            [
                dmc.Card(
                    [
                        dmc.Group(
                            [
                                DashIconify(icon="la:slack-hash", width=20),
                                "Number of calls",
                            ]
                        ),
                        dmc.Center(html.H2(df.shape[0], id="number-calls")),
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="md",
                ),
                dmc.Card(
                    [
                        dmc.Group(
                            [
                                DashIconify(
                                    icon="ic:sharp-access-time-filled", width=20
                                ),
                                "Total Minutes",
                            ]
                        ),
                        dmc.Center(
                            html.H2(f"{df['duration'].sum():,}", id="total-minutes")
                        ),
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="md",
                ),
                dmc.Card(
                    [
                        dmc.Group(
                            [
                                DashIconify(icon="ph:money-fill", width=20),
                                "Amount(₦)",
                            ]
                        ),
                        dmc.Center(html.H2(f"{df.shape[0]*500+100:,}", id="amount")),
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="md",
                ),
            ],
        ),
        dmc.Group(
            [
                dcc.Graph(id="call-volume", figure=fig1),
                dmc.Card(
                    [
                        dmc.Group(
                            [
                                DashIconify(icon="pajamas:status-alert", width=20),
                                "Status over period",
                            ]
                        ),
                        dcc.Graph(id="status-pie", figure=fig2),
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="md",
                ),
                dcc.Graph(id="countries-called", figure=fig3),
            ]
        ),
        dmc.Divider(variant="solid"),
        html.H2("Service"),
        dmc.Group(
            [
                dcc.Graph(id="downtime", figure=fig4),
                dcc.Graph(id="service-donut", figure=fig5),
            ]
        ),
    ]
)


@app.callback(
    Output("number-calls", "children"),
    Output("total-minutes", "children"),
    Output("amount", "children"),
    Output("call-volume", "figure"),
    Output('status-pie', 'figure'),
    Output('countries-called', 'figure'),
    Output('downtime', 'figure'),
    Output('service-donut', 'figure'),
    Input("call-type-segmented", "value"),
)
def change_call_type(call_type):
    if call_type == "inbound":
        dff = df[df["call_type"] == "inbound"]
    elif call_type == "outbound":
        dff = df[df["call_type"] == "outbound"]
    else:
        dff = df

    nc = dff.shape[0]
    tm = f"{dff['duration'].sum():,}"
    am = f"{dff.shape[0]*500+100:,}"

    fig1 = px.histogram(
        dff,
        x="start_time",
        y="duration",
        color="status",
        barmode="group",
        title="call volume",
        width=550,
        height=400,
    )

    dff_status = dff.groupby(["status"]).sum().reset_index()
    fig2 = px.pie(
        dff_status, names="status", values="duration", hole=0.5, width=350, height=300
    )

    dff_country = dff.groupby(["dest"]).sum().reset_index()
    fig3 = px.choropleth(
        dff_country,
        locations="dest",
        color="duration",  # lifeExp is a column of gapminder
        hover_name="dest",
        locationmode="country names",
        color_continuous_scale="Reds",
        width=550,
        height=400,
        title="countries called",
    )

    dff_days = dff.groupby(["day"]).sum()
    fig4 = px.line(
        dff_days,
        y="down_time",
        labels={"down_time": "total down time in minutes"},
        width=550,
        height=400,
    )

    ans = 80
    dff2 = pd.DataFrame({"names": ["answered", " "], "values": [ans, 100 - ans]})

    # plotly
    fig5 = px.pie(
        dff2,
        values="values",
        names="names",
        hole=0.5,
        color_discrete_sequence=["green", "rgba(0,0,0,0)"],
        width=550,
        height=400,
        title="",
    )


    return nc, tm, am, fig1, fig2, fig3, fig4, fig5


if __name__ == "__main__":
    app.run_server(
        debug=True,
        dev_tools_hot_reload_watch_interval=7,
        dev_tools_hot_reload_interval=7,
    )
