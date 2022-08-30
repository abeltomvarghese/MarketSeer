import pandas as pd
import numpy as np
import json

from forecastingbackend.data_queries import get_stock_data
from forecastingbackend.HPOAlgorithms.HPOStrategy.GridSearchHPO import GridSearchHPO
from forecastingbackend.HPOAlgorithms.HPOStrategy.RandomSearchHPO import RandomSearchHPO
from forecastingbackend.HPOAlgorithms.HPOStrategy.BayesianHPO import BayesianHPO
from forecastingbackend.HPOAlgorithms.HPOStrategy.HyperoptHPO import HyperoptHPO
from forecastingbackend.HPOAlgorithms.HPOStrategy.OptunaHPO import OptunaHPO
from forecastingbackend.HPOAlgorithms.HPOContext.HPOContext import HPOContext
from forecastingbackend.MLModels.ModelConcreteBuilders.base_model_generator import get_base_models, get_full_model

from sklearn.model_selection import TimeSeriesSplit

def prepare_data(raw_data):
	df = pd.DataFrame(list(
		raw_data.values('weekly_symbol', 'stock_open', 'stock_high', 'stock_low', 'stock_close', 'stock_adj_close','stock_volume', 'dividend_amount',
						'cobdate_partition')))

	df['cobdate_partition'] = pd.to_datetime(df['cobdate_partition'])
	df['rec_year'] = df['cobdate_partition'].dt.year
	df['rec_month'] = df['cobdate_partition'].dt.month
	df['rec_day'] = df['cobdate_partition'].dt.day

	split_index = round(0.9 * len(df.index))
	training_data = df[:split_index]
	testing_data = df[split_index:]

	training_x_data = training_data[
		['rec_year', 'rec_month', 'rec_day', 'stock_open', 'stock_high', 'stock_low', 'stock_adj_close', 'stock_volume', 'dividend_amount']]
	training_y_data = training_data['stock_close']

	test_x_data = testing_data[
		['rec_year', 'rec_month', 'rec_day', 'stock_open', 'stock_high', 'stock_low', 'stock_adj_close', 'stock_volume', 'dividend_amount']]
	test_y_data = testing_data['stock_close']

	return training_x_data, training_y_data, test_x_data, test_y_data


def get_tuned_parameters(ml_model, training_x_data, training_y_data):
	gs_context = HPOContext(GridSearchHPO())

	rs_context = HPOContext(RandomSearchHPO())

	bayes_context = HPOContext(BayesianHPO())

	hyper_context = HPOContext(HyperoptHPO())

	optuna_context = HPOContext(OptunaHPO())

	# gs_hpo = GridSearchHPO()
	# rs_hpo = RandomSearchHPO()
	# b_hpo = BayesianHPO()
	# hyper_hpo = HyperoptHPO()
	# optuna_hpo = OptunaHPO()

	gs_tuned_params = None
	rs_tuned_params = None
	bayes_tuned_params = None
	hyper_tuned_params = None
	optuna_tuned_params = None

	while True:
		try:
			gs_tuned_params = gs_context.get_tuned_parameters(model_type=ml_model, x_data=training_x_data,
														  y_data=training_y_data)
			break
		except ValueError:
			pass

	while True:
		try:
			rs_tuned_params = rs_context.get_tuned_parameters(model_type=ml_model, x_data=training_x_data,
														  y_data=training_y_data)
			break
		except ValueError:
			pass

	while True:
		try:
			bayes_tuned_params = bayes_context.get_tuned_parameters(model_type=ml_model, x_data=training_x_data,
															y_data=training_y_data)
			break
		except ValueError:
			pass

	while True:
		try:
			hyper_tuned_params = hyper_context.get_tuned_parameters(model_type=ml_model, x_data=training_x_data,
																y_data=training_y_data)
			break
		except ValueError:
			pass

	while True:
		try:
			optuna_tuned_params = optuna_context.get_tuned_parameters(model_type=ml_model, x_data=training_x_data,
																  y_data=training_y_data)
			break
		except ValueError:
			pass

	return gs_tuned_params, rs_tuned_params, bayes_tuned_params, hyper_tuned_params, optuna_tuned_params

def get_trained_model(model, training_x_data, training_y_data):
	cv_folds = TimeSeriesSplit(n_splits=6)

	for train_index, test_index in cv_folds.split(X=training_x_data):
		xtrain = training_x_data.iloc[train_index]
		xtest = training_x_data.iloc[test_index]
		ytrain = training_y_data.iloc[train_index]
		ytest = training_y_data.iloc[test_index]

		while True:
			try:
				model.fit(xtrain, ytrain)
				break
			except ValueError:
				pass

		predictions = model.predict(xtest)

	return model

