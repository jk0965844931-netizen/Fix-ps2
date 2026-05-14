#!/usr/bin/env python3
"""Apply safe iPSX2/PCSX2 configuration defaults for smoother iOS gameplay.

The tool edits an INI-style settings file in place, keeps a backup by default,
and writes atomically to avoid corrupting settings if the process is interrupted.
It intentionally avoids game-specific patches; the defaults reduce expensive
rendering and overlay work while enabling conservative speed-hack settings that
can be reverted by restoring the backup file.
"""
from __future__ import annotations

import argparse
import configparser
import os
import shutil
import tempfile
from pathlib import Path
from typing import Dict, Iterable, Tuple

SettingMap = Dict[str, Dict[str, str]]

# Conservative defaults: prefer stable performance gains over compatibility-risky
# hacks. Values are stored as strings because PCSX2/iPSX2 settings are INI-backed.
SMOOTH_PRESET: SettingMap = {
    "EmuCore/Speedhacks": {
        "EnableSpeedHacks": "true",
        "EECycleRate": "1",
        "EECycleSkip": "0",
        "vuThread": "true",
        "InstantVU1": "true",
        "MTVU": "true",
    },
    "EmuCore/CPU": {
        "AffinityControlMode": "1",
        "EnableFastmem": "true",
    },
    "EmuCore/GS": {
        "VsyncEnable": "false",
        "FrameLimitEnable": "true",
        "OptimalFramePacing": "true",
    },
    "GS": {
        "Renderer": "Metal",
        "upscale_multiplier": "1",
        "mipmap_hw": "0",
        "accurate_blending_unit": "0",
        "accurate_date": "false",
        "crc_hack_level": "1",
        "texture_preloading": "0",
        "OsdShowFPS": "true",
        "OsdShowSpeed": "false",
        "OsdShowCPU": "false",
        "OsdShowGPU": "false",
        "OsdShowFrameTimes": "false",
        "OsdShowResolution": "false",
    },
    "SPU2/Output": {
        "OutputLatencyMS": "80",
        "SynchMode": "1",
    },
}

BATTERY_PRESET: SettingMap = {
    **SMOOTH_PRESET,
    "EmuCore/Speedhacks": {
        **SMOOTH_PRESET["EmuCore/Speedhacks"],
        "EECycleRate": "2",
    },
    "GS": {
        **SMOOTH_PRESET["GS"],
        "OsdShowFPS": "false",
    },
}

QUALITY_PRESET: SettingMap = {
    **SMOOTH_PRESET,
    "EmuCore/Speedhacks": {
        **SMOOTH_PRESET["EmuCore/Speedhacks"],
        "EECycleRate": "0",
        "InstantVU1": "false",
    },
    "GS": {
        **SMOOTH_PRESET["GS"],
        "mipmap_hw": "1",
        "accurate_blending_unit": "1",
        "OsdShowSpeed": "true",
    },
}

PRESETS: Dict[str, SettingMap] = {
    "smooth": SMOOTH_PRESET,
    "battery": BATTERY_PRESET,
    "quality": QUALITY_PRESET,
}

# Known numeric bounds. Clamping these prevents accidental UI/hand-edited values
# from causing stalls, extreme slowdowns, or invalid emulator state.
BOUNDS: Dict[Tuple[str, str], Tuple[int, int]] = {
    ("EmuCore/Speedhacks", "EECycleRate"): (0, 3),
    ("EmuCore/Speedhacks", "EECycleSkip"): (0, 3),
    ("GS", "upscale_multiplier"): (1, 6),
    ("SPU2/Output", "OutputLatencyMS"): (20, 250),
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Apply safe iPSX2/PCSX2 FPS and stability settings to an INI file."
    )
    parser.add_argument("config", type=Path, help="Path to the iPSX2/PCSX2 INI config file")
    parser.add_argument(
        "--preset",
        choices=sorted(PRESETS),
        default="smooth",
        help="Performance profile to apply (default: smooth)",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not create a .bak file before writing changes",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print changes without modifying the file",
    )
    return parser


def load_config(path: Path) -> configparser.ConfigParser:
    parser = configparser.ConfigParser(interpolation=None)
    parser.optionxform = str  # preserve existing key case used by PCSX2/iPSX2
    if path.exists():
        with path.open("r", encoding="utf-8") as handle:
            parser.read_file(handle)
    return parser


def iter_changes(config: configparser.ConfigParser, preset: SettingMap) -> Iterable[Tuple[str, str, str, str | None]]:
    for section, values in preset.items():
        for key, value in values.items():
            old_value = config.get(section, key, fallback=None)
            if old_value != value:
                yield section, key, value, old_value


def apply_settings(config: configparser.ConfigParser, preset: SettingMap) -> list[Tuple[str, str, str, str | None]]:
    changes = list(iter_changes(config, preset))
    for section, key, value, _old_value in changes:
        if not config.has_section(section):
            config.add_section(section)
        config.set(section, key, value)
    clamp_numeric_values(config)
    return changes


def clamp_numeric_values(config: configparser.ConfigParser) -> None:
    for (section, key), (minimum, maximum) in BOUNDS.items():
        if not config.has_option(section, key):
            continue
        raw = config.get(section, key)
        try:
            value = int(raw)
        except ValueError:
            value = minimum
        clamped = min(max(value, minimum), maximum)
        if str(clamped) != raw:
            config.set(section, key, str(clamped))


def write_atomic(config: configparser.ConfigParser, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent or Path(".")))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            config.write(handle)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        finally:
            raise


def backup_file(path: Path) -> Path | None:
    if not path.exists():
        return None
    backup_path = path.with_suffix(path.suffix + ".bak")
    shutil.copy2(path, backup_path)
    return backup_path


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = load_config(args.config)
    changes = apply_settings(config, PRESETS[args.preset])

    if args.dry_run:
        for section, key, value, old_value in changes:
            print(f"{section}.{key}: {old_value!r} -> {value!r}")
        print(f"{len(changes)} change(s) would be applied.")
        return 0

    backup_path = None if args.no_backup else backup_file(args.config)
    write_atomic(config, args.config)
    print(f"Applied {len(changes)} setting change(s) using '{args.preset}' preset: {args.config}")
    if backup_path:
        print(f"Backup written to: {backup_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
