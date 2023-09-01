import requests

# 设置API端点URL
api_url = "http://127.0.0.1:5000/generate_tenant_data"

# 准备输入数据，这里是一个示例的对话历史
dialogue_history = """
tenant Q: Can I book a viewing for the property at 56 Mortimer road tomorrow at 3pm?
Agent: OK, let me check some information first. Do you intend to rent a property with your kids?
tenant Q: yes
Agent: Do you keep any pets
Tenant: Yes, we have a dog.
"""

# 创建一个包含输入数据的JSON payload
data = {
    "dialogue_history": dialogue_history
}

try:
    # 发起POST请求
    response = requests.post(api_url, json=data)

    # 检查响应状态码
    if response.status_code == 200:
        result = response.json()
        print("API Response:")
        print(result)
    else:
        print(f"API request failed with status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Error while making API request: {e}")
