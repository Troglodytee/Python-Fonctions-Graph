from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from math import sqrt,cos,acos,sin,asin,tan,atan,degrees,radians
from os import path
from PIL import ImageGrab
import time

def alerte_fermeture() :
    rep = False
    if save == 0 : rep = askyesno("Confirmer la fermeture","Le graphique actuel n'est pas enregistré. Voulez-vous l'enregistrer ?")
    if rep == True : save_as_file()
    elif rep == False :
        try : fenetre_aide.destroy()
        except : a = 0
        try : fenetre_aide_fonctions.destroy()
        except : a = 0
        try : fenetre_capture.destroy()
        except : a = 0
        fenetre.destroy()

def raccourci_alerte_fermeture(event) :
    alerte_fermeture()

def new_file() :
    global liste_fonctions
    global liste_dessin
    global xmin
    global xmax
    global ymin
    global ymax
    global pas
    global save
    rep = False
    if save == 0 : rep = askyesnocancel("Confirmer l'abandon des modifications","Le graphique actuel n'est pas enregistré. Voulez-vous l'enregistrer ?")
    if rep == True : save_as_file()
    elif rep == False :
        save = 0
        liste_fonctions = []
        liste_dessin = []
        xmin,xmax,ymin,ymax,pas = -10,10,-10,10,0.1
        actualisation()
        fenetre.title("Modélisateur de fonctions - Sans Nom *")

def raccourci_new_file(event) :
    new_file()

def open_file() :
    global xmin
    global xmax
    global ymin
    global ymax
    global pas
    global liste_fonctions
    global liste_dessin
    global save
    global chemin
    global nom
    chemin_f = askopenfilename(title="Ouvrir un fichier",filetypes=[('mf files','.mf')])
    if chemin_f != "" :
        try :
            f = open(chemin_f,"r")
            sauvegarde = f.read().split(",")
            f.close()
            rep = True
            if save == 0 :
                rep = askyesno("Confirmer l'abandon des modifications","Le graphique actuel n'est pas enregistré. Continuer quand même ?")
            if rep == True :
                chemin = chemin_f
                xmin,xmax,ymin,ymax,pas = int(sauvegarde[0]),int(sauvegarde[1]),int(sauvegarde[2]),int(sauvegarde[3]),float(sauvegarde[4])
                liste_fonctions = sauvegarde[5].split("/")
                if liste_fonctions == [""] : liste_fonctions = []
                else :
                    for i in range (len(liste_fonctions)) :
                        liste_fonctions[i] = liste_fonctions[i].split(";")
                        liste_fonctions[i][3] = liste_fonctions[i][3].split(":")
                liste_dessin = sauvegarde[6].split("/")
                if liste_dessin == [""] : liste_dessin = []
                else :
                    for i in range (len(liste_dessin)) :
                        liste_dessin[i] = liste_dessin[i].split(";")
                    for i in range (len(liste_dessin)) :
                        if liste_dessin[i][0] == "1" : liste_dessin[i][0],liste_dessin[i][1],liste_dessin[i][2],liste_dessin[i][4] = int(liste_dessin[i][0]),int(liste_dessin[i][1]),int(liste_dessin[i][2]),int(liste_dessin[i][4])
                        elif liste_dessin[i][0] == "2" : liste_dessin[i][0],liste_dessin[i][1],liste_dessin[i][2],liste_dessin[i][4],liste_dessin[i][6] = int(liste_dessin[i][0]),int(liste_dessin[i][1]),int(liste_dessin[i][2]),int(liste_dessin[i][4]),int(liste_dessin[i][6])
                        elif liste_dessin[i][0] == "3" : liste_dessin[i][0],liste_dessin[i][1],liste_dessin[i][2],liste_dessin[i][4],liste_dessin[i][6] = int(liste_dessin[i][0]),int(liste_dessin[i][1]),int(liste_dessin[i][2]),int(liste_dessin[i][4]),int(liste_dessin[i][6])
                        elif liste_dessin[i][0] == "4" : liste_dessin[i][0],liste_dessin[i][1],liste_dessin[i][2],liste_dessin[i][5] = int(liste_dessin[i][0]),int(liste_dessin[i][1]),int(liste_dessin[i][2]),int(liste_dessin[i][5])
                i = -1
                while chemin_f[i] != "/" : i -= 1
                nom = chemin_f[i+1:]
                actualisation()
                affich()
                save = 1
                fenetre.title("Modélisateur de fonctions - "+nom)
        except :
            save = 1
            new_file()
            showerror("Erreur", "Le fichier n'a pas pu être ouvert.")

def raccourci_open_file(event) :
    open_file()

def save_file() :
    global save
    if chemin != "" and os.path.isfile(chemin) :
        f = open(chemin,"w")
        f.write(crea_sauvegarde())
        f.close()
        fenetre.title("Modélisateur de fonctions - "+nom)
        save = 1
    else : save_as_file()

def raccourci_save_file(event) :
    save_file()

def save_as_file() :
    global chemin
    global save
    global nom
    rep = asksaveasfilename(title="Enregistrer un fichier",filetypes=[('mf files','.mf')],defaultextension=".mf")
    if rep != "" :
        chemin = rep
        f = open(rep,"w")
        f.write(crea_sauvegarde())
        f.close()
        i = -1
        while rep[i] != "/" : i -= 1
        nom = rep[i+1:]
        fenetre.title("Modélisateur de fonctions - "+nom)
        save = 1

def raccourci_save_as_file(event) :
    save_as_file()

def crea_sauvegarde() :
    texte = str(xmin)+","+str(xmax)+","+str(ymin)+","+str(ymax)+","+str(pas)
    texte2 = []
    for i in liste_fonctions :
        texte2 += [[i[0],i[1],i[2],":".join(i[3])]]
    for i in range (len(texte2)) :
        texte2[i] = ";".join(texte2[i])
    texte += ","+"/".join(texte2)
    texte2 = []
    for i in liste_dessin :
        texte2 += [";".join([str(j) for j in i])]
    texte += ","+"/".join(texte2)
    return texte

def save_capture() :
    time.sleep(0.5)
    capture = ImageGrab.grab((canvas.winfo_rootx(),canvas.winfo_rooty(),canvas.winfo_rootx()+505,canvas.winfo_rooty()+505))
    rep = asksaveasfilename(title="Enregistrer une capture d'écran",filetypes=[('png files','.png'),('jpg files','.jpg'),('jpeg files','.jpeg')],defaultextension=".png")
    if rep != "" :
        capture.save(rep)

def raccourci_save_capture(event) :
    save_capture()

def actualisation() :
    global save
    try :
        cadre.destroy()
        crea_cadre()
    except : a = 0
    try :
        cadre16.destroy()
        crea_cadre16()
    except : a = 0
    try :
        cadre10.destroy()
        crea_cadre10()
    except : a = 0
    try :
        cadre18.destroy()
        crea_cadre18()
    except : a = 0
    affich()
    save = 0

