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

    def _criar_widgets(self):
        self.columnconfigure(
            1,
            weight=1
        )
        ttk.Label(
            self,
            text="Pasta:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=5
        )
        ttk.Entry(
            self,
            textvariable=self.pasta_var
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            pady=5
        )
        ttk.Button(
            self,
            text="Procurar...",
            command=self._selecionar_pasta
        ).grid(
            row=0,
            column=2,
            padx=5
        )
        ttk.Label(
            self,
            text="Tipo:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=5
        )
        ttk.Combobox(
            self,
            textvariable=self.tipo_var,
            values=list(
                self.tipo_map.keys()
            ),
            state="readonly"
        ).grid(
            row=1,
            column=1,
            sticky="ew",
            pady=5
        )
        ttk.Label(
            self,
            text="Termo:"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=5
        )
        ttk.Entry(
            self,
            textvariable=self.termo_var
        ).grid(
            row=2,
            column=1,
            sticky="ew",
            pady=5
        )
        ttk.Label(
            self,
            text="Threads:"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=5
        )
        ttk.Entry(
            self,
            textvariable=self.threads_var
        ).grid(
            row=3,
            column=1,
            sticky="ew",
            pady=5
        )
        ttk.Button(
            self,
            text="Executar Benchmark",
            command=self._executar
        ).grid(
            row=4,
            column=0,
            columnspan=3,
            pady=10
        )

    def _selecionar_pasta(self):
        pasta = filedialog.askdirectory()

        if pasta:
            self.pasta_var.set(pasta)

    def _executar(self):
        try:
            config = self._obter_config()
            self.on_benchmark(config)

        except ValueError as erro:
            messagebox.showerror(
                "Erro",
                str(erro)
            )

    def _obter_config(self):
        pasta = Path(
            self.pasta_var.get().strip()
        )
        if not pasta.exists():
            raise ValueError(
                "Selecione uma pasta válida."
            )
        termo = (
            self.termo_var.get().strip()
        )
        if not termo:
            raise ValueError(
                "Informe um termo."
            )
        try:
            threads = [
                int(valor.strip())
                for valor
                in self.threads_var.get().split(",")
            ]
        except ValueError:
            raise ValueError(
                "Threads devem ser números "
                "separados por vírgula."
            )

        return {
            "pasta": str(pasta),
            "tipo_busca":
                self.tipo_map[
                    self.tipo_var.get()
                ],
            "termo_busca": termo,
            "threads": threads
        }
    