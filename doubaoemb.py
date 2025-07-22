from volcenginesdkarkruntime import Ark

client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)

print("----- embeddings request -----")
resp = client.embeddings.create(
    model="doubao-embedding-large-text-250515",
    input=["花椰菜又称菜花、花菜，是一种常见的蔬菜。"]
)
print(resp)