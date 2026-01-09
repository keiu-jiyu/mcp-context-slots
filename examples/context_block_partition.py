# 【例2-4】
# 文件名：context_block_partition.py

import uuid
import time
from typing import List, Dict


# 定义Slot结构
class Slot:
    def __init__(self, content: str, role: str, timestamp: float = None):
        self.slot_id = str(uuid.uuid4())
        self.content = content
        self.role = role
        self.timestamp = timestamp or time.time()

    def to_dict(self):
        return {
            "slot_id": self.slot_id,
            "content": self.content,
            "role": self.role,
            "timestamp": self.timestamp
        }


# 定义ContextBlock结构
class ContextBlock:
    def __init__(self, block_name: str):
        self.block_name = block_name
        self.slots: List[Slot] = []

    def add_slot(self, slot: Slot):
        self.slots.append(slot)

    def to_dict(self):
        return {
            "block_name": self.block_name,
            "slot_count": len(self.slots),
            "contents": [s.content for s in self.slots]
        }


# 模拟按“阶段”进行上下文划分
def build_context_blocks() -> List[ContextBlock]:
    intro_block = ContextBlock("Introduction Phase")
    tech_block = ContextBlock("Technical Q&A Phase")
    wrap_block = ContextBlock("Closing Phase")

    # 模拟插入Slot
    intro_block.add_slot(Slot("您好，我是候选人张伟，来自北京大学。", role="user"))
    intro_block.add_slot(Slot("您好张伟，请简单自我介绍并说明申请岗位。", role="interviewer"))

    tech_block.add_slot(Slot("请讲解一下Transformer的核心结构与优势。", role="interviewer"))
    tech_block.add_slot(Slot("Transformer通过多头注意力与位置编码实现了序列建模能力...", role="user"))

    wrap_block.add_slot(Slot("谢谢，您还有其他问题吗？", role="interviewer"))
    wrap_block.add_slot(Slot("没有了，感谢本次面试机会。", role="user"))

    return [intro_block, tech_block, wrap_block]


if __name__ == "__main__":
    blocks = build_context_blocks()
    print("=== ContextBlock分段结果 ===\n")
    for b in blocks:
        b_dict = b.to_dict()
        print(f"Block: {b_dict['block_name']}")
        print(f"Slot Count: {b_dict['slot_count']}")
        for c in b_dict['contents']:
            print(f"  - {c}")
        print("")
