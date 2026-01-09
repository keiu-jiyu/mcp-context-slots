# 【例2-1】
# 文件名：mcp_slot_demo.py

import uuid
import time
from typing import List, Dict


# 定义一个Slot数据结构
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


# 构造用户投诉的上下文Slot列表
def build_complaint_slots() -> List[Slot]:
    slots = []

    # Slot 1：用户首次输入
    slots.append(Slot(
        slot_id=str(uuid.uuid4()),
        content="我购买的洗衣机启动后电机有异常响声，请尽快处理。",
        role="user",
        metadata={
            "timestamp": time.time(),
            "channel": "web_form",
            "user_id": "u12345"
        }
    ))

    # Slot 2：系统自动识别意图
    slots.append(Slot(
        slot_id=str(uuid.uuid4()),
        content="识别意图：产品故障-电机异常",
        role="system",
        metadata={
            "source": "intent_classifier_v2",
            "confidence": 0.94
        }
    ))

    # Slot 3：Agent发出初步回复
    slots.append(Slot(
        slot_id=str(uuid.uuid4()),
        content="已记录问题，请提供产品序列号与购机发票照片以便安排售后服务。",
        role="agent",
        metadata={
            "agent_id": "svc-agent-001",
            "status": "response_issued"
        }
    ))

    return slots


# 主程序执行：构建Slot并打印结果
if __name__ == "__main__":
    slots = build_complaint_slots()

    print("=== 构建的上下文Slot结构 ===")
    for idx, slot in enumerate(slots):
        print(f"\n[Slot {idx+1}]")
        for k, v in slot.to_dict().items():
            print(f"{k}: {v}")
