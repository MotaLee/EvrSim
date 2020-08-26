from mod.AroCore import AroImage
class Pipe(AroImage):
    def __init__(self):
        super().__init__()
        self.position=[-4,2,0]
        self.size=[800,400]
        self.image='mod/STS/res/pipe.png'
        self.cur_pressure=0
        return
    pass

class ToeSleeve(AroImage):
    def __init__(self):
        super().__init__()
        self.position=[-2,1.8,0.01]
        self.size=[400,360]
        self.image='mod/STS/res/toe_sleeve.png'
        self.mass=0
        self.v=0
        return
    pass

class Mcu(AroImage):
    def __init__(self):
        super().__init__()
        self.position=[0,0,0]
        return
    pass

class Pistol(AroImage):
    def __init__(self):
        super().__init__()
        self.position=[0,-3.3,0.02]
        self.ratio=1
        self.size=[150,30]
        self.image='mod/STS/res/pistol.png'
        self.mass=0
        self.v=0
        self.delay_time=0
        self.start_pressure=0
        self.delay_pressure=0
        self.cur_pressure=0

        return
    pass

class Magnet(AroImage):
    def __init__(self):
        super().__init__()
        self.position=[0,0,0]
        self.pressure=0
        self.magnet_enable=False
        return
    pass
