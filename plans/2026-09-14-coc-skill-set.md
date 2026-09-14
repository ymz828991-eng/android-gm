# COC 跑团 Skill 集实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建成 COC 跑团 skill 集——5 个 skill + CLAUDE.md 引导 + 语料库种子 + 用《不息的渴望》完成备团管线与回放验收。

**Architecture:** 全部产物为 markdown 文件。skill 之间不调用，通过 campaign/ 与 corpus/ 的单一写者文件协议协作；跑团时生产者/消费者双会话并行。spec 第 5 章的文件格式即接口。

**Tech Stack:** 无代码。工具仅：Read（PDF 分页读取）、Bash+python（docx 解包，一次性提取）、git（提交与存档点）。

**Spec:** `spec/2026-09-14-coc-skill-set-design.md`（执行者必读，尤其第 4-6 章；格式以 spec 第 5 章为准）

## Global Constraints

- 不写任何工程代码；产物全部是 markdown（一次性 docx 提取命令除外，输出进 gitignored 目录）
- 全部内容中文；skill 目录名用 ASCII kebab-case（coc-prep / coc-pc-import / coc-producer / coc-consumer / coc-harvest）
- 每个 SKILL.md 有 YAML frontmatter：`name`（目录名）+ `description`（"Use when…"式触发描述，中文）
- 三条铁律写进 CLAUDE.md 与每个跑团期 skill：骰子不进 LLM / 走向归 KP / 记忆在文件
- 单一写者（spec 4.2 矩阵）：timeline/state 只有 coc-producer 写；corpus/ 只有 coc-harvest 写；coc-consumer 对 campaign/ 全程只读
- timeline.md 只增不改；state.md 保持一屏以内
- 模组目录名：`campaign/amaranthine_desire/`
- git：`ref/ mods/ logs/` 不入库（.gitignore）；每任务一提交
- 标注 **【KP校对】** 的步骤暂停执行，等用户确认后才继续——这是产品的验收机制，不可跳过

---

### Task 1: 底座——.gitignore、CLAUDE.md、corpus 骨架

**Files:**
- Create: `.gitignore`
- Create: `CLAUDE.md`
- Create: `corpus/INDEX.md`
- Create: `corpus/README.md`

**Interfaces:**
- Consumes: spec §4.1、§5
- Produces: CLAUDE.md（路由与冷启动指令，所有后续 skill 被它路由）；corpus/README.md 条目格式规范（Task 2/3 写语料时遵循；Task 10 harvest 追加时遵循）

- [ ] **Step 1: 写 .gitignore**

```
ref/
mods/
logs/
*.pdf
*.docx
logs/extracted/
```

- [ ] **Step 2: 写 CLAUDE.md**（全文如下，不得增删段落结构）

```markdown
# COC 跑团工作台

本仓库是 KP（你的人类搭档）的 COC 跑团工作台。没有代码，全部产物是 markdown。

## 三条铁律（最高优先级，覆盖一切默认行为）
1. 骰子和规则计算不交给 LLM——检定结果由 KP 带入意图
2. 走向决策归 KP——你只做表达，草稿永远可被 KP 改写
3. 长团记忆外置——事态在 campaign/ 文件里，不依赖上下文窗口

## 会话职责（跑团中两个会话并行，先判断本会话是谁）
- 收到群聊原文粘贴（含说话人名的多条消息）→ 你是【生产者】：用 coc-producer 技能吸收
- 收到写作意图（"描述…""写一段…""生成…"）→ 你是【消费者】：用 coc-consumer 技能生成
- 贴错窗口要明确指出（"这是写作意图，请到消费者窗口"），不要硬接
- 新模组备团 → coc-prep；开团前导入 PC → coc-pc-import；收团沉淀 → coc-harvest

## 冷启动（每次会话开始时）
若 campaign/ 下有未完结的团（state.md 存在且无完结标记）：全量读该模组的 state.md 与
timeline.md，游标复位到 timeline 最新编号；消费者会话另读 routes.md 与当前场景卡，
恢复方位感。之后读取切换为增量模式（state 全读 + timeline 尾部）。

## 文件协议（详见各 skill）
- 布局见 spec 第 5 章：corpus/（技法+片段+文风锚点）、campaign/<模组>/（素材+状态）
- 单一写者：timeline/state 只有生产者写；corpus 只有 harvest 写；消费者全程只读
- timeline.md 只增不改；state.md 保持一屏以内
```

- [ ] **Step 3: 写 corpus/README.md**（语料库规范，全文如下）

