from dataclasses import dataclass
from typing import Optional


@dataclass
class TransFormer:
    id:str
    x:str
    y:str
    length:str
    width:str
    baseP:Optional[str]=None
    P:Optional[str]=None
    Q:Optional[str]=None
    Freq:Optional[str]=None
    Grounded:Optional[str]=None
    # def __init__(self,id,x,y,p=None,q=None,grounded=None,freq=None) -> None:
    #     self.Id=id
    #     self.P=p
    #     self.Q=q
    #     self.Grounded=grounded
    #     self.Freq=freq
    #     self.x=x
    #     self.y=y
    def get_P(self):
        return self.P
    def get_Q(self):
        return self.Q
    def get_F(self):
        return self.Freq
    def get_ground(self):
        return self.Grounded
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
