class Token():
    def __init__(self, id, decimals, amount, issuer, name, description):
        self.id = id
        self.decimals = decimals
        self.amount = amount
        self.issuer = issuer
        self.name = name
        self.description = description
        self.normalized = amount / pow(10, decimals)
