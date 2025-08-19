import json

# 1. 加载章节全量数据（catalogs.json）
with open("pointpredict\catalog\catalogs.json", "r", encoding="utf-8") as f:
    catalogs = json.load(f)

# 2. 构建id ->节点映射，方便查找
catalog_dict = {str(item["id"]): item for item in catalogs}

# 3. 定义递归函数，获取完整章节路径名称列表（从顶层到当前）
def get_full_catalog_path(catalog_id):
    path = []
    current_id = str(catalog_id)
    while current_id != "0" and current_id in catalog_dict:
        node = catalog_dict[current_id]
        path.append(node["name"])
        current_id = str(node.get("parentId", "0"))
    path.reverse()  # 从顶层到当前节点
    return " > ".join(path)

# 4. 遍历匹配结果文件，补充完整章节路径
with open("pointpredict/res.json", "r", encoding="utf-8") as f:
    results = json.load(f)

# 为每条记录添加一个完整章节路径列表
for record in results:
    full_paths = []
    for cid in record["predictedCatalogIds"]:
        full_path = get_full_catalog_path(cid)
        full_paths.append(full_path)
    record["predictedCatalogsNames"] = full_paths

# 5. 保存补充后的结果
with open("pointpredict/res_with_fullpath.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("✅ 已生成带完整章节路径的新结果文件 res_with_fullpath.json")
