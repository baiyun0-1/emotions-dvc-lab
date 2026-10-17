\# Dataset Version Information

> Note: MS Azure storage account is NOT used in this project, to avoid unexpected cloud charges.

> DVC local cache `.dvc/cache` is used to demonstrate full data‑versioning workflow.

> Raw dataset is never pushed to GitHub; only `.dvc` pointer files are tracked by Git.



\## Dataset

Small toy CSV for workflow demo: columns id, value

\- v1 (git tag: v1): value=3

\- v2 (git tag: v2): value=4



Recover each version:

```bash

git checkout v1

dvc checkout



git checkout v2

dvc checkout

# Dataset Version Information

DVC 本地缓存 `.dvc/cache` 用于演示完整的数据版本管理流程。
原始数据不提交到 GitHub，Git 只跟踪 `.dvc` 指针文件。

## Dataset 说明

玩具数据集，两列：`id`（1~20）、`value`（目标值）。
真实规律为 `value ≈ 2*id + 1`，叠加 ±1 的高斯噪声。

## 版本演进

| 版本 | 说明 | 生成方式 |
|---|---|---|
| v1 | 最初的 3 行 toy 数据（旧版，已废弃） | 手填 |
| v2 | 干净的 20 行数据，value = 2*id+1 + 噪声 | `python ml/generate_data.py` |
| v3 | 在 v2 基础上，把第 5/10/15 行的 value 改成异常值（100 / -50 / 200），模拟脏数据 | 同左脚本自动生成 |
| v4 | 清洗掉异常值后的数据（等同 v2 的干净版） | 同左脚本自动生成 |

## v2 → v3 → v4 变化

- v2 → v3：人为注入 3 个异常值（outlier），测试数据质量对模型的影响
- v3 → v4：移除异常值，数据恢复干净状态

## 恢复某个版本

```bash
git checkout <tag>
dvc checkout
