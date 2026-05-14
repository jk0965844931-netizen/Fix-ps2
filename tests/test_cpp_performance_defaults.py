import re
from pathlib import Path

from tools.ipsx2_optimize_config import SMOOTH_PRESET


def test_cpp_smooth_defaults_match_python_optimizer_subset():
    header = Path("cpp/PerformanceDefaults.h").read_text(encoding="utf-8")
    cpp_defaults = {
        (section, key): value
        for section, key, value in re.findall(
            r'\{"([^"]+)",\s*"([^"]+)",\s*"([^"]+)"\}', header
        )
    }

    expected = {
        (section, key): value
        for section, values in SMOOTH_PRESET.items()
        for key, value in values.items()
        if (section, key) in cpp_defaults
    }

    assert cpp_defaults
    assert cpp_defaults == expected
