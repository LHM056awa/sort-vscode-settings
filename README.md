# Sort VS Code Settings

递归排序 VS Code `settings.json` 中的对象键名，保持数组元素顺序不变。

## 排序前后示例

排序前：

```json
{
    "window.commandCenter": false,
    "editor.tabSize": 4,
    "files.autoSave": "onFocusChange",
    "editor.fontSize": 14
}
```

排序后：

```json
{
    "editor.fontSize": 14,
    "editor.tabSize": 4,
    "files.autoSave": "onFocusChange",
    "window.commandCenter": false
}
```

## 环境要求

- Python 3.8 或更高版本，仅使用标准库，无需安装额外依赖
- 默认配置路径是 Windows 专属（`%APPDATA%\Code\User\settings.json`）；在 macOS / Linux 上请显式传入路径

## 使用方法

直接运行，处理当前 Windows 用户的默认 VS Code 配置：

```bash
python sort_vscode_settings.py
```

指定任意 JSON 文件：

```bash
python sort_vscode_settings.py "C:\path\to\settings.json"
```

双击 `sort_vscode_settings.bat` 等价于用默认路径运行；也可以把 JSON 文件拖到该批处理文件上处理其他文件。

## 处理过程

1. 读取文件（兼容带 UTF-8 BOM 的 JSON）。
2. 递归排序所有对象的键名，数组顺序保持不变。
3. 若键名已有序，输出提示并直接结束，不创建临时文件、不修改原文件。
4. 需要排序时，先在设置文件**同目录**写入临时文件并读回校验，确认无误后用原子替换（`replace`）覆盖原文件；即使中途崩溃也不会留下半截设置文件。
5. 临时文件在成功替换后自动删除；失败时保留并报错。
6. 解析失败（JSON 语法错误）时输出错误位置（行/列）并以退出码 1 结束，不修改原文件。
7. 若文件中有重复键，输出警告并仅保留最后一个值（标准 dict 语义）。
