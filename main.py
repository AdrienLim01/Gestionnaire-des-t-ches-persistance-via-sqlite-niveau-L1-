import sqlite3

DB_PATH = "data/gestionnaire_de_tache.db"

"""Class de gestion utilisateur elle permet de gérer l'ajout, la suppression et la modification d'un utilisateur de la table utilisateurs de la base sqlite DB_PATH"""
class GestionUtilisateurs:
    """Permet d'ajouter un utilisateur a la base sqlite de DB_PATH dans la table utilisateurs"""
    def ajouter_utilisateur(self, prenom : str, nom : str) -> str:
        try:
            with sqlite3.connect(DB_PATH) as db:
                cursor = db.execute("SELECT prenom, nom FROM utilisateurs WHERE prenom = ? and nom = ?", (prenom, nom))
                row = cursor.fetchone()
                if not row:
                    db.execute("INSERT INTO utilisateurs(prenom, nom) VALUES(?,?)", (prenom, nom))
                else:
                    return f"L'Utilisateur au Nom : **{nom}** et Prénom : **{prenom}** existe déjà."
        except Exception as e:
            raise Exception(f"Erreur innatendu de type : {e}")

    """Permet de supprimer un utilisateur a la base sqlite de DB_PATH dans la table utilisateurs"""
    def supprimer_utilisateur(self, prenom : str, nom : str) -> str:
        try:
            with sqlite3.connect(DB_PATH) as db:
                cursor = db.execute("SELECT id FROM utilisateurs WHERE prenom = ? and nom = ?", (prenom, nom))
                row = cursor.fetchone()
                if not row:
                    return f"Aucun utilisateur au Nom : **{nom}** et Prénom : **{prenom}**"
                else:
                    db.execute("DELETE FROM utilisateurs WHERE id = ?", (row[0],))
                    return f"Utilisateur au Nom : **{nom}** et Prénom : **{prenom}** les tâches associée a l'utilisateur on été automatiquement supprimer"
        except Exception as e:
            raise Exception(f"Erreur innatendu de type : {e}")

    """permet de modifier le nom et prenom d'un utilisateur existant dans la base sqlite DB_PATH, plus précisément dans la table utilisateurs"""
    def modifier_nom_et_prenom_utilisateur(self, id : int, nom : str, prenom : str) -> str:
        try:
            with sqlite3.connect(DB_PATH) as db:
                cursor = db.execute("SELECT id FROM utilisateurs WHERE nom = ? and prenom = ?",(nom, prenom))
                row = cursor.fetchone()
                if row:
                    return f"Utilisateur au Nom : **{nom}** et Prénom : **{prenom}** n'est pas disponible."
                db.execute("UPDATE utilisateurs SET nom = ?, prenom = ? WHERE id = ?", (nom, prenom, id))
                return "Modification de Prenom et Nom effectuer."
        except Exception as e:
            raise Exception(f"Erreur innatendu de type : {e}")

    """permet de modifier uniquement le prénom de l'utilisateur dans la base sqlite DB_PATH, plus précisément dans la table utilisateurs"""
    def modifier_prenom_utilisateur(self, id : int, prenom : str) -> str:
        try:
            if not self.verification_disponibilite_prenom(id, prenom):
                return f"Veuillez changer de prénom le prénom : {prenom} n'est pas disponible."
            else:
                with sqlite3.connect(DB_PATH) as db:
                    db.execute("UPDATE utilisateurs SET prenom = ? WHERE id = ?", (prenom, id))
                return "Modification de Prenom effectuer."
        except Exception as e:
            raise Exception(f"Erreur innatendu de type : {e}")

    """permet de modifier uniquement le nom de l'utilisateur dans la base sqlite DB_PATH, plus précisément dans la table utilisateurs"""
    def modifier_nom_utilisateur(self, id : int, nom : str) -> str:
        try:
            if not self.verification_disponibilite_nom(id, nom):
                return f"Veuillez changer de nom le nom : {nom} n'est pas disponible."
            else:
                with sqlite3.connect(DB_PATH) as db:
                    db.execute("UPDATE utilisateurs SET nom = ? WHERE id = ?", (nom, id))
                return "Modification de Nom effectuer."
        except Exception as e:
            raise Exception(f"Erreur innatendu de type : {e}")

    """permet de vérifier si le prenom choisi par l'utilisateur est disponible en format booléen"""
    def verification_disponibilite_prenom(self, id : int, prenom : str) -> bool:
        try:
            with sqlite3.connect(DB_PATH) as db:
                cursor = db.execute("SELECT nom FROM utilisateurs WHERE id = ?", (id,))
                row = cursor.fetchone()
                nom = row[0]
                cursor = db.execute("SELECT nom, prenom FROM utilisateurs WHERE nom = ? and prenom = ?", (nom, prenom))
                row = cursor.fetchone()
                if not row:
                    return True
                else:
                    return False
        except Exception as e:
            raise Exception(f"Erreur innatendu de type {e}")

    """permet de vérifier si le nom choisi par l'utilisateur est disponible en format booléen"""
    def verification_disponibilite_nom(self, id : int, nom : str) -> bool:
        try:
            with sqlite3.connect(DB_PATH) as db:
                cursor = db.execute("SELECT prenom FROM utilisateurs WHERE id = ?", (id,))
                row = cursor.fetchone()
                prenom = row[0]
                cursor = db.execute("SELECT nom, prenom FROM utilisateurs WHERE nom = ? and prenom = ?", (nom, prenom))
                row = cursor.fetchone()
                if not row:
                    return True
                else:
                    return False
        except Exception as e:
            raise Exception(f"Erreur innatendu de type {e}")