def aide() :
    global fenetre_aide
    fenetre_aide = Tk()
    texte = Label(fenetre_aide,text="Ce programme permet de modéliser des fonctions dans un graphique et de faire des calculs à partir de celles-ci.\n\n\nDans le menu 'Mode' vous pouvez choisir entre le mode curseur qui vous donne l'abscisse et l'ordonnée de la souris sur le graphique, ou le mode 'Dessin' avec lequel vous pouvez dessiner sur le graphique.\n\nDans le menu 'Affichage' vous pouvez affichez ou cacher les volets d'utilisation.\n\nDans le menu 'Arrondi' vous pouvez modifier le nombre de décimales qu'auront les résultats des calculs.\n\nUne fois que vous avez fini de règler les paramètres du graphiques, de créer une fonction, ou de changer la couleur d'une fonction, cliquez sur 'Appliquer' pour voir les modifications s'opérer.\n\nDans le volet 'Fonctions', vous pouvez voir toutes vos fonctions. Pour en supprimer une cliquez sur elle puis sur le bouton 'Supprimer'.\n\nDans le volet 'Calcul' vous pouvez choisir différents calculs à l'aide des boutons '<' et '>' puis entrez les paramètres et cliquez sur 'Calculer' pour lancer le calcul.\n\nLe volet 'Dessin' vous permet de dessiner sur le graphique. L'outil 'Crayon' permet de dessiner des traits comme vous le voulez en restant appuyé sur le clic gauche et en bougeant la souris.\nL'outil 'Ligne' vous permet de dessiner une ligne droite en cliquant sur un premier point (le point de départ de la ligne) puis sur un deuxième point (le point de fin de la ligne).\nL'outil 'Cercle' vous permet de dessiner un cercle ou une ellipse en cliquant sur un premier point (le coin en haut à gauche) puis sur un deuxième point (le coin en haut à droite).\nL'outil 'Texte' vous permet d'écrire quelque chose en cliquant sur le graphique puis en tapant ce que vous voulez et enfin en cliquant à côté pour valider.\nCliquez droit sur un objet dans le graphique et appuyez sur 'suppr' pour le supprimer ou cliquez sur 'Effacer' pour effacer tous vos traits.\n\nPour utiliser les listes qu'on retrouve dans le choix des couleurs des fonctions mais aussi dans le volet 'Calcul' et le volet 'Dessin' vous pouvez utiliser la molette de la souris mais celle-ci fait défiler un peu vite.\nSinon vous pouvez cliquer sur la liste puis vous déplacer dedans en utilisant les flèches directionnelles du haut et du bas. (N'oubliez pas de cliquez sur votre choix sinon celui-ci ne sera pas validé)\n\n\nATTENTION : Les résultats de certains calculs peuvent être inexacts à quelque centièmes/millièmes près.").pack(side=TOP,padx=5,pady=5)
    fenetre_aide.title("Aide")
    fenetre_aide.resizable(width=False,height=False)
    fenetre_aide.mainloop()

def aide_fonctions() :
    global fenetre_aide_fonctions
    fenetre_aide_fonctions = Tk()
    texte = Label(fenetre_aide_fonctions,text="Lorsque vous créez des fonctions vous pouvez utiliser ces opérateurs :\n\n+ : addition\n- : soustraction\n* : multiplication\n/ : division\n^ : élever un nombre à une puissance\nsqrt() : racine carrée\nabs() : valeur absolue\ncos(),sin(),tan() : cosinus,sinus,tangente\nacos(),asin(),atan() : arccos,arcsin,arctan\n() : parenthèses").pack(side=TOP,padx=5,pady=5)
    fenetre_aide_fonctions.title("Aide")
    fenetre_aide_fonctions.resizable(width=False,height=False)
    fenetre_aide_fonctions.mainloop()

def select_dessin(event) :
    global select
    global rect_select
    try : canvas.delete(rect_select)
    except : a = 0
    non = 0
    for i in range(len(liste_dessin)) :
        if liste_dessin[i][0] == 4 :
            t,m = liste_dessin[i][3],0
            total = 0
            for j in t :
                if j == "\n" :
                    if total > m : m = total
                    total = 0
                else : total += 1
            if total > m : m = total
            m2 = t.count("\n")+1
            if liste_dessin[i][1]-(liste_dessin[i][5]*m)/2 < event.x < liste_dessin[i][1]+(liste_dessin[i][5]*m)/2 and liste_dessin[i][2]-liste_dessin[i][5]*m2 < event.y < liste_dessin[i][2]+liste_dessin[i][5]*m2 :
                select = [i,liste_dessin[i][1]-(liste_dessin[i][5]*m)/2,liste_dessin[i][2]-liste_dessin[i][5]*m2,liste_dessin[i][1]+(liste_dessin[i][5]*m)/2,liste_dessin[i][2]+liste_dessin[i][5]*m2]
                non = 1
                break
        elif liste_dessin[i][0] == 1 and liste_dessin[i][1]-liste_dessin[i][4] < event.x < liste_dessin[i][1]+liste_dessin[i][4] and liste_dessin[i][2]-liste_dessin[i][4] < event.y < liste_dessin[i][2]+liste_dessin[i][4] :
            select = [i,liste_dessin[i][1]-liste_dessin[i][4],liste_dessin[i][2]-liste_dessin[i][4],liste_dessin[i][1]+liste_dessin[i][4],liste_dessin[i][2]+liste_dessin[i][4]]
            non = 1
            break
        elif (liste_dessin[i][0] == 2 or liste_dessin[i][0] == 3) and liste_dessin[i][1]-(liste_dessin[i][1]-liste_dessin[i][3])/2-abs(liste_dessin[i][1]-liste_dessin[i][3])/2 < event.x < liste_dessin[i][1]-(liste_dessin[i][1]-liste_dessin[i][3])/2+abs(liste_dessin[i][1]-liste_dessin[i][3])/2 and liste_dessin[i][2]-(liste_dessin[i][2]-liste_dessin[i][4])/2-abs(liste_dessin[i][2]-liste_dessin[i][4])/2 < event.y < liste_dessin[i][2]-(liste_dessin[i][2]-liste_dessin[i][4])/2+abs(liste_dessin[i][2]-liste_dessin[i][4])/2 :
            select = [i,liste_dessin[i][1],liste_dessin[i][2],liste_dessin[i][3],liste_dessin[i][4]]
            non = 1
            break
    if non == 0 : select = []
    else : rect_select = canvas.create_rectangle(select[1],select[2],select[3],select[4],outline="blue")

def suppr_objet(event) :
    global liste_dessin
    global select
    global rect_select
    global save
    if len(select) > 0 :
        save = 0
        fenetre.title("Modélisateur de fonctions - "+nom+" *")
        del liste_dessin[select[0]]
        select = []
        canvas.delete(rect_select)
        affich()

def mouse_button_down(event) :
    global liste_dessin
    if dessin.get() == True and mode.get() == 0 :
        if forme.get() == "2" :
            if len(liste_dessin) > 0 and len(liste_dessin[-1]) == 3 :
                if liste_dessin[-1][0] == 2 :
                    liste_dessin[-1] += [event.x,event.y,b_c2.get("active"),taille]
                    affich()
                else : del liste_dessin[-1]
            else : liste_dessin += [[2,event.x,event.y]]
        elif forme.get() == "3" :
            if len(liste_dessin) > 0 and len(liste_dessin[-1]) == 3 :
                if liste_dessin[-1][0] == 3 :
                    liste_dessin[-1] += [event.x,event.y,b_c2.get("active"),taille]
                    affich()
                else : del liste_dessin[-1]
            else : liste_dessin += [[3,event.x,event.y]]
        elif forme.get() == "4" :
            if len(liste_dessin) > 0 and len(liste_dessin[-1]) == 4 :
                if liste_dessin[-1][0] == 4 and (len(liste_dessin[-1][3]) > 0 and len(liste_dessin[-1][3]) != liste_dessin[-1][3].count("\n")) :
                    while liste_dessin[-1][3][0] == "\n" : liste_dessin[-1][3] = liste_dessin[-1][3][1:]
                    while liste_dessin[-1][3][-1] == "\n" : liste_dessin[-1][3] = liste_dessin[-1][3][:-1]
                    liste_dessin[-1] += [b_c2.get("active"),taille]
                    affich()
                else : del liste_dessin[-1]
            else : liste_dessin += [[4,event.x,event.y,""]]

def mouse_motion(event) :
    global ligne
    global ligne_x
    global ligne_y
    global texte_curseur
    if dessin.get() == True and mode.get() == 0 :
        if forme.get() == "2" :
            if len(liste_dessin) > 0 and len(liste_dessin[-1]) == 3 :
                if liste_dessin[-1][0] == 2 :
                    try : canvas.delete(ligne)
                    except : a = 0
                    ligne = canvas.create_line(liste_dessin[-1][1],liste_dessin[-1][2],event.x,event.y,fill=b_c2.get("active"),width=taille)
                else : del liste_dessin[-1]
        elif forme.get() == "3" :
            if len(liste_dessin) > 0 and len(liste_dessin[-1]) == 3 :
                if liste_dessin[-1][0] == 3 :
                    try : canvas.delete(ligne)
                    except : a = 0
                    ligne = canvas.create_oval(liste_dessin[-1][1],liste_dessin[-1][2],event.x,event.y,outline=b_c2.get("active"),width=taille)
                else : del liste_dessin[-1]
    elif mode.get() == 1 :
        try :
            canvas.delete(ligne_x)
            canvas.delete(ligne_y)
            canvas.delete(texte_curseur)
        except : a = 0
        ligne_x = canvas.create_line(event.x,0,event.x,500,width=1,fill="red")
        ligne_y = canvas.create_line(0,event.y,500,event.y,width=1,fill="red")
        x,y = (abs(xmin)+abs(xmax))/500*event.x-abs(xmin),-(abs(ymin)+abs(ymax))/500*event.y+abs(ymin)
        texte_curseur = canvas.create_text(event.x,event.y-10,text="("+str(x)[:len(str(int(x)))+5]+";"+str(y)[:len(str(int(y)))+5]+")")

