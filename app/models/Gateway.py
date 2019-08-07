class Gateway:
    def __init__(self, personal_addr, general_addr, fee, name, asset_id, url):
        self.personal_addr = personal_addr
        self.general_addr = general_addr
        self.fee = fee
        self.name = name
        self.asset_id = asset_id
        self.url = url

    def set_personal_wallet(self, personal_addr):
        self.personal_addr = personal_addr
