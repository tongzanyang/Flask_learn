# @Version  : 1.0
# @Author   : 故河
# import json
#
#
# # 读取 JSONL 文件并提取所有 reference 字段的值
# def load_docs_from_jsonl(file_path):
#     with open(file_path, "r", encoding="utf-8") as f:
#         docs = [json.loads(line).get("reference", []) for line in f]
#         docs = [item for sublist in docs for item in sublist]  # 展平嵌套列表
#
#         # 去重
#         seen = set()
#         unique_docs = []
#         for item in docs:
#             if item not in seen:
#                 seen.add(item)
#                 unique_docs.append(item)
#
#         print(f"从 JSONL 文件中成功加载了 {len(docs)} 条文档数据，去重后剩余 {len(unique_docs)} 条。")
#     return unique_docs
#
#
# file_path = "fal_txt.jsonl"
# docs = load_docs_from_jsonl(file_path)  # 一个列表
# print(docs)
#
# # 将结果写入 JSON 文件
# with open("unique_data.json", "w", encoding="utf-8") as files:
#     json.dump(docs, files, ensure_ascii=False, indent=4)

import requests
import json

def stream_chat(prompt, server_ip="192.168.0.168", port=11434):
    # 设置请求头和请求体
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "deepseek-r1:14b",
        "prompt": prompt,
        "stream": True
    }

    try:
        # 发送 POST 请求到 Ollama API
        url = f"http://{server_ip}:{port}/api/generate"
        response = requests.post(
            url,
            headers=headers,
            json=data,
            stream=True
        )

        # 检查响应状态码
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            return

        # 处理流式响应
        full_response = ""
        for chunk in response.iter_content(chunk_size=None):
            if chunk:
                # 解码 chunk
                chunk_str = chunk.decode("utf-8")
                # 移除可能的空格和换行
                chunk_str = chunk_str.strip()
                if chunk_str:
                    # 解析 JSON
                    try:
                        chunk_json = json.loads(chunk_str)
                        # 提取 response 字段
                        if "response" in chunk_json:
                            response_text = chunk_json["response"]
                            full_response += response_text
                            print(response_text, end="", flush=True)
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON: {chunk_str}")

        print()  # 换行以便后续输出

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")

if __name__ == "__main__":
    while True:
        # 输入你的问题
        user_input = input("请输入你的问题（按回车键发送）：")
        print("模型回答：")
        # 调用流式问答函数
        stream_chat(user_input)