def mouse_motion_down(event) :
    global liste_dessin
    if dessin.get() == True and forme.get() == "1" and mode.get() == 0 :
        liste_dessin += [[1,event.x,event.y,b_c2.get("active"),taille]]
        canvas.create_oval(event.x-taille,event.y-taille,event.x+taille,event.y+taille,fill=b_c2.get("active"),outline=b_c2.get("active"))

def key_down(event) :
    global ligne
    if dessin.get() == True and mode.get() == 0 :
        if forme.get() == "4" and len(liste_dessin) >= 1 and liste_dessin[-1][0] == 4 and len(liste_dessin[-1]) == 4 :
            alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789àâäÀÂÄéèêëÈÊËÿùûüÙÛÜìîïÌÎÏòôöÒÔÖçñÑ.,;:?!+-*/%&~#'{([|`_^@°)]=}£$¤µ<> "
            if event.char in alpha : liste_dessin[-1][3] += event.char
            elif event.keysym == "Return" : liste_dessin[-1][3] += "\n"
            elif event.keysym == "BackSpace" and len(liste_dessin[-1][3]) > 0 : liste_dessin[-1][3] = liste_dessin[-1][3][:-1]
            try : canvas.delete(ligne)
            except : a = 0
            ligne = canvas.create_text(liste_dessin[-1][1],liste_dessin[-1][2],text=liste_dessin[-1][3],font="Serif "+str(taille),fill=b_c2.get("active"))

def suppr_curseur() :
    try :
        canvas.delete(ligne_x)
        canvas.delete(ligne_y)
        canvas.delete(texte_curseur)
    except : a = 0
    crea_canvas()

def show_param() :
    global cadre
    if param.get() == True : crea_cadre()
    else : cadre.destroy()

def show_fonctions() :
    global cadre16
    if fonctions.get() == True : crea_cadre16()
    else : cadre16.destroy()

def show_calcul() :
    global cadre10
    if calcul.get() == True : crea_cadre10()
    else : cadre10.destroy()

def show_dessin() :
    global cadre18
    if dessin.get() == True : crea_cadre18()
    else : cadre18.destroy()

def affich() :
    global canvas
    global save
    save = 0
    fenetre.title("Modélisateur de fonctions - "+nom+" *")
    canvas.delete("all")
    if grille == 1 :
        for i in range (abs(xmin)+abs(xmax)) :
            canvas.create_line(i*(500/(abs(xmin)+abs(xmax))),0,i*(500/(abs(xmin)+abs(xmax))),500,fill="grey")
        for i in range (abs(ymin)+abs(ymax)) :
            canvas.create_line(0,i*(500/(abs(ymin)+abs(ymax))),500,i*(500/(abs(ymin)+abs(ymax))),fill="grey")
        if style.get() == "2" :
            for i in range (abs(xmin)+abs(xmax)) :
                canvas.create_rectangle(i*(500/(abs(xmin)+abs(xmax)))+0.2*(500/(abs(xmin)+abs(xmax))),0,i*(500/(abs(xmin)+abs(xmax)))+0.8*(500/(abs(xmin)+abs(xmax))),500,fill="white",outline="white")
            for i in range (abs(ymin)+abs(ymax)) :
                canvas.create_rectangle(0,i*(500/(abs(ymin)+abs(ymax)))+0.2*(500/(abs(ymin)+abs(ymax))),500,i*(500/(abs(ymin)+abs(ymax)))+0.8*(500/(abs(ymin)+abs(ymax))),fill="white",outline="white")
    if axes == 1 :
        canvas.create_line(250+(-(xmin+xmax)/2)*(500/(abs(xmin)+abs(xmax))),0,250+(-(xmin+xmax)/2)*(500/(abs(xmin)+abs(xmax))),500,fill="black",width=2)
        canvas.create_line(0,250+(-(ymin+ymax)/2)*(500/(abs(ymin)+abs(ymax))),500,250+(-(ymin+ymax)/2)*(500/(abs(ymin)+abs(ymax))),fill="black",width=2)

    l = [image(i,xmin) for i in range (len(liste_fonctions))]
    if int(pas) == pas : arrondi,pas2 = 1,pas
    else :
        i = 0
        while int(pas*10**i) != pas*10**i : i += 1
        arrondi,pas2 = 10**i,pas*10**i
    for i in range (int((xmin+pas)*arrondi),int(xmax*arrondi)+1,int(pas2)) :
        for j in range (len(liste_fonctions)) :
            if image(j,i/arrondi) != None and l[j] != None :
                canvas.create_line(abs(xmin)*(500/(abs(xmin)+abs(xmax)))+(500/(abs(xmin)+abs(xmax)))*((i-pas2)/arrondi),abs(ymin)*(500/(abs(ymin)+abs(ymax)))-(500/(abs(ymin)+abs(ymax)))*l[j],abs(xmin)*(500/(abs(xmin)+abs(xmax)))+(500/(abs(xmin)+abs(xmax)))*(i/arrondi),abs(ymin)*(500/(abs(ymin)+abs(ymax)))-(500/(abs(ymin)+abs(ymax)))*image(j,i/arrondi),fill=liste_fonctions[j][1])
            l[j] = image(j,i/arrondi)

    if len(liste_dessin) > 0 and type(liste_dessin[-1][-2]) != str : del liste_dessin[-1]
    for i in liste_dessin :
        if i[0] == 1 : canvas.create_oval(i[1]-i[4],i[2]-i[4],i[1]+i[4],i[2]+i[4],fill=i[3],outline=i[3])
        elif i[0] == 2 : canvas.create_line(i[1],i[2],i[3],i[4],fill=i[5],width=i[6])
        elif i[0] == 3 : canvas.create_oval(i[1],i[2],i[3],i[4],outline=i[5],width=i[6])
        elif i[0] == 4 : canvas.create_text(i[1],i[2],text=i[3],font="Serif "+str(i[5]),fill=i[4])

