# 📄 Système de Génération de CV Modulaire

Un système flexible pour générer des CV professionnels en PDF à partir d'un fichier CSV facilement modifiable.

## 🎯 Principe

- **Un template Python réutilisable** (`cv_template.py`) qui gère la mise en page
- **Un fichier CSV** (`cv_content.csv`) qui contient tout le contenu
- **Tu modifies le CSV** selon le poste visé, et tu génères un nouveau PDF en 1 commande !

## 📁 Fichiers

```
cv_template.py       # Template Python (ne pas modifier sauf pour le design)
cv_content.csv       # Contenu du CV (à modifier pour chaque candidature)
README.md            # Ce fichier
```

## 🚀 Utilisation

### Génération basique
```bash
python cv_template.py cv_content.csv mon_cv.pdf
```

### Pour différents postes

**Exemple 1 : Poste Data Scientist**
```bash
# 1. Copier le CSV de base
cp cv_content.csv cv_data_scientist.csv

# 2. Modifier cv_data_scientist.csv pour mettre en avant:
#    - Expériences en data science
#    - Projets ML/statistiques
#    - Compétences Python, pandas, scikit-learn

# 3. Générer le CV
python cv_template.py cv_data_scientist.csv cv_data_scientist.pdf
```

**Exemple 2 : Poste Lead IA**
```bash
cp cv_content.csv cv_lead_ia.csv
# Modifier pour mettre en avant:
# - Expériences de management
# - Stratégie IA
# - Leadership technique

python cv_template.py cv_lead_ia.csv cv_lead_ia.pdf
```

**Exemple 3 : Poste MLOps Engineer**
```bash
cp cv_content.csv cv_mlops.csv
# Modifier pour mettre en avant:
# - Docker, Kubernetes
# - CI/CD, pipelines ML
# - Cloud (AWS, Azure)

python cv_template.py cv_mlops.csv cv_mlops.pdf
```

## 📝 Structure du fichier CSV

Le CSV contient 5 colonnes :

| Colonne | Description | Exemple |
|---------|-------------|---------|
| `section` | Section du CV | `experience`, `formation`, `competences_cles` |
| `subsection` | Sous-section (identifiant unique) | `iafluence_titre`, `mba_description` |
| `type` | Type de contenu | `text`, `bullet`, `paragraph` |
| `content` | Le contenu lui-même | `Consultant IA et Formateur - IAfluence` |
| `order` | Ordre d'affichage | `1`, `2`, `3`, etc. |

### Sections disponibles

#### 📌 Header (colonne gauche)
```csv
header,nom,text,SUAN TAY,1
header,titre,text,Ingénieur IA,2
header,email,text,suan.tay@iafluence.fr,3
```

#### 🌍 Langues
```csv
langues,francais,text,Français - Bilingue,1
langues,anglais,text,Anglais - Courant,2
```

#### 💡 Compétences clés (sidebar)
```csv
competences_cles,strategie,text,"<b>Stratégie Data & IA</b>: Gouvernance, feuille de route",1
```

#### 🎨 Centres d'intérêt
```csv
centres_interet,velo,text,Vélo,1
```

#### 👤 Profil
```csv
profil,description,paragraph,"Ingénieur IA avec 5+ ans d'expérience...",1
```

#### 💼 Expériences
Format: `experience,{entreprise}_{champ},type,contenu,ordre`

```csv
experience,iafluence_titre,text,Consultant IA et Formateur - IAfluence,1
experience,iafluence_periode,text,Depuis mars 2024 | Volvic,1
experience,iafluence_bullet1,bullet,Conseil stratégique IA,1
experience,iafluence_bullet2,bullet,Formation en prompting,2
```

**Important:** Le préfixe avant `_` (ex: `iafluence`) regroupe les éléments d'une même expérience.

#### 🎓 Formations
Format similaire aux expériences:

```csv
formation,mba_titre,text,Master of Business Administration - MBA,1
formation,mba_periode,text,Sept. 2023 - Sept. 2024,1
formation,mba_description,text,Formation en gestion...,1
```

#### 🛠️ Compétences techniques (optionnel)
```csv
competences_tech,llm,text,"<b>LLM & GenAI</b>: GPT, LLaMA, Mistral",1
```

## ✏️ Personnalisation pour un poste

### Étape 1 : Analyser l'offre
Identifie les mots-clés de l'offre d'emploi :
- Compétences techniques requises
- Soft skills demandées
- Type de projets

### Étape 2 : Adapter le contenu

**A. Modifier le titre**
```csv
# Pour un poste "Senior Data Scientist"
header,titre,text,Senior Data Scientist,2

# Pour un poste "Lead IA"
header,titre,text,Lead Intelligence Artificielle,2
```

**B. Réorganiser les expériences**
Change l'`order` pour mettre les expériences les plus pertinentes en premier :

```csv
# Avant (ordre chronologique)
experience,screenact_titre,text,...,3
experience,iafluence_titre,text,...,1

# Après (pour poste management)
experience,screenact_titre,text,...,1  # Management en premier
experience,iafluence_titre,text,...,2
```

**C. Adapter les bullets**
Réécris les bullets pour matcher l'offre :

```csv
# Original
experience,screenact_bullet2,bullet,Déployé des modèles IA avancés,2

# Pour poste MLOps
experience,screenact_bullet2,bullet,"Déployé des modèles IA en production sur Databricks avec CI/CD",2

# Pour poste Management
experience,screenact_bullet2,bullet,"Piloté le déploiement de 5+ modèles IA avec une équipe de 8 personnes",2
```

