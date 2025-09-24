# Guide de Déploiement - Expérience Perception des Mots

## 🚀 Option 1: Railway (RECOMMANDÉ - Plus Simple)

### Étapes :
1. **Aller sur** : https://railway.app
2. **Se connecter avec GitHub**
3. **Cliquer "New Project" → "Deploy from GitHub repo"**
4. **Sélectionner votre dépôt** (ou upload le dossier web_app/)
5. **Railway détecte automatiquement** Flask et déploie
6. **Votre app sera disponible** à une URL comme : `https://votre-app.up.railway.app`

### Avantages Railway :
- ✅ Déploiement en 1 clic
- ✅ HTTPS automatique
- ✅ Base de données gratuite incluse
- ✅ Logs en temps réel
- ✅ 500h gratuites/mois

---

## 🌐 Option 2: Render (Également Simple)

### Étapes :
1. **Aller sur** : https://render.com
2. **Se connecter avec GitHub**
3. **Cliquer "New" → "Web Service"**
4. **Connecter votre dépôt GitHub**
5. **Configurer** :
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
6. **Déployer**

---

## 🔧 Option 3: Heroku (Si CLI installé)

### Après installation Heroku CLI :
```bash
heroku login
heroku create experience-perception-mots
git push heroku main
```

---

## 📁 Option 4: GitHub Pages + Backend séparé

Si vous voulez juste tester rapidement :

### Frontend seulement (GitHub Pages) :
1. Push sur GitHub
2. Activer GitHub Pages
3. Modifier le JavaScript pour utiliser un backend externe

### Backend sur Replit :
1. Créer un compte sur https://replit.com
2. Importer le code Python
3. Lancer automatiquement

---

## 🏠 Option 5: Serveur Local Accessible

Pour tester avec des participants locaux :

```bash
# Dans web_app/
python app.py
# Puis partager votre IP locale : http://VOTRE-IP:5000
```

Pour obtenir votre IP :
```bash
hostname -I
```

---

## 📊 Accès aux Résultats

Une fois déployé, les résultats seront accessibles à :
- **URL de votre app** + `/download_results`
- Exemple : `https://votre-app.railway.app/download_results`

---

## 🔒 Sécuriser l'Accès aux Résultats

Ajoutez cette route protégée dans `app.py` :

```python
@app.route('/admin/results')
def admin_results():
    password = request.args.get('password')
    if password != 'votre_mot_de_passe_secret':
        return "Accès refusé", 403
    return send_file(RESULTS_FILE, as_attachment=True)
```

Puis accédez à : `https://votre-app.com/admin/results?password=votre_mot_de_passe_secret`

---

## 🎯 Recommandation

**Railway** est le plus simple pour commencer :
1. Pas besoin d'installer de CLI
2. Interface web intuitive  
3. Déploiement automatique
4. Gratuit et fiable

Voulez-vous que je vous guide étape par étape avec Railway ?
