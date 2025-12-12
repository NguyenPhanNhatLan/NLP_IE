import mlflow

def init_mlflow(tracking_uri: str, experiment_name: str):
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)
