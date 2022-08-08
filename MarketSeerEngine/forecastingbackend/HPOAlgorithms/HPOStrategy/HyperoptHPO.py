from forecastingbackend.HPOAlgorithms.HPOStrategy.HPOStrategy import HPOStrategy
from forecastingbackend.MLModels.ModelConcreteBuilders.base_model_generator import get_base_models, get_full_model

from sklearn.model_selection import TimeSeriesSplit
from sklearn import metrics
from functools import partial
import numpy as np

from hyperopt import hp, fmin, tpe, Trials
from hyperopt.pyll.base import scope


class HyperoptHPO(HPOStrategy):

	def __init__(self):
		self.parameter_dict = {}
		self.current_model = None

		mlp_model = {}
		mlp_model['first_layer_neuron'] = scope.int(hp.quniform('first_layer_neuron', 5,20,1))
		mlp_model['second_layer_neuron'] = scope.int(hp.quniform('second_layer_neuron', 5, 20, 1))
		mlp_model['activation'] = hp.choice('activation', ['identity', 'logistic', 'tanh', 'relu'])
		mlp_model['learning_rate'] = hp.choice('learning_rate', ['constant', 'invscaling', 'adaptive'])
		mlp_model['solver'] = hp.choice('solver', ['lbfgs', 'sgd', 'adam'])
		self.parameter_dict['MLP'] = mlp_model

		knn_model = {}
		knn_model['leaf_size'] = scope.int(hp.quniform('leaf_size', 30,400,1))
		knn_model['p'] = scope.int(hp.quniform('p',1,2,1))
		knn_model['n_neighbors'] = scope.int(hp.quniform('n_neighbors', 1,5,1))
		self.parameter_dict['KNN'] = knn_model

	def get_parameters_to_tune(self, model_type):
		self.current_model = model_type
		return self.parameter_dict[model_type]

	def hyperopt_optimize(self, params, x_data, y_data):
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

		param_space = self.get_parameters_to_tune(model_type)

		optimization_function = partial(self.hyperopt_optimize, x_data=x_data, y_data=y_data)

		trials = Trials()

		result = fmin(optimization_function, space=param_space, algo=tpe.suggest, max_evals=15, trials=trials)

		# DO ALL EDITING FOR HYPEROPT PARAMETER DICT HERE!!!

		tuned_params = {}

		if model_type == 'MLP':
			mlp_activation = ['identity', 'logistic', 'tanh', 'relu']
			mlp_learning = ['constant', 'invscaling', 'adaptive']
			mlp_solver = ['lbfgs', 'sgd', 'adam']
			tuned_params['hidden_layer_sizes'] = (int(result['first_layer_neuron']), int(result['second_layer_neuron']))
			tuned_params['activation'] = mlp_activation[int(result['activation'])]
			tuned_params['learning_rate'] = mlp_learning[int(result['learning_rate'])]
			tuned_params['solver'] = mlp_solver[int(result['solver'])]
		elif model_type == 'KNN':
			tuned_params['leaf_size'] = int(result['leaf_size'])
			tuned_params['p'] = int(result['p'])
			tuned_params['n_neighbors'] = int(result['n_neighbors'])

		return tuned_params