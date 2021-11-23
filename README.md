# jianmu-runner-seafile

### 介绍

操作seafile

### seafile文件上传

#### 输入参数

```
username: 用户名
password: 密码
base_url: 基础url
repo_id: 仓库id
dir_path: 远端文件路径
upload_file_path: 本地的上传路径含文件名
```

#### 输出参数

```
remote_file_url: seafile中文件路径
```

#### 构建docker镜像

```
# 创建docker镜像
docker build -t jianmudev/jianmu-runner-seafile:${version} -f dockerfile/Dockerfile .

# 上传docker镜像
docker push jianmudev/jianmu-runner-seafile:${version}
```

#### 用法

```
# 1.0.1版本及以下
docker run --rm \
  -e JIANMU_USERNAME=xxx \
  -e JIANMU_PASSWORD=xxx \
  -e JIANMU_BASE_URL=xxx \
  -e JIANMU_REPO_ID=xxx \
  -e JIANMU_DIR_PATH=xxx \
  -e JIANMU_UPLOAD_FILE_PATH=xxx \
  jianmudev/jianmu-runner-seafile:${version}
  
# 1.0.2版本及以上
docker run --rm \
  -e JIANMU_USERNAME=xxx \
  -e JIANMU_PASSWORD=xxx \
  -e JIANMU_BASE_URL=xxx \
  -e JIANMU_REPO_ID=xxx \
  -e JIANMU_DIR_PATH=xxx \
  -e JIANMU_UPLOAD_FILE_PATH=xxx \
  jianmudev/jianmu-runner-seafile:${version} \
  /usr/local/bin/seafile_uploads.py
```

### seafile文件下载

#### 输入参数

```
username: 用户名
password: 密码
base_url: 基础url
repo_id: 仓库id
download_dir_path: 指定下载文件的特定路径
```

#### 输出参数

```
download_file_path: 下载成功后文件路径
```

#### 构建docker镜像

```
# 创建docker镜像
docker build -t jianmudev/jianmu-runner-seafile:${version} -f dockerfile/Dockerfile .

# 上传docker镜像
docker push jianmudev/jianmu-runner-seafile:${version}
```

#### 用法

```
docker run --rm \
  -e JIANMU_USERNAME=xxx \
  -e JIANMU_PASSWORD=xxx \
  -e JIANMU_BASE_URL=xxx \
  -e JIANMU_REPO_ID=xxx \
  -e JIANMU_DIR_PATH=xxx \
  -e JIANMU_UPLOAD_FILE_PATH=xxx \
  jianmudev/jianmu-runner-seafile:${version} \
  /usr/local/bin/seafile_downloads.py
```