"""class Gestionnaire de tache qui permet d'ajouter, modifier et supprimer une tache d'un utilisateur existant"""
class GestionnaireDeTaches:
    """Permet d'ajouter une tache a un utilisateur existant si la tache avec le même objectif existe propose de supprimer la tache déjà existante a l'utilisateur avec la commande /supprimer mais l'utilisateur devra refaire une commande d'ajout pour pouvoir ajouter par la suite la tache sinon il propose d'ajouter quand même la tache avec la commande /ajouter tout cela ce passe sur la base sqlite DB_PATH et agit sur la table taches"""
    def ajouter_tache(self, id_utilisateur : int, tache : str) -> str:
        try:
            if self.verification_id_utilisateur(id_utilisateur):
                with sqlite3.connect(DB_PATH) as db:
                    cursor = db.execute("SELECT id, tache_a_realiser, statut, created_at FROM taches WHERE id_utilisateur = ?", (id_utilisateur,))
                    row = cursor.fetchall()
                    if row:
                        for id, tache_a_realiser, statut, created_at in row:
                            if tache.strip().lower() == tache_a_realiser.strip().lower() and statut.strip().lower() == "actif":
                                choix_utilisateur = input(f"La tâche que vous voulez ajouter est déjà existante :\nid : {id}\ntache a réaliser : {tache_a_realiser}\nDate de création : {created_at}\nvoulez vous supprimer la tâche déjà existante (Si oui faite /supprimer), si vous ne voulez pas supprimer faite /ajouter\n")
                                if choix_utilisateur.strip().lower() == "/supprimer":
                                    return self.supprimer_tache(id)
                                elif choix_utilisateur.strip().lower() == "/ajouter":
                                    db.execute("INSERT INTO taches(id_utilisateur, tache_a_realiser, statut) VALUES(?,?,?)",(id_utilisateur, tache, "actif"))
                                    return f"La Tache a bien été ajouter."
                    db.execute("INSERT INTO taches(id_utilisateur, tache_a_realiser, statut) VALUES(?,?,?)",(id_utilisateur, tache, "actif"))
                    return f"La Tache a bien été ajouter."
            return f"Aucune action possible l'utilisateur avec l'id utilisateur : {id_utilisateur} n'existe pas."
        except Exception as e:
            raise Exception(f"Erreur innatendu de type : {e}")

    """permet de supprimer une tache via sa clé primaire donc son id la méthode agit sur la base sqlite DB_PATH et la table taches"""
    def supprimer_tache(self, id_tache : int) -> str:
        try:
            with sqlite3.connect(DB_PATH) as db:
                cursor = db.execute("SELECT id FROM taches WHERE id = ?", (id_tache, ))
                row = cursor.fetchone()
                if not row:
                    return "Erreur : La tache n'existe pas."
                db.execute("DELETE FROM taches WHERE id = ?", (id_tache,))
                return f"La Tache a bien été supprimer."
        except Exception as e:
            raise Exception(f"Erreur innatendu de type : {e}")

    """permet de modifier une tache existante via son id la méthode agit sur la base sqlite DB_PATH et la table taches"""
    def modifier_tache(self, id_tache : int, tache : str) -> str:
        try:
            if self.verification_id_tache(id_tache):
                with sqlite3.connect(DB_PATH) as db:
                    db.execute("UPDATE taches SET tache_a_realiser = ? WHERE id = ?",(tache, id_tache))
                    return "Tache modifier avec succès"
            return "l'id tache n'existe pas veuillez réessayer"
        except Exception as e:
            raise Exception(f"Erreur innatendu de type : {e}")


    """permet de vérifier si l'id utilisateur existe via un booléen"""
    def verification_id_utilisateur(self, id_utilisateur : int) -> bool:
        try:
            with sqlite3.connect(DB_PATH) as db:
                cursor = db.execute("SELECT * FROM utilisateurs WHERE id = ?", (id_utilisateur,))
                row = cursor.fetchone()
                if not row:
                    return False
                return True
        except Exception as e:
            raise Exception(f"Erreur innatendu de type : {e}")

    """permet de vérifier si l'id de la tache existe via un booléen"""
    def verification_id_tache(self, id_tache : int) -> bool:
        try:
            with sqlite3.connect(DB_PATH) as db:
                cursor = db.execute("SELECT * FROM taches WHERE id = ?",(id_tache,))
                row = cursor.fetchone()
                if not row:
                    return False
                return True
        except Exception as e:
            raise Exception(f"Erreur innatendu de type : {e}")
