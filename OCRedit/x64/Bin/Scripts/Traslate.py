import tkinter as tk
from tkinter import messagebox
from deep_translator import GoogleTranslator

class TraductorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Translator")

        tk.Label(root, text="Texto a traducir:").pack(pady=5)
        self.text_input = tk.Text(root, height=10, width=80)
        self.text_input.pack(pady=5)

        tk.Label(root, text="Selecciona idioma de destino:").pack(pady=5)
        self.idiomas = {
            "Inglés": "en",
            "Francés": "fr",
            "Alemán": "de",
            "Italiano": "it",
            "Portugués": "pt",
            "Español": "es"
        }
        self.selected_lang = tk.StringVar(value="Inglés")
        self.lang_menu = tk.OptionMenu(root, self.selected_lang, *self.idiomas.keys())
        self.lang_menu.pack(pady=5)

        tk.Button(root, text="Traducir", command=self.traducir).pack(pady=5)

        tk.Label(root, text="Traducción:").pack(pady=5)
        self.text_output = tk.Text(root, height=10, width=80, state="disabled")
        self.text_output.pack(pady=5)

    def traducir(self):
        texto = self.text_input.get("1.0", tk.END).strip()
        palabras = len(texto.split())

        if palabras > 1000:
            messagebox.showwarning("Límite excedido", "El texto no puede superar las 1000 palabras.")
            return

        if not texto:
            messagebox.showwarning("Texto vacío", "Por favor ingresa un texto para traducir.")
            return

        try:
            destino = self.idiomas[self.selected_lang.get()]
            traduccion = GoogleTranslator(source="auto", target=destino).translate(texto)
            self.text_output.config(state="normal")
            self.text_output.delete("1.0", tk.END)
            self.text_output.insert(tk.END, traduccion)
            self.text_output.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al traducir:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TraductorApp(root)
    root.mainloop()