**D. Ajuster les compétences clés**
```csv
# Pour poste technique
competences_cles,cloud,text,"<b>Cloud & MLOps</b>: Docker, Kubernetes, Azure ML, CI/CD",3

# Pour poste stratégique
competences_cles,cloud,text,"<b>Cloud & Sécurité</b>: Architecture cloud, standards de sécurité, RGPD",3
```

### Étape 3 : Supprimer ce qui n'est pas pertinent

Pour supprimer un élément, soit :
- Le retirer du CSV
- Ou commenter la ligne avec `#` au début

```csv
# Cette expérience ne sera pas affichée
# experience,ancien_poste_titre,text,Développeur Junior,10
```

## 🎨 Personnalisation du design

Si tu veux changer les couleurs ou la mise en page, modifie `cv_template.py` :

```python
# Ligne 20-23 : Changer les couleurs
DARK_BLUE = colors.HexColor('#1e3a5f')     # Couleur sidebar
ACCENT_BLUE = colors.HexColor('#2980b9')   # Couleur accents
TEXT_GRAY = colors.HexColor('#333333')     # Couleur texte

# Ligne 27 : Ajuster la largeur de la colonne gauche
LEFT_COLUMN_WIDTH = 7*cm  # Augmenter ou diminuer
```

## 💡 Astuces

### 1. Utiliser le formatage HTML
Le CSV supporte le HTML basique :

```csv
experience,bullet,bullet,"Développé une <b>application IA innovante</b> avec <i>+50% de ROI</i>",1
```

### 2. Créer des variantes par secteur
```bash
cv_content.csv              # Version générale
cv_startup.csv              # Startups tech (focus innovation)
cv_grand_groupe.csv         # Grands groupes (focus process)
cv_conseil.csv              # Conseil (focus stratégie)
```

### 3. Garder un historique
```bash
# Créer un dossier pour chaque candidature
mkdir candidatures/
mkdir candidatures/acme_corp_lead_ia/
cp cv_content.csv candidatures/acme_corp_lead_ia/
# Modifier et générer
```

### 4. Automatiser avec un script
```bash
#!/bin/bash
# generate_cv.sh

COMPANY=$1
POSTE=$2

mkdir -p "candidatures/${COMPANY}"
cp cv_content.csv "candidatures/${COMPANY}/cv_${POSTE}.csv"

echo "✏️  Modifie le fichier: candidatures/${COMPANY}/cv_${POSTE}.csv"
echo "📄 Puis génère avec: python cv_template.py candidatures/${COMPANY}/cv_${POSTE}.csv candidatures/${COMPANY}/cv_${COMPANY}_${POSTE}.pdf"
```

Usage:
```bash
./generate_cv.sh google "senior_ml_engineer"
```

## 📊 Exemples de personnalisation

### Exemple complet : Adapter pour un poste "ML Engineer chez Netflix"

**1. Analyse de l'offre fictive :**
- Python, TensorFlow, PyTorch
- Systèmes de recommandation
- MLOps (Docker, Kubernetes)
- Travail en équipe internationale

**2. Modifications dans le CSV :**

```csv
# Changer le titre
header,titre,text,Machine Learning Engineer,2

# Réorganiser les expériences (mettre ScreenACT en premier car c'est du ML en prod)
experience,screenact_titre,text,ML Engineer - COO,1
experience,screenact_periode,text,Mars 2022 - Avril 2024 | ScreenACT,1
experience,screenact_bullet1,bullet,"Développé et déployé des <b>systèmes de recommandation ML</b> sur Databricks (+30% engagement)",1
experience,screenact_bullet2,bullet,"Architecture MLOps complète: Docker, Kubernetes, CI/CD avec Azure DevOps",2
experience,screenact_bullet3,bullet,"Collaboration avec équipes internationales (US, Europe, Asie)",3

# Adapter les compétences clés
competences_cles,ml,text,"<b>ML Engineering</b>: PyTorch, TensorFlow, Systèmes de recommandation, A/B testing",1
competences_cles,mlops,text,"<b>MLOps</b>: Docker, Kubernetes, CI/CD, monitoring de modèles en production",2

# Ajouter des compétences techniques pertinentes
competences_tech,frameworks,text,"<b>ML Frameworks</b>: PyTorch, TensorFlow, scikit-learn, XGBoost",1
competences_tech,recommandation,text,"<b>RecSys</b>: Collaborative filtering, Content-based, Hybrid systems, Matrix factorization",2
```

**3. Générer :**
```bash
python cv_template.py cv_netflix_ml.csv cv_netflix_ml_engineer.pdf
```

## 🔧 Dépannage

### Le PDF ne se génère pas
```bash
# Vérifier que reportlab est installé
pip install reportlab

# Vérifier que le CSV est bien formaté
python -c "import csv; list(csv.DictReader(open('cv_content.csv')))"
```

### Les caractères spéciaux ne s'affichent pas
Assure-toi que le CSV est en UTF-8 :
```bash
file cv_content.csv  # Doit indiquer UTF-8
```

### Le contenu déborde de la page
Réduis le contenu ou ajuste les espacements dans `cv_template.py` (lignes `spaceAfter` et `spaceBefore`).

## 📦 Livraison

Pour partager le système avec quelqu'un :

```bash
# Créer une archive
tar -czf cv_system.tar.gz cv_template.py cv_content.csv README.md

# Ou zipper
zip cv_system.zip cv_template.py cv_content.csv README.md
```

## 🎓 Pour aller plus loin

- Ajouter des logos d'entreprises
- Intégrer une photo de profil
- Créer des graphiques de compétences
- Générer automatiquement depuis LinkedIn

---

**Créé par Suan Tay** • Novembre 2025
