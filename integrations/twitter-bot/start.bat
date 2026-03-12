@echo off
REM RustChain Twitter Bot 启动脚本 (Windows)

echo 🚀 RustChain Twitter Bot 启动中...

REM 检查虚拟环境
if not exist ".venv" (
    echo 创建虚拟环境...
    python -m venv .venv
)

REM 激活虚拟环境
call .venv\Scripts\activate.bat

REM 安装依赖
echo 安装依赖...
pip install -r requirements.txt -q

REM 运行机器人
echo 启动 Twitter Bot...
python twitter_bot.py

pause
