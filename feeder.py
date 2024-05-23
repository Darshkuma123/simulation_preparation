from dataclasses import dataclass
from typing import Optional

@dataclass
class Feeder():
    id:str
    x:str
    y:str
    length:str
    width:str
    baseP:Optional[str]=None
 
    # def __init__(self,id,x,y,basep=None,initialp=None,startupcost=None,startuptime=None) -> None:
    #     self.basep=basep
    #     self.initalp=initialp
    #     self.startupcost=startupcost
    #     self.startuptime=startuptime
    #     self.Id=id
    #     self.x=x
    #     self.y=y
        
    def set_basep(self,baseP=int):
        self.basep=baseP
    def get_id(self):
        return self.id
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y