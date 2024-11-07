import tkinter as tk
import customtkinter as ctk


class CustomPopUp(ctk.CTkToplevel):
    def __init__(self, master, title="Message", message=""):
        super().__init__(master)
        self.title(title)
        self.geometry("300x150")
        self.resizable(False, False)

        label = ctk.CTkLabel(self, text=message)
        label.pack(pady=20)

        button = ctk.CTkButton(self, text="OK", command=self.destroy)
        button.pack(pady=10)


class ConsultationWindow(ctk.CTkToplevel):
    def __init__(self, master, title, query_function):
        super().__init__(master)
        self.geometry("600x200")
        self.title(title)

        self.label = ctk.CTkLabel(
            self, text=f"Digite o ID para {title.lower()}:")
        self.label.pack(padx=20, pady=10)

        self.entry = ctk.CTkEntry(self, width=200)
        self.entry.pack(padx=20, pady=10)

        self.button = ctk.CTkButton(
            self, text="Consultar", command=query_function)
        self.button.pack(padx=20, pady=15)

        self.result_label = ctk.CTkLabel(self, text="")
        self.result_label.pack(padx=20, pady=10)

    def display_result(self, result):
        self.result_label.configure(text=result)
