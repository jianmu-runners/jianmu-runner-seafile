import json
import os
import sys

import requests

cover_flag = os.getenv("JIANMU_COVER_FLAG")
username = os.getenv("JIANMU_USERNAME")
password = os.getenv("JIANMU_PASSWORD")
base_url = os.getenv("JIANMU_BASE_URL")
repo_id = os.getenv("JIANMU_REPO_ID")
dir_path = os.getenv("JIANMU_DIR_PATH")
upload_file_path = os.getenv("JIANMU_UPLOAD_FILE_PATH")

# 对输入参数进行一些前置操作
if upload_file_path.endswith("/"):
    upload_file_path = upload_file_path.rstrip("/")
upload_file_name = upload_file_path.split("/")[-1]
upload_parent_dir = upload_file_path.split("/")[1]
if not (base_url.endswith("/")):
    base_url = base_url + "/"
if not (dir_path.startswith("/")):
    dir_path = "/" + dir_path
if (dir_path.endswith("/")):
    dir_path = dir_path.rstrip("/")

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


def generateRemoteFileUrl():
    """生成远端服务器已上传文件的地址"""
    if os.path.isdir(upload_file_path):
        remote_file_url = base_url + "#my-libs/lib/" + repo_id + dir_path + upload_file_path
    else:
        remote_file_url = base_url + "lib/" + repo_id + "/file" + dir_path + "/" + upload_file_name
    return remote_file_url


def generateResultFile():
    """生成结果文件"""
    remote_file_url = generateRemoteFileUrl()
    resultFile = open('/tmp/resultFile', 'w', encoding='utf-8')
    result = "{\n\t\"remote_file_url\" : \"" + remote_file_url + "\"\n}"
    resultFile.write(result)
    resultFile.close()


def printResultLog(response):
    """打印结果日志"""
    remote_file_url = generateRemoteFileUrl()
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


def update():
    """以下是执行更新操作"""
    # 获取更新链接
    try:
        response = requests.get(base_url + 'api2/repos/' + repo_id + '/update-link/',
                                headers=headers)
    except Exception as e:
        print("请求失败，请检查参数后重试，具体错误信息：", e)
        sys.exit(1)

    update_link = response.text.replace("\"", "")

    # 执行更新
    update_dir_path = dir_path + "/" + upload_file_name

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
        printResultLog(response)
        generateResultFile()
        exit(0)
    print("更新文件失败，将上传此文件")


def upload(upload_file_name, upload_file_path, dir_path):
    """以下是执行上传单个文件操作"""
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
        printResultLog(response)
    except Exception as e:
        print("请求失败，请检查参数后重试。具体错误信息：", e)
        sys.exit(1)


def deleteDir(delete_dir_path):
    params = (
        ('p', delete_dir_path),
    )
    try:
        requests.delete(base_url + 'api2/repos/' + repo_id + '/dir/',
                        headers=headers, params=params)
    except Exception as e:
        print("请求失败，请检查参数后重试。具体错误信息：", e)
        sys.exit(1)


def existDir(path):
    """是否存在此文件夹"""
    parent_path = os.path.dirname(path)
    path_name = path.split("/")[-1]
    params = (
        ('p', parent_path),
    )
    response = requests.get(base_url + 'api2/repos/' + repo_id + '/dir/',
                            headers=headers, params=params)

    for i in range(len(response.json())):
        if path_name == response.json()[i]["name"] and response.json()[i]["type"] == "dir":
            return True
    return False


def createDir(create_dir_path):
    """执行创建文件夹的操作"""
    # 创建文件夹之前判断一下，文件夹是否存在
    if existDir(create_dir_path):
        return

    params = (
        ('p', create_dir_path),
    )
    data = {
        'operation': 'mkdir'
    }
    try:
        response = requests.post(base_url + 'api2/repos/' + repo_id + '/dir/', headers=headers, params=params,
                                 data=data)
    except Exception as e:
        print("请求失败，请检查参数后重试。具体错误信息：", e)
        sys.exit(1)
    if not response.status_code == 201:
        print("请求失败，具体错误信息：" + response.text)


def widelyUpload(path):
    """宽泛的上传函数，既可以创建文件夹，也可以上传文件"""
    if os.path.isdir(path):
        # 发送请求，创建文件夹
        createDir(dir_path + path)
    else:
        # 发送请求，上传文件
        upload_file_name = path.split("/")[-1]
        local_dir_path = os.path.dirname(path)
        upload(upload_file_name, path, dir_path + local_dir_path)


def pre_files(path):
    """前序遍历，遍历文件树"""
    # 执行上传操作
    widelyUpload(path)
    # 遍历当前目录所有文件及文件夹
    if os.path.isdir(path):
        file_list = os.listdir(path)
        # 准备循环判断每个元素是文件夹还是文件，是文件的话，上传，是文件夹的话，递归
        for file in file_list:
            # 利用os.path.join()方法取得路径全名，并存入cur_path变量，否则每次只能遍历一层目录
            cur_path = os.path.join(path, file)
            pre_files(cur_path)


def batchUpload(upload_file_path):
    """以下是执行批量上传操作"""
    path_list = upload_file_path.split("/")
    path_list.remove("")
    cur_dir = ""
    # 创建前置文件夹
    for i in range(len(path_list) - 1):
        cur_dir = cur_dir + "/" + path_list[i]
        createDir(dir_path + cur_dir)

    pre_files(upload_file_path)


if not os.path.isdir(upload_file_path) and not os.path.isfile(upload_file_path):
    print("请配置正确的文件/文件夹路径")
    exit(1)

# 上传文件
if os.path.isfile(upload_file_path):
    # 更新文件，更新成功即成功覆盖源文件。若更新失败执行上传操作
    if cover_flag == "true":
        update()
        upload(upload_file_name, upload_file_path, dir_path)
        generateResultFile()
    else:
        # 直接执行上传操作
        upload(upload_file_name, upload_file_path, dir_path)
        generateResultFile()
else:
    if cover_flag == "true":
        # 尝试删除
        deleteDir(dir_path + "/" + upload_parent_dir)
        # 执行批量上传
        batchUpload(upload_file_path)
        generateResultFile()
    else:
        # 批量上传文件
        batchUpload(upload_file_path)
        generateResultFile()
