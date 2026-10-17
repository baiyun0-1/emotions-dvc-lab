
import subprocess
import hashlib
import joblib
import mlflow
import yaml
import argparse
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from ml.data_pipeline import load_raw_dataset, split_features_label

def get_git_head_sha():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    except Exception:
        return "no-git"

def get_dvc_file_hash():
    try:
        with open("data.dvc", "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()[:10]
    except Exception:
        return "no-dvc"

def run_training(config_path, data_path):
    cfg = yaml.safe_load(open(config_path, "r", encoding="utf8"))
    mlflow.set_tracking_uri("sqlite:///mlflow.db")#把实验记录到这个网址去
    mlflow.set_experiment("emotions_mlops")

    df = load_raw_dataset(data_path)
    X, y = split_features_label(df)

    # 80% 训练 / 20% 测试，固定 random_state 保证可复现
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    with mlflow.start_run(run_name=cfg["run_name"]):
        mlflow.log_param("git_commit_sha", get_git_head_sha())
        mlflow.log_param("dvc_pointer_hash", get_dvc_file_hash())
        mlflow.log_param("data_file", str(data_path))
        mlflow.log_params(cfg)

        # Ridge 回归，alpha 是真正起作用的正则化强度
        model = Ridge(alpha=cfg["alpha"])
        model.fit(X_train, y_train)

        # 训练集和测试集都算指标，重点看测试集
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)

        train_mse = mean_squared_error(y_train, y_train_pred)
        test_mse = mean_squared_error(y_test, y_test_pred)
        test_mae = mean_absolute_error(y_test, y_test_pred)
        test_r2 = r2_score(y_test, y_test_pred)

        mlflow.log_metric("train_mse", round(train_mse, 4))
        mlflow.log_metric("test_mse", round(test_mse, 4))
        mlflow.log_metric("test_mae", round(test_mae, 4))
        mlflow.log_metric("test_r2", round(test_r2, 4))

        joblib.dump(model, "temp_model.joblib")
        mlflow.log_artifact("temp_model.joblib")
        joblib.dump(model, "ml/registry/model.joblib")

        print(f"Trained on: {data_path}")
        print(f"  train_mse={train_mse:.4f}  test_mse={test_mse:.4f}")
        print(f"  test_mae={test_mae:.4f}   test_r2={test_r2:.4f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--data", default="data/sample.csv")
    args = parser.parse_args()
    run_training(args.config, args.data)
