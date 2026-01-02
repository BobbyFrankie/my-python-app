# 🔐 文件哈希计算器 (File Hash Calculator)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

一个基于 Python 和 Tkinter 开发的轻量级、现代化的哈希计算工具。支持文件拖拽、文本哈希以及批量文件处理。

> ![文件哈希](https://s1.locimg.com/2026/01/02/1a797c8f47f82.png)
> ![文本哈希](https://s1.locimg.com/2026/01/02/e8b2a11731f26.png)
> ![批量计算](https://s1.locimg.com/2026/01/02/1de1b058f929d.png)

## ✨ 主要功能

*   **全算法支持**：一次计算同时显示 **MD5, SHA-1, SHA-256, SHA-512, CRC32** 五种哈希值。
*   **拖拽操作**：支持直接将文件拖拽到窗口即可开始计算。
*   **三种模式**：
    *   📂 **文件哈希**：单文件详细计算，支持哈希值比对（自动检测匹配算法）。
    *   📝 **文本哈希**：计算字符串的哈希值。
    *   📦 **批量计算**：支持导入多文件或文件夹，一键计算并导出结果到 TXT。
*   **比对功能**：输入哈希值，自动与计算结果比对，绿色显示匹配，红色显示不匹配。
*   **无缝体验**：多线程后台计算，处理大文件时不卡顿。

## 🚀 快速开始

### 方式一：直接运行 (Windows)

前往 `dist/File_Hash_Calculator.exe` 下载体验，无需安装 Python 环境即可直接使用。

### 方式二：源码运行

如果你想查看源码或进行二次开发，请按以下步骤操作：

1.  **克隆仓库**
    ```bash
    git clone https://github.com/BobbyFrankie/file-hash-calculator.git
    cd ./file-hash-calculator
    ```

2.  **安装依赖**
    建议使用虚拟环境：
    ```bash
    python -m venv venv
    venv\Scripts\activate
    pip install tkinterdnd2
    ```

3.  **运行程序**
    ```bash
    python main.py
    ```

## 🛠️ 打包指南 (Build)

本项目推荐使用 `PyInstaller` 将源码打包成 Windows 可执行文件 (.exe)。

1.  **安装打包工具**
    ```bash
    pip install pyinstaller
    ```

2.  **执行打包命令**
    确保项目目录下有 `assets` (存放图标) 和 `icons` (存放资源图片) 文件夹，然后在命令行执行：

    ```bash
    pyinstaller --noconsole --onefile --icon="assets/app.ico" --collect-all tkinterdnd2 --add-data "icons;icons" --add-data "assets;assets" main.py
    ```

    *注：`--add-data` 参数用于确保图片资源正确打包进 exe 文件内部。*

## 📂 项目结构

```text
File-Hash-Calculator/
├── assets/              # 存放应用程序图标 (app.ico)
├── dist/                # 存放打包程序 (File_Hash_Calculator.exe)
├── icons/               # 存放界面资源图片 (correct.png, error.png)
├── LICENSE              # MIT License 协议
├── README.md            # 项目说明文档
├── main.py              # 主程序入口代码
└── requirements.txt     # 项目依赖文件
```

## 🤝 贡献 (Contributing)
    欢迎提交 `Issue` 或 `Pull Request` 来改进这个项目！如果你是 `Python` 初学者，这也是一个很好的练习机会。

    1. Fork 本仓库
    2. 新建 Feat_xxx 分支
    3. 提交代码
    4. 新建 Pull Request

## 📄 开源协议 (License)

    本项目遵循 MIT License 协议。
