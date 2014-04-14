from igralec import Igralec
from igralecgui import UserIgralec
from random import shuffle, randint, choice
from common import *

class Game:
    def __init__(self, root):
        self.igralci = {
            'Alenka': Igralec("Alenka"),
            'Bojan': Igralec("Bojan"),
            'Cecilija': Igralec("Cecilija"),
            'Uporabnik': UserIgralec('user',root),
        }
        self.order = list(self.igralci)
        shuffle(self.order)

        self.k = self.deliRundo()
        self.karte = dict(zip(self.order,map(set,self.k[1:])))
        self.pobrane = {i:set() for i in self.igralci}

    @staticmethod
    def deliRundo():
        karte = vseKarte()
        shuffle(karte)

        k = (karte[:6],karte[6:6+12],karte[6+12:6+24],karte[6+24:6+36],karte[6+36:6+48]) 
        while any(all(t.barva != TAROK for t in c) for c in k[1:]): # brez taroka ni taroka
            shuffle(karte)
            k = (karte[:6],karte[6:6+12],karte[6+12:6+24],karte[6+24:6+36],karte[6+36:6+48]) 
        return k

    def zacniRundo(self):
        self.order = self.order[1:]+[self.order[0]]
        k = self.k
        tipi = [self.igralci[i].zacniIgro(c) for i,c in zip(self.order,k[1:])]

        print("Igralci izbrali igre")
        print (tipi)
    
        igra = max(tipi)
        idx = tipi.index(igra)
        glavni = self.order[idx]
        if igra.stZalozenihKart == 3:
            talon = [k[0][:3],k[0][3:]]
        elif igra.stZalozenihKart == 2:
            talon = [k[0][:2],k[0][2:4],k[0][4:]]
        else:
            talon = list(map(lambda x:[x],k[0]))

        iztalona, izroke = self.igralci[glavni].zalozi(self.karte[glavni],talon)
        print("zalozil izroke",izroke,"iztalona",iztalona)
        ostanek = list(set(k[0])-set(iztalona))
        print('ostanek',ostanek)
        self.karte[glavni] |= set(iztalona)
        self.karte[glavni] -= set(izroke)
        self.pobrane[glavni] |= set(izroke)
        self.preostanek_talona = ostanek # shranimo za stetje
        self.igra = igra


        kralj = Karta(igra.klicaniKralj, 14)
        if igra.solo:
            self.soigralec = glavni
        else:
            try:
                self.soigralec = [name for name in self.order if kralj in self.karte[name]][0]
            except:
                self.soigralec = glavni
        self.glavni = glavni

        print (self.karte['Uporabnik'])
       
        print ('kazem stanje pred zacetkom')
        for i,n in enumerate(self.order):
            self.igralci[self.order[i]].zacniRedniDel(i,idx,igra,ostanek,iztalona)
        self.curorder = [0,1,2,3]
        self.curorder = self.curorder[idx:] + self.curorder[:idx]
       
    def krog_before_player(self):
        self.namizi = []
        curorder = self.curorder

        for i in curorder:
            self.curplayer = i 
            name = self.order[i]
            namizi = [x for x, y in self.namizi]
        
            vrgel = self.igralci[name].vrziKarto(list(self.karte[name]),namizi,curorder[0])
            if name == 'Uporabnik':
                return
            self.namizi.append((vrgel, i))
            self.karte[name].remove(vrgel)
                

    def krog_after_player(self, karta):
        curorder = self.curorder
        self.karte['Uporabnik'].remove(karta)
        self.namizi.append((karta, self.curplayer))

        idx = self.curorder.index(self.curplayer)

        for i in curorder[idx+1:]:
            name = self.order[i]
            namizi = [x for x, y in self.namizi]
        
            vrgel = self.igralci[name].vrziKarto(list(self.karte[name]),namizi,curorder[0])
            self.namizi.append((vrgel,i))
            self.karte[name].remove(vrgel)

        print(self.namizi)
        zmagal = self.kdo_je_zmagal(self.namizi)
        koncna_miza = [x[0] for x in self.namizi]
        self.pobrane[self.order[zmagal]] |= set(koncna_miza)

        for i in curorder:
            name = self.order[i]
            self.igralci[name].konecKroga(i==zmagal,curorder[0],zmagal,koncna_miza)

        zidx = curorder.index(zmagal)
        self.curorder = curorder[zidx:] + curorder[:zidx]

    def stetje_tock(self):
        self.glavni = set([self.glavni, self.soigralec])
        self.ostali = set(self.order) - self.glavni
        
        # tocke
        self.tA = sum([steviloTock(self.pobrane[idx]) for idx in self.glavni])
        self.tB = sum([steviloTock(self.pobrane[idx]) for idx in self.ostali]) + steviloTock(self.preostanek_talona)
        tt = (self.tA - self.tB)//2 + (1 if self.tA > self.tB else -1) * self.igra.vrednost()
        self.tocke = {idx: (tt//3 if idx in self.glavni else 0) for idx in self.order}

    def najvisja(self, miza, barva):
            potencialne = [karta for karta in miza if karta[0].barva == barva]
            if len(potencialne) == 0: return None
            return max(potencialne, key = lambda x: x[0].vrednost)[1]

    def kdo_je_zmagal(self, miza):
            ip = self.najvisja(miza, miza[0][0].barva)
            it = self.najvisja(miza, TAROK)
            return it if it!=None else ip
            
from tkinter import *
class GUI(Tk):
    def __init__(self):
        super().__init__()
        self["bg"] = 'green'
        self.title('Tarok')
        self.geometry('1000x800+100+100')
        self.load_images()
        print (list(self.images))

        self.game = Game(self)
        self.karte_img = {}

        self.draw_players()
        
        self.krog_num = 0 # kateri krog
        self.coor = [{'x':370,'y':340},{'x':230,'y':310},{'x':520,'y':270},{'x':660,'y':300}]

        self.start()
        self.mainloop()

    def start(self, *args):
        print("game started")
        self.game.deliRundo()
        self.game.zacniRundo()

    def main_game(self):
        self.krog_num += 1
        if self.krog_num > 2:
            self.konec()
            return
        self.game.krog_before_player()

    def load_images(self):
        self.images = {}
        for i in vseKarte():
            self.images[i] = PhotoImage(file='images/{}.ppm'.format(i))
        self.images["BG"] = PhotoImage(file='images/BG.ppm')

    def draw_players(self):
        for x in self.karte_img: self.karte_img[x].destroy()

        uidx = self.game.order.index('Uporabnik')
        self.draw_order = self.game.order[uidx:] + self.game.order[:uidx]
        self.karte_img = {}

        self.ld = Label(self, text=self.draw_order[0],bg='green',font=('Helvetica',16))
        self.ll = Label(self, text=self.draw_order[1],bg='green',font=('Helvetica',16))
        self.lu = Label(self, text=self.draw_order[2],bg='green',font=('Helvetica',16))
        self.lr = Label(self, text=self.draw_order[3],bg='green',font=('Helvetica',16))

        self.ld.place(x=405,y=750)
        self.ll.place(x=15,y=300)
        self.lu.place(x=480,y=10)
        self.lr.place(x=920,y=300)
        
        coor = [(100,550,60,0),(100,50,0,20),(300,50,30,0),(800,50,0,20)] # (x,y,dx,dy)
        for j,pl in enumerate(self.draw_order):
            for i, card in enumerate(sorted(self.game.karte[pl])):
                if pl == 'Uporabnik':
                    self.karte_img[card] = Button(image=self.images[card],anchor=NW, command=self.click_card(card))
                    self.karte_img[card].place(x=coor[j][0]+i*coor[j][2],y=coor[j][1]+i*coor[j][3])
                else:
                    self.karte_img[card] = Label(image=self.images['BG'],anchor=NW)
                    self.karte_img[card].place(x=coor[j][0]+i*coor[j][2],y=coor[j][1]+i*coor[j][3])
   
    def click_card(self, card):
        def f():
            veljavne = veljavnePoteze(self.game.karte['Uporabnik'],[x for x,y in self.game.namizi])
            if card in veljavne:
                self.game.krog_after_player(card)
        return f

    def konec(self):
        self.game.stetje_tock()
        self.konec_l = Label(self, text='KONEC',bg='green',font=('Helvetica',24))
        self.konec_l.place(x=400,y=300)

        self.labels = []
        for j, igr in enumerate(self.game.order):
            l = Label(self, text='{0}: {1:.0f}'.format(igr, steviloTock(self.game.pobrane[igr])),bg='green',font=('Helvetica',16))
            l.place(x=300, y=350+50*j)
            m = Label(self, text='{1:.0f}'.format(igr, self.game.tocke[igr]),bg='green',font=('Helvetica',16))
            m.place(x=450, y=350+50*j)
            self.labels.append(l)
            self.labels.append(m)
       # self.tocke = Label(self, text=str(self.game.tocke))
       # self.tocke.place(x=400, y=500)
        

g = GUI()
