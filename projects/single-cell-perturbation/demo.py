"""Synthetic smoke demo: no competition data, credentials or downloads required."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from baseline_ridge import fit_predict as ridge
from baseline_pca_ridge import fit_predict as pca_ridge, mrrmse
from baseline_MRRMSE_L2 import fit_predict as mrrmse_l2


def make_synthetic(seed=42):
    rng = np.random.default_rng(seed)
    cells, drugs, genes = 4, 12, 24
    cell_effect = rng.normal(0, 0.4, (cells, genes))
    drug_effect = rng.normal(0, 0.7, (drugs, genes))
    rows, targets = [], []
    for c in range(cells):
        for d in range(drugs):
            rows.append({'cell_type': f'cell_{c}', 'sm_name': f'drug_{d}'})
            targets.append(cell_effect[c] + drug_effect[d] + rng.normal(0, 0.05, genes))
    x = pd.DataFrame(rows)
    y = pd.DataFrame(targets, columns=[f'gene_{g:02d}' for g in range(genes)])
    # Hold out combinations from one cell; each held-out drug occurs in other cells.
    held_out = x.cell_type.eq('cell_3') & ~x.sm_name.isin(['drug_0', 'drug_1', 'drug_2'])
    return x.loc[~held_out], y.loc[~held_out], x.loc[held_out], y.loc[held_out]


def main():
    x, y, xv, yv = make_synthetic()
    predictions = {
        'Zero': np.zeros(yv.shape),
        'Gene mean': np.tile(y.mean().to_numpy(), (len(yv), 1)),
        'Ridge': ridge(x, y, xv, alpha=0.1),
        'PCA + Ridge': pca_ridge(x, y, xv, n_components=12, alpha=0.1),
        'MRRMSE + L2': mrrmse_l2(x, y, xv, alpha=0.03),
    }
    scores = {}
    for name, pred in predictions.items():
        values = np.asarray(pred)
        if values.shape != yv.shape or not np.isfinite(values).all():
            raise RuntimeError(f'{name}: invalid output shape or nonfinite prediction')
        scores[name] = round(mrrmse(yv, values), 6)
    result = {
        'data': 'SYNTHETIC ONLY; not biological or competition performance',
        'seed': 42, 'train_pairs': len(x), 'validation_pairs': len(xv),
        'gene_targets': y.shape[1], 'MRRMSE': scores,
    }
    print(json.dumps(result, indent=2))
    (Path(__file__).parent / 'synthetic_results.json').write_text(
        json.dumps(result, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
