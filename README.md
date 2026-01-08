# Heritage Knowledge System

**Student Name:** Mehmet Selman Baysan
**Student ID:** 2025800000

This repository contains the Knowledge Graph implementation for the Cmpe58H Final Exam. The project models cultural heritage data, handles conflicting claims between tribes, and validates permissions using SHACL.

## Tools & Versions Used

*   **Protégé:** 5.6.8 (Desktop)
*   **Triplestore:** GraphDB Free 11.1.3
*   **Language:** Python 3.11
*   **Libraries:**
    *   rdflib (7.5.0)
    *   pyshacl (0.30.1)
    *   SPARQLWrapper (2.0.0)
    *   requests (2.32.3)

## Project Structure

*   `ontology/`: Contains the OWL file (heritage-ontology.owl).
*   `data/`: All Turtle/TriG data files (base data, conflicting claims, violations).
*   `code/`: Python scripts to load data, run queries, and execute validation.
*   `validation/`: SHACL shapes and validation reports.
*   `queries/`: SPARQL query files and their JSON results.
*   `analysis/`: Performance comparison and design justification.

## Setup Instructions

### 1. Python Setup

Make sure you have Python installed. Create a virtual environment and install the required libraries:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r code/requirements.txt
```

### 2. GraphDB Setup

Start your GraphDB instance (default: http://localhost:7200).

The script below will automatically create the necessary repositories (heritage-reification, heritage-named, heritage-rdfstar) and load the data.

```bash
python code/load-triplestore.py
```

### 3. Run SPARQL Queries (Part 2)

This script executes the queries for conflicting claims and saves the results to `queries/results/`.

```bash
python code/run-queries.py
```

### 4. Run SHACL Validation (Part 3)

This script runs the validation on the problematic data heritage-base.ttl and violations.ttl separately (expected to fail) and the fixed-data.ttl (expected to pass).

```bash
python code/run-temporal-validation.py
```

## Analysis Answers

### Part 1: Automatic Classification & Human Approval

**Why does OWL reasoning automatically classify individuals as SpiritualGuardian?**
OWL uses the "Open World Assumption." In my ontology, a SpiritualGuardian is logically defined as anyone who has a GuardianRole AND cares for a SacredItem. Since the individuals in my data met these two conditions, the reasoner automatically inferred they belong to this class. It looks at logic, not permissions.

**Why can't OWL axioms alone enforce the human approval requirement?**
OWL is for discovering new information, not for checking rules. If I say "A Guardian needs approval," and a person in the data lacks the humanApproval property, OWL does not see this as an error. It just assumes the approval exists somewhere else but hasn't been added to the database yet.

**How does SHACL complement OWL in this scenario?**
SHACL works with a "Closed World Assumption." It assumes the data we have is complete. I used SHACL to act as a gatekeeper. While OWL classifies someone as a Guardian based on their actions, SHACL checks if they actually have the humanApproval=true flag. If they don't, SHACL reports a violation.

### Part 3: OWL Limitation Demonstration

**Why the OWL approach for temporal constraints fails?**
In the file `validation/owl-limitation-demo.owl`, I tried to write a rule saying "Recording Date must be before Restriction Date." However, this failed because standard OWL 2 DL can only compare a date against a constant value (like date > 2026-01-08). It cannot compare two variables against each other (like Property A > Property B). This kind of dynamic comparison is impossible in OWL, so I had to use SHACL-SPARQL to solve it.

### Fundamental Difference: OWL vs. SHACL

*   **OWL (Open World):** Good for classification and inference. If info is missing, it assumes it's just unknown. Adding new data never breaks old conclusions (Monotonic).
*   **SHACL (Closed World):** Good for validation. If info is missing, it's an error. It strictly enforces the rules we define.

### Known Limitations

*   **The Elder Paradox:** In the validation report, Tribal Elders appear as violations because the rule says "Everyone needs approval from an Elder." However, Elders are the highest authority and approve themselves. I left this as is to show the strictness of the SHACL rule.
*   **Legacy Data Warnings:** When validating the full dataset, some older ritual entries trigger warnings because they use performedBy instead of the newer hasPerformer property.
