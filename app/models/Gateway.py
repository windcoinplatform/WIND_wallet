class Gateway:
    def __init__(self, personal_addr, general_addr, fee, name, asset_id, url, image_name):
        self.personal_addr = personal_addr
        self.general_addr = general_addr
        self.fee = fee
        self.name = name
        self.asset_id = asset_id
        self.url = url
        self.image_name = "img/" + image_name

    def set_personal_wallet(self, personal_addr):
        self.personal_addr = personal_addr
