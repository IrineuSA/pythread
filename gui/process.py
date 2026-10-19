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
        self._criar_fila()
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
        
        self.waiting_label = ttk.Label(
            frame,
            text="WAITING: 0"
        )

        self.waiting_label.pack(
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

    def _criar_fila(self):
        frame=ttk.LabelFrame(
            self,
            text="Fila de Prontos"
        )
        frame.pack(
            fill="x",
            pady=(0,10)
        )
        self.ready_queue_label=ttk.Label(
            frame,
            text="Fila vazia",
            anchor="w"
        )
        self.ready_queue_label.pack(
            fill="x",
            padx=10,
            pady=10
        )
    
    def atualizar_processo(
        self,
        pid,
        arquivo,
        estado
    ):
        self.after(
            0,
            self._aplicar_atualizacao,
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
        waiting=0

        for processo in self.processos.values():
            estado = processo["estado"]
            if estado == EstadoProcesso.READY:
                ready += 1
            
            elif estado == EstadoProcesso.RUNNING:
                running += 1

            elif estado == EstadoProcesso.TERMINATED:
                terminated += 1
            
            elif estado == EstadoProcesso.WAITING:
                waiting += 1

        self.ready_label.config(
            text=f"READY: {ready}"
        )

        self.running_label.config(
            text=f"RUNNING: {running}"
        )

        self.terminated_label.config(
            text=f"TERMINATED: {terminated}"
        )

        self.waiting_label.config(
            text=f"WAITING: {waiting}"
        )

        ready_processes=[
            pid
            for pid,processo in self.processos.items()
            if processo["estado"] == EstadoProcesso.READY
        ]
        if ready_processes:
            primeiros=ready_processes[:15]
            texto=" -> ".join(
                f"P{pid}" for pid in primeiros
            )
            if len(ready_processes) > 15:
                texto += f" -> ... ({len(ready_processes)} na fila)"
        else:
            texto = "Fila vazia"
        self.ready_queue_label.config(
            text=texto
        )

    def limpar(self):
        self.processos.clear()

        for item in self.tree.get_children():
            self.tree.delete(item)
        self._atualizar_resumo()