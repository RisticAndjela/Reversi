from reversi import *

hashMap={} #koristimo je za cuvanje rezultata za zadatu tablu

while True:
    board = napraviTablu()
    igrac = crno
    dozvoliMogucnost(board,igrac)
    print(prikaziTablu(board,igrac))
    while True:
        if len(listaMogucihPoteza(board, igrac)) == 0:
            break
        if igrac == crno:
            if str(board) not in hashMap.keys():
                potez = najboljiPotez(board, igrac)
                ubaciUPolje(board, potez[0], potez[1], igrac)
                hashMap[str(board)]={
                    "rezultat":tuple(rezultat(board)),
                    "moguci potezi":listaMogucihPoteza(board,crno),
                    "najbolji potez":potez} 
            else:
                potez=hashMap[str(board)].get("najbolji potez") 
                ubaciUPolje(board, potez[0], potez[1], igrac) 
            print("crni igrac je igrao:", chr(potez[1] + 97) + str(potez[0] + 1))
            a,b=rezultat(board)
            print("belo rezultat:",a, "crno rezultat: ",b)
        else:
            while True:    
                if str(board) not in hashMap.keys():
                    listaMP=listaMogucihPoteza(board,belo)
                    listaSTR=[]
                    for i in listaMP:
                        listaSTR.append(chr(i[1] + 97)+str(i[0] + 1))
                    print("Vase moucnosti su",end=": ")
                    for i in listaSTR:
                        print(i,end="  ")
                    izabranPotez = input("\nUnesite potez: ")
                    if len(izabranPotez) != 2 or not izabranPotez[0].isalpha() or not izabranPotez[1].isdigit():
                        print("Neuspesno ocitavanje poteza, probajte ponovo.")
                        continue
                    kol = ord(izabranPotez[0].lower()) - 97
                    red = int(izabranPotez[1]) - 1
                    if [red,kol] not in listaMP:
                        print("Nemoguc potez, probajte ponovo")
                        continue
                    ubaciUPolje(board, red, kol, igrac)
                    hashMap[str(board)]={
                        "rezultat":tuple(rezultat(board)),
                        "moguci potezi": listaMP,
                        "najbolji potez": potez}          
                    
                else:
                    listaMP=hashMap[str(board)].get("moguci potezi")
                    listaSTR=[]
                    for i in listaMP:
                        listaSTR.append(chr(i[1] + 97)+str(i[0] + 1))
                    print("Vase moucnosti su",end=": ")
                    for i in listaSTR:
                        print(i,end="  ")
                    izabranPotez = input("\nUnesite potez: ")
                    if len(izabranPotez) != 2 or not izabranPotez[0].isalpha() or not izabranPotez[1].isdigit():
                        print("Neuspesno ocitavanje poteza, probajte ponovo.")
                        continue
                    kol = ord(izabranPotez[0].lower()) - 97
                    red = int(izabranPotez[1]) - 1
                    if [red,kol] not in listaMP:
                        print("Nemoguc potez, probajte ponovo")
                        continue
                    ubaciUPolje(board,red,kol, igrac)
                        
                        
                a,b=rezultat(board)
                print("belo rezultat:",a, "crno rezultat: ",b)
                break
        if igrac == belo:
            igrac = crno
        else:
            igrac = belo
        prikaziTablu(board,igrac)

    # Calculate and display the final rezultat
    a,b=rezultat(board)
    print("Game over!")
    print("belo rezultat:",a, "crno rezultat: ",b)

    if b > a:
        print("crni pobedjuje!")
    elif a > b:
        print("beli pobedjuje!")
    else:
        print("Izjednaceno je!")
       
    nastavak=input("Za nastavak unesite da: ")
    if nastavak.lower()=="da":
        continue
    else:
        break