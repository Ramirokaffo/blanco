from tkinter import *

from STATIC.ConstantFile import couleur_sous_fenetre, couleur_police_champs
from Service.AnyService import AnyService
from Service.InputCheckService import InputCheckService


class CreditSaleForm(Toplevel):
    avance: str = ""
    refund_date: str = ""
    is_credit: bool = False

    def __init__(self, master, avance_value: str = "", refund_value: str = ""):
        CreditSaleForm.is_credit = avance_value != "" or refund_value != ""
        super().__init__(master)
        self.configure(background=couleur_sous_fenetre)
        self.geometry("500x200+200+200")
        self.transient(self.master.winfo_toplevel())
        self.input_check_service = InputCheckService(self.master)
        main_frame = Frame(self, background=couleur_sous_fenetre)
        main_frame.pack(expand=YES, padx=20, pady=20)
        Label(main_frame, text="Avance", background=couleur_sous_fenetre, width=30, anchor=W).grid(row=2, column=2, sticky=EW, pady=20, padx=5)
        self.avance_entry = Entry(main_frame, width=30, validate="key", validatecommand=(self.input_check_service.check_digit, "%S"))
        self.avance_entry.insert(0, avance_value)
        self.avance_entry.grid(row=2, column=3, sticky=EW, padx=5)

        Label(main_frame, text="Date de remboursement", anchor=W, background=couleur_sous_fenetre).grid(row=3, column=2, pady=20, sticky=EW, padx=5)
        self.refund_entry = Entry(main_frame, fg=couleur_police_champs, validate="key",
                                  validatecommand=(self.input_check_service.check_date, "%S", "%P"))
        for value in refund_value:
            self.refund_entry.insert(END, value)
        self.refund_entry.grid(row=3, column=3, sticky=EW, padx=5)

        Button(main_frame, text="Enregistrer", command=self.save).grid(row=4, column=2, sticky=EW, padx=5)
        Button(main_frame, text="Annuler", command=self.abort).grid(row=4, column=3, sticky=EW, padx=5)
        self.winfo_toplevel().bind("<Return>", lambda x: self.save())
        self.bind("<FocusIn>", self.on_focus_in)
        self.focus_set()
        self.master.wait_window(self)

    def on_focus_in(self, event):
        AnyService.top_level_was_show = True

    def save(self):
        self.is_credit = True
        CreditSaleForm.avance = self.avance_entry.get()
        CreditSaleForm.refund_date = self.refund_entry.get()
        self.destroy()

    def abort(self):
        self.is_credit = False
        self.destroy()

