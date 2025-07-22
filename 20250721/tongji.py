import json

def sum_amount_for_course(data, target_course_id=20):
    total_amount = 0
    for item in data.get('items', []):
        if item.get('courseId') == target_course_id:
            # if(item.get('amount') > 0):
                total_amount += float(item.get('amount'))
    return total_amount

# 举例加载数据和调用
with open('20250721/record.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

total_20 = sum_amount_for_course(data, 20)
total_35 = sum_amount_for_course(data, 35)
print(f"amount总和为: {(total_20 * (1 + 0.195) + total_35 * (1 + 0.25)) * 0.93}")
