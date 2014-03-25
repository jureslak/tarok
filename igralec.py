# -*- coding: utf-8 -*-
from common import *

class Igralec:
    def __init__(self, ime):
        self.ime = ime
        pass

    def zacniIgro(self, karteZaVRoko):
        self.karte = karteZaVRoko
        t16 = len([x for x in self.karte if x.barva == TAROK and x.vrednost > 16])
        nujb = list(set([x.barva for x in self.karte if x.barva != TAROK]) - set([x.barva for x in self.karte if x.barva != TAROK and x.vrednost == 14]))
        nujk = [x for x in self.karte if x.barva in nujb]
        neup = len(list(set([x for x in self.karte if x.barva != TAROK and x.vrednost != 14]) - set(nujk)))
        nujk = len(nujk)
        plonk = 3
        go, solo = 3, False

        if (plonk > neup + nujk and t16 > 1) or (plonk + 1 > neup + nujk and (Karta(TAROK,22) in self.karte and Karta(TAROK, 21) in self.karte)): 
            # and ([x for x in self.karte if x.barva != TAROK and x.vrednost == 14] != [] or [x for x in self.karte if x.barva == TAROK and x.stTock() == 13] != [] ):
            go, solo = 1, True
        elif plonk + 1 > neup + nujk and t16 > 1 or (plonk + 2 > neup + nujk and (Karta(TAROK,22) in self.karte and Karta(TAROK, 21) in self.karte)):
            go, solo = 2, True
        elif plonk + 2 > neup + nujk and t16 > 1 or (plonk + 3 > neup + nujk and (Karta(TAROK,22) in self.karte and Karta(TAROK, 21) in self.karte)):
            go, solo = 3, True
        elif plonk + 3 > neup + nujk and t16 > 1 or (plonk + 4 > neup + nujk and (Karta(TAROK,22) in self.karte and Karta(TAROK, 21) in self.karte)):
            go, solo = 1, False
        elif plonk + 3 > neup + nujk:
            go, solo = 2, False
                
        mozbar = list(set([KARO, SRCE, PIK, KRIZ]) - set([x.barva for x in self.karte if x.barva != TAROK and x.vrednost == 14]))#barve kerih loh grem
        moz = [[x for x in self.karte if x.barva == mozbar[i]] for i in range(len(mozbar))]
        dol  = [len(x) for x in moz]
        if 1 in dol: #preverjeno
            kralj = moz[dol.index(1)][0].barva
        elif 2 in dol:
            kralj = moz[dol.index(2)][0].barva
        elif 0 in dol:
            kralj = mozbar[dol.index(0)]
        elif 3 in dol:
            kralj = moz[dol.index(3)][0].barva
        else:
            kralj = SRCE

        self.kralj = kralj #rabmo zarad zalaganja
        self.go = go # -||-
        self.solo = solo # -||-
        return TipIgre(go, solo, NEZNANA if solo else kralj)
        
    def zalozi(self, karte, talon):
        self.karte = karte #set
        if self.solo == True:
            self.kralj = NEZNANA #v solo ni kralja
        karte = list(karte)
        ##prvi del je da ugotovimo, ker kup bi vzeli
        kup = [0 for x in range(len(talon))]
        nesme = list(set([SRCE, KARO, PIK, KRIZ, TAROK]) - set([x.barva for x in karte]))
        for i in range(len(talon)):
            t5 = [x for x in talon[i] if x.barva == TAROK and x.stTock() == 13]
            tdo12 = [x for x in talon[i] if x.barva == TAROK and x.vrednost < 12]
            t1217 = [x for x in talon[i] if x.barva == TAROK and x.vrednost >= 12 and x.vrednost < 17]
            t17 = [x for x in talon[i] if x.barva == TAROK and x.vrednost >= 17]
            po5 = [x for x in talon[i] if x.stTock() == 13]
            niql = [x for x in talon[i] if x.barva in nesme and x.vrednost != 14]

            kup[i] += len(t5)*2 + len(t17)*5 + len(t1217)*4 + len(tdo12)*3 + len(po5)*7 - len(niql)*4

        kup = kup.index(max(kup))                        

