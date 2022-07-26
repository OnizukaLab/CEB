import os
import sys
import pandas as pd
from networkx.readwrite import json_graph
from query_representation.utils import *
from query_representation.query import *


def sql_to_qrep(input_file_path: str, output_dir_path: str):
    os.makedirs(output_dir_path, exist_ok=True)

    if input_file_path.endswith(".sql"):
        with open(input_file_path, "r") as f:
            data = f.read()
        queries = data.split(";")
    elif input_file_path.endswith(".csv"):
        queries = pd.read_csv(input_file_path)["sql"]
    else:
        raise ValueError("Input file should be ;-separated sql or csv with sql column")

    for i, sql in enumerate(queries):
        output_fn = os.path.join(output_dir_path, f"{i+1}.pkl")
        if os.path.exists(output_fn):
            print(f"Skip q{i+1}: already exists")
            continue
        if "SELECT" not in sql.upper():
            print(f"Skip q{i+1}: not select query")
            continue

        qrep = parse_sql(sql, None, None, None, None, None,
                compute_ground_truth=False)

        qrep["subset_graph"] = \
                nx.OrderedDiGraph(json_graph.adjacency_graph(qrep["subset_graph"]))
        qrep["join_graph"] = json_graph.adjacency_graph(qrep["join_graph"])

        save_qrep(output_fn, qrep)


if __name__ == "__main__":
    assert len(sys.argv) == 3, "Pass input sql file path and output dir path\n(e.g., python sql_to_qrep.py queries/jobm/imdb-job-m.sql queries/jobm/all_jobm)"
    sql_to_qrep(sys.argv[1], sys.argv[2])
