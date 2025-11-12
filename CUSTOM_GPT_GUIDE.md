# 🤖 Guide d'intégration Custom GPT - API CV Generator

## 📋 Vue d'ensemble

Cette API permet à ton Custom GPT de générer des CV professionnels en PDF à partir d'un contenu CSV.

## 🚀 Déploiement

### Option 1 : Déploiement sur Render.com (Gratuit)

1. **Crée un compte sur [Render.com](https://render.com)**

2. **Crée un nouveau Web Service**
   - Clique sur "New +" → "Web Service"
   - Connecte ton repo GitHub ou upload les fichiers

3. **Configuration :**
   ```
   Name: cv-generator-api
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn cv_api:app
   ```

4. **Variables d'environnement :**
   ```
   FLASK_ENV=production
   ```

5. **Deploy !**
   - Render va te donner une URL: `https://cv-generator-api.onrender.com`

### Option 2 : Déploiement sur Railway.app

1. **Crée un compte sur [Railway.app](https://railway.app)**

2. **Deploy from GitHub**
   - Sélectionne ton repo
   - Railway détecte automatiquement Flask

3. **Ajoute un fichier `Procfile` :**
   ```
   web: gunicorn cv_api:app
   ```

4. **Variables d'environnement :**
   ```
   FLASK_ENV=production
   ```

### Option 3 : Déploiement local (pour tests)

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer l'API
python cv_api.py
```

L'API sera accessible sur `http://localhost:5000`

## 🔗 Configuration du Custom GPT

### Étape 1 : Créer ton Custom GPT

1. Va sur ChatGPT → Ton profil → "My GPTs"
2. Clique sur "Create a GPT"
3. Donne-lui un nom : **"CV Generator Pro"**

### Étape 2 : Instructions du GPT

Colle ces instructions dans le champ "Instructions" :

```
Tu es un assistant expert en création de CV professionnels. Tu aides les utilisateurs à créer des CV personnalisés au format PDF.

## Ton rôle :

1. **Collecter les informations** : Pose des questions pour obtenir toutes les informations nécessaires au CV
2. **Structurer en CSV** : Organise les données au format CSV requis
3. **Générer le CV** : Utilise l'API pour créer le PDF
4. **Fournir le lien** : Donne le lien de téléchargement à l'utilisateur

## Format CSV requis :

Le CSV doit avoir ces colonnes : section, subsection, type, content, order

### Sections disponibles :
- **header** : nom, titre, email, telephone, localisation, remote, twitter, linkedin
- **langues** : francais, anglais, espagnol, etc.
- **competences_cles** : competences pour la sidebar
- **centres_interet** : hobbies et centres d'intérêt
- **profil** : description du profil professionnel
- **experience** : expériences professionnelles (format: {entreprise}_{champ})
- **formation** : diplômes et formations (format: {ecole}_{champ})
- **competences_tech** : compétences techniques détaillées

### Exemple de structure CSV :
```
section,subsection,type,content,order
header,nom,text,Jean Dupont,1
header,titre,text,Développeur Full Stack,2
header,email,text,jean.dupont@email.com,3
experience,google_titre,text,Senior Developer - Google,1
experience,google_periode,text,2020 - 2024 | Mountain View,1
experience,google_bullet1,bullet,Développé des applications scalables,1
```

## Workflow :

1. **Question initiale** : "Bonjour ! Je vais t'aider à créer un CV professionnel. Pour commencer, quel est ton nom complet ?"

2. **Collecte progressive** :
   - Informations personnelles
   - Expériences professionnelles (du plus récent au plus ancien)
   - Formations
   - Compétences
   - Langues
   - Centres d'intérêt

3. **Confirmation** : Résume les informations et demande confirmation

4. **Génération** : Crée le CSV et appelle l'API

5. **Livraison** : Fournis le lien de téléchargement du PDF

## Conseils à donner :

- Utiliser des verbes d'action pour les bullets
- Quantifier les réalisations quand possible
- Adapter le CV au poste visé
- Garder un style professionnel et concis

## Important :

- Toujours formater correctement le CSV (respecter les virgules et guillemets)
- Pour les expériences, utiliser un préfixe unique (ex: google_, microsoft_)
- L'order détermine l'affichage (1 = premier)
- Supporter le HTML basique dans le contenu (<b>, <i>)
```

### Étape 3 : Configurer l'Action (API)

1. **Active "Actions"** dans les paramètres du GPT

2. **Clique sur "Create new action"**

3. **Importe le schéma OpenAPI** :
   - Va sur ton API : `https://ton-api.onrender.com/openapi.json`
   - Copie tout le JSON
   - Colle-le dans le champ "Schema"

Ou colle directement ce schéma :

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "CV Generator API",
    "description": "API pour générer des CV professionnels à partir de fichiers CSV",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "https://TON-API.onrender.com"
    }
  ],
  "paths": {
    "/generate-cv": {
      "post": {
        "summary": "Génère un CV à partir d'un contenu CSV",
        "operationId": "generateCV",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "csv_content": {
                    "type": "string",
                    "description": "Contenu du fichier CSV"
                  }
                },
                "required": ["csv_content"]
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "CV généré avec succès"
          }
        }
      }
    }
  }
}
```

**⚠️ Important :** Remplace `https://TON-API.onrender.com` par l'URL réelle de ton API !

4. **Teste l'action** avec le bouton "Test"

