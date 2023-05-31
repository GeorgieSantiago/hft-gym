class Position(object):
    def __init__(self, user_id: int, accountId: str, shortQuantity: float, averagePrice: float, currentDayProfitLoss: float, currentDayProfitLossPercentage: float, longQuantity: float, settledLongQuantity: float, settledShortQuantity: float, agedQuantity: float, assetType: str, cusip: str, symbol: str, description: str, marketValue: float, maintenanceRequirement: float, previousSessionLongQuantity: float) -> None:
            self.user_id = user_id
            self.accountId = accountId
            self.shortQuantity = shortQuantity
            self.averagePrice = averagePrice
            self.currentDayProfitLoss = currentDayProfitLoss
            self.currentDayProfitLossPercentage = currentDayProfitLossPercentage
            self.longQuantity = longQuantity
            self.settledLongQuantity = settledLongQuantity
            self.settledShortQuantity = settledShortQuantity
            self.agedQuantity = agedQuantity
            self.assetType = assetType
            self.cusip = cusip
            self.symbol = symbol
            self.description = description
            self.marketValue = marketValue
            self.maintenanceRequirement = maintenanceRequirement
            self.previousSessionLongQuantity = previousSessionLongQuantity