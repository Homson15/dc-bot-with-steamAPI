

S = None

def getSteam():

    global S
    if S is None:
        S = Steam()

    return S



class Steam:

    def __init__(self):
        pass