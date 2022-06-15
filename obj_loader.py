
class Loader:
    def __init__(self , fileName):
        self.OBJ = open(fileName , "r")
        self.vertice = []
        self.texture = []
        self.crspndg = []
        self.verticeFinal = []
    
        while True:
            line = self.OBJ.readline()
            if not line:
                break
            line = line.split()
            if line[0] == "v":
                self.vertice.append(list(map(float,line[1:])))
            if line[0] == "vt":
                self.texture.append(list(map(float,line[1:])))
            if line[0] == "f":
                self.crspndg.append(line[1:])

        for i in self.crspndg:
            for j in range(3):
                curr = list(map(int , i[j].split("/")))
                temp = []
                for k in self.vertice[curr[0] - 1]:
                    temp.append(k)
                for z in self.texture[curr[1] - 1]:
                    temp.append(z) 
                self.verticeFinal.append(temp.copy())
        self.length = len(self.verticeFinal)
               













