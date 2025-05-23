# 端口占用监控工具

一个用于监控和管理端口占用的命令行工具，支持快速查看和终止占用端口的进程。

## 功能特点

- 多线程并行检测端口，检测速度快
- 支持检测常见的开发端口（前端、后端、数据库等）
- 彩色终端输出，界面美观
- 支持一键终止占用进程
- 实时更新端口占用状态

## 支持的端口类型

- Web服务端口 (80, 443, 8080等)
- 前端开发端口 (3000, 3001, 4200, 5173等)
- 后端开发端口 (5000, 8000, 9090等)
- 数据库端口 (3306, 5432, 27017等)
- 其他服务端口 (FTP, SSH, DNS等)

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

1. 以管理员权限运行程序：
```bash
python port_monitor.py
```

2. 查看端口占用情况
3. 输入进程ID (PID) 来终止对应进程
4. 输入 'q' 退出程序
5. 输入 'h' 显示帮助信息

## 注意事项

- 需要管理员权限才能运行
- 终止进程可能会影响正在运行的服务，请谨慎操作
- 建议在终止进程前确认该进程确实可以安全终止

## 开发环境

- Python 3.6+
- Windows/Linux/MacOS