################################################################################

        ##zalaganje (pomoje se ne da bolš)
        karte += talon[kup]
        cejenujno = [x for x in karte if x.stTock() != 13 and x.barva == TAROK] #taroki ki niso 14
        okkarte = [x for x in karte if x.barva != TAROK and x.vrednost != 14] #karte k jih smemo založit ne kralj in tarok
        qlbarve = list(set([SRCE, KARO, KRIZ, PIK]) - set([x.barva for x in karte if x.vrednost == 14 and x.barva != TAROK]) - set([self.kralj]))
        qlkarte = [x for x in karte if x.barva in qlbarve] #karte k bi jih blo dobr založit
        okbrezql = list(set(okkarte) - set(qlkarte))
        if qlkarte != []:# če so karte k bi jih blo treba založit
            if len(qlkarte) == self.go: # če jih je glih prou
                return (talon[kup], qlkarte)
            
            elif len(qlkarte) < self.go: # če jih je mn
                zal = qlkarte #najprej založimo vse k jih je treba
                k = []
                for i in range(self.go - len(qlkarte)):
                    if okbrezql != []: #dodamo še največjo k jih smemo
                        k += [self.maxKarta(okbrezql)]
                        okbrezql.remove(k[i])
                    else: # če unih k jih smemo ni več
                        k+= [self.minKarta(cejenujno, False)] # dodamo najnižjiga taroka, ki ni vreden 13
                        cejenujno.remove(k[i])
                
                return (talon[kup], qlkarte + k)
            
            elif len(qlkarte) > self.go: #če jih je več
                zal = []
                barve = list(set([x.barva for x in qlkarte]))
                qlkarte = [[x for x in qlkarte if x.barva == barve[i]] for i in range(len(barve))] #razporedimo po barvah
                while True: #delamo
##                    dol = [len(x) for x in qlkarte]
                    dol = [(10 - len(x)) * 100 + steviloTock(x) for x in qlkarte]
                    najmnkup =  qlkarte[dol.index(max(dol))] #najdemo namanjši kupček kart iste barve
                    if len(najmnkup) <= self.go - len(zal): # če je še plac zanj, ga damo not
                        zal += najmnkup
                        qlkarte.remove(najmnkup)
                    else: #če ne
                        qlkarte = [y for x in qlkarte for y in x] #vrnemo karte u 1d array
                        freespc = self.go - len(zal) # kok je še frej
                        k = []
                        for i in range(freespc): #in dodamo še največje karte po vrednosti iz teh k jih je treba, ni jih premal, ker jih je več od go, čene nebi bli kle
                            najvecjaKarta = self.maxKarta(qlkarte + okbrezql) 
                            k += [najvecjaKarta]
                            if najvecjaKarta in qlkarte:
                                qlkarte.remove(k[i])
                            elif najvecjaKarta in okbrezql:
                                okbrezql.remove(k[i])
