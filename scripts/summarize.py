import os
import sys

import pandas as pd

args = sys.argv
assert len(args) == 2, "summarize_ppc.py <target results>"

# pg cost plan
ppc_file_path = os.path.join("results", args[1], "PostgresPlanCost.csv")
ppc_df = pd.read_csv(ppc_file_path)
cost_percentiles = ppc_df["cost"].quantile([0.5, 0.9, 0.95, 0.99, 1.0])
print("ppc: ", end="")
print(", ".join([f"{cost:.03f}" for cost in cost_percentiles]), end=", ")
print(ppc_df["cost"].mean())

# p-err
true_ppc_file_path = os.path.join("results", "True", "PostgresPlanCost.csv")
if os.path.exists(true_ppc_file_path):
    true_ppc_df = pd.read_csv(true_ppc_file_path)
    p_errs = ppc_df.sort_values("qname").reset_index(drop=True)["cost"] / true_ppc_df.sort_values("qname").reset_index(drop=True)["cost"]
    assert p_errs.min() >= 1.0, p_errs.min()
    p_err_percentiles = p_errs.quantile([0.5, 0.9, 0.95, 0.99, 1.0])
    print("p-err: ", end="")
    print(", ".join([f"{p_err:.03f}" for p_err in p_err_percentiles]))

# simple cost plan
splan_file_path = os.path.join("results", args[1], "SimplePlanCost.csv")
splan_df = pd.read_csv(splan_file_path)
splan_percentiles = splan_df["errors"].quantile([0.5, 0.9, 0.95, 0.99, 1.0])
print("splan: ", end="")
print(", ".join([f"{splan:.03f}" for splan in splan_percentiles]), end=", ")
print(splan_df["errors"].mean())

# qerr (subqueries)
qerror_file_path = os.path.join("results", args[1], "QError.csv")
qerror_df = pd.read_csv(qerror_file_path)
qerror_percentiles = qerror_df["errors"].quantile([0.5, 0.9, 0.95, 0.99, 1.0])
print("qerr: ", end="")
print(", ".join([f"{qerror:.03f}" for qerror in qerror_percentiles]))
