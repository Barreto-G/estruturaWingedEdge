import tkinter as tk
import customtkinter as ctk
import transformations_3d as transf


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


class TransformationWindow(ctk.CTkToplevel):
    def __init__(self, master, mesh):
        super().__init__(master)
        self.mesh = mesh
        self.transformations = []
        self.geometry("600x300")
        self.title('Janela de Transformação')

        self.label = ctk.CTkLabel(self, text='Lista de transformações')
        self.label.pack(padx=20, pady=10)

        self.textbox = ctk.CTkTextbox(self, width=350, height=150, state='disabled')
        self.textbox.pack(pady=(5, 10))

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=(10, 0))

        self.add_button = ctk.CTkButton(self.button_frame, text="Adicionar", command=self.adicionar)
        self.add_button.grid(row=0, column=0, padx=10)

        self.apply_button = ctk.CTkButton(self.button_frame, text="Aplicar", command=self.aplicar)
        self.apply_button.grid(row=0, column=1, padx=10)

        self.cancel_button = ctk.CTkButton(self.button_frame, text="Cancelar", command=self.cancelar)
        self.cancel_button.grid(row=0, column=2, padx=10)

    def adicionar(self):
        SelectTransformation(self)

    def aplicar(self):
        pass

    def cancelar(self):
        self.destroy()

    def atualizar_lista(self):
        pass


class SelectTransformation(ctk.CTkToplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.transformations = ['Translação', 'Escala', 'Cisalhamento', 'Rotação', 'Reflexão']

        self.title("Selecionar Transformação")
        self.geometry("400x300")

        # Label
        self.label = ctk.CTkLabel(self, text="Selecione a transformação desejada")
        self.label.pack(pady=(10, 5))

        # Listbox para seleção de objetos
        self.lista = ctk.CTkComboBox(self, values=self.transformations)
        self.lista.pack(pady=(5, 10))

        # Botão Continuar
        self.continuar_button = ctk.CTkButton(self, text="Continuar", command=self.continuar)
        self.continuar_button.pack(pady=10)

    def continuar(self):
        opcao_selecionada = self.lista.get()
        print(f"Opção selecionada: {opcao_selecionada}")

        if opcao_selecionada == "Translação":
            pass
        elif opcao_selecionada == "Escala":
            pass
        elif opcao_selecionada == "Cisalhamento":
            pass
        elif opcao_selecionada == "Rotação":
            pass
        elif opcao_selecionada == "Reflexão":
            pass



