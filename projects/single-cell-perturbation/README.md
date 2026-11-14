# 单细胞药物扰动响应预测

**Single-cell perturbation response prediction | Python · PCA · Multi-output regression**

[返回作品集](../../README.md) · [合成数据演示](demo.py) · [数据说明](DATA.md)

## 做了什么

围绕药物干预后的细胞基因差异表达（DE）响应，研究如何从已有药物—细胞组合预测未观测组合的响应。源工作流读取 **614 个有标签组合、18,211 个基因靶标**，另有 **255 个官方测试组合**。这里的 614 指组合级 DE 行，不是单细胞数。

项目属于 JHU Biomedical Data Design 团队课程实践。当前展示重点是正向响应预测和评价流程，不把逆向分子设计或新药发现写成已完成工作。

## 本人贡献

- 参与项目方向讨论与文献整合，围绕可用数据、预测目标和评价标准形成分析任务。
- 承担数据清洗、统计分析和 PCA 相关工作，参与模型代码撰写与误差分析。
- 参与团队任务协作、成果展示和英文汇报，将模型输出整理为可解释的比较。

以上是本人参与范围，整个项目为团队共同完成。本页附带的是仓库中精选的基线与划分模块，不将所有团队模型都归为个人独立成果。

## 怎么做

### 1. 明确输入和输出

当前精选基线使用 `cell_type` 与 `sm_name` 两个类别特征，经 one-hot 编码后预测基因 DE 向量。它们没有直接输入分子结构或单细胞原始表达矩阵。

### 2. 比较基线与目标降维

| 文件 | 实现内容 |
| --- | --- |
| [baseline_ridge.py](baseline_ridge.py) | 直接在基因空间进行多输出 Ridge 回归 |
| [baseline_pca_ridge.py](baseline_pca_ridge.py) | 仅在训练标签上拟合 PCA，预测主成分后还原到基因空间；包含 MRRMSE 评价 |
| [baseline_MRRMSE_L2.py](baseline_MRRMSE_L2.py) | 使用迭代加权最小二乘拟合平均行 RMSE 与 L2 惩罚；截距不惩罚 |
| [split_data.py](split_data.py) | 按稀疏目标细胞构建四折划分，导出配对清单并检查靶标列 |

类别编码与 PCA 都只从训练数据拟合。未知类别可被编码处理，但“程序能预测”不等于“具备可靠的未见药物泛化能力”。

### 3. 按稀疏目标细胞验证

源工作流分别以 NK、CD4+ T、CD8+ T 和 T regulatory cells 为目标细胞。在目标细胞中保留控制样本与锚定药物，留出其他非控制药物—细胞组合。验证集药物仍可出现在其他细胞的训练样本中。

| 目标细胞 | 训练组合 | 目标细胞非控制锚定组合 | 验证组合 |
| --- | ---: | ---: | ---: |
| NK cells | 485 | 15 | 129 |
| T cells CD4+ | 485 | 15 | 129 |
| T cells CD8+ | 487 | 13 | 127 |
| T regulatory cells | 485 | 15 | 129 |

因此这项评价测试的是**已见药物在稀疏细胞背景下的组合补全**，不是所有药物均从训练中移除的“未见药物”测试。

评价指标 MRRMSE 先对每个组合的全部基因计算 RMSE，再对组合取均值；表中的四折结果为各折分数的算术平均，越低越好。

## 结果如何

### 源 Notebook 保存的本地验证记录

以下数字来自 [固定版本的 Model_workflow.ipynb](https://github.com/hallenfan222/Biomedical-Data-Design/blob/695eafb8d4eb9dbdb40be7516db741115beb33a8/Singlecell_perturbations/Model_workflow.ipynb)。本次整理核对了代码与保存输出，**没有重新下载原始数据并重跑这套全量实验**。它们不是官方测试集分数、排行榜结果或临床效果。

| 方法 | 四折平均 MRRMSE | 该次工作流参数 |
| --- | ---: | --- |
| Zero | 1.005772 | 全零预测 |
| Gene mean | 1.106285 | 训练基因均值 |
| Ridge | 1.106340 | alpha = 100000 |
| PCA + Ridge | 1.106340 | n_components = 200；alpha = 100000 |
| MRRMSE + L2 | 0.974028 | alpha = 0.03 |

该记录说明调整损失函数与正则化值得进一步分析；也显示强正则下 Ridge 与均值预测接近。尚不能据此宣布最终模型胜出：需要独立测试、参数选择记录和分细胞误差分析支持更强的结论。

### 本次独立运行的合成数据演示

`demo.py` 生成 4 个虚构细胞类别 × 12 个虚构药物、24 个靶标；固定种子 42，使用 39 组训练、9 组验证。数据来自简单加性效应加噪声，不模拟真实复杂生物机制。

```bash
python -m pip install -r requirements.txt
python projects/single-cell-perturbation/demo.py
```

程序运行 Zero、Gene mean、Ridge、PCA + Ridge、MRRMSE + L2，检查输出维度与有限值，并保存 [synthetic_results.json](synthetic_results.json)。这些数值仅证明演示流程可运行，不能与上表真实数据的验证分数比较。

## 局限与后续工作

- 类别特征不包含化学结构或细胞机制信息；未见药物不会拥有训练得到的药物效应。
- 稀疏细胞验证与真正未见药物验证回答不同问题，需要分开报告。
- 全量数据与团队完整模型不在这个精简副本中；本页没有复制大体积提交文件。
- 后续应在一致划分上比较模型、记录参数选择、分析不同细胞与响应幅度的误差，并以独立测试验证。新分子生成仍属于进一步探索方向。

**English summary.** A team course project predicts gene-level DE responses for cell–drug pairs. My contributions include data cleaning, statistics, PCA, model/error analysis and presentation. Selected modules cover categorical baselines and sparse-cell validation. Recorded notebook scores and freshly executed synthetic-demo scores are labeled separately; unseen-drug generalization and final test performance are not claimed.
