import customtkinter as ctk
import os
import json
import datetime

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
app = ctk.CTk()
app.withdraw()
app.title("NekoLearn")
app.geometry("900x600")
app.resizable(False, False)
app.grid_propagate(False)

splash = ctk.CTkToplevel(app)
splash.overrideredirect(True)
splash.configure(fg_color="#0b0b0e")
splash.attributes("-topmost", True)
splash.attributes("-alpha", 1.0)

W, H = 900, 600
splash.geometry(f"{W}x{H}+100+60")

welcome = ctk.CTkLabel(
    splash,
    text="Welcome to NekoLearn",
    font=("Inter", 28, "bold"),
    text_color="#ff9ec4"
)
welcome.place(relx=0.5, rely=0.5, anchor="center")


def fade_out_splash(step=0, steps=25, total_ms=700):
    alpha = max(0.0, 1.0 - step/steps)
    try:
        splash.attributes("-alpha", alpha)
    except Exception:
        splash.destroy()
        app.deiconify()
        return

    if step < steps:
        splash.after(max(1, total_ms // steps), fade_out_splash, step+1, steps, total_ms)
    else:
        splash.destroy()
        app.deiconify()
        app.lift()
        app.focus_force()


def _hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def _rgb_to_hex(rgb):
    return "#" + "".join(f"{c:02x}" for c in rgb)


def _lerp(a, b, t):
    return int(a + (b - a) * t)


def fade_in_label(label, start="#1e1e1e", end="#bda9c9", steps=24, duration_ms=600):
    start_rgb = _hex_to_rgb(start)
    end_rgb = _hex_to_rgb(end)
    interval = max(1, duration_ms // steps)

    def step(i=0):
        t = i / steps
        rgb = tuple(_lerp(sa, ea, t) for sa, ea in zip(start_rgb, end_rgb))
        label.configure(text_color=_rgb_to_hex(rgb))
        if i < steps:
            label.after(interval, step, i + 1)

    step()


def save_vocab():
    with open('vocab.json', 'w', encoding='utf-8') as file:
        json.dump(words, file, ensure_ascii=False, indent=2)


def load_vocab():
    if os.path.exists('vocab.json'):
        with open('vocab.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    return []


def get_words_per_day(words_list):
    counts = {}

    for w in words_list:
        raw = w.get("added")
        if not raw:
            continue
        day = raw.split("T")[0]
        counts[day] = counts.get(day, 0) + 1

    dates = sorted(counts.keys())
    values = [counts[d] for d in dates]
    return dates, values


# ---------------------------------------------------------
# GRAPH
# ---------------------------------------------------------
def update_graph():
    for widget in graph_frame.winfo_children():
        widget.destroy()

    dates, values = get_words_per_day(words)

    # Fake previous day if only 1 entry exists
    if len(dates) == 1:
        d0 = datetime.date.fromisoformat(dates[0])
        fake = (d0 - datetime.timedelta(days=1)).isoformat()
        dates = [fake, dates[0]]
        values = [0, values[0]]

    fig = Figure(figsize=(3.9, 2.8), dpi=100)
    ax = fig.add_subplot(111)

    fig.subplots_adjust(
        left=0.15,
        right=0.95,
        top=0.86,
        bottom=0.26
    )

    if dates:
        ax.plot(
            dates,
            values,
            marker="o",
            markersize=9,
            markerfacecolor="#ff8ac9",
            markeredgecolor="#ff8ac9",
            color="#ff8ac9",
            linewidth=3,
            solid_capstyle="round"
        )
    else:
        ax.text(0.5, 0.5, "No data yet.", ha="center", va="center", color="white")

    ax.set_facecolor("#3f2e49")
    fig.patch.set_facecolor("#3f2e49")

    # remove borders
    for spine in ax.spines.values():
        spine.set_visible(False)

    max_y = max(values) if values else 1
    ax.set_yticks(range(0, max_y + 1))
    ax.set_ylim(0, max_y)

    ax.tick_params(colors="white", labelsize=9)

    ax.set_title("Words Added Per Day", color="white", fontsize=13, pad=10)
    ax.set_xlabel("Date", color="white", fontsize=10)
    ax.set_ylabel("Count", color="white", fontsize=10)

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()

    widget = canvas.get_tk_widget()
    widget.pack(fill="both", expand=True)



# ---------------------------------------------------------
# USER ACTIONS
# ---------------------------------------------------------
def toggle_known(index):
    words[index]["known"] = not words[index].get("known", False)
    save_vocab()
    render_list()
    update_graph()


def delete_word(index):
    try:
        del words[index]
        save_vocab()
        render_list()
        update_graph()
    except:
        pass


words = load_vocab()


def on_add():
    term = word_entry.get().strip()
    definition = def_entry.get().strip()
    example = example_entry.get().strip()

    if not term or not definition:
        print("Please fill in Word and Definition.")
        return

    words.append({
        "term": term,
        "definition": definition,
        "example": example,
        "known": False,
        "added": datetime.datetime.now().isoformat()
    })

    save_vocab()

    word_entry.delete(0, "end")
    def_entry.delete(0, "end")
    example_entry.delete(0, "end")

    render_list()
    update_graph()


# helper to create bordered entrys
def make_bordered_entry(parent, placeholder, border_color="#ff8ac9"):
    border = ctk.CTkFrame(parent, fg_color=border_color, corner_radius=8)
    entry = ctk.CTkEntry(border, placeholder_text=placeholder)
    entry.pack(padx=2, pady=2, fill="both", expand=True)
    return border, entry


left_frame = ctk.CTkFrame(app, fg_color="#493457", corner_radius=10, width=400, height=200)
left_frame.grid_propagate(False)
left_frame.grid(row=0, column=0, sticky="nw", padx=20, pady=20)
left_frame.grid_columnconfigure(0, weight=1)

word_border, word_entry = make_bordered_entry(left_frame, "Word")
word_border.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

def_border, def_entry = make_bordered_entry(left_frame, "Definition")
def_border.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

example_border, example_entry = make_bordered_entry(left_frame, "Example")
example_border.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

addWordButton = ctk.CTkButton(
    left_frame,
    text="Add Word",
    fg_color="#C568C9",
    hover_color="#A04ABF",
    text_color="white",
    corner_radius=12,
    font=("Inter", 12, "bold")
)
addWordButton.grid(row=3, column=0, pady=1, padx=20, sticky="ew")

right_frame = ctk.CTkFrame(app, fg_color="#493457", corner_radius=10, width=400, height=500)
right_frame.grid_propagate(False)
right_frame.grid(row=0, column=1, sticky="ne", padx=20, pady=20)
right_frame.grid_columnconfigure(0, weight=1)

list_area = ctk.CTkScrollableFrame(right_frame, fg_color="#3f2e49")
list_area.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
right_frame.grid_rowconfigure(0, weight=1)


# ---------------------------------------------------------
# fixed frame cancer shit
# ---------------------------------------------------------
graph_frame = ctk.CTkFrame(
    app,
    fg_color="#3f2e49",
    corner_radius=10,
    width=420,
    height=320  
)
graph_frame.place(x=20, y=260)



def render_list():
    for child in list_area.winfo_children():
        child.destroy()

    if not words:
        ctk.CTkLabel(list_area, text="No words yet. Add one on the left!",
                     text_color="#e9d7f2").pack(pady=8)
        return

    for i, w in enumerate(words, start=1):
        row = ctk.CTkFrame(list_area, fg_color="#2f2236", corner_radius=8)
        row.pack(fill="x", padx=6, pady=6)

        known_state = w.get("known", False)
        color = "#38C172" if known_state else "#E74C3C"
        hover = "#2E8B57" if known_state else "#C0392B"

        title = f"{i}. {w['term']} → {w['definition']}"
        ctk.CTkLabel(row, text=title,
                     font=("Inter", 14, "bold"),
                     text_color=color).pack(anchor="w", padx=10, pady=(8, 2))

        ex = w.get("example", "").strip()
        if ex:
            ctk.CTkLabel(row, text=f"Example: {ex}", text_color="#d8c6e7")\
                .pack(anchor="w", padx=12, pady=(0, 8))

        btn_frame = ctk.CTkFrame(row, fg_color="#2f2236", corner_radius=0)
        btn_frame.pack(anchor="e", padx=10, pady=(0, 10))

        ctk.CTkButton(
            btn_frame, text="Delete", fg_color="#E74C3C", hover_color="#C0392B",
            text_color="white", width=80, height=28, corner_radius=6,
            command=lambda idx=i-1: delete_word(idx)
        ).pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            btn_frame,
            text=("Known" if known_state else "Unknown"),
            fg_color=color,
            hover_color=hover,
            text_color="white", width=80, height=28, corner_radius=6,
            command=lambda idx=i-1: toggle_known(idx)
        ).pack(side="left")


render_list()
update_graph()

addWordButton.configure(command=on_add)

credit_label = ctk.CTkLabel(
    app, text="Made with <3 by Eloping",
    text_color="#bda9c9",
    font=("Inter", 12, "italic")
)
credit_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

fade_in_label(credit_label, start="#1b1b1f", end="#bda9c9", steps=28, duration_ms=700)

splash.after(600, fade_out_splash)
app.mainloop()