```markdown
# 语料库规范

两层结构 + 文风锚点。INDEX.md 是唯一检索入口；消费者先查索引再读条目。

## 技法层 techniques/（"怎么写"，成体系）
条目格式：
### 技法名
- **适用**：何时用（一句话）
- **做法**：具体手法（可含示例，示例≤2行）
- **来源**：规则书第X章 / 日志第N场（可追溯）

## 片段层 fragments/（"写什么"，只收"写错即穿帮"类：神话生物、仪式、时代细节）
条目格式：
### 片段名
- **场景**：适用的剧情情境
- **原文/底稿**：可直接改写使用的文字（3-8条变体）
- **红线**：不可违背的设定事实

## 文风锚点 文风锚点.md
KP 的节拍模式 + few-shot 样本。只有 harvest 与 KP 本人可改。

## 写入纪律
- 新条目必须同步更新 INDEX.md 对应分类行
- 技法须经验证才入库（来源可追溯）；片段入库前核对设定红线
```

- [ ] **Step 4: 写 corpus/INDEX.md**（初始骨架）

```markdown
# 语料库索引

## 技法层 techniques/
- [ ] 写作纪律.md —— 规则书第十章蒸馏（证据不点破因果、少即是多…）
- [ ] 节拍手法.md —— KP 日志挖掘（连发节奏、过渡词、异常点置尾…）
- [ ] 氛围营造.md —— 待种子
- [ ] 伏笔技巧.md —— 待种子

## 片段层 fragments/
- （空，随团生长）

## 锚点
- [ ] 文风锚点.md —— KP 节拍模式与 few-shot
```

- [ ] **Step 5: 验证**：四个文件存在；CLAUDE.md 含"三条铁律""冷启动""单一写者"字样（grep 确认）
- [ ] **Step 6: Commit**

```bash
git add .gitignore CLAUDE.md corpus/
git commit -m "feat: 工作台底座——引导文件、语料库规范与索引骨架"
```

---

### Task 2: 语料种子（一）——日志提取：文风锚点 + 节拍手法

**Files:**
- Create: `corpus/文风锚点.md`
- Create: `corpus/techniques/节拍手法.md`
- Modify: `corpus/INDEX.md`（勾选对应行）
- Create: `logs/extracted/*.txt`（gitignored 中间产物）

**Interfaces:**
- Consumes: `logs/不息的渴望/*.docx`（5 个）、corpus/README.md 条目格式
- Produces: 文风锚点（Task 8 消费者装配的固定底座之一）；节拍手法（同）

- [ ] **Step 1: 提取五场日志为纯文本**（已验证的解包配方，输出到 gitignored 目录）

```bash
cd /c/Users/Administrator/Desktop/coc_v2 && mkdir -p logs/extracted && python -c "
import zipfile, re, sys, html, glob, os
sys.stdout.reconfigure(encoding='utf-8')
for f in glob.glob('logs/不息的渴望/*.docx'):
    with zipfile.ZipFile(f) as z:
        xml = z.read('word/document.xml').decode('utf-8')
    text = html.unescape(''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', xml)))
    msgs = re.split(r'(<[^<>]{1,20}>)', text)
    pairs, cur = [], None
    for part in msgs:
        if re.fullmatch(r'<[^<>]{1,20}>', part):
            if cur: pairs.append(cur)
            cur = [part[1:-1], '']
        elif cur: cur[1] += part
    if cur: pairs.append(cur)
    out = os.path.join('logs/extracted', os.path.basename(f).replace('.docx', '.txt'))
    with open(out, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(f'[{s}] {c.strip()}' for s, c in pairs))
    print(out, len(pairs), '条')
"
```

预期：5 个 txt，总消息数约 1500+（1初见实测 552 条）。

- [ ] **Step 2: 分析 KP 节拍模式**：通读提取文本，统计/归纳——KP 连发条数分布（2-6 条为主）、单条字数（35-60 字）、过渡词清单（"那么/你们看到/此时/…"完整列出）、节拍类型分布（环境/动作结果/NPC对白/检定指令/结算）、异常点在连发中的位置规律
- [ ] **Step 3: 写 corpus/文风锚点.md**，含四节：节拍模式（Step 2 统计结论）、过渡词表、语言风格要点（人称、时态、句长）、**few-shot 样本**（从日志逐字摘录，场景开场/检定结果/NPC对白/转场 各 3 条，标注出处"第N场"，不得改写一字）
- [ ] **Step 4: 写 corpus/techniques/节拍手法.md**：按 corpus/README.md 技法条目格式，至少覆盖——连发的起承结构（首条定位→中段展开→末条异常点/钩子）、检定分层描述法（成功/失败各自怎么写）、转场压缩法、重复事件变体法。每条技法注明来源场次
- [ ] **Step 5: 验证**：文风锚点的 few-shot 逐条与提取文本比对一致（抽 3 条 grep）；INDEX.md 两行已勾选
- [ ] **Step 6: 【KP校对】** 呈现两文件给用户确认文风归纳是否失真
- [ ] **Step 7: Commit**

