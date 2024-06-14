import copy
from node import Node


prazno=0
belo=1
crno=2
mogucnost=3


#napravi tablu
def napraviTablu():
    board=[]
    for i in range(8):
        board.append([prazno]*8)
    
    board[3][3]=belo
    board[3][4]=crno
    board[4][3]=crno
    board[4][4]=belo
    
    return board

#jednostavnije biranje protivnika
def biranjeProtivnika(igrac):
    if igrac==belo:
        protivnik=crno
    else:
        protivnik=belo
    return protivnik

#prikazuje tablu u trenutnom stanju sa svim mogucnostima
def prikaziTablu(board,igrac):
    board=izbrisiSveMogucnostiOdPre(board)
    board=dozvoliMogucnost(board,igrac)
    print("   a b c d e f g h")
    print("   ----------------")
    for red in range(8):
        print(red + 1,end=" |")
        for kolona in range(8):
            if board[red][kolona] == prazno:
                print(" ",end=" ")
            elif board[red][kolona] == crno:
                print("B",end=" ")
            elif board[red][kolona] == belo:
                print("W",end=" ")
            elif board[red][kolona] == mogucnost:
                print("*",end=" ")
            
        print("|")
    print("   ----------------")
    
#brise sve * iz tabele, da ne dodje do zabune sa sledecim koracima    
def izbrisiSveMogucnostiOdPre(board):
    board1=board
    for red in range(8):
        for kol in range(8):
            if board1[red][kol]==mogucnost:
                board1[red][kol]=prazno 
            else:
                continue
    return board1

#za odredjenu figuricu daje mogucnosti narednih koraka
def dozvoljenoUbacivanje(board,red,kol,igrac):
    protivnik=biranjeProtivnika(igrac)

    smerKretanja = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]  # svi sem 0,0 jer je to trenutna pozicija
    for i in smerKretanja:
        red1 = red + i[0]
        kol1 = kol + i[1]
        try:
            if red1 >= 8 or red1 < 0 or kol1 < 0 or kol1 >= 8 or board[red1][kol1] == igrac:
                continue  # nastavi dalje kroz listu jer si izasao van table ili si na zauzetom polju
        except IndexError:
            continue
        if 0 <= red1 < 8 or 0 <= kol1 < 8:
            if board[red1][kol1] == protivnik:  # kada pomerim pokazivac i stane na protivnicku figuru
                istinitost = True
                red2 = red1 
                kol2 = kol1 
                while istinitost:
                    red2+=i[0]
                    kol2+=i[1]
                    if red2 >= 8 or red2 < 0 or kol2 < 0 or kol2 >= 8:
                        istinitost = False
                    elif board[red2][kol2] == prazno:  # kada pomerim pokazivac i stane na prazno mesto, stavim mogucnost
                        board[red2][kol2] = mogucnost
                        istinitost = False
                    elif board[red2][kol2]==protivnik:
                        continue
                    else:
                        break
                        
            

    return board
  
#ubacuje mogucnosti za sve figurice igraca  
def dozvoliMogucnost(board, igrac):
    board=izbrisiSveMogucnostiOdPre(board)
    for red in range(8):
        for kol in range(8):
            if board[red][kol]==igrac: #prolazim kroz sva polja za igraca i ubacujem mogucnost u tablu
                board=dozvoljenoUbacivanje(board,red,kol,igrac) 
            else:
                continue
    
    return board

#prebacuje sve mogucnosti iz table u listu 
def listaMogucihPoteza(board,igrac):
    board=dozvoliMogucnost(board,igrac)
    lista=[]
    for red in range(8):
        for kol in range(8):
            if board[red][kol]==mogucnost: #prolazim kroz sva polja za igraca i ubacujem mogucnost u tablu
                lista.append([red,kol])
            else:
                continue
    return lista

#ubacuje igraca na odabrano mesto i menja sve figurice po pravilima igre , a ukoliko nije moguce vraca nepromenjenu tablu
def ubaciUPolje(board, red, kol, igrac):
    protivnik = biranjeProtivnika(igrac)
    board = izbrisiSveMogucnostiOdPre(board)
    if [red, kol] not in listaMogucihPoteza(board, igrac):
        return board
    else:
        board[red][kol] = igrac
        smerKretanja = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for i in smerKretanja:
            red1 = red + i[0]
            kol1 = kol + i[1]
            if red1 < 0 or red1 >= 8 or kol1 < 0 or kol1 >= 8:
                continue
            if board[red1][kol1] == protivnik:
                while 0 <= red1 < 8 and 0 <= kol1 < 8 and board[red1][kol1] == protivnik:
                    red1 += i[0]
                    kol1 += i[1]
                if 0 <= red1 < 8 and 0 <= kol1 < 8 and board[red1][kol1] == igrac:
                    while (red1, kol1) != (red, kol):
                        red1 -= i[0]
                        kol1 -= i[1]
                        board[red1][kol1] = igrac

    return board
    
