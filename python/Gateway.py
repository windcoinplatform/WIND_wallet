class Gateway():
    def __init__(self, personal_addr, general_addr, fee, name, assetId, url):
        self.personal_addr = personal_addr
        self.general_addr = general_addr
        self.fee = fee
        self.name = name
        self.assetId = assetId
        self.url = url

    def set_personal_wallet(self, personal_addr):
        self.personal_addr = personal_addr
