from tkinter import *


class StandardCalculator:
    def __init__(self, master, bottomBarInstance):
        self.total = 0
        self.current = ""
        self.input_value = True
        self.check_sum = False
        self.oper = ""
        self.result = False
        self.bordure = 5
        self.BottomBarInstance = bottomBarInstance
        self.master = master
        self.couleur_calculatrice = "#FF630B"
        self.frame_calculatrice = Frame(self.master, bg="#0642FF", bd=20, relief=RAISED)
        self.calculatrice_champs = Entry(self.frame_calculatrice, font=("arial", 20, "bold"), bd=20, bg="white",
                                         justify=RIGHT
                                         , relief=SUNKEN, width=24)
        self.calculatrice_champs.grid(row=0, column=0, columnspan=4, pady=1)
        self.calculatrice_champs.insert(0, "0")

        self.numero_standard = "789456123"
        self.liste_bouton_calculatrice = []
        # self.added_value = Calculator()
        i = 0
        for j in range(2, 5):
            for k in range(3):
                self.liste_bouton_calculatrice.append(
                    Button(self.frame_calculatrice, width=5, height=2, font=("arial", 20, "bold")
                           , activebackground="blue", bd=self.bordure, bg="#6B47FF",
                           text=self.numero_standard[i], relief=RAISED))
                self.liste_bouton_calculatrice[i].grid(row=j, column=k, pady=1)
                self.liste_bouton_calculatrice[i]["command"] = lambda x=self.numero_standard[i]: self.nombre_enter(x)
                i += 1

        self.bouton_effacer = Button(self.frame_calculatrice, text=chr(67), width=5, height=2,
                                     font=("arial", 20, "bold")
                                     , bd=self.bordure, bg=self.couleur_calculatrice, command=self.clear)
        self.bouton_effacer.grid(row=1, column=0, pady=1)
        self.bouton_effacer_tout = Button(self.frame_calculatrice, text=chr(67) + chr(69), width=5, height=2,
                                          font=("arial", 20, "bold")
                                          , bd=self.bordure, bg=self.couleur_calculatrice, command=self.clearall)
        self.bouton_effacer_tout.grid(row=1, column=1, pady=1)
        self.bouton_nsq = Button(self.frame_calculatrice, text="000", width=5, height=2, font=("arial", 20, "bold")
                                 , bd=self.bordure, bg=self.couleur_calculatrice,
                                 command=lambda: self.nombre_enter("000"))
        self.bouton_nsq.grid(row=1, column=2, pady=1)
        self.bouton_add = Button(self.frame_calculatrice, text="+", width=5, height=2, font=("arial", 20, "bold")
                                 , bd=self.bordure, bg=self.couleur_calculatrice, command=lambda: self.operateur("add"))
        self.bouton_add.grid(row=1, column=3, pady=1)
        self.bouton_supp = Button(self.frame_calculatrice, text="-", width=5, height=2, font=("arial", 20, "bold")
                                  , bd=self.bordure, bg=self.couleur_calculatrice,
                                  command=lambda: self.operateur("sub"))
        self.bouton_supp.grid(row=2, column=3, pady=1)
        self.bouton_mult = Button(self.frame_calculatrice, text="*", width=5, height=2, font=("arial", 20, "bold")
                                  , bd=self.bordure, bg=self.couleur_calculatrice,
                                  command=lambda: self.operateur("mul"))
        self.bouton_mult.grid(row=3, column=3, pady=1)
        self.bouton_div = Button(self.frame_calculatrice, text=chr(247), width=5, height=2, font=("arial", 20, "bold")
                                 , bd=self.bordure, bg=self.couleur_calculatrice, command=lambda: self.operateur("div"))
        self.bouton_div.grid(row=4, column=3, pady=1)

        self.bouton_zero = Button(self.frame_calculatrice, text="0", width=5, height=2, font=("arial", 20, "bold")
                                  , bd=self.bordure, bg=self.couleur_calculatrice, command=lambda: self.nombre_enter(0))
        self.bouton_zero.grid(row=5, column=0, pady=1)
        self.bouton_point = Button(self.frame_calculatrice, text=".", width=5, height=2, font=("arial", 20, "bold")
                                   , bd=self.bordure, bg=self.couleur_calculatrice,
                                   command=lambda: self.nombre_enter("."))
        self.bouton_point.grid(row=5, column=1, pady=1)
        self.bouton_pm = Button(self.frame_calculatrice, text=chr(177), width=5, height=2, font=("arial", 20, "bold")
                                , bd=self.bordure, bg=self.couleur_calculatrice, command=self.plus_moins)
        self.bouton_pm.grid(row=5, column=2, pady=1)
        self.bouton_egal = Button(self.frame_calculatrice, text="=", width=5, height=2, font=("arial", 20, "bold")
                                  , bd=self.bordure, bg="#FF0948", command=self.somme_of_total)
        self.bouton_egal.grid(row=5, column=3, pady=1)

        self.frame_calculatrice.bind("<B1-Motion>", self.deplace_calculatrice)

    def deplace_calculatrice(self, event):
        """Deplacer la calculatrice"""
        x, y = self.master.winfo_pointerxy()
        self.frame_calculatrice.place_configure(x=x - 30, y=y - 50)

    def nombre_enter(self, num):
        self.result = False
        first_number = self.calculatrice_champs.get()
        secondnumber = str(num)
        if self.input_value:
            self.current = secondnumber
            self.input_value = False
        else:
            if secondnumber == ".":
                if secondnumber in first_number:
                    return
            self.current = first_number + secondnumber
        self.display(self.current)

    def somme_of_total(self):
        self.result = True
        self.current = float(self.current)
        if self.check_sum:
            self.valid_fonction()
        else:
            self.total = float(self.calculatrice_champs.get())

    def valid_fonction(self):
        if self.oper == "add":
            self.total += self.current
        if self.oper == "sub":
            self.total -= self.current
        if self.oper == "mul":
            self.total *= self.current
        if self.oper == "div":
            self.total /= self.current
        self.input_value = True
        self.check_sum = False
        self.display(self.total)

    def operateur(self, oper):
        self.current = float(self.current)
        if self.check_sum:
            self.valid_fonction()
        elif not self.result:
            self.total = self.current
            self.input_value = True
        self.check_sum = True
        self.oper = oper
        self.result = False

    def clear(self):
        self.result = False
        if len(self.current) > 0:
            if len(self.current) == 1:
                self.display(0)
                self.input_value = True
            else:
                self.current = self.current[0:len((self.current)) - 1]
                self.display(self.current)
        else:
            self.display(0)
            self.input_value = True

    def clearall(self):
        self.display(0)
        self.input_value = True

    def plus_moins(self):
        self.result = False
        self.current = -(float(self.calculatrice_champs.get()))
        self.display(self.current)

    def display(self, valeur):
        self.calculatrice_champs.delete(0, END)
        if not str(valeur).endswith(".0"):
            self.calculatrice_champs.insert(0, valeur)
        else:
            try:
                self.calculatrice_champs.insert(0, f"{int(valeur):.0f}")
            except:
                self.calculatrice_champs.insert(0, valeur)

    def affiche_calculatrice_complement(self, event):
        self.frame_calculatrice.place_forget()
        self.BottomBarInstance.boutton_calculatrice.configure(command=self.affiche_calculatrice)

    def affiche_calculatrice(self):
        self.frame_calculatrice.place(x=0, y=50)
        self.BottomBarInstance.boutton_calculatrice.configure(command=lambda: self.affiche_calculatrice_complement(0))
        self.frame_calculatrice.bind("<Double-ButtonRelease-1>", self.affiche_calculatrice_complement)


