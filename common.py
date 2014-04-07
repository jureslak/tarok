import collections

TAROK, KARO, SRCE, KRIZ, PIK, NEZNANA = 0, 1, 2, 3, 4, -1

def barvaVString(barva):
    return {TAROK:'T', KARO:'K', SRCE:'S', KRIZ:'R', PIK:'P', NEZNANA: 'X'}[barva]

def stringVBarvo(s):
    return {'T':TAROK, 'K':KARO, 'S':SRCE, 'R':KRIZ, 'P':PIK, 'X':NEZNANA}.get(s,-2)

# vidi: Karta implementira __eq__ in __hash__ iz BARVE/VREDNOSTI, tko da se bodo dogajale grde stvari
#       ce spreminjas barvo/vrednost medtem ko je uporabljena npr. za key!
class Karta:
    def __init__(self, *args):
        if len(args) == 2:
            self.barva = args[0]
            self.vrednost = args[1]
        else:
            self.barva,self.vrednost = -1,-1
            self.parse(args[0])

    def copy(self):
        return Karta(self.barva, self.vrednost)
            
    def stTock(self):
        if self.barva != TAROK:
            return {11:4,12:7,13:10,14:13}.get(self.vrednost, 1)
        else:
            return 13 if self.vrednost in (1,21,22) else 1
    
    def __repr__(self):
        return '%s%d' % (barvaVString(self.barva),self.vrednost)

    def __lt__(self, other):
        if self.barva == other.barva:
            if self.barva == TAROK:
                return self.vrednost < other.vrednost
            else:
                return self.vrednost > other.vrednost
        b = [TAROK, SRCE, PIK, KARO, KRIZ]
        return b.index(self.barva) < b.index(other.barva)

    def __eq__(self, other):
        if isinstance(other, Karta):
            return self.barva==other.barva and self.vrednost==other.vrednost
        else:
            return NotImplemented
    
    def __hash__(self):
        if not self: return 0
        return 23*self.barva + self.vrednost
    
    def parse(self, s):
        if not (self.barva==-1 and self.vrednost==-1): raise Exception("Nekdo spreminja hash vrednost instance!")
        self.barva = stringVBarvo(s[:1])
        self.vrednost = int(s[1:])
        if self.barva < 0 or (self.barva==TAROK and (self.vrednost<1 or self.vrednost>22)) or (self.barva in [KARO,SRCE,KRIZ,PIK] and (self.vrednost<7 or self.vrednost>14)):
            raise Exception('Neobstojeca karta ' + s)

class TipIgre:
    def __init__(self, *args):
        if len(args) == 3:
            self.stZalozenihKart = args[0]
            self.solo = args[1]
            self.klicaniKralj = args[2]
        else:
            self.parse(args[0])
    
    def vrednost(self):
        return 90*int(self.solo) + 30*(4-self.stZalozenihKart)
    
    def __repr__(self):
        # primeri: S1K, N3X, N2P, ...
        return '%s%d%s' % ( {True:'S', False:'N'}[self.solo], self.stZalozenihKart, barvaVString(self.klicaniKralj))
    
    def __eq__(self, other):
        if isinstance(other, TipIgre):
            return self.stZalozenihKart==other.stZalozenihKart and self.solo==other.solo and self.klicaniKralj==other.klicaniKralj
        else:
            return NotImplemented
    
    def __cmp__(self,other):            # S1 > S2 > S3 > N1 > N2 > N3
        return self.vrednost() - other.vrednost()

    def __lt__(self,other):
            return self.vrednost() < other.vrednost()
    
    def parse(self, s):
        self.stZalozenihKart,self.solo,self.klicaniKralj = int(s[1]),s[0]=='S',stringVBarvo(s[2])

    def text(self):
        if self.solo:
            return "SOLO "+str(self.stZalozenihKart)
        else:
            return ['','KARO','SRCE','PIK','KRIZ'][self.klicaniKralj] + ' ' + str(self.stZalozenihKart)

def karteStr(karte):
    """
    Vzame seznam kart in vrne string, ki opisuje vse te karte (sortirane).
    Prikladno za debugiranje.
    """
    karte = sorted(list(karte), key = lambda k: (k.barva, k.vrednost))
    #return ' '.join(map(str, karte))
    ret = ""
    for b in range(5):
        if any(k.barva==b for k in karte): 
            ret += "%s(%s) " % (barvaVString(b), ' '.join(str(k.vrednost) for k in karte if k.barva==b))
    return ret

def veljavnePoteze(mojeKarte, karteNaMizi):
    if karteNaMizi==[]:
        # smo prvi na potezi, vrzemo lahko karkoli
        return mojeKarte
    else:
        barva = karteNaMizi[0].barva
        # imamo karto ustrezne barve?
        enakeBarve = [k for k in mojeKarte if k.barva==barva]
        if enakeBarve:
            return enakeBarve
        # ce smo prisli do sem, nimamo karte enake barve. Imamo taroka?
        taroki = [k for k in mojeKarte if k.barva==TAROK]
        if taroki:
            return taroki
        # ce smo prisli do sem, nimamo niti ustrezne barve niti taroka in lahko vrzemo karkoli
        return mojeKarte

def steviloTock(karte):
    return sum(k.stTock() for k in karte)

###########

def idxMaxKarte(karteNaMizi):
    """
    Vrne indeks tiste karte iz danega seznama stirih kart, ki pobere rundo.
    Predpostavka je, da v seznamu karte nastopajo v vrstnem redu, v kakrsnem so padle na mizo.
    """
    if any(k.barva==TAROK for k in karteNaMizi):
        odlocilnaBarva = TAROK
    else:
        odlocilnaBarva = karteNaMizi[0].barva
    return max(
        [i for i in range(4) if karteNaMizi[i].barva==odlocilnaBarva], 
        key=lambda i: karteNaMizi[i].vrednost )

###########

def vseKarte():
    return [Karta(TAROK,i) for i in range(1,23)] + [Karta(b,v) for b in [KARO,SRCE,KRIZ,PIK] for v in range(7,15)]

###########

def karteVString(karte):
    if type(karte) == set: karte=list(karte)
    return ' '.join([str(len(karte))] + [str(k) for k in karte])

def stringiVKarte(s):
    return [Karta(k) for k in s]

def stringiVKarteN(v):
    "vektor stringov v array kart"
    N = int(v[0])
    return ([Karta(s) for s in v[1:N+1]], v[N+1:])

#########
def permutationsX(iterable, r=None):
    # permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
    # permutations(range(3)) --> 012 021 102 120 201 210
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return
    indices = range(n)
    cycles = range(n, n-r, -1)
    yield tuple(pool[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return
