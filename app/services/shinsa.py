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
        if not uniq:
            try:
                self.shinsa_repo.save(shinsa)
                return shinsa
            except Exception as e:
                raise e

    def get_filtered_shinsas(
        self,
        filters,
        search,
        offect,limit,
        sort_by,
        order,
    ):
        try:
            return self.shinsa_repo.get_filtered_all(
                filters,
                search,
                offect, limit,
                sort_by, order
            )
        except Exception as e:
            raise e
