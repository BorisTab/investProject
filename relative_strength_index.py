from AlgorithmImports import *

class RsiCryptoAlgorithm(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2019, 1, 1)
        self.SetEndDate(2020, 1, 1)
        self.SetCash(100000)
        self.SetBrokerageModel(BrokerageName.GDAX, AccountType.Cash)
        self.crypto = self.AddCrypto("BTCUSD", Resolution.Minute, Market.GDAX)

        self.rsiPeriod = float(self.GetParameter("rsiPeriod"))
        self.rsiBuyThreshold = float(self.GetParameter("rsiBuyThreshold"))
        self.rsiSellThreshold = float(self.GetParameter("rsiSellThreshold"))
        self.rsi = self.RSI(self.crypto.Symbol, self.rsiPeriod, MovingAverageType.Simple, Resolution.Minute)

    def OnData(self, data):
        if not self.rsi.IsReady:
            return

        if self.rsi.Current.Value < self.rsiBuyThreshold and not self.crypto.Invested:
            self.SetHoldings(self.crypto.Symbol, 1)

        elif self.rsi.Current.Value > self.rsiSellThreshold and self.crypto.Invested:
            self.Liquidate(self.crypto.Symbol)