### Étape 4 : Paramètres supplémentaires

**Conversation starters** (suggestions) :
- "Aide-moi à créer un CV professionnel"
- "Je veux adapter mon CV pour un poste de Data Scientist"
- "Crée mon CV à partir de ces informations"
- "J'ai besoin d'un CV en urgence"

**Capabilities** :
- ✅ Web Browsing (pour des conseils actualisés)
- ❌ DALL-E (pas nécessaire)
- ❌ Code Interpreter (pas nécessaire)

## 📝 Exemple d'utilisation

**Utilisateur :** "Je veux créer un CV pour un poste de développeur Python"

**GPT :** "Super ! Je vais t'aider à créer un CV professionnel. Commençons par tes informations personnelles. Quel est ton nom complet ?"

**Utilisateur :** "Jean Dupont"

**GPT :** "Parfait Jean. Quelle est ton adresse email ?"

**Utilisateur :** "jean.dupont@gmail.com"

... [Le GPT collecte toutes les informations]

**GPT :** "Excellent ! Voici un résumé de ton CV :
- Nom : Jean Dupont
- Titre : Développeur Python Senior
- Expériences : 3 postes
- Formations : 2 diplômes

Je génère ton CV maintenant..."

[Le GPT appelle l'API]

**GPT :** "✅ Ton CV est prêt ! Tu peux le télécharger ici : [lien]

Quelques conseils :
- Le CV met en avant tes compétences Python et tes projets
- J'ai organisé tes expériences de la plus récente à la plus ancienne
- Les compétences clés sont visibles dans la colonne de gauche

Souhaites-tu que je crée une variante pour un autre type de poste ?"

## 🧪 Test de l'API

### Test avec curl

```bash
# Test de santé
curl https://ton-api.onrender.com/health

# Génération d'un CV
curl -X POST https://ton-api.onrender.com/generate-cv \
  -H "Content-Type: application/json" \
  -d '{
    "csv_content": "section,subsection,type,content,order\nheader,nom,text,SUAN TAY,1\nheader,titre,text,Ingénieur IA,2\nheader,email,text,suan.tay@iafluence.fr,3"
  }'

# Réponse attendue :
# {
#   "success": true,
#   "cv_id": "abc-123-def",
#   "download_url": "https://ton-api.onrender.com/download-cv/abc-123-def",
#   "message": "CV généré avec succès"
# }
```

### Test avec Python

```python
import requests
import json

# Préparer le contenu CSV
csv_content = """section,subsection,type,content,order
header,nom,text,Jean Dupont,1
header,titre,text,Développeur Python,2
header,email,text,jean@email.com,3
experience,google_titre,text,Dev Senior - Google,1
experience,google_periode,text,2020-2024,1
experience,google_bullet1,bullet,Python et Django,1"""

# Appeler l'API
response = requests.post(
    'https://ton-api.onrender.com/generate-cv',
    json={'csv_content': csv_content}
)

# Récupérer le lien
result = response.json()
print(f"CV généré : {result['download_url']}")
```

## 🔒 Sécurité

### Pour la production, ajoute :

1. **Authentification** (optionnel pour Custom GPT privé)
```python
# Dans cv_api.py, ajoute :
API_KEY = os.environ.get('API_KEY', 'ton-secret-key')

@app.before_request
def verify_api_key():
    if request.endpoint not in ['health', 'openapi_spec']:
        api_key = request.headers.get('X-API-Key')
        if api_key != API_KEY:
            return jsonify({"error": "Invalid API key"}), 401
```

2. **Rate limiting**
```bash
pip install flask-limiter
```

```python
from flask_limiter import Limiter

limiter = Limiter(
    app=app,
    key_func=lambda: request.remote_addr,
    default_limits=["100 per day", "10 per minute"]
)
```

3. **Nettoyage automatique des fichiers**
```python
import threading
import time

def cleanup_old_files():
    """Supprime les PDFs de plus de 1 heure"""
    while True:
        time.sleep(3600)  # Toutes les heures
        # Logique de nettoyage...
```

## 🐛 Dépannage

### Erreur : "Module not found"
```bash
pip install -r requirements.txt
```

### Erreur : "Port already in use"
```bash
# Change le port dans cv_api.py
app.run(port=5001)
```

### Le GPT ne trouve pas l'API
- Vérifie que l'URL dans le schéma OpenAPI est correcte
- Teste l'endpoint `/health` dans ton navigateur
- Vérifie les logs de Render/Railway

### Erreur 500 lors de la génération
- Vérifie le format du CSV
- Regarde les logs de l'API
- Teste avec un CSV minimal d'abord

## 📚 Ressources

- [Documentation OpenAI Custom GPTs](https://platform.openai.com/docs/actions)
- [Documentation Flask](https://flask.palletsprojects.com/)
- [Documentation ReportLab](https://www.reportlab.com/docs/reportlab-userguide.pdf)

## 💡 Améliorations futures

- [ ] Support de plusieurs templates (design 1, 2, 3)
- [ ] Upload de photo de profil
- [ ] Génération de lettres de motivation
- [ ] Traduction automatique (FR/EN)
- [ ] Export en DOCX en plus du PDF
- [ ] Analyse et scoring du CV
- [ ] Suggestions de mots-clés ATS

---

Besoin d'aide ? Contacte-moi : suan.tay@iafluence.fr
