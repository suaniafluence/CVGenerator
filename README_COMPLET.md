# 🚀 Système Complet de Génération de CV - Custom GPT

Un système complet pour créer des CV professionnels personnalisables, utilisable en ligne de commande ou via un Custom GPT.

## 📦 Contenu du package

### 🎯 Version Standalone (locale)
- **`cv_template.py`** - Template Python pour générer des CV
- **`cv_content.csv`** - Fichier CSV avec le contenu (facile à modifier)
- **`README.md`** - Guide d'utilisation du système local

### 🌐 Version API (pour Custom GPT)
- **`cv_api.py`** - API Flask avec endpoints REST
- **`requirements.txt`** - Dépendances Python
- **`test_api.py`** - Script de test de l'API
- **`CUSTOM_GPT_GUIDE.md`** - Guide complet pour intégrer avec Custom GPT

### 📄 Exemples générés
- **`cv_from_template.pdf`** - CV d'exemple généré
- **`CV_SUAN_TAY_2026_professionnel.pdf`** - CV avec design 2 colonnes

## 🎨 Aperçu du design

Le CV généré utilise un **design moderne à 2 colonnes** :
- **Colonne gauche (bleu foncé)** : Contact, langues, compétences clés, centres d'intérêt
- **Colonne droite (blanc)** : Profil, expériences, formations, compétences techniques

## 🚀 Démarrage rapide

### Option 1 : Utilisation locale (sans API)

```bash
# 1. Installer les dépendances
pip install reportlab

# 2. Modifier le CSV avec tes informations
# Édite cv_content.csv

# 3. Générer le CV
python cv_template.py cv_content.csv mon_cv.pdf
```

**Cas d'usage :** Tu veux générer des CV rapidement en local, sans déployer d'API.

### Option 2 : API + Custom GPT (recommandé)

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Lancer l'API
python cv_api.py

# 3. Tester l'API
python test_api.py

# 4. Déployer sur Render/Railway (voir CUSTOM_GPT_GUIDE.md)

# 5. Configurer ton Custom GPT avec l'URL de l'API
```

**Cas d'usage :** Tu veux un Custom GPT qui génère des CV professionnels automatiquement.

## 💼 Cas d'usage

### 1. Adapter ton CV pour différents postes

**Scénario :** Tu postules à 3 postes différents (Data Scientist, ML Engineer, Lead IA)

```bash
# Créer 3 versions du CSV
cp cv_content.csv cv_data_scientist.csv
cp cv_content.csv cv_ml_engineer.csv
cp cv_content.csv cv_lead_ia.csv

# Modifier chaque CSV pour mettre en avant les compétences pertinentes
# Puis générer les 3 CV :
python cv_template.py cv_data_scientist.csv cv_data_scientist.pdf
python cv_template.py cv_ml_engineer.csv cv_ml_engineer.pdf
python cv_template.py cv_lead_ia.csv cv_lead_ia.pdf
```

### 2. Custom GPT pour ton équipe

**Scénario :** Ton équipe RH veut un outil pour aider les candidats internes

1. **Déploie l'API** sur Render (gratuit)
2. **Crée un Custom GPT** "RH Assistant CV"
3. **Partage-le** avec ton organisation

Les employés peuvent alors dire :
> "Aide-moi à créer un CV pour une mobilité interne en Data Science"

Le GPT collecte les infos, génère le CV, et fournit le lien de téléchargement.

### 3. Génération de CV en masse

**Scénario :** Générer des CV pour 100 profils depuis une base de données

```python
import pandas as pd
import subprocess

# Charger les profils
df = pd.read_csv('profils_employees.csv')

for idx, row in df.iterrows():
    # Créer un CSV pour chaque profil
    csv_content = f"""section,subsection,type,content,order
header,nom,text,{row['nom']},1
header,titre,text,{row['titre']},2
experience,exp1_titre,text,{row['experience']},1
...
"""
    
    # Sauvegarder le CSV
    with open(f'cv_{row["id"]}.csv', 'w') as f:
        f.write(csv_content)
    
    # Générer le PDF
    subprocess.run([
        'python', 'cv_template.py',
        f'cv_{row["id"]}.csv',
        f'cv_{row["id"]}.pdf'
    ])

