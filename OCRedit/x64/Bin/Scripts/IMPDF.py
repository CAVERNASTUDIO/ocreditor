#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os
import io

try:
    from pypdf import PdfReader, PdfWriter, Transformation
    from pypdf.generic import RectangleObject
except Exception:
    PdfReader = None
    PdfWriter = None
    Transformation = None
    RectangleObject = None

# --- Configuración A4 ---
A4_WIDTH_PT = 595.276  # puntos (72 pts = 1 inch) ~210 mm
A4_HEIGHT_PT = 841.89  # puntos ~297 mm
TARGET_DPI = 300       # DPI objetivo para la página A4

def pts_to_pixels(points, dpi=TARGET_DPI):
    inches = points / 72.0
    return int(round(inches * dpi))

# Lista global de rutas
archivos_rutas = []

# --- UI básicas ---
def seleccionar_archivos():
    tipos = [
        ("Imágenes y PDF", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif *.gif *.webp *.pdf"),
        ("Imágenes", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif *.gif *.webp"),
        ("PDF", "*.pdf"),
        ("Todos los archivos", "*.*")
    ]
    archivos = filedialog.askopenfilenames(title="Selecciona imágenes o PDFs", filetypes=tipos)
    for archivo in archivos:
        archivos_rutas.append(archivo)
        lista.insert(tk.END, archivo)

def eliminar_seleccion():
    sel = lista.curselection()
    if not sel:
        messagebox.showinfo("Información", "No hay ningún elemento seleccionado.")
        return
    for index in reversed(sel):
        lista.delete(index)
        archivos_rutas.pop(index)

def limpiar_lista():
    archivos_rutas.clear()
    lista.delete(0, tk.END)

def elegir_destino():
    escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
    ruta = filedialog.asksaveasfilename(
        title="Guardar PDF como",
        defaultextension=".pdf",
        initialdir=escritorio,
        filetypes=[("PDF", "*.pdf")]
    )
    if ruta:
        salida_var.set(ruta)

# --- Guardar/abrir/ejecutar proyecto (.txt) ---
def guardar_proyecto():
    if not archivos_rutas:
        messagebox.showwarning("Aviso", "La lista está vacía. Añade archivos antes de guardar un proyecto.")
        return
    escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
    ruta = filedialog.asksaveasfilename(
        title="Guardar proyecto como",
        defaultextension=".txt",
        initialdir=escritorio,
        filetypes=[("Texto", "*.txt")]
    )
    if not ruta:
        return
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("# Proyecto de rutas - una ruta por línea\n")
            for p in archivos_rutas:
                f.write(p + "\n")
        messagebox.showinfo("Éxito", f"Proyecto guardado en:\n{ruta}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el proyecto:\n{e}")

def abrir_proyecto():
    ruta = filedialog.askopenfilename(
        title="Abrir proyecto (.txt)",
        filetypes=[("Texto", "*.txt"), ("Todos los archivos", "*.*")]
    )
    if not ruta:
        return
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")
        return

    nuevas_rutas = []
    errores = []
    for i, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Expandir ~ y variables de entorno
        line_expanded = os.path.expanduser(os.path.expandvars(line))
        if os.path.exists(line_expanded):
            nuevas_rutas.append(line_expanded)
        else:
            errores.append((i, line))

    if errores:
        msg = "Algunas rutas no existen y fueron omitidas:\n"
        for ln, val in errores[:10]:
            msg += f"Linea {ln}: {val}\n"
        if len(errores) > 10:
            msg += f"...y {len(errores)-10} más.\n"
        msg += "\n¿Deseas continuar cargando las rutas válidas?"
        if not messagebox.askyesno("Rutas faltantes", msg):
            return

    # Reemplazar lista actual por las nuevas rutas válidas
    archivos_rutas.clear()
    lista.delete(0, tk.END)
    for p in nuevas_rutas:
        archivos_rutas.append(p)
        lista.insert(tk.END, p)

    messagebox.showinfo("Proyecto cargado", f"Se cargaron {len(nuevas_rutas)} rutas válidas desde:\n{ruta}")

def ejecutar_proyecto():
    ruta = filedialog.askopenfilename(
        title="Seleccionar proyecto para ejecutar (.txt)",
        filetypes=[("Texto", "*.txt"), ("Todos los archivos", "*.*")]
    )
    if not ruta:
        return
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")
        return

    nuevas_rutas = []
    errores = []
    for i, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        line_expanded = os.path.expanduser(os.path.expandvars(line))
        if os.path.exists(line_expanded):
            nuevas_rutas.append(line_expanded)
        else:
            errores.append((i, line))

    if not nuevas_rutas:
        messagebox.showwarning("Aviso", "No se encontraron rutas válidas en el proyecto.")
        return

    if errores:
        msg = "Algunas rutas no existen y fueron omitidas:\n"
        for ln, val in errores[:10]:
            msg += f"Linea {ln}: {val}\n"
        if len(errores) > 10:
            msg += f"...y {len(errores)-10} más.\n"
        msg += "\nSe ejecutará el proyecto con las rutas válidas. ¿Continuar?"
        if not messagebox.askyesno("Rutas faltantes", msg):
            return

    # Cargar rutas en la lista y en la variable global
    archivos_rutas.clear()
    lista.delete(0, tk.END)
    for p in nuevas_rutas:
        archivos_rutas.append(p)
        lista.insert(tk.END, p)

    # Preguntar si desea elegir archivo de salida antes de ejecutar
    if not salida_var.get().strip():
        if messagebox.askyesno("Salida", "No hay archivo de salida seleccionado. ¿Deseas elegir uno ahora?"):
            elegir_destino()

    # Ejecutar la generación del PDF con las rutas cargadas
    generar_pdf()

# --- Convertir imagen a PDF A4 en memoria escalando siempre ---
def image_to_a4_pdf_bytes_scale_all(path):
    """
    Escala la imagen (upscale o downscale) para que ocupe lo máximo posible dentro de A4
    manteniendo la relación de aspecto. Devuelve BytesIO con PDF de una página A4.
    """
    px_w = pts_to_pixels(A4_WIDTH_PT, TARGET_DPI)
    px_h = pts_to_pixels(A4_HEIGHT_PT, TARGET_DPI)

    img = Image.open(path).convert("RGB")
    orig_w, orig_h = img.width, img.height

    # Calcular factor para escalar la imagen hasta que una de las dimensiones llene A4
    scale_w = px_w / orig_w
    scale_h = px_h / orig_h
    scale = min(scale_w, scale_h)  # para que quepa dentro de A4
    # Si quieres que llene completamente (posible recorte), usar max(scale_w, scale_h)
    new_w = max(1, int(round(orig_w * scale)))
    new_h = max(1, int(round(orig_h * scale)))

    # Redimensionar (si scale>1 se amplía; si <1 se reduce)
    img_resized = img.resize((new_w, new_h), Image.LANCZOS)

    # Crear fondo blanco A4 y pegar la imagen centrada
    fondo = Image.new("RGB", (px_w, px_h), (255, 255, 255))
    offset_x = (px_w - new_w) // 2
    offset_y = (px_h - new_h) // 2
    fondo.paste(img_resized, (offset_x, offset_y))

    bio = io.BytesIO()
    fondo.save(bio, format="PDF", resolution=TARGET_DPI)
    bio.seek(0)
    return bio

# --- Normalizar página PDF existente a A4 escalando siempre ---
def normalize_pdf_page_to_a4_scale_all(page):
    """
    Escala y centra una página PDF dentro de A4. Calcula factor de escala para que la
    página quepa en A4 manteniendo aspecto (se escala up o down según sea necesario).
    """
    try:
        w = float(page.mediabox.width)
        h = float(page.mediabox.height)
    except Exception:
        return page

    # factor para que quepa dentro de A4 (si quieres llenar y recortar, usar max)
    scale = min(A4_WIDTH_PT / w, A4_HEIGHT_PT / h)

    new_w = w * scale
    new_h = h * scale
    tx = (A4_WIDTH_PT - new_w) / 2.0
    ty = (A4_HEIGHT_PT - new_h) / 2.0

    trans = Transformation().scale(scale, scale).translate(tx, ty)
    try:
        page.add_transformation(trans)
    except Exception:
        # si add_transformation no está disponible, intentar aplicar matrix manualmente
        pass

    page.mediabox = RectangleObject([0, 0, A4_WIDTH_PT, A4_HEIGHT_PT])
    try:
        page.cropbox = RectangleObject([0, 0, A4_WIDTH_PT, A4_HEIGHT_PT])
    except Exception:
        pass

    return page

# --- Generación del PDF final (manteniendo streams vivos) ---
def generar_pdf():
    if not archivos_rutas:
        messagebox.showwarning("Aviso", "No se han cargado archivos.")
        return

    if PdfReader is None or PdfWriter is None or Transformation is None or RectangleObject is None:
        messagebox.showerror("Dependencia faltante", "Instala 'pypdf' y 'Pillow' con: pip install pypdf pillow")
        return

    ruta_pdf = salida_var.get().strip()
    if not ruta_pdf:
        escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
        ruta_pdf = os.path.join(escritorio, "resultado_a4_scaled.pdf")

    writer = PdfWriter()
    temp_streams = []

    try:
        for ruta in archivos_rutas:
            ext = os.path.splitext(ruta)[1].lower()
            if ext == ".pdf":
                try:
                    reader = PdfReader(ruta)
                    for page in reader.pages:
                        norm = normalize_pdf_page_to_a4_scale_all(page)
                        writer.add_page(norm)
                except Exception as e:
                    messagebox.showwarning("Aviso", f"No se pudo leer PDF: {ruta}\n{e}")
            else:
                try:
                    bio = image_to_a4_pdf_bytes_scale_all(ruta)
                    temp_streams.append(bio)
                    mem_reader = PdfReader(bio)
                    for page in mem_reader.pages:
                        try:
                            page.mediabox = RectangleObject([0, 0, A4_WIDTH_PT, A4_HEIGHT_PT])
                        except Exception:
                            pass
                        norm = normalize_pdf_page_to_a4_scale_all(page)
                        writer.add_page(norm)
                except Exception as e:
                    messagebox.showwarning("Aviso", f"No se pudo procesar imagen: {ruta}\n{e}")

        with open(ruta_pdf, "wb") as f_out:
            writer.write(f_out)

        messagebox.showinfo("Éxito", f"PDF generado exitosamente en: {ruta_pdf}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al generar el PDF:\n{e}")
    finally:
        for s in temp_streams:
            try:
                s.close()
            except Exception:
                pass

# --- Funciones de control y reordenado (idénticas a versiones previas) ---
def scroll_up():
    lista.yview_scroll(-1, "units")

def scroll_down():
    lista.yview_scroll(1, "units")

def page_up():
    lista.yview_scroll(-1, "pages")

def page_down():
    lista.yview_scroll(1, "pages")

def move_selected_up():
    sel = lista.curselection()
    if not sel:
        return
    for index in sel:
        if index == 0:
            continue
        text = lista.get(index)
        archivos_rutas[index], archivos_rutas[index-1] = archivos_rutas[index-1], archivos_rutas[index]
        lista.delete(index)
        lista.insert(index-1, text)
        lista.selection_set(index-1)
    lista.see(max(sel[0]-1,0))

def move_selected_down():
    sel = lista.curselection()
    if not sel:
        return
    for index in reversed(sel):
        if index >= lista.size()-1:
            continue
        text = lista.get(index)
        archivos_rutas[index], archivos_rutas[index+1] = archivos_rutas[index+1], archivos_rutas[index]
        lista.delete(index)
        lista.insert(index+1, text)
        lista.selection_set(index+1)
    lista.see(min(sel[-1]+1, lista.size()-1))

def move_selected_top():
    sel = lista.curselection()
    if not sel:
        return
    items = [lista.get(i) for i in sel]
    for i in reversed(sel):
        lista.delete(i)
        archivos_rutas.pop(i)
    for i, item in enumerate(items):
        lista.insert(i, item)
        archivos_rutas.insert(i, item)
        lista.selection_set(i)
    lista.see(0)

def move_selected_bottom():
    sel = lista.curselection()
    if not sel:
        return
    items = [lista.get(i) for i in sel]
    for i in reversed(sel):
        lista.delete(i)
        archivos_rutas.pop(i)
    start = lista.size()
    for i, item in enumerate(items):
        lista.insert(start + i, item)
        archivos_rutas.append(item)
        lista.selection_set(start + i)
    lista.see(lista.size()-1)

# --- Interfaz gráfica ---
root = tk.Tk()
root.title("IMG PDF A4")
root.geometry("900x560")

main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

list_frame = tk.Frame(main_frame)
list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
lista = tk.Listbox(list_frame, width=100, height=22, selectmode=tk.EXTENDED, yscrollcommand=scrollbar.set)
scrollbar.config(command=lista.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

control_frame = tk.Frame(main_frame)
control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(8,0))

tk.Label(control_frame, text="Reordenar").pack(pady=(12,2))
tk.Button(control_frame, text="Subir", width=12, command=move_selected_up).pack(pady=2)
tk.Button(control_frame, text="Bajar", width=12, command=move_selected_down).pack(pady=2)
tk.Button(control_frame, text="Mover al Top", width=12, command=move_selected_top).pack(pady=2)
tk.Button(control_frame, text="Mover al Bottom", width=12, command=move_selected_bottom).pack(pady=2)

frame_botones = tk.Frame(root)
frame_botones.pack(fill=tk.X, padx=12, pady=(6,0))

btn_seleccionar = tk.Button(frame_botones, text="Seleccionar archivos", command=seleccionar_archivos)
btn_seleccionar.pack(side=tk.LEFT, padx=6, pady=6)

btn_eliminar = tk.Button(frame_botones, text="Eliminar seleccionado", command=eliminar_seleccion)
btn_eliminar.pack(side=tk.LEFT, padx=6, pady=6)

btn_limpiar = tk.Button(frame_botones, text="Limpiar lista", command=limpiar_lista)
btn_limpiar.pack(side=tk.LEFT, padx=6, pady=6)

# Botones de proyecto
btn_guardar_proy = tk.Button(frame_botones, text="Guardar proyecto", command=guardar_proyecto)
btn_guardar_proy.pack(side=tk.LEFT, padx=6, pady=6)

btn_abrir_proy = tk.Button(frame_botones, text="Abrir proyecto", command=abrir_proyecto)
btn_abrir_proy.pack(side=tk.LEFT, padx=6, pady=6)

btn_ejecutar_proy = tk.Button(frame_botones, text="Ejecutar proyecto (.txt)", command=ejecutar_proyecto, bg="#2196F3", fg="white")
btn_ejecutar_proy.pack(side=tk.LEFT, padx=6, pady=6)

salida_var = tk.StringVar()
salida_frame = tk.Frame(root)
salida_frame.pack(fill=tk.X, padx=12, pady=(6,0))

tk.Label(salida_frame, text="Archivo de salida:").pack(side=tk.LEFT, padx=(0,6))
salida_entry = tk.Entry(salida_frame, textvariable=salida_var, width=80)
salida_entry.pack(side=tk.LEFT, padx=(0,6))
btn_elegir = tk.Button(salida_frame, text="Elegir...", command=elegir_destino)
btn_elegir.pack(side=tk.LEFT)

btn_generar = tk.Button(root, text="Generar PDF (A4 escalado)", command=generar_pdf, bg="#4CAF50", fg="white")
btn_generar.pack(pady=12)

help_text = (
    "Soportado: imágenes (.jpg .jpeg .png .bmp .tiff .gif .webp) y archivos .pdf.\n"
    "Todas las entradas se escalan para ajustarse a A4 manteniendo relación de aspecto.\n"
    "Ordena la lista antes de generar para definir el orden de las páginas.\n"
    "Puedes guardar/abrir proyectos (.txt) con una ruta por línea. Las líneas que comienzan con # son comentarios.\n"
    "Copiright (C) - 2025 Ing. Erik Alejandro García Aparicio. All right reserved."
)
tk.Label(root, text=help_text, fg="gray", justify=tk.LEFT).pack(pady=(0,12))


root.mainloop()
