from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from qdrant_client.http.models import PointStruct, Document
from dotenv import load_dotenv
import os
# 加载环境变量
load_dotenv()


client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
    cloud_inference=True,
)

# 删除集合（如果存在）
try:
    client.delete_collection(collection_name="hello_agents_vectors")
    print("集合已删除")
except:
    print("集合不存在或无法删除")
#
# # 用正确的维度重新创建（all-minilm-l6-v2 是 384 维）
# client.create_collection(
#     collection_name="hello_agents_vectors",
#     vectors_config=VectorParams(size=384, distance=Distance.COSINE)
# )
#
# points = [
#     PointStruct(
#         id=1,
#         payload={"topic": "cooking", "type": "dessert"},
#         vector=Document(
#             text="Recipe for baking chocolate chip cookies requires flour, sugar, eggs, and chocolate chips.",
#             model="sentence-transformers/all-minilm-l6-v2"
#         )
#     )
# ]
#
# client.upsert(collection_name="hello_agents_vectors", points=points)
#
# points = client.query_points(collection_name="hello_agents_vectors", query=Document(
#     text="Recipe for baking chocolate chip cookies requires flour",
#     model="sentence-transformers/all-minilm-l6-v2"
# ))
#
# print(points)