def image(f,a) :
    try :
        f = list(liste_fonctions[f][3])
        i = 0
        while i < len(f) :
            if f[i:i+2] == ["(",")"] :
                del f[i:i+2]
                i = 0
            else : i += 1
        for i in range (len(f)) :
            if f[i] == "x" : f[i] = a
            else :
                try : f[i] = float(f[i])
                except : f[i] = f[i]
        i = 0
        while i < len(f)-1 :
            try :
                b = float(f[i+1])
                non = 0
            except : non = 1
            if f[i] == "-" and (i == 0 or i > 0 and f[i-1] == "(") and non == 0 :
                f[i+1] = -f[i+1]
                del f[i]
            i += 1
        while "(" in f :
            i = len(f)-1
            while f[i] != "(" : i -= 1
            j = i+1
            while f[j] != ")" : j += 1
            k = i+1
            while k < j-1 :
                if f[k+1] == "^" :
                    f[k] = f[k]**f[k+2]
                    j -= 2
                    del f[k+1:k+3]
                else : k += 2
            k = i+1
            while k < j-1 :
                if f[k+1] == "*" :
                    f[k] = f[k]*f[k+2]
                    j -= 2
                    del f[k+1:k+3]
                elif f[k+1] == "/" :
                    f[k] = f[k]/f[k+2]
                    j -= 2
                    del f[k+1:k+3]
                else : k += 2
            k = i+1
            while k < j-1 :
                if f[k+1] == "+" :
                    f[k] = f[k]+f[k+2]
                    j -= 2
                    del f[k+1:k+3]
                elif f[k+1] == "-" :
                    f[k] = f[k]-f[k+2]
                    j -= 2
                    del f[k+1:k+3]
                else : k += 2
            b = len(f)
            if f[i-1] == "sqrt" :
                f[i+1] = sqrt(f[i+1])
                del f[i]
            elif f[i-1] == "abs" :
                f[i+1] = abs(f[i+1])
                del f[i]
            elif f[i-1] == "cos" :
                if degres.get() == "1" : f[i+1] = cos(radians(f[i+1]))
                else : f[i+1] = cos(f[i+1])
                del f[i]
            elif f[i-1] == "acos" :
                if degres.get() == "1" : f[i+1] = acos(radians(f[i+1]))
                else : f[i+1] = acos(f[i+1])
                del f[i]
            elif f[i-1] == "sin" :
                if degres.get() == "1" : f[i+1] = sin(radians(f[i+1]))
                else : f[i+1] = sin(f[i+1])
                del f[i]
            elif f[i-1] == "asin" :
                if degres.get() == "1" : f[i+1] = asin(radians(f[i+1]))
                else : f[i+1] = asin(f[i+1])
                del f[i]
            elif f[i-1] == "tan" :
                if degres.get() == "1" : f[i+1] = tan(radians(f[i+1]))
                else : f[i+1] = tan(f[i+1])
                del f[i]
            elif f[i-1] == "atan" :
                if degres.get() == "1" : f[i+1] = atan(radians(f[i+1]))
                else : f[i+1] = atan(f[i+1])
                del f[i]
            if len(f) != b :
                i -= 1
                j -= 1
            f = f[:i]+[f[i+1]]+f[j+1:]
            k = 0
            while k < len(f)-1 :
                if f[k] == "-" and k == 0 or f[k-1] == "("  :
                    try :
                        b = float(f[k+1])
                        non = 0
                    except : non = 1
                    if non == 0 :
                        f[k] = -f[k+1]
                        del f[k+1]
                k += 1
        i = 0
        while i < len(f)-2 :
            if f[i+1] == "^" :
                f[i] = f[i]**f[i+2]
                del f[i+1:i+3]
            else : i += 2
        i = 0
        while i < len(f)-2 :
            if f[i+1] == "*" :
                f[i] = f[i]*f[i+2]
                del f[i+1:i+3]
            elif f [i+1] == "/" :
                f[i] = f[i]/f[i+2]
                del f[i+1:i+3]
            else : i += 2
        i = 0
        while i < len(f)-2 :
            if f[i+1] == "+" :
                f[i] = f[i]+f[i+2]
                del f[i+1:i+3]
            elif f[i+1] == "-" :
                f[i] = f[i]-f[i+2]
                del f[i+1:i+3]
            else : i += 2
        return f[0]
    except : return None

def change_fenetre() :
    global xmin
    global xmax
    global ymin
    global ymax
    global pas
    global save
    save = 0
    fenetre.title("Modélisateur de fonctions - "+nom+" *")
    non = 0
    a = entree1.get()
    for i in range (len(a)) :
        if a[i] != "-" and a[i] != "0" and a[i] != "1" and a[i] != "2" and a[i] != "3" and a[i] != "4" and a[i] != "5" and a[i] != "6" and a[i] != "7" and a[i] != "8" and a[i] != "9" :
            showerror("Erreur", "La valeur doit être un chiffre ou un nombre entier.")
            non = 1
            break
    a = entree2.get()
    for i in range (len(a)) :
        if a[i] != "-" and a[i] != "0" and a[i] != "1" and a[i] != "2" and a[i] != "3" and a[i] != "4" and a[i] != "5" and a[i] != "6" and a[i] != "7" and a[i] != "8" and a[i] != "9" :
            showerror("Erreur", "La valeur doit être un chiffre ou un nombre entier.")
            non = 1
            break
    a = entree3.get()
    for i in range (len(a)) :
        if a[i] != "-" and a[i] != "0" and a[i] != "1" and a[i] != "2" and a[i] != "3" and a[i] != "4" and a[i] != "5" and a[i] != "6" and a[i] != "7" and a[i] != "8" and a[i] != "9" :
            showerror("Erreur", "La valeur doit être un chiffre ou un nombre entier.")
            non = 1
            break
    a = entree4.get()
    for i in range (len(a)) :
        if a[i] != "-" and a[i] != "0" and a[i] != "1" and a[i] != "2" and a[i] != "3" and a[i] != "4" and a[i] != "5" and a[i] != "6" and a[i] != "7" and a[i] != "8" and a[i] != "9" :
            showerror("Erreur", "La valeur doit être un chiffre ou un nombre entier.")
            non = 1
            break
    a = entree5.get()
    for i in range (len(a)) :
        if a[i] != "." and a[i] != "0" and a[i] != "1" and a[i] != "2" and a[i] != "3" and a[i] != "4" and a[i] != "5" and a[i] != "6" and a[i] != "7" and a[i] != "8" and a[i] != "9" :
            showerror("Erreur", "La valeur doit être supérieure ou égale à 0.")
            non = 1
            break
    if non == 0 :
        if int(entree1.get()) >= int(entree2.get()) :
            showerror("Erreur", "Xmin ne peut pas être supérieur ou égal à xmax.")
            non = 1
    if non == 0 :
        if int(entree3.get()) >= int(entree4.get()) :
            showerror("Erreur", "Ymin ne peut pas être supérieur ou égal à ymax.")
            non = 1
    if non == 0 :
        xmin = int(entree1.get())
        xmax = int(entree2.get())
        ymin = int(entree3.get())
        ymax = int(entree4.get())
        pas = float(entree5.get())
        affich()

def b_aff_axes() :
    global axes
    if axes == 0 : axes = 1
    else : axes = 0

def b_aff_grille() :
    global grille
    global cadre7
    global cadre22
    global style
    cadre7.destroy()
    cadre22.destroy()
    if grille == 0 : grille = 1
    else : grille = 0
    cadre7 = LabelFrame(cadre6,text="",padx=0,pady=0)
    cadre7.pack(side=TOP,fill="both",expand="no")
    style = StringVar()
    if grille == 0 :
        b_style1 = Radiobutton(cadre7,text="Traits",variable=style,value=1,state=DISABLED)
        b_style1.pack(side=LEFT,padx=0,pady=0)
        b_style2 = Radiobutton(cadre7,text="Pointillés",variable=style,value=2,state=DISABLED)
        b_style2.pack(side=LEFT,padx=0,pady=0)
    else :
        b_style1 = Radiobutton(cadre7,text="Traits",variable=style,value=1,state=ACTIVE)
        b_style1.pack(side=LEFT,padx=0,pady=0)
        b_style2 = Radiobutton(cadre7,text="Pointillés",variable=style,value=2,state=ACTIVE)
        b_style2.pack(side=LEFT,padx=0,pady=0)
    b_style1.select()
    cadre22 = LabelFrame(cadre6,text="",padx=0,pady=0)
    cadre22.pack(side=TOP,fill="both",expand="no")
    b_degres = Radiobutton(cadre22,text="Degrés",variable=degres,value=1,state=ACTIVE)
    b_degres.pack(side=LEFT,padx=0,pady=0)
    b_radians = Radiobutton(cadre22,text="Radians",variable=degres,value=2,state=ACTIVE)
    b_radians.pack(side=LEFT,padx=0,pady=0)


