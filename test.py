import requests

# Flask应用的上传API URL
url = 'http://127.0.0.1:5000/upload'

# 要上传的图片文件
file_path = 'testimg.png'

# 打开图片文件并发送POST请求
with open(file_path, 'rb') as f:
    files = {'image': (file_path, f)}
    response = requests.post(url, files=files)

# 打印响应
print(response.text)
