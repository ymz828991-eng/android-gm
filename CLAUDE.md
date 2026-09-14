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
扫描 campaign/*/runs/*/ 下未完结的 run（state.md 存在且无"已完结"标记）：
- 无 → 空闲，等 KP 指令（备团/开新团）
- 一个 → 全量读该 run 的 state.md 与 timeline.md，游标复位到最新编号；消费者另读模组库的 routes.md 与当前场景卡恢复方位感
- 多个 → 列出候选（模组 / run / 最新事件号），等 KP 选定再冷启动——同时开多团合法
之后读取切换为增量模式（state 全读 + timeline 尾部）。

## 文件协议（详见各 skill）
- 布局：corpus/（语料）；campaign/<模组>/（**模组库**：scenes/npcs/drafts/module/routes，coc-prep 产出，跨团复用只读）；campaign/<模组>/runs/<团名>/（**一次开团**：pcs/timeline/state/recaps/raw.md，团名用日期或你起的名；raw.md 是 **KP 终稿**的逐字底账——开团时记录 KP 发言标签，吸收时过滤归档，只增不改）
- 单一写者：模组库写者 = prep（备团）+ harvest（收团"模组修正"，KP 确认）+ KP 本人（任何时候手改）；场景卡"PC 挂注"节永久留空，挂注活在各 run 的 PC 卡钩子里。**跑团进行中 skill 不写模组库**——变化走 state，修正攒到收团。timeline/state 只有生产者写；corpus 只有 harvest 写；消费者全程只读
- timeline.md 只增不改；state.md 保持一屏以内
