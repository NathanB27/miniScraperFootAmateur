PYTHON = python3
VENV = env
ACTIVATE = source $(VENV)/bin/activate

.PHONY: help setup install run clean reset

help:
	@echo "Commandes disponibles :"
	@echo "  make setup    -> Crée l'environnement virtuel et installe les dépendances"
	@echo "  make run      -> Exécute le script dans l'environnement virtuel"
	@echo "  make clean    -> Supprime les fichiers temporaires"
	@echo "  make reset    -> Supprime l'environnement et recommence à zéro"

setup:
	@echo ">> Création de l'environnement virtuel..."
	@test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	@$(ACTIVATE) && pip install --upgrade pip && pip install -r requirements.txt
	@echo ">> Environnement prêt !"

run:
	@$(ACTIVATE) && $(PYTHON) script.py

clean:
	@echo ">> Nettoyage..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -f classement.csv
	@echo ">> Fichiers temporaires supprimés."

reset: clean
	@echo ">> Suppression complète de l'environnement virtuel..."
	@rm -rf $(VENV)
	@make setup
