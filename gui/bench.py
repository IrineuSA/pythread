import threading
from tkinter import ttk
from tkinter import messagebox

from scanner.benchmark import (
    benchmark_threads,
    melhor_resultado
)
from visual.graficos import gerar_graficos

class BenchmarkTab(ttk.Frame):

    def __init__(self, parent):
        super().__init__(
            parent,
            padding=10
        )
        self._criar_tabela()

    def _criar_tabela(self):

        colunas = (
            "threads",
            "tempo",
            "arquivos",
            "encontrados",
            "throughput"
        )

        self.tree = ttk.Treeview(
            self,
            columns=colunas,
            show="headings"
        )
        self.tree.heading(
            "threads",
            text="Threads"
        )
        self.tree.heading(
            "tempo",
            text="Tempo"
        )
        self.tree.heading(
            "arquivos",
            text="Arquivos"
        )
        self.tree.heading(
            "encontrados",
            text="Encontrados"
        )
        self.tree.heading(
            "throughput",
            text="Arquivos/s"
        )
        self.tree.pack(
            fill="both",
            expand=True
        )

    def executar(
        self,
        config,
        graph_dir,
        on_complete=None
    ):

        thread = threading.Thread(
            target=self._executar_thread,
            args=(
                config,
                graph_dir,
                on_complete
            ),
            daemon=True
        )
        thread.start()
    
    def _executar_thread(
        self,
        config,
        graph_dir,
        on_complete
    ):

        try:
            resultados = benchmark_threads(
                pasta=config["pasta"],
                tipo_busca=config["tipo_busca"],
                termo_busca=config["termo_busca"],
                n_threads=config["threads"]
            )

            gerar_graficos(
                resultados,
                salvar=True,
                pasta_saida=str(graph_dir),
                mostrar=False
            )

            self.after(
                0,
                lambda:
                self._mostrar_resultados(
                    resultados,
                    on_complete
                )
            )

        except Exception as erro:
            self.after(
                0,
                lambda erro=erro:
                messagebox.showerror(
                    "Erro",
                    str(erro)
                )
            )

    def _mostrar_resultados(
        self,
        resultados,
        on_complete
  ):

            for item in self.tree.get_children():
                self.tree.delete(item)
                
            for resultado in resultados:
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        resultado["threads"],
                        f"{resultado['tempo']:.4f}",
                        resultado[
                            "arquivos escaneados"
                        ],
                        resultado[
                            "equivalentes"
                        ],
                        f"{resultado['arquivos por segundo']:.2f}"
                    )
                )

            melhor = melhor_resultado(
            resultados
        )
            messagebox.showinfo(
                "Benchmark concluído",
                (
                    f"Melhor resultado: "
                    f"{melhor['threads']} threads\n"
                    f"{melhor['arquivos por segundo']:.2f} "
                   "arquivos/s"
                )
            )

            if on_complete:
                on_complete()
