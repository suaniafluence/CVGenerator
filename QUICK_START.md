# 🎯 QUICK START - Choisis ton mode

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   🚀 SYSTÈME COMPLET DE GÉNÉRATION DE CV                   │
│                                                             │
│   2 façons d'utiliser ce système :                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Mode 1️⃣ : LOCAL (Simple et rapide)

**Pour qui ?** 
- Tu veux générer des CV en ligne de commande
- Tu n'as pas besoin de Custom GPT
- Tu veux un contrôle total

**Fichiers nécessaires :**
```
📄 cv_template.py      (le générateur)
📄 cv_content.csv      (ton contenu à modifier)
📄 README.md           (le guide)
```

**Installation :**
```bash
pip install reportlab
```

**Utilisation :**
```bash
# 1. Modifier cv_content.csv avec tes infos

# 2. Générer le CV
python cv_template.py cv_content.csv mon_cv.pdf

# 3. Voilà ! Ton CV est dans mon_cv.pdf
```

**Personnalisation pour différents postes :**
```bash
# Copier le CSV
cp cv_content.csv cv_data_scientist.csv

# Modifier cv_data_scientist.csv
# (changer le titre, réordonner les expériences, etc.)

# Générer
python cv_template.py cv_data_scientist.csv cv_data_scientist.pdf
```

---

## Mode 2️⃣ : API + CUSTOM GPT (Professionnel)

**Pour qui ?**
- Tu veux un assistant IA qui génère des CV
- Tu veux partager l'outil avec ton équipe
- Tu veux une solution web

**Fichiers nécessaires :**
```
📄 cv_api.py                (l'API Flask)
📄 requirements.txt         (dépendances)
📄 Procfile                 (config déploiement)
📄 runtime.txt              (version Python)
📄 openapi_schema.json      (schéma pour GPT)
📄 CUSTOM_GPT_GUIDE.md      (guide détaillé)
📄 test_api.py              (tests)
```

**Étape 1 : Déployer l'API**

**Option A - Render.com (Gratuit, Recommandé)**
```
1. Crée un compte sur render.com
2. New → Web Service
3. Connect ton GitHub repo ou upload les fichiers
4. Configuration :
   - Build: pip install -r requirements.txt
   - Start: gunicorn cv_api:app
5. Deploy !

➡️ Tu obtiens une URL : https://cv-api-xyz.onrender.com
```

**Option B - Railway.app (Gratuit)**
```
1. Crée un compte sur railway.app
2. New Project → Deploy from GitHub
3. Sélectionne ton repo
4. Railway détecte tout automatiquement
5. Deploy !

➡️ Tu obtiens une URL : https://cv-api.railway.app
```

**Option C - Local (pour tester)**
```bash
# Installer
pip install -r requirements.txt

# Lancer
python cv_api.py

# Tester
python test_api.py

➡️ API accessible sur http://localhost:5000
```

**Étape 2 : Créer le Custom GPT**

```
1. Va sur ChatGPT → Ton profil → "My GPTs"

2. Clique "Create a GPT"

3. Nom : "CV Generator Pro"

4. Description :
   "Je génère des CV professionnels en PDF.
    Je collecte tes infos et crée un CV
    personnalisé avec un design moderne."

5. Instructions : (copie depuis CUSTOM_GPT_GUIDE.md)

6. Actions → Import OpenAPI Schema
   - Copie le contenu de openapi_schema.json
   - REMPLACE "TON-API-URL" par ton URL réelle
   - Exemple : https://cv-api-xyz.onrender.com

7. Test ! Dis "Aide-moi à créer un CV"
```

**Étape 3 : Utiliser ton Custom GPT**

```
Toi: "Crée-moi un CV pour un poste de Data Scientist"

GPT: "Avec plaisir ! Commençons par tes informations.
      Quel est ton nom complet ?"

Toi: "Jean Dupont"

GPT: "Super ! Ton email ?"

[... Le GPT collecte toutes les infos ...]

GPT: "Parfait ! Je génère ton CV maintenant..."
     [Appelle l'API]
     "✅ Ton CV est prêt !
     📥 Télécharge-le ici : [lien]"
```

---

## 📊 Comparaison des 2 modes

