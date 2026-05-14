#pragma once

#include <array>
#include <string_view>

struct IPSX2DefaultSetting {
  std::string_view section;
  std::string_view key;
  std::string_view value;
};

// The full PCSX2/iPSX2 engine is not vendored in this repository. Keep the
// runtime defaults mirrored with tools/ipsx2_optimize_config.py so the unsigned
// iOS shell advertises the same safe FPS/stability recommendations that the CLI
// applies to real emulator configurations.
constexpr std::array<IPSX2DefaultSetting, 18> kIPSX2SmoothDefaults{{
    {"EmuCore/Speedhacks", "EnableSpeedHacks", "true"},
    {"EmuCore/Speedhacks", "EECycleRate", "1"},
    {"EmuCore/Speedhacks", "EECycleSkip", "0"},
    {"EmuCore/Speedhacks", "vuThread", "true"},
    {"EmuCore/Speedhacks", "InstantVU1", "true"},
    {"EmuCore/Speedhacks", "MTVU", "true"},
    {"EmuCore/CPU", "AffinityControlMode", "1"},
    {"EmuCore/CPU", "EnableFastmem", "true"},
    {"EmuCore/GS", "VsyncEnable", "false"},
    {"EmuCore/GS", "FrameLimitEnable", "true"},
    {"EmuCore/GS", "OptimalFramePacing", "true"},
    {"GS", "Renderer", "Metal"},
    {"GS", "upscale_multiplier", "1"},
    {"GS", "mipmap_hw", "0"},
    {"GS", "accurate_blending_unit", "0"},
    {"GS", "accurate_date", "false"},
    {"SPU2/Output", "OutputLatencyMS", "80"},
    {"SPU2/Output", "SynchMode", "1"},
}};
