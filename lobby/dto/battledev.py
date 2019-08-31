from datetime import datetime

from lobby import models


class BattleDev:
    def __init__(self, id, nom, description, date_debut, date_fin):
        self.id: int = id
        self.nom: str = nom
        self.description = description
        self.date_debut: datetime = date_debut
        self.date_fin: datetime = date_fin

    @classmethod
    def from_model(cls, battle_dev: models.BattleDev):
        return cls(
            id=battle_dev.id,
            nom=battle_dev.nom,
            description=battle_dev.description,
            date_debut=battle_dev.date_debut,
            date_fin=battle_dev.date_fin
        )

    @property
    def data(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "description": self.description,
            "date_debut": self.date_debut.isoformat(),
            "date_fin": self.date_fin.isoformat()
        }