##                            k += [self.maxKarta(qlkarte)]
##                            qlkarte.remove(k[i])
                        zal += k
                        break
                return (talon[kup], zal)

        # če smo tukaj, potem ni kart ki bi jih nujno morali založit in smo veseli, založimo največje po vrednosti, od kart ki jih smemo, če obstajajo
        k = []
        for i in range(self.go):
            if okkarte != []:
                k += [self.maxKarta(okkarte)]
                okkarte.remove(k[i])
            else: #če smo tukaj, potem ni kart, ki bi jih smeli založiti in založimo najmanjšega taroka, kar pomeni da imamo ful dobre karte
                k += [self.minKarta(cejenujno, False)]
                cejenujno.remove(k[i])
        return (talon[kup], k)

    def zacniRedniDel(self, idxIgralca, glavniIgralec, tipIgre, ostanekTalona, pobraneKarteTalona):
        self.i = idxIgralca # jaz
        self.glavni = glavniIgralec #glavni
        self.go = tipIgre.stZalozenihKart #kok je šel
        self.solo = tipIgre.solo #a je solo
        self.kralj = tipIgre.klicaniKralj #v čem je šel SAMO BARVA, če želiš karto je to Karta(self.kralj, 14)
        self.igram = False #a igram jaz
        if self.glavni == self.i: # igram, če sem jaz glavni
            self.igram = True #če je to res, igram

        # kdo je z mano? tist k ma mojga kralja (igra ni solo)
        #                tist k je glavni, če mam js kralja
        #                tist k ni glavni, in nima kralja
        # če je pa solo? noben, če grem js solo
        #                vsi razn glavnega in mene, če gre glavni solo
        # pa še zarufaš se loh
        
        self.zmano = [] #z mano je nihče

        #ko je jasno s kom sm
        if Karta(self.kralj, 14) in self.karte: #bil sem porufan
            self.zmano = [self.glavni]
        if self.igram and self.solo:
            self.zmano = []
        if not self.igram and self.solo:
            self.zmano = list(set([0,1,2,3]) - set([self.glavni]) - set([self.i]))

        #kaj pa če se je zarufu
        if Karta(self.kralj, 14) in ostanekTalona or Karta(self.kralj, 14) in pobraneKarteTalona: #nekdo se je zarufu
            if self.igram: #bogi js
                self.zmano = []
            else: #ql zame
                self.zmano = list(set([0,1,2,3]) - set([self.glavni]) - set([self.i]))        
        
        self.barve = [TAROK, KARO, SRCE, KRIZ, PIK]
        self.padle = [[] for x in self.barve]
        #zapomnimo si kaj je že padlo
        for i in self.barve:
            self.padle[i] += [x for x in ostanekTalona if x.barva == i]

        self.prviKrog = [True for i in self.barve]
        self.stihnum = 1
        k = [[x for x in self.karte if x.barva == y] for y in [KARO, SRCE, KRIZ, PIK]]
        dol = [len(x) for x in k]
        self.mecem = dol.index(max(dol)) + 1
        return

    def vrziKarto(self, mojeKarte, karteNaMizi, prviIgralec):
        #ne pobiramo če ima že moj igralec, ampak mu šmeramo
        # hmm, kdo pa je z mano?
        #če sem glavni jaz, je z mano tisti, ki ima mojga kralja
        if self.igram and self.solo == False and self.zmano == []:
            if Karta(self.kralj, 14) in karteNaMizi: #če je padu moj kralj, vem gdo je z mano
                self.zmano = [(prviIgralec + karteNaMizi.index(Karta(self.kralj, 14))) % 4]
         
        elif self.zmano == [] and self.solo == False: #ne igram, nism rufan in nevem kdo je z mano -> z mano je tist k nima kralja in ne igra
            if Karta(self.kralj, 14) in karteNaMizi:
                self.zmano = list(set([0,1,2,3]) - set([(prviIgralec + karteNaMizi.index(Karta(self.kralj, 14)) % 4), self.glavni, self.i]))

        mozno = veljavnePoteze(mojeKarte, karteNaMizi)
        naj = self.pobereKarta(karteNaMizi)
        vecjeMoje = [x for x in mozno if self.prim(x,naj) == 1] #moje karte ki so večje
        KdajMond = 3

        if len(karteNaMizi) == 0: #mečemo prvi
            king = [x for x in mozno if x.vrednost == 14 and x.barva != TAROK]
            for i in king:
                if self.prviKrog[i.barva]:
                    return i
            zaloga = [x for x in mozno if x.barva == self.mecem]
            if zaloga != []:
                return self.minKarta(zaloga, False)
            return self.minKarta(mozno, False)
            
