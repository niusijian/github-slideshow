# Your GitHub Learning Lab Repository for Introducing GitHub

Welcome to **your** repository for your GitHub Learning Lab course. This repository will be used during the different activities that I will be guiding you through. See a word you don't understand? We've included an emoji 📖 next to some key terms. Click on it to see its definition.

Oh! I haven't introduced myself...

I'm the GitHub Learning Lab bot and I'm here to help guide you in your journey to learn and master the various topics covered in this course. I will be using Issue and Pull Request comments to communicate with you. In fact, I already added an issue for you to check out.

![issue tab](https://lab.github.com/public/images/issue_tab.png)

I'll meet you over there, can't wait to get started!

---

## Windows 本地项目管理工具（Python Tkinter）

我新增了一个可直接在 Windows 本地运行的轻量项目管理工具：`windows_project_manager.py`。

### 功能
- 记录 **项目开始信息**：项目名称、负责人、开始日期、项目目标。
- 记录 **项目过程信息**：每次更新自动附带时间戳并形成历史记录。
- 记录 **项目结束信息**：结束日期、项目结果、项目总结。
- 本地持久化：自动保存到同目录 `project_records.json`。

### 运行方式（Windows）
1. 安装 Python 3.10+。
2. 在项目目录打开命令行，执行：
   ```bash
   python windows_project_manager.py
   ```

### 使用建议
- 点击“新建项目”创建项目。
- 在不同标签页分别维护开始/过程/结束信息。
- 点击“保存到本地”可手动触发保存（部分操作也会自动保存）。
