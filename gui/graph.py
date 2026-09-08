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