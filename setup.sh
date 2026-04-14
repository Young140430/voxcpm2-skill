#!/usr/bin/env bash
# VoxCPM TTS 一键安装脚本 (Linux/macOS)
set -e

echo "[VoxCPM] 检查 Python 版本..."
if ! command -v python3 &>/dev/null; then
    echo "[VoxCPM] 错误: 未找到 python3，请安装 Python 3.10+"
    exit 1
fi

PYVER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "[VoxCPM] Python 版本: $PYVER"

if python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)"; then
    echo "[VoxCPM] Python 版本满足要求"
else
    echo "[VoxCPM] 错误: 需要 Python >= 3.10，当前 $PYVER"
    exit 1
fi

echo "[VoxCPM] 安装依赖..."
python3 -m pip install aiohttp -q
echo "[VoxCPM] 安装完成!"
echo ""
echo "使用方法:"
echo "  python3 voxcpm_tts.py '你好，欢迎使用语音合成'"
echo "  python3 voxcpm_tts.py 'Hello' --prompt ref.wav --prompt-text '参考文本'"
