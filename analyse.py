"""Recreate the November–May storage audit and Model 3 benchmarks."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

root = Path(__file__).resolve().parent
data = pd.read_csv(root / "ukai_dry_season.csv").set_index("month")
assert list(data.index) == "Oct Nov Dec Jan Feb Mar Apr May".split()
dry = data.iloc[1:].copy()
assert dry.notna().all().all()
dry["release_mcm"] = dry.ulbmc_release_mcm + dry.downstream_release_mcm
dry["budget_drawdown_mcm"] = dry.release_mcm + dry.evaporation_mcm - dry.inflow_mcm
dry["storage_drawdown_mcm"] = -data.end_storage_mcm.diff()
dry["residual_mcm"] = dry.storage_drawdown_mcm - dry.budget_drawdown_mcm
dry.to_csv(root / "monthly_audit.csv", float_format="%.3f")
print(dry.round(2).to_string())
print(dry.drop(columns="end_storage_mcm").sum().round(2))
print("Storage fraction of releases plus evaporation:", dry.storage_drawdown_mcm.sum() / (dry.release_mcm + dry.evaporation_mcm).sum())

bench = pd.read_csv(root / "model3.csv").set_index("algorithm")
bench["rms_mcm_per_canal_month"] = (bench.squared_deficiency_mcm2 / 36) ** 0.5
bench.to_csv(root / "model3_derived.csv", float_format="%.4f")
print(bench)
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})
fig, ax = plt.subplots(figsize=(8, 4.8))
ax.bar(dry.index, dry.release_mcm, color="#24677a", label="Controlled releases")
ax.bar(dry.index, dry.evaporation_mcm, bottom=dry.release_mcm, color="#d8aa63", label="Evaporation")
ax.plot(dry.index, dry.storage_drawdown_mcm, "o-", color="#822d42", label="Drawdown from storage endpoints")
ax.plot(dry.index, dry.inflow_mcm, "s--", color="#36854f", label="Inflow")
ax.set(ylabel="Monthly volume (million m³)", xlabel="Month in average-inflow operating year", ylim=(0,620))
ax.set_title("Figure 1. How Ukai supplied dry-season releases",loc="left")
ax.legend(ncol=2, fontsize=9, loc="center left", bbox_to_anchor=(0,0.36))
fig.text(.09,.02,"Calculated from Shiyekar et al. (2016), Table 2. Releases combine ULBMC and downstream outlets.",fontsize=9)
fig.tight_layout(rect=(0,.05,1,1))
fig.savefig(root / "Figure_1.png", dpi=220)
plt.close(fig)
fig, axes = plt.subplots(1,2,figsize=(9,3.6))
for ax, field, label in zip(axes, ["energy_million_kwh", "rms_mcm_per_canal_month"], ["Annual generation (million kWh)","RMS mismatch (MCM per canal-month)"]):
    bars = ax.barh(bench.index,bench[field],color=["#24677a","#78919a","#b07536"])
    ax.invert_yaxis()
    ax.bar_label(bars, fmt="%.2f", padding=3)
    ax.set_xlim(0,bench[field].max()*1.24)
    ax.set_xlabel(label, fontsize=10)
fig.suptitle("Figure 2. Energy and irrigation performance under Model 3")
fig.text(.06,.025,"Table 6 extrema plotted separately. RMS calculated from the squared-deficiency objective.",fontsize=9)
fig.tight_layout(rect=(0,.08,1,.94))
fig.savefig(root / "Figure_2.png", dpi=220)
