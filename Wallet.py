class Wallet:

    def __init__(self, cash):
        self.cash = cash

    def plus(self, num):
        self.cash += num
        return self.cash

    def minus(self, num):
        self.cash -= num
        return self.cash