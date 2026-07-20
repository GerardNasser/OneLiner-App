import customtkinter as ctk

from flatten import flatten_text

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class OneLinerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("One-Liner")
        self.geometry("660x700")
        self.minsize(500, 550)
        self.resizable(True, True)

        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(5, weight=1)

        # ── Title ──
        ctk.CTkLabel(
            self,
            text="One-Liner",
            font=ctk.CTkFont(size=28, weight="bold"),
        ).grid(row=0, column=0, padx=30, pady=(24, 2), sticky="w")

        ctk.CTkLabel(
            self,
            text="Paste text → get one clean line with no line breaks.",
            font=ctk.CTkFont(size=13),
            text_color="gray70",
        ).grid(row=1, column=0, padx=30, pady=(0, 10), sticky="w")

        # ── Input label ──
        input_label_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_label_frame.grid(row=2, column=0, padx=30, pady=(0, 4), sticky="nsew")
        input_label_frame.grid_columnconfigure(0, weight=1)
        input_label_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            input_label_frame,
            text="INPUT",
            font=ctk.CTkFont(size=11),
            text_color="gray60",
        ).grid(row=0, column=0, sticky="w")

        self.input_box = ctk.CTkTextbox(
            input_label_frame,
            font=ctk.CTkFont(family="Courier", size=13),
            wrap="word",
        )
        self.input_box.grid(row=1, column=0, sticky="nsew")
        self.input_box.insert("0.0", "Paste your text here…")
        self.input_box.bind("<FocusIn>", self._clear_placeholder)
        self.input_box.bind("<FocusOut>", self._restore_placeholder)
        self._placeholder_active = True

        # ── Buttons ──
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=3, column=0, pady=14)

        ctk.CTkButton(
            btn_frame,
            text="⌘⇧V  Paste & Flatten",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=200,
            height=42,
            command=self._paste_and_flatten,
        ).pack(side="left", padx=(0, 12))

        ctk.CTkButton(
            btn_frame,
            text="⟶  Flatten",
            font=ctk.CTkFont(size=13),
            fg_color="gray30",
            hover_color="gray40",
            width=120,
            height=42,
            command=self._do_flatten,
        ).pack(side="left", padx=(0, 12))

        ctk.CTkButton(
            btn_frame,
            text="Clear All",
            font=ctk.CTkFont(size=13),
            fg_color="gray30",
            hover_color="gray40",
            width=100,
            height=42,
            command=self._clear_all,
        ).pack(side="left")

        # ── Options ──
        options_frame = ctk.CTkFrame(self, fg_color="transparent")
        options_frame.grid(row=4, column=0, padx=30, pady=(0, 10))

        self.join_hyphens_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            options_frame,
            text="Join hyphenated line breaks (exam-ple → example)",
            variable=self.join_hyphens_var,
            font=ctk.CTkFont(size=12),
            checkbox_width=18,
            checkbox_height=18,
        ).pack(side="left", padx=(0, 18))

        self.keep_paragraphs_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            options_frame,
            text="Preserve paragraph breaks",
            variable=self.keep_paragraphs_var,
            font=ctk.CTkFont(size=12),
            checkbox_width=18,
            checkbox_height=18,
        ).pack(side="left")

        # ── Output label ──
        output_label_frame = ctk.CTkFrame(self, fg_color="transparent")
        output_label_frame.grid(row=5, column=0, padx=30, pady=(0, 4), sticky="nsew")
        output_label_frame.grid_columnconfigure(0, weight=1)
        output_label_frame.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(5, weight=1)

        ctk.CTkLabel(
            output_label_frame,
            text="OUTPUT",
            font=ctk.CTkFont(size=11),
            text_color="gray60",
        ).grid(row=0, column=0, sticky="w")

        self.output_box = ctk.CTkTextbox(
            output_label_frame,
            font=ctk.CTkFont(family="Courier", size=13),
            wrap="word",
            state="disabled",
            text_color="#4ECFA8",
        )
        self.output_box.grid(row=1, column=0, sticky="nsew")

        # ── Copy + status row ──
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.grid(row=6, column=0, pady=(8, 6))

        ctk.CTkButton(
            bottom_frame,
            text="Copy Result",
            font=ctk.CTkFont(size=13),
            fg_color="gray30",
            hover_color="gray40",
            width=140,
            height=36,
            command=self._copy_result,
        ).pack(side="left", padx=(0, 14))

        self.status_label = ctk.CTkLabel(
            bottom_frame,
            text="",
            font=ctk.CTkFont(size=13),
            text_color="#4ECFA8",
        )
        self.status_label.pack(side="left")

        # ── Footer tip ──
        ctk.CTkLabel(
            self,
            text="⌘⇧V pastes, flattens, and copies in one step  ·  ⌘↩ flattens the input box",
            font=ctk.CTkFont(size=11),
            text_color="gray50",
        ).grid(row=7, column=0, pady=(0, 14))

        # Keyboard shortcuts
        self.bind("<Command-Return>", lambda e: self._do_flatten())
        self.bind("<Control-Return>", lambda e: self._do_flatten())
        self.bind("<Command-Shift-v>", lambda e: self._paste_and_flatten())
        self.bind("<Command-Shift-V>", lambda e: self._paste_and_flatten())
        self.bind("<Control-Shift-v>", lambda e: self._paste_and_flatten())
        self.bind("<Control-Shift-V>", lambda e: self._paste_and_flatten())

    # ── Placeholder helpers ──
    def _clear_placeholder(self, event=None):
        if self._placeholder_active:
            self.input_box.delete("0.0", "end")
            self.input_box.configure(text_color=("gray10", "gray90"))
            self._placeholder_active = False

    def _restore_placeholder(self, event=None):
        content = self.input_box.get("0.0", "end").strip()
        if not content:
            self.input_box.configure(text_color="gray50")
            self.input_box.insert("0.0", "Paste your text here…")
            self._placeholder_active = True

    # ── Actions ──
    def _paste_and_flatten(self):
        try:
            clip = self.clipboard_get()
        except Exception:
            clip = ""
        if not clip.strip():
            self._flash_status("⚠  Clipboard is empty!", "orange")
            return

        self._clear_placeholder()
        self.input_box.delete("0.0", "end")
        self.input_box.insert("0.0", clip)
        self._placeholder_active = False

        self._do_flatten()

        result = self.output_box.get("0.0", "end").strip()
        if result and not result.startswith("(empty"):
            self.clipboard_clear()
            self.clipboard_append(result)
            self._flash_status(
                f"✓  Flattened & copied — {len(result):,} chars", "#4ECFA8"
            )

    def _do_flatten(self):
        if self._placeholder_active:
            self._flash_status("⚠  Paste some text first!", "orange")
            return

        raw = self.input_box.get("0.0", "end")
        result = flatten_text(
            raw,
            join_hyphens=self.join_hyphens_var.get(),
            keep_paragraphs=self.keep_paragraphs_var.get(),
        )

        self.output_box.configure(state="normal")
        self.output_box.delete("0.0", "end")

        if not result:
            self.output_box.configure(text_color="orange")
            self.output_box.insert("0.0", "(empty — input was whitespace only)")
        else:
            self.output_box.configure(text_color="#4ECFA8")
            self.output_box.insert("0.0", result)

        self.output_box.configure(state="disabled")
        self._flash_status(f"✓  Done — {len(result):,} chars", "#4ECFA8")

    def _clear_all(self):
        self.input_box.configure(text_color="gray50")
        self.input_box.delete("0.0", "end")
        self.input_box.insert("0.0", "Paste your text here…")
        self._placeholder_active = True

        self.output_box.configure(state="normal")
        self.output_box.delete("0.0", "end")
        self.output_box.configure(state="disabled")

        self.status_label.configure(text="")

    def _copy_result(self):
        content = self.output_box.get("0.0", "end").strip()
        if not content or content.startswith("(empty"):
            self._flash_status("⚠  Nothing to copy!", "orange")
            return
        self.clipboard_clear()
        self.clipboard_append(content)
        self._flash_status("✓  Copied to clipboard!", "#4ECFA8")

    def _flash_status(self, msg: str, color: str = "#4ECFA8"):
        self.status_label.configure(text=msg, text_color=color)
        self.after(3000, lambda: self.status_label.configure(text=""))


if __name__ == "__main__":
    app = OneLinerApp()
    app.mainloop()