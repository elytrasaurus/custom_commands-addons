# helpme but BETTER.
# /// script
# dependencies = ["customtkinter"]
# ///
import os
import sys
import customtkinter as ctk

COMMANDS_DIR = r"C:\Custom_Commands"

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class BetterHelpMeGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Terminal Toolkit Command Center")
        self.geometry("820x580")
        self.resizable(False, False)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(3, weight=1)

        self.sidebar_title = ctk.CTkLabel(
            self.sidebar, 
            text="TOOLKIT\nHUB", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.sidebar_title.grid(row=0, column=0, padx=20, pady=(30, 20))

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.filter_commands)
        self.search_bar = ctk.CTkEntry(
            self.sidebar, 
            placeholder_text="Search commands...", 
            width=160,
            textvariable=self.search_var
        )
        self.search_bar.grid(row=1, column=0, padx=20, pady=10)

        self.counter_lbl = ctk.CTkLabel(
            self.sidebar, 
            text="Loading tools...", 
            font=ctk.CTkFont(size=12, slant="italic")
        )
        self.counter_lbl.grid(row=2, column=0, padx=20, pady=10)

        self.version_lbl = ctk.CTkLabel(
            self.sidebar, 
            text="v2.0 Clean GUI", 
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="gray"
        )
        self.version_lbl.grid(row=4, column=0, padx=20, pady=15)

        # --- MAIN PANEL ---
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)

        self.header_lbl = ctk.CTkLabel(
            self.content_frame, 
            text="✨ CUSTOM TERMINAL TOOLKIT NAVIGATION", 
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        self.header_lbl.grid(row=0, column=0, sticky="w", pady=(10, 15))

        self.scroll_frame = ctk.CTkScrollableFrame(self.content_frame, corner_radius=10)
        self.scroll_frame.grid(row=1, column=0, sticky="nsew")

        self.all_commands = self.discover_local_commands()
        self.update_sidebar_counter(len(self.all_commands))
        self.render_list(self.all_commands)

    def get_description(self, cmd_name):
        existing_commands = {
            'calc': 'A quick command-line calculator for math evaluations.',
            'clear': 'Clears the terminal screen to give you a fresh workspace.',
            'clockin': 'Logs your start time, end time, and tracks total project hours.',
            'flip': 'Creates a surprised emoji.',
            'genpass': 'Generates a highly secure, random password instantly.',
            'grep': 'Searches inside files for matching text lines (like Linux grep).',
            'helpme': 'Displays this custom toolkit menu and command breakdown.',
            'look': 'Searches for specific text inside a file name in your current directory.',
            'lookm': 'Searches for specific text inside a file name in multiple directories.',
            'lookmultiple': 'Searches for specific text inside a file name in multiple directories.',
            'ls': 'Lists all files and directories in your current folder cleanly.',
            'math': 'A shortcut launcher to quickly run your calc.py script.',
            'matrix': 'Fills your terminal window with a falling green digital rain effect.',
            'pwd': 'Prints your exact current Working Directory path.',
            'read': 'Quickly reads and displays the entire contents of a text file.',
            'sysinfo': 'Displays your OS version, CPU usage, RAM, and hardware stats.',
            'touch': 'Creates a brand new empty file instantly from the terminal.',
            'unflip': 'Creates a calm emoji.',
            'weather': 'Fetches and displays live, local weather forecasts.',
            'whatiscustomcommands': 'This is self explanitory.',
            'write': "Writes text lines directly into a specified file. If it can't find the specified file, it will make a new one with the same name.",
            'zipit': 'Compresses files or folders into a single .zip archive.'
        }

        if cmd_name in existing_commands:
            return existing_commands[cmd_name]

        py_file = os.path.join(COMMANDS_DIR, f"{cmd_name}.py")
        if os.path.exists(py_file):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    if first_line.startswith('#'):
                        return first_line.lstrip('#').strip()
            except Exception:
                pass

        return 'Custom terminal command.'

    def discover_local_commands(self):
        commands_dict = {}
        if not os.path.exists(COMMANDS_DIR):
            return commands_dict

        try:
            files = os.listdir(COMMANDS_DIR)
            commands = sorted(list(set([os.path.splitext(f)[0] for f in files if f.endswith('.bat')])))

            for cmd in commands:
                # REMOVED 'betterhelpme' FROM HERE SO IT SHOWS UP DYNAMICALLY
                if cmd in ['lookmultiple', 'removecmd', 'calc']:
                    continue
                
                commands_dict[cmd] = self.get_description(cmd)
        except Exception as e:
            print(f"Error scanning folder structure maps: {e}")

        return commands_dict

    def update_sidebar_counter(self, count):
        self.counter_lbl.configure(text=f"Indexed: {count} Commands")

    def render_list(self, items_to_display):
        for child in self.scroll_frame.winfo_children():
            child.destroy()

        if not items_to_display:
            no_match = ctk.CTkLabel(
                self.scroll_frame, 
                text="No matching custom commands found.", 
                font=ctk.CTkFont(size=13, slant="italic"),
                text_color="gray"
            )
            no_match.pack(pady=50)
            return

        for name, desc in sorted(items_to_display.items()):
            row_card = ctk.CTkFrame(self.scroll_frame, corner_radius=8, fg_color=("#EAEAEA", "#2B2B2B"))
            row_card.pack(fill="x", pady=4, padx=8)

            tag_label = ctk.CTkLabel(
                row_card, 
                text=name.lower(), 
                font=ctk.CTkFont(size=12, weight="bold"),
                fg_color=("#1F6AA5", "#1F6AA5"),
                text_color="white",
                corner_radius=6,
                width=125,
                height=26
            )
            tag_label.pack(side="left", padx=12, pady=10)

            desc_label = ctk.CTkLabel(
                row_card, 
                text=desc, 
                font=ctk.CTkFont(size=12),
                wraplength=400,
                anchor="w",
                justify="left"
            )
            desc_label.pack(side="left", padx=(10, 15), pady=10, fill="x", expand=True)

    def filter_commands(self, *args):
        query = self.search_var.get().lower().strip()
        if not query:
            self.render_list(self.all_commands)
            self.update_sidebar_counter(len(self.all_commands))
            return

        filtered = {
            name: desc for name, desc in self.all_commands.items()
            if query in name or query in desc.lower()
        }
        self.render_list(filtered)
        self.update_sidebar_counter(len(filtered))

if __name__ == "__main__":
    app = BetterHelpMeGUI()
    app.mainloop()
