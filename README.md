# Ukai Reservoir – data and reproducible analysis

Run from any working directory with Python 3 and pandas and matplotlib installed:

    python analyse.py

Inputs are small transcriptions of published numerical results. ukai_dry_season.csv contains the two release columns, evaporation, inflow, and month-end storage from Shiyekar, Katdare and Patil (2016), Table 2, printed p. 385, https://www.ijraset.com/fileserve.php?FID=6013 . October supplies opening storage only. Blank October fluxes mean unused, not zero. November to May have zero reported overflow. The rows represent a modelled mean-inflow schedule. Model inputs and storage endpoints are transcribed independently at published precision.

model3.csv records the annual extrema in Kumar and Yadav (2022), Table 6, https://doi.org/10.2166/ws.2021.374 . Energy is in million kWh. Squared deficiency is in (million cubic metres) squared. The rows have no run identifiers. The RMS denominator is 3 canals times 12 months. Derived outputs are monthly_audit.csv, model3_derived.csv and both numbered PNG figures. The script prints seasonal totals and the storage fraction as a decimal. No historical operating record or optimizer implementation is included.
