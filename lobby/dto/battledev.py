from datetime import datetime

from lobby import models


class BattleDev:
    def __init__(self, id, nom, date_debut, date_fin):
        self.id: int = id
        self.nom: str = nom
        self.date_debut: datetime = date_debut
        self.date_fin: datetime = date_fin

    @classmethod
    def from_model(cls, battle_dev: models.BattleDev):
        return cls(
            id=battle_dev.id,
            nom=battle_dev.nom,
            date_debut=battle_dev.date_debut,
            date_fin=battle_dev.date_fin
        )

    @property
    def data(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "date_debut": self.date_debut.isoformat(),
            "date_fin": self.date_fin.isoformat()
        }