#############################################################################################################

        elif len(karteNaMizi) == 1: #mečemo drugi
            t = [x for x in mozno if x.barva == TAROK]
            after = set([0,1,2,3]) - set([self.i, prviIgralec]) # ta je za mano

            if after <= set(self.zmano): #lepo... če so vsi k so za mano tut z mano :)
                if t == []: #če morm vreči barvo
                    return self.maxKarta(mozno) #vržem max
                else: #če morm vržt tarok
                    if vecjeMoje == []: #če nimam večjega
                        return self.minKarta(mozno, False)
                    else:
                        if len(t) < KdajMond and Karta(TAROK, 21) in t and self.najTarok() == 22:# če mamo še dva tarok vržemo monda če ga mamo
                            return Karta(TAROK, 21)
                        return self.minKarta(vecjeMoje, True)
            else: #za mano ni moj
                if t == []: #vržemo barvo
                    if vecjeMoje == []:
                        return self.minKarta(mozno, False)
                    else: #mamo večjo
                        if self.prviKrog[karteNaMizi[0].barva] == True: #barva gre prvič okrog
                            return self.maxKarta(mozno)
                        else: return self.minKarta(mozno, False)
                else: #vržemo taroka
                    if vecjeMoje == []: #nimamo vecje
                        return self.minKarta(mozno, False)
                    else: #če lahko poberem
                        return self.minKarta(vecjeMoje, False)

#############################################################################################################

        elif len(karteNaMizi) == 2: #mečemo tretji
            # a je za mano moj?
            t = [x for x in mozno if x.barva == TAROK]
            after = set([0,1,2,3]) - set([self.i, prviIgralec, (prviIgralec + 1) % 4]) # ta je za mano

            if after <= set(self.zmano): #lepo... če so vsi k so za mano tut z mano :)
                if self.pobere(karteNaMizi, prviIgralec) in self.zmano: #če moj pobere
                    if t != []: #če mamo taroka
                        if len(t) < KdajMond and Karta(TAROK, 21) in t and self.najTarok() == 22:# če mamo še dva tarok vržemo monda če ga mamo
                            return Karta(TAROK, 21)
                        return self.minKarta(mozno, True) # vržemo najmanjšega taroka
                    else: return self.maxKarta(mozno) #ali največjo barvo
                else: #jaz pobiram
                    if t == []: #če morm vreči barvo
                        if vecjeMoje != []: #če lahko poberemo
                            return self.maxKarta(vecjeMoje) #vržem max
                        else:
                            return self.minKarta(mozno, False)
                    else: #če morm vržt tarok
                        if vecjeMoje == []: #če nimam večjega
                            return self.minKarta(mozno, False)
                        else:
                            if len(t) < KdajMond and Karta(TAROK, 21) in t and self.najTarok() == 22:# če mamo še dva tarok vržemo monda če ga mamo
                                return Karta(TAROK, 21)
                            return self.minKarta(vecjeMoje, True)
            else: #za mano ni moj
                if t == []: #vržemo barvo
                    if vecjeMoje == []:
                        return self.minKarta(mozno, False)
                    else: #mamo večjo
                        if self.prviKrog[karteNaMizi[0].barva] == True: #barva gre prvič okrog
                            return self.maxKarta(mozno)
                        else: return self.minKarta(mozno, False)
                else: #vržemo taroka
                    if vecjeMoje == []: #nimamo vecje
                        return self.minKarta(mozno, False)
                    else: #če lahko poberem
                        if self.prviKrog[karteNaMizi[0].barva] == True and Karta(TAROK, 1) in mozno:
                            return Karta(TAROK, 1)
                        elif steviloTock(karteNaMizi) > 22 and Karta(TAROK, self.najTarok()) in mozno:
                            return Karta(TAROK, self.najTarok())
                        return self.minKarta(vecjeMoje, False)

