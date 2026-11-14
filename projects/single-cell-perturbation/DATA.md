# 数据与复现范围

- 原项目数据来源：Open Problems – Single-Cell Perturbations。源工作流读取 `de_train.parquet`、`id_map.csv`、`sample_submission.csv`。
- 本展示仓库不打包原始数据、真实配对清单或提交预测文件。使用原数据时应从提供方获取，并遵守其访问与使用条件。
- `demo.py` 完全本地生成模拟数据，不联网、不需要账号。虚构标识为 `cell_0`、`drug_0`、`gene_00` 等。
- `split_data.py` 是保留的原始划分模块，针对原项目六类细胞与锚定药物结构设计；**不要直接把它用于本演示的小型合成数据**。`demo.py` 内有单独的模拟划分逻辑。
- 原规模、划分与数据文件名可追溯至 [源工作流](https://github.com/hallenfan222/Biomedical-Data-Design/blob/695eafb8d4eb9dbdb40be7516db741115beb33a8/Singlecell_perturbations/Model_workflow.ipynb)。
