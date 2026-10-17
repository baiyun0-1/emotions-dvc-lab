import numpy as np
import pandas as pd
from pathlib import Path

# 固定随机种子，保证每次生成的数据一模一样（可复现）
np.random.seed(42)

# 20 个点，规律：value ≈ 2*id + 1，再加一点 ±1 的小噪声
ids = np.arange(1, 21)
true_value = 2 * ids + 1
noise = np.random.normal(0, 1, size=len(ids))

out = Path("data")
out.mkdir(exist_ok=True)

# ---- v2: 干净数据 ----
df_v2 = pd.DataFrame({"id": ids, "value": true_value + noise})
df_v2.to_csv(out / "sample.csv", index=False)
print("v2 (clean) written:", len(df_v2), "rows")

# ---- v3: 脏数据（故意塞 3 个异常值）----
df_v3 = df_v2.copy()
df_v3.loc[4, "value"] = 100    # 第5行（索引4）改成100
df_v3.loc[9, "value"] = -50    # 第10行改成-50
df_v3.loc[14, "value"] = 200   # 第15行改成200
df_v3.to_csv(out / "sample_v3.csv", index=False)
print("v3 (dirty) written:", len(df_v3), "rows")

# ---- v4: 清洗后的数据（把异常值改回正常值）----
df_v4 = df_v2.copy()  # 直接用干净版，演示"洗干净"的结果
df_v4.to_csv(out / "sample_v4.csv", index=False)
print("v4 (cleaned) written:", len(df_v4), "rows")
