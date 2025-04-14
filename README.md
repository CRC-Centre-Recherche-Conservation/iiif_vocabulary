# Thésaurus *Matérialié* pour Annotate-On

## 📚 Vocabulaire contrôlé pour l'annotation d'acquisitions expérimentales sur documents historiques

Ce dépôt contient des fichiers de configuration JSON à importer dans le logiciel **Annotate-On**, permettant une annotation homogène et standardisée des documents historiques et de leurs analyses. Il permet l'alignement vers les différents thésaurus

### 🔍 Contexte

Ces thésaurus permettent de structurer l'annotation d'images de documents historiques et de leurs analyses physico-chimiques, en utilisant des vocabulaires contrôlés issus notamment des thésaurus AGORHA de l'INHA.

### 📋 Contenu

- **Modèles d'analyses :**
  - `Manuscript.json` : Configuration du modèle des analyses pour les manuscrits
  - `models/analysis_simple.json` : Configuration simplifiée pour les analyses génériques

- **Thésaurus d'analyses :**
  - `keywords/tapac_techniques_analysis.json` : Techniques d'analyses et d'examens (TAPAC)

- **Thésaurus descriptifs :**
  - `keywords/description_materielle.json` : Caractéristiques de description matérielle (AGORHA)
  - `keywords/type_description_materielle.json` : Types de description matérielle (AGORHA)

### 🛠️ Utilisation

1. Cloner ce dépôt sur votre machine locale ou télécharger les fichiers
2. Ouvrir Annotate-On
3. Aller dans les paramètres d'importation des taxonomies
4. Importer les fichiers JSON requis pour votre projet d'annotation

### 🔄 Structure des thésaurus

Les thésaurus sont organisés en catégories et sous-catégories hiérarchiques, avec des tags feuilles qui peuvent être assignés aux régions d'intérêt dans vos images. Chaque tag possède pour identifiant l'URI du concept. 

Exemple de structure pour les techniques d'analyses (TAPAC) :
- Techniques d'analyses et d'examens
  - Imagerie
    - Photographie
    - Microscopie
    - Tomographie
  - Spectrométrie
    - Fluorescence X
    - Spectrométrie Raman
    - Spectrométrie infrarouge
  - Échantillonnage
    - Prélèvement
    - Coupe stratigraphique

### 📝 Contribution

Les contributions pour améliorer ces thésaurus sont les bienvenues. N'hésitez pas à proposer des pull requests ou à ouvrir des issues pour suggérer des améliorations.

### 🔗 Références

- [Thésaurus AGORHA de l'INHA](https://thesaurus.inha.fr/)
- [Thésaurus TAPAC - Frollo](https://ark.notre-dame.science/ark:/35572/th12)
- [Annotate-On - Recolnat](https://www.recolnat.org/fr/annotate)
