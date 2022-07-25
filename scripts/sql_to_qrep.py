import os
import sys
from networkx.readwrite import json_graph
from query_representation.utils import *
from query_representation.query import *


def sql_to_qrep(input_file_path: str, output_dir_path: str):
    os.makedirs(output_dir_path, exist_ok=True)

    with open(input_file_path, "r") as f:
        data = f.read()

    queries = data.split(";")
    for i, sql in enumerate(queries):
        output_fn = output_dir_path + str(i+1) + ".pkl"
        if "SELECT" not in sql.lower():
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
