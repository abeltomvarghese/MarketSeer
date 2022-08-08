from forecastingbackend.MLModels.ModelConcreteBuilders import MLPBuilder
from forecastingbackend.MLModels.ModelConcreteBuilders import KNNBuilder
from forecastingbackend.MLModels.ModelConcreteBuilders import SVRBuilder




def get_base_models():
	mlp_model = MLPBuilder.MLPBuilder()
	knn_model = KNNBuilder.KNNBuilder()
	svr_model = SVRBuilder.SVRBuilder()

	ml_models = {}
	ml_models['MLP'] = mlp_model.release_model
	ml_models['KNN'] = knn_model.release_model
	ml_models['SVR'] = svr_model.release_model

	return ml_models

def get_full_model(model_type, param_dict):

	mlp_model = MLPBuilder.MLPBuilder()
	knn_model = KNNBuilder.KNNBuilder()

	relevant_model = None

	if model_type == 'MLP':
		relevant_model = mlp_model.build_model(param_dict)
	elif model_type == 'KNN':
		relevant_model = knn_model.build_model(param_dict)

	return relevant_model