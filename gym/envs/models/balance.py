from gym.envs.models.model import Model

BaseBalance = type("BaseBalance", (Model,), {
        'accountId': None,
        'balanceType': None,
        'user_id': None,
        'accruedInterest': None,
        'availableFunds': None,
        'availableFundsNonMarginableTrade': None,
        'bondValue': None,
        'buyingPower': None,
        'buyingPowerNonMarginableTrade': None,
        'cashBalance': None,
        'cashAvailableForTrading': None,
        'cashReceipts': None,
        'dayTradingBuyingPower': None,
        'dayTradingBuyingPowerCall': None,
        'dayTradingEquityCall': None,
        'equity': None,
        'equityPercentage': None,
        'liquidationValue': None,
        'longMarginValue': None,
        'longOptionMarketValue': None,
        'longStockValue': None,
        'maintenanceCall': None,
        'maintenanceRequirement': None,
        'margin': None,
        'marginEquity': None,
        'moneyMarketFund': None,
        'mutualFundValue': None,
        'regTCall': None,
        'shortMarginValue': None,
        'shortOptionMarketValue': None,
        'shortStockValue': None,
        'totalCash': None,
        'isInCall': None,
        'pendingDeposits': None,
        'marginBalance': None,
        'shortBalance': None,
        'accountValue': None,
        'savings': None,
        'sma': None,
        'shortMarketValue': None,
        'pendingDeposits': None,
        'mutualFundValue': None,
        'stockBuyingPower': None
})

class Balance(BaseBalance):
    def __init__(self, json: dict) -> None:
        super().__init__(json)
    def change(self, amount: int):
        self.stockBuyingPower += amount