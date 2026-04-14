---
name: voxcpm-tts
description: |
  VoxCPM 语音合成技能。将文本转换为自然语音，支持零样本合成、参考音色克隆、带文本引导的语音生成。
  触发条件：用户需要语音合成、TTS、文字转语音、音色克隆、生成语音文件。
  要求：Python >= 3.10，首次运行自动安装依赖。
---

# VoxCPM TTS — 一行命令生成语音

将任意文本转换为自然语音 MP3 文件，支持三种模式：零样本、参考音色、带文本引导。

## 快速开始

```bash
# 最简单用法 — 零样本合成
python voxcpm_tts.py "你好，欢迎使用语音合成"

# 指定输出文件
python voxcpm_tts.py "Hello world." -o hello.mp3

# 使用参考音色（克隆音色，无需文本）
python voxcpm_tts.py "今天天气不错" --prompt ref.wav

# 使用参考音色 + 参考文本（最佳效果）
python voxcpm_tts.py "今天天气不错" --prompt ref.wav --prompt-text "参考音频的文字内容"
```

## 命令参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `text` | 要合成的目标文本（必需） | - |
| `-o, --output` | 输出 MP3 文件路径 | `output.mp3` |
| `--prompt` | 参考音频文件路径（WAV/MP3） | 无 |
| `--prompt-text` | 参考音频对应的文本内容 | 无 |
| `--cfg` | CFG 值，越大越贴近文本 | `2` |
| `--api` | VoxCPM API 服务器默认地址 | `http://43.143.233.233:8000` |

## 三种合成模式

### 1. 零样本模式（无参考音频）
```bash
python voxcpm_tts.py "这是零样本合成的语音"
```
- 不提供任何参考音频，使用模型默认音色
- 适合快速测试

### 2. 参考音色模式（仅参考音频）
```bash
python voxcpm_tts.py "用参考音色说这句话" --prompt speaker.wav
```
- 提供参考音频，克隆说话人音色
- 不需要参考音频的文本内容
- 适合只有音频片段、不知道内容的场景

### 3. 带文本引导模式（参考音频 + 文本）★推荐
```bash
python voxcpm_tts.py "用参考音色说这句话" --prompt speaker.wav --prompt-text "参考音频中说的文字"
```
- 同时提供参考音频及其对应文本
- 合成效果最佳，音色还原度最高
- 适合已知音频内容的场景

## 工作流程

当用户请求生成语音时，按以下步骤执行：

```python
WORKFLOW = [
    {
        "step": 1,
        "name": "parse_request",
        "tasks": ["提取目标文本", "确定是否需要参考音频", "确定输出文件路径"]
    },
    {
        "step": 2,
        "name": "validate_inputs",
        "tasks": ["检查 Python 版本 >= 3.10", "确认参考音频文件存在（如有）", "确认 API 服务器可达"]
    },
    {
        "step": 3,
        "name": "generate_speech",
        "command": "python voxcpm_tts.py \"{text}\" --prompt {prompt} --prompt-text \"{prompt_text}\" -o {output}",
        "tasks": ["调用 voxcpm_tts.py 生成语音", "等待生成完成"]
    },
    {
        "step": 4,
        "name": "deliver_result",
        "tasks": ["确认输出文件已生成", "告知用户文件路径"]
    }
]
```

## 故障排除

| 问题 | 解决方案 |
|------|---------|
| `aiohttp` 缺失 | 首次运行自动安装，或手动 `pip install aiohttp` |
| 连接超时 | 检查 API 地址是否正确，`--api` 指定新地址 |
| 参考音频编码失败 | 确保音频为 WAV/MP3 格式，文件未损坏 |
| Python 版本过低 | 需要 Python >= 3.10，升级 Python |
