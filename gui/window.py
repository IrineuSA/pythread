from pathlib import Path
import tkinter as tk
from tkinter import ttk

class ScannerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pythread - Scanner de Arquivos em Paralelo")
        self.geometry("1000x700")
        self.minsize(850, 600)
        
        self.graph_dir = (
            Path(__file__).resolve().parent.parent
            / "graficos"
        )

        self.graph_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(
            fill="both",
            expand=True,
            pady=(15, 0)
        )

        self.notebook.add(
            self.benchmark_tab,
            text="Benchmark"
        )

        self.notebook.add(
            self.graphs_tab,
            text="Gráficos"
        )

    def executar_benchmark(self, config):
        self.benchmark_tab.executar(
            config,
            self.graph_dir,
            on_complete=self.graphs_tab.atualizar
        )
