"""Benchmark por partes para el TP de Sobel.

Ejemplos:
    python benchmark_sobel.py --size 750 --methods secuencial,numpy,numba_cpu --runs 5
    python benchmark_sobel.py --size 3000 --methods numba_cpu --runs 5 --workers 8
    python benchmark_sobel.py --size 6000 --methods numba_gpu --runs 5 --output-dir ../resultados/entrega2
"""

import argparse
import os
import sys
from pathlib import Path
from time import perf_counter

from sobel_lib import (
    METHOD_LABELS,
    VALID_SIZES,
    RunMeasurement,
    SummaryRow,
    aggregate_md_path_for_size,
    average_measurements,
    csv_path_for_size,
    environment_info,
    load_rgb_image_bytes,
    output_metrics,
    parse_method_list,
    partial_md_path,
    sobel_image_path,
    update_aggregate_rows,
    validate_size,
    write_gray_png,
    write_method_final_md,
    write_results_md,
)


def run_sequential(
    size: int,
    runs: int,
    seed: int,
    output_dir: Path,
    input_dir: Path,
) -> tuple[SummaryRow, list[RunMeasurement]]:
    from sobel_secuencial import rgb_to_gray_sequential, sobel_sequential

    print(f"[Progreso] secuencial {size}x{size}: cargando imagen fuera de la medicion", flush=True)
    rgb_bytes = load_rgb_image_bytes(input_dir, size)
    measurements: list[RunMeasurement] = []
    last_sobel: object | None = None
    for run_index in range(1, runs + 1):
        print(f"[Progreso] secuencial {size}x{size} corrida {run_index}/{runs}: midiendo", flush=True)
        t0 = perf_counter()
        gray = rgb_to_gray_sequential(rgb_bytes, size, size)
        t1 = perf_counter()
        sobel = sobel_sequential(gray, size, size)
        t2 = perf_counter()
        last_sobel = sobel

        white_pixels, total_pixels, white_percent, checksum, output_hash = output_metrics(sobel)
        measurements.append(
            RunMeasurement(
                run_index=run_index,
                rgb_to_gray_s=t1 - t0,
                sobel_s=t2 - t1,
                total_s=(t1 - t0) + (t2 - t1),
                white_pixels=white_pixels,
                total_pixels=total_pixels,
                white_percent=white_percent,
                checksum=checksum,
                output_hash=output_hash,
            )
        )
    if last_sobel is not None:
        path = sobel_image_path(output_dir, size, "secuencial")
        write_gray_png(last_sobel, size, size, path)
        print(f"[Progreso] Imagen Sobel guardada: {path}", flush=True)
    row = average_measurements("secuencial", size, runs, 1, seed, measurements)
    return row, measurements


def run_numpy(
    size: int,
    runs: int,
    seed: int,
    output_dir: Path,
    input_dir: Path,
) -> tuple[SummaryRow, list[RunMeasurement]]:
    import numpy as np

    from sobel_numpy import rgb_to_gray_numpy, sobel_numpy

    print(f"[Progreso] NumPy {size}x{size}: cargando imagen fuera de la medicion", flush=True)
    rgb_bytes = load_rgb_image_bytes(input_dir, size)
    rgb = np.frombuffer(rgb_bytes, dtype=np.uint8).reshape((size, size, 3))
    measurements: list[RunMeasurement] = []
    last_sobel: object | None = None
    for run_index in range(1, runs + 1):
        print(f"[Progreso] NumPy {size}x{size} corrida {run_index}/{runs}: midiendo", flush=True)
        t0 = perf_counter()
        gray = rgb_to_gray_numpy(rgb)
        t1 = perf_counter()
        sobel = sobel_numpy(gray)
        t2 = perf_counter()
        last_sobel = sobel

        white_pixels, total_pixels, white_percent, checksum, output_hash = output_metrics(sobel)
        measurements.append(
            RunMeasurement(
                run_index=run_index,
                rgb_to_gray_s=t1 - t0,
                sobel_s=t2 - t1,
                total_s=(t1 - t0) + (t2 - t1),
                white_pixels=white_pixels,
                total_pixels=total_pixels,
                white_percent=white_percent,
                checksum=checksum,
                output_hash=output_hash,
            )
        )
    if last_sobel is not None:
        path = sobel_image_path(output_dir, size, "numpy")
        write_gray_png(last_sobel, size, size, path)
        print(f"[Progreso] Imagen Sobel guardada: {path}", flush=True)
    row = average_measurements("numpy", size, runs, 1, seed, measurements)
    return row, measurements


