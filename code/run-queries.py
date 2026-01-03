import os
import csv
from SPARQLWrapper import SPARQLWrapper, JSON

GRAPHDB_URL = "http://localhost:7200/repositories"

QUERY_CONFIG = [
    {
        "repo": "heritage-reification",
        "query_file": "queries/q1-reification.rq",
        "output_file": "queries/results/q1-result.json"
    },
    {
        "repo": "heritage-named",
        "query_file": "queries/q2-named-graphs.rq",
        "output_file": "queries/results/q2-result.json"
    },
    {
        "repo": "heritage-rdfstar",
        "query_file": "queries/q3-rdfstar.rq",
        "output_file": "queries/results/q3-result.json"
    }
]

def run_queries():
    os.makedirs("queries/results", exist_ok=True)

    for config in QUERY_CONFIG:
        repo_url = f"{GRAPHDB_URL}/{config['repo']}"
        query_path = config['query_file']
        output_path = config['output_file']

        print(f"Executing {query_path} on {config['repo']}...")

        try:
            with open(query_path, 'r') as f:
                sparql_query = f.read()

            sparql = SPARQLWrapper(repo_url)
            sparql.setQuery(sparql_query)
            sparql.setReturnFormat(JSON)

            results = sparql.query().convert()

            import json
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2)
            
            print(f"  -> Success! Saved to {output_path}")

        except Exception as e:
            print(f"  -> Error: {e}")
            print("  Make sure GraphDB is running and repositories are created!")

if __name__ == "__main__":
    run_queries()