def ajout_fonction() :
    global liste_fonctions
    global cadre9
    global b_f
    global b_c
    global save
    save = 0
    fenetre.title("Modélisateur de fonctions - "+nom+" *")
    alpha = "0123456789.-+-*/^()sqrtabcoinx"
    a = entree6.get()
    non = 0
    for i in a :
        if not i in alpha :
            non = 1
            break
    if non == 0 :
        if a.count("(") != a.count(")") : non = 1
        else :
            for i in range (a.count("(")) :
                j,k = 0,0
                while k < i+1 :
                    if a[j] == ")" : k += 1
                    j += 1
                for l in a[:j] :
                    if l == "(" : k -= 1
                if k > 0 :
                    non = 1
                    break
    if non == 0 :
        alpha2 = "+-*/^"
        alpha3 = "0123456789"
        for i in range (len(a)) :
            if a[i] == "s" and a[i:i+5] != "sqrt(" and a[i:i+4] != "sin(" and not (i > 1 and (a[i-1] == "b" or a[i-1] == "o") or i > 0 and a[i-1] == "a") or a[i] == "a" and a[i:i+4] != "abs(" and a[i:i+5] != "acos(" and a[i:i+5] != "asin(" and a[i:i+5] != "atan(" and not (i > 0 and a[i-1] == "t") or a[i] == "c" and a[i:i+4] != "cos(" or a[i] == "t" and a[i:i+4] != "tan(" and not (i > 0 and (a[i-1] == "r" or a[i-1] == "a")) or a[i] in alpha2 and (i == 0 and a[i] != "-" or i == len(a)-1 or i > 0 and (a[i-1] in alpha2 or a[i-1] == "(" and a[i] != "-") or i < len(a)-1 and (a[i+1] in alpha2 or a[i+1] == ")")) or a[i] == "." and (i == 0 or i < len(a)-1 and not a[i+1] in alpha3) :
                non = 1
                break
    if non == 1 or a == "" :
        showerror("Erreur", "Formule invalide.")
    else :
        if len(liste_fonctions) > 0 :
            if ord(liste_fonctions[-1][0][len(liste_fonctions[-1][0])-4]) == 122 :
                liste_fonctions += [[liste_fonctions[-1][0][0:len(liste_fonctions[-1][0])-3]+"a(x)","purple",a,transform_fonction(a)]]
            else :
                if len(liste_fonctions) > 26 :
                    liste_fonctions += [[liste_fonctions[-1][0][0:len(liste_fonctions[-1][0])-4]+chr(ord(liste_fonctions[-1][0][-4])+1)+"(x)","purple",a,transform_fonction(a)]]
                else :
                    liste_fonctions += [[chr(ord(liste_fonctions[-1][0][-4])+1)+"(x)","purple",a,transform_fonction(a)]]
        else :
            liste_fonctions += [["a(x)","purple",a,transform_fonction(a)]]
    crea_cadre9()
    if fonctions.get() == True :
        cadre17.destroy()
        crea_cadre17()
    if calcul.get() == True :
        cadre12.destroy()
        crea_cadre12()

def transform_fonction(fonction) :
    f = []
    a = ""
    alpha1 = "0123456789."
    alpha2 = "+-*/^"
    alpha3 = "sqrtabcoin"
    for i in fonction :
        if i in alpha1 :
            if a == "x" :
                f += [a,"*"]
                a = ""
            elif len(f) > 0 and f[-1] == ")" : f += ["*"]
            a += i
        elif i in alpha2 :
            if a != "" :
                f += [a]
                a = ""
            f += [i]
        elif i == "(" :
            if a != "" :
                f += [a,"*",i]
                a = ""
            elif len(f) > 0 and f[-1] == ")" :
                f += ["*",i]
            else : f += [i]
        elif i == ")" :
            if a != "" :
                f += [a]
                a = ""
            f += [i]
        elif i == "x" :
            if a != "" : f += [a,"*"]
            elif len(f) > 0 and f[-1] == ")" : f += ["*"]
            a = i
        elif i in alpha3 :
            if i == "c" and a != "a" or i == "s" and a != "a" and a != "co" and a != "ab" or i == "t" and a != "a" and a != "sqr" or i == "a" and a != "t" and a != "at" :
                if a != "" : f += [a,"*"]
                a = i
            elif i == "s" and (a == "co" or a == "aco" or a == "ab") or i == "n" and (a == "si" or a == "asi" or a == "ta" or a == "ata") or i == "t" and a == "sqr" :
                f += [a+i]
                a = ""
            else : a += i
    if a != "" : f += [a]
    return f

def suppr_fonc() :
    global liste_fonctions
    global save
    if len(liste_fonctions) > 0 :
        save = 0
        fenetre.title("Modélisateur de fonctions - "+nom+" *")
        a = ""
        i = 0
        while b_f4.get("active")[i] != " " :
            a += b_f4.get("active")[i]
            i += 1
        j = 0
        while liste_fonctions[j][0] != a :
            j += 1
        del liste_fonctions[j]
        crea_cadre9()
        if fonctions.get() == True :
            cadre16.destroy()
            crea_cadre16()
        if calcul.get() == True :
            cadre12.destroy()
            crea_cadre12()
    else :
        showerror("Erreur", "Vous n'avez pas créé de fonction.")

def set_color() :
    global liste_fonctions
    global save
    if len(liste_fonctions) > 0 :
        save = 0
        fenetre.title("Modélisateur de fonctions - "+nom+" *")
        i = 0
        while liste_fonctions[i][0] != b_f.get("active") :
            i += 1
        liste_fonctions[i][1] = b_c.get("active")

def change_option1() :
    global option
    global cadre11
    option -= 1
    if option == -1 : option = len(liste_options)-1
    cadre11.destroy()
    cadre12.destroy()
    crea_cadre11()

def change_option2() :
    global option
    global cadre11
    option += 1
    if option == len(liste_options) : option = 0
    cadre11.destroy()
    cadre12.destroy()
    crea_cadre11()

def calcul_image() :
    global b_calcul
    global texte_reponse
    try : texte_reponse.destroy()
    except : a = 0
    if len(liste_fonctions) > 0 :
        non = 0
        alpha = "0123456789.-"
        for i in entree7.get() :
            if not i in alpha :
                non = 1
                break
        if non == 0 and entree7.get() != "" :
            i = 0
            while liste_fonctions[i][0] != b_f2.get("active") :
                i += 1
            b_calcul.destroy()
            if image(i,float(entree7.get())) != None : texte_reponse = Label(cadre12,text=liste_fonctions[i][0][:-2]+entree7.get()+") = "+str(image(i,float(entree7.get()))))
            else : texte_reponse = Label(cadre12,text="Aucun résultat")
            texte_reponse.pack(side=TOP,padx=0,pady=0)
            b_calcul = Button(cadre12,text="Calculer",command=calcul_image)
            b_calcul.pack(side=TOP,padx=0,pady=5)
        else :
            showerror("Erreur", "Valeur incorrecte de x.")
    else :
        showerror("Erreur", "Aucune fonction sélectionnée.")

def calcul_antecedent() :
    global b_calcul
    global texte_reponse
    try : texte_reponse.destroy()
    except : a = 0
    if len(liste_fonctions) > 0 :
        non = 0
        alpha = "0123456789.-"
        for i in entree7.get() :
            if not i in alpha :
                non = 1
                break
        if non == 0 and entree7.get() != "" :
            for i in entree8.get() :
                if not i in alpha :
                    non = 1
                    break
            for i in entree9.get() :
                if not i in alpha :
                    non = 1
                    break
            if non == 0 and float(entree8.get()) < float(entree9.get()) :
                i = 0
                while liste_fonctions[i][0] != b_f2.get("active") :
                    i += 1
                j = float(entree8.get())
                while j < float(entree9.get()) :
                    if image(i,j) != None and abs(float(entree7.get())-image(i,j)) <= 10**(-(decimales.get()-1)) : break
                    else : j += 5*10**(-(decimales.get()-1))
                j,k = str(j),0
                while j[k] != "." : k += 1
                j = j[:k+decimales.get()+1]
                while len(j[k+1:len(j)]) < decimales.get() : j += "0"
                if j[-1] == "." : j = j[:-1]
                b_calcul.destroy()
                if image(i,float(j)) != None and abs(float(entree7.get())-image(i,float(j))) <= 10**(-(decimales.get()-1)) : texte_reponse = Label(cadre12,text=liste_fonctions[i][0][:-2]+j+") = "+entree7.get())
                else : texte_reponse = Label(cadre12,text="Aucun résultat")
                texte_reponse.pack(side=TOP,padx=0,pady=0)

                b_calcul = Button(cadre12,text="Calculer",command=calcul_antecedent)
                b_calcul.pack(side=TOP,padx=0,pady=5)
            else :
                showerror("Erreur", "Interval incorrect.")
        else :
            showerror("Erreur", "Valeur incorrecte de y.")
    else :
        showerror("Erreur", "Aucune fonction sélectionnée.")

