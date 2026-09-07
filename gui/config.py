import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path

class ConfigFrame(ttk.LabelFrame):

    def __init__(
        self,
        parent,
        on_benchmark
    ):
        super().__init__(
            parent,
            text="Configuração",
            padding=10
        )
        self.on_benchmark = on_benchmark
        self.pasta_var = tk.StringVar()
        self.tipo_var = tk.StringVar(
            value="Extensão"
        )

        self.termo_var = tk.StringVar(
            value=".pdf"
        )
        self.threads_var = tk.StringVar(
            value="1,2,4,8,16,32,64"
        )
        self.tipo_map = {
            "Nome do arquivo": "filename",
            "Extensão": "extension",
            "Texto no arquivo": "text"
        }
        self._criar_widgets()