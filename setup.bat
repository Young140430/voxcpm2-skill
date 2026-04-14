@echo off
:: VoxCPM TTS 一键安装脚本 (Windows)
echo [VoxCPM] 检查 Python 版本...
python --version 2>nul || (
    echo [VoxCPM] 错误: 未找到 Python，请安装 Python 3.10+
    echo [VoxCPM] 下载地址: https://www.python.org/downloads/
    exit /b 1
)

:: 检查版本 >= 3.10
for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo [VoxCPM] Python 版本: %PYVER%

echo [VoxCPM] 安装依赖...
pip install aiohttp -q
echo [VoxCPM] 安装完成!
echo.
echo 使用方法:
echo   python voxcpm_tts.py "你好，欢迎使用语音合成"
echo   python voxcpm_tts.py "Hello" --prompt ref.wav --prompt-text "参考文本"
