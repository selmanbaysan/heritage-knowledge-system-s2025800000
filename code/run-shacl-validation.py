import sys
from pyshacl import validate
from rdflib import Graph

def run_validation():
    data_graph = Graph()
    try:
        data_graph.parse("data/heritage-base.ttl", format="turtle")
        data_graph.parse("ontology/heritage-ontology.owl", format="xml")
    except Exception as e:
        print(f"Error loading files: {e}")
        return

    conforms, v_graph, v_text = validate(
        data_graph,
        shacl_graph="validation/temporal-constraints.shacl",
        inference='owlrl',
        abort_on_first=False,
        allow_infos=False,
        allow_warnings=False,
        meta_shacl=False,
        advanced=True
    )

    print(f"Validation Complete. Conforms: {conforms}")
    
    output_path = "validation/validation-report-violations.txt"
    with open(output_path, "w") as f:
        f.write(v_text)
    
    print(f"Report saved to: {output_path}")
    print("--- Preview of Violations ---")
    print(v_text)

if __name__ == "__main__":
    run_validation()