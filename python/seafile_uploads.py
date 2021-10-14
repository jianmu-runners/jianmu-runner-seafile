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

if not (base_url.endswith("/")):
    base_url = base_url + "/"

# 获取用户的token
# curl -d "username=huang.xi@99cloud.net&password=huangxi1014" https://seafile.sh.99cloud.net/api2/auth-token/
acquire_token_data = {"username": username,
                      "password": password}
try:
    response = requests.post(base_url + 'api2/auth-token/', data=acquire_token_data)
except Exception as e:
    print("请求失败，请检查参数后重试，具体错误信息：", e)
    sys.exit(1)

token = response.text[10:50]

# 获得上传链接
# curl -H "Authorization: Token 4ca89a3b16291a8d8d6170e0a63b12f8d2356ac3" https://seafile.sh.99cloud.net/api2/repos/5066b940-2fc3-4da2-9da2-d8ec301020d9/upload-link/
get_upload_link_headers = {
    'Authorization': 'Token ' + token
}

try:
    response = requests.get(base_url + 'api2/repos/' + repo_id + '/upload-link/',
                            headers=get_upload_link_headers)
except Exception as e:
    print("请求失败，请检查参数后重试，具体错误信息：", e)
    sys.exit(1)

upload_link = response.text.replace("\"", "")

# 执行上传
# curl -H "Authorization: Token 4ca89a3b16291a8d8d6170e0a63b12f8d2356ac3" -F file=@Dockerfile_aliyun -F filename=Dockerfile_aliyun -F parent_dir=/fly https://seafile.sh.99cloud.net/seafhttp/upload-api/e639c020-d548-45d7-bcc0-8b0936002187
upload_file_headers = {
    'Authorization': 'Token ' + token
}

upload_file_name = upload_file_path.split("/")[-1]
try:
    files = {
        'file': (upload_file_name, open(upload_file_path, 'rb')),
        'parent_dir': (None, dir_path)
    }
    response = requests.post(upload_link, headers=upload_file_headers, files=files)
except Exception as e:
    print("请求失败，请检查参数后重试。具体错误信息：", e)
    sys.exit(1)

hash = response.text


# 用来存放返回文件的类
class Result(object):
    def __init__(self, remote_file_url):
        self.remote_file_url = remote_file_url


# 处理返回结果
def handleResult(remote_file_url, response):
    resultFile = open('/tmp/resultFile', 'w', encoding='utf-8')
    result = Result(remote_file_url)
    resultFile.write(json.dumps(result.__dict__))
    resultFile.close()

    resultJson = {
        "remote_file_url": remote_file_url.__str__(),
        "upload_link": response.url.__str__(),
        "encoding": response.encoding.__str__(),
        "headers": response.headers.__str__(),
        "reason": response.reason.__str__(),
        "status_code": response.status_code.__str__()
    }

    # resultJson ="{\"remote_file_url\" : \""+ remote_file_url +"\"}"
    print("response: ")
    print(json.dumps(resultJson, sort_keys=True, indent=2))

if dir_path == "/":
    handleResult(base_url + "lib/" + repo_id + "/file" + dir_path + upload_file_name, response)
else:
    handleResult(base_url + "lib/" + repo_id + "/file" + dir_path + "/" + upload_file_name, response)
