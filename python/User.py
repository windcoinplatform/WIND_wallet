from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, pk='', seed=''):
        self.id = pk
        self.seed = seed
        if pk == '' and seed != '':
            self.id = self.get_wallet_by_seed().privateKey
        self.wallet: py.Address = self.get_wallet()

    def get_wallet(self) -> py.Address:
        return py.Address(privateKey=self.id)

    def get_wallet_by_seed(self) -> py.Address:
        return py.Address(seed=self.seed)
