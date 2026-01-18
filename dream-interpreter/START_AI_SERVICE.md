# 启动 AI 服务 - 解决 Fallback 模式问题

## 问题说明

如果你看到 "Fallback Mode" 的提示，说明 AI 服务没有运行或模型没有加载。

## 快速解决方案

### 方法 1：使用启动脚本（推荐）

1. 打开 PowerShell 或 CMD
2. 导航到 AI 服务目录：
   ```powershell
   cd "D:\Study\4、创业\Dreamer2.0\Dreamer2\dream-interpreter\ai\inference"
   ```

3. 运行启动脚本：
   ```powershell
   .\start_ai_service.ps1
   ```
   或使用批处理文件：
   ```cmd
   start_ai_service.bat
   ```

### 方法 2：手动启动

1. 打开新的 PowerShell 窗口
2. 运行以下命令：

```powershell
# 清除代理设置
$env:HTTP_PROXY = $null
$env:HTTPS_PROXY = $null
$env:http_proxy = $null
$env:https_proxy = $null
$env:NO_PROXY = "*"

# 切换到 AI 服务目录
cd "D:\Study\4、创业\Dreamer2.0\Dreamer2\dream-interpreter\ai\inference"

# 启动服务
python app.py
```

## 预期输出

启动后，你应该看到：

```
Disabling proxy settings...
Removing proxy: HTTP_PROXY
...
Initializing AI Model...
Loading smaller model Qwen/Qwen2.5-0.5B-Instruct...
Loading tokenizer...
Loading model (this may take a while)...
```

## 等待模型加载

- 首次运行需要下载模型（约 1GB）
- 下载时间：5-15 分钟（取决于网络速度）
- 加载时间：1-3 分钟

## 检查服务状态

在另一个 PowerShell 窗口中运行：

```powershell
Invoke-WebRequest -Uri "http://localhost:5000/health" -UseBasicParsing | Select-Object -ExpandProperty Content
```

如果返回 `"model_loaded": true`，说明模型已加载成功！

## 验证修复

1. 等待模型加载完成（看到 "Model loaded successfully"）
2. 刷新浏览器页面 http://localhost:3001
3. 再次输入梦境描述
4. 应该看到真实的 AI 解析，而不是 Fallback 模式

## 常见问题

### Q: 仍然看到代理错误？
A: 确保在启动前清除了所有代理环境变量（见方法 2）

### Q: 模型下载很慢？
A: 可以启用 Hugging Face 镜像（中国用户）：
   - 编辑 `service.py`
   - 取消注释 `os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'`

### Q: 内存不足？
A: 当前使用的是 0.5B 小模型，需要约 2-4GB RAM。如果仍然不足，可能需要关闭其他程序。
