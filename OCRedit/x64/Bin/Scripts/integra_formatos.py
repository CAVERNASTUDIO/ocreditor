import os
import tkinter as tk
from tkinter import filedialog, messagebox, END
from PyPDF2 import PdfMerger
from docx2pdf import convert as docx2pdf
import comtypes.client  # Para PowerPoint y Excel en Windows
from fpdf import FPDF   # Para generar PDF desde texto si se requiere

# --- Conversión de formatos a PDF ---
def convert_to_pdf(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    output_pdf = filepath + ".pdf"

    if ext == ".pdf":
        return filepath
    elif ext in [".docx", ".doc"]:
        docx2pdf(filepath, output_pdf)
    elif ext in [".pptx", ".ppt"]:
        powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
        presentation = powerpoint.Presentations.Open(filepath)
        presentation.SaveAs(output_pdf, 32)  # formato PDF
        presentation.Close()
        powerpoint.Quit()
    elif ext in [".xlsx", ".xls"]:
        excel = comtypes.client.CreateObject("Excel.Application")
        wb = excel.Workbooks.Open(filepath)
        wb.ExportAsFixedFormat(0, output_pdf)
        wb.Close()
        excel.Quit()
    else:
        # Para audio, vídeo o web: se requiere conversión previa a PDF (capturas, transcripciones, etc.)
        raise ValueError(f"Formato {ext} no soportado directamente")

    return output_pdf

# --- Interfaz principal ---
class DocumentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Integrates Formats")

        # Lista de documentos seleccionados
        self.listbox = tk.Listbox(root, width=80, height=20, selectmode=tk.SINGLE)
        self.listbox.pack(pady=10)

        # Botones principales
        btn_frame = tk.Frame(root)
        btn_frame.pack()

        tk.Button(btn_frame, text="Seleccionar documentos", command=self.select_files).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Mover arriba", command=self.move_up).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Mover abajo", command=self.move_down).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Eliminar", command=self.delete_file).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Guardar proyecto", command=self.save_project).grid(row=0, column=4, padx=5)
        tk.Button(btn_frame, text="Abrir proyecto", command=self.open_project).grid(row=0, column=5, padx=5)
        tk.Button(btn_frame, text="Generar PDF", command=self.generate_pdf).grid(row=0, column=6, padx=5)

    def select_files(self):
        files = filedialog.askopenfilenames(title="Selecciona archivos")
        for f in files:
            self.listbox.insert(END, f)

    def move_up(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        index = sel[0]
        if index > 0:
            text = self.listbox.get(index)
            self.listbox.delete(index)
            self.listbox.insert(index-1, text)
            self.listbox.selection_set(index-1)

    def move_down(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        index = sel[0]
        if index < self.listbox.size()-1:
            text = self.listbox.get(index)
            self.listbox.delete(index)
            self.listbox.insert(index+1, text)
            self.listbox.selection_set(index+1)

    def delete_file(self):
        sel = self.listbox.curselection()
        if sel:
            self.listbox.delete(sel[0])

    def save_project(self):
        if self.listbox.size() == 0:
            messagebox.showwarning("Atención", "No hay documentos seleccionados.")
            return
        project_file = filedialog.asksaveasfilename(defaultextension=".txt",
                                                    filetypes=[("Archivo de texto", "*.txt")],
                                                    title="Guardar proyecto")
        if project_file:
            with open(project_file, "w", encoding="utf-8") as f:
                for i in range(self.listbox.size()):
                    f.write(self.listbox.get(i) + "\n")
            messagebox.showinfo("Proyecto guardado", f"Proyecto guardado en:\n{project_file}")

    def open_project(self):
        project_file = filedialog.askopenfilename(filetypes=[("Archivo de texto", "*.txt")],
                                                  title="Abrir proyecto")
        if project_file and os.path.exists(project_file):
            self.listbox.delete(0, END)  # limpiar lista actual
            with open(project_file, "r", encoding="utf-8") as f:
                for line in f:
                    self.listbox.insert(END, line.strip())
            messagebox.showinfo("Proyecto cargado", f"Proyecto cargado desde:\n{project_file}")

    def generate_pdf(self):
        if self.listbox.size() == 0:
            messagebox.showwarning("Atención", "No hay documentos seleccionados.")
            return
        pdfs = []
        try:
            for i in range(self.listbox.size()):
                filepath = self.listbox.get(i)
                pdfs.append(convert_to_pdf(filepath))
            merger = PdfMerger()
            for pdf in pdfs:
                merger.append(pdf)
            output_file = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                       filetypes=[("PDF", "*.pdf")],
                                                       title="Guardar PDF combinado")
            if output_file:
                merger.write(output_file)
                merger.close()
                messagebox.showinfo("PDF generado", f"PDF creado exitosamente:\n{output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al generar el PDF:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DocumentManagerApp(root)
    root.mainloop()
