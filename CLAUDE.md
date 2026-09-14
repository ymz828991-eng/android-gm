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
