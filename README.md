# COC 跑团工作台

AI 辅助的《克苏鲁的呼唤》（COC）KP 工作台。没有代码，全部产物是 markdown——用 Claude Code 做叙事表达，骰子和走向始终握在 KP 手里。

## 工作原理

- **双会话并行**：跑团时开两个 Claude Code 会话——**生产者**吸收群聊原文，提炼事件、追加 timeline、更新 state；**消费者**按 KP 的写作意图产出节拍式描述草稿。贴错窗口会被明确指出，不会硬接。
- **三条铁律**：骰子和规则计算不交给 LLM；走向决策归 KP，草稿永远可被改写；长团记忆外置在 campaign/ 文件里，不依赖上下文窗口。全文见 [CLAUDE.md](CLAUDE.md)。
- **冷启动**：每个会话开始时自动扫描未完结的 run 并复位游标，新会话不丢前情。

## 目录导览

| 路径 | 是什么 |
|---|---|
| [CLAUDE.md](CLAUDE.md) | 工作台总协议：会话职责、冷启动、文件协议、写者矩阵 |
| [.claude/skills/](.claude/skills/) | 6 个 coc-* 技能，驱动全流程（见下方速查） |
| [campaign/](campaign/) | 按模组分目录：**模组库**（module/routes/scenes/npcs/drafts/handouts/expand.md，跨团复用只读）+ **runs/**（一次开团：pcs/timeline/state/raw.md，raw.md 是 KP 终稿逐字底账） |
| [corpus/](corpus/) | 语料库：技法/片段两层 + 文风锚点，[INDEX.md](corpus/INDEX.md) 是唯一检索入口 |
| [mods/](mods/) | 模组 PDF 原件（备团原料） |
| [logs/](logs/) | 历史团跑团 log（docx 及提取的纯文本） |
| [ref/](ref/) | COC 规则书 |

## 当前状态

| 模组 | 状态 |
|---|---|
| 追书人 | **已收团**（[2026-09-15](campaign/追书人/runs/2026-09-15/state.md)，正史 #1–#71，唯一开放线：礼拜二托马斯是否来信） |
| 不息的渴望 | 已备团未开（模组库就绪，等 PC 导入开团） |

## 工作流速查

1. **备团** — 给出模组 PDF → [coc-prep](.claude/skills/coc-prep/SKILL.md)：场景切分、场景卡/NPC 卡、真相摘要、理想路线、预写稿
   - **拓展探测** — 备团步骤 5（同上下文）调用 [coc-expand](.claude/skills/coc-expand/SKILL.md)：按四类十六条规则对**模组原文**体检（卡关风险／深挖潜力／手稿机会／节奏结构），产出 expand.md 清单。只探测不代工——KP 点选条目（如"生成 A1-1"）才生成补线、多解方案、高密度手稿、NPC 深化、场景细节；已备模组随时可单独补探测
2. **导入 PC** — [coc-pc-import](.claude/skills/coc-pc-import/SKILL.md)：结合模组真相与场景卡，为每个 PC 生成个人情节钩子
3. **开团**（生产者 + 消费者双会话并行）
   - 粘贴群聊原文 → [coc-producer](.claude/skills/coc-producer/SKILL.md)：timeline 只增不改，state 保持一屏以内
   - 写作意图 → [coc-consumer](.claude/skills/coc-consumer/SKILL.md)：按读取协议装配上下文，产出节拍式描述草稿
4. **收团** — [coc-harvest](.claude/skills/coc-harvest/SKILL.md)：校验 timeline 完整性，从正史挖语料入库，git commit 存档

## 复刻这工作台

给想搭一套同样工作台的其他 KP：

1. **前置**：安装 Claude Code（CLI / VSCode 扩展 / 桌面端均可），`git init` 一个空仓库。
2. **核心引擎只有两样**：把本仓库的 [CLAUDE.md](CLAUDE.md) 和 [.claude/skills/](.claude/skills/) 抄过去——前者是总协议，后者是六个技能，都是纯 markdown 提示词，无任何依赖。
3. **素材自备**：mods/（模组 PDF）、logs/（旧团 log，可省）、ref/（规则书）换成你自己的。corpus/ 语料库从空开始也能跑——harvest 每次收团自动积累。
4. **开第一个团**：对 Claude 说“备团”并给出 PDF，coc-prep 会建出 campaign/<模组>/ 的完整结构。

协议细节（文件布局、单一写者矩阵、timeline/state 纪律）都在 [CLAUDE.md](CLAUDE.md) 与各 [SKILL.md](.claude/skills/) 里——README 只是导览，不是第二份协议。
