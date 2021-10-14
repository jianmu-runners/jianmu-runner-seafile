# seafile-upload

#### 介绍
建木的seafile上传节点

```
docker run --rm \
  -v /usr/test/acmesh:/tmp \
  -e JIANMU_USERNAME=huang.xi@99cloud.net \
  -e JIANMU_PASSWORD=huangxi1014 \
  -e JIANMU_BASE_URL=https://seafile.sh.99cloud.net/ \
  -e JIANMU_REPO_ID=dae0041c-c4a0-4d41-a222-966e71883286 \
  -e JIANMU_DIR_PATH=/fly \
  -e JIANMU_UPLOAD_FILE_PATH=/usr/test/acmesh/env-acmesh \
  jianmudev/jianmu-runner-seafile-uploads:1.0.0
```
docker build -t seafile-uploads -f dockerfile/Dockerfile .
docker build -t jianmudev/jianmu-runner-seafile:1.0.0 -f dockerfile/Dockerfile .