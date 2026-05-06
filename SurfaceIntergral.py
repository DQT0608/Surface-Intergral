import customtkinter as ctk
import sympy as sp
import numpy as np
from scipy import integrate as scipy_integrate
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AppGiaiTich(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Giải Tích Phân Mặt Loại 1 & Tính Diện Tích")
        self.geometry("1400x900")
        self.nt_entries = []
        self.u, self.v, self.x, self.y, self.z = sp.symbols('u v x y z', real=True)
        self.local_dict = {'u': self.u, 'v': self.v, 'x': self.x, 'y': self.y, 'z': self.z}
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.sidebar = ctk.CTkScrollableFrame(self, width=450, label_text="CẤU HÌNH BÀI TOÁN")
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.setup_sidebar()
        self.main_area = ctk.CTkFrame(self)
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        ctk.CTkLabel(self.main_area, text="KẾT QUẢ TOÁN HỌC", font=("Arial", 16, "bold")).pack(pady=5)
        self.txt_result = ctk.CTkTextbox(self.main_area, height=180, font=("Consolas", 14))
        self.txt_result.pack(fill="x", padx=20, pady=5)
        self.latex_frame = ctk.CTkFrame(self.main_area, height=50, fg_color="transparent")
        self.latex_frame.pack(fill="x", padx=20, pady=0)
        self.canvas_frame = ctk.CTkFrame(self.main_area)
        self.canvas_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.cap_nhat_giao_dien_khuon_mau("Paraboloid úp") 

    def create_entry(self, parent, label, default, **pack_opts):
        """Hàm rút gọn giúp tạo nhanh 1 nhãn (Label) và 1 ô nhập (Entry) liên tiếp nhau"""
        ctk.CTkLabel(parent, text=label, anchor="w", font=("Arial", 12)).pack(fill="x", padx=2, **pack_opts)
        ent = ctk.CTkEntry(parent)
        ent.pack(fill="x", pady=(0, 5))
        ent.insert(0, default)
        return ent

    def setup_sidebar(self):
        ctk.CTkLabel(self.sidebar, text="1️⃣ Chọn loại bài toán:", font=("Arial", 13, "bold")).pack(anchor="w", pady=(10,0))
        self.loai_tp_var = ctk.StringVar(value="Tính Diện Tích Mặt Cong")
        ctk.CTkOptionMenu(self.sidebar, variable=self.loai_tp_var, 
                          values=["Tính Diện Tích Mặt Cong", "Tích phân mặt Loại 1"],
                          command=self.cap_nhat_giao_dien_loai).pack(fill="x", pady=5)
        ctk.CTkLabel(self.sidebar, text="2️⃣ Thiết lập mặt cong S:", font=("Arial", 13, "bold")).pack(anchor="w", pady=(10,0))
        self.tab_S = ctk.CTkTabview(self.sidebar, height=200)
        self.tab_S.pack(fill="x", pady=5)
        tab_km = self.tab_S.add("Khuôn mẫu")
        self.km_hinh_var = ctk.StringVar(value="Paraboloid úp")
        ctk.CTkOptionMenu(tab_km, variable=self.km_hinh_var, values=["Paraboloid úp", "Mặt cầu", "Mặt trụ", "Mặt nón", "Mặt phẳng"], command=self.cap_nhat_giao_dien_khuon_mau).pack(fill="x", pady=5)
        self.frame_km_inputs = ctk.CTkFrame(tab_km, fg_color="transparent")
        self.frame_km_inputs.pack(fill="both", expand=True)
        tab_nt = self.tab_S.add("Nhập tay")
        self.nt_loai_var = ctk.StringVar(value="Tham số hóa R(u,v)")
        ctk.CTkOptionMenu(tab_nt, variable=self.nt_loai_var, values=["Tham số hóa R(u,v)", "Descartes z=f(x,y)", "Descartes y=g(x,z)", "Descartes x=h(y,z)"], command=self.cap_nhat_giao_dien_nhap_tay).pack(fill="x", pady=5)
        self.frame_nt_inputs = ctk.CTkFrame(tab_nt, fg_color="transparent")
        self.frame_nt_inputs.pack(fill="both", expand=True)
        self.cap_nhat_giao_dien_nhap_tay("Tham số hóa R(u,v)")
        ctk.CTkLabel(self.sidebar, text="Cận tích phân (Miền D):", font=("Arial", 12, "bold")).pack(anchor="w", pady=(15, 5))
        frame_can = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        frame_can.pack(fill="x", padx=5)
        frame_can.grid_columnconfigure(1, weight=1)
        self.can_entries = {}
        for i, (key, lbl, default) in enumerate([("u_min", "Cận dưới u:", "0"), ("u_max", "Cận trên u:", "2"), ("v_min", "Cận dưới v:", "0"), ("v_max", "Cận trên v:", "2*pi")]):
            ctk.CTkLabel(frame_can, text=lbl, anchor="w").grid(row=i, column=0, sticky="w", pady=5)
            ent = ctk.CTkEntry(frame_can)
            ent.grid(row=i, column=1, sticky="ew", padx=(10, 0), pady=5)
            ent.insert(0, default)
            self.can_entries[key] = ent
        self.frame_f = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.frame_f.pack(fill="x") 
        self.lbl_f = ctk.CTkLabel(self.frame_f, text="3️⃣ Nhập hàm tích phân f(x,y,z):", font=("Arial", 13, "bold"))
        self.f_ent = ctk.CTkEntry(self.frame_f)
        self.f_ent.insert(0, "x**2 + y**2")
        self.cap_nhat_giao_dien_loai("Tính Diện Tích Mặt Cong")
        ctk.CTkLabel(self.sidebar, text="4️⃣ Phương pháp giải:", font=("Arial", 13, "bold")).pack(anchor="w", pady=(10,0))
        self.pp_giai_var = ctk.StringVar(value="Tính nhanh Xấp xỉ")
        for txt, val in [("Tính nhanh Xấp xỉ", "SciPy"), ("Tính Chính xác", "SymPy")]:
            ctk.CTkRadioButton(self.sidebar, text=txt, variable=self.pp_giai_var, value=val).pack(anchor="w", pady=2)
        ctk.CTkButton(self.sidebar, text="BẮT ĐẦU GIẢI TOÁN", command=self.tinh_toan, fg_color="#28a745", hover_color="#218838", font=("Arial", 14, "bold")).pack(fill="x", pady=20)

    def cap_nhat_giao_dien_khuon_mau(self, hinh):
        for widget in self.frame_km_inputs.winfo_children(): widget.destroy()
        self.km_entries = {}
        configs = {
            "Paraboloid úp": [("a", "Hệ số a (Đỉnh z):", "2.0"), ("z_min", "Cắt bởi z_min:", "0.0"), ("z_max", "Cắt bởi z_max:", "1.0")],
            "Mặt cầu": [("R", "Bán kính R:", "2.0"), ("z_min", "Cắt bởi z_min:", "0.0"), ("z_max", "Cắt bởi z_max:", "2.0")],
            "Mặt trụ": [("R", "Bán kính R:", "2.0"), ("z_min", "z_min:", "0.0"), ("z_max", "z_max:", "3.0")],
            "Mặt nón": [("z_max", "Chiều cao nón:", "2.0"), ("z_min", "Cắt từ (z_min):", "0.0")],
            "Mặt phẳng": [("A", "Hệ số A:", "-1.0"), ("B", "Hệ số B:", "-1.0"), ("C", "Hệ số C:", "3.0")]
        }
        for key, lbl, default in configs.get(hinh, []):
            self.km_entries[key] = self.create_entry(self.frame_km_inputs, lbl, default, pady=(5,0))
    
    def cap_nhat_giao_dien_nhap_tay(self, loai):
        for widget in self.frame_nt_inputs.winfo_children(): widget.destroy()
        self.nt_entries = []
        configs = {
            "Tham số hóa R(u,v)": (["Hàm x(u, v):", "Hàm y(u, v):", "Hàm z(u, v):"], ["u*cos(v)", "u*sin(v)", "2 - u**2"]),
            "Descartes z=f(x,y)": (["Nhập phương trình z = f(x, y):"], ["x**2 + y**2"]),
            "Descartes y=g(x,z)": (["Nhập phương trình y = g(x, z):"], ["x**2 + z**2"]),
            "Descartes x=h(y,z)": (["Nhập phương trình x = h(y, z):"], ["y**2 + z**2"])
        }
        labels, defaults = configs.get(loai, ([], [])) 
        for lbl, d in zip(labels, defaults):
            self.nt_entries.append(self.create_entry(self.frame_nt_inputs, lbl, d))
    
    def cap_nhat_giao_dien_loai(self, loai):
        if loai == "Tích phân mặt Loại 1":
            self.lbl_f.pack(anchor="w", pady=(10,0))
            self.f_ent.pack(fill="x", pady=(0, 5))
        else:
            self.lbl_f.pack_forget()
            self.f_ent.pack_forget()

    def parse_sym(self, text):
        return sp.sympify(text.replace('^', '**'), locals=self.local_dict)

    def lay_du_lieu_mat_S(self):
        bounds = [self.parse_sym(self.can_entries[k].get()) for k in ["u_min", "u_max", "v_min", "v_max"]]
        if self.tab_S.get() == "Khuôn mẫu":
            hinh = self.km_hinh_var.get()
            vals = {k: float(v.get()) for k, v in self.km_entries.items()}
            u, v = self.u, self.v
            x_e = y_e = z_e = 0 
            if hinh == "Paraboloid úp":
                x_e, y_e, z_e = u * sp.cos(v), u * sp.sin(v), vals['a'] - u**2
                bounds[:2] = [np.sqrt(max(0, vals['a'] - vals['z_max'])), np.sqrt(max(0, vals['a'] - vals['z_min']))]
            elif hinh == "Mặt cầu":
                x_e, y_e, z_e = vals['R'] * sp.sin(u) * sp.cos(v), vals['R'] * sp.sin(u) * sp.sin(v), vals['R'] * sp.cos(u)
                bounds[:2] = [float(sp.acos(vals['z_max'] / vals['R'])), float(sp.acos(vals['z_min'] / vals['R']))]
            elif hinh == "Mặt trụ":
                x_e, y_e, z_e = vals['R'] * sp.cos(v), vals['R'] * sp.sin(v), u
                bounds[:2] = [vals['z_min'], vals['z_max']]
            elif hinh == "Mặt nón":
                x_e, y_e, z_e = u * sp.cos(v), u * sp.sin(v), u
                bounds[:2] = [vals['z_min'], vals['z_max']]
            elif hinh == "Mặt phẳng":
                x_e, y_e, z_e = u, v, vals['A']*u + vals['B']*v + vals['C']
            if hinh in ["Paraboloid úp", "Mặt cầu", "Mặt trụ", "Mặt nón"]: bounds[2:] = [0, 2 * sp.pi]
            return x_e, y_e, z_e, *bounds
        loai = self.nt_loai_var.get()
        if loai == "Tham số hóa R(u,v)": 
            s1, s2, s3 = [self.parse_sym(e.get()) for e in self.nt_entries]
            return s1, s2, s3, *bounds
        else:
            s1 = self.parse_sym(self.nt_entries[0].get())
            if loai == "Descartes z=f(x,y)": return self.u, self.v, s1.subs({self.x: self.u, self.y: self.v}), *bounds
            if loai == "Descartes y=g(x,z)": return self.u, s1.subs({self.x: self.u, self.z: self.v}), self.v, *bounds
            if loai == "Descartes x=h(y,z)": return s1.subs({self.y: self.u, self.z: self.v}), self.u, self.v, *bounds

    def tinh_toan(self):
        try:
            for w in self.latex_frame.winfo_children(): w.destroy()
            self.txt_result.delete("1.0", "end")
            self.txt_result.insert("end", "Đang xử lý toán học...\n")
            self.update() 
            loai_tp, pp_giai = self.loai_tp_var.get(), self.pp_giai_var.get()
            x_e, y_e, z_e, u_min_v, u_max_v, v_min_v, v_max_v = self.lay_du_lieu_mat_S()
            r = sp.Matrix([x_e, y_e, z_e])
            n = sp.diff(r, self.u).cross(sp.diff(r, self.v))
            norm_n = sp.simplify(sp.sqrt(sp.trigsimp(n.dot(n))))
            f_expr_str = "1" if "Diện Tích" in loai_tp else self.f_ent.get()
            f_expr = sp.sympify(f_expr_str, locals=self.local_dict)
            integrand = sp.simplify(f_expr.subs({self.x: x_e, self.y: y_e, self.z: z_e}) * norm_n)
            self.txt_result.insert("end", f"Biểu thức dS = ||ru x rv|| du dv:\n{norm_n}\n\n")
            self.txt_result.insert("end", f"Biểu thức tích phân:\n{integrand}\n\n")
            if "SymPy" in pp_giai:
                result = sp.integrate(integrand, (self.u, u_min_v, u_max_v), (self.v, v_min_v, v_max_v))
                if result.has(sp.Integral):
                    self.txt_result.insert("end", "SymPy không giải ra công thức chặn. Hãy chuyển sang tính xáp xỉ.\n")
                else:
                    self.txt_result.insert("end", f"KẾT QUẢ: Đã hiển thị dưới dạng công thức.\n   Giá trị thập phân: {result.evalf():.6f}\n")
                    self.hien_thi_latex(result)
            else:
                func_lam = sp.lambdify((self.u, self.v), integrand, "numpy")
                u_mi, u_ma, v_mi, v_ma = float(sp.N(u_min_v)), float(sp.N(u_max_v)), float(sp.N(v_min_v)), float(sp.N(v_max_v))
                res, err = scipy_integrate.dblquad(lambda v_v, u_v: func_lam(u_v, v_v), u_mi, u_ma, lambda _: v_mi, lambda _: v_ma)
                self.txt_result.insert("end", f" KẾT QUẢ XẤP XỈ: {res:.6f}\n   Sai số: {err:.2e}\n")
            self.ve_hinh(x_e, y_e, z_e, u_min_v, u_max_v, v_min_v, v_max_v)
        except Exception as e:
            self.txt_result.insert("end", f"\nCÓ LỖI XẢY RA:\n{e}")

    def ve_hinh(self, x_e, y_e, z_e, u_mi, u_ma, v_mi, v_ma):
        for w in self.canvas_frame.winfo_children(): w.destroy()
        fig = Figure(figsize=(6, 5), dpi=100)
        ax = fig.add_subplot(111, projection='3d')
        try:
            U, V = np.meshgrid(np.linspace(float(sp.N(u_mi)), float(sp.N(u_ma)), 40), np.linspace(float(sp.N(v_mi)), float(sp.N(v_ma)), 40))
            X, Y, Z = (np.broadcast_to(sp.lambdify((self.u, self.v), expr, "numpy")(U, V), U.shape) for expr in (x_e, y_e, z_e))
            ax.plot_surface(X, Y, Z, cmap='plasma', alpha=0.8, edgecolor='black', linewidth=0.3)
            ax.scatter([0], [0], [0], color='black', s=50, zorder=5)
            ax.text(0, 0, 0, "  O(0,0,0)", color='black', fontweight='bold')
            L = max(np.max(np.abs(X)), np.max(np.abs(Y)), np.max(np.abs(Z)), 2)
            for d, c, t in [((L,0,0), 'red', 'X'), ((0,L,0), 'green', 'Y'), ((0,0,L), 'blue', 'Z')]:
                ax.quiver(0,0,0, *d, color=c, arrow_length_ratio=0.1, linewidth=2)
                ax.text(*d, t, color=c, fontweight='bold', fontsize=12)
            ax.set_title("Đồ thị Mặt Cong S")
            FigureCanvasTkAgg(fig, master=self.canvas_frame).get_tk_widget().pack(fill="both", expand=True)
        except Exception as e:
            ctk.CTkLabel(self.canvas_frame, text=f"Lỗi vẽ đồ thị: {e}", text_color="red").pack()
    
    def hien_thi_latex(self, ket_qua_sympy):
        for w in self.latex_frame.winfo_children(): w.destroy()
        fig = Figure(figsize=(6, 0.8), dpi=100)
        bg, fg = ("#2b2b2b", "white") if ctk.get_appearance_mode() == "Dark" else ("#dbdbdb", "black")
        fig.patch.set_facecolor(bg)
        ax = fig.add_subplot(111)
        ax.axis('off')
        ax.text(0.5, 0.5, rf"$Kết \ quả: \mathbf{{I = {sp.latex(ket_qua_sympy)}}}$", fontsize=18, ha='center', va='center', color=fg)
        FigureCanvasTkAgg(fig, master=self.latex_frame).get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    app = AppGiaiTich()
    app.mainloop()
