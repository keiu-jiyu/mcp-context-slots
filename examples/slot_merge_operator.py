# 【例2-5】
# 文件名：slot_merge_operator.py

import uuid
import time
from typing import List, Dict


# 定义Slot结构
class Slot:
    def __init__(self, content: str, role: str, source: str = None):
        self.slot_id = str(uuid.uuid4())
        self.content = content
        self.role = role
        self.timestamp = time.time()
        self.source = source

    def to_dict(self):
        return {
            "slot_id": self.slot_id,
            "content": self.content,
            "role": self.role,
            "timestamp": self.timestamp,
            "source": self.source
        }


# 模拟Slot压缩算子（简化为句合并+去冗余关键词）
def compress_slots(slots: List[Slot]) -> Slot:
    unique_keywords = set()
    merged_sentences = []

    for slot in slots:
        text = slot.content
        merged_sentences.append(text)
        for word in text.split("，"):
            unique_keywords.add(word.strip())

    # 模拟摘要合并结果（真实项目中可换为LLM摘要）
    compressed_summary = "；".join(sorted(unique_keywords))
    return Slot(
        content=f"综合用户反馈：{compressed_summary}",
        role="compressed_summary",
        source="merge_operator"
    )


# 主程序
if __name__ == "__main__":
    # 模拟多个用户评价Slot
    raw_slots = [
        Slot("电池续航还不错，一天一充就够用了", role="user"),
        Slot("屏幕显示清晰，晚上护眼模式也很舒服", role="user"),
        Slot("手机反应快，就是充电发热有点明显", role="user"),
        Slot("续航确实比上一代强很多，适合重度用户", role="user"),
    ]

    compressed = compress_slots(raw_slots)

    print("=== 原始Slot内容 ===")
    for idx, s in enumerate(raw_slots):
        print(f"[{idx+1}] {s.content}")

    print("\n=== 压缩后Slot ===")
    print(f"SlotID: {compressed.slot_id}")
    print(f"Role: {compressed.role}")
    print(f"Source: {compressed.source}")
    print(f"Content: {compressed.content}")
