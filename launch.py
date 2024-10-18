import subprocess
import os
import sys

# Nom de l'environnement virtuel partagé
shared_env = "shared_env"

def create_virtualenv():
    """Crée un environnement virtuel partagé s'il n'existe pas déjà."""
    env_path = os.path.join(shared_env)
    if not os.path.exists(env_path):
        print("Création de l'environnement virtuel partagé...")
        subprocess.run([sys.executable, '-m', 'venv', env_path])
    else:
        print("Environnement virtuel partagé déjà existant.")

def install_requirements():
    """Installe les dépendances à partir du fichier requirements.txt commun."""
    requirements_path = 'requirements.txt'
    if os.path.exists(requirements_path):
        print(f"Installation des dépendances depuis {requirements_path}...")
        subprocess.run([os.path.join(shared_env, 'Scripts', 'pip'), 'install', '-r', requirements_path])
    else:
        print("Le fichier requirements.txt commun est introuvable.")

def run_script(path, script_name, db_path):
    """Active l'environnement virtuel partagé et exécute le script en lui passant le chemin de la base de données."""
    command = f"{os.path.join(shared_env, 'Scripts', 'activate')} & python {os.path.join(path, script_name)} {db_path}"
    return subprocess.Popen(command, shell=True)

# Les répertoires des projets, les scripts à exécuter et les bases de données correspondantes
projects = {
    "showtime": "showtime.py",
    "booking": "booking.py",
    "movie": "movie.py",
    "user": "user.py",
}

# Créer l'environnement virtuel partagé
create_virtualenv()

# Installer les dépendances une seule fois depuis le requirements.txt commun
install_requirements()

processes = []

# Lancer les scripts pour chaque projet
for project, script in projects.items():
    db_path = os.path.join(project, 'databases', f"{project}s.json")  # Construire le chemin vers la base de données JSON
    print(f"Lancement du composant {project}")
    process = run_script(project, script, db_path)  # Exécuter le script
    processes.append(process)

# Afficher un message après le lancement de tous les scripts
print("")
print("      ::::::::::       :::::::::::       ::::    :::       :::::::::::       ::::::::       :::    :::")
print("     :+:                  :+:           :+:+:   :+:           :+:          :+:    :+:      :+:    :+:")
print("    +:+                  +:+           :+:+:+  +:+           +:+          +:+             +:+    +:+")
print("   :#::+::#             +#+           +#+ +:+ +#+           +#+          +#++:++#++      +#++:++#++")
print("  +#+                  +#+           +#+  +#+#+#           +#+                 +#+      +#+    +#+")
print(" #+#                  #+#           #+#   #+#+#           #+#          #+#    #+#      #+#    #+#")
print("###              ###########       ###    ####       ###########       ########       ###    ###")
print("")
print("----- Les 4 composants ont été lancés, vous pouvez tester leur fonctionnement -----")
print("")

# Attendre que tous les processus se terminent
for process in processes:
    process.wait()
