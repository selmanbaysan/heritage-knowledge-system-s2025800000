Knowledge Graph Architecture & Design Justification

This document details the modeling decisions behind the Heritage Knowledge Graph and the rationale for the ontology structure.

1. Ontology Design Strategy

The ontology (heritage-ontology.owl) was designed to support both inference (OWL) and validation (SHACL).

1.1. Role-Based Modeling

Instead of modeling roles (e.g., Guardian, Elder) purely as subclasses of Person, I modeled them as separate entities under the Role class, linked via the hasRole object property.

Justification: This allows a single Person to hold multiple roles simultaneously (e.g., a person can be both an Archaeologist and a TribalElder). It also separates the "identity" of a person from their "function" within the heritage system, making the graph more flexible for dynamic role assignments.

1.2. The Logical Definition of Spiritual Guardian

The SpiritualGuardian class is defined using an Equivalent Class axiom:
SpiritualGuardian ≡ Role AND (hasRole some GuardianRole) AND (caresFor some SacredItem)

Justification: This enables Automatic Classification. We do not manually assert who is a Spiritual Guardian. Instead, the reasoner infers this status based on an individual's behavior (caring for sacred items) and assigned role. This aligns with the "Open World" nature of the domain, where status is derived from actions.

1.3. Data Properties for Validation

Properties like humanApproval (boolean), recordingDate (date), and accessLevel (string) were strictly defined as Data Properties.

Justification: These are essential for the SHACL validation layer. OWL reasoning uses the object properties for classification, while SHACL uses these data properties to enforce administrative rules (e.g., "An inferred Spiritual Guardian must have humanApproval=true").

2. Data Modeling Patterns

To handle the requirement of "Conflicting Claims" (Part 2), I implemented three distinct patterns to avoid logical contradictions in the knowledge base.

Named Graphs: Used to isolate contradictory claims (e.g., Tribe A vs. Tribe B) into separate graph contexts. This prevents the knowledge graph from becoming inconsistent while keeping all data accessible.

RDF Reification: Used to attach metadata (confidence, source) to individual statements, providing granular provenance tracking.

RDF-star: Utilized as a modern, more efficient alternative to reification for edge-level metadata.

3. Validation Architecture

The system uses a hybrid validation approach:

OWL Reasoner (HermiT): Handles the positive classification (Inference).

SHACL Engine: Handles the negative constraints (Validation).

Temporal Constraints: SHACL-SPARQL was chosen over SWRL because comparing two dynamic date values (recordingDate > restrictionEffectiveDate) is standard in SPARQL but computationally complex or impossible in standard OWL 2 DL.