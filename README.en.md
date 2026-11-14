# Biomedical & Digital Health Portfolio

**Zihan Fan | M.S.E. student, Biomedical Engineering, Johns Hopkins University**

[中文主页](README.md) · [GitHub profile](https://github.com/hallenfan222)

Selected course and team projects connecting biomedical problem formulation, Python implementation, model evaluation and presentation. Project pages distinguish my contributions from team scope and separate measured results from proposed work.

| Project | Focus | Evidence and status |
| --- | --- | --- |
| [Single-cell perturbation prediction](projects/single-cell-perturbation) | Data processing, PCA, categorical baselines and evaluation of gene-level responses | Selected code and synthetic demo; source notebook contains local validation results; final test outcome is not claimed |
| [Doctor–hospital assignment](projects/doctor-hospital-matching) | Capacity-constrained allocation using ranked preferences | Runnable Python demo; 20 doctors / 6 hospitals; comparison against 1,000 randomized greedy trials |
| [Eye Sentinel: glaucoma screening review](projects/glaucoma-review) | Comparing review strategies under a fixed 10% manual-review budget | Proposal overview and evaluation plan; no completed clinical outcome claimed |

## Run the demos

Python 3.12 was used for verification. The assignment demo needs only the standard library.

```bash
python projects/doctor-hospital-matching/assignment.py
python -m pip install -r requirements.txt
python projects/single-cell-perturbation/demo.py
python -m unittest discover -s tests -v
```

The synthetic examples run without credentials or external datasets. Synthetic scores demonstrate executable workflows, not biological performance. See [validation](VALIDATION.md) and [provenance](PROVENANCE.md) for the scope of the checks and source files.

Course repositories remain separate. This portfolio does not redistribute raw competition data, teaching materials or restricted research content, and does not grant a new license to upstream materials.
