class substation:
    def __init__(self,Id,pfixed,qfixed,voltagelevel,BreakerID) -> None:
        self.Id=Id
        self.Pfixed=pfixed
        self.Qfixed=qfixed
        self.VoltageLevel=voltagelevel
        self.breakerid=BreakerID
    def get_Pfixed(self):
        return self.Pfixed
    def get_Qfixed(self):
        return self.Qfixed
    def get_voltagelevel(self):
        return self.VoltageLevel