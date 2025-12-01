import tkinter as tk
from tkinter import ttk, colorchooser
from PIL import Image, ImageDraw, ImageTk

COLORES = {
    "base": "#1e1e2e",
    "mantle": "#181825",
    "surface0": "#313244",
    "surface1": "#45475a",
    "texto": "#cdd6f4",
    "lienzo": "#ffffff",
    "lavanda": "#b4befe",
    "rojo": "#f38ba8",
    "verde": "#a6e3a1"
}

COLORES_RAPIDOS = [
    "#11111b", "#f38ba8", "#fab387", "#f9e2af", 
    "#a6e3a1", "#94e2d5", "#89b4fa", "#cba6f7", 
    "#f5c2e7", "#f2cdcd"
]

class PaintCatppuccin:
    def __init__(self, root):
        self.root = root
        self.root.title("ARAX-PAINT")
        self.root.geometry("1000x700")
        self.root.configure(bg=COLORES["base"])

        self.color_pincel = "#11111b"
        self.tamano_pincel = 5
        self.herramienta_actual = "pincel"
        self.old_x = None
        self.old_y = None

        self.ancho = 1200
        self.alto = 900
        self.imagen = Image.new("RGB", (self.ancho, self.alto), "white")
        self.dibujo_img = ImageDraw.Draw(self.imagen)
        
        self._configurar_interfaz()

    def _configurar_interfaz(self):
        barra_lateral = tk.Frame(self.root, bg=COLORES["mantle"], width=220, padx=15, pady=15)
        barra_lateral.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(barra_lateral, text="by: Ars-byte :B", bg=COLORES["mantle"], fg=COLORES["texto"], 
                 font=("Segoe UI", 14, "bold")).pack(pady=(0, 20))

        lbl_herramientas = tk.Label(barra_lateral, text="Herramientas", bg=COLORES["mantle"], fg=COLORES["surface1"], font=("Segoe UI", 10, "bold"))
        lbl_herramientas.pack(anchor="w", pady=(0, 5))

        self.btn_pincel = self._crear_boton_herramienta(barra_lateral, "🖌 Pincel", "pincel")
        self.btn_cubo = self._crear_boton_herramienta(barra_lateral, "🪣 Relleno", "cubo")
        self.btn_borrador = self._crear_boton_herramienta(barra_lateral, "🧼 Borrador", "borrador")
        
        self._actualizar_botones_herramientas()

        tk.Frame(barra_lateral, bg=COLORES["surface0"], height=2).pack(fill=tk.X, pady=20)

        tk.Label(barra_lateral, text="Colores", bg=COLORES["mantle"], fg=COLORES["surface1"], font=("Segoe UI", 10, "bold")).pack(anchor="w")
        
        frame_colores = tk.Frame(barra_lateral, bg=COLORES["mantle"])
        frame_colores.pack(pady=10)

        r, c = 0, 0
        for color in COLORES_RAPIDOS:
            btn = tk.Button(frame_colores, bg=color, activebackground=color, width=3, relief=tk.FLAT, bd=0,
                            command=lambda x=color: self.cambiar_color(x))
            btn.grid(row=r, column=c, padx=2, pady=2)
            c += 1
            if c > 1: c=0; r+=1

        btn_rgb = tk.Button(barra_lateral, text="🎨 Selector RGB", bg=COLORES["surface0"], fg=COLORES["texto"],
                            relief=tk.FLAT, bd=0, pady=5, command=self.abrir_selector_color)
        btn_rgb.pack(fill=tk.X, pady=5)
        
        self.lbl_color_actual = tk.Label(barra_lateral, text="   ", bg=self.color_pincel, relief=tk.FLAT)
        self.lbl_color_actual.pack(fill=tk.X, pady=(5,0), padx=40)

        tk.Frame(barra_lateral, bg=COLORES["surface0"], height=2).pack(fill=tk.X, pady=20)

        tk.Label(barra_lateral, text="Tamaño", bg=COLORES["mantle"], fg=COLORES["surface1"], font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.slider = tk.Scale(barra_lateral, from_=1, to=50, orient=tk.HORIZONTAL, 
                               bg=COLORES["mantle"], fg=COLORES["texto"], troughcolor=COLORES["surface0"],
                               highlightthickness=0, activebackground=COLORES["lavanda"], 
                               command=self.cambiar_tamano)
        self.slider.set(self.tamano_pincel)
        self.slider.pack(fill=tk.X, pady=5)

        tk.Button(barra_lateral, text="🗑 Limpiar Todo", bg=COLORES["rojo"], fg=COLORES["mantle"],
                  relief=tk.FLAT, bd=0, pady=8, font=("Segoe UI", 10, "bold"),
                  command=self.limpiar_lienzo).pack(side=tk.BOTTOM, fill=tk.X)

        contenedor_canvas = tk.Frame(self.root, bg=COLORES["base"], padx=10, pady=10)
        contenedor_canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.lienzo = tk.Canvas(contenedor_canvas, bg=COLORES["lienzo"], highlightthickness=0)
        self.lienzo.pack(fill=tk.BOTH, expand=True)

        self.lienzo.bind('<Button-1>', self.al_clic)
        self.lienzo.bind('<B1-Motion>', self.al_dibujar)
        self.lienzo.bind('<ButtonRelease-1>', self.al_soltar)

    def _crear_boton_herramienta(self, padre, texto, modo):
        btn = tk.Button(padre, text=texto, bg=COLORES["surface0"], fg=COLORES["texto"],
                        relief=tk.FLAT, bd=0, pady=5, anchor="w", padx=10,
                        command=lambda: self.seleccionar_herramienta(modo))
        btn.pack(fill=tk.X, pady=2)
        return btn

    def seleccionar_herramienta(self, herramienta):
        self.herramienta_actual = herramienta
        self._actualizar_botones_herramientas()

    def _actualizar_botones_herramientas(self):
        bg_defecto = COLORES["surface0"]
        bg_activo = COLORES["lavanda"]
        fg_activo = COLORES["base"]
        
        botones = {
            "pincel": self.btn_pincel,
            "cubo": self.btn_cubo,
            "borrador": self.btn_borrador
        }
        
        for modo, btn in botones.items():
            if modo == self.herramienta_actual:
                btn.config(bg=bg_activo, fg=fg_activo)
            else:
                btn.config(bg=bg_defecto, fg=COLORES["texto"])

    def al_clic(self, evento):
        x, y = evento.x, evento.y

        if self.herramienta_actual == "cubo":
            self.rellenar_color(x, y)
        else:
            self.old_x = x
            self.old_y = y
            self.dibujar_linea(x, y, x, y)

    def al_dibujar(self, evento):
        if self.herramienta_actual == "cubo":
            return
        
        self.dibujar_linea(evento.x, evento.y)
        self.old_x = evento.x
        self.old_y = evento.y

    def al_soltar(self, evento):
        self.old_x = None
        self.old_y = None

    def dibujar_linea(self, x, y, inicio_x=None, inicio_y=None):
        if inicio_x is None: inicio_x = self.old_x
        if inicio_y is None: inicio_y = self.old_y

        color = self.color_pincel
        if self.herramienta_actual == "borrador":
            color = "#ffffff"
        
        self.lienzo.create_line(inicio_x, inicio_y, x, y, 
                                width=self.tamano_pincel, fill=color, 
                                capstyle=tk.ROUND, smooth=True)
        
        self.dibujo_img.line([inicio_x, inicio_y, x, y], fill=color, width=self.tamano_pincel, joint="curve")

    def rellenar_color(self, x, y):
        try:
            color_objetivo = self.imagen.getpixel((x, y))
            color_relleno_rgb = self.hex_a_rgb(self.color_pincel)
            
            ImageDraw.floodfill(self.imagen, (x, y), color_relleno_rgb, thresh=50)
            
            self.img_tk = ImageTk.PhotoImage(self.imagen)
            self.lienzo.create_image(0, 0, image=self.img_tk, anchor="nw")
            
        except Exception as e:
            print(f"Error: {e}")

    def abrir_selector_color(self):
        codigo_color = colorchooser.askcolor(title="Selecciona un color")[1]
        if codigo_color:
            self.cambiar_color(codigo_color)

    def cambiar_color(self, color):
        self.color_pincel = color
        self.lbl_color_actual.config(bg=color)
        if self.herramienta_actual == "borrador":
            self.seleccionar_herramienta("pincel")

    def cambiar_tamano(self, val):
        self.tamano_pincel = int(val)

    def limpiar_lienzo(self):
        self.lienzo.delete("all")
        self.imagen = Image.new("RGB", (self.ancho, self.alto), "white")
        self.dibujo_img = ImageDraw.Draw(self.imagen)

    def hex_a_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

if __name__ == "__main__":
    raiz = tk.Tk()
    app = PaintCatppuccin(raiz)
    raiz.mainloop()