import uuid
import time
from typing import List, Dict, Optional

# ==========================================
# 1. 基础结构定义 (Foundation)
# ==========================================

# [对应 例2-1] Slot 原子定义
class Slot:
    def __init__(self, content: str, role: str, metadata: Dict = None, priority: int = 1):
        self.slot_id = str(uuid.uuid4())
        self.content = content
        self.role = role
        # [对应 例2-1] metadata 存储元数据，priority 用于 [例2-3] 的保留策略
        self.metadata = metadata or {}
        self.priority = priority 
        self.timestamp = time.time()

    def __repr__(self):
        # 打印时的简略显示
        return f"[{self.role.upper()} | Prio:{self.priority}] {self.content[:30]}..."

# ==========================================
# 2. 上下文管理器 (Core Logic)
# ==========================================

class ContextManager:
    def __init__(self, max_slots_limit: int = 6):
        self.slots: List[Slot] = []
        self.max_slots_limit = max_slots_limit
        
        # 初始化：添加系统指令（高优先级，永不删除）
        self.add_slot(Slot(
            content="你是一个专业的硬件维修专家，请简明扼要地回答问题。",
            role="system",
            priority=100, # 最高优先级
            metadata={"type": "system_instruction"}
        ))

    # [对应 例2-4] 添加 Slot 的通用入口
    def add_slot(self, slot: Slot):
        self.slots.append(slot)
        # 每次添加后，检查是否需要优化上下文
        self._check_and_optimize()

    # [对应 例2-2] RAG 检索增强
    def inject_rag_knowledge(self, query: str):
        print(f"--- [系统] 正在为 '{query}' 检索知识库 ---")
        # 模拟检索过程
        retrieved_text = "【知识库】设备红灯闪烁通常意味着电源模块过热，建议断电静置10分钟。"
        
        rag_slot = Slot(
            content=retrieved_text,
            role="system",
            priority=10, # 较高优先级，尽量保留
            metadata={"source": "vector_db", "query": query, "type": "RAG"}
        )
        self.add_slot(rag_slot)

    # [对应 例2-5] 压缩算子：将多个 Slot 合并为一个摘要
    def _compress_slots(self, slots_to_compress: List[Slot]) -> Slot:
        # 模拟 LLM 摘要过程
        raw_texts = [s.content for s in slots_to_compress]
        merged_content = " -> ".join(raw_texts)
        summary_text = f"【历史对话摘要】用户之前询问了故障细节，经过多轮排查 ({merged_content[:50]}...)"
        
        return Slot(
            content=summary_text,
            role="system", # 摘要通常作为 System 提示词存在
            priority=50,   # 摘要的优先级很高，因为它是历史的浓缩
            metadata={"type": "compressed_summary", "source_count": len(slots_to_compress)}
        )

    # [对应 例2-3] & [例2-5] 核心优化策略
    def _check_and_optimize(self):
        if len(self.slots) <= self.max_slots_limit:
            return

        print(f"\n>>> [触发策略] 当前 Slot 数 ({len(self.slots)}) 超过限制 ({self.max_slots_limit})，开始优化...")
        
        # 策略：
        # 1. 保留 System 指令 (Priority >= 100)
        # 2. 保留最近的 2 条消息 (Recency)
        # 3. 对中间的消息进行压缩 (Compression)
        
        system_slots = [s for s in self.slots if s.priority >= 100]
        recent_slots = self.slots[-2:] # 最后两条
        
        # 中间待处理的 Slot（排除掉系统指令和最近的两条）
        middle_slots = [s for s in self.slots if s not in system_slots and s not in recent_slots]
        
        if middle_slots:
            print(f"    - 正在压缩中间的 {len(middle_slots)} 条消息...")
            compressed_slot = self._compress_slots(middle_slots)
            
            # [对应 例2-3] 重构链条
            self.slots = system_slots + [compressed_slot] + recent_slots
            print("    - 优化完成。")
        else:
            # 简单的 FIFO 兜底
            self.slots.pop(1)

    # [对应 例2-6] 渲染：生成发给 LLM 的 Prompt
    def get_render_prompt(self) -> List[Dict]:
        prompt = []
        for s in self.slots:
            # 简单适配 OpenAI 格式
            role_map = {"user": "user", "agent": "assistant", "system": "system"}
            prompt.append({
                "role": role_map.get(s.role, "system"),
                "content": s.content
            })
        return prompt

    # 调试打印用
    def print_current_status(self):
        print(f"\n=== 当前上下文状态 (Slot数: {len(self.slots)}) ===")
        for i, s in enumerate(self.slots):
            meta_info = f"[Prio:{s.priority}]"
            if "type" in s.metadata:
                meta_info += f" [{s.metadata['type']}]"
            print(f"{i}. {meta_info} {s.role.upper()}: {s.content[:40]}...")
        print("============================================\n")


# ==========================================
# 3. 模拟主程序 (Simulation)
# ==========================================

if __name__ == "__main__":
    # 初始化管理器，设定最大容量为 6 条 Slot
    ctx = ContextManager(max_slots_limit=6)
    
    # --- 阶段 1: 用户接入 ---
    print("--- 阶段 1: 用户咨询 ---")
    ctx.add_slot(Slot("你好，我的机器报警了。", role="user", priority=1))
    ctx.add_slot(Slot("请描述一下报警灯的颜色。", role="agent", priority=1))
    ctx.print_current_status()

    # --- 阶段 2: 触发 RAG ---
    print("--- 阶段 2: 知识库检索 ---")
    ctx.add_slot(Slot("是红灯在一直闪烁。", role="user", priority=1))
    # 系统检测到关键词，自动注入知识
    ctx.inject_rag_knowledge("红灯闪烁")
    ctx.add_slot(Slot("根据手册，这可能是过热，请问您使用了多久？", role="agent", priority=1))
    ctx.print_current_status()

    # --- 阶段 3: 多轮对话导致上下文溢出 ---
    print("--- 阶段 3: 模拟长对话 (触发压缩) ---")
    # 此时 Slot 数约为 6，再加两条就会触发优化
    time.sleep(0.1)
    ctx.add_slot(Slot("大概用了3个小时吧。", role="user", priority=1))
    
    # 这条加入后，总数超过 6，将触发 _check_and_optimize
    ctx.add_slot(Slot("那请先关机，我们尝试冷却一下。", role="agent", priority=1))
    
    # 打印最终状态，观察中间的消息是否变为了“摘要 Slot”
    ctx.print_current_status()

    # --- 阶段 4: 最终渲染 ---
    print("--- 阶段 4: 发送给 LLM 的 Prompt ---")
    final_prompt = ctx.get_render_prompt()
    for msg in final_prompt:
        print(msg)
