import os
import subprocess
import sys
import tkinter as tk
from tkinter import ttk

class GraphsTab(ttk.Frame):

    def __init__(
        self,
        parent,
        graph_dir
    ):
        super().__init__(
            parent,
            padding=10
        )

        self.graph_dir = graph_dir
        self.lista = tk.Listbox(
            self
        )
        self.lista.pack(
            fill="both",
            expand=True
        )
        self.lista.bind(
            "<Double-1>",
            lambda event:
            self.abrir_selecionado()
        )
        botoes = ttk.Frame(self)
        botoes.pack(
            fill="x",
            pady=10
        )
        ttk.Button(
            botoes,
            text="Abrir",
            command=self.abrir_selecionado
        ).pack(
            side="left"
        )
        ttk.Button(
            botoes,
            text="Atualizar",
            command=self.atualizar
        ).pack(
            side="left",
            padx=5
        )
        ttk.Button(
            botoes,
            text="Abrir pasta",
            command=self.abrir_pasta
        ).pack(
            side="left"
        )
        self.atualizar()

    def atualizar(self):
        self.lista.delete(
            0,
            tk.END
        )
        arquivos = sorted(
            self.graph_dir.glob("*.png"),
            key=lambda arquivo:
                arquivo.stat().st_mtime,
            reverse=True
        )
        for arquivo in arquivos:
            self.lista.insert(
                tk.END,
                arquivo.name
            )

    def abrir_selecionado(self):
        selecao = self.lista.curselection()
        if not selecao:
            return

        arquivo = (
            self.graph_dir
            / self.lista.get(
                selecao[0]
            )
        )
        self._abrir(arquivo)

    def abrir_pasta(self):
        self._abrir(
            self.graph_dir
        )

    def _abrir(
        self,
        caminho
    ):
        if sys.platform.startswith("win"):
            os.startfile(caminho)

        elif sys.platform == "darwin":
            subprocess.Popen(
                ["open", str(caminho)]
            )
        else:
            subprocess.Popen(
                ["xdg-open", str(caminho)]
            )