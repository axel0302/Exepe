from flask import Flask, render_template, request, jsonify, session, send_file
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

# Données de l'expérience (reprises du code original)
WORDS = [
    "chien", "chat", "maison", "voiture", "pomme", "livre", "plage", "arbre",
    "soleil", "lune", "fleur", "oiseau", "poisson", "montagne", "rivière", "forêt",
    "table", "chaise", "fenêtre", "porte", "jardin", "école", "hôpital", "magasin"
]

NON_WORDS = [
    "chion", "chet", "maisan", "voitare", "pomne", "livro", "plago", "arbro",
    "solail", "luno", "floir", "oisiau", "poissan", "montegne", "rivièro", "forît",
    "tablo", "chaiso", "fenêtre", "porto", "jardun", "écolo", "hôpitel", "magasun"
]

ALL_STIMULI = WORDS + NON_WORDS
DISPLAY_TIME = 50  # ms

SIMILAR_DISTRACTORS = {
    "chien": ["chion", "chine", "chier", "chean", "chuen", "chien", "chies"],
    "chat": ["chet", "char", "chant", "chot", "chats", "cha", "chad"],
    "maison": ["maisan", "mason", "raison", "saison", "maisen", "maisons", "maisan"],
    "voiture": ["voitare", "voitere", "voitures", "voitire", "voitune", "voitore"],
    "pomme": ["pomne", "homme", "somme", "comme", "pommen", "pommes", "porme"],
    "livre": ["livro", "libre", "litre", "lièvre", "livri", "livres", "livne"],
    "plage": ["plago", "place", "image", "rage", "plege", "plages", "plabe"],
    "arbre": ["arbro", "marbre", "sabre", "libre", "arbri", "arbres", "arbre"],
    "soleil": ["solail", "sommeil", "conseil", "réveil", "soliel", "soleils", "soleal"],
    "lune": ["luno", "dune", "prune", "rune", "lene", "lunes", "lune"],
    "fleur": ["floir", "pleur", "coeur", "peur", "fluer", "fleurs", "fleur"],
    "oiseau": ["oisiau", "roseau", "bateau", "château", "oiseaux", "oisiau", "oiseau"],
    "poisson": ["poissan", "boisson", "moisson", "poison", "poissons", "poissen", "poisson"],
    "montagne": ["montegne", "campagne", "compagne", "bretagne", "montagnes", "montegni"],
    "rivière": ["rivièro", "carrière", "barrière", "matière", "rivières", "rivièri"],
    "forêt": ["forît", "secret", "regret", "projet", "forêts", "forêt"],
    "table": ["tablo", "stable", "sable", "fable", "tabli", "tables", "table"],
    "chaise": ["chaiso", "fraise", "braise", "caisse", "cheise", "chaises", "chaise"],
    "fenêtre": ["fenître", "centre", "ventre", "rentre", "fenêtres", "fenetre"],
    "porte": ["porto", "forte", "sorte", "morte", "parti", "portes", "porte"],
    "jardin": ["jardun", "marin", "martin", "pardin", "jardien", "jardins", "jardin"],
    "école": ["écolo", "parole", "rigole", "écoli", "écoles", "école"],
    "hôpital": ["hôpitel", "capital", "digital", "vital", "hôpitaux", "hôpital"],
    "magasin": ["magasun", "raisin", "bassin", "cousin", "magesen", "magasins", "magasin"],
    # Non-mots avec leurs distracteurs
    "chion": ["chien", "chine", "chier", "chean", "chuen"],
    "chet": ["chat", "char", "chant", "chot", "chet"],
    "maisan": ["maison", "mason", "raison", "saison", "maisen"],
    "voitare": ["voiture", "voitere", "culture", "nature", "voitire"],
    "pomne": ["pomme", "homme", "somme", "comme", "pommen"],
    "livro": ["livre", "libre", "litre", "lièvre", "livri"],
    "plago": ["plage", "place", "image", "rage", "plege"],
    "arbro": ["arbre", "marbre", "sabre", "libre", "arbri"],
    "solail": ["soleil", "sommeil", "conseil", "réveil", "soliel"],
    "luno": ["lune", "dune", "prune", "rune", "lene"],
    "floir": ["fleur", "pleur", "coeur", "peur", "fluer"],
    "oisiau": ["oiseau", "roseau", "bateau", "château", "oisiau"],
    "poissan": ["poisson", "boisson", "moisson", "poison", "poissen"],
    "montegne": ["montagne", "campagne", "compagne", "bretagne", "montegni"],
    "rivièro": ["rivière", "carrière", "barrière", "matière", "rivièri"],
    "forît": ["forêt", "secret", "regret", "projet", "forêt"],
    "tablo": ["table", "stable", "sable", "fable", "tabli"],
    "chaiso": ["chaise", "fraise", "braise", "caisse", "cheise"],
    "fenître": ["fenêtre", "centre", "ventre", "rentre", "fenetre"],
    "porto": ["porte", "forte", "sorte", "morte", "parti"],
    "jardun": ["jardin", "marin", "martin", "pardin", "jardien"],
    "écolo": ["école", "parole", "rigole", "école", "écoli"],
    "hôpitel": ["hôpital", "capital", "digital", "vital", "hôpitel"],
    "magasun": ["magasin", "raisin", "bassin", "cousin", "magesen"]
}

