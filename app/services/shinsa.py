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

    # TODO fix sync problem
    def save_shinsa_dans(self, dan_name, shinsa_location, shinsa_start_at):
        uniq = self.shinsa_repo.get_by_unique(shinsa_location, shinsa_start_at)
        dan = self.dan_repo.get_by_name(dan_name)
        if uniq and dan:
            try:
                dan.shinsas.append(uniq)
                return self.dan_repo.save()
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
