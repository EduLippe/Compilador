import glob
import os
import re
import subprocess
import sys

# Roda o compilador (main.py) em cada arquivo da pasta testes/ e confere o
# resultado com o que esta escrito na primeira linha de cada arquivo:
#   // espera: ok
#   // espera: lexico linha 3
#   // espera: sintatico linha 5      (a linha e opcional)
#   // espera: semantico linha 4

FASES = {
    "erros lexicos": "lexico",
    "erros sintaticos": "sintatico",
    "erros semanticos": "semantico",
}


def ler_expectativa(caminho):
    with open(caminho, encoding="utf-8") as arquivo:
        primeira = arquivo.readline()
    m = re.match(r"//\s*espera:\s*(\w+)(?:\s+linha\s+(\d+))?", primeira)
    if m is None:
        return None, None
    linha = int(m.group(2)) if m.group(2) else None
    return m.group(1), linha


def rodar(caminho):
    r = subprocess.run(
        [sys.executable, "main.py", caminho],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return r.returncode, r.stdout, r.stderr


def obtido(codigo, saida, erros):
    texto = erros + saida
    if codigo == 0:
        valido = saida.lstrip().startswith("INPP") and saida.rstrip().endswith("FIM")
        return ("ok" if valido else "saida_invalida"), None
    for frase, fase in FASES.items():
        if frase in texto:
            m = re.search(r"linha (\d+)", texto)
            return fase, int(m.group(1)) if m else None
    return "quebrou", None


def main():
    pasta = sys.argv[1] if len(sys.argv) > 1 else "testes"
    arquivos = sorted(glob.glob(os.path.join(pasta, "*.coda")))
    falhas = 0

    print(f"{'teste':44} {'esperado':22} {'obtido':22} resultado")
    print("-" * 100)
    for caminho in arquivos:
        nome = os.path.basename(caminho)[:-5]
        fase_esp, linha_esp = ler_expectativa(caminho)
        codigo, saida, erros = rodar(caminho)
        fase_obt, linha_obt = obtido(codigo, saida, erros)

        passou = fase_esp == fase_obt
        if passou and linha_esp is not None:
            passou = linha_esp == linha_obt

        esp = fase_esp + (f" l.{linha_esp}" if linha_esp else "")
        obt = fase_obt + (f" l.{linha_obt}" if linha_obt else "")
        print(f"{nome:44} {esp:22} {obt:22} {'ok' if passou else 'FALHOU'}")
        if not passou:
            falhas += 1
            ultima = [l for l in (erros.strip().splitlines()) if l.strip()][-1:] 
            if fase_obt == "quebrou" and ultima:
                print(f"    ultima linha do erro: {ultima[0]}")

    print("-" * 100)
    print(f"{len(arquivos) - falhas} de {len(arquivos)} testes passaram")
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