| Critère | Mode Local | Mode API + GPT |
|---------|------------|----------------|
| **Facilité** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Rapidité** | ⚡ Instantané | ⚡ Instantané |
| **Setup** | 2 min | 30 min |
| **Partage** | ❌ | ✅ |
| **Interface** | Terminal | Chat GPT |
| **Automatisation** | ✅ Scripts | ✅ Conversationnel |
| **Coût** | Gratuit | Gratuit* |

*Render/Railway offrent un tier gratuit suffisant

---

## 🎨 Structure du CV généré

```
┌─────────────────────────────────────────────┐
│  COLONNE GAUCHE (Bleu)   │  COLONNE DROITE  │
│                          │                  │
│  📸 [Photo optionnelle]  │  PROFIL          │
│                          │  Description...  │
│  📧 Contact              │                  │
│  • Email                 │  EXPÉRIENCES     │
│  • Téléphone             │  ─────────────   │
│  • Localisation          │  Poste 1         │
│                          │  • Bullet 1      │
│  🌍 Langues              │  • Bullet 2      │
│  • Français              │                  │
│  • Anglais               │  Poste 2         │
│                          │  • Bullet 1      │
│  💡 Compétences clés     │                  │
│  • Stratégie IA          │  FORMATIONS      │
│  • Leadership            │  ─────────────   │
│  • Cloud                 │  Diplôme 1       │
│                          │  Description     │
│  🎨 Centres d'intérêt    │                  │
│  • Vélo                  │  Diplôme 2       │
│  • Méditation            │  Description     │
│                          │                  │
└─────────────────────────────────────────────┘
```

---

## 🔥 Cas d'usage rapides

### 📱 "Je veux un CV maintenant !"
```bash
python cv_template.py cv_content.csv mon_cv.pdf
```
⏱️ Temps : 5 secondes

### 🎯 "J'ai 3 entretiens pour 3 postes différents"
```bash
# Créer 3 versions
cp cv_content.csv cv_backend.csv
cp cv_content.csv cv_devops.csv  
cp cv_content.csv cv_lead.csv

# Modifier chaque CSV pour le poste
# Générer les 3 CV
python cv_template.py cv_backend.csv cv_backend.pdf
python cv_template.py cv_devops.csv cv_devops.pdf
python cv_template.py cv_lead.csv cv_lead.pdf
```
⏱️ Temps : 5 minutes

### 🤖 "Je veux un assistant IA pour mon équipe RH"
```
1. Déploie l'API sur Render (15 min)
2. Crée un Custom GPT (10 min)
3. Partage le GPT avec ton équipe
```
⏱️ Temps : 30 minutes setup, puis usage illimité

---

## 🆘 Aide rapide

**Problème : "Module not found"**
```bash
pip install -r requirements.txt
```

**Problème : "Le CSV ne marche pas"**
```
Vérifie :
- Les virgules sont bien placées
- Pas de virgules dans le contenu (ou entre guillemets)
- Le fichier est en UTF-8
```

**Problème : "L'API ne démarre pas"**
```bash
# Vérifie que le port 5000 est libre
lsof -i :5000

# Ou change le port
python cv_api.py  # modifie le port dans le code
```

**Problème : "Le Custom GPT ne trouve pas l'API"**
```
1. Vérifie l'URL dans openapi_schema.json
2. Teste l'API : curl https://ton-api.com/health
3. Regarde les logs sur Render/Railway
```

---

## 📚 Documentation détaillée

Pour aller plus loin, lis :

- **`README.md`** - Guide du système local
- **`CUSTOM_GPT_GUIDE.md`** - Guide complet API + GPT
- **`README_COMPLET.md`** - Vue d'ensemble totale

---

## ✨ Fonctionnalités

✅ Design professionnel 2 colonnes  
✅ Format PDF A4  
✅ Personnalisation facile via CSV  
✅ Support HTML dans le contenu  
✅ Génération en < 1 seconde  
✅ API REST avec OpenAPI 3.1.0  
✅ Compatible Custom GPT  
✅ 100% gratuit et open source  

---

**Créé avec ❤️ par Suan Tay**

Questions ? suan.tay@iafluence.fr

⭐ Si ça t'aide, star le projet !