def calcul_min_max() :
    global b_calcul
    global texte_reponse
    try : texte_reponse.destroy()
    except : a = 0
    if len(liste_fonctions) > 0 :
        non = 0
        alpha = "0123456789.-"
        for i in entree8.get() :
            if not i in alpha :
                non = 1
                break
        for i in entree9.get() :
            if not i in alpha :
                non = 1
                break
        if non == 0 and entree8.get() != "" and entree9.get() != "" and float(entree8.get()) < float(entree9.get()) :
            i = 0
            while liste_fonctions[i][0] != b_f2.get("active") :
                i += 1
            min = float(entree8.get())
            max = float(entree9.get())
            if option == 2 :
                while max-min > 10**(-decimales.get()) :
                    if image(i,min+(max-min)/3) != None and image(i,min+(max-min)/3*2) != None and image(i,min+(max-min)/3) == image(i,min+(max-min)/3*2) : min,max = min+(max-min)/3,min+(max-min)/3*2
                    elif image(i,min+(max-min)/3) != None and image(i,min+(max-min)/3*2) != None and image(i,min+(max-min)/3) < image(i,min+(max-min)/3*2) : max = min+(max-min)/3*2
                    elif image(i,min+(max-min)/3) != None and image(i,min+(max-min)/3*2) != None and image(i,min+(max-min)/3) > image(i,min+(max-min)/3*2) : min = min+(max-min)/3
                    else : break
            else :
                while max-min > 10**(-decimales.get()) :
                    if image(i,min+(max-min)/3) != None and image(i,min+(max-min)/3*2) != None and image(i,min+(max-min)/3) == image(i,min+(max-min)/3*2) : min,max = min+(max-min)/3,min+(max-min)/3*2
                    elif image(i,min+(max-min)/3) != None and image(i,min+(max-min)/3*2) != None and image(i,min+(max-min)/3) > image(i,min+(max-min)/3*2) : max = min+(max-min)/3*2
                    elif image(i,min+(max-min)/3) != None and image(i,min+(max-min)/3*2) != None and image(i,min+(max-min)/3) < image(i,min+(max-min)/3*2) : min = min+(max-min)/3
                    else : break
            j = str(min+(max-min)/2)
            if "e" in j :
                k,l = -1,0
                while j[k] != "e" : k -= 1
                p = int(j[k+1:])
                while j[l] != "." : l += 1
                if j[0] == "-" : m = 1
                else : m = 0
                j = "0."+j[:k+p][m:l]+j[:k+p][m:l]+j[:k+p][m:l]+j[:k+p][l+1:]
                for n in range (abs(p)-1) :
                    j = "0.0"+j[2:]
                if m == 1 : j = "-"+j
            k = 0
            while j[k] != "." : k += 1
            j = j[:k+decimales.get()+1]
            while len(j[k+1:len(j)]) < decimales.get() : j += "0"
            if j[-1] == "." : j = j[:-1]
            k = 0
            resultat = str(image(i,float(j)))
            b_calcul.destroy()
            if resultat != "None" :
                while resultat[k] != "." : k += 1
                resultat = resultat[:k+decimales.get()+1]
                while len(resultat[k+1:len(resultat)]) < decimales.get() : resultat += "0"
                if resultat[-1] == "." : resultat = resultat[:-1]
                texte_reponse = Label(cadre12,text=liste_fonctions[i][0][:-2]+j+") = "+resultat)
            else : texte_reponse = Label(cadre12,text="Aucun résultat")
            texte_reponse.pack(side=TOP,padx=0,pady=0)

            b_calcul = Button(cadre12,text="Calculer",command=calcul_min_max)
            b_calcul.pack(side=TOP,padx=0,pady=5)
        else :
            showerror("Erreur", "Interval incorrect.")
    else :
        showerror("Erreur", "Aucune fonction sélectionnée.")

def calcul_tangente() :
    global b_calcul
    global texte_reponse
    try : texte_reponse.destroy()
    except : a = 0
    if len(liste_fonctions) > 0 :
        non = 0
        alpha = "0123456789.-"
        for i in entree7.get() :
            if not i in alpha :
                non = 1
                break
        if non == 0 and entree7.get() != "" :
            i = 0
            while liste_fonctions[i][0] != b_f2.get("active") :
                i += 1
            x = float(entree7.get())
            h = 1*10**(-decimales.get())
            b_calcul.destroy()
            if image(i,x) != None and image(i,x+h) != None :
                affich()
                canvas.create_line(0,(500-abs(ymin)*(500/(abs(ymin)+abs(ymax))))-(((image(i,x+h)-image(i,x))/h)*(xmin-x)+image(i,x))*(500/(abs(ymin)+abs(ymax))),500,(500-abs(ymin)*(500/(abs(ymin)+abs(ymax))))-(((image(i,x+h)-image(i,x))/h)*(xmax-x)+image(i,x))*(500/(abs(ymin)+abs(ymax))),fill="red")
                texte_reponse = Label(cadre12,text=liste_fonctions[i][0][:-3]+"'(x) = "+str(((image(i,x+h)-image(i,x))/h))+"*(x+"+str(-x)+")+"+str(image(i,x)))
            else : texte_reponse = Label(cadre12,text="Aucun résultat")
            texte_reponse.pack(side=TOP,padx=0,pady=0)

            b_calcul = Button(cadre12,text="Calculer",command=calcul_tangente)
            b_calcul.pack(side=TOP,padx=0,pady=5)
        else :
            showerror("Erreur", "Valeur incorrecte de x.")
    else :
        showerror("Erreur", "Aucune fonction sélectionnée.")

def set_taille() :
    global taille
    non = 0
    alpha = "0123456789"
    for i in entree10.get() :
        if not i in alpha :
            non = 1
            showerror("Erreur", "La valeur doit être un chiffre ou un nombre entier positif.")
            break
    if non == 0 and entree10.get() != "" :
        taille = int(entree10.get())

def efface_dessin() :
    global liste_dessin
    global save
    save = 0
    fenetre.title("Modélisateur de fonctions - "+nom+" *")
    liste_dessin = []
    affich()

def change_forme() :
    if forme.get() == "4" : canvas.focus_set()
    else : fenetre.focus_set()

def crea_canvas() :
    global canvas
    try : canvas.destroy()
    except : a = 0
    if mode.get() == 0 : canvas = Canvas(fenetre,width=500,height=500,bg="white")
    else : canvas = Canvas(fenetre,width=500,height=500,bg="white",cursor="none")
    canvas.bind("<Button-1>",mouse_button_down)
    canvas.bind("<Button-3>",select_dessin)
    canvas.bind("<Motion>",mouse_motion)
    canvas.bind("<B1-Motion>",mouse_motion_down)
    canvas.bind("<Key>",key_down)
    canvas.pack(side=LEFT,padx=5,pady=5)
    try :
        cadre.destroy()
        crea_cadre()
    except : a = 0
    try :
        cadre16.destroy()
        crea_cadre16()
    except : a = 0
    try :
        cadre10.destroy()
        crea_cadre10()
    except : a = 0
    try :
        cadre18.destroy()
        crea_cadre18()
    except : a = 0
    affich()

