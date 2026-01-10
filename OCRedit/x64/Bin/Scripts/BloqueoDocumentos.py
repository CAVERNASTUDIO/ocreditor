import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pikepdf

# Lista de documentos aceptados
DOCUMENTOS_ACEPTADOS = [".pdf"]

def proteger_pdf(ruta_pdf, permisos_obj):
    """
    Aplica restricciones de seguridad al PDF indicado usando el objeto pikepdf.Permissions recibido.
    """
    try:
        with pikepdf.open(ruta_pdf, allow_overwriting_input=True) as pdf:
            pdf.save(
                ruta_pdf,
                encryption=pikepdf.Encryption(
                    user="",       # No se requiere contraseña para abrir
                    owner="",      # No se establece contraseña de propietario
                    allow=permisos_obj,
                    R=6            # Cifrado AES-256
                )
            )
        messagebox.showinfo("Éxito", "✅ El archivo ha sido protegido y sobrescrito con las restricciones seleccionadas.")
    except Exception as e:
        messagebox.showerror("Error", f"❌ Error al proteger el archivo:\n{e}")

def seleccionar_archivo(vars_permisos):
    """
    Abre un cuadro de diálogo para seleccionar el archivo PDF y aplica los permisos seleccionados.
    """
    ruta_pdf = filedialog.askopenfilename(
        title="Seleccione un documento",
        filetypes=[("Documentos PDF", "*.pdf")]
    )

    if not ruta_pdf:
        return  # Usuario canceló

    _, extension = os.path.splitext(ruta_pdf)
    if extension.lower() not in DOCUMENTOS_ACEPTADOS:
        messagebox.showerror("Archivo no válido", f"❌ Solo se aceptan: {', '.join(DOCUMENTOS_ACEPTADOS)}")
        return

    # Construir objeto pikepdf.Permissions a partir de las variables (True = bloquear en UI)
    permisos = pikepdf.Permissions(
        accessibility=not vars_permisos["accessibility"].get(),
        extract=not vars_permisos["extract"].get(),
        modify_annotation=not vars_permisos["modify_annotation"].get(),
        modify_assembly=not vars_permisos["modify_assembly"].get(),
        modify_form=not vars_permisos["modify_form"].get(),
        modify_other=not vars_permisos["modify_other"].get(),
        print_lowres=not vars_permisos["print_lowres"].get(),
        print_highres=not vars_permisos["print_highres"].get()
    )

    proteger_pdf(ruta_pdf, permisos)

def main():
    # Crear ventana principal
    ventana = tk.Tk()
    ventana.title("RCO Blockdf")
    ventana.geometry("420x420")
    ventana.resizable(False, False)

    # Etiqueta principal
    etiqueta = tk.Label(ventana, text="Seleccione un documento PDF y los permisos a bloquear", font=("Arial", 12))
    etiqueta.pack(pady=12)

    # Frame para checkbuttons de permisos
    frame_permisos = tk.LabelFrame(ventana, text="Permisos a bloquear (marque para bloquear)", padx=10, pady=10, font=("Arial", 10))
    frame_permisos.pack(padx=12, pady=6, fill="both")

    # Variables para cada permiso (True = bloquear)
    vars_permisos = {
        "accessibility": tk.BooleanVar(value=True),
        "extract": tk.BooleanVar(value=True),
        "modify_annotation": tk.BooleanVar(value=True),
        "modify_assembly": tk.BooleanVar(value=True),
        "modify_form": tk.BooleanVar(value=True),
        "modify_other": tk.BooleanVar(value=True),
        "print_lowres": tk.BooleanVar(value=True),
        "print_highres": tk.BooleanVar(value=True)
    }

    # Crear checkbuttons (cada llamada está en una sola línea para evitar truncados)
    tk.Checkbutton(frame_permisos, text="Bloquear accesibilidad (lectores de pantalla)", variable=vars_permisos["accessibility"], anchor="w", justify="left").pack(fill="x", pady=2)
    tk.Checkbutton(frame_permisos, text="Bloquear extracción de contenido (copiar/extraer)", variable=vars_permisos["extract"], anchor="w", justify="left").pack(fill="x", pady=2)
    tk.Checkbutton(frame_permisos, text="Bloquear modificación de anotaciones", variable=vars_permisos["modify_annotation"], anchor="w", justify="left").pack(fill="x", pady=2)
    tk.Checkbutton(frame_permisos, text="Bloquear ensamblaje (reordenar/páginas)", variable=vars_permisos["modify_assembly"], anchor="w", justify="left").pack(fill="x", pady=2)
    tk.Checkbutton(frame_permisos, text="Bloquear modificación de formularios", variable=vars_permisos["modify_form"], anchor="w", justify="left").pack(fill="x", pady=2)
    tk.Checkbutton(frame_permisos, text="Bloquear otras modificaciones", variable=vars_permisos["modify_other"], anchor="w", justify="left").pack(fill="x", pady=2)
    tk.Checkbutton(frame_permisos, text="Bloquear impresión en baja resolución", variable=vars_permisos["print_lowres"], anchor="w", justify="left").pack(fill="x", pady=2)
    tk.Checkbutton(frame_permisos, text="Bloquear impresión en alta resolución", variable=vars_permisos["print_highres"], anchor="w", justify="left").pack(fill="x", pady=2)

    # Botón para seleccionar archivo y aplicar permisos
    boton = tk.Button(ventana, text="Seleccionar archivo y aplicar permisos", command=lambda: seleccionar_archivo(vars_permisos), font=("Arial", 10), bg="#4CAF50", fg="white")
    boton.pack(pady=14)

    # Texto con formatos aceptados
    formatos = tk.Label(ventana, text=f"Documentos aceptados: {', '.join(DOCUMENTOS_ACEPTADOS)}", font=("Arial", 10))
    formatos.pack(pady=6)

    # Botón para restaurar valores por defecto (bloquear todo)
    def restaurar_defecto():
        for v in vars_permisos.values():
            v.set(True)
        messagebox.showinfo("Restaurado", "Se han marcado los permisos para bloquear por defecto.")

    btn_defecto = tk.Button(ventana, text="Restaurar bloqueo por defecto", command=restaurar_defecto, font=("Arial", 9))
    btn_defecto.pack(pady=6)

    ventana.mainloop()

if __name__ == "__main__":
    main()

#Copyright (c) - Erik Alejandro García Aparcio. 