```bash
git add corpus/ && git commit -m "feat: 语料种子——文风锚点与节拍手法（源自不息的渴望日志）"
```

---

### Task 3: 语料种子（二）——规则书蒸馏：写作纪律 + 氛围/伏笔

**Files:**
- Create: `corpus/techniques/写作纪律.md`
- Create: `corpus/techniques/氛围营造.md`
- Create: `corpus/techniques/伏笔技巧.md`
- Modify: `corpus/INDEX.md`

**Interfaces:**
- Consumes: `ref/call-of-cthulhu-keeper-rulebook-cn-Version2002c.pdf`（第十章附近：守密人技艺/场景描述/氛围）
- Produces: 写作纪律（消费者固定底座 + 自检清单来源）

- [ ] **Step 1: 定位章节**：Read 该 PDF 前 10 页（目录），找到"守密人技艺/场景描述/恐怖氛围/伏笔铺垫"相关章节的页码区间
- [ ] **Step 2: 分段读取**：按页码区间用 pages 参数读取（每次 ≤20 页），通读相关章节
- [ ] **Step 3: 写 corpus/techniques/写作纪律.md**：蒸馏为可执行纪律清单——第二人称现在时；**描述证据不点破因果**（"地毯上有泥"而非"凶手翻窗而入"）；box text 只可原文引用；怪物描写"少即是多"；NPC 按声线卡说话、不越知情边界；检定服务于剧情。每条注规则书章节出处
- [ ] **Step 4: 写 氛伏营造.md 与 伏笔技巧.md**：规则书蒸馏为主（五感递进、时间/天气/声音的运用；线索三层法：可发现→可解读→可行动），辅以日志中观察到的实例。条目格式遵循 corpus/README.md
- [ ] **Step 5: 验证**：三文件均含"来源"字段；INDEX.md 三行勾选
- [ ] **Step 6: 【KP校对】** 用户确认蒸馏无失真（用户熟悉规则书）
- [ ] **Step 7: Commit**

```bash
git add corpus/ && git commit -m "feat: 语料种子——写作纪律/氛围营造/伏笔技巧（规则书蒸馏）"
```

---

### Task 4: coc-prep skill（备团管线）

**Files:**
- Create: `.claude/skills/coc-prep/SKILL.md`

**Interfaces:**
- Consumes: spec §5.3（卡片内容清单）、§6.1
- Produces: `campaign/<模组id>/` 全部素材文件的生成规范（Task 5/6 执行此规范）

- [ ] **Step 1: 写 SKILL.md**，结构与必备内容：

```markdown
---
name: coc-prep
description: 备团时使用——新模组导入、场景切分、场景卡/NPC卡生成、真相摘要、路线分析、预写稿。触发：用户给出新模组 PDF 或要求备团。
---
```

