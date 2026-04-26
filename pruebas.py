"""
SISTEMA DE GESTIÓN DE PERMISOS — GUI
Interfaz gráfica profesional sobre la misma lógica de negocio original.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Any, Callable

# ============================================================
# CONSTANTES (sin cambios)
# ============================================================
HORAS_POR_DIA   = 8
DIAS_POR_MES    = 30
HORAS_POR_MES   = HORAS_POR_DIA * DIAS_POR_MES
FORMATO_FECHA   = "%Y-%m-%d"

# ============================================================
# CLASE ABSTRACTA — sin cambios
# ============================================================
class Validable(ABC):
    @abstractmethod
    def validar(self) -> bool:
        pass

# ============================================================
# MIXIN — sin cambios
# ============================================================
class EstadisticasMixin:
    def total_empleados(self) -> int:
        return len(self.empleados)
    def total_permisos(self) -> int:
        return len(self.permisos)
    def permisos_remunerados(self) -> int:
        return sum(1 for p in self.permisos if p.es_remunerado)
    def permisos_no_remunerados(self) -> int:
        return len(self.permisos) - self.permisos_remunerados()
    def total_tiempo_solicitado(self) -> float:
        return sum(p.tiempo for p in self.permisos)
    def total_descuentos(self) -> float:
        return sum(p.calcular_descuento() for p in self.permisos)

# ============================================================
# HOF — sin cambios
# ============================================================
def aplicar_a_lista(func: Callable, lista: List[Any]) -> List[Any]:
    return [func(e) for e in lista]

def filtrar_por(condicion: Callable, lista: List[Any]) -> List[Any]:
    return list(filter(condicion, lista))

def crear_validador_rango(min_val: float, max_val: float) -> Callable:
    def validador(valor: float) -> bool:
        return min_val <= valor <= max_val
    return validador

# ============================================================
# ENTIDADES — sin cambios
# ============================================================
class Empleado(Validable):
    _contador_id = 1
    def __init__(self, nombre: str, sueldo: float):
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre no puede estar vacío.")
        if sueldo <= 0:
            raise ValueError("El sueldo debe ser mayor a 0.")
        self.id = Empleado._contador_id
        Empleado._contador_id += 1
        self.nombre     = nombre.strip().title()
        self.sueldo     = sueldo
        self.valor_hora = sueldo / HORAS_POR_MES
    def validar(self) -> bool:
        return bool(self.nombre) and self.sueldo > 0
    def __str__(self) -> str:
        return f"ID:{self.id} | {self.nombre} | ${self.sueldo:,.2f} | Hora:${self.valor_hora:.2f}"

class TipoPermiso(Validable):
    _contador_id = 1
    def __init__(self, descripcion: str, remunerado: str):
        if not descripcion:
            raise ValueError("La descripción no puede estar vacía.")
        remunerado = remunerado.upper()
        if remunerado not in ['S', 'N']:
            raise ValueError("El campo remunerado debe ser S o N.")
        self.id          = TipoPermiso._contador_id
        TipoPermiso._contador_id += 1
        self.descripcion = descripcion.strip().capitalize()
        self.remunerado  = remunerado
    @property
    def es_remunerado(self) -> bool:
        return self.remunerado == 'S'
    def validar(self) -> bool:
        return bool(self.descripcion) and self.remunerado in ['S', 'N']
    def __str__(self) -> str:
        return f"ID:{self.id} | {self.descripcion} | {'Remunerado' if self.es_remunerado else 'No remunerado'}"

class Permiso(Validable):
    _contador_id = 1
    def __init__(self, id_emp: int, id_tipo: int, fd: str, fh: str, tipo: str, tiempo: float):
        if id_emp <= 0 or id_tipo <= 0 or tiempo <= 0:
            raise ValueError("IDs o tiempo inválidos.")
        tipo = tipo.upper()
        if tipo not in ['D', 'H']:
            raise ValueError("El tipo debe ser D (días) o H (horas).")
        self.id               = Permiso._contador_id
        Permiso._contador_id += 1
        self.id_empleado      = id_emp
        self.id_tipo_permiso  = id_tipo
        self.fecha_desde      = fd
        self.fecha_hasta      = fh
        self.tipo             = tipo
        self.tiempo           = tiempo
        self._sistema         = None
    def set_sistema(self, sistema):
        self._sistema = sistema
    @property
    def es_remunerado(self) -> bool:
        if self._sistema:
            tp = self._sistema.buscar_tipo_permiso(self.id_tipo_permiso)
            return tp.es_remunerado if tp else False
        return False
    def calcular_descuento(self) -> float:
        if self.es_remunerado:
            return 0.0
        if not self._sistema:
            return 0.0
        emp = self._sistema.buscar_empleado(self.id_empleado)
        if not emp:
            return 0.0
        if self.tipo == 'H':
            return self.tiempo * emp.valor_hora
        else:
            return self.tiempo * HORAS_POR_DIA * emp.valor_hora
    def validar(self) -> bool:
        try:
            desde = datetime.strptime(self.fecha_desde, FORMATO_FECHA)
            hasta = datetime.strptime(self.fecha_hasta, FORMATO_FECHA)
            if desde > hasta:
                return False
        except:
            return False
        return True

# ============================================================
# SISTEMA PRINCIPAL — sin cambios
# ============================================================
class SistemaPermisos(EstadisticasMixin):
    def __init__(self):
        self.empleados     = []
        self.tipos_permiso = []
        self.permisos      = []

    def crear_empleado(self, nombre, sueldo):
        e = Empleado(nombre, sueldo)
        self.empleados.append(e)
        return e
    def consultar_empleado(self, id_):
        for e in self.empleados:
            if e.id == id_: return e
        return None
    def eliminar_empleado(self, id_):
        for i, e in enumerate(self.empleados):
            if e.id == id_:
                self.empleados.pop(i); return True
        return False
    def listar_empleados(self):
        return self.empleados.copy()

    def crear_tipo_permiso(self, desc, rem):
        tp = TipoPermiso(desc, rem)
        self.tipos_permiso.append(tp)
        return tp
    def consultar_tipo_permiso(self, id_):
        for tp in self.tipos_permiso:
            if tp.id == id_: return tp
        return None
    def eliminar_tipo_permiso(self, id_):
        for i, tp in enumerate(self.tipos_permiso):
            if tp.id == id_:
                self.tipos_permiso.pop(i); return True
        return False
    def listar_tipos_permiso(self):
        return self.tipos_permiso.copy()

    def crear_permiso(self, id_emp, id_tp, fd, fh, tipo, tiempo):
        if not self.consultar_empleado(id_emp):
            raise ValueError("El empleado seleccionado no existe.")
        if not self.consultar_tipo_permiso(id_tp):
            raise ValueError("El tipo de permiso seleccionado no existe.")
        p = Permiso(id_emp, id_tp, fd, fh, tipo, tiempo)
        p.set_sistema(self)
        self.permisos.append(p)
        return p
    def consultar_permiso(self, id_):
        for p in self.permisos:
            if p.id == id_: return p
        return None
    def eliminar_permiso(self, id_):
        for i, p in enumerate(self.permisos):
            if p.id == id_:
                self.permisos.pop(i); return True
        return False
    def listar_permisos(self):
        return self.permisos.copy()

    def buscar_empleado(self, id_):
        return self.consultar_empleado(id_)
    def buscar_tipo_permiso(self, id_):
        return self.consultar_tipo_permiso(id_)

    def obtener_estadisticas(self):
        aplicar_a_lista(lambda p: p.calcular_descuento(), self.permisos)
        return {
            "total_empleados":        self.total_empleados(),
            "total_permisos":         self.total_permisos(),
            "permisos_remunerados":   self.permisos_remunerados(),
            "permisos_no_remunerados":self.permisos_no_remunerados(),
            "total_tiempo":           self.total_tiempo_solicitado(),
            "total_descuentos":       self.total_descuentos(),
        }


# ╔══════════════════════════════════════════════════════════╗
# ║                   CAPA DE INTERFAZ GUI                   ║
# ╚══════════════════════════════════════════════════════════╝

# ── Paleta de colores ──────────────────────────────────────
C = {
    "nav_bg":       "#0F1923",
    "nav_hover":    "#1A2B3C",
    "nav_active":   "#1E3A5F",
    "nav_accent":   "#2563EB",
    "canvas_bg":    "#F1F5F9",
    "card_bg":      "#FFFFFF",
    "border":       "#E2E8F0",
    "text_h":       "#0F172A",
    "text_body":    "#334155",
    "text_muted":   "#94A3B8",
    "text_nav":     "#94A3B8",
    "text_nav_on":  "#F8FAFC",
    "blue":         "#2563EB",
    "blue_h":       "#1D4ED8",
    "green":        "#16A34A",
    "red":          "#DC2626",
    "amber":        "#D97706",
    "violet":       "#7C3AED",
    "teal":         "#0D9488",
    "input_bg":     "#F8FAFC",
    "tag_green_bg": "#AEC8B7",
    "tag_green_fg": "#15803D",
    "tag_red_bg":   "#FEE2E2",
    "tag_red_fg":   "#B91C1C",
}

F = {
    "brand":   ("Segoe UI", 13, "bold"),
    "h1":      ("Segoe UI", 20, "bold"),
    "h2":      ("Segoe UI", 14, "bold"),
    "h3":      ("Segoe UI", 11, "bold"),
    "body":    ("Segoe UI", 10),
    "small":   ("Segoe UI", 9),
    "micro":   ("Segoe UI", 8),
    "nav":     ("Segoe UI", 10),
    "nav_b":   ("Segoe UI", 10, "bold"),
    "stat":    ("Segoe UI", 24, "bold"),
    "mono":    ("Consolas", 10),
}


# ── Componentes reutilizables ──────────────────────────────

class NavButton(tk.Frame):
    """Botón de navegación lateral con ícono + texto."""
    def __init__(self, parent, icon, label, key, on_click):
        super().__init__(parent, bg=C["nav_bg"], cursor="hand2")
        self.key       = key
        self._active   = False
        self._on_click = on_click

        self._pill = tk.Frame(self, bg=C["nav_bg"], width=4)
        self._pill.pack(side="left", fill="y")

        self._inner = tk.Frame(self, bg=C["nav_bg"], padx=14, pady=11)
        self._inner.pack(side="left", fill="x", expand=True)

        self._icon = tk.Label(self._inner, text=icon, font=("Segoe UI", 13),
                              bg=C["nav_bg"], fg=C["text_nav"])
        self._icon.pack(side="left", padx=(0, 10))

        self._lbl = tk.Label(self._inner, text=label, font=F["nav"],
                             bg=C["nav_bg"], fg=C["text_nav"])
        self._lbl.pack(side="left")

        for w in (self, self._inner, self._icon, self._lbl, self._pill):
            w.bind("<Button-1>", lambda e, k=key: self._on_click(k))
            w.bind("<Enter>",    self._hover_on)
            w.bind("<Leave>",    self._hover_off)

    def _hover_on(self, _=None):
        if not self._active:
            for w in (self, self._inner, self._icon, self._lbl):
                w.config(bg=C["nav_hover"])
            self._pill.config(bg=C["nav_hover"])

    def _hover_off(self, _=None):
        if not self._active:
            for w in (self, self._inner, self._icon, self._lbl):
                w.config(bg=C["nav_bg"])
            self._pill.config(bg=C["nav_bg"])

    def activate(self):
        self._active = True
        for w in (self, self._inner, self._icon, self._lbl):
            w.config(bg=C["nav_active"])
        self._pill.config(bg=C["nav_accent"])
        self._icon.config(fg=C["text_nav_on"])
        self._lbl.config(fg=C["text_nav_on"], font=F["nav_b"])

    def deactivate(self):
        self._active = False
        for w in (self, self._inner, self._icon, self._lbl):
            w.config(bg=C["nav_bg"])
        self._pill.config(bg=C["nav_bg"])
        self._icon.config(fg=C["text_nav"])
        self._lbl.config(fg=C["text_nav"], font=F["nav"])


class Btn(tk.Frame):
    """Botón plano con estilo y hover."""
    _STYLES = {
        "primary": (C["blue"],   "#FFFFFF", C["blue_h"]),
        "danger":  (C["red"],    "#FFFFFF", "#B91C1C"),
        "success": (C["green"],  "#FFFFFF", "#15803D"),
        "ghost":   (C["border"], C["text_body"], "#CBD5E1"),
    }
    def __init__(self, parent, text, cmd=None, style="primary", padx=18, pady=7, **kw):
        bg_p = parent.cget("bg") if isinstance(parent, (tk.Frame, tk.LabelFrame)) else C["canvas_bg"]
        super().__init__(parent, bg=bg_p)
        bg, fg, hov = self._STYLES.get(style, self._STYLES["primary"])
        self._bg, self._hov = bg, hov
        self._btn = tk.Button(self, text=text, bg=bg, fg=fg, relief="flat",
                              font=F["h3"], cursor="hand2",
                              padx=padx, pady=pady, bd=0,
                              activebackground=hov, activeforeground=fg,
                              command=cmd)
        self._btn.pack(fill="both", expand=True)
        self._btn.bind("<Enter>", lambda _: self._btn.config(bg=hov))
        self._btn.bind("<Leave>", lambda _: self._btn.config(bg=bg))

    def config(self, **kw):
        if "command" in kw:
            self._btn.config(command=kw.pop("command"))
        if kw: self._btn.config(**kw)


class Field(tk.Frame):
    """Campo de entrada con etiqueta flotante."""
    def __init__(self, parent, label: str, numeric=False, **kw):
        super().__init__(parent, bg=C["card_bg"])
        self._numeric = numeric

        tk.Label(self, text=label, font=F["small"], bg=C["card_bg"],
                 fg=C["text_muted"]).pack(anchor="w")

        self.var   = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.var, font=F["body"],
                              bg=C["input_bg"], fg=C["text_h"],
                              relief="flat", bd=0,
                              insertbackground=C["blue"])
        self.entry.pack(fill="x", ipady=7, padx=1)

        self._line       = tk.Frame(self, bg=C["border"], height=1)
        self._focus_line = tk.Frame(self, bg=C["blue"],   height=2)
        self._line.pack(fill="x")

        self.entry.bind("<FocusIn>",  self._on_focus)
        self.entry.bind("<FocusOut>", self._on_blur)

    def _on_focus(self, _):
        self._line.pack_forget()
        self._focus_line.pack(fill="x")

    def _on_blur(self, _):
        self._focus_line.pack_forget()
        self._line.pack(fill="x")

    def get(self) -> str:
        return self.var.get().strip()

    def set(self, v: str):
        self.var.set(v)

    def clear(self):
        self.var.set("")


class Table(tk.Frame):
    """Treeview estilizado con zebra-striping y scrollbars."""
    def __init__(self, parent, columns: tuple, col_widths: tuple = None):
        super().__init__(parent, bg=C["card_bg"])

        style = ttk.Style()
        uid   = f"T{id(self)}"
        style.configure(f"{uid}.Treeview",
            background=C["card_bg"], foreground=C["text_body"],
            fieldbackground=C["card_bg"], font=F["body"], rowheight=38, borderwidth=0)
        style.configure(f"{uid}.Treeview.Heading",
            background=C["canvas_bg"], foreground=C["text_muted"],
            font=F["h3"], relief="flat", borderwidth=0)
        style.map(f"{uid}.Treeview",
            background=[("selected", C["blue"])],
            foreground=[("selected", "#FFFFFF")])
        style.layout(f"{uid}.Treeview",
            [("Treeview.treearea", {"sticky": "nswe"})])

        vsb = ttk.Scrollbar(self, orient="vertical")
        hsb = ttk.Scrollbar(self, orient="horizontal")

        self.tv = ttk.Treeview(self, columns=columns, show="headings",
                               style=f"{uid}.Treeview",
                               yscrollcommand=vsb.set,
                               xscrollcommand=hsb.set)
        vsb.config(command=self.tv.yview)
        hsb.config(command=self.tv.xview)

        for i, col in enumerate(columns):
            w = (col_widths[i] if col_widths and i < len(col_widths) else 120)
            self.tv.heading(col, text=col)
            self.tv.column(col, width=w, minwidth=60, anchor="w")

        self.tv.tag_configure("odd",  background="#F8FAFC")
        self.tv.tag_configure("even", background=C["card_bg"])
        self.tv.tag_configure("rem",  foreground=C["green"])
        self.tv.tag_configure("norem",foreground=C["red"])

        self.tv.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def clear(self):
        self.tv.delete(*self.tv.get_children())

    def add(self, values, tags=()):
        n   = len(self.tv.get_children())
        row = ("odd",) if n % 2 == 0 else ("even",)
        self.tv.insert("", "end", values=values, tags=row + tags)

    def selected_id(self):
        sel = self.tv.selection()
        if sel:
            return self.tv.item(sel[0])["values"][0]
        return None


class StatCard(tk.Frame):
    """Tarjeta de KPI con ícono, valor y etiqueta."""
    def __init__(self, parent, icon, title, value, color):
        super().__init__(parent, bg=C["card_bg"],
                         highlightbackground=C["border"], highlightthickness=1)
        tk.Frame(self, bg=color, height=3).pack(fill="x")
        body = tk.Frame(self, bg=C["card_bg"], padx=20, pady=16)
        body.pack(fill="both", expand=True)

        top = tk.Frame(body, bg=C["card_bg"])
        top.pack(fill="x", pady=(0, 8))

        tk.Label(top, text=icon, font=("Segoe UI", 18), bg=C["card_bg"],
                 fg=color).pack(side="left")
        self._val = tk.Label(body, text=str(value), font=F["stat"],
                             bg=C["card_bg"], fg=color)
        self._val.pack(anchor="w")
        tk.Label(body, text=title, font=F["small"], bg=C["card_bg"],
                 fg=C["text_muted"]).pack(anchor="w")

    def update(self, v):
        self._val.config(text=str(v))


class SectionHeader(tk.Frame):
    """Encabezado de sección con título y botón opcional."""
    def __init__(self, parent, title: str, subtitle: str = "", btn_text: str = "", btn_cmd=None):
        super().__init__(parent, bg=C["canvas_bg"])
        left = tk.Frame(self, bg=C["canvas_bg"])
        left.pack(side="left", fill="y")
        tk.Label(left, text=title, font=F["h1"], bg=C["canvas_bg"],
                 fg=C["text_h"]).pack(anchor="w")
        if subtitle:
            tk.Label(left, text=subtitle, font=F["small"], bg=C["canvas_bg"],
                     fg=C["text_muted"]).pack(anchor="w")
        if btn_text and btn_cmd:
            Btn(self, btn_text, btn_cmd).pack(side="right", anchor="center")


class FormPanel(tk.Frame):
    """Panel lateral deslizante para formularios."""
    def __init__(self, parent, title: str, width=310):
        super().__init__(parent, bg=C["card_bg"], width=width,
                         highlightbackground=C["border"], highlightthickness=1)
        self.pack_propagate(False)
        self._visible = False

        # Título + botón cerrar
        hdr = tk.Frame(self, bg=C["nav_accent"], padx=20, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text=title, font=F["h2"], bg=C["nav_accent"],
                 fg="#FFFFFF").pack(side="left")

        self.body = tk.Frame(self, bg=C["card_bg"])
        self.body.pack(fill="both", expand=True, padx=20, pady=16)

    def show(self):
        if not self._visible:
            self.pack(side="right", fill="y", padx=(10, 0))
            self._visible = True

    def hide(self):
        if self._visible:
            self.pack_forget()
            self._visible = False

    def toggle(self):
        self.hide() if self._visible else self.show()


# ── Vistas ──────────────────────────────────────────────────

class BaseView(tk.Frame):
    def __init__(self, parent, sistema: SistemaPermisos):
        super().__init__(parent, bg=C["canvas_bg"])
        self.sistema = sistema
        self._build()
        self.refresh()

    def _build(self): pass
    def refresh(self): pass



class EmpleadosView(BaseView):
    def _build(self):
        wrap = tk.Frame(self, bg=C["canvas_bg"])
        wrap.pack(fill="both", expand=True, padx=32, pady=28)

        SectionHeader(wrap, "Empleados", "Gestión del personal registrado",
                      "＋  Nuevo empleado", self._open_form).pack(fill="x", pady=(0, 20))

        row = tk.Frame(wrap, bg=C["canvas_bg"])
        row.pack(fill="both", expand=True)

        # Tabla
        card = tk.Frame(row, bg=C["card_bg"],
                        highlightbackground=C["border"], highlightthickness=1)
        card.pack(side="left", fill="both", expand=True)

        cols   = ("ID", "Nombre", "Sueldo mensual", "Valor por hora")
        widths = (50,   220,      150,               150)
        self._table = Table(card, cols, widths)
        self._table.pack(fill="both", expand=True, padx=1, pady=1)

        foot = tk.Frame(card, bg=C["card_bg"], pady=10, padx=14)
        foot.pack(fill="x")
        tk.Label(foot, text="Seleccione una fila para eliminar",
                 font=F["small"], bg=C["card_bg"], fg=C["text_muted"]).pack(side="left")
        Btn(foot, "🗑  Eliminar", self._eliminar, style="danger").pack(side="right", padx=4)

        # Panel formulario
        self._panel = FormPanel(row, "Nuevo Empleado")
        self._build_form(self._panel.body)

    def _build_form(self, body):
        tk.Label(body, text="ID — generado automáticamente", font=F["small"],
                 bg=C["card_bg"], fg=C["text_muted"]).pack(anchor="w", pady=(0, 12))

        self._f_nombre = Field(body, "Nombre completo")
        self._f_nombre.pack(fill="x", pady=6)

        self._f_sueldo = Field(body, "Sueldo mensual ($)", numeric=True)
        self._f_sueldo.pack(fill="x", pady=6)

        # Preview valor/hora
        prev = tk.Frame(body, bg="#EFF6FF", pady=10, padx=12)
        prev.pack(fill="x", pady=10)
        tk.Label(prev, text="Valor estimado por hora", font=F["small"],
                 bg="#EFF6FF", fg=C["blue"]).pack(anchor="w")
        self._lbl_vh = tk.Label(prev, text="$ 0.00", font=("Segoe UI", 16, "bold"),
                                bg="#EFF6FF", fg=C["blue"])
        self._lbl_vh.pack(anchor="w")
        self._f_sueldo.var.trace("w", self._calc_vh)

        sep = tk.Frame(body, bg=C["border"], height=1)
        sep.pack(fill="x", pady=12)

        btns = tk.Frame(body, bg=C["card_bg"])
        btns.pack(fill="x")
        Btn(btns, "Guardar",   self._guardar,           style="primary").pack(side="left", padx=(0, 8))
        Btn(btns, "Cancelar",  self._panel.hide,         style="ghost").pack(side="left")

    def _calc_vh(self, *_):
        try:
            v = float(self._f_sueldo.get())
            self._lbl_vh.config(text=f"$ {v / HORAS_POR_MES:.2f}")
        except:
            self._lbl_vh.config(text="$ 0.00")

    def _open_form(self):
        self._f_nombre.clear()
        self._f_sueldo.clear()
        self._lbl_vh.config(text="$ 0.00")
        self._panel.show()

    def _guardar(self):
        nombre = self._f_nombre.get()
        if not nombre:
            messagebox.showwarning("Campo requerido", "Ingrese el nombre del empleado.")
            return
        try:
            sueldo = float(self._f_sueldo.get())
            if sueldo <= 0: raise ValueError()
        except:
            messagebox.showwarning("Campo inválido", "Ingrese un sueldo válido mayor a 0.")
            return
        try:
            emp = self.sistema.crear_empleado(nombre, sueldo)
            messagebox.showinfo("Empleado registrado",
                                f"'{emp.nombre}' fue registrado con ID {emp.id}.")
            self._panel.hide()
            self.refresh()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def _eliminar(self):
        id_ = self._table.selected_id()
        if id_ is None:
            messagebox.showwarning("Sin selección", "Seleccione un empleado de la tabla.")
            return
        emp = self.sistema.consultar_empleado(int(id_))
        nombre = emp.nombre if emp else f"ID {id_}"
        if messagebox.askyesno("Confirmar eliminación",
                               f"¿Eliminar a '{nombre}'? Esta acción no se puede deshacer."):
            if self.sistema.eliminar_empleado(int(id_)):
                messagebox.showinfo("Eliminado", f"'{nombre}' fue eliminado.")
                self.refresh()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el empleado.")

    def refresh(self):
        self._table.clear()
        for e in self.sistema.listar_empleados():
            self._table.add((e.id, e.nombre, f"${e.sueldo:,.2f}", f"${e.valor_hora:.2f}"))


class TiposPermisoView(BaseView):
    def _build(self):
        wrap = tk.Frame(self, bg=C["canvas_bg"])
        wrap.pack(fill="both", expand=True, padx=32, pady=28)

        SectionHeader(wrap, "Tipos de Permiso", "Catálogo de tipos disponibles",
                      "＋  Nuevo tipo", self._open_form).pack(fill="x", pady=(0, 20))

        row = tk.Frame(wrap, bg=C["canvas_bg"])
        row.pack(fill="both", expand=True)

        card = tk.Frame(row, bg=C["card_bg"],
                        highlightbackground=C["border"], highlightthickness=1)
        card.pack(side="left", fill="both", expand=True)

        cols   = ("ID", "Descripción", "Clasificación")
        widths = (50,   300,            160)
        self._table = Table(card, cols, widths)
        self._table.pack(fill="both", expand=True, padx=1, pady=1)

        foot = tk.Frame(card, bg=C["card_bg"], pady=10, padx=14)
        foot.pack(fill="x")
        tk.Label(foot, text="Seleccione una fila para eliminar",
                 font=F["small"], bg=C["card_bg"], fg=C["text_muted"]).pack(side="left")
        Btn(foot, "🗑  Eliminar", self._eliminar, style="danger").pack(side="right", padx=4)

        self._panel = FormPanel(row, "Nuevo Tipo de Permiso")
        self._build_form(self._panel.body)

    def _build_form(self, body):
        self._f_desc = Field(body, "Descripción del permiso")
        self._f_desc.pack(fill="x", pady=(0, 14))

        tk.Label(body, text="¿Se remunerará al empleado?", font=F["h3"],
                 bg=C["card_bg"], fg=C["text_body"]).pack(anchor="w", pady=(0, 8))

        self._rem_var = tk.StringVar(value="S")

        for ico, lbl, val, bg_c, fg_c in [
            ("✅", " Sí, remunerado  (sin descuento)",   "S", C["tag_green_bg"], C["tag_green_fg"]),
            ("❌", " No remunerado  (genera descuento)", "N", C["tag_red_bg"],   C["tag_red_fg"]),
        ]:
            rb_frame = tk.Frame(body, bg=bg_c, pady=8, padx=12, cursor="hand2")
            rb_frame.pack(fill="x", pady=4)

            tk.Label(rb_frame, text=ico, font=("Segoe UI", 14),
                     bg=bg_c, fg=fg_c).pack(side="left")
            tk.Radiobutton(rb_frame, text=lbl, variable=self._rem_var, value=val,
                           bg=bg_c, fg=fg_c, selectcolor=bg_c, font=F["body"],
                           activebackground=bg_c, cursor="hand2",
                           relief="flat", bd=0).pack(side="left")

        sep = tk.Frame(body, bg=C["border"], height=1)
        sep.pack(fill="x", pady=14)

        btns = tk.Frame(body, bg=C["card_bg"])
        btns.pack(fill="x")
        Btn(btns, "Guardar",  self._guardar,   style="primary").pack(side="left", padx=(0, 8))
        Btn(btns, "Cancelar", self._panel.hide, style="ghost").pack(side="left")

    def _open_form(self):
        self._f_desc.clear()
        self._rem_var.set("S")
        self._panel.show()

    def _guardar(self):
        desc = self._f_desc.get()
        if not desc:
            messagebox.showwarning("Campo requerido", "Ingrese la descripción del tipo.")
            return
        try:
            tp = self.sistema.crear_tipo_permiso(desc, self._rem_var.get())
            messagebox.showinfo("Tipo registrado",
                                f"'{tp.descripcion}' fue registrado con ID {tp.id}.")
            self._panel.hide()
            self.refresh()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def _eliminar(self):
        id_ = self._table.selected_id()
        if id_ is None:
            messagebox.showwarning("Sin selección", "Seleccione un tipo de permiso.")
            return
        if messagebox.askyesno("Confirmar", f"¿Eliminar tipo de permiso ID {id_}?"):
            if self.sistema.eliminar_tipo_permiso(int(id_)):
                messagebox.showinfo("Eliminado", "Tipo de permiso eliminado.")
                self.refresh()

    def refresh(self):
        self._table.clear()
        for tp in self.sistema.listar_tipos_permiso():
            tag = ("rem",) if tp.es_remunerado else ("norem",)
            label = "✅  Remunerado" if tp.es_remunerado else "❌  No remunerado"
            self._table.add((tp.id, tp.descripcion, label), tags=tag)


class PermisosView(BaseView):
    def _build(self):
        wrap = tk.Frame(self, bg=C["canvas_bg"])
        wrap.pack(fill="both", expand=True, padx=32, pady=28)

        SectionHeader(wrap, "Registro de Permisos", "Historial de permisos del personal",
                      "＋  Nuevo permiso", self._open_form).pack(fill="x", pady=(0, 20))

        row = tk.Frame(wrap, bg=C["canvas_bg"])
        row.pack(fill="both", expand=True)

        card = tk.Frame(row, bg=C["card_bg"],
                        highlightbackground=C["border"], highlightthickness=1)
        card.pack(side="left", fill="both", expand=True)

        cols   = ("#", "Empleado",  "Tipo",  "Desde",  "Hasta",  "Tiempo", "Rem.", "Descuento")
        widths = (40,   180,         140,     100,      100,      80,       60,     110)
        self._table = Table(card, cols, widths)
        self._table.pack(fill="both", expand=True, padx=1, pady=1)

        foot = tk.Frame(card, bg=C["card_bg"], pady=10, padx=14)
        foot.pack(fill="x")
        tk.Label(foot, text="Seleccione un permiso para eliminarlo",
                 font=F["small"], bg=C["card_bg"], fg=C["text_muted"]).pack(side="left")
        Btn(foot, "🗑  Eliminar", self._eliminar, style="danger").pack(side="right", padx=4)

        # Panel — necesita scroll por número de campos
        self._panel = FormPanel(row, "Registrar Permiso", width=320)
        self._build_form(self._panel.body)

    def _build_form(self, body):
        # Empleado
        tk.Label(body, text="Empleado", font=F["small"],
                 bg=C["card_bg"], fg=C["text_muted"]).pack(anchor="w")
        self._emp_var  = tk.StringVar()
        self._cb_emp   = ttk.Combobox(body, textvariable=self._emp_var,
                                      state="readonly", font=F["body"])
        self._cb_emp.pack(fill="x", pady=(2, 12))
        self._cb_emp.bind("<<ComboboxSelected>>", self._preview)

        # Tipo permiso
        tk.Label(body, text="Tipo de permiso", font=F["small"],
                 bg=C["card_bg"], fg=C["text_muted"]).pack(anchor="w")
        self._tp_var   = tk.StringVar()
        self._cb_tipo  = ttk.Combobox(body, textvariable=self._tp_var,
                                      state="readonly", font=F["body"])
        self._cb_tipo.pack(fill="x", pady=(2, 12))
        self._cb_tipo.bind("<<ComboboxSelected>>", self._preview)

        # Fechas
        dates = tk.Frame(body, bg=C["card_bg"])
        dates.pack(fill="x", pady=4)

        lf = tk.Frame(dates, bg=C["card_bg"])
        lf.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self._f_desde = Field(lf, "Fecha desde")
        self._f_desde.pack(fill="x")
        tk.Label(lf, text="AAAA-MM-DD", font=F["micro"],
                 bg=C["card_bg"], fg=C["text_muted"]).pack(anchor="w")

        rf = tk.Frame(dates, bg=C["card_bg"])
        rf.pack(side="left", fill="x", expand=True)
        self._f_hasta = Field(rf, "Fecha hasta")
        self._f_hasta.pack(fill="x")
        tk.Label(rf, text="AAAA-MM-DD", font=F["micro"],
                 bg=C["card_bg"], fg=C["text_muted"]).pack(anchor="w")

        # Unidad de tiempo
        tk.Label(body, text="Unidad de tiempo", font=F["small"],
                 bg=C["card_bg"], fg=C["text_muted"]).pack(anchor="w", pady=(10, 4))
        self._tipo_var = tk.StringVar(value="D")

        rb_row = tk.Frame(body, bg=C["card_bg"])
        rb_row.pack(fill="x")
        for lbl, val in [("📅  Días", "D"), ("⏰  Horas", "H")]:
            tk.Radiobutton(rb_row, text=lbl, variable=self._tipo_var, value=val,
                           bg=C["card_bg"], fg=C["text_body"], font=F["body"],
                           selectcolor=C["card_bg"], activebackground=C["card_bg"],
                           cursor="hand2", command=self._preview
                           ).pack(side="left", padx=(0, 14))

        # Cantidad
        self._f_tiempo = Field(body, "Cantidad (días u horas)", numeric=True)
        self._f_tiempo.pack(fill="x", pady=(8, 10))
        self._f_tiempo.var.trace("w", self._preview)

        # Preview descuento
        self._prev_frame = tk.Frame(body, bg="#FEF2F2", pady=12, padx=14)
        self._prev_frame.pack(fill="x", pady=6)
        tk.Label(self._prev_frame, text="Descuento calculado",
                 font=F["small"], bg="#FEF2F2", fg=C["red"]).pack(anchor="w")
        self._lbl_desc = tk.Label(self._prev_frame, text="$ 0.00",
                                  font=("Segoe UI", 20, "bold"),
                                  bg="#FEF2F2", fg=C["red"])
        self._lbl_desc.pack(anchor="w")
        self._lbl_info = tk.Label(self._prev_frame, text="",
                                  font=F["small"], bg="#FEF2F2", fg=C["text_muted"])
        self._lbl_info.pack(anchor="w")

        sep = tk.Frame(body, bg=C["border"], height=1)
        sep.pack(fill="x", pady=12)

        btns = tk.Frame(body, bg=C["card_bg"])
        btns.pack(fill="x")
        Btn(btns, "Registrar", self._guardar,    style="primary").pack(side="left", padx=(0, 8))
        Btn(btns, "Cancelar",  self._panel.hide,  style="ghost").pack(side="left")

    def _preview(self, *_):
        try:
            emp_s  = self._emp_var.get()
            tipo_s = self._tp_var.get()
            t_str  = self._f_tiempo.get()
            if not emp_s or not tipo_s or not t_str: return
            id_emp = int(emp_s.split("|")[0].strip())
            id_tp  = int(tipo_s.split("|")[0].strip())
            emp    = self.sistema.buscar_empleado(id_emp)
            tp     = self.sistema.buscar_tipo_permiso(id_tp)
            tiempo = float(t_str)
            unidad = self._tipo_var.get()

            if tp and tp.es_remunerado:
                for w in self._prev_frame.winfo_children():
                    w.config(bg="#F0FFF4")
                self._prev_frame.config(bg="#F0FFF4")
                self._lbl_desc.config(text="$ 0.00", fg=C["green"], bg="#F0FFF4")
                self._lbl_info.config(text="✅ Remunerado — sin descuento", bg="#F0FFF4")
            elif emp and tp:
                desc = (tiempo * emp.valor_hora if unidad == "H"
                        else tiempo * HORAS_POR_DIA * emp.valor_hora)
                for w in self._prev_frame.winfo_children():
                    w.config(bg="#FEF2F2")
                self._prev_frame.config(bg="#FEF2F2")
                self._lbl_desc.config(text=f"${desc:,.2f}", fg=C["red"], bg="#FEF2F2")
                self._lbl_info.config(text="❌ No remunerado — se descontará del sueldo",
                                      bg="#FEF2F2")
        except:
            pass

    def _open_form(self):
        emps  = [f"{e.id} | {e.nombre}"         for e in self.sistema.listar_empleados()]
        tipos = [f"{tp.id} | {tp.descripcion}"   for tp in self.sistema.listar_tipos_permiso()]
        self._cb_emp["values"]  = emps
        self._cb_tipo["values"] = tipos
        self._emp_var.set("");  self._tp_var.set("")
        self._f_desde.clear();  self._f_hasta.clear()
        self._f_tiempo.clear(); self._tipo_var.set("D")
        self._panel.show()

    def _guardar(self):
        emp_s  = self._emp_var.get()
        tipo_s = self._tp_var.get()
        fd     = self._f_desde.get()
        fh     = self._f_hasta.get()
        tipo   = self._tipo_var.get()
        t_str  = self._f_tiempo.get()

        if not emp_s:
            messagebox.showwarning("Campo requerido", "Seleccione un empleado."); return
        if not tipo_s:
            messagebox.showwarning("Campo requerido", "Seleccione un tipo de permiso."); return
        if not fd or not fh:
            messagebox.showwarning("Campos requeridos", "Complete ambas fechas."); return

        for fecha, lbl in [(fd, "Fecha desde"), (fh, "Fecha hasta")]:
            try:
                datetime.strptime(fecha, FORMATO_FECHA)
            except:
                messagebox.showwarning("Formato de fecha",
                    f"{lbl} no tiene el formato correcto (AAAA-MM-DD)."); return

        if datetime.strptime(fd, FORMATO_FECHA) > datetime.strptime(fh, FORMATO_FECHA):
            messagebox.showwarning("Fechas inválidas",
                "La fecha 'desde' no puede ser posterior a la fecha 'hasta'."); return

        try:
            tiempo = float(t_str)
            if tiempo <= 0: raise ValueError()
        except:
            messagebox.showwarning("Tiempo inválido", "Ingrese una cantidad mayor a 0."); return

        id_emp = int(emp_s.split("|")[0].strip())
        id_tp  = int(tipo_s.split("|")[0].strip())

        try:
            p = self.sistema.crear_permiso(id_emp, id_tp, fd, fh, tipo, tiempo)
            messagebox.showinfo("Permiso registrado",
                                f"Permiso #{p.id} registrado exitosamente.")
            self._panel.hide()
            self.refresh()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def _eliminar(self):
        id_ = self._table.selected_id()
        if id_ is None:
            messagebox.showwarning("Sin selección", "Seleccione un permiso de la tabla."); return
        if messagebox.askyesno("Confirmar eliminación", f"¿Eliminar permiso #{id_}?"):
            if self.sistema.eliminar_permiso(int(id_)):
                messagebox.showinfo("Eliminado", f"Permiso #{id_} eliminado."); self.refresh()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el permiso.")

    def refresh(self):
        self._table.clear()
        for p in self.sistema.listar_permisos():
            emp = self.sistema.buscar_empleado(p.id_empleado)
            tp  = self.sistema.buscar_tipo_permiso(p.id_tipo_permiso)
            tag = ("rem",) if p.es_remunerado else ("norem",)
            self._table.add((
                p.id,
                emp.nombre if emp else "—",
                tp.descripcion if tp else "—",
                p.fecha_desde, p.fecha_hasta,
                f"{p.tiempo}{'h' if p.tipo == 'H' else 'd'}",
                "✅" if p.es_remunerado else "❌",
                f"${p.calcular_descuento():,.2f}",
            ), tags=tag)


# ── Ventana raíz ────────────────────────────────────────────

class App(tk.Tk):
    _NAV = [
        ("empleados", "👥", "Empleados"),
        ("tipos",     "📂", "Tipos de Permiso"),
        ("permisos",  "📋", "Permisos"),
    ]
    _VIEW_MAP = {
        "empleados": EmpleadosView,
        "tipos":     TiposPermisoView,
        "permisos":  PermisosView,
    }

    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Permisos")
        self.configure(bg=C["nav_bg"])
        self.minsize(980, 620)

        # Centrar ventana
        W, H = 1600, 800
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{W}x{H}+{(sw - W)//2}+{(sh - H)//2}")

        self.resizable(False, False)

        self.sistema   = SistemaPermisos()
        self._seed()
        self._views    = {}
        self._current  = None
        self._nav_btns = {}

        self._build()
        self._navigate("empleados")

    def _seed(self):
        """Datos de ejemplo (idénticos al main() original)."""
        self.sistema.crear_empleado("Juan Pérez",    2400)
        self.sistema.crear_empleado("María García",  3000)
        self.sistema.crear_tipo_permiso("Enfermedad", "S")
        self.sistema.crear_tipo_permiso("Personal",   "N")
        self.sistema.crear_tipo_permiso("Vacaciones", "S")

    def _build(self):
        # ── Sidebar ──────────────────────────────────────────
        self._sidebar = tk.Frame(self, bg=C["nav_bg"], width=220)
        self._sidebar.pack(side="left", fill="y")
        self._sidebar.pack_propagate(False)

        # Branding
        brand = tk.Frame(self._sidebar, bg=C["nav_bg"], pady=24, padx=20)
        brand.pack(fill="x")
        tk.Label(brand, text="🏢", font=("Segoe UI", 30),
                 bg=C["nav_bg"], fg="#FFFFFF").pack()
        tk.Label(brand, text="Gestión de Permisos", font=F["brand"],
                 bg=C["nav_bg"], fg="#FFFFFF").pack(pady=(4, 0))
        tk.Label(brand, text="Sistema de RRHH", font=F["micro"],
                 bg=C["nav_bg"], fg=C["text_nav"]).pack()

        tk.Frame(self._sidebar, bg="#1E3050", height=1).pack(fill="x", padx=16, pady=8)

        # Nav items
        nav_wrap = tk.Frame(self._sidebar, bg=C["nav_bg"])
        nav_wrap.pack(fill="x", pady=4)

        for key, icon, label in self._NAV:
            btn = NavButton(nav_wrap, icon, label, key, self._navigate)
            btn.pack(fill="x", padx=8, pady=1)
            self._nav_btns[key] = btn

        # Pie de sidebar
        tk.Frame(self._sidebar, bg=C["nav_bg"]).pack(fill="y", expand=True)
        foot = tk.Frame(self._sidebar, bg=C["nav_bg"], pady=16, padx=20)
        foot.pack(fill="x")
        tk.Frame(foot, bg="#1E3050", height=1).pack(fill="x", pady=(0, 10))
        tk.Label(foot, text=f"v2.0  ·  {datetime.now().year}",
                 font=F["micro"], bg=C["nav_bg"], fg="#374151").pack()

        # ── Área de contenido ─────────────────────────────────
        self._canvas = tk.Frame(self, bg=C["canvas_bg"])
        self._canvas.pack(side="right", fill="both", expand=True)

    def _navigate(self, key: str):
        if self._current == key:
            return

        # Desactivar botón anterior
        if self._current:
            self._nav_btns[self._current].deactivate()
            if self._current in self._views:
                self._views[self._current].pack_forget()

        self._current = key
        self._nav_btns[key].activate()

        # Crear o refrescar vista
        if key not in self._views:
            self._views[key] = self._VIEW_MAP[key](self._canvas, self.sistema)
        else:
            self._views[key].refresh()

        self._views[key].pack(fill="both", expand=True)


# ── Entry point ──────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()