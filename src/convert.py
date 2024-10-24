"""
RDF Thesaurus to JSON Converter

This script converts an RDF/SKOS thesaurus into a hierarchical JSON structure
where each category contains both its subcategories and its direct children's tags.

Features:
- Converts SKOS concepts to categories (if they have children) or tags
- Places each concept's tag in its immediate parent's children list
- Root concept is only represented as a category
- Preserves hierarchical relationships using parent-child structure

Usage:
    python rdf_to_json.py input.rdf output.json
"""

import argparse
import json
import uuid
import time
from typing import List, Dict, Any, Optional
from rdflib import Graph, Namespace, RDF, URIRef, Literal

# Define namespaces used in RDF file
DC = Namespace("http://purl.org/dc/elements/1.1/")
DCT = Namespace("http://purl.org/dc/terms/")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")

def generate_id(uri: str) -> str:
    """Generate a stable UUID based on the concept's URI."""
    return str(uuid.uuid5(uuid.NAMESPACE_URL, uri))

def has_children(graph: Graph, subject: URIRef) -> bool:
    """Check if an RDF concept has any child concepts."""
    return len(list(graph.objects(subject, SKOS.narrower))) > 0

def get_pref_label_fr(graph: Graph, concept: URIRef) -> str:
    """Get the preferred French label for a concept, falling back to any available label."""
    for _, _, label in graph.triples((concept, SKOS.prefLabel, None)):
        if label.language == "fr-fr":
            return str(label)
    return str(graph.value(concept, SKOS.prefLabel, None))

def get_creation_date(graph: Graph, concept: URIRef) -> Optional[str]:
    """Get the creation date for a concept."""
    for _, _, creation_date in graph.triples((concept, DCT.created, None)):
        return str(creation_date)
    return None

def create_tag(uri: str, name: str, creation_date: Optional[str]) -> Dict[str, Any]:
    """Create a tag representation of a concept."""
    return {
        "type": "tag",
        "id": uri,
        "name": name,
        "creationDate": creation_date,
        "creationTimestamp": int(time.time() * 1000)
    }

def concept_to_json(graph: Graph, concept: URIRef) -> Dict[str, Any]:
    """
    Convert an RDF concept to JSON, placing tags in their immediate parent category.
    
    For a concept with children:
    - Creates a category with the concept's details
    - Processes all child concepts
    - For each child that has its own children (is a category), adds its tag to the current category's children
    """
    uri = str(concept)
    obj_id = generate_id(uri)
    creation_date = get_creation_date(graph, concept)
    name = get_pref_label_fr(graph, concept)
    
    # If the concept has children, create a category
    if has_children(graph, concept):
        children = []
        
        # Process each child concept
        for child in graph.objects(concept, SKOS.narrower):
            child_obj = concept_to_json(graph, child)
            children.append(child_obj)
            
            # If this child is a category, also add its tag to the current category's children
            if child_obj["type"] == "category":
                child_tag = create_tag(
                    str(child),
                    get_pref_label_fr(graph, child),
                    get_creation_date(graph, child)
                )
                children.append(child_tag)
        
        return {
            "type": "category",
            "id": obj_id,
            "name": name,
            "children": children,
            "creationDate": creation_date,
            "creationTimestamp": int(time.time() * 1000),
            "showChildren": True
        }
    else:
        # For leaf concepts, just create a tag
        return create_tag(uri, name, creation_date)

def rdf_to_json(input_file: str) -> List[Dict[str, Any]]:
    """Convert an RDF thesaurus file to a JSON structure."""
    g = Graph()
    g.parse(input_file)

    # Find the ConceptScheme and treat it as the root category
    concept_scheme = list(g.subjects(RDF.type, SKOS.ConceptScheme))[0]
    scheme_name = str(g.value(concept_scheme, DC.title, None))
    
    children = []
    # Process each top-level concept
    for concept in g.objects(concept_scheme, SKOS.hasTopConcept):
        concept_obj = concept_to_json(g, concept)
        children.append(concept_obj)
        
        # If this top-level concept is a category, also add its tag
        if concept_obj["type"] == "category":
            concept_tag = create_tag(
                str(concept),
                get_pref_label_fr(g, concept),
                get_creation_date(g, concept)
            )
            children.append(concept_tag)
    
    # Create the root category (without a tag)
    root_category = {
        "type": "category",
        "id": str(concept_scheme),
        "name": scheme_name,
        "children": children,
        "creationDate": get_creation_date(g, concept_scheme),
        "creationTimestamp": int(time.time() * 1000),
        "showChildren": True
    }

    return [root_category]

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Convert an RDF/SKOS thesaurus to a hierarchical JSON structure"
    )
    parser.add_argument("input", help="Input RDF file path")
    parser.add_argument("output", help="Output JSON file path")
    args = parser.parse_args()

    try:
        # Convert the RDF thesaurus to JSON
        json_data = rdf_to_json(args.input)

        # Save the result to a JSON file
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)

        print(f"Conversion complete. Output saved to {args.output}")
        
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
