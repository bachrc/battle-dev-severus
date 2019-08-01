class Problem:
    def __init__(self, id_problem, title, contenu, question):
        self.question = question
        self.contenu = contenu
        self.title = title
        self.id = id_problem

    @property
    def data(self):
        return {
            "id": self.id,
            "titre": self.title,
            "contenu": self.contenu,
            "question": self.question
        }
