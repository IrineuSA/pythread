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