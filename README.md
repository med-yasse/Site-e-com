Le projet consiste en un tableau de bord web qui charge un fichier de transactions de vente (Sales_Transaction.csv), génère automatiquement cinq graphiques statistiques via Matplotlib et Seaborn, et les affiche dans une interface HTML stylisée.

Structure des fichiers :

  vis_project/
  
  ├── app.py                  ← application Flask principale
  
  ├── Sales_Transaction.csv   ← données brutes
  
  ├── static/                 ← graphiques générés automatiquement
  
  └── templates/
      └── index.html          ← interface du dashboard  
      
Pour exécuter le projet :

  1. Telecharger le DataFrame dans: https://www.kaggle.com/datasets/gabrielramos87/an-online-shop-business/data
  2. Installer les dépendances : pip install flask pandas matplotlib seaborn
  3. Se placer dans le dossier parent du projet
  4. Lancer : python app.py
  5. Ouvrir un navigateur à l'adresse : http://127.0.0.1:5000
