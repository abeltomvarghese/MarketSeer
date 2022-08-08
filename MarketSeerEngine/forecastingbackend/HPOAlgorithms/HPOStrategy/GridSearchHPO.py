from forecastingbackend.HPOAlgorithms.HPOStrategy.HPOStrategy import HPOStrategy
from forecastingbackend.MLModels.ModelConcreteBuilders.base_model_generator import get_base_models

from sklearn.model_selection import TimeSeriesSplit
from sklearn import model_selection


import numpy as np

class GridSearchHPO(HPOStrategy):
	def __init__(self):
		self.parameter_dict = {}


		mlp_model = {}
		mlp_model['hidden_layer_sizes'] = [(5,5),(10,10),(15,15),(20,20)]
		mlp_model['activation'] = ['identity', 'logistic', 'tanh', 'relu']
		mlp_model['learning_rate'] = ['constant', 'invscaling', 'adaptive']
		mlp_model['solver'] = ['lbfgs', 'sgd', 'adam']

		knn_model = {}
		knn_model['leaf_size'] = np.arange(30,400,1)
		knn_model['p'] = [1,2]
		knn_model['n_neighbors'] = [1,2,3,4,5]

		self.parameter_dict['MLP'] = mlp_model
		self.parameter_dict['KNN'] = knn_model


	def get_parameters_to_tune(self, model_type):
		return self.parameter_dict[model_type]


	def get_tuned_parameters(self, model_type, x_data, y_data):
		model_dict = get_base_models()

		current_model = model_dict[model_type]
		param_grid = self.get_parameters_to_tune(model_type)

		tuning_prototype = model_selection.GridSearchCV(
			estimator=current_model,
			param_grid=param_grid,
			scoring='neg_mean_absolute_percentage_error',
			verbose=1,
			n_jobs=1,
			cv=TimeSeriesSplit(n_splits=6).split(x_data)
		)

		tuning_prototype.fit(x_data, y_data)

		return tuning_prototype.best_estimator_.get_params()