def run_numba_cpu(
    size: int,
    runs: int,
    seed: int,
    workers: int | None,
    output_dir: Path,
    input_dir: Path,
) -> tuple[SummaryRow, list[RunMeasurement]]:
    import numpy as np

    from sobel_numba_cpu import rgb_to_gray_numba, set_numba_workers, sobel_numba, warmup_numba

    effective_workers = set_numba_workers(workers)
    print(f"[Progreso] Numba CPU: compilando kernels fuera de la medicion", flush=True)
    warmup_numba()
    print(f"[Progreso] Numba CPU {size}x{size}: cargando imagen fuera de la medicion", flush=True)
    rgb_bytes = load_rgb_image_bytes(input_dir, size)
    rgb = np.frombuffer(rgb_bytes, dtype=np.uint8).reshape((size, size, 3))

    measurements: list[RunMeasurement] = []
    last_sobel: object | None = None
    for run_index in range(1, runs + 1):
        print(f"[Progreso] Numba CPU {size}x{size} corrida {run_index}/{runs}: midiendo", flush=True)
        t0 = perf_counter()
        gray = rgb_to_gray_numba(rgb)
        t1 = perf_counter()
        sobel = sobel_numba(gray)
        t2 = perf_counter()
        last_sobel = sobel

        white_pixels, total_pixels, white_percent, checksum, output_hash = output_metrics(sobel)
        measurements.append(
            RunMeasurement(
                run_index=run_index,
                rgb_to_gray_s=t1 - t0,
                sobel_s=t2 - t1,
                total_s=(t1 - t0) + (t2 - t1),
                white_pixels=white_pixels,
                total_pixels=total_pixels,
                white_percent=white_percent,
                checksum=checksum,
                output_hash=output_hash,
            )
        )
    if last_sobel is not None:
        path = sobel_image_path(output_dir, size, "numba_cpu")
        write_gray_png(last_sobel, size, size, path)
        print(f"[Progreso] Imagen Sobel guardada: {path}", flush=True)
    row = average_measurements("numba_cpu", size, runs, effective_workers, seed, measurements)
    return row, measurements


def run_numba_gpu(
    size: int,
    runs: int,
    seed: int,
    output_dir: Path,
    input_dir: Path,
) -> tuple[SummaryRow, list[RunMeasurement]]:
    import numpy as np
    from numba import cuda

    from sobel_numba_gpu import (
        THREADS_PER_BLOCK,
        blocks_per_grid,
        rgb_to_gray_cuda,
        sobel_cuda,
        warmup_numba_gpu,
    )

    print("[Progreso] Numba GPU: compilando kernels fuera de la medicion", flush=True)
    warmup_numba_gpu()
    print(f"[Progreso] Numba GPU {size}x{size}: cargando imagen fuera de la medicion", flush=True)
    rgb_bytes = load_rgb_image_bytes(input_dir, size)
    rgb = np.frombuffer(rgb_bytes, dtype=np.uint8).reshape((size, size, 3))
    blocks = blocks_per_grid(size, size)
    threads_per_block = THREADS_PER_BLOCK[0] * THREADS_PER_BLOCK[1]

    measurements: list[RunMeasurement] = []
    last_sobel: object | None = None
    for run_index in range(1, runs + 1):
        print(f"[Progreso] Numba GPU {size}x{size} corrida {run_index}/{runs}: midiendo", flush=True)

        transfer_in_start = perf_counter()
        rgb_device = cuda.to_device(rgb)
        gray_device = cuda.device_array((size, size), dtype=np.uint8)
        sobel_device = cuda.device_array((size, size), dtype=np.uint8)
        cuda.synchronize()
        transfer_in_s = perf_counter() - transfer_in_start

        t0 = perf_counter()
        rgb_to_gray_cuda[blocks, THREADS_PER_BLOCK](rgb_device, gray_device)
        cuda.synchronize()
        t1 = perf_counter()
        sobel_cuda[blocks, THREADS_PER_BLOCK](gray_device, sobel_device)
        cuda.synchronize()
        t2 = perf_counter()

        transfer_out_start = perf_counter()
        sobel = sobel_device.copy_to_host()
        cuda.synchronize()
        transfer_out_s = perf_counter() - transfer_out_start
        last_sobel = sobel

        white_pixels, total_pixels, white_percent, checksum, output_hash = output_metrics(sobel)
        measurements.append(
            RunMeasurement(
                run_index=run_index,
                rgb_to_gray_s=t1 - t0,
                sobel_s=t2 - t1,
                total_s=(t1 - t0) + (t2 - t1),
                white_pixels=white_pixels,
                total_pixels=total_pixels,
                white_percent=white_percent,
                checksum=checksum,
                output_hash=output_hash,
                transfer_h2d_s=transfer_in_s,
                transfer_d2h_s=transfer_out_s,
                transfer_total_s=transfer_in_s + transfer_out_s,
            )
        )
    if last_sobel is not None:
        path = sobel_image_path(output_dir, size, "numba_gpu")
        write_gray_png(last_sobel, size, size, path)
        print(f"[Progreso] Imagen Sobel guardada: {path}", flush=True)
    row = average_measurements("numba_gpu", size, runs, threads_per_block, seed, measurements)
    return row, measurements


