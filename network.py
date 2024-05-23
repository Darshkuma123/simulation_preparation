class NetWork():
    def __init__(self,id,x,y,basep=None,initialp=None,startupcost=None,startuptime=None) -> None:
        self.basep=basep
        self.initalp=initialp
        self.startupcost=startupcost
        self.startuptime=startuptime
        self.Id=id
        self.x=x
        self.y=y
        
    def set_basep(self,baseP=int):
        self.basep=baseP
    def get_id(self):
        return self.Id
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y