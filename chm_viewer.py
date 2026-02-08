import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from pathlib import Path
from tkinterweb import HtmlFrame
from chm_parser import CHMParser

class CHMViewer(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Leitor de CHM Moderno")
        self.geometry("1100x800")
        
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.current_parser = None
        self.chm_files = ["MSXBIOS.CHM", "MANUALS.CHM", "MSX.CHM", "SOFTWARE.CHM"]
        
        self._build_ui()
        self._load_chm(self.chm_files[0])

    def _build_ui(self):
        # Header with selector
        header = ctk.CTkFrame(self)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        ctk.CTkLabel(header, text="Arquivo CHM:").pack(side="left", padx=10)
        
        self.chm_selector = ctk.CTkComboBox(header, values=self.chm_files, command=self._on_chm_change, width=200)
        self.chm_selector.pack(side="left", padx=10)
        self.chm_selector.set(self.chm_files[0])

        # Left panel (TOC)
        left_panel = ctk.CTkFrame(self, width=300)
        left_panel.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=(0, 10))
        left_panel.grid_rowconfigure(0, weight=1)
        left_panel.grid_columnconfigure(0, weight=1)
        
        # We use a standard Treeview for TOC because CTK doesn't have one yet
        style = ttk.Style()
        style.configure("Treeview", font=("Segoe UI", 10))
        
        self.tree = ttk.Treeview(left_panel, show="tree", selectmode="browse")
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)
        
        scrollbar = ttk.Scrollbar(left_panel, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Right panel (HTML Content)
        right_panel = ctk.CTkFrame(self)
        right_panel.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=(0, 10))
        right_panel.grid_rowconfigure(0, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)
        
        self.html_view = HtmlFrame(right_panel)
        self.html_view.grid(row=0, column=0, sticky="nsew")

    def _load_chm(self, filename):
        path = Path(filename)
        if not path.exists():
            print(f"Arquivo não encontrado: {filename}")
            return
            
        self.current_parser = CHMParser(path)
        toc = self.current_parser.get_toc()
        
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        self._populate_tree("", toc)

    def _populate_tree(self, parent, items):
        for item in items:
            node = self.tree.insert(parent, "end", text=item['name'], values=(item['local'],))
            if item['children']:
                self._populate_tree(node, item['children'])

    def _on_chm_change(self, choice):
        self._load_chm(choice)

    def _on_tree_select(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
            
        local_path = self.tree.item(selected_item[0], "values")[0]
        if local_path and Path(local_path).exists():
            self.html_view.load_file(local_path)

if __name__ == "__main__":
    app = ctk.CTk()
    viewer = CHMViewer(app)
    app.mainloop()
