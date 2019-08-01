class Whoami:
    def __init__(self, id_utilisateur, prenom, nom):
        self.id_utilisateur = id_utilisateur
        self.prenom = prenom
        self.nom = nom

    @property
    def data(self):
        return {
            "id_utilisateur": self.id_utilisateur,
            "prenom": self.prenom,
            "nom": self.nom
        }