import json
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 尝试自动检测系统中的中文字体
def get_available_fonts():
    """获取系统中可用的中文字体列表"""
    chinese_fonts = []
    for font in fm.findSystemFonts():
        try:
            font_name = fm.FontProperties(fname=font).get_name()
            if any(c in font_name for c in ['sim', 'hei', 'song', 'microsoft', 'yahei', 'deng']):
                chinese_fonts.append(font)
        except:
            continue
    return chinese_fonts

# 设置中文字体
def set_chinese_font():
    """设置支持中文的字体"""
    chinese_fonts = get_available_fonts()
    
    # 优先尝试的字体列表
    preferred_fonts = [
        'SimHei', 'WenQuanYi Micro Hei', 'Heiti TC',
        'Microsoft YaHei', 'DengXian', 'SimSun'
    ]
    
    # 尝试设置优先字体
    for font in preferred_fonts:
        try:
            plt.rcParams["font.family"] = font
            return True
        except:
            continue
    
    # 如果优先字体都不可用，尝试使用检测到的第一个中文字体
    if chinese_fonts:
        try:
            plt.rcParams["font.family"] = fm.FontProperties(fname=chinese_fonts[0]).get_name()
            return True
        except:
            pass
    
    # 如果所有尝试都失败，使用默认字体并警告
    print("警告：未找到合适的中文字体，可能导致中文显示异常")
    return False

# 确保负号正确显示
plt.rcParams["axes.unicode_minus"] = False

# 设置中文字体
set_chinese_font()

# 读取排序后的岗位数据
with open('test/sorted_jobs.json', 'r', encoding='utf-8') as f:
    jobs_sorted = json.load(f)

# 提取可视化所需数据（取前15个岗位，避免图表拥挤）
top_n = 15  # 可调整显示的岗位数量
positions = [job['position'] for job in jobs_sorted[:top_n]]
max_salaries = [job['max_salary'] for job in jobs_sorted[:top_n]]

# 创建条形图
plt.figure(figsize=(12, 8))  # 图表大小
bars = plt.barh(positions, max_salaries, color='skyblue')

# 在条形上标注薪资数值
for bar in bars:
    width = bar.get_width()
    plt.text(width + 0.5, bar.get_y() + bar.get_height()/2,
             f'{width}k', va='center')

# 设置图表标题和坐标轴标签
plt.title(f'岗位最高薪资排名（前{top_n}名）', fontsize=15)
plt.xlabel('最高薪资（k）', fontsize=12)
plt.ylabel('岗位名称', fontsize=12)

# 调整布局，避免内容被截断
plt.tight_layout()

# 保存图表为图片文件
plt.savefig('salary_ranking.png', dpi=300, bbox_inches='tight')
print("图表已保存为 salary_ranking.png")

# 显示图表
plt.show()
