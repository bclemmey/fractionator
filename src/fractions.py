import re
import os
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import Button, Message, Label

if not os.getenv("fractionator_is_localrun", False):
    license_location = "files/LICENCE.txt"
    ico_location = "files/favicon.ico"
else:
    license_location = "LICENCE.txt"
    ico_location = "./src/favicon.ico"


with open(license_location, "r") as file:
    licence = "".join(file.readlines())

root = tk.Tk()
input_box = ScrolledText(root, width=75, height=15)
output_box = ScrolledText(root, width=75, height=15)
licence_msg = Message(root, text=licence)


def button_action():
    output_box.delete("0.0", tk.END)
    output_box.insert("0.0", process(input_box.get("1.0", tk.END)).rstrip())


button = Button(root, text="Convert Fractions", command=button_action, font=", 12")


def process(string: str):
    vulgar = {
        '1/4': '¼', '1/2': '½', '3/4': '¾', '1/7': '⅐', '1/9': '⅑', '1/10': '⅒', '1/3': '⅓', '2/3': '⅔', '1/5': '⅕',
        '2/5': '⅖', '3/5': '⅗', '4/5': '⅘', '1/6': '⅙', '5/6': '⅚', '1/8': '⅛', '3/8': '⅜', '5/8': '⅝', '7/8': '⅞',
        '0/3': '↉'
    }

    mini_numbers = {
        '0': ('⁰', '₀'), '1': ('¹', '₁'), '2': ('²', '₂'), '3': ('³', '₃'), '4': ('⁴', '₄'),
        '5': ('⁵', '₅'), '6': ('⁶', '₆'), '7': ('⁷', '₇'), '8': ('⁸', '₈'), '9': ('⁹', '₉'),
    }

    for bad, good in vulgar.items():
        string = string.replace(bad, good)

    while True:
        match = re.search(r"(\d+)(/)(\d+)", string)
        if match is None:
            break
        group = match.group()
        split = group.split("/")
        if len(split) != 2:
            continue
        for orig, repl in mini_numbers.items():
            split[0] = split[0].replace(orig, repl[0])
            split[1] = split[1].replace(orig, repl[1])
        joined = "⁄".join(split)
        string = string.replace(group, joined)

    return string


def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(output_box.get("1.0", tk.END))


def clear_licence():
    licence_btn.destroy()
    licence_msg.destroy()
    Label(root, text="Original Text", justify=tk.CENTER, height=2, font=", 16").pack()
    input_box.pack(padx=10, pady=10)
    button.pack(padx=10, pady=10)
    Label(root, text="Converted Text", justify=tk.CENTER, height=2, font=", 16").pack()
    output_box.pack(padx=10, pady=10)
    clipboard_btn.pack(padx=10, pady=10)


licence_btn = Button(root, text="I Understand", command=clear_licence)
clipboard_btn = Button(root, text="Copy to Clipboard", command=copy_to_clipboard)


# if __name__ == '__main__':
licence_msg.pack(padx=10, pady=10)
licence_btn.pack(padx=10, pady=10)
root.title("Fractionator 1.0")
root.iconbitmap(ico_location)
root.mainloop()
