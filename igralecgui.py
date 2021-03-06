from common import *
from tkinter import *        
from itertools import product
import time

class UserIgralec:
    """
    Razred, ki implementira komunikacijo z igralcem. Kličejo se enake fukcije kot pri
    računalniških igralcih.
    """
    def __init__(self, root):
        """
        Konstruktor, shranimo si glavno okno za risanje.
        """
        self.root = root

    def zacniIgro(self, karte):
        """
        Shranimo si karte in uprašamo uporabnika po izbiri igre.
        """
        self.karte = karte
        return self.izbira_igre()
    
    def bf_creator(self, barva, vrednost):
        """
        Callback creator, izbira tipa igre: nastavi izbrano igro.
        """
        if barva == 'SOLO':
            t = 'S'+vrednost+'X'
        elif barva == 'KRIZ':
            t = 'N'+vrednost+'R'
        else:
            t = 'N'+vrednost+barva[0]

        def f(*args):
            self.top.destroy()
            self.return_v = TipIgre(t)

        return f

    def izbira_igre(self):
        """
        Implementira okno za izbiro igre in vrne uporabnikovo izbiro.
        """
        self.top = Toplevel(self.root)
        self.top.title('Izbira igre')
        self.top.geometry('300x220+450+400')
        self.top.grab_set()
        self.top.focus_set()
        self.top.transient(self.root)
     #   self.top.overrideredirect(True)
        self.top['bg'] = 'green'
