"""Funciones compartidas para el benchmark de Sobel."""

import csv
import hashlib
import os
import platform
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Iterable


VALID_SIZES = (750, 1500, 3000, 6000)
METHOD_LABELS = {
    "secuencial": "secuencial",
    "numpy": "NumPy",
    "numba_cpu": "Numba paralelo CPU",
}


@dataclass
class RunMeasurement:
    run_index: int
    rgb_to_gray_s: float
    sobel_s: float
    total_s: float
    white_pixels: int
    total_pixels: int
    white_percent: float
    checksum: int
    output_hash: str


@dataclass
class SummaryRow:
    timestamp: str
    method_key: str
    method_label: str
    size: int
    runs: int
    workers: int
    seed: int
    rgb_to_gray_s: float | None
    sobel_s: float | None
    total_s: float | None
    white_percent: float | None
    white_pixels: int | None
    total_pixels: int | None
    checksum: int | None
    output_hash: str | None
    status: str
    error: str


CSV_FIELDS = [
    "timestamp",
    "method_key",
    "method_label",
    "size",
    "runs",
    "workers",
    "seed",
    "rgb_to_gray_s",
    "sobel_s",
    "total_s",
    "white_percent",
    "white_pixels",
    "total_pixels",
    "checksum",
    "output_hash",
    "status",
    "error",
]


def parse_method_list(raw: str) -> list[str]:
    methods = [item.strip() for item in raw.split(",") if item.strip()]
    if not methods:
        raise ValueError("Debes indicar al menos un metodo")
    invalid = [m for m in methods if m not in METHOD_LABELS]
    if invalid:
        valid = ", ".join(METHOD_LABELS)
        raise ValueError(f"Metodo invalido: {', '.join(invalid)}. Validos: {valid}")
    return methods


def validate_size(value: str | int) -> int:
    size = int(value)
    if size <= 0:
        raise ValueError("--size debe ser positivo")
    return size


