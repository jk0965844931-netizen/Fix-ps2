import configparser
from pathlib import Path

from tools.ipsx2_optimize_config import apply_settings, load_config, main, SMOOTH_PRESET


def test_apply_settings_adds_performance_sections_and_preserves_case():
    config = configparser.ConfigParser(interpolation=None)
    config.optionxform = str

    changes = apply_settings(config, SMOOTH_PRESET)

    assert changes
    assert config.get("GS", "Renderer") == "Metal"
    assert config.get("GS", "upscale_multiplier") == "1"
    assert config.get("EmuCore/Speedhacks", "MTVU") == "true"
    assert "upscale_multiplier" in config["GS"]


def test_apply_settings_clamps_invalid_numeric_values():
    config = configparser.ConfigParser(interpolation=None)
    config.optionxform = str
    config.add_section("GS")
    config.set("GS", "upscale_multiplier", "99")
    config.add_section("SPU2/Output")
    config.set("SPU2/Output", "OutputLatencyMS", "broken")

    apply_settings(config, {"GS": {"Renderer": "Metal"}, "SPU2/Output": {}})

    assert config.get("GS", "upscale_multiplier") == "6"
    assert config.get("SPU2/Output", "OutputLatencyMS") == "20"


def test_cli_writes_atomically_and_creates_backup(tmp_path: Path):
    config_path = tmp_path / "PCSX2.ini"
    config_path.write_text("[GS]\nupscale_multiplier = 4\n", encoding="utf-8")

    assert main([str(config_path), "--preset", "smooth"]) == 0

    optimized = load_config(config_path)
    assert optimized.get("GS", "Renderer") == "Metal"
    assert optimized.get("GS", "upscale_multiplier") == "1"
    assert config_path.with_suffix(".ini.bak").exists()
