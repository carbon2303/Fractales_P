import tkinter as tk
from tkinter import ttk
import math

class GeneradorFractales:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Fractales - Python")
        self.root.geometry("1100x750")
        self.root.configure(bg="#111B28")

        self.fractal_actual = "SierpinskiTriangulo"
        self.color_fractal = "#5CC5DF" # Turquesa
        self.color_fondo = "#000000"   # Negro

        self.crear_interfaz()
        self.dibujar()

    def crear_interfaz(self):
        # Panel lateral izquierdo
        panel_izq = tk.Frame(self.root, bg="#111B28", width=280)
        panel_izq.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=15)

        tk.Label(panel_izq, text="Generador Fractales", font=("Segoe UI", 16, "bold"), fg="white", bg="#111B28").pack(anchor="w", pady=(0, 10))

        # Botones de selección de fractal
        tk.Label(panel_izq, text="Selecciona un Fractal:", font=("Segoe UI", 10, "bold"), fg="#87CEFA", bg="#111B28").pack(anchor="w", pady=5)
        
        btn_config = {"font": ("Segoe UI", 9), "fg": "white", "bg": "#273444", "activebackground": "#1F6FEB", "activeforeground": "white", "bd": 0, "height": 2}
        
        tk.Button(panel_izq, text="1. Triángulo Sierpinski", command=lambda: self.cambiar_fractal("SierpinskiTriangulo"), **btn_config).pack(fill=tk.X, pady=2)
        tk.Button(panel_izq, text="2. Alfombra Sierpinski", command=lambda: self.cambiar_fractal("SierpinskiAlfombra"), **btn_config).pack(fill=tk.X, pady=2)
        tk.Button(panel_izq, text="3. Copo de Koch", command=lambda: self.cambiar_fractal("CopoKoch"), **btn_config).pack(fill=tk.X, pady=2)
        tk.Button(panel_izq, text="4. Cruz de Vicsek", command=lambda: self.cambiar_fractal("Vicsek"), **btn_config).pack(fill=tk.X, pady=2)

        # Imagen / Miniatura de Referencia
        tk.Label(panel_izq, text="Imagen de Referencia:", font=("Segoe UI", 10, "bold"), fg="#87CEFA", bg="#111B28").pack(anchor="w", pady=(12, 2))
        self.canvas_ref = tk.Canvas(panel_izq, bg="#192332", width=240, height=130, highlightthickness=1, highlightbackground="#273444")
        self.canvas_ref.pack(pady=2)

        # Controles de parámetros
        tk.Label(panel_izq, text="Nivel de iteraciones (1 a 6):", fg="white", bg="#111B28").pack(anchor="w", pady=(12, 2))
        self.spn_iter = tk.Spinbox(panel_izq, from_=1, to=6, command=self.dibujar)
        self.spn_iter.delete(0, "end")
        self.spn_iter.insert(0, 4)
        self.spn_iter.pack(fill=tk.X, pady=2)

        tk.Label(panel_izq, text="Tamaño (200 a 800):", fg="white", bg="#111B28").pack(anchor="w", pady=(8, 2))
        self.spn_tam = tk.Spinbox(panel_izq, from_=200, to=800, increment=50, command=self.dibujar)
        self.spn_tam.delete(0, "end")
        self.spn_tam.insert(0, 500)
        self.spn_tam.pack(fill=tk.X, pady=2)

        # Selección de color
        tk.Label(panel_izq, text="Color del fractal:", fg="white", bg="#111B28").pack(anchor="w", pady=(8, 2))
        self.cmb_color = ttk.Combobox(panel_izq, values=["Turquesa", "Naranja", "Morado", "Verde", "Blanco"], state="readonly")
        self.cmb_color.current(0)
        self.cmb_color.bind("<<ComboboxSelected>>", self.actualizar_colores)
        self.cmb_color.pack(fill=tk.X, pady=2)

        # Lienzo principal de dibujo (Canvas)
        self.canvas = tk.Canvas(self.root, bg=self.color_fondo, highlightthickness=0)
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=15, pady=15)

    def cambiar_fractal(self, nombre):
        self.fractal_actual = nombre
        self.dibujar()

    def actualizar_colores(self, event=None):
        colores = {"Turquesa": "#5CC5DF", "Naranja": "#FF9132", "Morado": "#9370DB", "Verde": "#90EE90", "Blanco": "#FFFFFF"}
        self.color_fractal = colores.get(self.cmb_color.get(), "#FFFFFF")
        self.dibujar()

    def dibujar(self):
        self.canvas.delete("all")
        nivel = int(self.spn_iter.get())
        tamano = float(self.spn_tam.get())
        
        ancho = self.canvas.winfo_width() or 700
        alto = self.canvas.winfo_height() or 650

        # Dibujar fractal principal
        self.dibujar_fractal_en_canvas(self.canvas, ancho, alto, tamano, nivel, self.color_fractal)
        
        # Dibujar imagen de referencia (miniatura fija)
        self.dibujar_miniatura_referencia()

    def dibujar_miniatura_referencia(self):
        self.canvas_ref.delete("all")
        self.dibujar_fractal_en_canvas(self.canvas_ref, 240, 130, 100, 3, "#87CEFA")

    def dibujar_fractal_en_canvas(self, target_canvas, ancho, alto, tamano, nivel, color):
        if self.fractal_actual == "SierpinskiTriangulo":
            h = tamano * (math.sqrt(3) / 2)
            x, y = (ancho - tamano) / 2, (alto - h) / 2
            self.rec_sierpinski_triangulo(target_canvas, x + tamano/2, y, x, y + h, x + tamano, y + h, nivel, color)
        elif self.fractal_actual == "SierpinskiAlfombra":
            x, y = (ancho - tamano) / 2, (alto - tamano) / 2
            self.rec_sierpinski_alfombra(target_canvas, x, y, tamano, nivel, color)
        elif self.fractal_actual == "CopoKoch":
            h = tamano * (math.sqrt(3) / 2)
            x, y = (ancho - tamano) / 2, (alto - h) / 2 + h * 0.1
            p1, p2, p3 = (x + tamano/2, y), (x + tamano, y + h), (x, y + h)
            self.rec_koch(target_canvas, p1, p2, nivel, color)
            self.rec_koch(target_canvas, p2, p3, nivel, color)
            self.rec_koch(target_canvas, p3, p1, nivel, color)
        elif self.fractal_actual == "Vicsek":
            x, y = (ancho - tamano) / 2, (alto - tamano) / 2
            self.rec_vicsek(target_canvas, x, y, tamano, nivel, color)

    # --- ALGORITMOS RECURSIVOS ---

    def rec_sierpinski_triangulo(self, c, ax, ay, bx, by, cx, cy, n, col):
        if n == 0:
            c.create_polygon(ax, ay, bx, by, cx, cy, fill=col, outline=col)
            return
        abx, aby = (ax + bx) / 2, (ay + by) / 2
        acx, acy = (ax + cx) / 2, (ay + cy) / 2
        bcx, bcy = (bx + cx) / 2, (by + cy) / 2
        self.rec_sierpinski_triangulo(c, ax, ay, abx, aby, acx, acy, n - 1, col)
        self.rec_sierpinski_triangulo(c, abx, aby, bx, by, bcx, bcy, n - 1, col)
        self.rec_sierpinski_triangulo(c, acx, acy, bcx, bcy, cx, cy, n - 1, col)

    def rec_sierpinski_alfombra(self, c, x, y, tam, n, col):
        if n == 0:
            c.create_rectangle(x, y, x + tam, y + tam, fill=col, outline=col)
            return
        ntam = tam / 3.0
        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1: continue
                self.rec_sierpinski_alfombra(c, x + i * ntam, y + j * ntam, ntam, n - 1, col)

    def rec_koch(self, c, p1, p5, n, col):
        if n == 0:
            c.create_line(p1[0], p1[1], p5[0], p5[1], fill=col, width=1)
            return
        dx, dy = p5[0] - p1[0], p5[1] - p1[1]
        p2 = (p1[0] + dx / 3.0, p1[1] + dy / 3.0)
        p4 = (p1[0] + 2.0 * dx / 3.0, p1[1] + 2.0 * dy / 3.0)
        ang = math.atan2(dy, dx) - math.pi / 3.0
        dist = math.sqrt(dx**2 + dy**2) / 3.0
        p3 = (p2[0] + math.cos(ang) * dist, p2[1] + math.sin(ang) * dist)
        
        self.rec_koch(c, p1, p2, n - 1, col)
        self.rec_koch(c, p2, p3, n - 1, col)
        self.rec_koch(c, p3, p4, n - 1, col)
        self.rec_koch(c, p4, p5, n - 1, col)

    def rec_vicsek(self, c, x, y, tam, n, col):
        if n == 0:
            c.create_rectangle(x, y, x + tam, y + tam, fill=col, outline=col)
            return
        ntam = tam / 3.0
        self.rec_vicsek(c, x + ntam, y, ntam, n - 1, col)
        self.rec_vicsek(c, x, y + ntam, ntam, n - 1, col)
        self.rec_vicsek(c, x + ntam, y + ntam, ntam, n - 1, col)
        self.rec_vicsek(c, x + 2 * ntam, y + ntam, ntam, n - 1, col)
        self.rec_vicsek(c, x + ntam, y + 2 * ntam, ntam, n - 1, col)

if __name__ == "__main__":
    root = tk.Tk()
    app = GeneradorFractales(root)
    root.mainloop()