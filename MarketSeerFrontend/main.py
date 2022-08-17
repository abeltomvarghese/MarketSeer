import ast
from datetime import datetime, date
import pandas as pd
import json
import requests
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import gridplot, row, layout, column
from bokeh.models import Button, Select, ColumnDataSource, TableColumn, DataTable
from bokeh.io import curdoc
from bokeh.models.widgets import AutocompleteInput

def get_data_from_backend(stock_ticker, model_name):
    api_connection_string = f'http://localhost:8000/stock/{stock_ticker}/{model_name}'
    data_request = requests.get(api_connection_string)

    forecast_json = data_request.json()
    forecast_string = json.dumps(forecast_json, indent=2)
    forecast_json = json.loads(forecast_string)
    pred_list = forecast_json['data']
    pred_list = ast.literal_eval(pred_list)
    df = pd.DataFrame(pred_list)
    error_rates_dict = dict((error_rate, forecast_json[error_rate]) for error_rate in ('basic', 'grid', 'random', 'bayes', 'hyperopt', 'optuna'))

    df['cobdate_partition'] = pd.to_datetime(df['cobdate_partition'], origin='unix', unit='ms').dt.date
    return df, error_rates_dict


def get_stock_info_dict():
    stock_info_dict = {}

    r = requests.get("https://dumbstockapi.com/stock?exchanges=NYSE&exchanges=NASDAQ&exchanges=AMEX")
    json_data = r.json()

    for item in json_data:
        stock_info_dict[item['ticker'] + " " + item['name']] = item['ticker']

    return stock_info_dict


def update_dashboard():
    ticker_input = stock_input.value
    model_input = model_select.value

    new_df, smape_errors = get_data_from_backend(stock_dict[ticker_input], model_input)
    data_df.data = new_df
    smape_errors = convert_to_dict_object(smape_errors)
    smape_data.data = smape_errors


def convert_to_dict_object(err_dict):
    dict_object = {}
    for each_key in err_dict:
        if err_dict[each_key] >= 100.0 or err_dict[each_key] <= 0.0:
            dict_object[each_key] = [100.0]
        else:
            dict_object[each_key] = [err_dict[each_key]]

    return dict_object
# returned_df, smape_dict = get_data_from_backend('HMC', 'KNN')
#
#
#
#
# returned_df.to_csv('starting_data.csv', index=False)
#
# with open('error_data.json', 'w') as data_file:
#     json.dump(smape_dict, data_file)

smape_dict = {}
with open('error_data.json', 'r') as err_data_file:
    smape_dict = json.load(err_data_file)

smape_dict = convert_to_dict_object(smape_dict)

static_df = pd.read_csv('starting_data.csv')
static_df['cobdate_partition'] =pd.to_datetime(static_df['cobdate_partition'])

data_df = ColumnDataSource(data=static_df)
smape_data = ColumnDataSource(data=smape_dict)

print(data_df)
stock_dict = get_stock_info_dict()


basic_graph = figure(
    title=f"Forecast From Basic Model",
    x_axis_label="Cobdate Partition",
    y_axis_label="Price",
    x_axis_type='datetime',
    plot_height=500,
    plot_width=750)

basic_graph.title.text_font_size = '20px'
basic_graph.line(x='cobdate_partition', y='actual_data', legend_label="Actual Price", line_width=2, line_color="blue", source=data_df)
basic_graph.line(x='cobdate_partition', y='basic_pred', legend_label="Basic Prediction", line_width=2, line_color="orange", source=data_df)



grid_graph = figure(
    title=f"Forecast From Grid Search Optimized Model",
    x_axis_label="Cobdate Partition",
    y_axis_label="Price",
    x_axis_type='datetime',
    plot_height=350,
    plot_width=750)

grid_graph.title.text_font_size = '20px'
grid_graph.line(x='cobdate_partition', y='actual_data', legend_label="Actual Price", line_width=2, line_color="blue", source=data_df)
grid_graph.line(x='cobdate_partition', y='grid_search', legend_label="Grid Search", line_width=2, line_color="orange", source=data_df)


random_graph = figure(
    title=f"Forecast From Random Search Optimized Model",
    x_axis_label="Cobdate Partition",
    y_axis_label="Price",
    x_axis_type='datetime',
    plot_height=350,
    plot_width=750)

random_graph.title.text_font_size = '20px'
random_graph.line(x='cobdate_partition', y='actual_data', legend_label="Actual Price", line_width=2, line_color="blue", source=data_df)
random_graph.line(x='cobdate_partition', y='random_search', legend_label="Random Search", line_width=2, line_color="orange", source=data_df)


bayes_graph = figure(
    title=f"Forecast From Bayesian Optimized Model",
    x_axis_label="Cobdate Partition",
    y_axis_label="Price",
    x_axis_type='datetime',
    plot_height=350,
    plot_width=750)

bayes_graph.title.text_font_size = '20px'
bayes_graph.line(x='cobdate_partition', y='actual_data', legend_label="Actual Price", line_width=2, line_color="blue", source=data_df)
bayes_graph.line(x='cobdate_partition', y='bayes', legend_label="Bayesian", line_width=2, line_color="orange", source=data_df)


hyperopt_smape_error = smape_data.data['hyperopt']

hyperopt_graph = figure(
    title=f"Forecast From Hyperopt Optimized Model",
    x_axis_label="Cobdate Partition",
    y_axis_label="Price",
    x_axis_type='datetime',
    plot_height=350,
    plot_width=750)

hyperopt_graph.title.text_font_size = '20px'
hyperopt_graph.line(x='cobdate_partition', y='actual_data', legend_label="Actual Price", line_width=2, line_color="blue", source=data_df)
hyperopt_graph.line(x='cobdate_partition', y='hyperopt', legend_label="Hyperopt", line_width=2, line_color="orange", source=data_df)


optuna_smape_error = smape_data.data['optuna']

optuna_graph = figure(
    title=f"Forecast From Optuna Optimized Model",
    x_axis_label="Cobdate Partition",
    y_axis_label="Price",
    x_axis_type='datetime',
    plot_height=350,
    plot_width=1500)

optuna_graph.title.text_font_size = '20px'
optuna_graph.line(x='cobdate_partition', y='actual_data', legend_label="Actual Price", line_width=2, line_color="blue", source=data_df)
optuna_graph.line(x='cobdate_partition', y='optuna', legend_label="Optuna", line_width=2, line_color="orange", source=data_df)

stock_input = AutocompleteInput(title="Enter stock ticker & Select Model", value="HMC", completions=list(stock_dict.keys()), case_sensitive=False )
model_select = Select(value="KNN", options=['KNN', 'MLP'])
submit_btn = Button(label="Submit", button_type='success')
submit_btn.on_click(update_dashboard)

model_select_button = row(model_select, submit_btn)

table_columns = [
    TableColumn(field='basic', title='Basic Prediction'),
    TableColumn(field='grid', title='Grid Search'),
    TableColumn(field='random', title='Random Search'),
    TableColumn(field='bayes', title='Bayesian Optimization'),
    TableColumn(field='hyperopt', title='Hyperopt'),
    TableColumn(field='optuna', title='Optuna'),
]

my_table = DataTable(source=smape_data, columns=table_columns)

controls = column(stock_input, model_select_button, my_table)

first = row(basic_graph, controls)
second = row(grid_graph, random_graph)
third = row(bayes_graph, hyperopt_graph)
root_elm = column(first, second, third, optuna_graph)


curdoc().add_root(root_elm)
curdoc().title = "Stock Dashboard"
