import pygame
import random
import time
import sys

# -------------------
# Paramètres
# -------------------
# Mots réels
WORDS = [
    "chien", "chat", "maison", "voiture", "pomme", "livre", "plage", "arbre",
    "soleil", "lune", "fleur", "oiseau", "poisson", "montagne", "rivière", "forêt",
    "table", "chaise", "fenêtre", "porte", "jardin", "école", "hôpital", "magasin"
]

# Non-mots (pseudomots qui ressemblent à des mots français)
NON_WORDS = [
    "chion", "chet", "maisan", "voitare", "pomne", "livro", "plago", "arbro",
    "solail", "luno", "floir", "oisiau", "poissan", "montegne", "rivièro", "forît",
    "tablo", "chaiso", "fenêtre", "porto", "jardun", "écolo", "hôpitel", "magasun"
]

# Tous les stimuli (mots + non-mots)
ALL_STIMULI = WORDS + NON_WORDS

# Temps d'affichage fixe
DISPLAY_TIME = 50  # ms

# Distracteurs très similaires pour induire en erreur (mots et non-mots)
SIMILAR_DISTRACTORS = {
    # Mots réels avec distracteurs très trompeurs
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

# Mots associés aux couleurs pour l'effet Stroop
COLOR_ASSOCIATED_WORDS = {
    (255, 0, 0): ["sang", "tomate", "rose", "cerise", "feu"],  # rouge
    (0, 200, 0): ["herbe", "salade", "forêt", "nature", "pomme"],  # vert
    (0, 0, 255): ["ciel", "mer", "océan", "bleuet", "saphir"],  # bleu
    (255, 255, 0): ["soleil", "citron", "banane", "or", "blé"],  # jaune
}

COLORS = {
    "noir": (0, 0, 0),
    "rouge": (255, 0, 0),
    "vert": (0, 200, 0),
    "bleu": (0, 0, 255),
    "jaune": (255, 255, 0),
}
BACKGROUND = (255, 255, 255)  # fond blanc

# Couleurs de fond pour le bloc 3 - plus prononcées
BACKGROUND_COLORS = [
    (200, 200, 200),  # gris prononcé
    (255, 180, 180),  # rose prononcé
    (180, 255, 180),  # vert prononcé
    (180, 180, 255),  # bleu prononcé
    (255, 255, 180),  # jaune prononcé
    (255, 200, 255),  # magenta prononcé
    (200, 255, 255),  # cyan prononcé
]
# Plus de variable DISPLAY_TIMES - temps fixe à 40ms

# -------------------
# Initialisation Pygame
# -------------------
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Expérience perception des mots et couleurs")

# Obtenir les dimensions de l'écran
screen_width, screen_height = screen.get_size()
center_x, center_y = screen_width // 2, screen_height // 2

font = pygame.font.SysFont("Arial", 80)
font_small = pygame.font.SysFont("Arial", 30)

clock = pygame.time.Clock()

def show_fixation_cross(duration=1000, background_color=BACKGROUND):
    """Affiche une croix de fixation au centre de l'écran."""
    screen.fill(background_color)
    cross_size = 20
    cross_thickness = 3
    cross_color = (0, 0, 0)
    
    # Ligne horizontale
    pygame.draw.rect(screen, cross_color, 
                    (center_x - cross_size//2, center_y - cross_thickness//2, 
                     cross_size, cross_thickness))
    # Ligne verticale
    pygame.draw.rect(screen, cross_color, 
                    (center_x - cross_thickness//2, center_y - cross_size//2, 
                     cross_thickness, cross_size))
    
    pygame.display.flip()
    pygame.time.delay(duration)

def show_word(word, color, duration, background_color=BACKGROUND):
    """Affiche un mot à l'écran pendant 'duration' ms."""
    screen.fill(background_color)
    text_surface = font.render(word, True, color)
    rect = text_surface.get_rect(center=(center_x, center_y))
    screen.blit(text_surface, rect)
    pygame.display.flip()
    pygame.time.delay(duration)
    
    # Plus de retour à la croix après le mot - passage direct aux choix

def get_choices(correct_stimulus, n=4, with_color_word=False, display_color=None):
    """Génère des choix très difficiles pour induire en erreur maximale."""
    # GARANTIR que la bonne réponse est toujours incluse
    choices = [correct_stimulus]
    
    # Noms de couleurs pour créer des pièges
    color_names = ["rouge", "vert", "bleu", "jaune", "noir", "blanc", "rose", "violet", "orange", "marron"]
    
    # Créer une liste de distracteurs potentiels
    potential_distractors = []
    
    # 1. Ajouter des distracteurs très similaires (priorité maximale)
    if correct_stimulus in SIMILAR_DISTRACTORS:
        similar = [w for w in SIMILAR_DISTRACTORS[correct_stimulus] if w != correct_stimulus]
        potential_distractors.extend(similar[:2])  # Réduire à 2 pour faire place à plus de variété
    
    # 2. Si c'est un mot réel, ajouter son non-mot correspondant (et vice versa)
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
    
    # 3. Ajouter des mots associés à la couleur si c'est un bloc couleur
    if with_color_word and display_color and display_color in COLOR_ASSOCIATED_WORDS:
        color_words = [w for w in COLOR_ASSOCIATED_WORDS[display_color] if w != correct_stimulus]
        potential_distractors.extend(color_words[:1])  # Réduire à 1 mot de couleur
    
    # 4. Ajouter des noms de couleurs comme pièges
    if with_color_word:
        available_colors = [c for c in color_names if c != correct_stimulus]
        potential_distractors.extend(available_colors[:1])  # Réduire à 1 nom de couleur
    
    # 5. Ajouter des stimuli très similaires visuellement (même longueur et lettres communes)
    same_length = [w for w in ALL_STIMULI if w != correct_stimulus and len(w) == len(correct_stimulus)]
    # Privilégier ceux qui partagent des lettres communes
    similar_visual = []
    for word in same_length:
        common_letters = sum(1 for i, char in enumerate(word) if i < len(correct_stimulus) and char == correct_stimulus[i])
        if common_letters >= 2:  # Au moins 2 lettres en commun à la même position
            similar_visual.append(word)
    potential_distractors.extend(similar_visual[:2])  # Max 2 visuellement similaires
    
    # 6. Ajouter des mots qui commencent ou finissent pareil
    same_start = [w for w in ALL_STIMULI if w != correct_stimulus and len(w) >= 3 and w[:2] == correct_stimulus[:2]]
    same_end = [w for w in ALL_STIMULI if w != correct_stimulus and len(w) >= 3 and w[-2:] == correct_stimulus[-2:]]
    potential_distractors.extend(same_start[:1])  # 1 qui commence pareil
    potential_distractors.extend(same_end[:1])   # 1 qui finit pareil
    
    # 7. Ajouter quelques stimuli de même longueur restants
    remaining_same_length = [w for w in same_length if w not in potential_distractors]
    potential_distractors.extend(remaining_same_length[:2])  # Compléter avec d'autres de même longueur
    
    # Supprimer les doublons tout en gardant l'ordre
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
        # Compléter avec des stimuli aléatoires si nécessaire
        remaining = [w for w in ALL_STIMULI if w not in seen]
        while len(selected_distractors) < n-1 and remaining:
            choice = random.choice(remaining)
            selected_distractors.append(choice)
            remaining.remove(choice)
    
    # Construire la liste finale
    final_choices = [correct_stimulus] + selected_distractors
    
    # Mélanger les choix
    random.shuffle(final_choices)
    
    # VÉRIFICATION CRITIQUE : S'assurer que la bonne réponse est présente
    if correct_stimulus not in final_choices:
        print(f"ERREUR: La bonne réponse '{correct_stimulus}' n'est pas dans les choix!")
        final_choices[0] = correct_stimulus  # Forcer l'inclusion
    
    return final_choices[:n]

def show_instructions(text_lines, wait_for_key=True):
    """Affiche des instructions à l'écran."""
    screen.fill(BACKGROUND)
    title_font = pygame.font.SysFont("Arial", 40, bold=True)
    
    # Commencer plus haut sur l'écran
    y_offset = screen_height // 4
    for i, line in enumerate(text_lines):
        if i == 0:  # Titre
            text_surface = title_font.render(line, True, (0, 0, 0))
        else:
            text_surface = font_small.render(line, True, (0, 0, 0))
        
        rect = text_surface.get_rect(center=(center_x, y_offset))
        screen.blit(text_surface, rect)
        y_offset += 50 if i == 0 else 35
    
    if wait_for_key:
        instruction = font_small.render("Appuyez sur ESPACE pour continuer...", True, (100, 100, 100))
        rect = instruction.get_rect(center=(center_x, screen_height - 100))
        screen.blit(instruction, rect)
    
    pygame.display.flip()
    
    if wait_for_key:
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:  # Permettre de quitter avec Échap
                        pygame.quit()
                        sys.exit()

def show_choices(choices, duration_ms=None):
    """Affiche les choix de réponse et attend la saisie clavier 1-4."""
    screen.fill(BACKGROUND)
    
    # Afficher la question avec emphasis sur la rapidité
    question = "Quel mot avez-vous vu ? (Répondez RAPIDEMENT !)"
    
    question_surface = font_small.render(question, True, (0, 0, 0))
    question_rect = question_surface.get_rect(center=(center_x, center_y - 150))
    screen.blit(question_surface, question_rect)
    
    # Afficher les choix centrés
    choice_start_y = center_y - 60
    for i, choice in enumerate(choices):
        txt = font_small.render(f"{i+1}. {choice}", True, (0, 0, 0))
        txt_rect = txt.get_rect(center=(center_x, choice_start_y + i * 40))
        screen.blit(txt, txt_rect)
    
    # Instructions avec emphasis sur la rapidité
    instruction = pygame.font.SysFont("Arial", 20).render("Utilisez les touches 1-4 pour répondre RAPIDEMENT", True, (100, 100, 100))
    instruction_rect = instruction.get_rect(center=(center_x, center_y + 120))
    screen.blit(instruction, instruction_rect)
    
    # Instruction supplémentaire sur la rapidité
    speed_instruction = pygame.font.SysFont("Arial", 18, bold=True).render("VITESSE = PRIORITÉ !", True, (200, 0, 0))
    speed_rect = speed_instruction.get_rect(center=(center_x, center_y + 145))
    screen.blit(speed_instruction, speed_rect)
    
    # Ajouter instruction pour quitter
    quit_instruction = pygame.font.SysFont("Arial", 16).render("Appuyez sur ÉCHAP pour quitter", True, (150, 150, 150))
    quit_rect = quit_instruction.get_rect(center=(center_x, screen_height - 50))
    screen.blit(quit_instruction, quit_rect)
    
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    return choices[event.key - pygame.K_1]
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def show_feedback(correct, correct_word, response):
    """Affiche un feedback après chaque réponse."""
    screen.fill(BACKGROUND)
    
    if correct:
        feedback_text = "Correct !"
        feedback_color = (0, 150, 0)  # vert
    else:
        feedback_text = f"Incorrect. Le mot était : {correct_word}"
        feedback_color = (200, 0, 0)  # rouge
    
    feedback_surface = font_small.render(feedback_text, True, feedback_color)
    feedback_rect = feedback_surface.get_rect(center=(center_x, center_y))
    screen.blit(feedback_surface, feedback_rect)
    
    pygame.display.flip()
    pygame.time.delay(1000)  # Afficher pendant 1 seconde

def run_block(use_colors=False, use_colored_backgrounds=False, block_name=""):
    """Fait un bloc complet de l'expérience."""
    results = []
    
    # Instructions pour le bloc
    if use_colored_backgrounds:
        instructions = [
            f"Bloc 3: Mots colorés sur fonds colorés",
            "Des mots colorés vont apparaître sur des fonds colorés.",
            "Votre tâche est d'identifier le mot qui était affiché.",
            "Attention: le contraste couleur/fond peut être difficile !",
            "Série de 12 essais à 50ms - Répondez RAPIDEMENT !",
            "Fixez la croix au centre de l'écran"
        ]
    elif use_colors:
        instructions = [
            f"Bloc 2: Mots en couleur",
            "Des mots vont apparaître en couleur pendant de très courts instants.",
            "Votre tâche est d'identifier le mot qui était affiché.",
            "Attention: la couleur peut influencer votre perception !",
            "Série de 12 essais à 50ms - Répondez RAPIDEMENT !",
            "Fixez la croix au centre de l'écran"
        ]
    else:
        instructions = [
            f"Bloc 1: Mots en noir",
            "Des mots vont apparaître en noir pendant de très courts instants.",
            "Votre tâche est d'identifier le mot qui était affiché.",
            "Série de 12 essais à 50ms - Répondez RAPIDEMENT !",
            "Fixez la croix au centre de l'écran"
        ]
    
    show_instructions(instructions)
    
    # Nombre d'essais par bloc
    num_trials = 12
    
    for i in range(num_trials):
        # Afficher le numéro de l'essai
        trial_info = [f"Essai {i+1}/{num_trials}", "Fixez la croix et préparez-vous..."]
        show_instructions(trial_info, wait_for_key=False)
        pygame.time.delay(1500)  # Pause de 1.5 secondes
        
        # Choisir un stimulus (mot ou non-mot)
        stimulus = random.choice(ALL_STIMULI)
        
        # Choisir les couleurs selon le bloc
        if use_colored_backgrounds:
            # Bloc 3: couleurs de texte et de fond
            text_color = random.choice(list(COLORS.values()))
            background_color = random.choice(BACKGROUND_COLORS)
            block_type = "colored_bg"
        elif use_colors:
            # Bloc 2: couleurs de texte, fond blanc
            text_color = random.choice(list(COLORS.values()))
            background_color = BACKGROUND
            block_type = "color"
        else:
            # Bloc 1: noir sur blanc
            text_color = (0, 0, 0)
            background_color = BACKGROUND
            block_type = "bw"
        
        # Afficher la croix de fixation avant le mot (sur fond blanc)
        show_fixation_cross(1000, BACKGROUND)  # Croix pendant 1 seconde sur fond blanc
        
        # Affiche le stimulus avec le fond coloré synchronisé
        show_word(stimulus, text_color, DISPLAY_TIME, background_color)

        # Génère les choix (retour au fond blanc pour les questions)
        choices = get_choices(stimulus, n=4, with_color_word=use_colors or use_colored_backgrounds, display_color=text_color)
        response = show_choices(choices)

        correct = (response == stimulus)
        is_word = stimulus in WORDS
        results.append((stimulus, response, correct, DISPLAY_TIME, block_type, text_color, background_color, is_word))

        # Afficher le feedback
        show_feedback(correct, stimulus, response)

        # Pause courte entre les essais
        if i < num_trials - 1:  # Pas de pause après le dernier essai
            time.sleep(0.5)

    return results

def show_results(results):
    """Affiche les résultats finaux de l'expérience."""
    # Calculer les statistiques par bloc
    bw_results = [r for r in results if r[4] == "bw"]
    color_results = [r for r in results if r[4] == "color"]
    colored_bg_results = [r for r in results if r[4] == "colored_bg"]
    
    bw_correct = sum(1 for r in bw_results if r[2])
    color_correct = sum(1 for r in color_results if r[2])
    colored_bg_correct = sum(1 for r in colored_bg_results if r[2])
    
    bw_accuracy = (bw_correct / len(bw_results)) * 100 if bw_results else 0
    color_accuracy = (color_correct / len(color_results)) * 100 if color_results else 0
    colored_bg_accuracy = (colored_bg_correct / len(colored_bg_results)) * 100 if colored_bg_results else 0
    
    # Statistiques mots vs non-mots
    word_results = [r for r in results if len(r) > 7 and r[7]]  # is_word = True
    nonword_results = [r for r in results if len(r) > 7 and not r[7]]  # is_word = False
    
    word_correct = sum(1 for r in word_results if r[2])
    nonword_correct = sum(1 for r in nonword_results if r[2])
    
    word_accuracy = (word_correct / len(word_results)) * 100 if word_results else 0
    nonword_accuracy = (nonword_correct / len(nonword_results)) * 100 if nonword_results else 0
    
    # Afficher les résultats
    result_lines = [
        "Résultats de l'expérience",
        "",
        f"Bloc 1 (noir/blanc): {bw_correct}/{len(bw_results)} correct ({bw_accuracy:.1f}%)",
        f"Bloc 2 (couleur/blanc): {color_correct}/{len(color_results)} correct ({color_accuracy:.1f}%)",
        f"Bloc 3 (couleur/couleur): {colored_bg_correct}/{len(colored_bg_results)} correct ({colored_bg_accuracy:.1f}%)",
        "",
        "Analyse mots vs non-mots:",
        f"Mots réels: {word_correct}/{len(word_results)} correct ({word_accuracy:.1f}%)",
        f"Non-mots: {nonword_correct}/{len(nonword_results)} correct ({nonword_accuracy:.1f}%)",
        "",
        f"Temps d'affichage: {DISPLAY_TIME}ms (fixe)",
        "",
        "Effets observés:",
        f"Couleur vs Noir: {color_accuracy - bw_accuracy:+.1f}%",
        f"Fond coloré vs Blanc: {colored_bg_accuracy - color_accuracy:+.1f}%",
        f"Mots vs Non-mots: {word_accuracy - nonword_accuracy:+.1f}%",
        f"Difficulté totale: {colored_bg_accuracy - bw_accuracy:+.1f}%",
        "",
        "Merci d'avoir participé à cette expérience !"
    ]
    
    show_instructions(result_lines)

def main():
    # Instructions d'accueil
    welcome_instructions = [
        "Expérience de perception des mots",
        "",
        "Cette expérience étudie l'effet de la couleur sur la reconnaissance rapide des mots.",
        "",
        "Vous allez voir des stimuli (mots et non-mots) affichés très brièvement.",
        "Votre tâche est d'identifier chaque stimulus parmi 4 choix proposés.",
        "",
        "L'expérience se déroule en 3 blocs:",
        "1. Stimuli en noir sur fond blanc (12 essais)",
        "2. Stimuli en couleur sur fond blanc (12 essais)",
        "3. Stimuli colorés sur fonds colorés (12 essais)",
        "",
        "IMPORTANT: Fixez toujours la croix au centre !",
        "Les temps d'affichage sont très courts (50ms)",
        "",
        "IMPORTANT: Répondez le plus RAPIDEMENT et précisément possible !",
        "La vitesse de réponse est cruciale pour cette expérience."
    ]
    
    show_instructions(welcome_instructions)
    
    all_results = []

    # Bloc 1 : Noir sur blanc
    all_results.extend(run_block(use_colors=False))
    
    # Pause entre les blocs 1 et 2
    pause_instructions_1 = [
        "Fin du Bloc 1",
        "",
        "Prenez une petite pause si nécessaire.",
        "Le prochain bloc utilisera des mots en couleur sur fond blanc.",
        "",
        "Prêt pour le Bloc 2 ?"
    ]
    show_instructions(pause_instructions_1)

    # Bloc 2 : Mots en couleur
    all_results.extend(run_block(use_colors=True))
    
    # Pause entre les blocs 2 et 3
    pause_instructions_2 = [
        "Fin du Bloc 2",
        "",
        "Prenez une petite pause si nécessaire.",
        "Le dernier bloc sera plus difficile:",
        "mots colorés sur des fonds colorés !",
        "",
        "Prêt pour le Bloc 3 ?"
    ]
    show_instructions(pause_instructions_2)

    # Bloc 3 : Mots colorés sur fonds colorés
    all_results.extend(run_block(use_colors=True, use_colored_backgrounds=True))

    # Afficher les résultats
    show_results(all_results)
    
    # Sauvegarder les résultats détaillés dans un fichier
    with open("resultats_experience.txt", "w", encoding="utf-8") as f:
        f.write("Résultats détaillés de l'expérience\n")
        f.write("=====================================\n\n")
        f.write("Format: (stimulus, réponse, correct, durée_ms, type_bloc, couleur_texte, couleur_fond, est_mot)\n\n")
        for r in all_results:
            f.write(f"{r}\n")
    
    print("Résultats sauvegardés dans 'resultats_experience.txt'")
    pygame.quit()

if __name__ == "__main__":
    main()
