@echo off
setlocal

python "%~dp0sort_vscode_settings.py" %*
set "exit_code=%errorlevel%"
if not "%exit_code%"=="0" (
    echo.
    echo 处理失败，请检查 Python 环境和设置文件路径。
)

rem 仅双击运行（交互式窗口）时暂停；被其他程序调用时直接返回，不吞 exit code
if not defined CI if not defined NONINTERACTIVE pause

exit /b %exit_code%