#!/usr/bin/env python3
"""
生成2月2日到3月11日的模拟关键词数据
基于现有趋势进行线性外推和随机波动
"""

import json
import random
from datetime import datetime, timedelta

# 读取现有数据
with open('all_keywords.json', 'r') as f:
    data = json.load(f)

# 需要生成的日期范围
start_date = datetime(2026, 2, 2)
end_date = datetime(2026, 3, 11)

def generate_next_value(history_values, last_conversion, last_click_rate):
    """基于历史数据生成下一个值"""
    if len(history_values) < 2:
        return history_values[-1] if history_values else 1000
    
    # 计算最近的趋势
    recent = history_values[-7:]  # 最近7个点
    if len(recent) >= 2:
        avg_change = (recent[-1] - recent[0]) / len(recent)
    else:
        avg_change = 0
    
    # 基于趋势预测下一个值，添加随机波动
    base_value = history_values[-1]
    trend_factor = avg_change * 0.5  # 趋势权重50%
    random_factor = base_value * random.uniform(-0.05, 0.05)  # 随机波动±5%
    
    next_value = int(base_value + trend_factor + random_factor)
    next_value = max(1000, next_value)  # 最小值1000
    
    return next_value

# 为每个关键词生成数据
new_dates_generated = 0
current_date = start_date

while current_date <= end_date:
    date_str = current_date.strftime('%Y-%m-%d')
    
    for keyword in data:
        history = data[keyword]
        last_entry = history[-1]
        
        # 生成新数据点
        new_value = generate_next_value(
            [h['value'] for h in history],
            last_entry['conversion'],
            last_entry['click_rate']
        )
        
        # 转化率随机波动
        new_conversion = max(0.01, min(0.5, last_entry['conversion'] + random.uniform(-0.005, 0.005)))
        
        # 点击率随机波动
        new_click_rate = max(0.1, min(2.0, last_entry['click_rate'] + random.uniform(-0.05, 0.05)))
        
        # 添加新数据点
        history.append({
            'date': date_str,
            'value': new_value,
            'conversion': round(new_conversion, 4),
            'click_rate': round(new_click_rate, 4)
        })
    
    new_dates_generated += 1
    current_date += timedelta(days=1)
    
    if new_dates_generated % 10 == 0:
        print(f"已生成 {new_dates_generated} 天数据...")

# 保存更新后的数据
print(f"\n生成完成！共生成 {new_dates_generated} 天数据")
print(f"数据现在从 2025-01-01 到 2026-03-11")
print(f"总数据点数: {len(data[list(data.keys())[0]])}")

# 保存数据
with open('all_keywords.json', 'w') as f:
    json.dump(data, f)

print("\n数据已保存到 all_keywords.json")