def crea_cadre() :
    global cadre
    global cadre6
    global cadre7
    global cadre22
    global entree1
    global entree2
    global entree3
    global entree4
    global entree5
    global entree6
    global entree7
    global entree8
    global entree9
    global axes
    global grille
    global style
    global degres
    cadre = LabelFrame(fenetre,text="Paramètres :",padx=5,pady=5)
    cadre.pack(side=LEFT,fill="both",expand="yes")

    cadre2 = LabelFrame(cadre,text="Fenêtre :",padx=5,pady=5)
    cadre2.pack(side=TOP,fill="both",expand="no")

    cadre3 = LabelFrame(cadre2,text="",padx=0,pady=0)
    cadre3.pack(side=TOP,fill="both",expand="no")
    texte_xmin = Label(cadre3,text="xmin :").pack(side=LEFT,padx=0,pady=0)
    b_xmin = StringVar()
    b_xmin.set(str(xmin))
    entree1 = Entry(cadre3,textvariable=b_xmin,width=5)
    entree1.pack(side=LEFT,padx=0,pady=0)
    texte_xmax = Label(cadre3,text="xmax :").pack(side=LEFT,padx=0,pady=0)
    b_xmax = StringVar()
    b_xmax.set(str(xmax))
    entree2 = Entry(cadre3,textvariable=b_xmax,width=5)
    entree2.pack(side=LEFT,padx=0,pady=0)

    cadre4 = LabelFrame(cadre2,text="",padx=0,pady=0)
    cadre4.pack(side=TOP,fill="both",expand="no")
    texte_ymin = Label(cadre4,text="ymin :").pack(side=LEFT,padx=0,pady=0)
    b_ymin = StringVar()
    b_ymin.set(str(ymin))
    entree3 = Entry(cadre4,textvariable=b_ymin,width=5)
    entree3.pack(side=LEFT,padx=0,pady=0)
    texte_ymax = Label(cadre4,text="ymax :").pack(side=LEFT,padx=0,pady=0)
    b_ymax = StringVar()
    b_ymax.set(str(ymax))
    entree4 = Entry(cadre4,textvariable=b_ymax,width=5)
    entree4.pack(side=LEFT,padx=0,pady=0)

    cadre5 = LabelFrame(cadre2,text="",padx=0,pady=0)
    cadre5.pack(side=TOP,fill="both",expand="no")
    texte_pas = Label(cadre5,text="Pas de trace :").pack(side=LEFT,padx=0,pady=0)
    b_pas = StringVar()
    b_pas.set(str(pas))
    entree5 = Entry(cadre5,textvariable=b_pas,width=5)
    entree5.pack(side=LEFT,padx=0,pady=0)

    cadre6 = LabelFrame(cadre2,text="",padx=0,pady=0)
    cadre6.pack(side=TOP,fill="both",expand="no")
    b_axes = Checkbutton(cadre6,text="Axes",command=b_aff_axes).pack(side=TOP,anchor="w",padx=0,pady=0)
    b_grille = Checkbutton(cadre6,text="Grille",command=b_aff_grille).pack(side=TOP,anchor="w",padx=0,pady=0)

    cadre7 = LabelFrame(cadre6,text="",padx=0,pady=0)
    cadre7.pack(side=TOP,fill="both",expand="no")
    style = StringVar()
    if grille == 0 : b_style1 = Radiobutton(cadre7,text="Traits",variable=style,value=1,state=DISABLED)
    else : b_style1 = Radiobutton(cadre7,text="Traits",variable=style,value=1,state=ACTIVE)
    b_style1.pack(side=LEFT,padx=0,pady=0)
    if axes == 0 : b_style2 = Radiobutton(cadre7,text="Pointillés",variable=style,value=2,state=DISABLED)
    else : b_style2 = Radiobutton(cadre7,text="Pointillés",variable=style,value=2,state=ACTIVE)
    b_style2.pack(side=LEFT,padx=0,pady=0)
    style.set("1")

    cadre22 = LabelFrame(cadre6,text="",padx=0,pady=0)
    cadre22.pack(side=TOP,fill="both",expand="no")
    degres = StringVar()
    b_degres = Radiobutton(cadre22,text="Degrés",variable=degres,value=1,state=ACTIVE)
    b_degres.pack(side=LEFT,padx=0,pady=0)
    b_radians = Radiobutton(cadre22,text="Radians",variable=degres,value=2,state=ACTIVE)
    b_radians.pack(side=LEFT,padx=0,pady=0)
    degres.set("1")

    b_appliquer = Button(cadre2,text="Appliquer",command=change_fenetre).pack()

    cadre8 = LabelFrame(cadre,text="Nouvelle fonction :",padx=5,pady=5)
    cadre8.pack(fill="both",expand="no")
    texte_fx = Label(cadre8,text="f(x)=").pack(side=LEFT,padx=0,pady=5)
    fx = StringVar()
    fx.set("")
    entree6 = Entry(cadre8,textvariable=fx,width=25)
    entree6.pack(side=LEFT,padx=0,pady=5)
    b_appliquer2 = Button(cadre8,text=">",command=ajout_fonction).pack(side=LEFT,padx=0,pady=5)

    crea_cadre9()

def crea_cadre9() :
    global cadre9
    global b_f
    global b_c
    try :
        cadre9.destroy()
    except :
        a = 0
    cadre9 = LabelFrame(cadre,text="Couleurs :",padx=5,pady=5)
    cadre9.pack(fill="both",expand="no")
    b_f = Listbox(cadre9,width=14,height=1)
    for i in range (len(liste_fonctions)) :
        b_f.insert(i+1,liste_fonctions[i][0])
    b_f.pack(side=LEFT,padx=0,pady=5)
    texte_couleur = Label(cadre9,text=":").pack(side=LEFT,padx=0,pady=0)
    b_c = Listbox(cadre9,width=14,height=1)
    for i in ("purple","blue","green","yellow","orange","red","pink","brown","white","grey","black") :
        b_c.insert("end",i)
    b_c.pack(side=LEFT,padx=0,pady=5)
    b_appliquer3 = Button(cadre9,text=">",command=set_color).pack(side=LEFT,padx=0,pady=5)

def crea_cadre10() :
    global cadre10
    cadre10 = LabelFrame(fenetre,text="Calcul :",padx=5,pady=5)
    cadre10.pack(side=LEFT,fill="both",expand="yes")

    crea_cadre11()

def crea_cadre11() :
    global cadre11
    cadre11 = LabelFrame(cadre10,text="",padx=0,pady=0)
    cadre11.pack(side=TOP,fill="both",expand="no")
    b_gauche = Button(cadre11,text="<",command=change_option1).pack(side=LEFT,padx=0,pady=5)
    texte_option = Label(cadre11,text=liste_options[option]).pack(side=LEFT,padx=0,pady=5)
    b_droite = Button(cadre11,text=">",command=change_option2).pack(side=LEFT,padx=0,pady=5)

    crea_cadre12()

def crea_cadre12() :
    global cadre12
    global b_f2
    global b_calcul
    global entree7
    global entree8
    global entree9
    cadre12 = LabelFrame(cadre10,text="",padx=0,pady=0)
    cadre12.pack(side=TOP,fill="both",expand="no")
    cadre13 = LabelFrame(cadre12,text="",padx=0,pady=0)
    cadre13.pack(side=TOP,fill="both",expand="no")
    texte_fonction = Label(cadre13,text="Fonction :").pack(side=LEFT,padx=0,pady=5)
    b_f2 = Listbox(cadre13,width=12,height=1)
    for i in range (len(liste_fonctions)) :
        b_f2.insert(i+1,liste_fonctions[i][0])
    b_f2.pack(side=LEFT,padx=0,pady=5)
    cadre14 = LabelFrame(cadre12,text="",padx=0,pady=0)
    cadre14.pack(side=TOP,fill="both",expand="no")
    if option == 0 or option == 1 or option == 4 :
        if option == 0 or option == 4 : texte_fonction = Label(cadre14,text="x :").pack(side=LEFT,padx=0,pady=5)
        else : texte_fonction = Label(cadre14,text="y :").pack(side=LEFT,padx=0,pady=5)
        b_x = StringVar()
        b_x.set("")
        entree7 = Entry(cadre14,textvariable=b_x,width=19)
        entree7.pack(side=LEFT,padx=0,pady=0)
    if option == 1 or option == 2 or option == 3 :
        cadre15 = LabelFrame(cadre12,text="",padx=0,pady=0)
        cadre15.pack(side=TOP,fill="both",expand="no")
        texte_interval = Label(cadre15,text="Interval de x : [").pack(side=LEFT,padx=0,pady=0)
        b_deb = StringVar()
        b_deb.set("")
        entree8 = Entry(cadre15,textvariable=b_deb,width=2)
        entree8.pack(side=LEFT,padx=0,pady=0)
        texte_interval = Label(cadre15,text=";").pack(side=LEFT,padx=0,pady=0)
        b_fin = StringVar()
        b_fin.set("")
        entree9 = Entry(cadre15,textvariable=b_fin,width=2)
        entree9.pack(side=LEFT,padx=0,pady=0)
        texte_interval = Label(cadre15,text="]").pack(side=LEFT,padx=0,pady=0)
    if option == 0 : b_calcul = Button(cadre12,text="Calculer",command=calcul_image)
    elif option == 1 : b_calcul = Button(cadre12,text="Calculer",command=calcul_antecedent)
    elif option == 2 or option == 3 : b_calcul = Button(cadre12,text="Calculer",command=calcul_min_max)
    elif option == 4 : b_calcul = Button(cadre12,text="Calculer",command=calcul_tangente)
    b_calcul.pack(side=TOP,padx=0,pady=5)

