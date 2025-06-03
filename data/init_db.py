import sqlite3

DB_PATH = "data/gestionnaire_de_tache.db"

with sqlite3.connect(DB_PATH) as db:
    db.execute("PRAGMA foreign_keys = ON")
    
    db.execute("""
        CREATE TABLE IF NOT EXISTS utilisateurs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prenom TEXT NOT NULL,
            nom TEXT NOT NULL
        )
    """)


    db.execute("""
        CREATE TABLE IF NOT EXISTS taches(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_utilisateur INTEGER,
            tache_a_realiser TEXT NOT NULL,
            statut TEXT NOT NULL,
            FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id)
        )
    """)
