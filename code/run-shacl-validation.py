import sys
from pyshacl import validate
from rdflib import Graph

def validate_dataset(data_file, report_file, description):
    print(f"\n--- Running Validation: {description} ---")
    print(f"Loading Data: {data_file}")
    
    data_graph = Graph()
    try:
        data_graph.parse(data_file, format="turtle")
        data_graph.parse("ontology/heritage-ontology.owl", format="xml")
    except Exception as e:
        print(f"Error loading files: {e}")
        return

    print("Executing SHACL...")
    conforms, v_graph, v_text = validate(
        data_graph,
        shacl_graph="validation/temporal-constraints.shacl",
        inference='rdfs',
        advanced=True,
        debug=False
    )

    print(f"Validation Result -> Conforms: {conforms}")
    
    with open(report_file, "w") as f:
        f.write(v_text)
    
    print(f"Report saved to: {report_file}")
    
    # Ekrana hatası sayısını yazdır
    if not conforms:
        print("Preview of Violations (Truncated):")
        print("\n".join(v_text.splitlines()[:15]))
        print("...")
    else:
        print(">> GREAT SUCCESS! Zero violations detected.")

def main():
    validate_dataset(
        "data/heritage-base.ttl", 
        "validation/validation-report-violations-heritage-base.txt",
        "Part D: Checking Violations (Should fail)"
    )

    validate_dataset(
        "data/violations.ttl", 
        "validation/validation-report-violations.txt",
        "Part D: Checking Violations (Should fail)"
    )

    validate_dataset(
        "data/fixed-data.ttl", 
        "validation/validation-report-clean.txt",
        "Part D: Checking Fixed Data (Should pass)"
    )

if __name__ == "__main__":
    main()