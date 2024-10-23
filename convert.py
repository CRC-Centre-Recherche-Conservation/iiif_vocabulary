import argparse
import json
import uuid
import time
from rdflib import Graph, Namespace, URIRef, RDF

# Définition des namespaces utilisés dans le fichier RDF
DC = Namespace("http://purl.org/dc/elements/1.1/")
DCT = Namespace("http://purl.org/dc/terms/")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")

# Générer un identifiant basé sur l'attribut skos:Concept@rdf:about
def generate_id(uri):
    return str(uri)

# Fonction pour obtenir la date de création d'un concept
def get_creation_date(g, concept):
    for _, _, creation_date in g.triples((concept, DCT.created, None)):
        return str(creation_date)
    return None

# Fonction pour obtenir le titre du schéma de concepts (racine)
def get_scheme_title(g, scheme):
    for _, _, title in g.triples((scheme, DC.title, None)):
        return str(title)
    return "Unknown Title"

# Fonction pour obtenir le prefLabel en français
def get_pref_label_fr(g, concept):
    for _, _, label in g.triples((concept, SKOS.prefLabel, None)):
        if label.language == "fr-fr":
            return str(label)
    return None

# Fonction pour construire une hiérarchie
def build_hierarchy(g, scheme):
    root = {
        "type": "category",
        "id": generate_id(scheme),
        "name": get_scheme_title(g, scheme),
        "children": [],
        "creationDate": get_creation_date(g, scheme),
        "creationTimestamp": int(time.time()),  # Ajout de la timestamp
        "showChildren": True
    }

    # Parcourir les concepts du fichier RDF
    for concept in g.subjects(SKOS.inScheme, scheme):
        category = {
            "id": generate_id(concept),
            "name": get_pref_label_fr(g, concept),
            "creationDate": get_creation_date(g, concept),
            "creationTimestamp": int(time.time()),  # Ajout de la timestamp
        }

        # Vérifier si le concept a des enfants (sous-concepts)
        children = list(g.objects(concept, SKOS.broader))
        
        if children:  # Si le concept a des enfants
            category["type"] = "tag"  # Traité comme un tag
            category["children"] = []

            for child in children:
                child_tags = {
                    "type": "tag",
                    "id": generate_id(child),
                    "name": get_pref_label_fr(g, child),
                    "creationDate": get_creation_date(g, child),
                    "creationTimestamp": int(time.time())  # Ajout de la timestamp
                }
                category["children"].append(child_tags)  # Ajouter le tag enfant
            root["children"].append(category)  # Ajouter le concept avec ses enfants à la racine
        else:  # Si le concept n'a pas d'enfants
            category["type"] = "tag"  # Traité comme un tag sans enfants
            root["children"].append(category)  # Ajouter le tag à la racine

    return root

# Fonction principale pour gérer les arguments du CLI
def main():
    parser = argparse.ArgumentParser(description="Transforme un fichier RDF en un fichier JSON hiérarchique.")
    
    # Argument pour le fichier RDF
    parser.add_argument("rdf_file", help="Chemin vers le fichier RDF à transformer.")
    
    # Argument pour le fichier JSON de sortie
    parser.add_argument("output_file", help="Chemin pour sauvegarder le fichier JSON généré.")
    
    args = parser.parse_args()
    
    # Charger le fichier RDF dans un graphe
    g = Graph()
    g.parse(args.rdf_file, format="xml")  # Lire le fichier RDF
    
    # Trouver le schéma de concept
    for scheme in g.subjects(RDF.type, SKOS.ConceptScheme):
        # Construire la hiérarchie
        hierarchy = build_hierarchy(g, scheme)
        break
    
    # Envelopper la hiérarchie dans une liste
    json_output = [hierarchy]

    # Sauvegarder la hiérarchie dans le fichier JSON
    with open(args.output_file, "w") as f:
        json.dump(json_output, f, indent=4)
    
    print(f"Hiérarchie JSON générée et sauvegardée dans {args.output_file}.")

if __name__ == "__main__":
    main()
