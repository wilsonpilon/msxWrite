from __future__ import annotations

import os
import time
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

import customtkinter as ctk

from app_db import AppDatabase
from msx_basic_decoder import decode_msx_basic


APP_TITLE = "msxRead"
DB_NAME = "msxread.db"


class MSXViewer(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.db = AppDatabase(Path(DB_NAME))

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.title(APP_TITLE)
        geometry = self.db.get_setting("window_geometry", "1100x700")
        if geometry:
            self.geometry(geometry)

        self.base_dir = self.db.get_setting("last_dir", str(Path.cwd()))
        self.current_file: str | None = None

        self._load_fonts()
        self._build_layout()
        self._refresh_file_list()
        self._load_last_file()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _load_fonts(self) -> None:
        self.text_font = ("Consolas", 12)
        ttf_path = Path("MSX-Screen0.ttf")
        if ttf_path.exists():
            try:
                ctk.FontManager.load_font(str(ttf_path))
                self.text_font = ("MSX Screen 0", 14)
            except Exception:
                self.text_font = ("Consolas", 12)

    def _build_layout(self) -> None:
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        header.grid_columnconfigure(1, weight=1)

        self.dir_label = ctk.CTkLabel(header, text="Diretorio:")
        self.dir_label.grid(row=0, column=0, sticky="w", padx=(10, 5), pady=10)

        self.dir_value = ctk.CTkLabel(header, text=self.base_dir, anchor="w")
        self.dir_value.grid(row=0, column=1, sticky="ew", padx=5, pady=10)

        choose_button = ctk.CTkButton(header, text="Selecionar", command=self._choose_directory)
        choose_button.grid(row=0, column=2, padx=5, pady=10)

        refresh_button = ctk.CTkButton(header, text="Atualizar", command=self._refresh_file_list)
        refresh_button.grid(row=0, column=3, padx=(5, 10), pady=10)

        left = ctk.CTkFrame(self)
        left.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=(0, 10))
        left.grid_rowconfigure(0, weight=1)
        left.grid_columnconfigure(0, weight=1)

        list_frame = ctk.CTkFrame(left)
        list_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        self.file_listbox = tk.Listbox(list_frame, activestyle="none")
        self.file_listbox.grid(row=0, column=0, sticky="nsew")
        self.file_listbox.bind("<<ListboxSelect>>", self._on_file_select)

        scrollbar = tk.Scrollbar(list_frame, command=self.file_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.file_listbox.config(yscrollcommand=scrollbar.set)

        right = ctk.CTkFrame(self)
        right.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=(0, 10))
        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)

        self.file_label = ctk.CTkLabel(right, text="Selecione um arquivo MSX BASIC")
        self.file_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

        self.textbox = ctk.CTkTextbox(right, wrap="none")
        self.textbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.textbox.configure(font=self.text_font, state="disabled")

        self.status_label = ctk.CTkLabel(right, text="", anchor="w")
        self.status_label.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))

    def _choose_directory(self) -> None:
        path = filedialog.askdirectory(initialdir=self.base_dir, title="Selecione o diretorio")
        if not path:
            return
        self.base_dir = path
        self.dir_value.configure(text=path)
        self.db.set_setting("last_dir", path)
        self._refresh_file_list()

    def _refresh_file_list(self) -> None:
        self.file_listbox.delete(0, tk.END)
        base_path = Path(self.base_dir)
        files = []
        if base_path.exists():
            for entry in base_path.iterdir():
                if entry.is_file() and self._looks_like_msx_basic(entry):
                    files.append(entry.name)
        for name in sorted(files, key=str.lower):
            self.file_listbox.insert(tk.END, name)
        self.status_label.configure(text=f"{len(files)} arquivos MSX BASIC encontrados")

    def _looks_like_msx_basic(self, path: Path) -> bool:
        try:
            with path.open("rb") as handle:
                first = handle.read(1)
            return first == b"\xFF"
        except OSError:
            return False

    def _on_file_select(self, _event: tk.Event) -> None:
        selection = self.file_listbox.curselection()
        if not selection:
            return
        name = self.file_listbox.get(selection[0])
        file_path = str(Path(self.base_dir) / name)
        self._open_file(file_path)

    def _open_file(self, file_path: str) -> None:
        try:
            data = Path(file_path).read_bytes()
            decoded = decode_msx_basic(data)
        except Exception as exc:
            messagebox.showerror("Erro ao abrir", str(exc))
            return

        self.current_file = file_path
        self.db.set_setting("last_file", file_path)
        self.db.touch_recent_file(file_path, int(time.time()))

        self.file_label.configure(text=Path(file_path).name)
        self._set_text(decoded)

    def _set_text(self, text: str) -> None:
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", tk.END)
        self.textbox.insert("1.0", text)
        self.textbox.configure(state="disabled")

    def _load_last_file(self) -> None:
        last_file = self.db.get_setting("last_file")
        if not last_file:
            return
        path = Path(last_file)
        if path.exists():
            self.base_dir = str(path.parent)
            self.dir_value.configure(text=self.base_dir)
            self._refresh_file_list()
            self._open_file(str(path))

    def _on_close(self) -> None:
        self.db.set_setting("window_geometry", self.geometry())
        self.destroy()


def main() -> None:
    app = MSXViewer()
    app.mainloop()


if __name__ == "__main__":
    main()
