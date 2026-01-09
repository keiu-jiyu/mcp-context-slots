# 【例2-3】
# 文件名：slot_chain_rebuild.py

import uuid
import time
from typing import List, Dict


class Slot:
    def __init__(self, content: str, role: str, priority: int = 1):
        self.slot_id = str(uuid.uuid4())
        self.content = content
        self.role = role
        self.timestamp = time.time()
        self.priority = priority  # 用于后续语义保留策略

    def to_dict(self):
        return {
            "slot_id": self.slot_id,
            "content": self.content,
            "role": self.role,
            "timestamp": self.timestamp,
            "priority": self.priority
        }


# 模拟Slot链构建与重构
class SlotChain:
    def __init__(self, max_tokens: int = 3):
        self.slots: List[Slot] = []
        self.max_tokens = max_tokens  # 简化Token预算限制，用Slot数量代替

    def add_slot(self, slot: Slot):
        self.slots.append(slot)
        self._rebuild_chain()

    def _rebuild_chain(self):
        # 如果超出Token预算，按优先级+时间裁剪
        if len(self.slots) <= self.max_tokens:
            return
        # 优先保留高priority + 最新Slot
        self.slots.sort(key=lambda x: (-x.priority, -x.timestamp))
        self.slots = self.slots[:self.max_tokens]
        # 恢复排序（按时间）
        self.slots.sort(key=lambda x: x.timestamp)

    def print_chain(self):
        print("=== 当前有效Slot链 ===")
        for s in self.slots:
            d = s.to_dict()
            print(f"SlotID: {d['slot_id']}")
            print(f"  Role: {d['role']}")
            print(f"  Content: {d['content']}")
            print(f"  Priority: {d['priority']}")
            print(f"  Timestamp: {int(d['timestamp'])}\n")


if __name__ == "__main__":
    chain = SlotChain(max_tokens=3)

    # 模拟用户与系统交互插入的多个Slot
    chain.add_slot(Slot("我的笔记本电脑开机风扇一直响", role="user", priority=1))
    chain.add_slot(Slot("识别为硬件故障咨询", role="system", priority=2))
    chain.add_slot(Slot("建议进行散热模块清灰", role="agent", priority=2))
    chain.add_slot(Slot("用户再次反馈清灰后仍旧高温", role="user", priority=3))
    chain.add_slot(Slot("建议更换导热硅脂或联系售后", role="agent", priority=2))

    chain.print_chain()
