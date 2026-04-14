#!/usr/bin/env python3
"""
VoxCPM TTS Skill — 一行命令生成语音

用法:
  python voxcpm_tts.py "你好，欢迎使用语音合成"
  python voxcpm_tts.py "Hello world." --prompt prompt.wav --prompt-text "参考音频的文本"
  python voxcpm_tts.py "生成的内容" -o output.mp3 --cfg 3 --api http://localhost:8000

首次运行会自动安装依赖 (aiohttp)。
要求: Python >= 3.10
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import importlib
import shutil
import subprocess
import sys
from pathlib import Path

# ── 自动安装依赖 ──────────────────────────────────────────────
REQUIRED_PACKAGES = ["aiohttp"]


def _ensure_deps() -> None:
    missing = []
    for pkg in REQUIRED_PACKAGES:
        try:
            importlib.import_module(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"[VoxCPM] 正在安装缺失依赖: {', '.join(missing)} ...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", *missing, "-q"]
        )
        print("[VoxCPM] 依赖安装完成。")


_ensure_deps()

# ── 延迟导入 ──────────────────────────────────────────────────
import aiohttp  # noqa: E402

# ── 默认配置 ──────────────────────────────────────────────────
DEFAULT_API_BASE = "http://43.143.233.233:8000"
DEFAULT_CFG = 2
DEFAULT_OUTPUT = "output.mp3"


# ── 核心功能 ──────────────────────────────────────────────────
async def encode_latents(
    session: aiohttp.ClientSession,
    wav_path: Path,
    wav_format: str,
    api_base: str,
) -> dict:
    """将参考音频编码为 latents（可用于跨请求复用）"""
    wav_b64 = base64.b64encode(wav_path.read_bytes()).decode("utf-8")
    async with session.post(
        f"{api_base}/encode_latents",
        json={"wav_base64": wav_b64, "wav_format": wav_format},
    ) as resp:
        resp.raise_for_status()
        return await resp.json()


async def generate_mp3(
    session: aiohttp.ClientSession,
    payload: dict,
    out_path: Path,
    api_base: str,
) -> None:
    """调用 API 生成 MP3 并写入文件"""
    async with session.post(f"{api_base}/generate", json=payload) as resp:
        resp.raise_for_status()
        with out_path.open("wb") as f:
            async for chunk in resp.content.iter_chunked(64 * 1024):
                f.write(chunk)


async def run(
    text: str,
    output: Path,
    api_base: str,
    prompt_wav: Path | None,
    prompt_text: str | None,
    cfg: float,
) -> None:
    async with aiohttp.ClientSession() as session:
        # 构建 payload
        payload: dict = {
            "target_text": text,
            "cfg_value": cfg,
        }

        # 如果提供了参考音频
        if prompt_wav is not None:
            if not prompt_wav.exists():
                print(f"[VoxCPM] 错误: 参考音频文件不存在 → {prompt_wav}")
                sys.exit(1)

            wav_format = prompt_wav.suffix.lstrip(".") or "wav"
            print(f"[VoxCPM] 正在编码参考音频: {prompt_wav} ...")
            result = await encode_latents(session, prompt_wav, wav_format, api_base)
            latents_b64 = result["prompt_latents_base64"]

            if prompt_text:
                # prompted 模式: 提供参考音频 + 参考文本
                payload["prompt_latents_base64"] = latents_b64
                payload["prompt_text"] = prompt_text
            else:
                # zero-shot with ref: 只提供参考音频，不提供文本
                payload["ref_audio_latents_base64"] = latents_b64

        # 生成
        mode = "prompted" if prompt_wav and prompt_text else (
            "zero-shot (with ref audio)" if prompt_wav else "zero-shot"
        )
        print(f"[VoxCPM] 模式: {mode}")
        print(f"[VoxCPM] 目标文本: {text}")
        print(f"[VoxCPM] CFG: {cfg}")
        print(f"[VoxCPM] 正在生成语音 → {output} ...")

        await generate_mp3(session, payload, output, api_base)
        print(f"[VoxCPM] 完成! 文件已保存: {output.resolve()}")


# ── CLI 入口 ──────────────────────────────────────────────────
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="VoxCPM 语音合成 — 一行命令生成语音",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "你好，欢迎使用语音合成"
  %(prog)s "Hello world." -o hello.mp3
  %(prog)s "今天天气不错" --prompt ref.wav --prompt-text "参考音频的文字内容"
  %(prog)s "使用参考音色" --prompt ref.wav
  %(prog)s "自定义服务器" --api http://192.168.1.100:8000
        """,
    )
    p.add_argument("text", help="要合成的目标文本")
    p.add_argument("-o", "--output", default=DEFAULT_OUTPUT, help=f"输出文件路径 (默认: {DEFAULT_OUTPUT})")
    p.add_argument("--prompt", type=Path, default=None, help="参考音频文件路径 (WAV/MP3)")
    p.add_argument("--prompt-text", default=None, help="参考音频对应的文本内容（配合 --prompt 使用，提供则启用 prompted 模式）")
    p.add_argument("--cfg", type=float, default=DEFAULT_CFG, help=f"CFG 值 (默认: {DEFAULT_CFG})")
    p.add_argument("--api", default=DEFAULT_API_BASE, help=f"API 地址 (默认: {DEFAULT_API_BASE})")
    return p


def main() -> None:
    # Python 版本检查
    if sys.version_info < (3, 10):
        print(f"[VoxCPM] 错误: 需要 Python >= 3.10，当前版本 {sys.version}")
        sys.exit(1)

    args = build_parser().parse_args()
    output = Path(args.output)

    asyncio.run(
        run(
            text=args.text,
            output=output,
            api_base=args.api,
            prompt_wav=args.prompt,
            prompt_text=args.prompt_text,
            cfg=args.cfg,
        )
    )


if __name__ == "__main__":
    main()
