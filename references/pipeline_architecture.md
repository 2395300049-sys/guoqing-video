# 国庆视频 · 3D 白模生成极简科技宣传片系统架构 (Pipeline Architecture)

## 1. 核心设计原则 (Core Principles)
* **保真优先 (Fidelity First)**：针对机械与工业模型，严禁大模型擅自篡改螺丝数量、曲轴结构或添加不存在的数显屏幕。通过多图锚点（`@1` 全景基准、`@2` 爆炸图基准）强制锁定几何与物理拓扑。
* **分镜节奏律动 (Beat-Synced Rhythm)**：采用 15s + 15s 的对称结构，前 15 秒展示解构之美（Exploded View），后 15 秒展示运转之势（Continuous Operation）。
* **广播级声画混响 (Broadcast Audio Mastering)**：
  - **人声音频避让 (Audio Ducking)**：背景音乐（如《Best Friend》）在旁白出现时自动衰减至 -14dB，留出人声频段；
  - **高保真神经语音 (Neural TTS)**：利用微调音色生成沉稳、有科技权威感的英文解说；
  - **环境音叠合 (Foley Ambience)**：保留 3D 生成模型自带的机械微动风切与高压气动声。

## 2. 视频模型调用规范
* **MiniMax-H3 (推荐工业级快速成片)**：
  - 分辨率推荐：`768P`（1344×768，16:9）或 `2K`
  - 时长设定：`15` 秒
  - 角色设定：`role: "reference_image"`
* **Google Veo 3.1 (顶级影视级画质)**：
  - 推荐模型：`models/veo-3.1-generate-preview`
  - 计费要求：需启用 Google Cloud 结算账户（Pay-as-you-go）
