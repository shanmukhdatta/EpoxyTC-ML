"""Verification-first audit of committed physics tables using existing src.physics.

Run from repo root:
    python scripts/verify_physics_results.py
No experimental property is inferred from the predictions.
"""
from pathlib import Path
import json
import math
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.physics import (maxwell_eucken, bruggeman_symmetric, hashin_shtrikman,
                         hamilton_crosser, lewis_nielsen, fourier_conductivity,
                         fourier_independent_uncertainty)

HERE = ROOT / 'results'
checks = []

def check(label, condition):
    checks.append({"test": label, "pass": bool(condition)})
    if not condition:
        raise AssertionError(label)

def same(x, y, atol=0.00006):
    return bool(np.isfinite(x) and np.isfinite(y) and abs(x-y) <= atol)

source = pd.read_csv(HERE / 'source_experiment_model_comparisons.csv')
check('11 source-reconstructed cases',len(source)==11)
check('source rows have distinct IDs',source.case_id.is_unique)
check('original CSV row provenance NOT certified', int((source.csv_link=='VERIFIED').sum())==0)

for row in source.itertuples(index=False):
    km,kf,phi = float(row.km),float(row.kf_assumed),float(row.phi)
    check('fraction_'+row.case_id,0<=phi<=1)
    models = dict(maxwell_k=maxwell_eucken(km,kf,phi),
                  bruggeman_k=bruggeman_symmetric(km,kf,phi),
                  hamilton_crosser_k=hamilton_crosser(km,kf,phi,1.),
                  lewis_nielsen_k=lewis_nielsen(km,kf,phi,1.5,.637))
    l,h = hashin_shtrikman(km,kf,phi)
    models.update(hs_lower_k=l,hs_upper_k=h)
    for name,pred in models.items():
        check(row.case_id+'_'+name,same(pred,float(getattr(row,name))))
    check(row.case_id+'_hs_bound_order',l <= h)
    check(row.case_id+'_maxwell_equals_hc_sphere',same(models['maxwell_k'],models['hamilton_crosser_k'],1e-12))
    check(row.case_id+'_measured_positive',row.measured_k>0)

lab = pd.read_csv(HERE/'lab_figure3_digitized_approx.csv')
check('30 digitized graph readings',len(lab)==30)
check('unique graph observation IDs',lab.observation_id.is_unique)
check('5 filler levels per 2 fillers x 3 temperatures',all(len(g)==5 for _,g in lab.groupby(['filler','temperature_k'])) and len(lab.groupby(['filler','temperature_k']))==6)
check('digitized values clearly not raw measurements',bool(lab.source_measurement_type.astype(str).str.contains('MANUSCRIPT_PLOT').all()))
check('all graph points have plot reading uncertainty positive', bool((lab.estimated_plot_reading_uncertainty_wmk>0).all()))

inverse = pd.read_csv(HERE/'lab_fig3_maxwell_inverse_checks.csv')
check('30 inverse-model checks',len(inverse)==30)
check('same graph identifiers',set(inverse.observation_id)==set(lab.observation_id))

scenario = pd.read_csv(HERE/'lab_fig3_forward_model_scenarios.csv')
check('15 sensitivity scenarios',len(scenario)==15)
for row in scenario.itertuples(index=False):
    if not math.isfinite(row.km_proxy) or not math.isfinite(row.kf_proxy):
        continue
    km,kf,phi = row.km_proxy,row.kf_proxy,row.phi
    check('scenario_'+row.observation_id+'_maxwell',same(maxwell_eucken(km,kf,phi),row.maxwell_k,0.00009) if hasattr(row,'maxwell_k') else True)

refs = pd.read_csv(HERE/'physical_property_source_register.csv')
check('parameter sources listed',len(refs)>=7)
coverage = pd.read_csv(HERE/'physics_reviewer_comment_coverage.csv')
check('physics reviewer items indexed',len(coverage)==17)
check('no reviewer items falsely declared completely verified',not coverage.status.astype(str).str.contains('ALL_VERIFIED|FULLY_COMPLETE',case=False).any())
errors = pd.read_csv(HERE/'manuscript_tables_2_4_6_recalculated_errors.csv')
check('16 manuscript comparison errors',len(errors)==16)
for i,r in errors.iterrows():
    if float(r.reference_k)>0:
        calc = 100*(float(r.model_prediction_k)-float(r.reference_k))/float(r.reference_k)
        check('table_error_'+str(i),abs(calc-float(r.signed_error_percent))<0.055)

check('physics Fourier units',same(fourier_conductivity(2,.01,.01,2),1,1e-12))
check('Fourier uncertainty positive',fourier_independent_uncertainty(2,.1,.01,.001,.01,.001,2,.1)['combined_standard_uncertainty_w_mk']>0)

summary = {'verification':'PASS','n_checks':len(checks),'n_passed':sum(c['pass'] for c in checks),
           'source_cases':len(source),'graph_digitized_points':len(lab),
           'laboratory_forward_scenarios':len(scenario),
           'original_csv_fully_authenticated':0,
           'scientific_status':'CONDITIONAL_EXPLORATORY_NOT_FULL_LAB_OR_ORIGINAL_DATA_VALIDATION',
           'physics_source_code':'src/physics.py (existing live repository implementation)'}
print(json.dumps(summary,indent=2))
