# 【例2-7】
# 文件名：compress_semantic_group_demo.py

import uuid
import time
from typing import List, Dict


# 定义Slot结构
class Slot:
    def __init__(self, content: str, role: str):
        self.slot_id = str(uuid.uuid4())
        self.content = content
        self.role = role
        self.timestamp = time.time()

    def to_dict(self):
        return {
            "slot_id": self.slot_id,
            "content": self.content,
            "role": self.role,
            "timestamp": self.timestamp
        }

# 定义语义分组结构（Semantic Group）
class SemanticGroup:
    def __init__(self, topic: str):
        self.topic = topic
        self.slots: List[Slot] = []

    def add_slot(self, slot: Slot):
        self.slots.append(slot)

    def compress(self) -> Slot:
        # 简化压缩方式为句子拼接，实际可替换为LLM摘要
        merged_text = "；".join([s.content for s in self.slots])
        summary_text = f"[{self.topic}] 客户反馈汇总：{merged_text}"
        return Slot(summary_text, role="compressed_summary")

# 主程序模拟执行
if __name__ == "__main__":
    # 创建一个“产品发热问题”语义组
    group = SemanticGroup(topic="产品发热问题")

    # 添加多个客服对话Slot
    group.add_slot(Slot("设备在视频播放30分钟后发烫严重", role="user"))
    group.add_slot(Slot("建议先关闭后台应用观察温度变化", role="agent"))
    group.add_slot(Slot("即便只运行一个应用也有发热现象", role="user"))
    group.add_slot(Slot("可能与系统更新后的功耗策略有关", role="agent"))

    # 执行compress生成摘要Slot
    compressed_slot = group.compress()

    # 输出结果
    print("=== 原始对话Slot ===")
    for s in group.slots:
        print(f"{s.role.upper()}: {s.content}")

    print("\n=== 压缩后生成的Slot ===")
    print(f"Role: {compressed_slot.role}")
    print(f"Content: {compressed_slot.content}")
