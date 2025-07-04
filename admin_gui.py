import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
from chatbot.workflow_manager import add_node, edit_node, delete_node, list_nodes, load_tree

class WorkflowAdminApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Workflow Admin Center")
        self.geometry("1000x700")
        self.configure(bg="#2b2b2b")

        self.style = ttk.Style(self)
        self._setup_style()

        self.nodes = []
        self.selected_node = None
        self.tree = {}

        self._build_ui()
        self._load_nodes()

    def _setup_style(self):
        self.style.theme_use('clam')

        # Style for Treeview/Listbox
        self.style.configure('Treeview',
                             background='#404040',
                             foreground='white',
                             fieldbackground='#404040',
                             font=('Consolas', 11),
                             rowheight=24)
        self.style.map('Treeview',
                       background=[('selected', '#0078d4')],
                       foreground=[('selected', 'white')])

        # Style for buttons
        self.style.configure('TButton',
                             font=('Helvetica', 10, 'bold'),
                             foreground='white',
                             background='#0078d4',
                             borderwidth=0,
                             padding=6)
        self.style.map('TButton',
                       background=[('active', '#005a9e')])

    def _build_ui(self):
        # Header
        header = tk.Label(self, text="🔧 Workflow Admin Center",
                          font=('Helvetica', 24, 'bold'),
                          fg='#0078d4', bg='#2b2b2b', pady=10)
        header.pack(fill='x')

        subtitle = tk.Label(self, text="Manage and configure your troubleshooting workflow nodes",
                            font=('Helvetica', 12),
                            fg='#cccccc', bg='#2b2b2b', pady=5)
        subtitle.pack(fill='x')

        # Search frame
        search_frame = tk.Frame(self, bg="#2b2b2b")
        search_frame.pack(fill='x', padx=20, pady=(10, 0))

        search_label = tk.Label(search_frame, text="Search:", font=('Helvetica', 10), fg='white', bg='#2b2b2b')
        search_label.pack(side='left')

        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', self._on_search)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side='left', padx=(5, 0))

        # Main frame with list and details side by side
        main_frame = tk.Frame(self, bg="#2b2b2b")
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Node list frame
        list_frame = tk.Frame(main_frame, bg="#2b2b2b")
        list_frame.pack(side='left', fill='y')

        list_label = tk.Label(list_frame, text="📋 Available Nodes", font=('Helvetica', 16, 'bold'), fg='white', bg='#2b2b2b')
        list_label.pack(anchor='w', pady=(0,5))

        self.node_listbox = tk.Listbox(list_frame, width=40, height=25, bg='#404040', fg='white',
                                       font=('Consolas', 11), selectbackground='#0078d4', selectforeground='white',
                                       activestyle='none', highlightthickness=0, borderwidth=0)
        self.node_listbox.pack(side='left', fill='y')
        self.node_listbox.bind('<<ListboxSelect>>', self._on_node_select)

        scrollbar = tk.Scrollbar(list_frame, command=self.node_listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.node_listbox.config(yscrollcommand=scrollbar.set)

        # Buttons below node list
        btn_frame = tk.Frame(list_frame, bg="#2b2b2b")
        btn_frame.pack(fill='x', pady=(10,0))

        add_btn = ttk.Button(btn_frame, text="➕ Add Node", command=self._add_node)
        add_btn.pack(side='left', expand=True, fill='x', padx=2)

        edit_btn = ttk.Button(btn_frame, text="✏️ Edit Node", command=self._edit_node)
        edit_btn.pack(side='left', expand=True, fill='x', padx=2)

        del_btn = ttk.Button(btn_frame, text="🗑️ Delete Node", command=self._delete_node)
        del_btn.pack(side='left', expand=True, fill='x', padx=2)

        refresh_btn = ttk.Button(btn_frame, text="🔄 Refresh", command=self._load_nodes)
        refresh_btn.pack(side='left', expand=True, fill='x', padx=2)

        # Node details frame
        details_frame = tk.Frame(main_frame, bg="#2b2b2b")
        details_frame.pack(side='left', fill='both', expand=True, padx=(20,0))

        details_label = tk.Label(details_frame, text="🔍 Node Details", font=('Helvetica', 16, 'bold'), fg='white', bg='#2b2b2b')
        details_label.pack(anchor='w', pady=(0,5))

        selected_label_frame = tk.Frame(details_frame, bg="#2b2b2b")
        selected_label_frame.pack(fill='x')

        sel_label = tk.Label(selected_label_frame, text="Current Selection:", font=('Helvetica', 10, 'bold'), fg='#cccccc', bg='#2b2b2b')
        sel_label.pack(side='left')

        self.selected_node_label = tk.Label(selected_label_frame, text="None", font=('Helvetica', 10), fg='#0078d4', bg='#2b2b2b')
        self.selected_node_label.pack(side='left')

        separator = ttk.Separator(details_frame, orient='horizontal')
        separator.pack(fill='x', pady=5)

        self.details_text = scrolledtext.ScrolledText(details_frame, wrap='word', font=('Consolas', 10),
                                                      bg='#404040', fg='white', state='disabled', height=25)
        self.details_text.pack(fill='both', expand=True)

        # Status bar
        self.status_var = tk.StringVar(value="Status: Ready")
        status_bar = tk.Label(self, textvariable=self.status_var, font=('Helvetica', 9), fg='#28a745', bg='#2b2b2b', anchor='w')
        status_bar.pack(fill='x', side='bottom', ipady=3)

    def _set_status(self, message, color='#28a745'):
        self.status_var.set(f"Status: {message}")
        self.status_var_label = color
        # Changing label fg color dynamically:
        # (Tkinter requires a little trick for that)
        self.children['!label'].config(fg=color)

    def _load_nodes(self):
        try:
            self.tree = load_tree()
            self.nodes = list_nodes()
            self._update_node_list()
            self._clear_details()
            self._set_status("Node list refreshed")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load nodes: {e}")
            self._set_status("Failed to load nodes", '#dc3545')

    def _update_node_list(self, filtered=None):
        self.node_listbox.delete(0, tk.END)
        data = filtered if filtered is not None else self.nodes
        for node in data:
            self.node_listbox.insert(tk.END, node)

    def _clear_details(self):
        self.selected_node = None
        self.selected_node_label.config(text="None")
        self.details_text.config(state='normal')
        self.details_text.delete('1.0', tk.END)
        self.details_text.config(state='disabled')

    def _on_search(self, *args):
        search_term = self.search_var.get().lower()
        if search_term:
            filtered = [node for node in self.nodes if search_term in node.lower()]
            self._update_node_list(filtered)
        else:
            self._update_node_list()

    def _on_node_select(self, event):
        sel = self.node_listbox.curselection()
        if not sel:
            self._clear_details()
            self._set_status("No node selected")
            return
        idx = sel[0]
        node_id = self.node_listbox.get(idx)
        self.selected_node = node_id
        self.selected_node_label.config(text=node_id)
        self._show_node_details(node_id)
        self._set_status(f"Selected node: {node_id}")

    def _show_node_details(self, node_id):
        node = self.tree.get(node_id, {})
        self.details_text.config(state='normal')
        self.details_text.delete('1.0', tk.END)

        if not node:
            self.details_text.insert(tk.END, "No data found.")
            self.details_text.config(state='disabled')
            return

        details = f"Node ID: {node_id}\n{'='*40}\n\n"
        for key, val in node.items():
            if key == 'edges' and isinstance(val, dict):
                details += f"{key.title()}:\n"
                for k, v in val.items():
                    details += f"  {k} → {v}\n"
                details += "\n"
            else:
                details += f"{key.title()}: {val}\n\n"

        self.details_text.insert(tk.END, details)
        self.details_text.config(state='disabled')

    def _add_node(self):
        node_id = simpledialog.askstring("Add Node", "Enter new node ID:", parent=self)
        if not node_id:
            return

        terminal = messagebox.askyesno("Node Type", "Is this a terminal node?", parent=self)
        if terminal:
            response = simpledialog.askstring("Terminal Node", "Enter response text:", parent=self)
            if response is None:
                return
            try:
                msg = add_node(node_id=node_id, response=response, terminal=True)
                messagebox.showinfo("Success", msg, parent=self)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add node: {e}", parent=self)
        else:
            prompt = simpledialog.askstring("Non-Terminal Node", "Enter prompt text:", parent=self)
            if prompt is None:
                return
            edges_text = simpledialog.askstring(
                "Node Edges",
                "Enter edges (keyword:next_node), one per line:",
                parent=self,
                )
            edges = {}
            if edges_text:
                for line in edges_text.splitlines():
                    if ':' in line:
                        k, v = line.split(':', 1)
                        edges[k.strip()] = v.strip()
            try:
                msg = add_node(node_id=node_id, prompt=prompt, edges=edges)
                messagebox.showinfo("Success", msg, parent=self)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add node: {e}", parent=self)

        self._load_nodes()

    def _edit_node(self):
        if not self.selected_node:
            messagebox.showwarning("Warning", "Please select a node first.", parent=self)
            return

        node = self.tree.get(self.selected_node, {})
        if not node:
            messagebox.showerror("Error", "Selected node data not found.", parent=self)
            return

        field = simpledialog.askstring("Edit Node", "Field to edit (prompt, response, edges, terminal):", parent=self)
        if not field:
            return
        field = field.strip().lower()

        try:
            if field == "edges":
                edges_text = simpledialog.askstring("Edit Edges", "Enter edges (keyword:next_node), one per line:", parent=self)
                if edges_text is None:
                    return
                edges = {}
                for line in edges_text.splitlines():
                    if ':' in line:
                        k, v = line.split(':', 1)
                        edges[k.strip()] = v.strip()
                updates = {'edges': edges}
            elif field == "terminal":
                val = messagebox.askyesno("Terminal Status", "Set terminal? Yes for True, No for False", parent=self)
                updates = {'terminal': val}
            else:
                val = simpledialog.askstring("Edit Field", f"New value for {field}:", parent=self)
                if val is None:
                    return
                updates = {field: val}

            msg = edit_node(self.selected_node, updates)
            messagebox.showinfo("Success", msg, parent=self)
            self._load_nodes()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to edit node: {e}", parent=self)

    def _delete_node(self):
        if not self.selected_node:
            messagebox.showwarning("Warning", "Please select a node first.", parent=self)
            return

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete node '{self.selected_node}'?\n\nThis action cannot be undone.",
            parent=self
        )
        if not confirm:
            return

        try:
            msg = delete_node(self.selected_node)
            messagebox.showinfo("Success", msg, parent=self)
            self.selected_node = None
            self._load_nodes()
            self._clear_details()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete node: {e}", parent=self)

if __name__ == "__main__":
    app = WorkflowAdminApp()
    app.mainloop()
