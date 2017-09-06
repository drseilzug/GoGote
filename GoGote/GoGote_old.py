class Group:
    """ Klasse hat Go Gruppen als Objekte.
    Felder:
    color:: Farbe der Gruppe ('b' oder 'w')
    group:: Koordinaten der Gruppe als Menge von (int,int)
    libertys:: Freiheiten der Gruppe als Menge von (int,int)
    """
    def __init__(self, color):
        """Initialisiert eine leere Gruppe der farbe color mit 0 Freiheiten."""
        self.color = color
        self.group = set()
        self.libertys = set()

    def merge_with(self, other_group):
        """ fuegt other_group zur gruppe hinzu"""
        self.group.update(other_group.group)
        self.libertys.update(other_group.libertys)

    def __str__(self):
        """String representation"""
        return str(self.group)

    def __repr__(self):
        return str(self.group)


class Board:
    """
    size:: groesse des spielbrettes
    name:: Name, des Spiels
    postion:: size x size matrix mit eintraegen:
        0:: unbesetzt
        key:: Element der Gruppe key
    groups:: dict mit Eintraegen aus Group und integer keys
    last_player:: letzter Spieler, der gesetzt hat.
        "b":: schwarz
        "w":: weiss
    last_group_key:: letzter vergebener gruppen key
    last_move:: zuletzt gesetzter zug.
    captures_whites:: gefangene weisse steine
    captures_blacks:: gefangene schwarze steine
    """
    def __init__(self, size, name):
        self.size = size
        self.name = name
        self.position = [[0]*size for _ in range(size)]
        self.groups = {}
        self.last_group_key = 0
        self.last_player = "w"
        self.move = 0
        self.last_move = None
        self.captures_white = 0
        self.captures_black = 0

    def neighbours_of(self, stone):
        """Gibt Menge der Nachbarkoordinaten auf dem Brett von stone zurueck"""
        neighbours = {(stone[0]+1, stone[1]), (stone[0]-1, stone[1]),
                      (stone[0], stone[1]+1), (stone[0], stone[1]-1)}
        not_on_board = set()
        for stone in neighbours:
            if not self.is_on_board(stone):
                not_on_board.add(stone)
        return neighbours-not_on_board

    def is_on_board(self, stone):
        if stone[0] >= self.size or stone[0] < 0\
                or stone[1] >= self.size or stone[1] < 0:
            return False
        else:
            return True

    def check_color(self, key):
        """Gibt die Farbe, der Gruppe key zurueck"""
        if key == 0:
            return 0
        group = self.groups[key]  # holt die Gruppe von stone
        color = group.color
        return color

    def add_captures(self, n, color):
        """Fuegt n Gefangene der FArbe color hinzu"""
        if color == "b":
            self.captures_black += n
        else:
            self.captures_white += n

    def capture_group(self, key):
        """ Entfernt die Gruppe key"""
        group = self.groups[key]
        neighbour_keys = set()
        for stone in group.group:
            self.position[stone[0]][stone[1]] = 0           # setze felder auf unbesetzt
        for neighbour in self.group_neighbours_of(key):  # findet nachbarguppen keys
            neighbour_keys.add(self.position[neighbour[0]][neighbour[1]])
            neighbour_keys.discard(0)
        for n_key in neighbour_keys:
            self.update_libertys(n_key)
        self.add_captures(len(group.group), group.color)   # fuegt Gefangene hinzu
        del self.groups[key]    # loesche Gruppe aus dict

    def play_stone(self, stone):
        """Stein spielen und das drumherum an Werten updaten"""
        if self.set_stone(stone, self.last_player):
            if self.last_player == "w":  #spieler aendern:
                self.last_player = "b"
            else:
                self.last_player = "w"
            self.move += 1
            self.last_move = stone
        else:
            print("you can't play here")


    def set_stone(self, stone, color):
        """Setzt den Stein aufs Brett fuegt ihn zu einer Gruppe hinzu usw. gibt True zurueck, falls der Zug legal war und ausgefuehrt wurde"""
        neighbours = self.neighbours_of(stone)
        friends_keys = set()
        foe_keys = set()
        legal=False
        if self.position[stone[0]][stone[1]] != 0: #Feld nicht frei
            return legal
        for neighbour in neighbours:
            neighbour_key = self.position[neighbour[0]][neighbour[1]]
            if  self.check_color(neighbour_key) == 0: #freies Feld
                continue#free.add(neighbour)
            elif self.check_color(neighbour_key) == color: #befreundeter stein
                friends_keys.add(neighbour_key)
            else:           #feindlicher stein
                foe_keys.add(neighbour_key)

        for key in foe_keys: #killckeck fuer die benachbarten feindlichen gruppen
            self.groups[key].libertys.remove(stone)
            if len(self.groups[key].libertys) == 0:
                self.capture_group(key)

        pot_group = Group(color) #erzeugen de rpotentiellen neune Gruppe
        pot_group.group.add(stone)
        for neighbour in neighbours:
            if self.position[neighbour[0]][neighbour[1]] == 0:
                pot_group.libertys.add(neighbour)
        for key in friends_keys:
            pot_group.merge_with(self.groups[key])
        pot_group.libertys = pot_group.libertys - {stone}
        if len(pot_group.libertys)>0: #neue Gruppe hat freiheiten --> wird hinzugefuegt und alte gruppen geloescht
            self.last_group_key += 1                            #neuer key
            self.groups[self.last_group_key]=pot_group          #eintragen der neuen gruppe
            for key in friends_keys:                            #fuege angrenzende befreundete Gruppen zur neuen hinzu
                self.replace_group_keys(key, self.last_group_key)
                del self.groups[key]
            legal=True
            self.position[stone[0]][stone[1]] = self.last_group_key
        return legal

    def replace_group_keys(self, old_key, new_key):
        """ ersetzt die keys in der postion matrix mit den keys der neuen Gruppe"""
        old_group=self.groups[old_key]
        for stone in old_group.group:
            self.position[stone[0]][stone[1]] = new_key

    def update_libertys(self, key):
        """setzt die freiheiten von gruppe key neu"""
        libs=set()
        for stone in self.group_neighbours_of(key):
            if self.position[stone[0]][stone[1]] == 0:
                libs.add(stone)
        self.groups[key].libertys=libs

    def group_neighbours_of(self, key):
        """gibt die nachbarfelder der Gruppe key aus"""
        neighbours = set()
        group = self.groups[key].group
        for stone in group:
            neighbours.update(self.neighbours_of(stone)-group)
        return neighbours



    def read_group(self, stone):
        """fuegt alle angrenzenden zugehoerigen Felder (gleicher eintrag) aus position zu einer Menge hinzu und gibt diese zurueck. """
        group=set()
        if self.position[stone[0]][stone[1]] == 0:#wenn kein Stein an stone --> None
            return None
        def foo(a):
            group.add(a)
            for neighbour in (self.neighbours_of(a)-group):
                if self.position[a[0]][a[1]] == self.position[neighbour[0]][neighbour[1]]: #weiteren gruppenteil gefunden -> teste das
                    foo(neighbour)
        foo(stone)
        return group

    def generate_board(self, matrix):
        """generiert Brett aus einer n mal n list of lists matrix mit den eintraegen 'b' 'w' '0'
        Zu Testzwecken"""
        self.size = len(matrix) #setzt Brettgroesse
        self.last_player = "w"    #setzt letzten spieler
        self.position = matrix  #erzeugt positionsmatrix
        read_points = set()     #Menge, der schon eingelesenen Punkte
        for x in range(len(matrix)):
            for y in range(len(matrix[x])):
                if (x,y) not in read_points:
                    if self.position[x][y] == 0:
                        read_points.add((x,y))
                    else:
                        color = self.position[x][y]                     #TODO: hier evtl. mehr einlesemoeglcihkeiten schaffen
                        new_group = Group(color)
                        new_group.group = self.read_group((x,y))        #neue Gruppe einlesen
                        self.last_group_key += 1                        #erzeuge neuen key
                        self.groups[self.last_group_key] = new_group    #schreibe gruppe ins dict
                        self.update_libertys(self.last_group_key)       #setze Freiheiten
                        read_points.update(new_group.group)             #eingelesene steine -> read_points
                        for stone in new_group.group:                   #schreibe keys in die positionsmatrix
                            self.position[stone[0]][stone[1]]=self.last_group_key

    def __str__(self):
        """ String representation"""
        tmp=""
        for line in self.position:
            for col in line:
                if col==0:
                    tmp=tmp+"0"
                elif self.groups[col].color == "b":
                    tmp=tmp+"B"
                else:
                    tmp=tmp+"W"
            tmp=tmp+"\n"
        return(tmp)


# Testbereich
testspiel = Board(4, "First try")
matrix = [[0, 0, "b", "w"],
          ["w", "b", "b", 0],
          [0, "w", "w", "w"],
          ["b", "w", "w", "w"]]
testspiel.generate_board(matrix)
print(testspiel)
testspiel.play_stone((1,3))
print(testspiel)
testspiel.play_stone((0,1))
print(testspiel)
print (testspiel.groups)
print(testspiel.position)
testspiel.play_stone((0,0))
print("setze 0,0")
print(testspiel.groups)
print(testspiel.position)
print(testspiel)
