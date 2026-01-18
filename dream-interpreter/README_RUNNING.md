# Dreamer2.0 运行指南

## 当前状态

✅ **后端服务** - 运行在端口 3000
✅ **前端服务** - 运行在端口 3001 (因为 3000 被后端占用)
⏳ **AI 服务** - 正在启动中，模型加载中

## 已完成的优化

1. **AI 模型优化**：
   - 默认使用更小的模型 `Qwen/Qwen2.5-0.5B-Instruct` (约 1GB)
   - 替代原来的 `DeepSeek-R1-Distill-Qwen-7B` (约 14GB)
   - 大大减少了内存需求和加载时间

2. **错误处理改进**：
   - 添加了详细的错误日志
   - 改进了模型加载的错误处理
   - 支持 CPU 和 GPU 自动检测

## 如何访问

- **前端界面**: http://localhost:3001
- **后端 API**: http://localhost:3000
- **AI 服务健康检查**: http://localhost:5000/health

## 当前问题解决

### 问题：AI 服务显示 Fallback 模式

**原因**：AI 模型正在下载和加载中（首次运行需要时间）

**解决方案**：
1. 等待模型下载完成（可能需要几分钟到十几分钟，取决于网络速度）
2. 模型会自动加载，加载完成后系统会自动切换到真实 AI 解析

**检查模型加载状态**：
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/health" -UseBasicParsing | Select-Object -ExpandProperty Content
```

如果返回 `"model_loaded": true`，说明模型已加载成功。

## 手动启动服务

如果服务停止，可以手动启动：

### 1. 启动后端服务
```powershell
cd "D:\Study\4、创业\Dreamer2.0\Dreamer2\dream-interpreter\backend"
node app.js
```

### 2. 启动 AI 服务
```powershell
cd "D:\Study\4、创业\Dreamer2.0\Dreamer2\dream-interpreter\ai\inference"
python app.py
```

### 3. 启动前端服务
```powershell
cd "D:\Study\4、创业\Dreamer2.0\Dreamer2\dream-interpreter\frontend"
npm start
```

## 使用更大的模型（可选）

如果你想使用原来的 DeepSeek-R1 模型（需要更多内存和时间），可以设置环境变量：

```powershell
$env:USE_SMALL_MODEL = "false"
python "ai\inference\app.py"
```

## 注意事项

1. **首次运行**：模型需要从 Hugging Face 下载，可能需要较长时间
2. **内存需求**：
   - 小模型（0.5B）：约 2-4GB RAM
   - 大模型（7B）：约 16GB+ RAM
3. **网络连接**：首次下载模型需要稳定的网络连接
