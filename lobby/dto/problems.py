class ProblemContent:
    def __init__(self, id, title, contenu, question):
        self.question = question
        self.contenu = contenu
        self.titre = title
        self.id = id

    @property
    def data(self):
        return vars(self)


class ProblemAbridged:
    def __init__(self, id, titre, index, accessible, image_url):
        self.accessible = accessible
        self.index = index
        self.titre = titre
        self.id = id
        self.image_url = image_url
        
    @property
    def data(self):
        return vars(self)


class AnswerResult:
    def __init__(self, correct, details):
        self.details = details
        self.correct = correct

    @property
    def data(self):
        return vars(self)
