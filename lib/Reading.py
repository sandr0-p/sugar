class Reading:
    def __init__(self, WT, ST, DT, Value, Trend):
        self.WT = WT
        self.ST = ST
        self.DT = DT
        self.Value = Value
        self.Trend = Trend

    @classmethod
    def from_dict(cls, data):
        return cls(
            WT=data.get("WT"),
            ST=data.get("ST"),
            DT=data.get("DT"),
            Value=data.get("Value"),
            Trend=data.get("Trend")
        )