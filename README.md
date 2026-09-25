# 国庆视频 · 3D 白模生成商业科技宣传片全流程技能 (Guoqing Video Skill)

[![Antigravity](https://img.shields.io/badge/Antigravity-Skill-blue.svg)](https://deepmind.google/technologies/antigravity)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

> **一键将 3D 白模视频/CAD 动画，转化为具备 Apple 发布会质感、工业级金属光影、人物英文配音、节奏 BGM、品牌 Logo 与双语字幕的商业科技宣传成片。**

---

## 🌟 核心特性 (Features)

1. **白模智能关键帧解构 (Smart Keyframe Extraction)**
   * 自动探测 CAD / Blender 导出的白模视频（MP4/MOV）；
   * 精确抽取 3 组结构锚点（全景亮相、精密零件爆炸、重构运转），作为生成式 AI 的结构拓扑约束。
2. **双模型渲染调度 (Dual-Engine AI Rendering)**
   * **MiniMax-H3**：国内极速多图锚点支持，保持零件拓扑不形变，原生输出 768P/2K 与环境音效；
   * **Google Veo 3.1**：Google DeepMind 旗舰级电影质感视频生成大模型，支持首尾帧插值与高反光金属摄影棚光照。
3. **15s + 15s 对称分镜叙事 (Dual-Shot Narrative)**
   * **镜头一 (0~15s：机械解构)**：螺栓、法兰与活塞沿轴线展开，展现内部工业之美；
   * **镜头二 (15~30s：重构运转)**：零件回位锁紧，大型配重飞轮匀速旋转驱动往复连杆。
4. **全套广播级商业包装 (Full Post-Production Package)**
   * **左上角 Logo 悬浮**：透明 PNG 优雅常驻；
   * **片尾海报收尾**：在最后 4 秒平滑淡入品牌定格画面；
   * **电影级英文旁白**：集成 `edge-tts` 顶级科技男声（`en-US-ChristopherNeural`）；
   * **经典商业 BGM 与智能避让**：内置《Best Friend》等高能量商业配乐，带自动人声避让（Audio Ducking）；
   * **中英双语无损字幕**：冬青黑体（`Hiragino Sans GB`）双层居中排版，自动压制入片。

---

## 📂 项目结构 (Repository Structure)

```text
guoqing-video/
├── SKILL.md                          # Antigravity 官方技能规范入口
├── README.md                         # 项目中文/英文说明文档
├── requirements.txt                  # Python 依赖清单
├── skills/
│   └── guoqing-video/
│       └── SKILL.md                  # 适配 .agents/skills/ 结构
├── scripts/
│   ├── 01_extract_anchors.py         # 智能白模抽帧脚本
│   ├── 02_render_shots.py            # 双镜头渲染调度脚本
│   ├── 03_splice_shots.py            # FFmpeg 无缝镜头拼接
│   ├── 04_generate_voiceover.py      # 神经英文语音生成脚本
│   ├── 05_final_synthesis.py         # 多轨混音与包装合成脚本
│   └── 06_burn_subtitles.py          # 双语字幕硬字幕压制
├── templates/
│   ├── commercial_subtitles.ass      # Apple 风格双语 ASS 字幕工程模板
│   └── prompts.json                  # 工业机械/消费电子顶级科技提示词库
└── references/
    └── pipeline_architecture.md       # 系统技术架构与原理解析
```

---

## 🚀 快速上手 (Quick Start)

### 1. 环境安装
```bash
pip install -r requirements.txt
```

### 2. 配置密钥
在环境变量或 `.env` 中填入模型 Key：
```bash
export METASO_API_KEY="your_minimax_or_metaso_key"
# 或启用 Google Veo:
export GEMINI_API_KEY="your_google_ai_studio_key"
```

### 3. 一步生成成片
```bash
# 1. 抽取白模锚点
python3 scripts/01_extract_anchors.py --input raw_white_model.mp4

# 2. 调度 AI 渲染两个 15 秒镜头
python3 scripts/02_render_shots.py --duration 15

# 3. 拼接并转码为 720P 标准横屏
python3 scripts/03_splice_shots.py

# 4. 生成英文商业配音
python3 scripts/04_generate_voiceover.py

# 5. 合成 BGM、Logo、片尾海报
python3 scripts/05_final_synthesis.py

# 6. 压制中英双语字幕
python3 scripts/06_burn_subtitles.py
```

---

## 📄 License
MIT License.
