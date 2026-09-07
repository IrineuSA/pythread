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
from visual.graficos import gerar_graficos

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

    #Conf
    def _criar_configuracoes(self, parent):

        frame = ttk.LabelFrame(
            parent,
            text="Configuração da pesquisa",
            padding=10
        )
        frame.pack(
            fill="x"
        )
        frame.columnconfigure(
            1,
            weight=1
        )

        ttk.Label(
            frame,
            text="Pasta:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 8),
            pady=5
        )
        ttk.Entry(
            frame,
            textvariable=self.pasta_var
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            pady=5
        )

        ttk.Button(
            frame,
            text="Procurar...",
            command=self.selecionar_pasta
        ).grid(
            row=0,
            column=2,
            padx=(8, 0),
            pady=5
        )

        ttk.Label(
            frame,
            text="Tipo:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=(0, 8),
            pady=5
        )

        tipo_combo = ttk.Combobox(
            frame,
            textvariable=self.tipo_busca_var,
            values=list(
                self.tipo_busca_map.keys()
            ),
            state="readonly"
        )

        tipo_combo.grid(
            row=1,
            column=1,
            sticky="ew",
            pady=5
        )

        tipo_combo.bind(
            "<<ComboboxSelected>>",
            self.tipo_busca_alterado
        )

        ttk.Label(
            frame,
            text="Termo:"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=(0, 8),
            pady=5
        )

        self.termo_entry = ttk.Entry(
            frame,
            textvariable=self.termo_busca_var
        )
        self.termo_entry.grid(
            row=2,
            column=1,
            sticky="ew",
            pady=5
        )
        # Botões

        botoes = ttk.Frame(frame)

        botoes.grid(
            row=4,
            column=0,
            columnspan=3,
            sticky="ew",
            pady=(10, 0)
        )

        self.botao_pesquisar.pack(
            side="left"
        )

        self.botao_benchmark = ttk.Button(
            botoes,
            text="Benchmark + Gerar Gráficos",
            command=self.iniciar_benchmark
        )

        self.botao_benchmark.pack(
            side="left",
            padx=10
        )