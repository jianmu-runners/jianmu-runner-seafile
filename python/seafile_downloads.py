import json
import os
import sys
import zipfile

import requests

username = os.getenv("JIANMU_USERNAME")
password = os.getenv("JIANMU_PASSWORD")
base_url = os.getenv("JIANMU_BASE_URL")
repo_id = os.getenv("JIANMU_REPO_ID")
download_dir_path = os.getenv("JIANMU_DOWNLOAD_DIR_PATH")
share_dir = os.getenv("JM_SHARE_DIR")

# 处理参数
if not (base_url.endswith("/")):
    base_url = base_url + "/"
if not download_dir_path.startswith("/"):
    download_dir_path = "/" + download_dir_path
if download_dir_path.endswith("/"):
    download_dir_path = download_dir_path.rstrip("/")

# 获取用户的token
acquire_token_data = {"username": username,
                      "password": password}
try:
    response = requests.post(base_url + 'api2/auth-token/', data=acquire_token_data)
except Exception as e:
    print("请求失败，请检查参数后重试，具体错误信息：", e)
    sys.exit(1)
token = response.text[10:50]
# 构建请求头
headers = {
    'Authorization': 'Token ' + token,
    'Accept': 'application/json; charset=utf-8; indent=4',
}


def generateResult(download_result):
    """生成结果"""
    resultJson = "{\n\t\"download_file_path\" : \"" + share_dir + "/" + download_result + "\"\n}"
    resultFile = open('/tmp/downloadResultFile', 'w', encoding='utf-8')
    resultFile.write(resultJson)
    resultFile.close()
    print(resultJson)


def zip_decompress(file_path, new_path):
    """
    支持中文的解压缩程序
    file_path：原zip文件路径
    new_path：新文件夹路径
    """
    z = zipfile.ZipFile(f'{file_path}', 'r')
    z.extractall(path=f"{new_path}")
    # 得到压缩包里所有文件
    zip_list = z.namelist()
    rename_dir = zip_list[0].split("/")[0]
    z.close()
    pre_files(share_dir + "/" + rename_dir)
    os.remove(file_path)

def pre_files(path):
    """前序遍历，遍历文件树"""
    # 执行重命名操作
    parent_dir = os.path.dirname(path)
    path_name = path.split("/")[-1]
    new_file_name = ""
    try:
        new_file_name = path_name.encode('cp437').decode('utf-8')
        os.rename(os.path.join(parent_dir, path_name), os.path.join(parent_dir, new_file_name))
    except:
        pass
    # 遍历当前目录所有文件及文件夹
    if os.path.isdir(parent_dir + "/" + new_file_name):
        file_list = os.listdir(parent_dir + "/" + new_file_name)
        # 准备循环判断每个元素是文件夹还是文件，是文件的话，更名，是文件夹的话，更名并递归
        for file in file_list:
            # 利用os.path.join()方法取得路径全名，并存入cur_path变量，否则每次只能遍历一层目录
            cur_path = os.path.join(parent_dir + "/" + new_file_name, file)
            pre_files(cur_path)


def singleFileDownload(download_dir_path):
    """单个文件下载"""
    file_name = download_dir_path.split("/")[-1]
    # 获取下载地址
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
    with open(share_dir + "/" + file_name, "wb") as code:
        code.write(response.content)

    generateResult(file_name)
    sys.exit(0)


def judgePathType(path):
    """判断文件类型"""
    parent_path = os.path.dirname(path)
    path_name = path.split("/")[-1]
    params = (
        ('p', parent_path),
    )
    response = requests.get(base_url + 'api2/repos/' + repo_id + '/dir/',
                            headers=headers, params=params)

    for i in range(len(response.json())):
        if path_name == response.json()[i]["name"] and response.json()[i]["type"] == "dir":
            return "dir"
        if path_name == response.json()[i]["name"] and response.json()[i]["type"] == "file":
            return "file"
    print("[ERROR] Please configure the correct file path")
    sys.exit(1)


def batchDownload(download_dir_path):
    """批量下载"""
    dir_name = "/" + download_dir_path.split("/")[-1]
    parent_dir = os.path.dirname(download_dir_path)
    params = (
        ('parent_dir', parent_dir),
        ('dirents', dir_name),
    )
    response = requests.get(base_url + 'api/v2.1/repos/' + repo_id + '/zip-task/',
                            headers=headers, params=params)

    zip_token = json.loads(response.text)["zip_token"]

    response = requests.get(base_url + "seafhttp/zip/" + zip_token)

    with open(share_dir + dir_name + ".zip", "wb") as code:
        code.write(response.content)

    # zip_decompress(share_dir + dir_name + ".zip", share_dir)

    generateResult(dir_name.lstrip("/"))
    exit(0)


file_type = judgePathType(download_dir_path)
if file_type == "dir":
    batchDownload(download_dir_path)
if file_type == "file":
    singleFileDownload(download_dir_path)

print("[ERROR] unknown error")
sys.exit(1)
