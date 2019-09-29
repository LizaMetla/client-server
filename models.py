import pickle
from dataclasses import dataclass
from uuid import uuid4


@dataclass
class TouristOrganisation:
    pk: uuid4().hex
    name: str
    cost: float
    timeline: str
    type_of_transport: str

    def save(self):
        all_tours = self.get_all_tours()
        all_tours.append(self)
        self._save_in_db(all_tours)

    @classmethod
    def filter(cls, cost):
        all_tours = cls.get_all_tours()
        return list(filter(lambda tour: tour.cost < cost, all_tours))

    @classmethod
    def get(cls, tour_pk):
        all_tours = cls.get_all_tours()
        search_list = list(filter(lambda tour: tour.pk == tour_pk, all_tours))
        return search_list.pop(0)

    @classmethod
    def delete(cls, tour_uuid):
        tour = cls.get(tour_uuid)
        all_tours = cls.get_all_tours()
        if tour_uuid in all_tours:
            all_tours.remove(tour)
        cls._save_in_db(all_tours)

    @classmethod
    def is_tour_by_uuid_exists(cls, tour_uuid):
        all_tours = cls.get_all_tours()
        search_list = list(filter(lambda tour: tour.uuid == tour_uuid, all_tours))
        if len(search_list) < 1:
            return False
        else:
            return True

    @staticmethod
    def get_all_tours():
        with open('database.pickle', 'rb+') as f:
            try:
                data = pickle.load(f)
            except EOFError:
                data = list()
            return data

    @staticmethod
    def _save_in_db(data):
        with open('database.pickle', 'wb') as f:
            pickle.dump(data, f)


if __name__ == '__main__':
    tour = {'pk': uuid4().hex, 'name': 'Париж', 'cost': 3000, 'timeline': '1 неделя',
            'type_of_transport': 'Космо-шатл Илона Макса'}
    # TouristOrganisation(**tour).save()
    print(TouristOrganisation.filter(cost=4000))