def crea_cadre16() :
    global cadre16
    cadre16 = LabelFrame(fenetre,text="Fonctions :",padx=5,pady=5)
    cadre16.pack(side=LEFT,fill="both",expand="yes")

    crea_cadre17()

def crea_cadre17() :
    global cadre17
    global b_f4
    cadre17 = LabelFrame(cadre16,text="",padx=5,pady=5)
    cadre17.pack(side=TOP,fill="both",expand="yes")
    b_f4 = Listbox(cadre17,width=30,height=26)
    for i in range (len(liste_fonctions)) :
        b_f4.insert(i+1,liste_fonctions[i][0]+" = "+liste_fonctions[i][2])
    b_f4.pack(side=TOP,padx=0,pady=5)
    b_suppr = Button(cadre17,text="Supprimer",command=suppr_fonc).pack(side=TOP,padx=0,pady=5)

def crea_cadre18() :
    global cadre18
    global b_c2
    global entree10
    global forme
    cadre18 = LabelFrame(fenetre,text="Dessin :",padx=5,pady=5)
    cadre18.pack(side=LEFT,fill="both",expand="yes")
    cadre19 = LabelFrame(cadre18,text="Couleur :",padx=5,pady=5)
    cadre19.pack(side=TOP,fill="both",expand="no")
    b_c2 = Listbox(cadre19,width=30,height=1)
    for i in ("purple","blue","green","yellow","orange","red","pink","brown","white","grey","black") :
        b_c2.insert("end",i)
    b_c2.pack(side=TOP,padx=0,pady=5)
    cadre20 = LabelFrame(cadre18,text="Outils :",padx=5,pady=5)
    cadre20.pack(side=TOP,fill="both",expand="no")
    forme = StringVar()
    b_forme1 = Radiobutton(cadre20,text="Crayon",variable=forme,value=1,state=ACTIVE,command=change_forme)
    b_forme1.pack(side=TOP,anchor="w",padx=0,pady=0)
    b_forme2 = Radiobutton(cadre20,text="Ligne",variable=forme,value=2,state=ACTIVE,command=change_forme)
    b_forme2.pack(side=TOP,anchor="w",padx=0,pady=0)
    b_forme3 = Radiobutton(cadre20,text="Cercle",variable=forme,value=3,state=ACTIVE,command=change_forme)
    b_forme3.pack(side=TOP,anchor="w",padx=0,pady=0)
    b_forme4 = Radiobutton(cadre20,text="Texte",variable=forme,value=4,state=ACTIVE,command=change_forme)
    b_forme4.pack(side=TOP,anchor="w",padx=0,pady=0)
    forme.set("1")
    cadre21 = LabelFrame(cadre18,text="Taille de trait/police :",padx=5,pady=5)
    cadre21.pack(side=TOP,fill="both",expand="no")
    b_taille = StringVar()
    b_taille.set("2")
    entree10 = Entry(cadre21,textvariable=b_taille,width=27)
    entree10.pack(side=LEFT,padx=0,pady=0)
    b_appliquer4 = Button(cadre21,text=">",command=set_taille).pack(side=LEFT,padx=0,pady=5)
    b_efface_dessin = Button(cadre18,text="Effacer",command=efface_dessin).pack(side=TOP,padx=0,pady=5)

liste_fonctions = []
liste_options = ["image","antécédent","min","max","tangente"]
liste_dessin = []
option = 0
taille = 2
xmin,xmax,ymin,ymax,pas = -10,10,-10,10,0.1
axes,grille = 0,0
select = []
save = 0
chemin = ""
nom = "Sans Nom"

fenetre = Tk()
fenetre.title("Modélisateur de fonctions - Sans Nom *")

menubar = Menu(fenetre)

menu = Menu(menubar,tearoff=0)
menu.add_command(label="Nouveau",command=new_file,accelerator="Ctrl+n")
menu.add_command(label="Ouvrir...",command=open_file,accelerator="Ctrl+o")
menu.add_command(label="Enregistrer",command=save_file,accelerator="Ctrl+s")
menu.add_command(label="Enregistrer sous...",command=save_as_file,accelerator="Ctrl+Shift+s")
menu.add_command(label="Enregistrer une capture d'écran",command=save_capture,accelerator="Ctrl+Alt+s")
menu.add_separator()
menu.add_command(label="Quitter",command=alerte_fermeture,accelerator="Alt+F4")
menubar.add_cascade(label="Fichier",menu=menu)

menu0 = Menu(menubar,tearoff=0)
mode = IntVar()
menu0.add_radiobutton(label="Dessin",variable=mode,value=0,state=ACTIVE,command=suppr_curseur)
menu0.add_radiobutton(label="Curseur",variable=mode,value=1,state=ACTIVE,command=crea_canvas)
mode.set(0)
menubar.add_cascade(label="Mode",menu=menu0)

menu1 = Menu(menubar,tearoff=0)
param = BooleanVar()
param.set(True)
menu1.add_checkbutton(label="Paramètres",command=show_param,variable=param)
fonctions = BooleanVar()
fonctions.set(False)
menu1.add_checkbutton(label="Fonctions",command=show_fonctions,variable=fonctions)
calcul = BooleanVar()
calcul.set(False)
menu1.add_checkbutton(label="Calcul",command=show_calcul,variable=calcul)
dessin = BooleanVar()
dessin.set(False)
menu1.add_checkbutton(label="Dessin",command=show_dessin,variable=dessin)
menubar.add_cascade(label="Affichage",menu=menu1)


menu2 = Menu(menubar,tearoff=0)
menu_arrondi = Menu(menu2,tearoff=0)
decimales = IntVar()
menu_arrondi.add_radiobutton(label="0 décimales",variable=decimales,value=0,state=ACTIVE)
menu_arrondi.add_radiobutton(label="1 décimale",variable=decimales,value=1,state=ACTIVE)
menu_arrondi.add_radiobutton(label="2 décimales",variable=decimales,value=2,state=ACTIVE)
menu_arrondi.add_radiobutton(label="3 décimales",variable=decimales,value=3,state=ACTIVE)
menu_arrondi.add_radiobutton(label="4 décimales",variable=decimales,value=4,state=ACTIVE)
menu_arrondi.add_radiobutton(label="5 décimales",variable=decimales,value=5,state=ACTIVE)
menu_arrondi.add_radiobutton(label="6 décimales",variable=decimales,value=6,state=ACTIVE)
menu_arrondi.add_radiobutton(label="7 décimales",variable=decimales,value=7,state=ACTIVE)
menu_arrondi.add_radiobutton(label="8 décimales",variable=decimales,value=8,state=ACTIVE)
menu_arrondi.add_radiobutton(label="9 décimales",variable=decimales,value=9,state=ACTIVE)
decimales.set(3)
menu2.add_cascade(label="Arrondi",menu=menu_arrondi)
menubar.add_cascade(label="Calcul",menu=menu2)

menu3 = Menu(menubar,tearoff=0)
menu3.add_command(label="Aide",command=aide)
menu3.add_command(label="Création de fonction",command=aide_fonctions)
menubar.add_cascade(label="Aide",menu=menu3)

crea_canvas()
crea_cadre()

fenetre.bind("<Control-n>",raccourci_new_file)
fenetre.bind("<Control-o>",raccourci_open_file)
fenetre.bind("<Control-s>",raccourci_save_file)
fenetre.bind("<Control-Shift-s>",raccourci_save_as_file)
fenetre.bind("<Control-Alt-s>",raccourci_save_capture)
fenetre.bind("<Alt-F4>",raccourci_alerte_fermeture)
fenetre.bind("<Key-Delete>",suppr_objet)
fenetre.config(menu=menubar)
fenetre.resizable(width=False,height=False)
fenetre.protocol("WM_DELETE_WINDOW",alerte_fermeture)
fenetre.mainloop()