############################################################################################################

        elif len(karteNaMizi) == 3: #mečemo zadnji (narejeno)
            t = [x for x in mozno if x.barva == TAROK]
            if self.pobere(karteNaMizi, prviIgralec) in self.zmano: #če moj pobere
                #print "smeram", self.zmano, self.i, self.maxKarta(mozno), self.minKarta(mozno, True)
                if t != []: #če mamo taroka
                    if len(t) < KdajMond and Karta(TAROK, 21) in t and self.najTarok() == 22:# če mamo še dva tarok vržemo monda če ga mamo
                        return Karta(TAROK, 21)
                    return self.minKarta(mozno, True) # vržemo najmanjšega taroka
                else: return self.maxKarta(mozno) #ali največjo barvo
            else: #jaz pobiram
                if t == []: #če morm vreči barvo
                    if vecjeMoje != []: #če lahko poberemo
                        return self.maxKarta(vecjeMoje) #vržem max
                    else:
                        return self.minKarta(mozno, False)
                else: #če morm vržt tarok
                    if vecjeMoje == []: #če nimam večjega
                        return self.minKarta(mozno, False)
                    else:
                        if len(t) < KdajMond and Karta(TAROK, 21) in t and self.najTarok() == 22:# če mamo še dva tarok vržemo monda če ga mamo
                            return Karta(TAROK, 21)
                        return self.minKarta(vecjeMoje, True)
                        
        return self.minKarta(mozno, True)

    def konecKroga(self, zmagal, prviIgralecVKrogu, zmagovalec, karteNaMizi):
        if self.igram and self.solo == False:
            if Karta(self.kralj, 14) in karteNaMizi: #če je padu moj kralj, vem gdo je z mano
                self.zmano = [(prviIgralecVKrogu + karteNaMizi.index(Karta(self.kralj, 14))) % 4]

        elif self.zmano == [10] and self.solo == False: #ne igram, nism rufan in nevem kdo je z mano -> z mano je tist k nima kralja in ne igra
            if Karta(self.kralj, 14) in karteNaMizi:
                self.zmano = list(set([0,1,2,3]) - set([(prviIgralecVKrogu + karteNaMizi.index(Karta(self.kralj, 14)) % 4), self.glavni, self.i]))

        for i in self.barve:
            self.padle[i] += [x for x in karteNaMizi if x.barva == i]
            self.prviKrog[i] = False if karteNaMizi[0].barva == i else self.prviKrog[i] 
        self.stihnum += 1
        return

    def konecIgre(self, razlog):
        # izpisemo razlog, da vidimo, ce je šlo vse po nacrtih
        print('KONEC IGRE.', razlog)

    def maxKarta(self, arrKart):# najvecja iz arraya kart
        return sorted(arrKart, key=self.sortkey)[-1] if arrKart != [] else None
    
    def minKarta(self, arrKart, pagat):# najmanjša iz arraya kart
        if arrKart != []:
            if pagat: return sorted(arrKart, key=self.sortkey)[0] 
            else:
                if Karta(TAROK, 1) in arrKart:
                    arrKart.remove(Karta(TAROK, 1))
                    if arrKart != []: return sorted(arrKart, key=self.sortkey)[0]
                    else: return Karta(TAROK, 1)
                else: return sorted(arrKart, key=self.sortkey)[0]
   
    def sortkey(self,a):
        if not a: return 0
        if a.barva == TAROK: return 100+a.vrednost
        return a.vrednost

    def prim(self, a, b):
        if not a or not b: return 1
        if a.barva == TAROK and b.barva == TAROK:
            if a.vrednost > b.vrednost: return 1
            else: return -1
        if a.barva == TAROK: return 1
        if b.barva == TAROK: return -1
        if a.vrednost > b.vrednost: return 1
        else: return -1
        
    def pobere(self, karteNaMizi, prvi):
        if karteNaMizi == []:
            return
        if any(k.barva==TAROK for k in karteNaMizi): odlocilnaBarva = TAROK
        else: odlocilnaBarva = karteNaMizi[0].barva
        return (max([i for i in range(len(karteNaMizi)) if karteNaMizi[i].barva==odlocilnaBarva], key=lambda i: karteNaMizi[i].vrednost ) + prvi) % 4 #idx igralca ki pobere

    def pobereKarta(self, karteNaMizi):
        if karteNaMizi == []:
            return
        if any(k.barva==TAROK for k in karteNaMizi): odlocilnaBarva = TAROK
        else: odlocilnaBarva = karteNaMizi[0].barva
        return max([i for i in karteNaMizi if i.barva==odlocilnaBarva], key=lambda i: i.vrednost)

    def najTarok(self):
        return self.maxKarta(list(set([Karta(TAROK,i) for i in range(1,23)]) - set([x for
            x in self.padle[TAROK]]))).vrednost

