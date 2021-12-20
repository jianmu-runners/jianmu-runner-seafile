import json
import sys
import requests
import os

username = os.getenv("JIANMU_USERNAME")
password = os.getenv("JIANMU_PASSWORD")
base_url = os.getenv("JIANMU_BASE_URL")
repo_id = os.getenv("JIANMU_REPO_ID")
dir_path = os.getenv("JIANMU_DIR_PATH")
upload_file_path = os.getenv("JIANMU_UPLOAD_FILE_PATH")

# 处理返回结果
def handleResult(response):
    # 生成结果文件
    resultFile = open('/tmp/resultFile', 'w', encoding='utf-8')
    lstrip_dir_path = dir_path.rstrip("/")
    remote_file_url = base_url + "lib/" + repo_id + "/file" + lstrip_dir_path + "/" + upload_file_name
    result = "{\n\t\"remote_file_url\" : \"" + remote_file_url + "\"\n}"
    resultFile.write(result)
    resultFile.close()

    # 打印结果日志
    resultJson = {
        "remote_file_url": remote_file_url.__str__(),
        "upload_link": response.url.__str__(),
        "encoding": response.encoding.__str__(),
        "headers": response.headers.__str__(),
        "reason": response.reason.__str__(),
        "status_code": response.status_code
    }
    print("response: ")
    print(json.dumps(resultJson, sort_keys=True, indent=2) + "")
    # resultJson ="{\"remote_file_url\" : \""+ remote_file_url +"\"}"

# 对输入参数进行一些前置操作
upload_file_name = upload_file_path.split("/")[-1]
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

# 构建headers
headers = {
    'Authorization': 'Token ' + token
}

# 上传之前，尝试更新文件，更新成功即成功覆盖源文件。更新失败执行上传操作
# 以下是执行更新操作

# 获取更新链接
try:
    response = requests.get(base_url + 'api2/repos/' + repo_id + '/update-link/',
                            headers=headers)
except Exception as e:
    print("请求失败，请检查参数后重试，具体错误信息：", e)
    sys.exit(1)

update_link = response.text.replace("\"", "")

# 执行更新
update_dir_path = dir_path + upload_file_name if dir_path.endswith("/") else dir_path + "/" +upload_file_name

files = {
    'file': (upload_file_name, open(upload_file_path, 'rb')),
    'target_file': (None, update_dir_path),
}

try:
    response = requests.post(update_link, headers=headers, files=files)
except Exception as e:
    print("请求失败，请检查参数后重试，具体错误信息：", e)
    sys.exit(1)

# 更新成功
if not response.status_code == 441:
    handleResult(response)
    exit(0)

# 更新失败，进行上传操作
# 获得上传链接
try:
    response = requests.get(base_url + 'api2/repos/' + repo_id + '/upload-link/',
                            headers=headers)
except Exception as e:
    print("请求失败，请检查参数后重试，具体错误信息：", e)
    sys.exit(1)

upload_link = response.text.replace("\"", "")

# 执行上传
try:
    files = {
        'file': (upload_file_name, open(upload_file_path, 'rb')),
        'parent_dir': (None, dir_path)
    }
    response = requests.post(upload_link, headers=headers, files=files)
    handleResult(response)
except Exception as e:
    print("请求失败，请检查参数后重试。具体错误信息：", e)
    sys.exit(1)
