# Old version


class GoBrett:
    def __init__(self, size, name):
        """
        size:: groesse des spielbrettes
        postion:: size x size matrix mit eintraegen:
            0:: unbesetzt
            1:: schwarz
            2:: weiss
        name:: Name, des Spiels
        last_player:: letzter Spieler, der gesetzt hat.
            0:: niemand
            1:: schwarz
            2:: weiss
        last_move:: zu gesetzter zug.
        """
        self.size = size
        self.name = name
        self.position = [[0]*size for _ in range(size)]
        self.last_player = 0

    @staticmethod
    def input_int(x):
        if isinstance(x, int):
            return(x)
        elif isinstance(x, str):
            if x.isalpha():
                x = x.lower()[0]
                return(ord(x)-ord('a'))
        else:
            print("ungueltige eingabe")
            return(-1)

    def get_status(self, a):
        """gibt aus was an position a (2-tupel) ist.
        -1 :: nicht auf dem feld
        """
        if a[0] < 0 or a[0] >= self.size or a[1] < 0 or a[1] >= self.size:
            return -1
        else:
            return self.position[a[0]][a[1]]

    def set_status(self, a, new_status):
        self.position[a[0]][a[1]]=new_status



    def relation(self, a, b):
        """Testet, ob a=(a_1,a_2) und b=(b_1,b_2)
        befreundet (2)
        gegeneinander (1)
        min einer unbesetzt (0)
        a oder b nicht auf dem feld (-1)
        """
        if self.get_status(a)==0 or self.get_status(b)==0: #einer unbesetzt
            return 0
        elif self.get_status(a)==-1 or self.get_status(b)==-1:#einer nicht auf dem brett
            return -1
        elif self.get_status(a)==self.get_status(b):#gleich
            return 2
        else:
            return 1

    def neighbors_of(self, a):
        """gibt menge der nachbarkoordinaten von a zurueck
        """
        neighbors={(a[0]+1,a[1]),(a[0]-1,a[1]),(a[0],a[1]+1),(a[0],a[1]-1)}
        return neighbors


    def get_group(self, a):
        """ Gibt die zur Gruppe von a gehoerigen Steine zurueck
        """
        group=set()
        if self.get_status(a)<1:#wenn kein Stein auf a --> leere Menge
            return group
        def foo(a):
            group.add(a)
            for neighbor in (self.neighbors_of(a)-group):
                if self.relation(a, neighbor)==2: #weiteren gruppenteil gefunden -> teste das
                    foo(neighbor)
        foo(a)
        return group

    def count_libs(self, a):
        """Zaehlt die Freiheiten der zu a gehoerigen Gruppe
        """
        group=self.get_group(a)         #steine der Gruppe
        libs=set()                      #koordinaten der Freiheiten
        for groupstone in group:
            for neighbour in self.neighbors_of(groupstone)-group:
                if self.get_status(neighbour)==0:
                    libs.add(neighbour)
        return len(libs)

    def remove_group(self, a):
        """entfehrnt die Gruppe von a vom Feld
        """
        group=self.get_group(a)
        for stone in group:
            self.set_status(stone, 0)



#===============================================================================
#     def no_libertys(self, a):
#         """
#         Prueft, ob die zu a gehoerige Gruppe keine Freiheiten hat.
#         """
#         if self.get_status(a)<1: # wenn kein stein da oder nicht auf dem feld
#             return False #TODO: das hier gilt es zu ueberdenken!!! hinsichtlich kill test
#         checked=set()#menge der schon getesteten steine
#         def foo(a):
#             status_tmp = True
#             checked.add(a)
#             for s in (self.neighbors_of(a)-checked):
#                 if self.relation(a, s)==0: #freiheit gefunden -> nicht tot
#                     return False
#                 elif self.relation(a, s)==2: #weiteren gruppenteil gefunden -> teste das
#                     status_tmp=status_tmp and foo(s)
# #                else: #nachbarfeld gegnerisch oder rand
# #                    status_tmp=status_tmp and True
#             return status_tmp
#         return foo(a)
#===============================================================================

    def is_legal_position(self):
        legal=True
        for i in range(self.size):
            for j in range(self.size):
                legal=legal and not (self.count_libs((i,j))==0 and self.get_status((i,j))>0)
        return legal


    def __str__(self):
        tmp=""
        for line in self.position:
            for col in line:
                if col==0:
                    tmp=tmp+"0"
                elif col==1:
                    tmp=tmp+"B"
                else:
                    tmp=tmp+"W"
            tmp=tmp+"\n"
        return(tmp)

    #===========================================================================
    # def set_hc(self, hc):
    #     """
    #     Setzt HC Steine in position
    #     nur in 9x9; 19x19
    #     """
    #     if self.size==9:
    #         if hc=1:
    #
    #     elif self.size==19:
    #         #soon (TM)
    #     else:
    #         print("no handicap presettings for bordsize "+str(self.size))
    #===========================================================================




"""
Test-Objekt
"""
x=(1,2)
testspiel= GoBrett(4, "First try")
testspiel.position=[[0, 0, 1, 2], [2, 1, 1, 1], [0, 1, 2, 2], [1, 2, 2, 1]]
testspiel.set_status((1,1), 1)
print(testspiel)
print(testspiel.count_libs((3,0)))
print(testspiel.is_legal_position())