def run_method(
    method_key: str,
    size: int,
    runs: int,
    seed: int,
    workers: int | None,
    output_dir: Path,
    input_dir: Path,
) -> tuple[SummaryRow, list[RunMeasurement]]:
    try:
        if method_key == "secuencial":
            return run_sequential(size, runs, seed, output_dir, input_dir)
        if method_key == "numpy":
            return run_numpy(size, runs, seed, output_dir, input_dir)
        if method_key == "numba_cpu":
            return run_numba_cpu(size, runs, seed, workers, output_dir, input_dir)
        if method_key == "numba_gpu":
            return run_numba_gpu(size, runs, seed, output_dir, input_dir)
    except Exception as exc:
        row = SummaryRow(
            timestamp="",
            method_key=method_key,
            method_label=METHOD_LABELS[method_key],
            size=size,
            runs=runs,
            workers=workers or 1,
            seed=seed,
            rgb_to_gray_s=None,
            sobel_s=None,
            total_s=None,
            white_percent=None,
            white_pixels=None,
            total_pixels=None,
            checksum=None,
            output_hash=None,
            status="error",
            error=str(exc),
        )
        return row, []

    raise ValueError(f"Metodo no soportado: {method_key}")


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    default_output_dir = base_dir.parent / "resultados"
    default_input_dir = base_dir.parent / "imagenes"

    parser = argparse.ArgumentParser(
        description="Ejecuta benchmarks parciales de Sobel y genera CSV/Markdown por tamanio.",
    )
    parser.add_argument(
        "--size",
        type=validate_size,
        default=750,
        help=f"Tamanio NxN a ejecutar. Consigna: {', '.join(str(s) for s in VALID_SIZES)}. Default: 750.",
    )
    parser.add_argument(
        "--methods",
        type=parse_method_list,
        default=["secuencial"],
        help="Metodos separados por coma: secuencial,numpy,numba_cpu,numba_gpu. Default: secuencial.",
    )
    parser.add_argument("--runs", type=int, default=5, help="Cantidad de corridas. Consigna: minimo 5.")
    parser.add_argument("--seed", type=int, default=2026, help="Seed registrada en resultados para reproducibilidad.")
    parser.add_argument(
        "--workers",
        type=int,
        default=os.cpu_count() or 1,
        help="Hilos para Numba CPU. No afecta secuencial ni NumPy.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=default_output_dir,
        help="Carpeta de resultados Markdown/CSV.",
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=default_input_dir,
        help="Carpeta con IMG_0358_<NxN>.jpg.",
    )
    parser.add_argument(
        "--allow-non-consigna-size",
        action="store_true",
        help="Permite usar tamanios chicos para smoke test, por ejemplo --size 64.",
    )
    args = parser.parse_args()

    if args.runs < 1:
        raise SystemExit("--runs debe ser >= 1")
    if args.runs < 5:
        print("[Aviso] La consigna pide al menos 5 corridas; este valor sirve solo para prueba rapida.", flush=True)
    if args.size not in VALID_SIZES and not args.allow_non_consigna_size:
        valid = ", ".join(str(s) for s in VALID_SIZES)
        raise SystemExit(f"--size debe ser uno de la consigna ({valid}) o usar --allow-non-consigna-size")

    output_dir = args.output_dir.resolve()
    input_dir = args.input_dir.resolve()
    csv_path = csv_path_for_size(output_dir, args.size)
    aggregate_md_path = aggregate_md_path_for_size(output_dir, args.size)
    env = environment_info()

    new_rows: list[SummaryRow] = []
    measurements_by_method: dict[str, list[RunMeasurement]] = {}

    print(f"[Progreso] Benchmark Sobel {args.size}x{args.size} | metodos={','.join(args.methods)}", flush=True)
    for method_key in args.methods:
        row, measurements = run_method(method_key, args.size, args.runs, args.seed, args.workers, output_dir, input_dir)
        new_rows.append(row)
        measurements_by_method[method_key] = measurements
        print(f"[Progreso] Finalizado {METHOD_LABELS[method_key]}: estado={row.status}", flush=True)

    aggregate_rows = update_aggregate_rows(csv_path, new_rows)
    write_results_md(
        aggregate_md_path,
        f"Resultados Sobel {args.size}x{args.size}",
        aggregate_rows,
        measurements_by_method,
        env,
        aggregate_rows_for_speedup=aggregate_rows,
    )

    for row in new_rows:
        write_results_md(
            partial_md_path(output_dir, args.size, row.method_key),
            f"Resultado parcial Sobel {args.size}x{args.size} - {row.method_label}",
            [row],
            {row.method_key: measurements_by_method.get(row.method_key, [])},
            env,
            aggregate_rows_for_speedup=aggregate_rows,
        )
        final_path = write_method_final_md(output_dir, row.method_key, env)
        if final_path is not None:
            print(f"Markdown final por metodo: {final_path}")

    print(f"CSV actualizado: {csv_path}")
    print(f"Markdown agregado: {aggregate_md_path}")
    print(f"Markdown parciales: {output_dir / 'parciales'}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.", file=sys.stderr)
        raise SystemExit(130)
