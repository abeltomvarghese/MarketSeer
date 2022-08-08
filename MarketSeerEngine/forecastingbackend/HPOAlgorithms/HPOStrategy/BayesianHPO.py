from forecastingbackend.HPOAlgorithms.HPOStrategy.HPOStrategy import HPOStrategy
from forecastingbackend.MLModels.ModelConcreteBuilders.base_model_generator import get_base_models, get_full_model
import numpy as np

from sklearn.model_selection import TimeSeriesSplit
from sklearn import ensemble
from sklearn import metrics

from functools import partial
from skopt import space
from skopt import gp_minimize


class BayesianHPO(HPOStrategy):

	def __init__(self):
		self.parameter_dict = {}
		self.current_model = None

		mlp_model = {}
		mlp_model['first_layer_neuron'] = space.Integer(5,20, name="first_layer_neuron")
		mlp_model['second_layer_neuron'] = space.Integer(5, 20, name="second_layer_neuron")
		mlp_model['activation'] = space.Categorical(['identity', 'logistic', 'tanh', 'relu'], name='activation')
		mlp_model['learning_rate'] = space.Categorical(['constant', 'invscaling', 'adaptive'], name='learning_rate')
		mlp_model['solver'] = space.Categorical(['lbfgs', 'sgd', 'adam'], name='solver')
		self.parameter_dict['MLP'] = mlp_model

		knn_model = {}
		knn_model['leaf_size'] = space.Integer(30,400, name='leaf_size')
		knn_model['p'] = space.Integer(1,2, name='p')
		knn_model['n_neighbors'] = space.Integer(1,5, name='n_neighbors')
		self.parameter_dict['KNN'] = knn_model


	def get_parameters_to_tune(self, model_type):
		model_dict = self.parameter_dict[model_type]
		param_space = []

		self.current_model = model_type

		for each_key in model_dict:
			param_space.append(model_dict[each_key])

		return param_space

	def bayesian_optimize(self, params, param_names, x_data, y_data):
		params = dict(zip(param_names, params))

		if self.current_model == 'MLP':
			first_layer_neurons = params['first_layer_neuron']
			second_layer_neurons = params['second_layer_neuron']

			params['hidden_layer_sizes'] = (first_layer_neurons,second_layer_neurons)
			params.pop('first_layer_neuron')
			params.pop('second_layer_neuron')

		model = get_full_model(model_type=self.current_model, param_dict=params)

		cv_folds = TimeSeriesSplit(n_splits=6)
		accuracies = []

		for train_index, test_index in cv_folds.split(X=x_data):

			# xtrain, xtest = x_data[train_index], x_data[test_index]
			# ytrain, ytest = y_data[train_index], y_data[test_index]

			# xtrain, xtest = x_data.iloc[[train_index]], x_data.iloc[[test_index]]
			# ytrain, ytest = y_data.iloc[[train_index]], y_data.iloc[[test_index]]

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


		param_space = self.get_parameters_to_tune(model_type)

		param_names = []

		if model_type == 'KNN':
			param_names = ['leaf_size', 'p', 'n_neighbors']
		elif model_type == 'MLP':
			param_names = ['first_layer_neuron', 'second_layer_neuron', 'activation', 'learning_rate', 'solver']

		optimization_function = partial(self.bayesian_optimize, param_names=param_names, x_data=x_data, y_data=y_data)

		result = gp_minimize(optimization_function, dimensions=param_space, n_calls=10, n_random_starts=10, verbose=1)

		param_dict = dict(zip(param_names, result.x))

		if model_type == 'MLP':
			mlp_params = {}
			mlp_params['hidden_layer_sizes'] = (param_dict['first_layer_neuron'], param_dict['second_layer_neuron'])
			mlp_params['activation'] = param_dict['activation']
			mlp_params['learning_rate'] = param_dict['learning_rate']
			mlp_params['solver'] = param_dict['solver']
			param_dict = mlp_params


		return param_dict