# 运行验证记录

## 环境

Python 3.12.14；NumPy 2.3.5；pandas 2.2.3；SciPy 1.17.0；scikit-learn 1.8.0；threadpoolctl 3.6.0。

## 已实际执行

| 命令 | 结果 |
| --- | --- |
| `python projects/doctor-hospital-matching/assignment.py` | 成功；20 人全部分配，Hungarian 总成本 30，随机贪心 1,000 次平均成本 37.699 |
| `python projects/single-cell-perturbation/demo.py` | 成功；39 训练组合、9 验证组合、24 靶标；5 种方法输出维度正确且均为有限值 |
| `python -m unittest discover -s tests -v` | 6 项检查通过 |

测试覆盖：示例容量可行性、60 个小型随机成本矩阵与穷举最优解的对照、容量不足输入、重复偏好输入、MRRMSE 定义、未知类别预测的维度与标签一致性。

## 未在本次重跑

- 614 × 18,211 原始单细胞目标上的完整训练与验证。README 中对应分数属于源 Notebook 保存的结果，不属于本次执行记录。
- 官方竞赛测试评分、未见药物独立测试、临床测试。
- 青光眼 proposal 的训练与复核策略实验。

## 合成数据的解释边界

单细胞模拟数据采用简单的细胞效应、药物效应与噪声叠加，因此特别适合加性模型。其分数用于检查代码可运行，不支持对真实数据模型优劣作结论。