正文必须包含（协议性内容逐条写入，措辞可润色）：
1. **四步管线总览**，每步末尾固定一句："停下，请 KP 校对：直接修改生成文件后说'继续'。"
2. **步骤1 场景切分**：Read 模组 PDF 全文（>10页则每次≤20页分段）→ 按场景边界切分 → 产出 `campaign/<模组id>/scenes/<id>.md` 骨架（id 用英文小写下划线，如 mill、town_road）。**box text 识别规则**：模组中标注"读出/朗读/box"或成段的环境描写文字标记为 box_texts，只可原文引用
3. **步骤2 卡片生成**：场景卡按 spec §5.3（原文+浓缩+box_texts+出入口+在场NPC引用+PC挂注位）；NPC卡按 spec §5.3（声线卡四字段+知情边界+stats_ref 占位）
4. **步骤3 module.md 与 routes.md**：module.md = 元信息 + 真相摘要（≤500字）+ **伏笔登记表**（编号/内容/预期揭示点）；routes.md = 主线序、关键节点（错过即坏局的）、可跳过项
5. **步骤4 预写稿 drafts/**：每场景开场白一份、关键检定成败两版（依 routes.md 的关键节点选取）
6. 尾部：三条铁律 + "数值表不进上下文，只留 stats_ref"

- [ ] **Step 2: 验证**：frontmatter 合法；含"停下，请 KP 校对"×4；含伏笔登记表、box text 识别规则
- [ ] **Step 3: Commit**

```bash
git add .claude/skills/coc-prep/ && git commit -m "feat: coc-prep 备团管线skill"
```

---

### Task 5: 执行备团步骤 1-2（不息的渴望：场景卡 + NPC 卡）

**Files:**
- Create: `campaign/amaranthine_desire/scenes/*.md`
- Create: `campaign/amaranthine_desire/npcs/*.md`

**Interfaces:**
- Consumes: coc-prep SKILL.md、`mods/不息的渴望-An Amaranthine Desire.pdf`
- Produces: 场景卡与 NPC 卡（Task 8 消费者装配输入；Task 7 pc-import 挂注对象）

- [ ] **Step 1: Read 模组 PDF**（先读前 5 页判断总页数，再分段读完全文）
- [ ] **Step 2: 按 coc-prep 步骤 1 切分场景**，产出全部场景卡骨架
- [ ] **Step 3: 按步骤 2 生成场景卡与 NPC 卡**（本模组为线性+时光圈事件轴：场景 order 链写入各卡"出入口"字段）
- [ ] **Step 4: 自检**：场景 id 无重复；每张 NPC 卡有知情边界；box_texts 均为原文摘录（与 PDF 比对抽 3 处）
- [ ] **Step 5: 【KP校对】** 用户逐卡确认（这是 spec 定义的"校对是一次性成本"环节）
- [ ] **Step 6: Commit**

```bash
git add campaign/amaranthine_desire/ && git commit -m "feat: 不息的渴望场景卡与NPC卡（备团步骤1-2）"
```

---

### Task 6: 执行备团步骤 3-4（真相/路线/预写稿）

**Files:**
- Create: `campaign/amaranthine_desire/module.md`
- Create: `campaign/amaranthine_desire/routes.md`
- Create: `campaign/amaranthine_desire/drafts/*.md`

**Interfaces:**
- Consumes: Task 5 的场景卡
- Produces: module.md 真相摘要+伏笔登记表（消费者固定底座）；routes.md（W0 冷启动方位感来源）；drafts/（跑团中可调出微调）

- [ ] **Step 1: 按 coc-prep 步骤 3 写 module.md**（真相≤500字；伏笔登记表编号 F1、F2…）
- [ ] **Step 2: 写 routes.md**（本模组注意：时光圈事件轴——每圈的关键差异点单列一节）
- [ ] **Step 3: 按步骤 4 写预写稿**：每个场景开场白 + 关键检定成败两版
- [ ] **Step 4: 自检**：routes 关键节点与 drafts 一一对应；伏笔登记表覆盖模组全部伏笔
- [ ] **Step 5: 【KP校对】**
- [ ] **Step 6: Commit**

```bash
git add campaign/amaranthine_desire/ && git commit -m "feat: 不息的渴望真相/路线/预写稿（备团步骤3-4）"
```

---

### Task 7: coc-pc-import skill + 历史PC试运行

**Files:**
- Create: `.claude/skills/coc-pc-import/SKILL.md`
- Create: `campaign/amaranthine_desire/pcs/理查德.md`（试运行产物，作为格式样板）

**Interfaces:**
- Consumes: Task 5 场景卡、module.md 真相
- Produces: pcs/<id>.md 格式；场景卡"PC挂注"写入规范

- [ ] **Step 1: 写 SKILL.md**：frontmatter（name: coc-pc-import，触发=开团前导入玩家角色）+ 流程：读 PC 背景 → 对照 module.md 真相与场景卡找连接点 → 生成个人情节钩子（独有线索/情感联结/NPC旧缘，每 PC 2-3 个）→ 写 pcs/<id>.md（背景+一句话状态+钩子清单）→ 在相关场景卡的"PC挂注"节追加一行。尾部三条铁律
- [ ] **Step 2: 试运行**：从 `logs/extracted/` 提取理查德的玩家发言风格与行为模式，作为"背景"输入，跑一遍流程产出 pcs/理查德.md + 场景卡挂注
- [ ] **Step 3: 【KP校对】**（KP 最清楚历史 PC）
- [ ] **Step 4: Commit**

```bash
git add .claude/skills/coc-pc-import/ campaign/amaranthine_desire/pcs/ && git commit -m "feat: coc-pc-import skill 与历史PC样板"
```

---

### Task 8: coc-consumer skill + 首次回放测试

**Files:**
- Create: `.claude/skills/coc-consumer/SKILL.md`
- Create: `docs/replays/2026-09-14-首次回放.md`（测试报告）

**Interfaces:**
- Consumes: 全部素材（场景卡/NPC卡/module.md/corpus 全部）；spec §6.4 协议
- Produces: 消费者协议（W2 回路心脏）；回放测试方法论（Task 11 复用）

- [ ] **Step 1: 写 SKILL.md**，正文必须包含（协议逐条写入）：
  1. **第0步 冷启动**（spec §7 W0：state+timeline 全量、routes+当前场景卡、游标复位）
  2. **读取两模式表**（spec §6.4 原表照录）
  3. **装配顺序**：state 全量 → timeline 增量 → 场景卡（意图定位，1-2张）→ 在场NPC卡 → corpus/INDEX 按需 → 固定底座（写作纪律+文风锚点+module.md 真相摘要）
  4. **意图解析**：自然语言+可选（骰子结果/语气/篇幅）；若意图含检定数值——提醒铁律1：KP 已定成败，不得自行掷骰
  5. **生成**：节拍草稿 2-6 条连发，每条标注类型（环境/动作结果/NPC对白/检定指令/结算），单条≤60字
  6. **自检清单**（呈现前逐项过）：是否点破因果（剧透）？box text 是否原文？NPC 是否越知情边界？节拍形态是否符合文风锚点？
  7. **反馈循环**：KP 指出第 N 条问题 → 仅重生成该条及受影响条
  8. **防呆**：收到群聊原文粘贴 → "我是消费者，请到生产者窗口"；发现 timeline 断号 → 提醒先喂生产者；**对 campaign/ 零写入**
- [ ] **Step 2: 搭建回放环境**：从 `logs/extracted/2再见.txt` 选一段含"场景到场+一次检定"的 10-20 条 KP 连发片段；从该片段之前的日志手工重建 `campaign/amaranthine_desire/state.md` 与 `timeline.md`（写到片段前一刻，标注文件头"回放测试用，第2场中途"）——这是测试脚手架，KP 终稿即"正史"来源
- [ ] **Step 3: 执行回放**：以当时 KP 实际作为意图输入（从上文反推），跑消费者协议生成节拍
- [ ] **Step 4: 写测试报告** `docs/replays/2026-09-14-首次回放.md`：生成的节拍全文 + 当年 KP 原文 + 四维评分（贴合模组/文风/节拍形态/剧透控制，各 1-5 分 + 一句理由）+ 失败模式记录
- [ ] **Step 5: 【KP校对】** 用户读报告，判定是否达到可用线（总分≥14/20 且无剧透翻车）；未达标则按失败模式修 SKILL.md 或语料后重跑（此循环预期 1-3 轮）
- [ ] **Step 6: Commit**

```bash
git add .claude/skills/coc-consumer/ docs/replays/ && git commit -m "feat: coc-consumer skill 与首次回放测试"
```

---

### Task 9: coc-producer skill + 吸收回放验证

**Files:**
- Create: `.claude/skills/coc-producer/SKILL.md`

**Interfaces:**
- Consumes: spec §5.1/§5.2（timeline/state 格式）、§6.3
- Produces: 生产者协议；timeline/state 的唯一写入规范（消费者与 harvest 依赖其格式稳定性）

- [ ] **Step 1: 写 SKILL.md**，正文必须包含：
  1. **第0步 冷启动**（同 W0）
  2. **吸收协议**（spec §6.3 四步照录）：解析说话人（KP 消息=正史节拍，玩家消息=行动）→ 提炼 1-3 条事件/轮，**追加** timeline（格式 spec §5.1：`#编号 [N场] 一句话事实`，涉及伏笔写"（F# 保住/暴露）"）→ **更新** state.md 五节（格式 spec §5.2）→ 极简简报（"新增3事件，NPC状态改1"），KP 说"改"即修正
  3. **前情提要模式**：续团时基于 timeline+state 生成 recaps/<日期>.md（面向玩家的 300-500 字，只含玩家可知）
  4. **防呆**：收到写作意图 → "我是生产者，请到消费者窗口"；无法识别说话人时列出候选问 KP
  5. 尾部三条铁律 + "timeline 只增不改；state 一屏以内"
- [ ] **Step 2: 吸收回放验证**：把 `logs/extracted/1初见.txt` 开场 40 条（导入段+石滩段）作为粘贴输入跑吸收协议；检查：timeline 条目编号连续、每条≤30字、KP 的导入段被正确标为正史；state.md 生成后五节齐全且一屏内
- [ ] **Step 3: 清理**：验证产物写入 `docs/replays/2026-09-14-生产者验证.md` 留档；把验证用的 timeline/state 恢复为回放脚手架状态（git checkout）
- [ ] **Step 4: Commit**

```bash
git add .claude/skills/coc-producer/ docs/replays/ && git commit -m "feat: coc-producer skill 与吸收回放验证"
```

---

### Task 10: coc-harvest skill

**Files:**
- Create: `.claude/skills/coc-harvest/SKILL.md`

**Interfaces:**
- Consumes: timeline.md（正史）、corpus/README.md 写入纪律
- Produces: 语料沉淀协议 + git 存档点

- [ ] **Step 1: 写 SKILL.md**，正文必须包含：
  1. **完整性校验**：timeline 编号连续、当前场次闭合（KP 确认团已收）
  2. **语料沉淀**（只从 timeline 正史挖，不碰草稿）：新技法候选（本场出现且验证有效的手法，按 README 格式入库+更新 INDEX）；片段候选（神话生物/仪式等"写错即穿帮"类）；文风样本补充（追加到文风锚点 few-shot，保持逐字）
  3. **git commit**：`第N场存档点`（campaign/ + corpus/ 一并提交）
  4. 尾部：corpus 只有本 skill 可写；三条铁律
- [ ] **Step 2: 干跑验证**：对回放脚手架的 timeline 跑一遍沉淀逻辑（只产出建议清单呈 KP，不实际写 corpus——数据是脚手架，不入库）
- [ ] **Step 3: Commit**

```bash
git add .claude/skills/coc-harvest/ && git commit -m "feat: coc-harvest 收团沉淀skill"
```

---

### Task 11: CLAUDE.md 终化 + 全链路回放验收

**Files:**
- Modify: `CLAUDE.md`（按实测补充）
- Create: `docs/replays/2026-09-14-全链路验收.md`

**Interfaces:**
- Consumes: 全部 5 skill + 全部素材 + Task 8 回放方法论
- Produces: 验收报告（v1 完成判据）

- [ ] **Step 1: 全链路模拟**（单会话内顺序扮演，记录每步）：
  a. W0：清上下文后仅凭 CLAUDE.md 判断职责并冷启动（验证引导文件自足性）
  b. W2 生产者侧：粘贴 `logs/extracted/3又见.txt` 一段 20 条 → 吸收 → 简报
  c. W2 消费者侧：反推意图 → 生成 → 自检 → 模拟 KP 反馈局部重生成一次
  d. 防呆抽检：向"生产者"投喂一条写作意图，应被拒收并指路
- [ ] **Step 2: 按实测修订 CLAUDE.md**（路由是否清晰、冷启动是否自足、防呆措辞）
- [ ] **Step 3: 写验收报告**：各环节通过/失败、回放四维评分（复用 Task 8 方法，换 `3又见.txt` 片段）、遗留问题清单（v2 项归档：分线/偏离引导/自由模式/玩家已知信息/日后谈）
- [ ] **Step 4: 【KP校对】** 用户终验
- [ ] **Step 5: Commit**

```bash
git add CLAUDE.md docs/replays/ && git commit -m "feat: v1全链路验收通过与CLAUDE.md终化"
```

---

## Self-Review 记录

- **Spec 覆盖**：§4 五 skill → Task 4/7/8/9/10；§4.1 CLAUDE.md → Task 1/11；§4.2 单一写者 → Global Constraints + 各 skill 防呆；§5 格式 → Task 1(corpus规范)/4(卡片规范)/9(timeline/state规范)；§6 协议 → Task 8(6.4)/9(6.3)/4(6.1-6.2)；§7 W0-W3 → Task 8/9/11(冷启动与回路)、Task 10(收团)；§9 语料两层+锚点 → Task 2/3；§11 回放验收 → Task 8/11；§12 构建顺序 → 任务顺序一致。无缺口
- **占位符扫描**：无 TBD/TODO；所有内容性步骤给出了具体格式、配方或选取标准
- **命名一致性**：coc-prep/coc-pc-import/coc-producer/coc-consumer/coc-harvest 全文一致；伏笔编号 F#（Task 6 定义，Task 9 引用）；`campaign/amaranthine_desire/` 全文一致
