"""Genera el resumen Markdown del TP4 a partir del CSV existente.

No vuelve a procesar el video. Solo fusiona resultados ya medidos.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from video_lib import csv_path, environment_info, final_md_path, load_csv_rows, write_results_md


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    default_output_dir = base_dir.parent / "resultados"

    parser = argparse.ArgumentParser(description="Fusiona resultados parciales del TP4 en un Markdown.")
    parser.add_argument("--output-dir", type=Path, default=default_output_dir, help="Carpeta de resultados.")
    args = parser.parse_args()

    output_dir = args.output_dir.resolve()
    rows = load_csv_rows(csv_path(output_dir))
    if not rows:
        raise SystemExit(f"No hay resultados para fusionar en {csv_path(output_dir)}")

    env = environment_info()
    final_path = final_md_path(output_dir)
    write_results_md(
        final_path,
        "Resumen benchmarks TP4 posterize",
        rows,
        env,
        all_rows_for_speedup=rows,
    )
    print(f"Markdown final actualizado: {final_path}")


if __name__ == "__main__":
    main()
