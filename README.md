# msxRead

Leitor e visualizador de arquivos MSX BASIC tokenizados (formato binario com 0xFF no inicio)
e arquivos do Graphos III, com interface grafica para navegar e visualizar.

Este programa nao faz parte do Basic Dignified Suite nem do MSX Converter; e um projeto independente apenas inspirado neles.

![Screenshot do msxRead](read-00.png)

## O que foi usado nesta parte
- Parser MSX BASIC: decodificacao de tokens 0x80.., 0xFF e numeros (inclui BCD customizado).
- Detector simples de arquivo MSX BASIC: verifica byte 0xFF no inicio.
- Persistencia local: guarda ultima pasta/arquivo e tamanho da janela em `msxread.db`.
- Fontes MSX (opcional): `MSX-Screen0.ttf` e `MSX-Screen1.ttf`.

## Projetos que inspiraram esta parte
- Basic Dignified Suite: https://github.com/farique1/basic-dignified
- MSX Converter: https://github.com/fgroen/msxconverter

## Instalacao
Requer Python 3.10+ (testado com Tkinter no Windows).

```sh
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Execucao
```sh
python main.py
```

Selecione um diretorio com arquivos MSX/Graphos.
O programa lista os arquivos, abre o selecionado e mostra o texto ASCII ou o visualizador adequado.

Formatos suportados (Graphos III):
- `.SHP` (Shapes)
- `.ALF` (Alfabeto)
- `.LAY` (Layout)
- `.SCR` (Screen 2)

## Bibliotecas usadas
- `customtkinter` (UI)
- `tkinter` (widgets nativos)
- `sqlite3` (persistencia local)
- `pathlib` (paths)

## Ferramentas usadas
- Python
- pip/venv
- Git

## Ferramenta de IA usada
- OpenAI Codex CLI (GPT-5)