#          self.top.protocol('WM_DELETE_WINDOW', self.close)

        self.izbira_igre_but = {}
        for x, (i, j) in enumerate(product(['KARO','PIK','SRCE','KRIZ','SOLO'],['1','2','3'])):
            self.izbira_igre_but[i+j] = Button(self.top, text=i+' '+j, width=7,command=self.bf_creator(i,j))
            self.izbira_igre_but[i+j].place(x=10 + x%3 * 100, y=10 + x//3 * 40)

        self.top.wait_window(self.top)
        return self.return_v

#      def close(self, *args):
#          self.top.destroy()
#          self.root.destroy()

    def zalozi(self, karte, talon):
        """
        Implementira okno za zalaganje in vrne uporabnikovo izbiro.
        """
        self.top = Toplevel(self.root)
        self.top.title('Zalaganje')
        self.top['bg']='green'
        self.top.geometry('1000x800+100+100')
        self.top.grab_set()
        self.top.focus_set()
        self.top.transient(self.root)
#          self.top.protocol('WM_DELETE_WINDOW', self.close)

        self.karte = set(karte)
        self.izroke = set() 
        self.iztalona = set()
        self.karte_but = {}
        self.talon_but = {}
        self.izroke_but = {}
        self.talon = talon
        
        self.lezim = Button(self.top, text='Ležim', command=self.lezim)
        self.lezim.place(x=900,y=600)
        
        self.redraw()

        self.top.wait_window(self.top)
        return self.iztalona, self.izroke

    def zaloziKarto(self, card):
        """
        Callback creator, karto da na kupček založenih kart.
        """
        def f(*args):
            if len(self.izroke) < len(self.talon[0]):
                if card not in [Karta(SRCE,14),Karta(KARO,14),Karta(PIK,14),Karta(KRIZ,14),Karta(TAROK,1),Karta(TAROK,21),Karta(TAROK,22)]:
                    self.izroke.add(card)
                    self.karte.remove(card)
                    self.redraw()
        return f

    def take(self, i):
        """
        Callback creator, vzame ta kupcek kart iz talona. Morebitnega starega da nazaj.
        """
        def f(*args):
            if self.iztalona:
                self.talon.append(list(self.iztalona))
            self.izroke -= self.iztalona
            self.karte -= self.iztalona
            self.iztalona = set(self.talon.pop(i))
            self.karte |= self.iztalona
            self.redraw()
        return f
 
    def putback(self, card):
        """
        Callback creator, karto da nazaj v roko.
        """

        def f(*args):
            self.izroke.remove(card)
            self.karte.add(card)
            self.redraw()
        return f

    def redraw(self):
        """ 
        Narise okno za zalaganje, se kliče ko se kaj spremeni.
        """

        for x in self.izroke_but: self.izroke_but[x].destroy()
        for x in self.talon_but: self.talon_but[x].destroy()
        for x in self.karte_but: self.karte_but[x].destroy()

        for j, card in enumerate(sorted(self.karte)):
            self.karte_but[card] = Button(self.top, image=self.root.images[card],anchor=NW,command=self.zaloziKarto(card))
            self.karte_but[card].place(y=550,x=50+j*50)
        
        for i, g in enumerate(self.talon):
            for j, card in enumerate(g):
                self.talon_but[card] = Button(self.top, image=self.root.images[card],anchor=NW,command=self.take(i))
                self.talon_but[card].place(y=30,x=50+i*len(g)*150+j*60)

        for i,card in enumerate(self.izroke):
            self.izroke_but[card] = Button(self.top, image=self.root.images[card],anchor=NW,command=self.putback(card))
            self.izroke_but[card].place(y=300,x=100+i*50)

#          print ("karte:", self.karte)
#          print ("iz talona:", self.iztalona)
#          print ("talon: ", self.talon)
#          print ("iz roke:", self.izroke)

    def lezim(self):
        """
        Ce je vse v redu, vrne izbrane karte uporabnika.
        """
        if len(self.izroke) == len(self.talon[0]) and len(self.iztalona) > 0:
            self.top.destroy()

    def zacniRedniDel(self,idx,glavni,tip,ostanek,pobrane):
        """
        Prikaže uporabniku vse podatke o zalaganju in klicajnu iger.
        """
        self.l = Label(self.root, text="Igra {}, tip igre: {}.".format(self.root.game.order[glavni],tip.text()), font=('Helvetica',16),bg='green')
        self.l1 = Label(self.root, text='Izbrane karte', font=('Helvetica',14), bg='green')
        self.l2 = Label(self.root, text='Ostale karte', font=('Helvetica',14), bg='green')
        
        self.l.place(x=350,y=260)
        self.l1.place(x=280,y=290)
        self.l2.place(x=600,y=290)

#          print (ostanek)
#          print (pobrane)
        
        self.talon_lab = []
        for j, card in enumerate(ostanek):
            self.talon_lab.append(Label(self.root, image=self.root.images[card],anchor=NW))
            self.talon_lab[-1].place(y=320,x=len(pobrane)*50+400+50*j)

        for j, card in enumerate(pobrane):
            self.talon_lab.append(Label(self.root, image=self.root.images[card],anchor=NW))
            self.talon_lab[-1].place(y=320,x=250+50*j)

        self.b = Button(self.root,text='OK',width=5,command=self.startgame)
        self.b.place(x=900,y=700)

        self.root.bind("<Return>",self.startgame)
        self.root.bind("<space>",self.startgame)

        self.root.draw_players()

    def startgame(self, *args):
        """
        Callback, uporabnik potrdu da je videl podatke, začne se igra
        """
        self.l.destroy()
        self.l1.destroy()
        self.l2.destroy()
        self.b.destroy()
        for x in self.talon_lab: x.destroy()
        self.root.unbind("<Return>")
        self.root.unbind("<space>")
        self.root.main_game()

    def vrziKarto(self, karte, namizi, prvi):
        """
        Uporabniku nariše stanje na mizi in počaka, da uporabnik izbere karto.
        """
#          print ("mecem karto")
        self.root.draw_players(True)
#          print (self.root.draw_order)
        self.na_vrsti = Label(self.root, text=': na vrsti ste.',bg='green',font=('Helvetica',16))
        self.na_vrsti.place(x=510,y=750)
        self.ontable = []
        for card, pl in zip(namizi, self.root.game.curorder):
            didx = self.root.draw_order.index(self.root.game.order[pl])
            self.ontable.append(Label(self.root, image=self.root.images[card]))
            self.ontable[-1].place(**self.root.coor[didx])

    def konecKroga(self, zmagal, prvi, zmagovalec, namizi):
        """ 
        Uporabniku nariše stanje po koncu kroga, počaka da potrdi.
        """
        self.na_vrsti.destroy()
        for card, pl in zip(namizi, self.root.game.curorder):
            didx = self.root.draw_order.index(self.root.game.order[pl])
            self.ontable.append(Label(self.root, image=self.root.images[card]))
            self.ontable[-1].place(**self.root.coor[didx])

        self.root.draw_players()
        self.message_label = Label(self.root, text='Pobral/a: '+self.root.game.order[zmagovalec],
                font=('Helvetica',15),bg='green')
        self.nextround_but = Button(self.root, text='OK',width=5, command=self.next_round)
        self.root.bind("<Return>",self.next_round)
        self.root.bind("<space>",self.next_round)
        self.message_label.place(x=330, y=270)
        self.nextround_but.place(x=900,y=700)

    def next_round(self, *args):
        """
        Callback, uporabnik potrdi stanje po koncu kroga.
        """
        self.nextround_but.destroy()
        self.message_label.destroy()
        for x in self.ontable: x.destroy()
        self.root.unbind("<Return>")
        self.root.unbind("<space>")
        self.root.main_game()