from tkinter import *        
from itertools import product
class UserIgralec:
    def __init__(self, name, root):
        self.root = root
        self.name = name

    def zacniIgro(self, karte):
        self.karte = karte
        return self.izbira_igre()
    
    def bf_creator(self, barva, vrednost):
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
        self.top = Toplevel(self.root)
        self.top.title('Izbira igre')
        self.top.geometry('300x220+450+400')
        self.top.grab_set()
        self.top.focus_set()
        self.top.transient(self.root)
     #   self.top.overrideredirect(True)
        self.top['bg'] = 'green'
        self.top.protocol('WM_DELETE_WINDOW', lambda: 1)

        self.izbira_igre_but = {}
        for x, (i, j) in enumerate(product(['KARO','PIK','SRCE','KRIZ','SOLO'],['1','2','3'])):
            self.izbira_igre_but[i+j] = Button(self.top, text=i+' '+j, width=7,command=self.bf_creator(i,j))
            self.izbira_igre_but[i+j].place(x=10 + x%3 * 100, y=10 + x//3 * 40)

        self.top.wait_window(self.top)
        self.root.stage = 'zalozi'
        return self.return_v

    def zalozi(self, karte, talon):
        self.top = Toplevel(self.root)
        self.top.title('Zalaganje')
        self.top['bg']='green'
        self.top.geometry('1000x800+100+100')
        self.top.grab_set()
        self.top.focus_set()
        self.top.transient(self.root)
        self.top.protocol('WM_DELETE_WINDOW', lambda: 1)

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
        self.root.stage = 'lezim'
        return self.iztalona, self.izroke

    def zaloziKarto(self, card):
        def f(*args):
            if len(self.izroke) < len(self.talon[0]):
                if card not in [Karta(SRCE,14),Karta(KARO,14),Karta(PIK,14),Karta(KRIZ,14),Karta(TAROK,1),Karta(TAROK,21),Karta(TAROK,22)]:
                    self.izroke.add(card)
                    self.karte.remove(card)
                    self.redraw()
        return f

    def take(self, i):
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
        def f(*args):
            self.izroke.remove(card)
            self.karte.add(card)
            self.redraw()
        return f

    def redraw(self):

        for x in self.izroke_but: self.izroke_but[x].destroy()
        for x in self.talon_but: self.talon_but[x].destroy()
        for x in self.karte_but: self.karte_but[x].destroy()

        for j, card in enumerate(self.karte):
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
        if len(self.izroke) == len(self.talon[0]) and len(self.iztalona) > 0:
            self.top.destroy()

    def zacniRedniDel(self,idx,glavni,tip,ostanek,pobrane):
        self.l = Label(self.root, text="Igra {}, tip igre: {}.".format(self.root.game.order[glavni],tip.text()), font=('Helvetica',16),bg='green')
        self.l1 = Label(self.root, text='Izbrane karte', font=('Helvetica',14), bg='green')
        self.l2 = Label(self.root, text='Ostale karte', font=('Helvetica',14), bg='green')
        
        self.l.place(x=350,y=260)
        self.l1.place(x=280,y=290)
        self.l2.place(x=600,y=290)

        print (ostanek)
        print (pobrane)
        
        self.talon_lab = []
        for j, card in enumerate(ostanek):
            self.talon_lab.append(Label(self.root, image=self.root.images[card],anchor=NW))
            self.talon_lab[-1].place(y=320,x=len(pobrane)*50+400+50*j)
        
        for j, card in enumerate(pobrane):
            self.talon_lab.append(Label(self.root, image=self.root.images[card],anchor=NW))
            self.talon_lab[-1].place(y=320,x=250+50*j)

        self.b = Button(self.root,text='OK',width=5,command=self.startgame)
        self.b.place(x=900,y=700)

        self.root.draw_players()

    def startgame(self):
        self.l.destroy()
        self.l1.destroy()
        self.l2.destroy()
        self.b.destroy()
        for x in self.talon_lab: x.destroy()
        self.root.state = 'start'
        
