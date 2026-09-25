@echo off
setlocal

python "%~dp0sort_vscode_settings.py" %*
if errorlevel 1 (
    echo.
    echo 处理失败，请检查 Python 环境和设置文件路径。
)

pause