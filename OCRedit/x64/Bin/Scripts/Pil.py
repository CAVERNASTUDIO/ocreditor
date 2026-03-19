import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import cv2
import pytesseract
from pdf2image import convert_from_path
from reportlab.pdfgen import canvas
from docx import Document

# Configuración de Tesseract-OCR en Windows
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\HP\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tool")

        # Botón para seleccionar archivo
        tk.Button(root, text="Seleccionar archivo (imagen o PDF)", command=self.cargar_archivo).pack(pady=5)

        # Menú de selección de idioma
        tk.Label(root, text="Selecciona el idioma del documento:").pack(pady=5)
        self.idiomas = {
            "Español": "spa",
            "Inglés": "eng",
            "Francés": "fra",
            "Alemán": "deu",
            "Italiano": "ita",
            "Portugués": "por"
        }
        self.selected_lang = tk.StringVar(value="Español")
        tk.OptionMenu(root, self.selected_lang, *self.idiomas.keys()).pack(pady=5)

        # Botón para ejecutar OCR
        tk.Button(root, text="Ejecutar OCR", command=self.ejecutar_ocr).pack(pady=5)

        # Botón para exportar texto
        tk.Button(root, text="Exportar texto", command=self.exportar_texto).pack(pady=5)

        # Campo de salida del texto reconocido
        tk.Label(root, text="Texto reconocido:").pack(pady=5)
        self.text_output = tk.Text(root, height=20, width=90, state="disabled")
        self.text_output.pack(pady=5)

        self.file_path = None
        self.texto_recognized = ""

    def cargar_archivo(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=[("Imágenes y PDF", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.pdf")]
        )
        if archivo:
            self.file_path = archivo
            messagebox.showinfo("Archivo seleccionado", f"Has seleccionado:\n{archivo}")

    def ejecutar_ocr(self):
        if not self.file_path:
            messagebox.showwarning("Sin archivo", "Primero selecciona una imagen o PDF.")
            return

        try:
            texto_total = ""
            idioma = self.idiomas[self.selected_lang.get()]

            if self.file_path.lower().endswith(".pdf"):
                # Convertir PDF a imágenes (una por página)
                paginas = convert_from_path(self.file_path)
                for i, pagina in enumerate(paginas):
                    temp_path = f"temp_page_{i}.png"
                    pagina.save(temp_path, "PNG")
                    texto_total += pytesseract.image_to_string(Image.open(temp_path), lang=idioma) + "\n"
            else:
                # Procesar imagen con OpenCV
                img = cv2.imread(self.file_path)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                thresh = cv2.adaptiveThreshold(
                    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                    cv2.THRESH_BINARY, 11, 2
                )
                temp_path = "temp_ocr.png"
                cv2.imwrite(temp_path, thresh)
                texto_total = pytesseract.image_to_string(Image.open(temp_path), lang=idioma)

            # Guardar texto reconocido
            self.texto_recognized = texto_total

            # Mostrar resultado
            self.text_output.config(state="normal")
            self.text_output.delete("1.0", tk.END)
            self.text_output.insert(tk.END, texto_total)
            self.text_output.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Error OCR", f"Ocurrió un error:\n{e}")

    def exportar_texto(self):
        if not self.texto_recognized.strip():
            messagebox.showwarning("Sin texto", "Primero ejecuta OCR para obtener texto.")
            return

        formato = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivo de texto", "*.txt"),
                       ("Documento Word", "*.docx"),
                       ("PDF", "*.pdf")],
            title="Guardar texto como..."
        )
        if formato:
            try:
                if formato.endswith(".txt"):
                    with open(formato, "w", encoding="utf-8") as f:
                        f.write(self.texto_recognized)

                elif formato.endswith(".docx"):
                    doc = Document()
                    doc.add_paragraph(self.texto_recognized)
                    doc.save(formato)

                elif formato.endswith(".pdf"):
                    c = canvas.Canvas(formato)
                    c.setFont("Helvetica", 12)
                    y = 800
                    for linea in self.texto_recognized.splitlines():
                        c.drawString(50, y, linea)
                        y -= 20
                        if y < 50:  # Nueva página si se llena
                            c.showPage()
                            c.setFont("Helvetica", 12)
                            y = 800
                    c.save()

                messagebox.showinfo("Exportación exitosa", f"Texto exportado a:\n{formato}")
            except Exception as e:
                messagebox.showerror("Error exportación", f"No se pudo exportar:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()
