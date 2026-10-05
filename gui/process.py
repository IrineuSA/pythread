import tkinter as tk
from tkinter import ttk
from scanner.process import EstadoProcesso

class ProcessTab(ttk.Frame):

    def __init__(self, parent):
        super().__init__(
            parent,
            padding=10
        )

        self.processos = {}
        self._criar_resumo()
        self._criar_tabela()

    def _criar_resumo(self):
        frame = ttk.Frame(self)
        frame.pack(
            fill="x",
            pady=(0, 10)
        )

        self.ready_label = ttk.Label(
            frame,
            text="READY: 0"
        )

        self.ready_label.pack(
            side="left",
            padx=10
        )

        self.running_label = ttk.Label(
            frame,
            text="RUNNING: 0"
        )

        self.running_label.pack(
            side="left",
            padx=10
        )

        self.terminated_label = ttk.Label(
            frame,
            text="TERMINATED: 0"
        )

        self.terminated_label.pack(
            side="left",
            padx=10
        )

    def _criar_tabela(self):
        colunas = (
            "pid",
            "arquivo",
            "estado"
        )

        self.tree = ttk.Treeview(
            self,
            columns=colunas,
            show="headings"
        )

        self.tree.heading(
            "pid",
            text="PID"
        )

        self.tree.heading(
            "arquivo",
            text="Arquivo"
        )

        self.tree.heading(
            "estado",
            text="Estado"
        )

        self.tree.column(
            "pid",
            width=80
        )

        self.tree.column(
            "arquivo",
            width=600
        )

        self.tree.column(
            "estado",
            width=150
        )

        self.tree.pack(
            fill="both",
            expand=True
        )
    
    def atualizar_processo(
        self,
        pid,
        arquivo,
        estado
    ):
        self.after(
            0,
            self._aplica_atualizacao,
            pid,
            arquivo,
            estado
        )
    
    def _aplicar_atualizacao(
        self,
        pid,
        arquivo,
        estado
    ):
        self.processos[pid] = {
            "arquivo": arquivo,
            "estado": estado
        }

        item_id = str(pid)

        valores = (
            pid,
            arquivo.name,
            estado.value
        )
        if self.tree.exists(item_id):
            self.tree.item(
                item_id,
                values=valores
            )
        else:
            self.tree.insert(
                "",
                "end",
                iid=item_id,
                values=valores
            )
        self._atualizar_resumo()

    def _atualizar_resumo(self):
        ready=0
        running=0
        terminated=0

        for processo in self.processos.values():
            estado = processo["estado"]
            if estado == EstadoProcesso.READY:
                ready += 1
            
            elif estado == EstadoProcesso.RUNNING:
                running += 1

            elif estado == EstadoProcesso.TERMINATED:
                terminated += 1

        self.ready_label.config(
            text=f"READY: {ready}"
        )

        self.running_label_config(
            text=f"RUNNING: {running}"
        )

        self.terminated_label.config(
            text=f"TERMINATED: {terminated}"
        )

    def limpar(self):
        self.processos.clear()

        for item in self.tree.get_children():
            self.tree.delete(item)
        self._atualizar_resumo()