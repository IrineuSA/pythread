import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

import os
import subprocess
import sys
import threading
from pathlib import Path

from scanner.scanner import busca_pasta
from scanner.benchmark import (
    benchmark_threads,
    melhor_resultado
)
from visualization.charts import gerar_graficos

class ScannerApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Parallel File Scanner")
        self.geometry("1000x700")
        self.minsize(850, 600)
        
        self.graph_dir = (
            Path(__file__).resolve().parent
            / "graficos"
        )

        self.graph_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.tipo_busca_map = {
            "Nome do arquivo": "filename",
            "Extensão": "extension",
            "Texto no arquivo": "text"
        }

        self._criar_variaveis()
        self._criar_interface()
        self.atualizar_lista_graficos()

    def _criar_variaveis(self):

        self.pasta_var = tk.StringVar(
        )
        self.tipo_busca_var = tk.StringVar(
            value="Extensão"
        )
        self.termo_busca_var = tk.StringVar(
            value=".pdf"
        )
        self.threads_busca_var = tk.StringVar(
            value="8"
        )
        self.threads_benchmark_var = tk.StringVar(
            value="1,2,4,8,16,32,64"
        )
        self.status_var = tk.StringVar(
            value="Pronto."
        )

    def _criar_interface(self):

        container = ttk.Frame(
            self,
            padding=15
        )

        container.pack(
            fill="both",
            expand=True
        )

        self._criar_configuracoes(container)
        self.notebook = ttk.Notebook(container)
        self.notebook.pack(
            fill="both",
            expand=True,
            pady=(15, 0)
        )

        self._cria_aba_pesquisa()
        self._cria_aba_benchmark()
        self._cria_aba_graficos()
        self._cria_status(container)

    