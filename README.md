# Expérience de Perception des Mots - Application Web

Cette application web permet de mener l'expérience de perception des mots en ligne, accessible à plusieurs participants simultanément.

[https://experience-mg57.onrender.com/](https://experience-mg57.onrender.com/ "https://experience-mg57.onrender.com/")

## Fonctionnalités

- ✅ **Multi-sessions simultanées** : Plusieurs participants peuvent faire l'expérience en même temps
- ✅ **Collecte automatique des résultats** : Sauvegarde en CSV thread-safe
- ✅ **Interface responsive** : Fonctionne sur ordinateur, tablette et mobile
- ✅ **Temps d'affichage précis** : 50ms avec JavaScript haute précision
- ✅ **Distracteurs intelligents** : Algorithme de génération de choix trompeurs
- ✅ **Résultats cachés** : Le fichier CSV n'est pas accessible publiquement

## Structure de l'application

```
web_app/
├── app.py                 # Serveur Flask principal
data/
	fichier.csv
├── templates/
│   └── index.html        # Interface utilisateur
├── static/
│   ├── style.css         # Styles CSS
│   └── script.js         # Logique JavaScript
├── requirements.txt      # Dépendances Python
├── Procfile             # Configuration Heroku
├── runtime.txt          # Version Python
└── results.csv          # Résultats (généré automatiquement)
```

## Installation locale

1. **Installer les dépendances :**

```bash
pip install -r requirements.txt
```

2. **Lancer l'application :**

```bash
python app.py
```

3. **Accéder à l'application :**
   Ouvrir http://localhost:5000 dans votre navigateur

## Déploiement en ligne

### Render (Gratuit)

1. **Créer un compte Render** : https://render.com
2. **Connecter GitHub** et sélectionner le dossier web_app/

## Utilisation

### Pour les participants :

1. Accéder à l'URL de l'application
2. Entrer un ID participant (optionnel)
3. Suivre les instructions à l'écran
4. Compléter les 3 blocs de l'expérience

### Pour le chercheur :

- **Télécharger les résultats** : Accéder à `/download_results` (vous pouvez ajouter une authentification)
- **Surveiller l'activité** : Les logs montrent les connexions en temps réel

## Format des données CSV

Le fichier `results.csv` contient les colonnes suivantes :

| Colonne           | Description                        |
| ----------------- | ---------------------------------- |
| session_id        | ID unique de session               |
| participant_id    | ID du participant                  |
| timestamp         | Horodatage de la réponse          |
| trial_number      | Numéro de l'essai (1-12)          |
| block_type        | Type de bloc (bw/color/colored_bg) |
| stimulus          | Mot/non-mot affiché               |
| response          | Réponse du participant            |
| correct           | Réponse correcte (True/False)     |
| reaction_time     | Temps de réaction (ms)            |
| text_color        | Couleur du texte                   |
| background_color  | Couleur de fond                    |
| is_word           | Vrai mot ou non-mot                |
| choices_presented | Les 4 choix proposés              |

## Sécurité

- Les résultats sont stockés côté serveur
- Le fichier CSV n'est pas accessible publiquement
- Chaque session a un ID unique
- Pas de données personnelles collectées par défaut

## Personnalisation

### Modifier les stimuli :

Éditer les listes `WORDS` et `NON_WORDS` dans `app.py`

### Changer les temps d'affichage :

Modifier `DISPLAY_TIME` dans `app.py`

### Ajouter une authentification :

Ajouter une route protégée pour `/download_results`

### Modifier l'interface :

Éditer `templates/index.html` et `static/style.css`

## Support technique

L'application est compatible avec :

- ✅ Chrome, Firefox, Safari, Edge
- ✅ Ordinateurs, tablettes, smartphones
- ✅ Connexions simultanées multiples
- ✅ Sauvegarde automatique des résultats

## Avantages par rapport à la version Pygame

1. **Accessibilité** : Aucune installation requise
2. **Multi-plateforme** : Fonctionne sur tous les appareils
3. **Collecte centralisée** : Tous les résultats dans un seul fichier
4. **Sessions simultanées** : Plusieurs participants en même temps
5. **Déploiement facile** : Hébergement gratuit disponible
6. **Interface moderne** : Design responsive et accessible
