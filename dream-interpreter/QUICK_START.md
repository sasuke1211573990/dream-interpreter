# Dreamer2.0 快速启动指南

## ✅ 当前运行状态

所有服务已成功启动！

### 服务列表

1. **后端服务** ✅
   - 端口: 3000
   - 状态: 运行中
   - URL: http://localhost:3000

2. **AI 服务** ⏳
   - 端口: 5000
   - 状态: 启动中（模型加载中）
   - URL: http://localhost:5000/health
   - 注意: 首次运行需要下载模型（约 1GB），可能需要 5-15 分钟

3. **前端服务** ✅
   - 端口: 3001
   - 状态: 运行中
   - URL: http://localhost:3001

## 🚀 立即使用

**打开浏览器访问：** http://localhost:3001

即使 AI 模型还在加载，系统也可以正常使用（会使用 fallback 模式）。一旦模型加载完成，系统会自动切换到真实的 AI 解析。

## 📋 检查服务状态

### 检查后端
```powershell
Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing
```

### 检查 AI 服务
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/health" -UseBasicParsing | Select-Object -ExpandProperty Content
```

如果返回 `"model_loaded": true`，说明模型已加载成功！

## 🔧 手动启动服务（如果需要）

### 启动后端
```powershell
cd "D:\Study\4、创业\Dreamer2.0\Dreamer2\dream-interpreter\backend"
node app.js
```

### 启动 AI 服务（使用修复后的代码）
```powershell
cd "D:\Study\4、创业\Dreamer2.0\Dreamer2\dream-interpreter\ai\inference"
.\start_ai_service.ps1
```

或者直接运行：
```powershell
cd "D:\Study\4、创业\Dreamer2.0\Dreamer2\dream-interpreter\ai\inference"
python app.py
```

### 启动前端
```powershell
cd "D:\Study\4、创业\Dreamer2.0\Dreamer2\dream-interpreter\frontend"
npm start
```

## ⚠️ 已修复的问题

1. ✅ **代理错误** - 已自动禁用代理设置
2. ✅ **模型优化** - 使用更小的模型（0.5B）减少内存需求
3. ✅ **错误处理** - 改进了错误日志和异常处理

## 💡 提示

- AI 模型首次下载可能需要较长时间，请耐心等待
- 系统在模型加载期间仍可使用（fallback 模式）
- 如果遇到问题，检查 PowerShell 窗口中的错误信息

## 📞 需要帮助？

如果遇到问题：
1. 检查所有服务的 PowerShell 窗口是否有错误
2. 确认端口 3000, 3001, 5000 没有被其他程序占用
3. 检查网络连接（模型下载需要网络）
