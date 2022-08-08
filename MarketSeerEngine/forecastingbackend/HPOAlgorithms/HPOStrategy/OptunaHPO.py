from forecastingbackend.HPOAlgorithms.HPOStrategy.HPOStrategy import HPOStrategy
from forecastingbackend.MLModels.ModelConcreteBuilders.base_model_generator import get_base_models, get_full_model

import pandas as pd
import numpy as np
from functools import partial

import optuna

from sklearn.model_selection import TimeSeriesSplit
from sklearn import ensemble
from sklearn import metrics
from sklearn import model_selection

class OptunaHPO(HPOStrategy):
	def __init__(self):
		self.parameter_dict = {}
		self.current_model = None


	def get_parameters_to_tune(self, model_type):
		self.current_model = model_type
		return self.current_model

	def optuna_optimize(self, trial, x_data, y_data):

		mlp_model = {}
		mlp_model['first_layer_neuron'] = trial.suggest_int(name="first_layer_neuron", low=5, high=20, step=1)
		mlp_model['second_layer_neuron'] = trial.suggest_int(name="second_layer_neuron", low=5, high=20, step=1)
		mlp_model['activation'] = trial.suggest_categorical(name='activation',
																	choices=['identity', 'logistic', 'tanh', 'relu'])
		mlp_model['learning_rate'] = trial.suggest_categorical(name='learning_rate',
																	   choices=['constant', 'invscaling', 'adaptive'])
		mlp_model['solver'] = trial.suggest_categorical(name='solver', choices=['lbfgs', 'sgd', 'adam'])
		self.parameter_dict['MLP'] = mlp_model

		knn_model = {}
		knn_model['leaf_size'] = trial.suggest_int(name="leaf_size", low=30, high=400, step=1)
		knn_model['p'] = trial.suggest_int(name="p", low=1, high=2, step=1)
		knn_model['n_neighbors'] = trial.suggest_int(name="n_neighbors", low=1, high=5, step=1)
		self.parameter_dict['KNN'] = knn_model

		params = self.parameter_dict[self.current_model]


		if self.current_model == 'MLP':
			first_layer_neurons = params['first_layer_neuron']
			second_layer_neurons = params['second_layer_neuron']

			params['hidden_layer_sizes'] = (first_layer_neurons, second_layer_neurons)
			params.pop('first_layer_neuron')
			params.pop('second_layer_neuron')

		model = get_full_model(model_type=self.current_model, param_dict=params)
		cv_folds = TimeSeriesSplit(n_splits=6)
		accuracies = []

		for train_index, test_index in cv_folds.split(X=x_data):
			xtrain = x_data.iloc[train_index]
			xtest = x_data.iloc[test_index]
			ytrain = y_data.iloc[train_index]
			ytest = y_data.iloc[test_index]

			model.fit(xtrain, ytrain)
			predictions = model.predict(xtest)

			fold_acc = metrics.mean_absolute_percentage_error(ytest, predictions)
			accuracies.append(fold_acc)

		return -1.0 * np.mean(accuracies)

	def get_tuned_parameters(self, model_type, x_data, y_data):

		model_type = self.get_parameters_to_tune(model_type)

		optimization_function = partial(self.optuna_optimize, x_data=x_data, y_data=y_data)

		study = optuna.create_study(sampler=optuna.samplers.TPESampler(multivariate=True))
		study.optimize(optimization_function, n_trials=15)
		param_dict = study.best_params


		if model_type == 'MLP':
			mlp_param_dict = {}
			mlp_param_dict['hidden_layer_sizes'] = (param_dict['first_layer_neuron'], param_dict['second_layer_neuron'])
			mlp_param_dict['activation'] = param_dict['activation']
			mlp_param_dict['learning_rate'] = param_dict['learning_rate']
			mlp_param_dict['solver'] = param_dict['solver']
			param_dict = mlp_param_dict

		return param_dict