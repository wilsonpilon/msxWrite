import os
import subprocess
import shutil
import tempfile
from pathlib import Path
from bs4 import BeautifulSoup

class CHMParser:
    def __init__(self, chm_path):
        self.chm_path = Path(chm_path)
        self.temp_dir = Path(tempfile.gettempdir()) / "msxwrite_chm" / self.chm_path.stem
        self._decompile()

    def _decompile(self):
        if not self.temp_dir.exists():
            self.temp_dir.mkdir(parents=True, exist_ok=True)
            # Use hh.exe to decompile CHM
            subprocess.run(['hh.exe', '-decompile', str(self.temp_dir), str(self.chm_path)], shell=True)

    def get_toc(self):
        # Look for .hhc or .hhk
        hhc_files = list(self.temp_dir.glob("*.hhc"))
        hhk_files = list(self.temp_dir.glob("*.hhk"))
        
        toc_file = hhc_files[0] if hhc_files else (hhk_files[0] if hhk_files else None)
        
        if not toc_file:
            return []

        with open(toc_file, 'r', encoding='latin-1', errors='replace') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
        return self._parse_ul(soup.find('ul'))

    def _parse_ul(self, ul):
        if not ul:
            return []
        
        items = []
        for li in ul.find_all('li', recursive=False):
            obj = li.find('object', type="text/sitemap")
            if obj:
                name = ""
                local = ""
                for param in obj.find_all('param'):
                    p_name = param.get('name', '').lower()
                    if p_name == 'name':
                        name = param.get('value', '')
                    elif p_name == 'local':
                        local = param.get('value', '')
                
                # Check for nested UL
                sub_items = []
                next_ul = li.find_next_sibling('ul')
                # In some CHM structures, UL is inside LI, in others it's after LI
                if not next_ul:
                    next_ul = li.find('ul')
                
                item = {
                    'name': name,
                    'local': str(self.temp_dir / local) if local else "",
                    'children': self._parse_ul(next_ul)
                }
                items.append(item)
        return items

    def cleanup(self):
        # Optional: cleanup temp files
        # shutil.rmtree(self.temp_dir, ignore_errors=True)
        pass
