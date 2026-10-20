from pathlib import Path
import tkinter as tk
from tkinter import ttk

from gui.config import ConfigFrame
from gui.bench import BenchmarkTab
from gui.graph import GraphsTab

from gui.utils import obter_diretorio_app

from gui.process import ProcessTab

import threading
from scanner.scanner import busca_pasta

from tkinter import messagebox
from scanner.benchmark import benchmark_comparativo
from visual.graficos import grafico_comparativo
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
            on_simulation=self.executar_simulacao,
            on_comparison=self.executar_comparacao
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
    
    def _executar_simulacao_thread(
        self,
        config
    ):
        busca_pasta(
            pasta=config["pasta"],
            tipo_busca=config["tipo_busca"],
            termo_busca=config["termo_busca"],
            n_threads=max(config["threads"]),
            max_io=config["max_io"],
            algoritmo=config["algoritmo"],
            delay_ms=config["delay_ms"],
            processo_callback=self.process_tab.atualizar_processo,
            fila_callback=self.process_tab.atualizar_fila
        )
    
    def executar_comparacao(self,config):
        self.notebook.select(
            self.benchmark_tab
        )
        self.benchmark_tab.status_label.config(
            text="Comparando FCFS e SJF..."
        )
        thread = threading.Thread(
            target=self._executar_comparacao_thread,
            args=(config,),
            daemon=True
        )
        thread.start()

    def _executar_comparacao_thread(self, config):
        try:
            resultados = benchmark_comparativo(
                pasta=config["pasta"],
                tipo_busca=config["tipo_busca"],
                termo_busca=config["termo_busca"],
                n_threads=config["threads"],
                max_io=config["max_io"]
            )

            grafico_comparativo(
                resultados,
                salvar=True,
                pasta_saida=str(self.graph_dir),
                run_id="comparacao"
            )

            self.after(
                0,
                self._comparacao_concluida
            )

        except Exception as erro:
            self.after(
                0,
                lambda erro=erro: messagebox.showerror(
                    "Erro na comparação",
                    str(erro)
                )
            )
    
    def _comparacao_concluida(self):
        self.graphs_tab.atualizar()
        self.benchmark_tab.status_label.config(
        text="Comparação FCFS × SJF concluída."
        )
        self.notebook.select(
            self.graphs_tab
        )

        messagebox.showinfo(
            "Comparação concluída",
            "Gráfico comparativo gerado com sucesso."
        )