#razultat oba igraca
def rezultat(board):
    return rezultatIgraca(board,belo),rezultatIgraca(board,crno)

#rezultat izabranog igraca
def rezultatIgraca(board,igrac):
    rezultatIgraca=0
    for red in range(8):
        for kol in range(8):
            if board[red][kol]==igrac: 
                rezultatIgraca+=1
            
            else:
                continue
    return rezultatIgraca

#minimax algoritam   
def minimax(node, alpha, beta, vrednost):
    board=node.board
    if node.dubina==0:
        return node.poeni
    if vrednost:
        for child in node.children:
            boardKopija=copy.deepcopy(board)
            child.board=boardKopija
            ubaciUPolje(boardKopija,node.move[0],node.move[1],belo)
            naCosku(node)
            naIvici(node)
            vrednost = minimax(child, alpha, beta, False)
            alpha = max(alpha, vrednost)
            if beta <= alpha:
                break
        return vrednost
    
    else:
        for child in node.children:
            boardKopija=copy.deepcopy(board)
            child.board=boardKopija
            ubaciUPolje(boardKopija,node.move[0],node.move[1],crno)
            naCosku(node)
            naIvici(node)
            vrednost = minimax(child, alpha, beta, True)
            beta = min(beta, vrednost)
            if beta <= alpha:
                break
        return vrednost


def naCosku(node):
    board=node.board
    if board[0][0]==1:
        node.poeni-=5
    if board[0][7]==1 :
        node.poeni-=5
    if board[7][0]==1 :
        node.poeni-=5
    if board[7][7]==1:
        node.poeni-=5
        
    if board[0][0]==2:
        node.poeni+=15
    if board[0][7]==2 :
        node.poeni+=15
    if board[7][0]==2 :
        node.poeni+=15
    if board[7][7]==2:
        node.poeni+=15

                
def naIvici(node):
    board=node.board
    for i in range (0,8):
        if board[0][i]==1:
            node.poeni-=2
        if board[7][i]==1:
            node.poeni-=2
        if board[i][0]==1:
            node.poeni-=2
        if board[i][7]==1:
            node.poeni-=2
            
        if board[0][i]==2:
            node.poeni+=4
        if board[7][i]==2:
            node.poeni+=4
        if board[i][0]==2:
            node.poeni+=4
        if board[i][7]==2:
            node.poeni+=4


    
    
#pravljenje stabla za odredjenog igraca 
def napraviStablo(board, dubina, player):
    root = Node(board, dubina, player)
    popuniStablo(root)
    return root

#ubacujem decu na grane
def popuniStablo(node):
    if node.dubina == 0 or len(listaMogucihPoteza(node.board, node.player)) == 0:
        node.vrednost = rezultatIgraca(node.board, node.player)
        return

    for i in listaMogucihPoteza(node.board, node.player):
        new_board = copy.deepcopy(node.board)
        ubaciUPolje(new_board, i[0], i[1], node.player)
        child = Node(new_board, node.dubina - 1, biranjeProtivnika(node.player), i) 
        node.children.append(child)
        popuniStablo(child) #zavrsavam granu

#bot bira najbolji potez, poziva se minimax
def najboljiPotez(board, igrac):
    board=izbrisiSveMogucnostiOdPre(board)
    listaMP=listaMogucihPoteza(board, igrac)
    if len(listaMP)<3:
        root = napraviStablo(board, 6, igrac)
    if len(listaMP)<7:
        root = napraviStablo(board, 5, igrac)
    elif len(listaMP)<9:
        root = napraviStablo(board, 4, igrac)
    else:
        root= napraviStablo(board, 3, igrac)
    alpha = float('-inf')
    beta = float('inf')
    najboljiRezultat = float('-inf') #sigurno ce biti veci
    najboljiPotez = None 

    for child in root.children:
        child.board=board
        vrednost = minimax(child, alpha, beta, False) 
        if vrednost > najboljiRezultat:
            najboljiRezultat = vrednost
            najboljiPotez = child.move

    return najboljiPotez