class PrincipalCalculator:
    def __init__(self, master):
        self.master = master
        self.var_verif_cal = 0
        self.calcul = 0
        self.id_cal = IntVar()
        self.frame_calculatrice2 = Frame(self.master, bg="#0642FF", bd=20, relief=RAISED)
        self.bg_cal2 = "#FF0948"
        self.bordure = 5
        self.with_cal2 = 6
        self.height_cal2 = 1
        self.relief_bouton = SUNKEN
        self.coul_chiff2 = "#1016FF"
        self.fg_bout123 = "#ffffff"
        self.variable_control_last_result = StringVar()
        self.dico_ancien_resultat = {}
        self.dico_ancien_expression = {}
        self.control_delete1 = IntVar(value=0)
        self.control_import = IntVar()
        self.control_import.set(0)
        self.ans_verif = self.master.register(self.verif_ans_entry)
        self.champs_de_saisie_cal2 = Entry(self.frame_calculatrice2, font=("arial", 20, "bold"), bd=20, bg="white",
                                           justify=RIGHT,
                                           relief=SUNKEN, width=37, name="stop", validate="key",
                                           validatecommand=(self.ans_verif, "%S",
                                                            "%i", "%d"))
        self.champs_de_result_cal2 = Entry(self.frame_calculatrice2, font=("arial", 20, "bold"), bd=14, bg="white",
                                           justify=LEFT,
                                           relief=SUNKEN, width=21)
        self.champs_de_saisie_cal2.insert(0, "0")
        self.champs_de_result_cal2.insert(0, "0")
        self.champs_de_result_cal2.config(state=DISABLED)

        self.champs_de_saisie_cal2.grid(row=0, column=0, columnspan=5)
        self.champs_de_result_cal2.grid(row=1, column=0, columnspan=3, sticky=EW)

        self.bout2calparenthese1 = Button(self.frame_calculatrice2, text="(", width=self.with_cal2,
                                          height=self.height_cal2,
                                          font=("arial", 20, "bold"),
                                          bd=self.bordure, bg=self.bg_cal2,
                                          command=lambda: self.remplir_calculator2("("),
                                          relief=self.relief_bouton)
        self.bout2calparenthese2 = Button(self.frame_calculatrice2, text=")", width=self.with_cal2,
                                          height=self.height_cal2,
                                          font=("arial", 20, "bold"),
                                          bd=self.bordure, bg=self.bg_cal2,
                                          command=lambda: self.remplir_calculator2(")"),
                                          relief=self.relief_bouton)
        self.bout2calexp = Button(self.frame_calculatrice2, text=f"{chr(215)}10^", width=self.with_cal2,
                                  height=self.height_cal2,
                                  font=("arial", 20, "bold"),
                                  bd=self.bordure, bg=self.bg_cal2,
                                  command=lambda: self.remplir_calculator2(f"{chr(215)}10^"),
                                  relief=self.relief_bouton)
        self.bout2calremplirfocus = Button(self.frame_calculatrice2, text="Export", width=self.with_cal2,
                                           height=self.height_cal2,
                                           font=("arial", 20, "bold"),
                                           bd=self.bordure, bg=self.bg_cal2, command=self.remplir_bouton_focus,
                                           relief=self.relief_bouton)
        self.bout2calimport = Button(self.frame_calculatrice2, text="Import", width=self.with_cal2,
                                     height=self.height_cal2,
                                     font=("arial", 20, "bold"),
                                     bd=self.bordure, bg=self.bg_cal2, command=self.import_result,
                                     relief=self.relief_bouton)
        self.bout2cal1 = Button(self.frame_calculatrice2, text="1", width=self.with_cal2, height=self.height_cal2,
                                font=("arial", 20, "bold"),
                                bd=self.bordure, bg=self.coul_chiff2, command=lambda: self.remplir_calculator2("1"),
                                relief=self.relief_bouton,
                                fg=self.fg_bout123)
        self.bout2cal2 = Button(self.frame_calculatrice2, text="2", width=self.with_cal2, height=self.height_cal2,
                                font=("arial", 20, "bold"),
                                bd=self.bordure, bg=self.coul_chiff2, command=lambda: self.remplir_calculator2("2"),
                                relief=self.relief_bouton,
                                fg=self.fg_bout123)
        self.bout2cal3 = Button(self.frame_calculatrice2, text="3", width=self.with_cal2, height=self.height_cal2,
                                font=("arial", 20, "bold"),
                                bd=self.bordure, bg=self.coul_chiff2, command=lambda: self.remplir_calculator2("3"),
                                relief=self.relief_bouton,
                                fg=self.fg_bout123)
        self.bout2cal4 = Button(self.frame_calculatrice2, text="4", width=self.with_cal2, height=self.height_cal2,
                                font=("arial", 20, "bold"),
                                bd=self.bordure, bg=self.coul_chiff2, command=lambda: self.remplir_calculator2("4"),
                                relief=self.relief_bouton,
                                fg=self.fg_bout123)
        self.bout2cal5 = Button(self.frame_calculatrice2, text="5", width=self.with_cal2, height=self.height_cal2,
                                font=("arial", 20, "bold"),
                                bd=self.bordure, bg=self.coul_chiff2, command=lambda: self.remplir_calculator2("5"),
                                relief=self.relief_bouton,
                                fg=self.fg_bout123)
        self.bout2cal6 = Button(self.frame_calculatrice2, text="6", width=self.with_cal2, height=self.height_cal2,
                                font=("arial", 20, "bold"),
                                bd=self.bordure, bg=self.coul_chiff2, command=lambda: self.remplir_calculator2("6"),
                                relief=self.relief_bouton,
                                fg=self.fg_bout123)
        self.bout2cal7 = Button(self.frame_calculatrice2, text="7", width=self.with_cal2, height=self.height_cal2,
                                font=("arial", 20, "bold"),
                                bd=self.bordure, bg=self.coul_chiff2, command=lambda: self.remplir_calculator2("7"),
                                relief=self.relief_bouton,
                                fg=self.fg_bout123)
        self.bout2cal8 = Button(self.frame_calculatrice2, text="8", width=self.with_cal2, height=self.height_cal2,
                                font=("arial", 20, "bold"),
                                bd=self.bordure, bg=self.coul_chiff2, command=lambda: self.remplir_calculator2("8"),
                                relief=self.relief_bouton,
                                fg=self.fg_bout123)
        self.bout2cal9 = Button(self.frame_calculatrice2, text="9", width=self.with_cal2, height=self.height_cal2,
                                font=("arial", 20, "bold"),
                                bd=self.bordure, bg=self.coul_chiff2, command=lambda: self.remplir_calculator2("9"),
                                relief=self.relief_bouton,
                                fg=self.fg_bout123)
        self.bout2cal0 = Button(self.frame_calculatrice2, text="0", width=self.with_cal2, height=self.height_cal2,
                                font=("arial", 20, "bold"),
                                bd=self.bordure, bg=self.bg_cal2, command=lambda: self.remplir_calculator2("0"),
                                relief=self.relief_bouton)
        self.bout2calcleanall = Button(self.frame_calculatrice2, text="CA", width=self.with_cal2,
                                       height=self.height_cal2,
                                       font=("arial", 20, "bold"),
                                       bd=self.bordure, bg=self.bg_cal2, command=self.cleaallvaluecal2,
                                       relief=self.relief_bouton)
        self.bout2calplus = Button(self.frame_calculatrice2, text="+", width=self.with_cal2, height=self.height_cal2,
                                   font=("arial", 20, "bold"),
                                   bd=self.bordure, bg=self.bg_cal2, command=lambda: self.remplir_calculator2("+"),
                                   relief=self.relief_bouton)
        self.bout2caldel = Button(self.frame_calculatrice2, text="DEL", width=self.with_cal2, height=self.height_cal2,
                                  font=("arial", 20, "bold"),
                                  bd=self.bordure, bg=self.bg_cal2, command=self.clean1valuecal2,
                                  relief=self.relief_bouton)
        self.bout2calmoins = Button(self.frame_calculatrice2, text="-", width=self.with_cal2, height=self.height_cal2,
                                    font=("arial", 20, "bold"),
                                    bd=self.bordure, bg=self.bg_cal2, command=lambda: self.remplir_calculator2("-"),
                                    relief=self.relief_bouton)
        self.bout2caldivision = Button(self.frame_calculatrice2, text=f"{chr(247)}", width=self.with_cal2,
                                       height=self.height_cal2,
                                       font=("arial", 20, "bold"),
                                       bd=self.bordure, bg=self.bg_cal2,
                                       command=lambda: self.remplir_calculator2(str(chr(247))),
                                       relief=self.relief_bouton)
        self.bout2calmultiplication = Button(self.frame_calculatrice2, text=f"{chr(215)}", width=self.with_cal2,
                                             height=self.height_cal2,
                                             font=("arial", 20, "bold"),
                                             bd=self.bordure, bg=self.bg_cal2,
                                             command=lambda: self.remplir_calculator2(f"{chr(215)}"),
                                             relief=self.relief_bouton)
        self.bout2calegale = Button(self.frame_calculatrice2, text="=", width=self.with_cal2, height=self.height_cal2,
                                    font=("arial", 20, "bold"),
                                    bd=self.bordure, bg="#1016FF", command=lambda: self.eval_cal2(0),
                                    relief=self.relief_bouton,
                                    fg=self.fg_bout123)
        self.bout2calpoint = Button(self.frame_calculatrice2, text=".", width=self.with_cal2, height=self.height_cal2,
                                    font=("arial", 20, "bold"),
                                    bd=self.bordure, bg=self.bg_cal2, command=lambda: self.remplir_calculator2("."),
                                    relief=self.relief_bouton)
        self.bout2calanser = Button(self.frame_calculatrice2, text="Ans", width=self.with_cal2, height=self.height_cal2,
                                    font=("arial", 20, "bold"),
                                    bd=self.bordure, bg=self.bg_cal2, command=lambda: self.remplir_calculator2("Ans"),
                                    relief=self.relief_bouton)
        self.bout2cal3zero = Button(self.frame_calculatrice2, text="000", width=self.with_cal2, height=self.height_cal2,
                                    font=("arial", 20, "bold"),
                                    bd=self.bordure, bg=self.bg_cal2, command=lambda: self.remplir_calculator2("000"),
                                    relief=self.relief_bouton)
        self.bout2cal2prev = Button(self.frame_calculatrice2, text=f"{chr(9668)}", width=self.with_cal2,
                                    height=self.height_cal2,
                                    font=("arial", 20, "bold"),
                                    bd=self.bordure, bg="#FFE804", command=self.historique_inf,
                                    relief=self.relief_bouton)
        self.bout2cal2next = Button(self.frame_calculatrice2, text=f"{chr(9658)}", width=self.with_cal2,
                                    height=self.height_cal2,
                                    font=("arial", 20, "bold"),
                                    bd=self.bordure, bg="#FFE804", command=self.historique_supp,
                                    relief=self.relief_bouton)

        self.bout2calparenthese1.grid(row=2, column=0)
        self.bout2calparenthese2.grid(row=2, column=1)
        self.bout2calimport.grid(row=2, column=3)
        self.bout2calremplirfocus.grid(row=2, column=4)
        self.bout2calexp.grid(row=2, column=2)
        self.bout2cal7.grid(row=3, column=0)
        self.bout2cal4.grid(row=4, column=0)
        self.bout2cal1.grid(row=5, column=0)
        self.bout2cal0.grid(row=6, column=0)
        self.bout2cal8.grid(row=3, column=1)
        self.bout2cal5.grid(row=4, column=1)
        self.bout2cal2.grid(row=5, column=1)
        self.bout2calpoint.grid(row=6, column=1)
        self.bout2cal9.grid(row=3, column=2)
        self.bout2cal6.grid(row=4, column=2)
        self.bout2cal3.grid(row=5, column=2)
        self.bout2cal3zero.grid(row=6, column=2)
        self.bout2caldel.grid(row=3, column=3)
        self.bout2calmultiplication.grid(row=4, column=3)
        self.bout2calplus.grid(row=5, column=3)
        self.bout2calanser.grid(row=6, column=3)
        self.bout2calcleanall.grid(row=3, column=4)
        self.bout2caldivision.grid(row=4, column=4)
        self.bout2calmoins.grid(row=5, column=4)
        self.bout2calegale.grid(row=6, column=4)
        self.bout2cal2prev.grid(row=1, column=3)
        self.bout2cal2next.grid(row=1, column=4)

        self.champs_de_saisie_cal2.bind("<Enter>", self.control_focus_calculator)
        self.champs_de_saisie_cal2.bind("<KeyRelease>", self.result_auto_calco2)

        # self.bout2calimport.bind("<Enter>", self.details_import_calculatrice)
        # self.bout2calremplirfocus.bind("<Enter>", self.details_export_calculatrice)
        self.frame_calculatrice2.bind("<B1-Motion>", self.deplace_calculatrice2)

    # def details_import_calculatrice(self, event):
    #     info_bas_vente("Ciquez dessus pour importer les données dans le champs de saisie qui a le curseur")
    #
    # def details_export_calculatrice(self, event):
    #     info_bas_vente("Ciquez dessus pour exporter les données vers le champs de saisie qui a le curseur")

    def affiche_calculator2complement(self, event):
        self.frame_calculatrice2.place_forget()
        self.frame_calculatrice2.destroy()

    def affiche_calculator2(self):
        """Afficher la calculatrice 2 (normal) a l'ecran"""
        self.frame_calculatrice2.place(x=400, y=100)
        self.frame_calculatrice2.bind("<Double-ButtonRelease-1>", self.affiche_calculator2complement)

    def deplace_calculatrice2(self, event):
        """Deplacer la calculatrice"""
        x, y = self.master.winfo_pointerxy()
        self.frame_calculatrice2.place_configure(x=x - 30, y=y - 50)

    def remplir_calculator2(self, valeur):
        """Remplir le champs de saisis de la calculatrice 2 en fonction de la touche enfoncee"""
        self.control_import.set(1)
        self.master.after(5, self.control_import.set, 0)
        if not self.var_verif_cal:
            val_courante = self.champs_de_saisie_cal2.get()
            self.champs_de_saisie_cal2.delete(0, END)
            if val_courante == "0" and valeur != ".":
                self.champs_de_saisie_cal2.delete(0, END)
            self.champs_de_saisie_cal2.insert(INSERT, valeur)
            self.var_verif_cal = 1
        else:
            val_courante = self.champs_de_saisie_cal2.get()
            if val_courante == "0" and valeur != ".":
                self.champs_de_saisie_cal2.delete(0, END)
            self.champs_de_saisie_cal2.insert(INSERT, valeur)
        self.result_auto_calco2(0)

    def verif_ans_entry(self, quoi, ou, pourquoi):
        """Verifier si c'est ANS qui est en train d'etre supprimer pour supprimer totalement"""
        if pourquoi == "1" and quoi == "A" or quoi == "a" and pourquoi == "1":
            self.master.after(5, self.champs_de_saisie_cal2.insert, INSERT, "Ans")
            return False
        if pourquoi == "1" and quoi not in [str(f) for f in range(10)] + ["A", "a", ".", "(", ")", "000",
                                                                          f"{chr(215)}10^",
                                                                          str(chr(247)), str(chr(215)), "+", "-", "Ans"] \
                and self.control_import.get() == 0:
            if self.control_delete1.get() == 0:
                return False
            else:
                return True
        if quoi == "s" and pourquoi == "0":
            self.master.after(5, self.champs_de_saisie_cal2.delete, int(ou) - 2, int(ou))
        elif quoi == "n" and pourquoi == "0":
            self.master.after(5, self.champs_de_saisie_cal2.delete, int(ou) - 1, int(ou) + 1)
        elif quoi == "A" and pourquoi == "0":
            self.master.after(5, self.champs_de_saisie_cal2.delete, int(ou), int(ou) + 2)
        return True

    def clean1valuecal2(self):
        # return
        """Effacer la dernere valeur saisie dans le champs de la calculatrice 2 (normale)"""
        val_courante = self.champs_de_saisie_cal2.get()
        # val_courante = self.champs_de_saisie_cal2.
        if val_courante.endswith("Ans"):
            self.champs_de_saisie_cal2.delete((len(val_courante) - 3), len(val_courante))
        # elif val_courante.endswith("Ans"):
        #     print("d'abord ici")
        #     self.champs_de_saisie_cal2.delete((len(val_courante) - 1), len(val_courante) + 1)
        else:
            self.champs_de_saisie_cal2.selection_range(0, INSERT)
            selection = self.champs_de_saisie_cal2.selection_get()
            self.champs_de_saisie_cal2.delete(0, len(selection))
            self.control_delete1.set(1)
            self.champs_de_saisie_cal2.insert(0, selection[0:-1])
            self.control_delete1.set(0)

    def cleaallvaluecal2(self):
        """Tous effacer dans le champs de saisie de la calculatrice 2 (Normal)"""
        self.champs_de_saisie_cal2.delete(0, END)

    def eval_cal2(self, event):
        """Evaluer l'expression saisie et afficher le resultat dans la calculatrice2(Normal)"""
        self.control_delete1.set(1)
        try:
            val_obtenue = self.champs_de_saisie_cal2.get()
            val_courante = val_obtenue
            if ("(" in val_courante) and (not (")" in val_courante)):
                self.champs_de_saisie_cal2.delete(0, END)
                self.champs_de_saisie_cal2.insert(0, f"{val_courante})")
                self.var_verif_cal = 0
                self.control_delete1.set(0)
                return
            if (")" in val_courante) and (not ("(" in val_courante)):
                self.champs_de_saisie_cal2.delete(0, END)
                self.champs_de_saisie_cal2.insert(0, f"({val_courante}")
                self.var_verif_cal = 0
                self.control_delete1.set(0)
                return
            if " " in val_courante:
                val_courante = val_courante.replace(" ", "")
            if (not "0." in val_courante) and (f"{chr(247)}0" in val_courante) and (val_courante.endswith("0")):
                self.champs_de_saisie_cal2.delete(0, END)
                self.champs_de_saisie_cal2.insert(0, "ZeroDivisionError")
                self.var_verif_cal = 0
                self.control_delete1.set(0)
                return
            if "+0" in val_courante:
                while "+0" in val_courante:
                    val_courante = val_courante.replace("+0", "+")
            if "-0" in val_courante:
                while "+0" in val_courante:
                    val_courante = val_courante.replace("+0", "+")
            if f"{str(chr(247))}0" in val_courante:
                while f"{str(chr(247))}0" in val_courante:
                    val_courante = val_courante.replace(f"{str(chr(247))}0", str(chr(247)))
            if val_courante.endswith("+"):
                while val_courante.endswith("+"):
                    val_courante = val_courante.removesuffix("+")
            if val_courante.endswith("-"):
                while val_courante.endswith("-"):
                    val_courante = val_courante.removesuffix("-")
            if val_courante.endswith(f"{chr(215)}"):
                self.champs_de_saisie_cal2.delete(0, END)
                self.champs_de_saisie_cal2.insert(0, f"{val_courante}{chr(8592)}Error")
                self.control_delete1.set(0)
                return
            if f"{chr(215)}0" in val_courante:
                while f"{chr(215)}0" in val_courante:
                    val_courante = val_courante.replace(f"{chr(215)}0", f"{chr(215)}")
            if val_courante.endswith(str(chr(247))):
                self.champs_de_saisie_cal2.delete(0, END)
                self.champs_de_saisie_cal2.insert(0, f"{val_courante}{chr(8592)}Error")
                self.var_verif_cal = 0
                self.control_delete1.set(0)
                return
            if val_courante.startswith(str(chr(247))):
                self.champs_de_saisie_cal2.delete(0, END)
                self.champs_de_saisie_cal2.insert(0, f"Error{chr(8594)}{val_courante}")
                self.var_verif_cal = 0
                self.control_delete1.set(0)
                return
            if val_courante.startswith(f"{chr(215)}"):
                self.champs_de_saisie_cal2.delete(0, END)
                self.champs_de_saisie_cal2.insert(0, f"Error{chr(8594)}{val_courante}")
                self.var_verif_cal = 0
                self.control_delete1.set(0)
                return
            for i in range(10):
                if f"{i}Ans" in val_courante:
                    val_courante = val_courante.replace(f"{i}Ans", f"{i}*Ans")
            for i in range(10):
                if f"Ans{i}" in val_courante:
                    val_courante = val_courante.replace(f"Ans{i}", f"Ans*{i}")
                if f"{i}(" in val_courante:
                    val_courante = val_courante.replace(f"{i}(", f"{i}*(")
                if f"){i}" in val_courante:
                    val_courante = val_courante.replace(f"){i}", f")*{i}")
            val_courante = val_courante.replace(str(chr(247)), "/")
            val_courante = val_courante.replace(f"{chr(215)}", "*")
            val_courante = val_courante.replace("^", "**")
            val_courante = val_courante.replace(")(", ")*(")
            val_courante = val_courante.replace(str(chr(178)), "**2")
            val_courante = val_courante.replace("Ans",
                                                f"{self.variable_control_last_result.get()}")
            if "(" in val_courante:
                control_boucle = 0
                while "(" and ")" in val_courante:
                    i = 0
                    for v in val_courante:
                        if v == "(":
                            i = val_courante.index(v)
                        if v == ")":
                            try:
                                val_courante = val_courante.replace(val_courante[i:val_courante.index(v) + 1],
                                                                    str(eval(
                                                                        val_courante[i:val_courante.index(v) + 1])))
                            except SyntaxError:
                                try:
                                    val_courante = val_courante.replace(val_courante[i:val_courante.index(v) + 1],
                                                                        str(eval(val_courante[
                                                                                 i:val_courante.index(v) + 1] + ")")))
                                except SyntaxError:
                                    val_courante = val_courante.replace(val_courante[i:val_courante.index(v) + 1],
                                                                        str(eval("(" + val_courante[
                                                                                       i:val_courante.index(v) + 1])))
                    if control_boucle > 100000:
                        self.champs_de_saisie_cal2.delete(0, END)
                        self.champs_de_saisie_cal2.insert(0, "Math error")
                        self.var_verif_cal = 0
                        self.control_delete1.set(0)
                        return
                    control_boucle += 100
            resultat = eval(val_courante)
            self.champs_de_result_cal2.config(state=NORMAL)
            self.champs_de_result_cal2.delete(0, END)
            self.variable_control_last_result.set(str(resultat))
            if not str(resultat).endswith(".0") and ("." in str(resultat)):
                self.champs_de_result_cal2.insert(0, f"{resultat:,}")
            else:
                try:
                    resultat = int(f"{int(resultat):.0f}")
                    self.champs_de_result_cal2.insert(0, f"{resultat:,}")
                except:
                    self.champs_de_result_cal2.insert(0, resultat)
            self.dico_ancien_resultat[self.calcul] = resultat
            self.dico_ancien_expression[self.calcul] = val_obtenue
            self.id_cal.set(self.calcul)
            self.calcul += 1
            self.var_verif_cal = 0
            self.champs_de_result_cal2.config(state=DISABLED)
            self.control_delete1.set(0)
        except:
            self.champs_de_result_cal2.config(state=NORMAL)
            self.champs_de_saisie_cal2.delete(0, END)
            self.champs_de_result_cal2.config(state=DISABLED)
            self.champs_de_saisie_cal2.insert(0, "Syntax Error")
            self.var_verif_cal = 0
            self.control_delete1.set(0)
            return

    def historique_supp(self):
        """Boutton d'avancement sur les resultats suivants sur la calculatrice 2"""
        try:
            self.champs_de_result_cal2.config(state=NORMAL)
            self.champs_de_saisie_cal2.delete(0, END)
            self.champs_de_result_cal2.delete(0, END)
            if int(self.dico_ancien_resultat[self.id_cal.get() + 1]) == int(
                    self.dico_ancien_resultat[self.id_cal.get()]):
                self.id_cal.set(self.id_cal.get() + 1)
            if (not str(self.dico_ancien_resultat[self.id_cal.get() + 1]).endswith(".0")) and (
                    "." in str(self.dico_ancien_resultat[self.id_cal.get() + 1])):
                self.champs_de_result_cal2.insert(0, self.dico_ancien_resultat[self.id_cal.get() + 1])
            else:
                try:
                    self.champs_de_result_cal2.insert(0,
                                                      f'{int(f"{int(self.dico_ancien_resultat[self.id_cal.get() + 1]):.0f}"):,}')
                except:
                    self.champs_de_result_cal2.insert(0, f"{int(self.dico_ancien_resultat[self.id_cal.get() + 1]):,}")
            self.control_delete1.set(1)
            self.champs_de_saisie_cal2.insert(0, self.dico_ancien_expression[self.id_cal.get() + 1])
            self.control_delete1.set(0)
            self.id_cal.set(self.id_cal.get() + 1)
            self.champs_de_result_cal2.config(state=DISABLED)
        except:
            try:
                self.champs_de_result_cal2.config(state=NORMAL)
                self.champs_de_saisie_cal2.delete(0, END)
                self.champs_de_result_cal2.delete(0, END)
                if not str(self.dico_ancien_resultat[self.id_cal.get() - 1]).endswith(".0") and (
                        "." in str(self.dico_ancien_resultat[self.id_cal.get() + 1])):
                    self.champs_de_result_cal2.insert(0, f"{int(self.dico_ancien_resultat[self.id_cal.get() - 1]):,}")
                else:
                    try:
                        self.champs_de_result_cal2.insert(0,
                                                          f'{int(f"{int(self.dico_ancien_resultat[self.id_cal.get() - 1]):.0f}"):,}')
                    except:
                        self.champs_de_result_cal2.insert(0,
                                                          f"{int(self.dico_ancien_resultat[self.id_cal.get() - 1]):,}")
                self.control_delete1.set(1)
                self.champs_de_saisie_cal2.insert(0, self.dico_ancien_expression[self.id_cal.get() - 1])
                self.control_delete1.set(0)
                self.champs_de_result_cal2.config(state=DISABLED)
            except:
                self.champs_de_result_cal2.config(state=NORMAL)
                self.champs_de_result_cal2.insert(0, "0")
                self.champs_de_saisie_cal2.insert(0, "0")
                self.champs_de_result_cal2.config(state=DISABLED)

    def result_auto_calco2(self, event):
        """Essayer a chaque fois d'evaluer le resultat et afficher"""
        try:
            val_courante = self.champs_de_saisie_cal2.get()
            val_courante = val_courante.replace(str(chr(247)), "/")
            val_courante = val_courante.replace(f"{chr(215)}", "*")
            val_courante = val_courante.replace("^", "**")
            val_courante = val_courante.replace(")(", ")*(")
            val_courante = val_courante.replace(str(chr(178)), "**2")
            val_courante = val_courante.replace("Ans", f"{self.variable_control_last_result.get()}")
            result = eval(val_courante)
            self.champs_de_result_cal2.config(state=NORMAL)
            self.champs_de_result_cal2.delete(0, END)
            self.champs_de_result_cal2.insert(0, result)
            self.champs_de_result_cal2.config(state=DISABLED)
        except:
            self.champs_de_result_cal2.config(state=NORMAL)
            self.champs_de_result_cal2.delete(0, END)
            self.champs_de_result_cal2.insert(0, "...")
            self.champs_de_result_cal2.config(state=DISABLED)

    def historique_inf(self):
        """Boutton de retour arriere sur les resultats precedentes sur la calculatrice 2"""
        try:
            self.champs_de_result_cal2.config(state=NORMAL)
            self.champs_de_saisie_cal2.delete(0, END)
            self.champs_de_result_cal2.delete(0, END)
            if int(self.dico_ancien_resultat[self.id_cal.get() - 1]) == int(self.dico_ancien_resultat[
                                                                                self.id_cal.get()]):
                self.id_cal.set(self.id_cal.get() - 1)
            if not str(self.dico_ancien_resultat[self.id_cal.get() - 1]).endswith(".0") and (
                    "." in str(self.dico_ancien_resultat[self.id_cal.get() - 1])):
                self.champs_de_result_cal2.insert(0, f"{int(self.dico_ancien_resultat[self.id_cal.get() - 1]):,}")
            else:
                try:
                    self.champs_de_result_cal2.insert(0,
                                                      f"{int(f'{int(self.dico_ancien_resultat[self.id_cal.get() - 1]):.0f}'):,}")
                except:
                    self.control_delete1.set(1)
                    self.champs_de_result_cal2.insert(0, f"{int(self.dico_ancien_resultat[self.id_cal.get() - 1]):,}")
            self.control_delete1.set(1)
            self.champs_de_saisie_cal2.insert(0, self.dico_ancien_expression[self.id_cal.get() - 1])
            self.control_delete1.set(0)
            self.id_cal.set(self.id_cal.get() - 1)
            self.champs_de_result_cal2.config(state=DISABLED)
        except:
            try:
                self.champs_de_result_cal2.config(state=NORMAL)
                self.champs_de_saisie_cal2.delete(0, END)
                self.champs_de_result_cal2.delete(0, END)
                if not str(self.dico_ancien_resultat[self.id_cal.get() - 1]).endswith(".0"):
                    self.champs_de_result_cal2.insert(0, self.dico_ancien_resultat[self.id_cal.get() - 1])
                else:
                    try:
                        self.champs_de_result_cal2.insert(0,
                                                          f"{int(self.dico_ancien_resultat[self.id_cal.get() - 1]):.0f}")
                    except:
                        self.champs_de_result_cal2.insert(0, self.dico_ancien_resultat[self.id_cal.get() - 1])
                self.control_delete1.set(1)
                self.champs_de_saisie_cal2.insert(0, self.dico_ancien_expression[self.id_cal.get() - 1])
                self.control_delete1.set(0)
                self.champs_de_result_cal2.config(state=DISABLED)
            except:
                self.champs_de_result_cal2.config(state=NORMAL)
                self.champs_de_result_cal2.insert(0, "0")
                self.champs_de_saisie_cal2.insert(0, "0")
                self.champs_de_result_cal2.config(state=DISABLED)

    def control_focus_calculator(self, event):
        self.control_delete1.set(1)
        valeur_courante = self.champs_de_saisie_cal2.get()
        if valeur_courante in ("ZeroDivisionError", "Math error", "Syntax Error"):
            self.champs_de_saisie_cal2.delete(0, END)
        if f"{chr(8592)}Error" in valeur_courante:
            self.champs_de_saisie_cal2.delete(0, END)
            self.champs_de_saisie_cal2.insert(0, valeur_courante.replace(f"{chr(8592)}Error", ""))
        if f"Error{chr(8594)}" in valeur_courante:
            self.champs_de_saisie_cal2.delete(0, END)
            self.champs_de_saisie_cal2.insert(0, valeur_courante.replace(f"Error{chr(8594)}", ""))
        self.var_verif_cal = 1
        self.control_delete1.set(0)

    def remplir_bouton_focus(self):
        """Exporter les donnees dans un champs qui a le focus a l'ecran"""
        val_remplir = self.champs_de_result_cal2.get()
        try:
            val_remplir = val_remplir.replace(",", "")
            wid_focus = self.master.focus_get()
            if not str(wid_focus).endswith(".stop"):
                wid_focus.insert(INSERT, val_remplir)
        except:
            pass

    def import_result(self):
        """Importer les donnees du champs qui a le focus a l'ecran"""
        wid_focus = self.master.focus_get()
        try:
            try:
                valeur_import = wid_focus.get()
            except:
                valeur_import = wid_focus.get("0.0", END)
            if not str(wid_focus).endswith(".stop"):
                try:
                    print(valeur_import)
                    a = float(valeur_import)
                    self.remplir_calculator2(valeur_import)
                except:
                    print("error")
                    pass
        except:
            pass
