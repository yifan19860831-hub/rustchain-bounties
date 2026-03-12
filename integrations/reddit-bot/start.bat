@echo off
echo 🦞 RustChain Reddit Bot 启动中...

REM 检查虚拟环境
if not exist ".venv" (
    echo 创建虚拟环境...
    python -m venv .venv
)

REM 激活虚拟环境
call .venv\Scripts\activate.bat

REM 安装依赖
echo 检查依赖...
pip install -r requirements.txt -q

REM 运行机器人
echo 启动 Reddit 机器人...
python reddit_bot.py

pause
