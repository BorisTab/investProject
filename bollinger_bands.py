from AlgorithmImports import *
from QuantConnect.Algorithm import QCAlgorithm
from QuantConnect.Indicators import BollingerBands

class BollingerBandsStrategy(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2020, 1, 1) 
        self.SetEndDate(2021, 1, 1)
        self.SetCash(100000)
 
        self.crypto = self.AddCrypto ("BTCUSD", Resolution.Minute, Market.GDAX)
        self.bollinger = self.BB(self.crypto.Symbol, 20, 3)
 
        self.SetBenchmark("SPY")
 
        self.Plot("Price", "BTCUSD", self.Securities[self.crypto.Symbol].Close)
 
    def OnData(self, data):
        if not self.bollinger.IsReady:
            return
 
        holdings = self.Portfolio[self.crypto.Symbol].Quantity
        price = data[self.crypto.Symbol].Close
 
        if holdings == 0 and price < self.bollinger.LowerBand.Current.Value:
            self.SetHoldings(self.crypto.Symbol, 1)
        elif holdings > 0 and price > self.bollinger.MiddleBand.Current.Value:
            self.Liquidate(self.crypto.Symbol)
 
        self.Plot("BollingerBands", "bollinger", self.bollinger.Current.Value)
        self.Plot("BollingerBands", "standarddeviation", self.bollinger.StandardDeviation.Current.Value)
        self.Plot("BollingerBands", "middleband", self.bollinger.MiddleBand.Current.Value)
        self.Plot("BollingerBands", "upperband", self.bollinger.UpperBand.Current.Value)
        self.Plot("BollingerBands", "lowerband", self.bollinger.LowerBand.Current.Value)
        self.Plot("BollingerBands", "bandwidth", self.bollinger.BandWidth.Current.Value)
        self.Plot("BollingerBands", "percentb", self.bollinger.PercentB.Current.Value)
        self.Plot("BollingerBands", "price", self.bollinger.Price.Current.Value)
