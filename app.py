from flask import Flask, render_template, request, jsonify, session, send_file, redirect, url_for
import csv
import os
import uuid
import datetime
import random
import threading
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'experience_perception_mots_couleurs_2024'

# Configuration
RESULTS_FILE = 'results.csv'
RESULTS_LOCK = threading.Lock()

# Mots réels français
REAL_WORDS = [
    "chien", "chat", "maison", "voiture", "pomme", "livre", "plage", "arbre", 
    "soleil", "lune", "fleur", "oiseau", "poisson", "montagne", "rivière", 
    "forêt", "table", "chaise", "fenêtre", "porte", "jardin", "école", 
    "hôpital", "magasin"
]

# Non-mots avec lettres complètement aléatoires
FAKE_WORDS = [
    "blixor", "frunez", "glopek", "tralux", "vokrim", "zephiq", "quilmex", 
    "braxon", "flumig", "krenov", "doltex", "prixel", "vextor", "glumix", 
    "tronez", "blefox", "krimol", "floxen", "vraliq", "gextom", "pluvex", 
    "drixel", "blomek", "kraxon"
]

# Données de l'expérience
WORDS = REAL_WORDS
NON_WORDS = FAKE_WORDS
ALL_STIMULI = WORDS + NON_WORDS
DISPLAY_TIME = 50  # ms

SIMILAR_DISTRACTORS = {}

COLOR_ASSOCIATED_WORDS = {
    "rouge": ["sang", "tomate", "rose", "cerise", "feu"],
    "vert": ["herbe", "salade", "forêt", "nature", "pomme"],
    "bleu": ["ciel", "mer", "océan", "bleuet", "saphir"],
    "violet": ["lavande", "prune", "aubergine", "lilas", "améthyste"],
    "orange": ["carotte", "citrouille", "abricot", "mandarine", "flamme"],
}

COLORS = {
    "rouge": "#FF0000",
    "vert": "#00C800", 
    "bleu": "#0000FF",
    "violet": "#8B00FF",
    "orange": "#FF6600",
}

BACKGROUND_COLORS = [
    "#FF4444",  # rouge vif
    "#44FF44",  # vert vif
    "#4444FF",  # bleu vif
    "#FF44FF",  # magenta vif
    "#44FFFF",  # cyan vif
    "#FF8800",  # orange vif
    "#8844FF",  # violet vif
]

def init_csv():
    """Initialise le fichier CSV avec les en-têtes si il n'existe pas."""
    if not os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'session_id', 'participant_id', 'timestamp', 'trial_number', 'block_type',
                'stimulus', 'response', 'correct', 'reaction_time', 'text_color', 
                'background_color', 'is_word', 'choices_presented'
            ])