def smape(actual_data, predicted_data):
	return 100 / len(actual_data) * np.sum(2 * np.abs(predicted_data - actual_data) / (np.abs(actual_data) + np.abs(predicted_data)))

# def smape(A, F):
#     tmp = 2 * np.abs(F - A) / (np.abs(A) + np.abs(F))
#     len_ = np.count_nonzero(~np.isnan(tmp))
#     if len_ == 0 and np.nansum(tmp) == 0: # Deals with a special case
#         return 100
#     return 100 / len_ * np.nansum(tmp)

def get_forecast_data(stock_symbol, ml_model):
	the_data = get_stock_data(stock_symbol)
	training_x_data, training_y_data, test_x_data, test_y_data = prepare_data(the_data)

	gs_tuned_params, rs_tuned_params, bayes_tuned_params, hyper_tuned_params, optuna_tuned_params = get_tuned_parameters(ml_model, training_x_data, training_y_data)

	print("The results are as follows: ")
	print("============================")
	print(f'Grid Search Params: {gs_tuned_params}')
	print(f'Random Search Params: {rs_tuned_params}')
	print(f'Bayesian Params: {bayes_tuned_params}')
	print(f'Hyperopt Params: {hyper_tuned_params}')
	print(f'Optuna Params: {optuna_tuned_params}')

	## initialise basic models
	## train and test basic models
	## predict & then store results
	## create tuned models
	##train and test tuned models
	## predict & then store results in one dataframe for each hpo
	## combine all dataframes into one dict accessed by hpo name keys
	## return created dict

	basic_model_dict = get_base_models()
	basic_model = basic_model_dict[ml_model]

	basic_model = get_trained_model(basic_model, training_x_data, training_y_data)
	predicted_y_data = basic_model.predict(test_x_data)

	pred_df = pd.DataFrame()
	pred_df['cobdate_partition'] = pd.to_datetime(dict(year=test_x_data.rec_year, month=test_x_data.rec_month, day=test_x_data.rec_day))
	pred_df['actual_data'] = test_y_data.astype(float)
	pred_df['basic_pred'] = predicted_y_data.astype(float)

	rs_tuned_model = get_full_model(ml_model,rs_tuned_params)
	rs_tuned_model = get_trained_model(rs_tuned_model, training_x_data, training_y_data)
	predicted_y_data = rs_tuned_model.predict(test_x_data)
	pred_df['random_search'] = predicted_y_data.astype(float)

	gs_tuned_model = get_full_model(ml_model, gs_tuned_params)
	gs_tuned_model = get_trained_model(gs_tuned_model, training_x_data, training_y_data)
	predicted_y_data = gs_tuned_model.predict(test_x_data)
	pred_df['grid_search'] = predicted_y_data.astype(float)

	bayes_tuned_model = get_full_model(ml_model, bayes_tuned_params)
	bayes_tuned_model = get_trained_model(bayes_tuned_model, training_x_data, training_y_data)
	predicted_y_data = bayes_tuned_model.predict(test_x_data)
	pred_df['bayes'] = predicted_y_data.astype(float)

	hyper_tuned_model = get_full_model(ml_model, hyper_tuned_params)
	hyper_tuned_model = get_trained_model(hyper_tuned_model, training_x_data, training_y_data)
	predicted_y_data = hyper_tuned_model.predict(test_x_data)
	pred_df['hyperopt'] = predicted_y_data.astype(float)

	optuna_tuned_model = get_full_model(ml_model, optuna_tuned_params)
	optuna_tuned_model = get_trained_model(optuna_tuned_model, training_x_data, training_y_data)
	predicted_y_data = optuna_tuned_model.predict(test_x_data)
	pred_df['optuna'] = predicted_y_data.astype(float)

	print(pred_df)
	print("Types")
	print(pred_df.dtypes)

	data_response = {}

	data_response['data'] = pred_df.to_json(orient="records")
	data_response['basic'] = round(smape(pred_df['actual_data'], pred_df['basic_pred']),2)
	data_response['grid'] = round(smape(pred_df['actual_data'], pred_df['grid_search']),2)
	data_response['random'] = round(smape(pred_df['actual_data'], pred_df['random_search']), 2)
	data_response['bayes'] = round(smape(pred_df['actual_data'], pred_df['bayes']),2)
	data_response['hyperopt'] = round(smape(pred_df['actual_data'], pred_df['hyperopt']),2)
	data_response['optuna'] = round(smape(pred_df['actual_data'], pred_df['optuna']), 2)

	return data_response
