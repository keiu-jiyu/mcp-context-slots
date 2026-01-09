# 【例2-2】
# 文件名：slot_compression_vs_retrieval.py

import uuid
import time
from typing import List, Dict

# Slot结构定义
class Slot:
    def __init__(self, slot_id: str, content: str, role: str, metadata: Dict):
        self.slot_id = slot_id
        self.content = content
        self.role = role
        self.metadata = metadata

    def to_dict(self):
        return {
            "slot_id": self.slot_id,
            "content": self.content,
            "role": self.role,
            "metadata": self.metadata
        }

# 构建Prompt压缩Slot
def build_compressed_prompt_slot(history: List[str]) -> Slot:
    compressed_summary = "用户咨询涉及产品连接失败、指示灯闪烁、固件更新等问题，已尝试重启设备无果。"
    return Slot(
        slot_id=str(uuid.uuid4()),
        content=compressed_summary,
        role="compressed_prompt",
        metadata={
            "source_slots": len(history),
            "compression_method": "llm-summary",
            "timestamp": time.time()
        }
    )

# 构建检索增强Slot（如来自FAQ文档）
def build_retrieval_slot() -> Slot:
    retrieved_passage = "若设备指示灯持续红闪，可能表示无法联网，请尝试连接手机热点验证网络模块是否损坏。"
    return Slot(
        slot_id=str(uuid.uuid4()),
        content=retrieved_passage,
        role="retrieved_knowledge",
        metadata={
            "retrieved_from": "FAQ_Doc_v3",
            "doc_id": "faq-102",
            "confidence": 0.88
        }
    )

# 主程序
if __name__ == "__main__":
    # 模拟对话历史
    history_inputs = [
        "我家路由器突然连不上设备",
        "灯一直闪，重启也没用",
        "是否需要重新配网或者恢复出厂设置？"
    ]

    prompt_slot = build_compressed_prompt_slot(history_inputs)
    retrieval_slot = build_retrieval_slot()

    print("=== Prompt压缩Slot ===")
    for k, v in prompt_slot.to_dict().items():
        print(f"{k}: {v}")

    print("\n=== 检索增强Slot ===")
    for k, v in retrieval_slot.to_dict().items():
        print(f"{k}: {v}")
