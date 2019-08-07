import pywaves as py
import requests
from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, pk='', seed=''):
        self.id = pk
        self.seed = seed
        if pk == '' and seed != '':
            self.id = self.get_wallet_by_seed().privateKey
        self.wallet: py.Address = self.get_wallet()
        self.extra_fees = self.state_fees(self.wallet.address)['extraFee']

    def get_wallet(self) -> py.Address:
        return py.Address(privateKey=self.id)

    def get_wallet_by_seed(self) -> py.Address:
        return py.Address(seed=self.seed)

    @staticmethod
    def state_fees(addr: str):
        r = requests.get(py.NODE + "/addresses/scriptInfo/" + addr)
        return r.json()
