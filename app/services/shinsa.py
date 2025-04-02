from ..repositories.shinsa import ShinsaRepository
from ..repositories.dan import DanRepository
from ..models.shinsa import ShinsaModel

class ShinsaService:
    def __init__(
            self,
            shinsa_repo: ShinsaRepository,
            dan_repo: DanRepository
        ):

        self.shinsa_repo = shinsa_repo
        self.dan_repo = dan_repo

    def save_shinsa(self, shinsa: ShinsaModel):
        uniq = self.shinsa_repo.get_by_unique(shinsa.location, shinsa.start_at)
        if uniq:
            raise ValueError("Shinsa with this unique already exists")

        try:
          self.shinsa_repo.save(shinsa)
          return shinsa
        except Exception as e:
            print(f"save_shinsa: {e}")
            raise e
