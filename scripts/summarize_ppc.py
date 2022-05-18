import os
import sys

import pandas as pd

args = sys.argv
assert len(args) == 2, "summarize_ppc.py <target results>"

ppc_file_path = os.path.join("results", args[1], "PostgresPlanCost.csv")
ppc_df = pd.read_csv(ppc_file_path)
cost_percentiles = ppc_df["cost"].quantile([0.5, 0.9, 0.95, 0.99, 1.0])
print(", ".join([f"{cost:.03f}" for cost in cost_percentiles]))
