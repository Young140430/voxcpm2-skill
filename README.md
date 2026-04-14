# VoxCPM TTS Skill

一行命令将文本转换为自然语音，支持音色克隆。

## 前置要求

- Python >= 3.10
- 网络连接（需访问 VoxCPM API 服务器，如需使用API请加入QQ群：321776831）
- 首次运行自动安装 `aiohttp` 依赖

## 安装

无需额外安装步骤，直接运行脚本即可。首次运行会自动安装 Python 依赖。

## 使用

### 基础用法
```bash
python voxcpm_tts.py "你好，欢迎使用语音合成"
```

### 指定输出文件
```bash
python voxcpm_tts.py "Hello world." -o hello.mp3
```

### 克隆音色（仅参考音频）
```bash
python voxcpm_tts.py "今天天气不错" --prompt ref.wav
```

### 最佳效果（参考音频 + 文本）
```bash
python voxcpm_tts.py "今天天气不错" --prompt ref.wav --prompt-text "参考音频中说的文字"
```

### 自定义 API 服务器
```bash
python voxcpm_tts.py "测试" --api http://your-server:8000
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `text` | 要合成的目标文本（必需） | - |
| `-o, --output` | 输出 MP3 文件路径 | `output.mp3` |
| `--prompt` | 参考音频文件路径 | 无 |
| `--prompt-text` | 参考音频对应文本 | 无 |
| `--cfg` | CFG 值 | `2` |
| `--api` | API 服务器默认地址 | `http://43.143.233.233:8000` |


## 文件结构

```
voxcpm2-skill/
├── SKILL.md          # Skill 定义文件（AI Agent 读取）
├── README.md         # 本文件
├── voxcpm_tts.py     # 主脚本（CLI 入口）
├── client.py         # 原始 API 客户端示例
└── prompt_audio.wav  # 参考音频示例
```

## 相关链接

- **GitHub**: https://github.com/OpenBMB/VoxCPM
- **ModelScope**: https://www.modelscope.cn/models/OpenBMB/VoxCPM2