print(f"✅ {len(df)} CV générés !")
```

## 📊 Structure du fichier CSV

Le CSV est super simple à modifier. Il a 5 colonnes :

| Colonne | Description | Exemple |
|---------|-------------|---------|
| `section` | Section du CV | `experience`, `formation` |
| `subsection` | Identifiant unique | `google_titre`, `mba_description` |
| `type` | Type de contenu | `text`, `bullet`, `paragraph` |
| `content` | Le contenu | `Consultant IA - Google` |
| `order` | Ordre d'affichage | `1`, `2`, `3` |

**Exemple :**
```csv
section,subsection,type,content,order
header,nom,text,SUAN TAY,1
header,titre,text,Ingénieur IA,2
experience,google_titre,text,ML Engineer - Google,1
experience,google_periode,text,2020-2024 | Mountain View,1
experience,google_bullet1,bullet,Développé des modèles ML,1
```

## 🔧 Configuration

### Personnaliser les couleurs

Dans `cv_template.py` ou `cv_api.py`, lignes 20-23 :

```python
DARK_BLUE = colors.HexColor('#1e3a5f')     # Sidebar
ACCENT_BLUE = colors.HexColor('#2980b9')   # Accents
TEXT_GRAY = colors.HexColor('#333333')     # Texte principal
```

### Ajuster la largeur des colonnes

```python
LEFT_COLUMN_WIDTH = 7*cm  # Colonne gauche
```

## 🌐 API Endpoints

### `POST /generate-cv`
Génère un CV à partir d'un contenu CSV

**Request:**
```json
{
  "csv_content": "section,subsection,type,content,order\nheader,nom,text,Jean Dupont,1\n..."
}
```

**Response:**
```json
{
  "success": true,
  "cv_id": "abc-123-def-456",
  "download_url": "https://api.com/download-cv/abc-123-def-456",
  "message": "CV généré avec succès"
}
```

### `GET /download-cv/{cv_id}`
Télécharge un CV généré

**Response:** Fichier PDF

### `GET /health`
Vérifie l'état de l'API

### `GET /openapi.json`
Récupère la spécification OpenAPI 3.1.0

## 🧪 Tests

### Test local
```bash
# Lancer l'API
python cv_api.py

# Dans un autre terminal, lancer les tests
python test_api.py
```

### Test avec curl
```bash
# Health check
curl http://localhost:5000/health

# Générer un CV
curl -X POST http://localhost:5000/generate-cv \
  -H "Content-Type: application/json" \
  -d '{"csv_content": "section,subsection,type,content,order\nheader,nom,text,Test User,1"}'
```

## 📚 Documentation complète

- **`README.md`** - Guide du système local
- **`CUSTOM_GPT_GUIDE.md`** - Guide complet Custom GPT (déploiement, configuration, sécurité)

## 🎓 Tutoriel vidéo (à créer)

1. **Installation et premier CV** (5 min)
2. **Personnalisation pour différents postes** (10 min)
3. **Déploiement de l'API** (15 min)
4. **Configuration du Custom GPT** (10 min)

## 🔐 Sécurité

Pour la production, considère :

1. **Rate limiting** - Limiter le nombre de requêtes
2. **API Key** - Authentification par clé
3. **File cleanup** - Supprimer les vieux PDFs
4. **Input validation** - Valider le contenu CSV
5. **CORS** - Configurer les origines autorisées

Voir `CUSTOM_GPT_GUIDE.md` pour les détails.

## 🐛 Problèmes courants

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Permission denied"
```bash
chmod +x cv_template.py cv_api.py test_api.py
```

### Le PDF est vide ou corrompu
- Vérifie que le CSV est bien formaté (pas de virgules manquantes)
- Vérifie l'encodage UTF-8 du fichier CSV

### L'API ne démarre pas
- Vérifie que le port 5000 n'est pas utilisé
- Change le port : `app.run(port=5001)`

## 🚀 Améliorations futures

- [ ] Templates multiples (classique, moderne, créatif)
- [ ] Support photo de profil
- [ ] Export DOCX en plus du PDF
- [ ] Traduction automatique FR/EN/ES
- [ ] Scoring ATS (Applicant Tracking System)
- [ ] Génération de lettres de motivation
- [ ] Interface web (React/Vue)
- [ ] Intégration LinkedIn (import auto)

## 📊 Statistiques

- **Lignes de code :** ~1500
- **Dépendances :** 3 (Flask, reportlab, werkzeug)
- **Temps de génération :** <1 seconde par CV
- **Format de sortie :** PDF A4
- **Taille moyenne :** 5-10 KB par PDF

## 🤝 Contribution

Pour contribuer :

1. Fork le projet
2. Crée une branche : `git checkout -b feature/ma-feature`
3. Commit : `git commit -m 'Ajout de ma feature'`
4. Push : `git push origin feature/ma-feature`
5. Crée une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Tu es libre de l'utiliser, le modifier et le distribuer.

## 📞 Support

- **Email :** suan.tay@iafluence.fr
- **GitHub Issues :** Pour reporter des bugs
- **Discussions :** Pour poser des questions

## 🙏 Remerciements

- **ReportLab** pour la génération de PDF
- **Flask** pour le framework API
- **OpenAI** pour les Custom GPTs

---

**Créé par Suan Tay** • Novembre 2025

⭐ Si ce projet t'aide, n'hésite pas à le star sur GitHub !
