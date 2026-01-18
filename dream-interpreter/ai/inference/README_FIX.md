# AI 服务代理问题修复指南

## 问题描述

如果遇到以下错误：
```
ProxyError('Unable to connect to proxy', FileNotFoundError(2, 'No such file or directory'))
```

这是因为系统配置了代理，但代理设置不正确或代理服务不可用。

## 解决方案

### 方案 1：使用修复后的启动脚本（推荐）

我已经创建了启动脚本，会自动禁用代理设置：

**Windows PowerShell:**
```powershell
cd "D:\Study\4、创业\Dreamer2.0\Dreamer2\dream-interpreter\ai\inference"
.\start_ai_service.ps1
```

**Windows CMD:**
```cmd
cd "D:\Study\4、创业\Dreamer2.0\Dreamer2\dream-interpreter\ai\inference"
start_ai_service.bat
```

### 方案 2：手动禁用代理后启动

在启动服务前，先清除代理环境变量：

**PowerShell:**
```powershell
$env:HTTP_PROXY = $null
$env:HTTPS_PROXY = $null
$env:http_proxy = $null
$env:https_proxy = $null
$env:ALL_PROXY = $null
$env:all_proxy = $null
$env:NO_PROXY = "*"

cd "D:\Study\4、创业\Dreamer2.0\Dreamer2\dream-interpreter\ai\inference"
python app.py
```

**CMD:**
```cmd
set HTTP_PROXY=
set HTTPS_PROXY=
set http_proxy=
set https_proxy=
set ALL_PROXY=
set all_proxy=
set NO_PROXY=*

cd "D:\Study\4、创业\Dreamer2.0\Dreamer2\dream-interpreter\ai\inference"
python app.py
```

### 方案 3：使用 Hugging Face 镜像（中国用户推荐）

如果你在中国，可以使用 Hugging Face 镜像站点加速下载：

1. 编辑 `service.py`，找到以下行：
```python
# os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
```

2. 取消注释这两行：
```python
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
print("Using Hugging Face mirror: https://hf-mirror.com")
```

3. 然后启动服务

## 代码已自动修复

我已经更新了代码，现在 `app.py` 和 `service.py` 都会自动：
- 清除所有代理环境变量
- 设置 NO_PROXY 为 '*'
- 在加载模型时禁用代理

## 验证修复

启动服务后，你应该看到：
```
Disabling proxy settings...
Removing proxy: HTTP_PROXY
...
Loading smaller model Qwen/Qwen2.5-0.5B-Instruct...
Loading tokenizer...
```

如果不再出现代理错误，说明修复成功。

## 如果仍然有问题

1. **检查网络连接**：确保可以访问互联网
2. **检查防火墙**：确保防火墙没有阻止 Python 访问网络
3. **使用镜像站点**：如果在中国，使用方案 3 的镜像站点
4. **检查 Python 版本**：确保使用 Python 3.8 或更高版本
