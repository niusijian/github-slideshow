import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

DATA_FILE = "project_records.json"


def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@dataclass
class ProjectRecord:
    name: str
    owner: str
    start_date: str
    goal: str
    process_updates: list
    end_date: str = ""
    result: str = ""
    summary: str = ""


class ProjectManagerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("项目管理工具（本地版）")
        self.root.geometry("980x660")

        self.projects: list[ProjectRecord] = []
        self.selected_index: int | None = None

        self._build_ui()
        self.load_data()
        self.refresh_project_list()

    def _build_ui(self):
        main = ttk.Frame(self.root, padding=12)
        main.pack(fill=tk.BOTH, expand=True)

        left = ttk.Frame(main)
        left.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(left, text="项目列表", font=("Microsoft YaHei", 11, "bold")).pack(anchor="w")
        self.project_list = tk.Listbox(left, width=30, height=30)
        self.project_list.pack(fill=tk.Y, pady=6)
        self.project_list.bind("<<ListboxSelect>>", self.on_select_project)

        btn_group = ttk.Frame(left)
        btn_group.pack(fill=tk.X, pady=8)
        ttk.Button(btn_group, text="新建项目", command=self.add_project).pack(fill=tk.X, pady=2)
        ttk.Button(btn_group, text="删除项目", command=self.delete_project).pack(fill=tk.X, pady=2)
        ttk.Button(btn_group, text="保存到本地", command=self.save_data).pack(fill=tk.X, pady=2)

        right = ttk.Frame(main)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(16, 0))

        notebook = ttk.Notebook(right)
        notebook.pack(fill=tk.BOTH, expand=True)

        self.start_tab = ttk.Frame(notebook, padding=10)
        self.process_tab = ttk.Frame(notebook, padding=10)
        self.end_tab = ttk.Frame(notebook, padding=10)
        notebook.add(self.start_tab, text="开始信息")
        notebook.add(self.process_tab, text="过程信息")
        notebook.add(self.end_tab, text="结束信息")

        self._build_start_tab()
        self._build_process_tab()
        self._build_end_tab()

    def _build_start_tab(self):
        self.start_name = tk.StringVar()
        self.start_owner = tk.StringVar()
        self.start_date = tk.StringVar(value=now_str().split(" ")[0])

        ttk.Label(self.start_tab, text="项目名称").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(self.start_tab, textvariable=self.start_name, width=48).grid(row=0, column=1, sticky="ew")

        ttk.Label(self.start_tab, text="负责人").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(self.start_tab, textvariable=self.start_owner, width=48).grid(row=1, column=1, sticky="ew")

        ttk.Label(self.start_tab, text="开始日期").grid(row=2, column=0, sticky="w", pady=4)
        ttk.Entry(self.start_tab, textvariable=self.start_date, width=48).grid(row=2, column=1, sticky="ew")

        ttk.Label(self.start_tab, text="项目目标").grid(row=3, column=0, sticky="nw", pady=4)
        self.start_goal = tk.Text(self.start_tab, height=12, width=56)
        self.start_goal.grid(row=3, column=1, sticky="ew")

        ttk.Button(self.start_tab, text="保存开始信息", command=self.save_start_info).grid(
            row=4, column=1, sticky="e", pady=10
        )
        self.start_tab.columnconfigure(1, weight=1)

    def _build_process_tab(self):
        ttk.Label(self.process_tab, text="过程记录（每次更新一条）").pack(anchor="w")

        self.process_text = tk.Text(self.process_tab, height=8)
        self.process_text.pack(fill=tk.X, pady=8)

        btns = ttk.Frame(self.process_tab)
        btns.pack(fill=tk.X)
        ttk.Button(btns, text="添加过程记录", command=self.add_process_update).pack(side=tk.RIGHT)

        ttk.Label(self.process_tab, text="历史过程记录").pack(anchor="w", pady=(12, 4))
        self.process_history = tk.Text(self.process_tab, height=18, state=tk.DISABLED)
        self.process_history.pack(fill=tk.BOTH, expand=True)

    def _build_end_tab(self):
        self.end_date = tk.StringVar(value=now_str().split(" ")[0])
        ttk.Label(self.end_tab, text="结束日期").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(self.end_tab, textvariable=self.end_date, width=48).grid(row=0, column=1, sticky="ew")

        ttk.Label(self.end_tab, text="项目结果").grid(row=1, column=0, sticky="nw", pady=4)
        self.end_result = tk.Text(self.end_tab, height=8)
        self.end_result.grid(row=1, column=1, sticky="ew")

        ttk.Label(self.end_tab, text="项目总结").grid(row=2, column=0, sticky="nw", pady=4)
        self.end_summary = tk.Text(self.end_tab, height=10)
        self.end_summary.grid(row=2, column=1, sticky="ew")

        ttk.Button(self.end_tab, text="保存结束信息", command=self.save_end_info).grid(
            row=3, column=1, sticky="e", pady=10
        )
        self.end_tab.columnconfigure(1, weight=1)

    def get_selected_project(self) -> ProjectRecord | None:
        if self.selected_index is None or not (0 <= self.selected_index < len(self.projects)):
            return None
        return self.projects[self.selected_index]

    def add_project(self):
        name = self.start_name.get().strip() or f"新项目-{len(self.projects) + 1}"
        record = ProjectRecord(
            name=name,
            owner=self.start_owner.get().strip(),
            start_date=self.start_date.get().strip(),
            goal=self.start_goal.get("1.0", tk.END).strip(),
            process_updates=[],
        )
        self.projects.append(record)
        self.selected_index = len(self.projects) - 1
        self.refresh_project_list()
        self.project_list.selection_clear(0, tk.END)
        self.project_list.selection_set(self.selected_index)
        self.project_list.activate(self.selected_index)
        self.show_project(record)

    def delete_project(self):
        p = self.get_selected_project()
        if p is None:
            messagebox.showwarning("提示", "请先选择一个项目。")
            return
        if not messagebox.askyesno("确认", f"确定删除项目：{p.name}？"):
            return
        del self.projects[self.selected_index]
        self.selected_index = None
        self.refresh_project_list()
        self.clear_editor()

    def save_start_info(self):
        p = self.get_selected_project()
        if p is None:
            self.add_project()
            p = self.get_selected_project()
        p.name = self.start_name.get().strip()
        p.owner = self.start_owner.get().strip()
        p.start_date = self.start_date.get().strip()
        p.goal = self.start_goal.get("1.0", tk.END).strip()
        self.refresh_project_list()
        self.save_data()
        messagebox.showinfo("成功", "开始信息已保存。")

    def add_process_update(self):
        p = self.get_selected_project()
        if p is None:
            messagebox.showwarning("提示", "请先在左侧创建或选择一个项目。")
            return
        content = self.process_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("提示", "过程内容不能为空。")
            return
        p.process_updates.append({"time": now_str(), "content": content})
        self.process_text.delete("1.0", tk.END)
        self.render_process_history(p)
        self.save_data()

    def save_end_info(self):
        p = self.get_selected_project()
        if p is None:
            messagebox.showwarning("提示", "请先选择一个项目。")
            return
        p.end_date = self.end_date.get().strip()
        p.result = self.end_result.get("1.0", tk.END).strip()
        p.summary = self.end_summary.get("1.0", tk.END).strip()
        self.save_data()
        messagebox.showinfo("成功", "结束信息已保存。")

    def on_select_project(self, _event=None):
        sel = self.project_list.curselection()
        if not sel:
            return
        self.selected_index = sel[0]
        p = self.get_selected_project()
        if p:
            self.show_project(p)

    def show_project(self, p: ProjectRecord):
        self.start_name.set(p.name)
        self.start_owner.set(p.owner)
        self.start_date.set(p.start_date)

        self.start_goal.delete("1.0", tk.END)
        self.start_goal.insert("1.0", p.goal)

        self.end_date.set(p.end_date or now_str().split(" ")[0])
        self.end_result.delete("1.0", tk.END)
        self.end_result.insert("1.0", p.result)
        self.end_summary.delete("1.0", tk.END)
        self.end_summary.insert("1.0", p.summary)
        self.render_process_history(p)

    def render_process_history(self, p: ProjectRecord):
        self.process_history.config(state=tk.NORMAL)
        self.process_history.delete("1.0", tk.END)
        if not p.process_updates:
            self.process_history.insert("1.0", "暂无过程记录。")
        else:
            lines = []
            for i, item in enumerate(p.process_updates, start=1):
                lines.append(f"[{i}] {item['time']}\n{item['content']}\n")
            self.process_history.insert("1.0", "\n".join(lines))
        self.process_history.config(state=tk.DISABLED)

    def clear_editor(self):
        self.start_name.set("")
        self.start_owner.set("")
        self.start_date.set(now_str().split(" ")[0])
        self.start_goal.delete("1.0", tk.END)
        self.process_text.delete("1.0", tk.END)
        self.process_history.config(state=tk.NORMAL)
        self.process_history.delete("1.0", tk.END)
        self.process_history.config(state=tk.DISABLED)
        self.end_date.set(now_str().split(" ")[0])
        self.end_result.delete("1.0", tk.END)
        self.end_summary.delete("1.0", tk.END)

    def refresh_project_list(self):
        self.project_list.delete(0, tk.END)
        for p in self.projects:
            status = "（已结束）" if p.end_date and (p.result or p.summary) else "（进行中）"
            self.project_list.insert(tk.END, f"{p.name} {status}")

    def save_data(self):
        data = [asdict(p) for p in self.projects]
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            return
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
        self.projects = [ProjectRecord(**item) for item in raw]


if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectManagerApp(root)
    root.mainloop()
