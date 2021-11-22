import sys
import requests
import os
import shutil


username = os.getenv("JIANMU_USERNAME")
password = os.getenv("JIANMU_PASSWORD")
base_url = os.getenv("JIANMU_BASE_URL")
repo_id = os.getenv("JIANMU_REPO_ID")
download_dir_path = os.getenv("JIANMU_DOWNLOAD_DIR_PATH")
share_dir = os.getenv("JM_SHARE_DIR")

if not (base_url.endswith("/")):
    base_url = base_url + "/"

# 获取用户的token
acquire_token_data = {"username": username,
                      "password": password}
try:
    response = requests.post(base_url + 'api2/auth-token/', data=acquire_token_data)
except Exception as e:
    print("请求失败，请检查参数后重试，具体错误信息：", e)
    sys.exit(1)

token = response.text[10:50]

# 获取下载地址
headers = {
    'Authorization': 'Token ' + token,
    'Accept': 'application/json; charset=utf-8; indent=4',
}

params = (
    ('p', download_dir_path),
)

try:
    response = requests.get(base_url + 'api2/repos/' + repo_id + '/file/',
                            headers=headers, params=params)
except Exception as e:
    print("请求失败，请检查参数后重试，具体错误信息：", e)
    sys.exit(1)

url = response.text
download_url = url.strip(url[0] + url[-1])

# 执行下载
try:
    response = requests.get(download_url)
except Exception as e:
    print("请求失败，请检查参数后重试，具体错误信息：", e)
    sys.exit(1)

# 写入硬盘
file_name = download_dir_path.split("/")[-1]
with open(file_name, "wb") as code:
    code.write(response.content)

shutil.move("./" + file_name, share_dir)

resultJson = "{\"download_file_path\" : \"" + share_dir + "/" + file_name + "\"}"
print(resultJson)