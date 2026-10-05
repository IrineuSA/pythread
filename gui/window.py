from pathlib import Path
import tkinter as tk
from tkinter import ttk

from gui.config import ConfigFrame
from gui.bench import BenchmarkTab
from gui.graph import GraphsTab

from gui.utils import obter_diretorio_app

from gui.process import ProcessTab
import threading
class ScannerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pythread - Scanner de Arquivos em Paralelo")
        self.geometry("1000x700")
        self.minsize(850, 600)
        
        self.graph_dir = (
            obter_diretorio_app()
            / "graficos"
        )

        self.graph_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.config_frame = ConfigFrame(
            self,
            on_benchmark=self.executar_benchmark,
            on_simulation=self.executar_simulacao
        )
        self.config_frame.pack(
            fill="x",
            padx=15,
            pady=15
        )

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(
            fill="both",
            expand=True,
            pady=(0, 15)
        )

        self.benchmark_tab = BenchmarkTab(
            self.notebook
        )

        self.graphs_tab = GraphsTab(
            self.notebook,
            self.graph_dir
        )

        self.notebook.add(
            self.benchmark_tab,
            text="Benchmark"
        )

        self.notebook.add(
            self.graphs_tab,
            text="Gráficos"
        )

        self.process_tab = ProcessTab(
            self.notebook
        )

        self.notebook.add(
            self.process_tab,
            text="Processos"
        )

    def executar_benchmark(self, config):
        self.benchmark_tab.executar(
            config,
            self.graph_dir,
            on_complete=self.graphs_tab.atualizar
        )

    def executar_simulacao(
        self,
        config
    ):
        self.process_tab.limpar()

        self.notebook.select(
            self.process_tab
        )
        thread = threading.Thread(
            target=self._executar_simulacao_thread,
            args=(config,),
            daemon=True
        )
        thread.start()
