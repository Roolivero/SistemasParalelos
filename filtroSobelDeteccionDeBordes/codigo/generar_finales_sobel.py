"""Genera Markdown finales por metodo a partir de los CSV ya existentes.

Uso:
    python generar_finales_sobel.py
    python generar_finales_sobel.py --methods secuencial,numpy,numba_cpu
"""

import argparse
from pathlib import Path

from sobel_lib import METHOD_LABELS, environment_info, parse_method_list, write_method_final_md


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    default_output_dir = base_dir.parent / "resultados"

    parser = argparse.ArgumentParser(
        description="Genera resultados/finales/resultado_final_<metodo>.md desde los CSV disponibles.",
    )
    parser.add_argument(
        "--methods",
        type=parse_method_list,
        default=list(METHOD_LABELS),
        help="Metodos separados por coma: secuencial,numpy,numba_cpu.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=default_output_dir,
        help="Carpeta donde estan los CSV resultados_sobel_<NxN>.csv.",
    )
    args = parser.parse_args()

    env = environment_info()
    output_dir = args.output_dir.resolve()

    generated = 0
    for method_key in args.methods:
        md_path = write_method_final_md(output_dir, method_key, env)
        if md_path is None:
            print(f"[Aviso] Sin resultados para {METHOD_LABELS[method_key]}")
            continue
        generated += 1
        print(f"Final generado: {md_path}")

    if generated == 0:
        raise SystemExit("No se genero ningun final: no hay CSV con resultados para los metodos pedidos.")


if __name__ == "__main__":
    main()