COLOR_ASSOCIATED_WORDS = {
    "rouge": ["sang", "tomate", "rose", "cerise", "feu"],
    "vert": ["herbe", "salade", "forêt", "nature", "pomme"],
    "bleu": ["ciel", "mer", "océan", "bleuet", "saphir"],
    "jaune": ["soleil", "citron", "banane", "or", "blé"],
}

COLORS = {
    "noir": "#000000",
    "rouge": "#FF0000",
    "vert": "#00C800",
    "bleu": "#0000FF",
    "jaune": "#FFFF00",
}

BACKGROUND_COLORS = [
    "#C8C8C8",  # gris prononcé
    "#FFB4B4",  # rose prononcé
    "#B4FFB4",  # vert prononcé
    "#B4B4FF",  # bleu prononcé
    "#FFFFB4",  # jaune prononcé
    "#FFC8FF",  # magenta prononcé
    "#C8FFFF",  # cyan prononcé
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
        with open(RESULTS_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                session_id,
                participant_id,
                datetime.datetime.now().isoformat(),
                trial_data['trial_number'],
                trial_data['block_type'],
                trial_data['stimulus'],
                trial_data['response'],
                trial_data['correct'],
                trial_data['reaction_time'],
                trial_data['text_color'],
                trial_data['background_color'],
                trial_data['is_word'],
                '|'.join(trial_data['choices'])
            ])

def get_choices(correct_stimulus, n=4, with_color_word=False):
    """Génère des choix très difficiles pour induire en erreur maximale."""
    choices = [correct_stimulus]
    
    color_names = ["rouge", "vert", "bleu", "jaune", "noir", "blanc", "rose", "violet", "orange", "marron"]
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

@app.route('/submit_response', methods=['POST'])
def submit_response():
    """Enregistre la réponse d'un participant."""
    if 'session_id' not in session:
        return jsonify({'error': 'Session non initialisée'}), 400
    
    data = request.json
    
    trial_data = {
        'trial_number': data['trial_number'],
        'block_type': data['block_type'],
        'stimulus': data['stimulus'],
        'response': data['response'],
        'correct': data['response'] == data['stimulus'],
        'reaction_time': data['reaction_time'],
        'text_color': data['text_color'],
        'background_color': data['background_color'],
        'is_word': data['is_word'],
        'choices': data['choices']
    }
    
    # Sauvegarder dans le CSV
    save_result(session['session_id'], session.get('participant_id', 'anonymous'), trial_data)
    
    return jsonify({
        'success': True,
        'correct': trial_data['correct']
    })

@app.route('/admin')
def admin_login():
    """Page de connexion administrateur."""
    return render_template('admin_login.html')

@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    """Tableau de bord administrateur avec tous les résultats."""
    # Protection basique - vous pouvez améliorer cela
    if request.method == 'POST':
        password = request.form.get('password')
        if password != 'admin123':  # Changez ce mot de passe !
            return render_template('admin_login.html', error='Mot de passe incorrect')
    elif 'admin_authenticated' not in session:
        return render_template('admin_login.html')
    
    session['admin_authenticated'] = True
    
    if not os.path.exists(RESULTS_FILE):
        return render_template('admin_dashboard.html', results=[], stats={})
    
    # Lire tous les résultats
    results = []
    with open(RESULTS_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append(row)
    
    # Calculer les statistiques par bloc
    stats = calculate_block_statistics(results)
    
    return render_template('admin_dashboard.html', results=results, stats=stats)

@app.route('/download_results')
def download_results():
    """Télécharge les résultats (accès protégé)."""
    if 'admin_authenticated' not in session:
        return "Accès non autorisé", 403
    
    if os.path.exists(RESULTS_FILE):
        return send_file(RESULTS_FILE, as_attachment=True, download_name=f'results_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
    else:
        return "Aucun résultat disponible", 404

def calculate_block_statistics(results):
    """Calcule les statistiques par bloc."""
    stats = {}
    
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
            
        # Temps de réaction moyen
        reaction_times = [float(r.get('reaction_time', 0)) for r in block_results if r.get('reaction_time')]
        avg_reaction_time = sum(reaction_times) / len(reaction_times) if reaction_times else 0
        
        # Pourcentage de bonnes réponses
        correct_answers = [r for r in block_results if r.get('correct', '').lower() == 'true']
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
    
    return stats

if __name__ == '__main__':
    init_csv()
    app.run(debug=True, host='0.0.0.0', port=5000)
