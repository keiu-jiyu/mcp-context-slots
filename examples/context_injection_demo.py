# 【例2-6】
# 文件名：context_injection_demo.py

import uuid
import time
from typing import List, Dict


# Slot结构定义
class Slot:
    def __init__(self, content: str, role: str):
        self.slot_id = str(uuid.uuid4())
        self.content = content
        self.role = role
        self.timestamp = time.time()

    def to_prompt_line(self) -> str:
        return f"{self.role.upper()}: {self.content}"

# 构造inject函数（单个Slot注入）
def inject(slot: Slot, context: List[str]) -> List[str]:
    context.append(slot.to_prompt_line())
    return context

# 构造injectChain函数（Slot链注入）
def injectChain(slots: List[Slot], context: List[str]) -> List[str]:
    for s in slots:
        context.append(s.to_prompt_line())
    return context

# 示例运行主程序
if __name__ == "__main__":
    context_window = []

    # 用户最新输入（单注入）
    user_input = Slot("我家的空调插上电源就断电，请问是什么原因？", role="user")
    context_window = inject(user_input, context_window)

    # 历史诊断链（多Slot注入）
    history_slots = [
        Slot("空调在低温环境下启动，可能引起压缩机过载", role="agent"),
        Slot("建议检查电源线路是否老化，使用稳压器供电", role="agent")
    ]
    context_window = injectChain(history_slots, context_window)

    # 构造最终Prompt片段
    print("=== 构造后的上下文Prompt片段 ===\n")
    for line in context_window:
        print(line)
