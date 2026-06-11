"""Benchmark del TP4: video 4K con filtro posterize.

Ejemplos desde video4k/codigo:
    python benchmark_video4k.py --method secuencial --runs 3
    python benchmark_video4k.py --method pytorch_cpu --runs 3 --workers 6
    python benchmark_video4k.py --method pytorch_gpu --runs 3 --merge-audio

Para una prueba corta antes del benchmark final:
    python benchmark_video4k.py --method pytorch_cpu --runs 1 --max-frames 60
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from time import perf_counter

import numpy as np

from posterize_filter import METHOD_LABELS, build_processor
from video_lib import (
    RunMeasurement,
    average_measurements,
    csv_path,
    environment_info,
    frame_hash,
    merge_audio_with_ffmpeg,
    output_video_path,
    output_video_with_audio_path,
    partial_md_path,
    peak_rss_mb,
    update_csv,
    video_info,
    write_results_md,
)


def parse_method(value: str) -> str:
    if value not in METHOD_LABELS:
        valid = ", ".join(METHOD_LABELS)
        raise argparse.ArgumentTypeError(f"Metodo invalido: {value}. Validos: {valid}")
    return value


def process_video_once(
    *,
    run_index: int,
    input_path: Path,
    output_dir: Path,
    method_key: str,
    processor,
    codec: str,
    max_frames: int | None,
    merge_audio: bool,
    show_progress: bool,
) -> RunMeasurement:
    try:
        import cv2
    except ImportError as exc:
        raise RuntimeError("Falta OpenCV. Instalalo con: conda install opencv") from exc

    info = video_info(input_path)
    if info.width <= 0 or info.height <= 0:
        raise RuntimeError("No se pudo detectar la resolucion del video")
    if info.fps <= 0:
        raise RuntimeError("No se pudo detectar el FPS del video")

    output_path = output_video_path(output_dir, method_key)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(input_path))
    if not cap.isOpened():
        raise RuntimeError(f"No se pudo abrir el video: {input_path}")

    fourcc = cv2.VideoWriter_fourcc(*codec)
    writer = cv2.VideoWriter(str(output_path), fourcc, info.fps, (info.width, info.height))
    if not writer.isOpened():
        cap.release()
        raise RuntimeError(f"No se pudo crear el video de salida: {output_path}")

    frames = 0
    read_s = 0.0
    filter_s = 0.0
    filter_compute_s = 0.0
    write_s = 0.0
    transfer_h2d_s = 0.0
    transfer_d2h_s = 0.0
    checksum = 0
    hasher = frame_hash()

    try:
        while max_frames is None or frames < max_frames:
            read_start = perf_counter()
            ok, frame = cap.read()
            read_s += perf_counter() - read_start
            if not ok:
                break

            out_frame, timing = processor.process(frame)
            filter_s += timing.filter_s
            filter_compute_s += timing.compute_s
            if timing.transfer_h2d_s is not None:
                transfer_h2d_s += timing.transfer_h2d_s
                transfer_d2h_s += timing.transfer_d2h_s or 0.0

            # Datos de control fuera de la medicion de lectura/filtro/escritura.
            checksum += int(np.sum(out_frame, dtype=np.uint64))
            hasher.update(out_frame.tobytes())

            write_start = perf_counter()
            writer.write(out_frame)
            write_s += perf_counter() - write_start

            frames += 1
            if show_progress and (frames == 1 or frames % 30 == 0):
                print(
                    f"[Progreso] {METHOD_LABELS[method_key]} corrida {run_index}: {frames} frames",
                    flush=True,
                )

            del frame
            del out_frame
    finally:
        cap.release()
        writer.release()

    pipeline_total_s = read_s + filter_s + write_s
    effective_fps = frames / pipeline_total_s if pipeline_total_s > 0 else 0.0

    audio_merge_s = None
    audio_path = ""
    if merge_audio:
        audio_output = output_video_with_audio_path(output_dir, method_key)
        audio_merge_s = merge_audio_with_ffmpeg(input_path, output_path, audio_output)
        audio_path = str(audio_output)

    return RunMeasurement(
        run_index=run_index,
        frames=frames,
        read_s=read_s,
        filter_s=filter_s,
        filter_compute_s=filter_compute_s,
        write_s=write_s,
        pipeline_total_s=pipeline_total_s,
        effective_fps=effective_fps,
        transfer_h2d_s=transfer_h2d_s if transfer_h2d_s > 0.0 else None,
        transfer_d2h_s=transfer_d2h_s if transfer_d2h_s > 0.0 else None,
        transfer_total_s=(transfer_h2d_s + transfer_d2h_s) if transfer_h2d_s > 0.0 else None,
        audio_merge_s=audio_merge_s,
        peak_rss_mb=peak_rss_mb(),
        checksum=checksum,
        output_hash=hasher.hexdigest()[:16],
        output_video_path=str(output_path),
        output_video_with_audio_path=audio_path,
    )


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    default_input = base_dir.parent / "15785079_2160_3840_30fps.mp4"
    default_output_dir = base_dir.parent / "resultados"

    parser = argparse.ArgumentParser(
        description="Procesa un video 4K con posterize y guarda benchmark parcial por metodo.",
    )
    parser.add_argument("--method", type=parse_method, required=True, help="secuencial, pytorch_cpu o pytorch_gpu")
    parser.add_argument("--input", type=Path, default=default_input, help="Video de entrada.")
    parser.add_argument("--output-dir", type=Path, default=default_output_dir, help="Carpeta de resultados.")
    parser.add_argument("--runs", type=int, default=3, help="Cantidad de corridas para promediar.")
    parser.add_argument(
        "--workers",
        type=int,
        default=os.cpu_count() or 1,
        help="Hilos para PyTorch CPU. No afecta secuencial ni PyTorch GPU.",
    )
    parser.add_argument("--codec", default="mp4v", help="Codec OpenCV de 4 caracteres. Default: mp4v.")
    parser.add_argument(
        "--max-frames",
        type=int,
        default=None,
        help="Procesa solo los primeros N frames. Usar solo para pruebas, no para el benchmark final.",
    )
    parser.add_argument(
        "--merge-audio",
        action="store_true",
        help="Reincorpora audio con ffmpeg al terminar cada corrida. Ese tiempo se registra aparte.",
    )
    parser.add_argument("--no-progress", action="store_true", help="Oculta mensajes de progreso por frame.")
    args = parser.parse_args()

    if args.runs < 1:
        raise SystemExit("--runs debe ser >= 1")
    if len(args.codec) != 4:
        raise SystemExit("--codec debe tener exactamente 4 caracteres, por ejemplo mp4v")
    if args.max_frames is not None and args.max_frames < 1:
        raise SystemExit("--max-frames debe ser >= 1")

    input_path = args.input.resolve()
    output_dir = args.output_dir.resolve()
    info = video_info(input_path)
    env = environment_info()
    processor = build_processor(args.method, workers=args.workers)

    measurements: list[RunMeasurement] = []
    try:
        for run_index in range(1, args.runs + 1):
            print(f"[Progreso] Iniciando {METHOD_LABELS[args.method]} corrida {run_index}/{args.runs}", flush=True)
            measurement = process_video_once(
                run_index=run_index,
                input_path=input_path,
                output_dir=output_dir,
                method_key=args.method,
                processor=processor,
                codec=args.codec,
                max_frames=args.max_frames,
                merge_audio=args.merge_audio,
                show_progress=not args.no_progress,
            )
            measurements.append(measurement)
            print(
                f"[Progreso] Finalizada corrida {run_index}: "
                f"{measurement.frames} frames, {measurement.pipeline_total_s:.3f} s",
                flush=True,
            )
    except Exception as exc:
        row = average_measurements(
            args.method,
            args.runs,
            getattr(processor, "workers", args.workers),
            input_path,
            info,
            args.codec,
            args.max_frames,
            measurements,
            status="error",
            error=str(exc),
        )
    else:
        row = average_measurements(
            args.method,
            args.runs,
            getattr(processor, "workers", args.workers),
            input_path,
            info,
            args.codec,
            args.max_frames,
            measurements,
        )

    all_rows = update_csv(csv_path(output_dir), row)
    write_results_md(
        partial_md_path(output_dir, args.method),
        f"Resultado parcial TP4 posterize - {METHOD_LABELS[args.method]}",
        [row],
        env,
        all_rows_for_speedup=all_rows,
    )
    write_results_md(
        output_dir / "resultados_video4k.md",
        "Resultados TP4 posterize",
        all_rows,
        env,
        all_rows_for_speedup=all_rows,
    )

    print(f"CSV actualizado: {csv_path(output_dir)}")
    print(f"Markdown parcial: {partial_md_path(output_dir, args.method)}")
    print(f"Markdown agregado: {output_dir / 'resultados_video4k.md'}")
    if row.status != "ok":
        raise SystemExit(f"Benchmark finalizado con error: {row.error}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.", file=sys.stderr)
        raise SystemExit(130)