def save_result(session_id, participant_id, trial_data):
    """Sauvegarde un résultat dans le fichier CSV de manière thread-safe."""
    with RESULTS_LOCK:
        # S'assurer que le fichier existe
        init_csv()
        
        with open(RESULTS_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Gérer les choix (peut être une liste ou None)
            choices_str = ''
            if 'choices' in trial_data and trial_data['choices']:
                if isinstance(trial_data['choices'], list):
                    choices_str = '|'.join(trial_data['choices'])
                else:
                    choices_str = str(trial_data['choices'])
            
            writer.writerow([
                session_id,
                participant_id,
                trial_data.get('timestamp', datetime.datetime.now().isoformat()),
                trial_data.get('trial_number', ''),
                trial_data.get('block_type', ''),
                trial_data.get('stimulus', ''),
                trial_data.get('response', ''),
                trial_data.get('correct', False),
                trial_data.get('reaction_time', 0),
                trial_data.get('text_color', '#000000'),
                trial_data.get('background_color', '#ffffff'),
                trial_data.get('is_word', False),
                choices_str
            ])
            
        print(f"✅ Résultat sauvegardé: {participant_id[:8]}... - {trial_data.get('stimulus', 'N/A')} - {trial_data.get('correct', 'N/A')}")

def get_choices(correct_stimulus, n=4, with_color_word=False):
    """Génère des choix très difficiles pour induire en erreur maximale."""
    choices = [correct_stimulus]
    
    color_names = ["rouge", "vert", "bleu", "violet", "orange", "rose", "magenta", "cyan", "turquoise", "indigo"]
    potential_distractors = []
    
    # 1. Ajouter des distracteurs très similaires
    if correct_stimulus in SIMILAR_DISTRACTORS:
        similar = [w for w in SIMILAR_DISTRACTORS[correct_stimulus] if w != correct_stimulus]
        potential_distractors.extend(similar[:2])
    
    # 2. Correspondance mot/non-mot
    if correct_stimulus in WORDS:
        word_index = WORDS.index(correct_stimulus)
        if word_index < len(NON_WORDS):
            corresponding_nonword = NON_WORDS[word_index]
            if corresponding_nonword != correct_stimulus:
                potential_distractors.append(corresponding_nonword)
    elif correct_stimulus in NON_WORDS:
        nonword_index = NON_WORDS.index(correct_stimulus)
        if nonword_index < len(WORDS):
            corresponding_word = WORDS[nonword_index]
            if corresponding_word != correct_stimulus:
                potential_distractors.append(corresponding_word)
    
    # 3. Mots associés aux couleurs
    if with_color_word:
        for color_word_list in COLOR_ASSOCIATED_WORDS.values():
            color_words = [w for w in color_word_list if w != correct_stimulus]
            potential_distractors.extend(color_words[:1])
        
        available_colors = [c for c in color_names if c != correct_stimulus]
        potential_distractors.extend(available_colors[:1])
    
    # 4. Stimuli similaires visuellement
    same_length = [w for w in ALL_STIMULI if w != correct_stimulus and len(w) == len(correct_stimulus)]
    similar_visual = []
    for word in same_length:
        common_letters = sum(1 for i, char in enumerate(word) if i < len(correct_stimulus) and char == correct_stimulus[i])
        if common_letters >= 2:
            similar_visual.append(word)
    potential_distractors.extend(similar_visual[:2])
    
    # 5. Mots qui commencent/finissent pareil
    if len(correct_stimulus) >= 3:
        same_start = [w for w in ALL_STIMULI if w != correct_stimulus and len(w) >= 3 and w[:2] == correct_stimulus[:2]]
        same_end = [w for w in ALL_STIMULI if w != correct_stimulus and len(w) >= 3 and w[-2:] == correct_stimulus[-2:]]
        potential_distractors.extend(same_start[:1])
        potential_distractors.extend(same_end[:1])
    
    # Supprimer les doublons
    seen = set([correct_stimulus])
    unique_distractors = []
    for item in potential_distractors:
        if item not in seen:
            unique_distractors.append(item)
            seen.add(item)
    
    # Sélectionner exactement n-1 distracteurs
    if len(unique_distractors) >= n-1:
        selected_distractors = random.sample(unique_distractors, n-1)
    else:
        selected_distractors = unique_distractors
        remaining = [w for w in ALL_STIMULI if w not in seen]
        while len(selected_distractors) < n-1 and remaining:
            choice = random.choice(remaining)
            selected_distractors.append(choice)
            remaining.remove(choice)
    
    # Construire la liste finale
    final_choices = [correct_stimulus] + selected_distractors
    random.shuffle(final_choices)
    
    # Vérification critique
    if correct_stimulus not in final_choices:
        final_choices[0] = correct_stimulus
    
    return final_choices[:n]

@app.route('/')
def index():
    """Page d'accueil de l'expérience."""
    return render_template('index.html')

@app.route('/start_experiment', methods=['POST'])
def start_experiment():
    """Démarre une nouvelle session d'expérience."""
    session['session_id'] = str(uuid.uuid4())
    session['participant_id'] = str(uuid.uuid4())  # Génération automatique de l'ID participant
    session['current_block'] = 0
    session['current_trial'] = 0
    session['results'] = []
    
    return jsonify({
        'success': True,
        'session_id': session['session_id'],
        'participant_id': session['participant_id']  # Retourner l'ID généré
    })

@app.route('/get_trial', methods=['POST'])
def get_trial():
    """Génère un nouvel essai pour l'expérience."""
    if 'session_id' not in session:
        return jsonify({'error': 'Session non initialisée'}), 400
    
    data = request.json
    block_type = data.get('block_type', 'bw')  # bw, color, colored_bg
    trial_number = data.get('trial_number', 1)
    
    # Sélectionner un stimulus
    stimulus = random.choice(ALL_STIMULI)
    
    # Déterminer les couleurs selon le bloc
    if block_type == 'colored_bg':
        text_color = random.choice(list(COLORS.values()))
        background_color = random.choice(BACKGROUND_COLORS)
    elif block_type == 'color':
        text_color = random.choice(list(COLORS.values()))
        background_color = "#FFFFFF"
    else:  # bw
        text_color = "#000000"
        background_color = "#FFFFFF"
    
    # Générer les choix
    with_color = block_type in ['color', 'colored_bg']
    choices = get_choices(stimulus, n=4, with_color_word=with_color)
    
    return jsonify({
        'stimulus': stimulus,
        'text_color': text_color,
        'background_color': background_color,
        'choices': choices,
        'display_time': DISPLAY_TIME,
        'is_word': stimulus in WORDS
    })

@app.route('/submit_trial', methods=['POST'])
def submit_trial():
    """Soumet un essai et retourne le feedback."""
    data = request.json
    
    # Récupérer les données de l'essai
    trial_data = {
        'timestamp': datetime.datetime.now().isoformat(),
        'block_type': data.get('block_type'),
        'trial_number': data.get('trial_number'),
        'stimulus': data.get('stimulus'),
        'response': data.get('response'),
        'correct': data.get('correct'),
        'reaction_time': data.get('reaction_time'),
        'text_color': data.get('text_color'),
        'background_color': data.get('background_color'),
        'is_word': data.get('is_word'),
        'choices': data.get('choices', [])
    }
    
    # Sauvegarder dans le CSV
    save_result(session['session_id'], session.get('participant_id', 'anonymous'), trial_data)
    
    return jsonify({
        'success': True,
        'correct': trial_data['correct']
    })

@app.route('/save_result', methods=['POST'])
def save_result_endpoint():
    """Sauvegarde un résultat envoyé par le client."""
    try:
        data = request.json
        print(f"📥 Réception données: {data}")
        
        # Récupérer les données du résultat
        result_data = {
            'timestamp': datetime.datetime.now().isoformat(),
            'participant_id': session.get('participant_id', 'anonymous'),
            'session_id': session.get('session_id', 'unknown'),
            'block_type': data.get('block', 'unknown'),
            'trial_number': data.get('trial', 0),
            'stimulus': data.get('stimulus', ''),
            'response': data.get('response', ''),
            'correct': str(data.get('correct', False)).lower(),
            'reaction_time': data.get('reactionTime', 0),
            'text_color': data.get('textColor', '#000000'),
            'background_color': data.get('backgroundColor', '#ffffff'),
            'is_word': str(data.get('stimulus', '') in WORDS).lower(),
            'choices': data.get('choices', [])
        }
        
        # Sauvegarder dans le CSV
        save_result(session.get('session_id', 'unknown'), session.get('participant_id', 'anonymous'), result_data)
        
        return jsonify({'success': True, 'message': 'Données sauvegardées avec succès'})
        
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/test_csv')
def test_csv():
    """Route de test pour vérifier la création du CSV."""
    try:
        init_csv()
        
        # Créer un résultat de test
        test_data = {
            'timestamp': datetime.datetime.now().isoformat(),
            'trial_number': 1,
            'block_type': 'test',
            'stimulus': 'test_word',
            'response': 'test_response',
            'correct': True,
            'reaction_time': 500,
            'text_color': '#000000',
            'background_color': '#ffffff',
            'is_word': True,
            'choices': ['test_word', 'choice2', 'choice3', 'choice4']
        }
        
        save_result('test_session', 'test_participant', test_data)
        
        return jsonify({
            'success': True, 
            'message': 'Test CSV réussi',
            'file_exists': os.path.exists(RESULTS_FILE),
            'file_path': os.path.abspath(RESULTS_FILE)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/admin')
@app.route('/admin/')
def admin_login():
    """Page de connexion administrateur."""
    # Si déjà authentifié, rediriger vers le dashboard
    if 'admin_authenticated' in session:
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html')

@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    """Tableau de bord administrateur avec tous les résultats."""
    # Protection basique - vous pouvez améliorer cela
    if request.method == 'POST':
        password = request.form.get('password')
        if password != 'admin123':  # Changez ce mot de passe !
            return render_template('admin_login.html', error='Mot de passe incorrect')
        else:
            session['admin_authenticated'] = True
    elif 'admin_authenticated' not in session:
        return render_template('admin_login.html')
    
    if not os.path.exists(RESULTS_FILE):
        return render_template('admin_dashboard.html', results=[], stats={})
    
    # Lire tous les résultats avec gestion d'erreur
    results = []
    try:
        with open(RESULTS_FILE, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # S'assurer que toutes les clés nécessaires existent
                safe_row = {
                    'participant_id': row.get('participant_id', 'N/A'),
                    'session_id': row.get('session_id', 'N/A'),
                    'timestamp': row.get('timestamp', 'N/A'),
                    'block_type': row.get('block_type', 'unknown'),
                    'trial_number': row.get('trial_number', 'N/A'),
                    'stimulus': row.get('stimulus', 'N/A'),
                    'response': row.get('response', 'N/A'),
                    'correct': row.get('correct', 'false'),
                    'reaction_time': row.get('reaction_time', 'N/A'),
                    'text_color': row.get('text_color', '#000000'),
                    'background_color': row.get('background_color', '#ffffff'),
                    'is_word': row.get('is_word', 'false')
                }
                results.append(safe_row)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier CSV: {e}")
        return render_template('admin_dashboard.html', results=[], stats={}, error="Erreur lors de la lecture des données")
    
    # Calculer les statistiques par bloc
    stats = calculate_block_statistics(results)
    
    return render_template('admin_dashboard.html', results=results, stats=stats)

@app.route('/download_results')
def download_results():
    """Télécharge les résultats (accès protégé)."""
    if 'admin_authenticated' not in session:
        return "Accès non autorisé", 403
    
    # S'assurer que le fichier existe
    init_csv()
    
    if os.path.exists(RESULTS_FILE):
        filename = f'experience_results_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        return send_file(RESULTS_FILE, as_attachment=True, download_name=filename)
    else:
        return "Aucun résultat disponible", 404

@app.route('/csv_status')
def csv_status():
    """Vérifie le statut du fichier CSV."""
    try:
        init_csv()
        file_exists = os.path.exists(RESULTS_FILE)
        file_size = os.path.getsize(RESULTS_FILE) if file_exists else 0
        
        # Compter les lignes
        line_count = 0
        if file_exists:
            with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
                line_count = sum(1 for line in f) - 1  # -1 pour l'en-tête
        
        return jsonify({
            'file_exists': file_exists,
            'file_path': os.path.abspath(RESULTS_FILE),
            'file_size': file_size,
            'entries_count': max(0, line_count),
            'last_modified': datetime.datetime.fromtimestamp(os.path.getmtime(RESULTS_FILE)).isoformat() if file_exists else None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def calculate_block_statistics(results):
    """Calcule les statistiques par bloc."""
    stats = {}
    
    try:
        # Grouper par bloc
        blocks = {'bw': [], 'color': [], 'colored_bg': []}
        block_names = {'bw': 'Bloc 1: Noir/Blanc', 'color': 'Bloc 2: Couleurs', 'colored_bg': 'Bloc 3: Fonds colorés'}
        
        for result in results:
            block_type = result.get('block_type', '')
            if block_type in blocks:
                blocks[block_type].append(result)
        
        # Calculer les stats pour chaque bloc
        for block_type, block_results in blocks.items():
            if not block_results:
                continue
                
            # Temps de réaction moyen (avec gestion d'erreurs)
            reaction_times = []
            for r in block_results:
                try:
                    rt = r.get('reaction_time', '0')
                    if rt and str(rt).replace('.', '').isdigit():
                        reaction_times.append(float(rt))
                except (ValueError, TypeError):
                    continue
            
            avg_reaction_time = sum(reaction_times) / len(reaction_times) if reaction_times else 0
            
            # Pourcentage de bonnes réponses
            correct_answers = [r for r in block_results if str(r.get('correct', '')).lower() == 'true']
            accuracy = (len(correct_answers) / len(block_results)) * 100 if block_results else 0
            
            # Nombre total d'essais
            total_trials = len(block_results)
            
            stats[block_type] = {
                'name': block_names[block_type],
                'total_trials': total_trials,
                'correct_answers': len(correct_answers),
                'accuracy': round(accuracy, 1),
                'avg_reaction_time': round(avg_reaction_time, 0)
            }
    
    except Exception as e:
        print(f"Erreur dans calculate_block_statistics: {e}")
        # Retourner des stats vides en cas d'erreur
        stats = {}
    
    return stats

if __name__ == '__main__':
    init_csv()
    app.run(debug=True, host='0.0.0.0', port=5000)
