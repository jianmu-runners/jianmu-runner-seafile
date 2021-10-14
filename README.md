# jianmu-runner-seafile

### 介绍

操作seafile的节点

### seafile上传节点

#### 输入参数

```
username: 用户名
password: 密码
base_url: 基础url
rep_name: 仓库名
dir_path: 远端文件路径
upload_file_path: 本地的上传路径含文件名
```

#### 构建docker镜像

```
# 创建docker镜像
docker build -t jianmudev/jianmu-runner-seafile:1.0.0 -f dockerfile/Dockerfile .

# 上传docker镜像
docker push jianmudev/jianmu-runner-seafile:1.0.0
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
  jianmudev/jianmu-runner-seafile-uploads:1.0.0
```