def build_synthetic_rgb(size: int, seed: int) -> bytes:
    """Genera una imagen RGB reproducible usando solo tipos basicos de Python."""
    width = size
    height = size
    row_stride = width * 3
    rgb = bytearray(height * row_stride)

    base_pixel = bytes(((18 + seed) & 255, (24 + seed // 3) & 255, (31 + seed // 7) & 255))
    base_row = base_pixel * width
    for row in range(height):
        row_start = row * row_stride
        rgb[row_start : row_start + row_stride] = base_row

    center_x = width // 2
    center_y = height // 2
    rect_top = height // 5
    rect_bottom = height // 2
    rect_left = width // 7
    rect_right = width // 3
    band_left = (2 * width) // 3
    band_right = min(width, band_left + max(width // 18, 1))

    rect_row = bytes((245, 35, 45)) * max(rect_right - rect_left, 0)
    for row in range(rect_top, rect_bottom):
        start = row * row_stride + rect_left * 3
        rgb[start : start + len(rect_row)] = rect_row

    band_row = bytes((25, 235, 250)) * max(band_right - band_left, 0)
    for row in range(height):
        start = row * row_stride + band_left * 3
        rgb[start : start + len(band_row)] = band_row

    square_half = max(size // 9, 1)
    square_top = max(center_y - square_half, 0)
    square_bottom = min(center_y + square_half, height)
    square_left = max(center_x - square_half, 0)
    square_right = min(center_x + square_half, width)
    square_row = bytes((255, 255, 245)) * max(square_right - square_left, 0)
    for row in range(square_top, square_bottom):
        start = row * row_stride + square_left * 3
        rgb[start : start + len(square_row)] = square_row

    line_width = max(size // 120, 1)
    line_pixel = bytes((250, 250, 40))
    for row in range(height):
        col = (row * width) // height
        left = max(col - line_width, 0)
        right = min(col + line_width, width)
        if left < right:
            start = row * row_stride + left * 3
            rgb[start : start + (right - left) * 3] = line_pixel * (right - left)

    return bytes(rgb)


def output_metrics(output: object) -> tuple[int, int, float, int, str]:
    """Devuelve white_pixels, total_pixels, white_percent, checksum y hash corto."""
    if hasattr(output, "tobytes"):
        raw = output.tobytes()
    else:
        raw = bytes(output)

    total_pixels = len(raw)
    white_pixels = raw.count(255)
    checksum = sum(raw)
    white_percent = (white_pixels / total_pixels) * 100.0 if total_pixels else 0.0
    output_hash = hashlib.sha256(raw).hexdigest()[:16]
    return white_pixels, total_pixels, white_percent, checksum, output_hash


def average_measurements(
    method_key: str,
    size: int,
    runs: int,
    workers: int,
    seed: int,
    measurements: list[RunMeasurement],
    status: str = "ok",
    error: str = "",
) -> SummaryRow:
    timestamp = datetime.now().isoformat(timespec="seconds")
    label = METHOD_LABELS[method_key]
    if not measurements:
        return SummaryRow(
            timestamp=timestamp,
            method_key=method_key,
            method_label=label,
            size=size,
            runs=runs,
            workers=workers,
            seed=seed,
            rgb_to_gray_s=None,
            sobel_s=None,
            total_s=None,
            white_percent=None,
            white_pixels=None,
            total_pixels=None,
            checksum=None,
            output_hash=None,
            status=status,
            error=error,
        )

    n = len(measurements)
    rgb_to_gray_s = sum(m.rgb_to_gray_s for m in measurements) / n
    sobel_s = sum(m.sobel_s for m in measurements) / n
    total_s = sum(m.total_s for m in measurements) / n
    white_percent = sum(m.white_percent for m in measurements) / n
    last = measurements[-1]
    return SummaryRow(
        timestamp=timestamp,
        method_key=method_key,
        method_label=label,
        size=size,
        runs=runs,
        workers=workers,
        seed=seed,
        rgb_to_gray_s=rgb_to_gray_s,
        sobel_s=sobel_s,
        total_s=total_s,
        white_percent=white_percent,
        white_pixels=last.white_pixels,
        total_pixels=last.total_pixels,
        checksum=last.checksum,
        output_hash=last.output_hash,
        status=status,
        error=error,
    )


def cpu_model() -> str:
    cpuinfo = Path("/proc/cpuinfo")
    if cpuinfo.exists():
        for line in cpuinfo.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.lower().startswith("model name"):
                return line.split(":", 1)[1].strip()
    return platform.processor() or "no detectado"


def cpu_physical_cores() -> str:
    cpuinfo = Path("/proc/cpuinfo")
    if not cpuinfo.exists():
        return "no detectado"

    physical_core_pairs: set[tuple[str, str]] = set()
    current_physical = ""
    current_core = ""
    for line in cpuinfo.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line.strip():
            if current_physical and current_core:
                physical_core_pairs.add((current_physical, current_core))
            current_physical = ""
            current_core = ""
            continue
        if line.startswith("physical id"):
            current_physical = line.split(":", 1)[1].strip()
        elif line.startswith("core id"):
            current_core = line.split(":", 1)[1].strip()

    if current_physical and current_core:
        physical_core_pairs.add((current_physical, current_core))

    if physical_core_pairs:
        return str(len(physical_core_pairs))
    return "no detectado"


def ram_info() -> str:
    meminfo = Path("/proc/meminfo")
    if not meminfo.exists():
        return "no detectada"

    values: dict[str, int] = {}
    for line in meminfo.read_text(encoding="utf-8", errors="ignore").splitlines():
        match = re.match(r"^(MemTotal|MemAvailable):\s+(\d+)\s+kB", line)
        if match:
            values[match.group(1)] = int(match.group(2))

    def gib(kb: int) -> float:
        return kb / (1024 * 1024)

    total = values.get("MemTotal")
    available = values.get("MemAvailable")
    if total is None:
        return "no detectada"
    if available is None:
        return f"{gib(total):.2f} GiB total"
    return f"{gib(total):.2f} GiB total, {gib(available):.2f} GiB disponible"


def package_version(package_name: str) -> str:
    try:
        return version(package_name)
    except PackageNotFoundError:
        return "no disponible"
    except Exception:
        return "sin dato"


def environment_info() -> dict[str, str]:
    gil_value = getattr(sys, "_is_gil_enabled", lambda: "sin dato")()
    return {
        "cpu_model": cpu_model(),
        "cpu_physical_cores": cpu_physical_cores(),
        "cpu_logical_cores": str(os.cpu_count() or "no detectado"),
        "ram": ram_info(),
        "os": platform.platform(),
        "python": sys.version.replace("\n", " "),
        "gil_enabled": str(gil_value),
        "numpy": package_version("numpy"),
        "numba": package_version("numba"),
    }


def csv_path_for_size(output_dir: Path, size: int) -> Path:
    return output_dir / f"resultados_sobel_{size}x{size}.csv"


def aggregate_md_path_for_size(output_dir: Path, size: int) -> Path:
    return output_dir / f"resultados_sobel_{size}x{size}.md"


def partial_md_path(output_dir: Path, size: int, method_key: str) -> Path:
    return output_dir / "parciales" / f"resultado_parcial_{size}x{size}_{method_key}.md"


def final_md_path(output_dir: Path, method_key: str) -> Path:
    return output_dir / "finales" / f"resultado_final_{method_key}.md"


def _summary_to_csv_row(row: SummaryRow) -> dict[str, str]:
    return {
        "timestamp": row.timestamp,
        "method_key": row.method_key,
        "method_label": row.method_label,
        "size": str(row.size),
        "runs": str(row.runs),
        "workers": str(row.workers),
        "seed": str(row.seed),
        "rgb_to_gray_s": f"{row.rgb_to_gray_s:.9f}" if row.rgb_to_gray_s is not None else "",
        "sobel_s": f"{row.sobel_s:.9f}" if row.sobel_s is not None else "",
        "total_s": f"{row.total_s:.9f}" if row.total_s is not None else "",
        "white_percent": f"{row.white_percent:.9f}" if row.white_percent is not None else "",
        "white_pixels": str(row.white_pixels) if row.white_pixels is not None else "",
        "total_pixels": str(row.total_pixels) if row.total_pixels is not None else "",
        "checksum": str(row.checksum) if row.checksum is not None else "",
        "output_hash": row.output_hash or "",
        "status": row.status,
        "error": row.error,
    }


def _csv_row_to_summary(row: dict[str, str]) -> SummaryRow:
    def f(value: str) -> float | None:
        return float(value) if value.strip() else None

    def i(value: str) -> int | None:
        return int(value) if value.strip() else None

    method_key = row["method_key"]
    return SummaryRow(
        timestamp=row.get("timestamp", ""),
        method_key=method_key,
        method_label=row.get("method_label", METHOD_LABELS.get(method_key, method_key)),
        size=int(row["size"]),
        runs=int(row["runs"]),
        workers=int(row.get("workers", "1") or "1"),
        seed=int(row.get("seed", "2026") or "2026"),
        rgb_to_gray_s=f(row.get("rgb_to_gray_s", "")),
        sobel_s=f(row.get("sobel_s", "")),
        total_s=f(row.get("total_s", "")),
        white_percent=f(row.get("white_percent", "")),
        white_pixels=i(row.get("white_pixels", "")),
        total_pixels=i(row.get("total_pixels", "")),
        checksum=i(row.get("checksum", "")),
        output_hash=row.get("output_hash", "") or None,
        status=row.get("status", "ok"),
        error=row.get("error", ""),
    )


def load_csv_rows(csv_path: Path) -> list[SummaryRow]:
    if not csv_path.exists():
        return []
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [_csv_row_to_summary(row) for row in reader]


def load_all_result_rows(output_dir: Path) -> list[SummaryRow]:
    rows: list[SummaryRow] = []
    for size in VALID_SIZES:
        rows.extend(load_csv_rows(csv_path_for_size(output_dir, size)))
    rows.sort(key=lambda row: (row.size, row.method_key))
    return rows


def write_csv_rows(csv_path: Path, rows: Iterable[SummaryRow]) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(_summary_to_csv_row(row))


def update_aggregate_rows(csv_path: Path, new_rows: list[SummaryRow]) -> list[SummaryRow]:
    old_rows = load_csv_rows(csv_path)
    replacement_keys = {row.method_key for row in new_rows}
    kept = [row for row in old_rows if row.method_key not in replacement_keys]
    combined = kept + new_rows
    order = {"secuencial": 0, "numpy": 1, "numba_cpu": 2}
    combined.sort(key=lambda row: order.get(row.method_key, 99))
    write_csv_rows(csv_path, combined)
    return combined


def speedup_and_performance(rows: list[SummaryRow]) -> dict[str, tuple[float | None, float | None]]:
    baseline_by_size: dict[int, float] = {}
    for row in rows:
        if row.method_key == "secuencial" and row.status == "ok" and row.total_s:
            baseline_by_size[row.size] = row.total_s

    out: dict[str, tuple[float | None, float | None]] = {}
    for row in rows:
        speedup = None
        performance = None
        baseline = baseline_by_size.get(row.size)
        if baseline and row.status == "ok" and row.total_s and row.total_s > 0:
            speedup = baseline / row.total_s
            units = row.workers if row.method_key == "numba_cpu" else 1
            if units > 0:
                performance = (speedup / units) * 100.0
        out[f"{row.method_key}:{row.size}"] = (speedup, performance)
    return out


def format_float(value: float | None, digits: int = 6) -> str:
    if value is None:
        return ""
    return f"{value:.{digits}f}"


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def write_results_md(
    md_path: Path,
    title: str,
    rows: list[SummaryRow],
    measurements_by_method: dict[str, list[RunMeasurement]] | None,
    env: dict[str, str],
    *,
    aggregate_rows_for_speedup: list[SummaryRow] | None = None,
) -> None:
    md_path.parent.mkdir(parents=True, exist_ok=True)
    speed_rows = aggregate_rows_for_speedup if aggregate_rows_for_speedup is not None else rows
    speed_data = speedup_and_performance(speed_rows)

    lines: list[str] = [
        f"# {title}",
        "",
        "## Entorno",
        "",
        f"- CPU: {env['cpu_model']}",
        f"- Nucleos fisicos: {env['cpu_physical_cores']}",
        f"- Nucleos logicos: {env['cpu_logical_cores']}",
        f"- RAM: {env['ram']}",
        f"- Sistema operativo: {env['os']}",
        f"- Python: {env['python']}",
        f"- GIL habilitado: {env['gil_enabled']}",
        f"- NumPy: {env['numpy']}",
        f"- Numba: {env['numba']}",
        "",
        "## Tabla solicitada",
        "",
        "| metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]

    for row in rows:
        speedup, performance = speed_data.get(f"{row.method_key}:{row.size}", (None, None))
        lines.append(
            "| "
            + " | ".join(
                [
                    md_escape(row.method_label),
                    format_float(row.rgb_to_gray_s),
                    format_float(row.sobel_s),
                    format_float(row.total_s),
                    format_float(row.white_percent),
                    format_float(speedup),
                    format_float(performance),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Datos de control",
            "",
            "| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---|---|",
        ]
    )

    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    md_escape(row.method_label),
                    f"{row.size}x{row.size}",
                    str(row.runs),
                    str(row.workers),
                    str(row.seed),
                    str(row.white_pixels or ""),
                    str(row.total_pixels or ""),
                    str(row.checksum or ""),
                    row.output_hash or "",
                    md_escape(row.status),
                ]
            )
            + " |"
        )

    if measurements_by_method:
        lines.extend(["", "## Detalle de corridas", ""])
        for method_key, measurements in measurements_by_method.items():
            if not measurements:
                continue
            method_label = METHOD_LABELS[method_key]
            lines.extend(
                [
                    f"### {method_label}",
                    "",
                    "| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |",
                    "|---:|---:|---:|---:|---:|---:|---|",
                ]
            )
            for m in measurements:
                lines.append(
                    "| "
                    + " | ".join(
                        [
                            str(m.run_index),
                            format_float(m.rgb_to_gray_s),
                            format_float(m.sobel_s),
                            format_float(m.total_s),
                            format_float(m.white_percent),
                            str(m.checksum),
                            m.output_hash,
                        ]
                    )
                    + " |"
                )
            lines.append("")

    lines.extend(
        [
            "## Notas",
            "",
            "- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.",
            "- La imagen de entrada es sintetica y reproducible: mismo tamanio y seed producen los mismos pixeles.",
            "- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.",
            "- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.",
            "- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.",
            "",
        ]
    )

    md_path.write_text("\n".join(lines), encoding="utf-8")


def partial_environment_lines(output_dir: Path, method_key: str, rows: list[SummaryRow]) -> list[str] | None:
    for row in rows:
        partial_path = partial_md_path(output_dir, row.size, method_key)
        if not partial_path.exists():
            continue
        source_lines = partial_path.read_text(encoding="utf-8").splitlines()
        try:
            start = source_lines.index("## Entorno")
            end = source_lines.index("## Tabla solicitada")
        except ValueError:
            continue
        env_lines = source_lines[start + 1 : end]
        while env_lines and env_lines[0] == "":
            env_lines.pop(0)
        while env_lines and env_lines[-1] == "":
            env_lines.pop()
        if env_lines:
            return env_lines
    return None


def write_method_final_md(
    output_dir: Path,
    method_key: str,
    env: dict[str, str],
) -> Path | None:
    """Genera resultados/finales/resultado_final_<metodo>.md usando todos los CSV disponibles."""
    all_rows = load_all_result_rows(output_dir)
    method_rows = [row for row in all_rows if row.method_key == method_key and row.status == "ok"]
    method_rows.sort(key=lambda row: row.size)
    if not method_rows:
        return None

    md_path = final_md_path(output_dir, method_key)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    speed_data = speedup_and_performance(all_rows)
    method_label = METHOD_LABELS.get(method_key, method_key)

    base_row = method_rows[0]
    base_size = base_row.size
    base_normalized = float(base_row.white_pixels or 0)
    env_lines = partial_environment_lines(output_dir, method_key, method_rows)

    lines: list[str] = [
        f"# Resultado final parcial - Sobel {method_label}",
        "",
        f"Este documento junta los resultados parciales del metodo **{method_label}** para los tamanios disponibles.",
        "",
        "## Entorno",
        "",
    ]

    if env_lines:
        lines.extend(env_lines)
    else:
        lines.extend(
            [
                f"- CPU: {env['cpu_model']}",
                f"- Nucleos fisicos: {env['cpu_physical_cores']}",
                f"- Nucleos logicos: {env['cpu_logical_cores']}",
                f"- RAM registrada al generar este archivo: {env['ram']}",
                f"- Sistema operativo: {env['os']}",
                f"- Python: {env['python']}",
                f"- GIL habilitado: {env['gil_enabled']}",
                f"- NumPy: {env['numpy']}",
                f"- Numba: {env['numba']}",
            ]
        )

    lines.extend(
        [
            "",
            "## Tabla consolidada",
            "",
            "| tamanio | metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |",
            "|---:|---|---:|---:|---:|---:|---:|---:|",
        ]
    )

    for row in method_rows:
        speedup, performance = speed_data.get(f"{row.method_key}:{row.size}", (None, None))
        lines.append(
            "| "
            + " | ".join(
                [
                    f"{row.size}x{row.size}",
                    md_escape(row.method_label),
                    format_float(row.rgb_to_gray_s),
                    format_float(row.sobel_s),
                    format_float(row.total_s),
                    format_float(row.white_percent),
                    format_float(speedup),
                    format_float(performance),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Datos de control",
            "",
            "| tamanio | corridas | workers/hilos | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |",
            "|---:|---:|---:|---:|---:|---:|---|---|",
        ]
    )

    for row in method_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"{row.size}x{row.size}",
                    str(row.runs),
                    str(row.workers),
                    str(row.white_pixels or ""),
                    str(row.total_pixels or ""),
                    str(row.checksum or ""),
                    row.output_hash or "",
                    md_escape(row.status),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Blancos normalizados por escala",
            "",
            "Esta tabla compara la cantidad de pixeles blancos teniendo en cuenta que los contornos crecen",
            "principalmente como lineas. Por eso se normaliza por el crecimiento del lado de la imagen respecto",
            f"de `{base_size}x{base_size}`.",
            "",
            f"| tamanio | factor de lado vs {base_size} | pixeles blancos | blancos normalizados | indice vs {base_size} (%) |",
            "|---:|---:|---:|---:|---:|",
        ]
    )

    for row in method_rows:
        factor = row.size / base_size if base_size else 0.0
        white_pixels = float(row.white_pixels or 0)
        normalized = white_pixels / factor if factor else None
        index = (normalized / base_normalized * 100.0) if normalized is not None and base_normalized else None
        lines.append(
            "| "
            + " | ".join(
                [
                    f"{row.size}x{row.size}",
                    format_float(factor, 2),
                    str(row.white_pixels or ""),
                    format_float(normalized, 2),
                    format_float(index, 2),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Conclusiones",
            "",
        ]
    )

    if len(method_rows) >= 2:
        first = method_rows[0]
        last = method_rows[-1]
        lines.extend(
            [
                f"El metodo **{method_label}** fue ejecutado para {len(method_rows)} tamanios. "
                f"El tiempo total promedio pasa de {format_float(first.total_s)} s en `{first.size}x{first.size}` "
                f"a {format_float(last.total_s)} s en `{last.size}x{last.size}`.",
                "",
            ]
        )
    else:
        only = method_rows[0]
        lines.extend(
            [
                f"Hasta ahora solo hay resultados de **{method_label}** para `{only.size}x{only.size}`. "
                "Cuando se agreguen mas tamanios, esta seccion permitira comparar la evolucion.",
                "",
            ]
        )

    lines.extend(
        [
            "El porcentaje de pixeles blancos sobre el total de la imagen puede disminuir cuando aumenta la resolucion.",
            "Esa baja no significa necesariamente peor deteccion: el total de pixeles crece como area, mientras que",
            "los contornos crecen principalmente como lineas.",
            "",
            "La tabla de blancos normalizados permite comparar de forma mas equitativa. Si los valores normalizados",
            f"quedan cerca del valor base de `{base_size}x{base_size}`, la deteccion de contornos se mantiene estable",
            "al escalar la imagen.",
            "",
            "Los checksums y hashes sirven como control de reproducibilidad: para una misma entrada sintetica, mismo",
            "metodo y mismo tamanio, deberian mantenerse constantes entre corridas.",
            "",
            "## Archivos parciales esperados",
            "",
        ]
    )

    for row in method_rows:
        lines.append(f"- `parciales/resultado_parcial_{row.size}x{row.size}_{method_key}.md`")

    md_path.write_text("\n".join(lines), encoding="utf-8")
    return md_path
