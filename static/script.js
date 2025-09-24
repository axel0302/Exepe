class ExperimentApp {
    constructor() {
        this.currentScreen = 'welcome-screen';
        this.currentBlock = 0;
        this.currentTrial = 0;
        this.totalTrials = 10;
        this.totalBlocks = 3;
        this.blockTypes = ['bw', 'color', 'colored_bg'];
        this.blockNames = [
            'Bloc 1: Stimuli en noir',
            'Bloc 2: Stimuli en couleur', 
            'Bloc 3: Stimuli colorés sur fonds colorés'
        ];
        this.blockDescriptions = [
            'Des stimuli vont apparaître en noir pendant de très courts instants.<br>Votre tâche est d\'identifier le stimulus qui était affiché.<br>Série de 10 essais à 50ms - Répondez RAPIDEMENT !<br>Fixez la croix au centre de l\'écran',
            'Des stimuli vont apparaître en couleur pendant de très courts instants.<br>Votre tâche est d\'identifier le stimulus qui était affiché.<br>Attention: la couleur peut influencer votre perception !<br>Série de 10 essais à 50ms - Répondez RAPIDEMENT !<br>Fixez la croix au centre de l\'écran',
            'Des stimuli colorés vont apparaître sur des fonds colorés.<br>Votre tâche est d\'identifier le stimulus qui était affiché.<br>Attention: le contraste couleur/fond peut être difficile !<br>Série de 10 essais à 50ms - Répondez RAPIDEMENT !<br>Fixez la croix au centre de l\'écran'
        ];
        
        this.currentTrialData = null;
        this.trialStartTime = null;
        this.results = [];
        this.currentBackgroundColor = '#ffffff';
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.showScreen('welcome-screen');
    }
    
    bindEvents() {
        // Bouton démarrer
        document.getElementById('start-btn').addEventListener('click', () => {
            this.startExperiment();
        });
        
        // Bouton démarrer bloc
        document.getElementById('start-block-btn').addEventListener('click', () => {
            this.startBlock();
        });
        
        // Boutons de choix
        document.querySelectorAll('.choice-btn').forEach((btn, index) => {
            btn.addEventListener('click', () => {
                this.selectChoice(index);
            });
        });
        
        // Bouton continuer (pause)
        document.getElementById('continue-btn').addEventListener('click', () => {
            this.nextBlock();
        });
        
        // Bouton recommencer
        document.getElementById('restart-btn').addEventListener('click', () => {
            this.restart();
        });
        
        // Touches clavier pour les choix
        document.addEventListener('keydown', (e) => {
            if (this.currentScreen === 'choice-screen') {
                const key = e.key;
                if (['1', '2', '3', '4'].includes(key)) {
                    this.selectChoice(parseInt(key) - 1);
                }
            }
        });
    }
    
    showScreen(screenId) {
        // Cacher tous les écrans
        document.querySelectorAll('.screen').forEach(screen => {
            screen.classList.remove('active');
        });
        
        // Afficher l'écran demandé
        document.getElementById(screenId).classList.add('active');
        this.currentScreen = screenId;
    }
    
    async startExperiment() {
        this.showScreen('loading-screen');
        
        try {
            const response = await fetch('/start_experiment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({})
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.sessionId = data.session_id;
                this.participantId = data.participant_id;
                
                // Afficher l'ID généré automatiquement
                document.getElementById('participant-id-display').textContent = this.participantId;
                
                this.currentBlock = 0;
                this.currentTrial = 0;
                this.results = [];
                this.showBlockInstructions();
            } else {
                alert('Erreur lors du démarrage de l\'expérience');
                this.showScreen('welcome-screen');
            }
        } catch (error) {
            console.error('Erreur:', error);
            alert('Erreur de connexion');
            this.showScreen('welcome-screen');
        }
    }
    
    showBlockInstructions() {
        document.getElementById('block-title').textContent = this.blockNames[this.currentBlock];
        document.getElementById('block-description').innerHTML = this.blockDescriptions[this.currentBlock];
        this.showScreen('block-instructions');
    }
    
    async startBlock() {
        this.currentTrial = 0;
        this.nextTrial();
    }
    
    async nextTrial() {
        if (this.currentTrial >= this.totalTrials) {
            // Bloc terminé
            if (this.currentBlock < this.totalBlocks - 1) {
                this.showPause();
            } else {
                this.showResults();
            }
            return;
        }
        
        this.currentTrial++;
        
        // Afficher info de l'essai
        document.getElementById('trial-counter').textContent = 
            `Essai ${this.currentTrial}/${this.totalTrials}`;
        
        this.showScreen('trial-screen');
        
        // Attendre 1.5 secondes puis afficher croix
        setTimeout(() => {
            this.showFixationCross();
        }, 1500);
    }
    
    showFixationCross() {
        document.getElementById('trial-info').style.display = 'none';
        document.getElementById('fixation-cross').style.display = 'block';
        
        // Afficher croix pendant 1 seconde puis stimulus
        setTimeout(() => {
            this.showStimulus();
        }, 1000);
    }
    
    async showStimulus() {
        try {
            const response = await fetch('/get_trial', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    block_type: this.blockTypes[this.currentBlock],
                    trial_number: this.currentTrial
                })
            });
            
            const trialData = await response.json();
            this.currentTrialData = trialData;
            
            // Cacher la croix
            document.getElementById('fixation-cross').style.display = 'none';
            
            // Configurer l'affichage du stimulus
            const stimulusEl = document.getElementById('stimulus-display');
            stimulusEl.textContent = trialData.stimulus;
            stimulusEl.style.color = trialData.text_color;
            stimulusEl.style.display = 'block';
            
            // Changer la couleur de fond si nécessaire
            if (trialData.background_color !== '#FFFFFF') {
                this.currentBackgroundColor = trialData.background_color;
                document.body.style.backgroundColor = trialData.background_color;
            } else {
                this.currentBackgroundColor = '#ffffff';
            }
            
            // Afficher pendant le temps spécifié
            setTimeout(() => {
                this.hideStimulus();
            }, trialData.display_time);
            
        } catch (error) {
            console.error('Erreur lors de la récupération de l\'essai:', error);
        }
    }
    
    hideStimulus() {
        // Cacher le stimulus
        document.getElementById('stimulus-display').style.display = 'none';
        
        // Pour le bloc 3 (colored_bg), garder le fond coloré pendant les choix
        if (this.blockTypes[this.currentBlock] === 'colored_bg') {
            // Garder la couleur de fond actuelle
            document.body.style.backgroundColor = this.currentBackgroundColor;
        } else {
            // Pour les autres blocs, remettre le fond blanc
            document.body.style.backgroundColor = '#ffffff';
            this.currentBackgroundColor = '#ffffff';
        }
        
        // Afficher les choix
        this.showChoices();
    }
    
    showChoices() {
        // Configurer les boutons de choix
        const choices = this.currentTrialData.choices;
        document.querySelectorAll('.choice-btn').forEach((btn, index) => {
            btn.textContent = `${index + 1}. ${choices[index]}`;
        });
        
        // Enregistrer le temps de début pour mesurer le temps de réaction
        this.trialStartTime = Date.now();
        
        this.showScreen('choice-screen');
    }
    
    async selectChoice(choiceIndex) {
        const reactionTime = Date.now() - this.trialStartTime;
        const selectedChoice = this.currentTrialData.choices[choiceIndex];
        const isCorrect = selectedChoice === this.currentTrialData.stimulus;
        
        // Envoyer la réponse au serveur
        try {
            await fetch('/submit_response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    trial_number: this.currentTrial,
                    block_type: this.blockTypes[this.currentBlock],
                    stimulus: this.currentTrialData.stimulus,
                    response: selectedChoice,
                    reaction_time: reactionTime,
                    text_color: this.currentTrialData.text_color,
                    background_color: this.currentTrialData.background_color,
                    is_word: this.currentTrialData.is_word,
                    choices: this.currentTrialData.choices
                })
            });
        } catch (error) {
            console.error('Erreur lors de l\'envoi de la réponse:', error);
        }
        
        // Sauvegarder localement aussi
        this.results.push({
            trial: this.currentTrial,
            block: this.currentBlock,
            stimulus: this.currentTrialData.stimulus,
            response: selectedChoice,
            correct: isCorrect,
            reactionTime: reactionTime
        });
        
        // Afficher feedback
        this.showFeedback(isCorrect, this.currentTrialData.stimulus, selectedChoice);
    }
    
    showFeedback(isCorrect, correctAnswer, userAnswer) {
        const messageEl = document.getElementById('feedback-message');
        const detailsEl = document.getElementById('feedback-details');
        
        // Pour le bloc 3, remettre temporairement le fond blanc pour le feedback
        if (this.blockTypes[this.currentBlock] === 'colored_bg') {
            document.body.style.backgroundColor = '#ffffff';
        }
        
        if (isCorrect) {
            messageEl.textContent = 'Correct !';
            messageEl.className = 'correct';
            detailsEl.textContent = '';
        } else {
            messageEl.textContent = 'Incorrect';
            messageEl.className = 'incorrect';
            detailsEl.textContent = `Le stimulus était : ${correctAnswer}`;
        }
        
        this.showScreen('feedback-screen');
        
        // Continuer après 1 seconde
        setTimeout(() => {
            this.nextTrial();
        }, 1000);
    }
    
    showPause() {
        const pauseTitles = [
            'Fin du Bloc 1',
            'Fin du Bloc 2'
        ];
        
        const pauseMessages = [
            'Prenez une petite pause si nécessaire.<br>Le prochain bloc utilisera des stimuli en couleur sur fond blanc.<br><br>Prêt pour le Bloc 2 ?',
            'Prenez une petite pause si nécessaire.<br>Le dernier bloc sera plus difficile:<br>stimuli colorés sur des fonds colorés !<br><br>Prêt pour le Bloc 3 ?'
        ];
        
        document.getElementById('pause-title').textContent = pauseTitles[this.currentBlock];
        document.getElementById('pause-message').innerHTML = pauseMessages[this.currentBlock];
        
        this.showScreen('pause-screen');
    }
    
    nextBlock() {
        // Remettre le fond blanc entre les blocs
        document.body.style.backgroundColor = '#ffffff';
        this.currentBlock++;
        this.showBlockInstructions();
    }
    
    showResults() {
        // Remettre le fond blanc pour l'affichage des résultats
        document.body.style.backgroundColor = '#ffffff';
        
        // Calculer les statistiques
        const totalCorrect = this.results.filter(r => r.correct).length;
        const totalTrials = this.results.length;
        const accuracy = ((totalCorrect / totalTrials) * 100).toFixed(1);
        
        const avgReactionTime = (this.results.reduce((sum, r) => sum + r.reactionTime, 0) / totalTrials).toFixed(0);
        
        // Statistiques par bloc
        const blockStats = [];
        for (let i = 0; i < 3; i++) {
            const blockResults = this.results.filter(r => r.block === i);
            const blockCorrect = blockResults.filter(r => r.correct).length;
            const blockAccuracy = ((blockCorrect / blockResults.length) * 100).toFixed(1);
            blockStats.push({
                name: this.blockNames[i],
                correct: blockCorrect,
                total: blockResults.length,
                accuracy: blockAccuracy
            });
        }
        
        // Afficher les résultats
        const resultsHTML = `
            <h3>Résultats Globaux</h3>
            <p><strong>Précision totale:</strong> ${totalCorrect}/${totalTrials} (${accuracy}%)</p>
            <p><strong>Temps de réaction moyen:</strong> ${avgReactionTime}ms</p>
            <br>
            <h3>Résultats par Bloc</h3>
            ${blockStats.map(block => 
                `<p><strong>${block.name}:</strong> ${block.correct}/${block.total} correct (${block.accuracy}%)</p>`
            ).join('')}
            <br>
            <h3>Analyse</h3>
            <p>Effet de la couleur: ${(blockStats[1].accuracy - blockStats[0].accuracy).toFixed(1)}%</p>
            <p>Effet du fond coloré: ${(blockStats[2].accuracy - blockStats[1].accuracy).toFixed(1)}%</p>
            <p>Difficulté totale: ${(blockStats[2].accuracy - blockStats[0].accuracy).toFixed(1)}%</p>
        `;
        
        document.getElementById('results-content').innerHTML = resultsHTML;
        this.showScreen('results-screen');
    }
    
    restart() {
        this.currentBlock = 0;
        this.currentTrial = 0;
        this.results = [];
        this.currentTrialData = null;
        this.trialStartTime = null;
        this.currentBackgroundColor = '#ffffff';
        
        // Réinitialiser l'affichage
        document.getElementById('trial-info').style.display = 'block';
        document.getElementById('fixation-cross').style.display = 'none';
        document.getElementById('stimulus-display').style.display = 'none';
        document.body.style.backgroundColor = '#ffffff';
        
        this.showScreen('welcome-screen');
    }
}

// Initialiser l'application quand la page est chargée
document.addEventListener('DOMContentLoaded', () => {
    new ExperimentApp();
});
