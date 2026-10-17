# MLflow Experiments Summary

Two experiment runs have been tracked with MLflow:
1. **baseline_exp**: Baseline reference run, max_iter = 100.
   - MSE = 0.0556
2. **improved_exp**: Tuned demo run, max_iter = 150.
   - MSE = 0.0556

Every run logs these required items:
- Git commit SHA (code version)
- DVC pointer hash (dataset version reference)
- All hyper-parameters from yaml config
- Evaluation metric: MSE (mean squared error)
- Model artifact (trained model file)

All MLflow artifacts and run history are stored locally inside `./mlruns`.

> Note: This is a toy dataset for demonstrating MLOps workflow, not a high-performance real-world model.

---

# 更新：4 run 对比实验（Ridge + train/test split）

为了让实验对比有意义，改用 **Ridge 回归**，并做了真正的 80/20 train/test split。
MLflow 后端改为 SQLite 数据库，启动网页版查看：

```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db
