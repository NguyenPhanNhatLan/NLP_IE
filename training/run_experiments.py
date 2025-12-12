import numpy as np
from sklearn.linear_model import LogisticRegression
import mlflow

from app.core.config import settings
from training.mlops.mlflows_utils import init_mlflow
from training.evaluation.metrics import compute_metrics

def main():
    init_mlflow(settings.mlflow_tracking_uri, "default")


    np.random.seed(42)
    X_train = np.random.randn(100, 64)
    y_train = np.random.choice([0,1,2,3,4], size=100)
    X_test  = np.random.randn(30, 64)
    y_test  = np.random.choice([0,1,2,3,4], size=30)

    # 3) baseline model
    with mlflow.start_run(run_name="baseline_lr_dummy"):
        mlflow.log_param("model", "LogisticRegression")
        mlflow.log_param("features", "dummy_64d")

        clf = LogisticRegression(max_iter=200)
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)

        metrics = compute_metrics(y_test, y_pred)
        for k,v in metrics.items():
            mlflow.log_metric(k, v)

        print("Logged to MLflow:", metrics)

main()
