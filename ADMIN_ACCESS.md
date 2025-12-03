# 🔐 Accès Administrateur - Résultats Expérience

## Comment accéder aux résultats sur Railway

### 1. URL d'accès
Une fois votre application déployée sur Railway, accédez à :
```
https://experience-mg57.onrender.com/admin
```

### 2. Connexion
- **Mot de passe par défaut** : `admin123`
- ⚠️ **IMPORTANT** : Changez ce mot de passe dans le fichier `app.py` ligne 319

### 3. Fonctionnalités disponibles

#### 📊 Statistiques par bloc
- **Bloc 1** (Noir/Blanc) : Précision + Temps moyen
- **Bloc 2** (Couleurs) : Précision + Temps moyen  
- **Bloc 3** (Fonds colorés) : Précision + Temps moyen

#### 📋 Tableau détaillé
Pour chaque réponse de chaque participant :
- ID Participant (généré automatiquement)
- Session ID
- Date et heure
- Bloc et numéro d'essai
- Stimulus présenté
- Réponse donnée
- Correct/Incorrect
- Temps de réaction (ms)
- Couleurs utilisées
- Type (Mot/Non-mot)

#### 📥 Export CSV
- Téléchargement direct des données
- Format compatible Excel/Google Sheets
- Toutes les colonnes incluses

### 4. Sécurité

#### Changer le mot de passe
Dans `app.py`, ligne 319, remplacez :
```python
if password != 'admin123':  # Changez ce mot de passe !
```

Par :
```python
if password != 'VOTRE_MOT_DE_PASSE_SECURISE':
```

#### Améliorer la sécurité (optionnel)
Pour une sécurité renforcée, vous pouvez :
1. Utiliser des variables d'environnement
2. Ajouter une authentification par utilisateur
3. Implémenter des sessions avec expiration

### 5. Actualisation automatique
- La page se rafraîchit automatiquement toutes les 30 secondes
- Bouton "Actualiser" disponible pour un refresh manuel

### 6. Responsive Design
- Interface adaptée aux mobiles et tablettes
- Tableau scrollable horizontalement
- Cartes statistiques empilées sur petits écrans

---

## 🚀 Déploiement sur Railway

1. Commitez tous les fichiers
2. Poussez vers votre repository
3. Railway détectera automatiquement les changements
4. L'interface admin sera disponible à `/admin`

## 📱 Accès mobile
L'interface est optimisée pour tous les appareils. Vous pouvez consulter les résultats depuis votre téléphone.
