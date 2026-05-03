import customtkinter as ctk
import sympy as sp
import numpy as np
from scipy import integrate as scipy_integrate
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Thiết lập giao diện người dùng
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AppGiaiTich(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Giải Tích Phân Mặt 3D PRO - Bản Đầy Đủ")
        self.geometry("1400x900")

        # Khởi tạo các biến ký hiệu toán học (u, v cho tham số và x, y, z cho không gian)
        self.u, self.v, self.x, self.y, self.z = sp.symbols('u v x y z', real=True)
        # local_dict giúp SymPy hiểu các ký tự nhập từ Entry là các biến toán học đã định nghĩa
        self.local_dict = {'u': self.u, 'v': self.v, 'x': self.x, 'y': self.y, 'z': self.z}

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # KHU VỰC TRÁI (nhập dữ liệu đầu vào)

        self.sidebar = ctk.CTkScrollableFrame(self, width=450, label_text="⚙️ CẤU HÌNH BÀI TOÁN")
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.setup_sidebar()

        # KHU VỰC PHẢI (hiển thị kết quả toán học và đồ thị)

        self.main_area = ctk.CTkFrame(self)
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        self.lbl_res_title = ctk.CTkLabel(self.main_area, text="KẾT QUẢ TOÁN HỌC", font=("Arial", 16, "bold"))
        self.lbl_res_title.pack(pady=5)

        # Ô hiển thị các bước trung gian và giá trị số
        self.txt_result = ctk.CTkTextbox(self.main_area, height=180, font=("Consolas", 14))
        self.txt_result.pack(fill="x", padx=20, pady=5)

        # Frame render công thức LaTeX từ SymPy
        self.latex_frame = ctk.CTkFrame(self.main_area, height=50, fg_color="transparent")
        self.latex_frame.pack(fill="x", padx=20, pady=0)

        # Frame chứa khung vẽ Matplotlib
        self.canvas_frame = ctk.CTkFrame(self.main_area)
        self.canvas_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.cap_nhat_giao_dien_khuon_mau("Paraboloid úp") 

    def setup_sidebar(self):
        # 1. Menu chọn loại bài toán: tính diện tích loại 1 hoặc loại 2 
        ctk.CTkLabel(self.sidebar, text="1️⃣ Chọn loại bài toán:", font=("Arial", 13, "bold")).pack(anchor="w", pady=(10,0))
        self.loai_tp_var = ctk.StringVar(value="Tính Diện Tích Mặt Cong")
        ctk.CTkOptionMenu(self.sidebar, variable=self.loai_tp_var, 
                          values=["Tính Diện Tích Mặt Cong", "Tích phân mặt Loại 1", "Tích phân mặt Loại 2"]).pack(fill="x", pady=5)

        # 2. Thiết lập mặt cong S: cho phép chọn hình mẫu có sẵn hoặc tự nhập phương trình tham số
        ctk.CTkLabel(self.sidebar, text="2️⃣ Thiết lập mặt cong S:", font=("Arial", 13, "bold")).pack(anchor="w", pady=(10,0))
        self.tab_S = ctk.CTkTabview(self.sidebar, height=200)
        self.tab_S.pack(fill="x", pady=5)
        
        tab_khuon_mau = self.tab_S.add("Khuôn mẫu")
        tab_nhap_tay = self.tab_S.add("Nhập tay")

        # Cấu hình tab khuôn mẫu (cầu, trụ, nón, ...)
        self.km_hinh_var = ctk.StringVar(value="Paraboloid úp")
        ctk.CTkOptionMenu(tab_khuon_mau, variable=self.km_hinh_var, 
                          values=["Paraboloid úp", "Mặt cầu", "Mặt trụ", "Mặt nón", "Mặt phẳng"],
                          command=self.cap_nhat_giao_dien_khuon_mau).pack(fill="x", pady=5)
        
        self.frame_km_inputs = ctk.CTkFrame(tab_khuon_mau, fg_color="transparent")
        self.frame_km_inputs.pack(fill="both", expand=True)

        # Cấu hình tab Nhập tay (tự do tham số hóa hoặc tọa độ Descartes)
        self.nt_loai_var = ctk.StringVar(value="Tham số hóa R(u,v)")
        ctk.CTkOptionMenu(tab_nhap_tay, variable=self.nt_loai_var, 
                          values=["Tham số hóa R(u,v)", "Descartes z=f(x,y)", "Descartes y=g(x,z)", "Descartes x=h(y,z)"]).pack(fill="x", pady=5)
        
        ctk.CTkLabel(tab_nhap_tay, text="x(u, v):", anchor="w", font=("Arial", 12)).pack(fill="x", padx=2)
        self.nt_1 = ctk.CTkEntry(tab_nhap_tay)
        self.nt_1.pack(fill="x", pady=(0, 5))
        
        ctk.CTkLabel(tab_nhap_tay, text="y(u, v):", anchor="w", font=("Arial", 12)).pack(fill="x", padx=2)
        self.nt_2 = ctk.CTkEntry(tab_nhap_tay)
        self.nt_2.pack(fill="x", pady=(0, 5))
        
        ctk.CTkLabel(tab_nhap_tay, text="z(u, v):", anchor="w", font=("Arial", 12)).pack(fill="x", padx=2)
        self.nt_3 = ctk.CTkEntry(tab_nhap_tay)
        self.nt_3.pack(fill="x", pady=(0, 5))
        
        self.nt_1.insert(0, "u*cos(v)"); self.nt_2.insert(0, "u*sin(v)"); self.nt_3.insert(0, "2 - u**2")

        # Thiết lập miền D: cận cho biến u và v
        ctk.CTkLabel(self.sidebar, text="Cận tích phân (Miền D):", font=("Arial", 12, "bold")).pack(anchor="w", pady=(15, 5))
        frame_can = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        frame_can.pack(fill="x", padx=5)
        frame_can.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame_can, text="Cận dưới u (min):", anchor="w").grid(row=0, column=0, sticky="w", pady=5)
        self.can_u_min = ctk.CTkEntry(frame_can)
        self.can_u_min.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=5)

        ctk.CTkLabel(frame_can, text="Cận trên u (max):", anchor="w").grid(row=1, column=0, sticky="w", pady=5)
        self.can_u_max = ctk.CTkEntry(frame_can)
        self.can_u_max.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=5)

        ctk.CTkLabel(frame_can, text="Cận dưới v (min):", anchor="w").grid(row=2, column=0, sticky="w", pady=5)
        self.can_v_min = ctk.CTkEntry(frame_can)
        self.can_v_min.grid(row=2, column=1, sticky="ew", padx=(10, 0), pady=5)

        ctk.CTkLabel(frame_can, text="Cận trên v (max):", anchor="w").grid(row=3, column=0, sticky="w", pady=5)
        self.can_v_max = ctk.CTkEntry(frame_can)
        self.can_v_max.grid(row=3, column=1, sticky="ew", padx=(10, 0), pady=5)

        self.can_u_min.insert(0, "0"); self.can_u_max.insert(0, "2")
        self.can_v_min.insert(0, "0"); self.can_v_max.insert(0, "2*pi")

        # 3. Nhập hàm tích phân f(x,y,z) cho loại 1 hoặc Trường Vector (P,Q,R) cho loại 2
        ctk.CTkLabel(self.sidebar, text="3️⃣ Hàm / Trường Vector:", font=("Arial", 13, "bold")).pack(anchor="w", pady=(10,0))
        self.tab_F = ctk.CTkTabview(self.sidebar, height=150)
        self.tab_F.pack(fill="x", pady=5)
        
        tab_vo_huong = self.tab_F.add("Hàm Vô Hướng (Loại 1)")
        self.f_ent = ctk.CTkEntry(tab_vo_huong, placeholder_text="Nhập f(x,y,z)"); self.f_ent.pack(fill="x", pady=10)
        self.f_ent.insert(0, "x**2 + y**2")

        tab_vector = self.tab_F.add("Trường Vector (Loại 2)")
        self.p_ent = ctk.CTkEntry(tab_vector, placeholder_text="P(x,y,z)"); self.p_ent.pack(fill="x", pady=2)
        self.q_ent = ctk.CTkEntry(tab_vector, placeholder_text="Q(x,y,z)"); self.q_ent.pack(fill="x", pady=2)
        self.r_ent = ctk.CTkEntry(tab_vector, placeholder_text="R(x,y,z)"); self.r_ent.pack(fill="x", pady=2)
        self.p_ent.insert(0, "0"); self.q_ent.insert(0, "0"); self.r_ent.insert(0, "z")

        # 4. Chọn công cụ giải: SciPy hoặc SymPy (đối với SymPy, nếu không giải được công thức chặn sẽ thông báo và khuyến nghị chuyển sang SciPy)
        ctk.CTkLabel(self.sidebar, text="4️⃣ Phương pháp giải:", font=("Arial", 13, "bold")).pack(anchor="w", pady=(10,0))
        self.pp_giai_var = ctk.StringVar(value="Tính nhanh Xấp xỉ (SciPy)")
        ctk.CTkRadioButton(self.sidebar, text="Tính nhanh Xấp xỉ (SciPy)", variable=self.pp_giai_var, value="SciPy").pack(anchor="w", pady=2)
        ctk.CTkRadioButton(self.sidebar, text="Tính Chính xác tuyệt đối (SymPy)", variable=self.pp_giai_var, value="SymPy").pack(anchor="w", pady=2)

        self.btn_solve = ctk.CTkButton(self.sidebar, text="🚀 BẮT ĐẦU GIẢI TOÁN", command=self.tinh_toan, fg_color="#28a745", hover_color="#218838", font=("Arial", 14, "bold"))
        self.btn_solve.pack(fill="x", pady=20)

    def cap_nhat_giao_dien_khuon_mau(self, hinh):
        """Hàm động: Thay đổi các ô nhập thông số tùy theo hình hình học được chọn"""
        for widget in self.frame_km_inputs.winfo_children():
            widget.destroy()

        self.km_entries = {} 

        def ve_o_nhap(key, label_text, default_val):
            ctk.CTkLabel(self.frame_km_inputs, text=label_text, anchor="w", font=("Arial", 12)).pack(fill="x", padx=2, pady=(5,0))
            ent = ctk.CTkEntry(self.frame_km_inputs)
            ent.pack(fill="x", pady=2)
            ent.insert(0, default_val)
            self.km_entries[key] = ent 

        if hinh == "Paraboloid úp":
            ve_o_nhap("a", "Hệ số a (Đỉnh z):", "2.0")
            ve_o_nhap("z_min", "Cắt bởi z_min:", "0.0")
            ve_o_nhap("z_max", "Cắt bởi z_max:", "1.0")
        elif hinh == "Mặt cầu":
            ve_o_nhap("R", "Bán kính R:", "2.0")
            ve_o_nhap("z_min", "Cắt bởi z_min:", "0.0")
            ve_o_nhap("z_max", "Cắt bởi z_max:", "2.0")
        elif hinh == "Mặt trụ":
            ve_o_nhap("R", "Bán kính R:", "2.0")
            ve_o_nhap("z_min", "z_min:", "0.0")
            ve_o_nhap("z_max", "z_max:", "3.0")
        elif hinh == "Mặt nón":
            ve_o_nhap("z_max", "Chiều cao nón (z_max):", "2.0")
            ve_o_nhap("z_min", "Cắt từ (z_min):", "0.0")
        elif hinh == "Mặt phẳng":
            ve_o_nhap("A", "Hệ số A:", "-1.0")
            ve_o_nhap("B", "Hệ số B:", "-1.0")
            ve_o_nhap("C", "Hệ số C:", "3.0")

    def lay_du_lieu_mat_S(self):
        """Logic xử lý chuyển đổi từ thông số hình học/nhập tay sang dạng phương trình tham số R(u,v)"""
        che_do = self.tab_S.get()
        u_min_v = sp.sympify(self.can_u_min.get(), locals=self.local_dict)
        u_max_v = sp.sympify(self.can_u_max.get(), locals=self.local_dict)
        v_min_v = sp.sympify(self.can_v_min.get(), locals=self.local_dict)
        v_max_v = sp.sympify(self.can_v_max.get(), locals=self.local_dict)

        if che_do == "Khuôn mẫu":
            hinh = self.km_hinh_var.get()
            
            if hinh == "Paraboloid úp":
                a_val = float(self.km_entries["a"].get())
                z_min, z_max = float(self.km_entries["z_min"].get()), float(self.km_entries["z_max"].get())
                x_e, y_e, z_e = self.u * sp.cos(self.v), self.u * sp.sin(self.v), a_val - self.u**2
                u_min_v, u_max_v = np.sqrt(max(0, a_val - z_max)), np.sqrt(max(0, a_val - z_min))
                v_min_v, v_max_v = 0, 2 * sp.pi
                
            elif hinh == "Mặt cầu":
                R_val = float(self.km_entries["R"].get())
                z_min, z_max = float(self.km_entries["z_min"].get()), float(self.km_entries["z_max"].get())
                x_e = R_val * sp.sin(self.u) * sp.cos(self.v)
                y_e = R_val * sp.sin(self.u) * sp.sin(self.v)
                z_e = R_val * sp.cos(self.u)
                u_min_v, u_max_v = float(sp.acos(z_max / R_val)), float(sp.acos(z_min / R_val))
                v_min_v, v_max_v = 0, 2 * sp.pi
                
            elif hinh == "Mặt trụ":
                R_val = float(self.km_entries["R"].get())
                z_min, z_max = float(self.km_entries["z_min"].get()), float(self.km_entries["z_max"].get())
                x_e, y_e, z_e = R_val * sp.cos(self.v), R_val * sp.sin(self.v), self.u
                u_min_v, u_max_v = z_min, z_max
                v_min_v, v_max_v = 0, 2 * sp.pi
                
            elif hinh == "Mặt nón":
                z_max = float(self.km_entries["z_max"].get())
                z_min = float(self.km_entries["z_min"].get())
                x_e, y_e, z_e = self.u * sp.cos(self.v), self.u * sp.sin(self.v), self.u
                u_min_v, u_max_v = z_min, z_max
                v_min_v, v_max_v = 0, 2 * sp.pi
                
            elif hinh == "Mặt phẳng":
                A = float(self.km_entries["A"].get())
                B, C = float(self.km_entries["B"].get()), float(self.km_entries["C"].get())
                x_e, y_e, z_e = self.u, self.v, A*self.u + B*self.v + C
                
            return x_e, y_e, z_e, u_min_v, u_max_v, v_min_v, v_max_v

        else: # Chế độ Nhập tay
            loai = self.nt_loai_var.get()
            s1, s2, s3 = self.nt_1.get(), self.nt_2.get(), self.nt_3.get()
            
            if loai == "Tham số hóa R(u,v)":
                x_e = sp.sympify(s1.replace('^', '**'), locals=self.local_dict)
                y_e = sp.sympify(s2.replace('^', '**'), locals=self.local_dict)
                z_e = sp.sympify(s3.replace('^', '**'), locals=self.local_dict)
            elif loai == "Descartes z=f(x,y)":
                x_e, y_e = self.u, self.v
                z_e = sp.sympify(s1.replace('^', '**'), locals=self.local_dict).subs({self.x: self.u, self.y: self.v})
            elif loai == "Descartes y=g(x,z)":
                x_e, z_e = self.u, self.v
                y_e = sp.sympify(s1.replace('^', '**'), locals=self.local_dict).subs({self.x: self.u, self.z: self.v})
            elif loai == "Descartes x=h(y,z)":
                y_e, z_e = self.u, self.v
                x_e = sp.sympify(s1.replace('^', '**'), locals=self.local_dict).subs({self.y: self.u, self.z: self.v})
                
            return x_e, y_e, z_e, u_min_v, u_max_v, v_min_v, v_max_v

    def tinh_toan(self):
        """Hàm xử lý chính: Thực hiện thuật toán Hình học vi phân để giải Tích phân mặt"""
        try:
            # 1. Dọn dẹp giao diện trước khi giải bài mới
            for widget in self.latex_frame.winfo_children():
                widget.destroy()

            self.txt_result.delete("1.0", "end")
            self.txt_result.insert("end", "Đang xử lý toán học...\n")
            self.update()

            # 2. Lấy thông tin phương trình mặt S từ giao diện
            loai_tp = self.loai_tp_var.get()
            pp_giai = self.pp_giai_var.get()
            x_e, y_e, z_e, u_min_v, u_max_v, v_min_v, v_max_v = self.lay_du_lieu_mat_S()

            # 3. Tính Vector pháp tuyến n = ru x rv
            # ru, rv là các đạo hàm riêng của vector vị trí r theo tham số u và v
            r = sp.Matrix([x_e, y_e, z_e])
            ru, rv = sp.diff(r, self.u), sp.diff(r, self.v)
            n = ru.cross(rv)

            # 4. Phân loại và xây dựng biểu thức dưới dấu tích phân
            if "Loại 1" in loai_tp or "Diện Tích" in loai_tp:
                # Tích phân loại 1: f * |n| du dv
                norm_n = sp.simplify(sp.sqrt(sp.trigsimp(n.dot(n))))
                if "Diện Tích" in loai_tp:
                    f_str = "1"
                else:
                    f_str = self.f_ent.get()
                
                f_expr = sp.sympify(f_str, locals=self.local_dict)
                f_uv = f_expr.subs({self.x: x_e, self.y: y_e, self.z: z_e})
                integrand = sp.simplify(f_uv * norm_n)
            else: 
                # Tích phân loại 2: F . n du dv (Tích vô hướng trường Vector F và pháp tuyến n)
                P = sp.sympify(self.p_ent.get(), locals=self.local_dict)
                Q = sp.sympify(self.q_ent.get(), locals=self.local_dict)
                R_vec = sp.sympify(self.r_ent.get(), locals=self.local_dict)
                subs_dict = {self.x: x_e, self.y: y_e, self.z: z_e}
                F_uv = sp.Matrix([P.subs(subs_dict), Q.subs(subs_dict), R_vec.subs(subs_dict)])
                integrand = sp.simplify(F_uv.dot(n))

            self.txt_result.insert("end", f"Biểu thức Integrand d(u,v):\n{integrand}\n\n")

            # 5. Thực hiện tính Tích phân kép
            if "SymPy" in pp_giai:
                self.txt_result.insert("end", "⏳ Đang tính chính xác (SymPy), có thể hơi lâu...\n")
                self.update()
                # Giải bằng giải tích 
                result = sp.integrate(integrand, (self.u, u_min_v, u_max_v), (self.v, v_min_v, v_max_v))
                if result.has(sp.Integral):
                    self.txt_result.insert("end", "⚠️ SymPy không giải ra công thức chặn. Hãy chuyển sang SciPy.\n")
                else:
                    self.txt_result.insert("end", f"✅ KẾT QUẢ CHÍNH XÁC: Đã hiển thị dưới dạng công thức toán.\n")
                    self.txt_result.insert("end", f"   Giá trị thập phân: {result.evalf():.6f}\n")
                    self.hien_thi_latex(result)
            else: 
                # Giải bằng phương pháp số (xấp xỉ dblquad của SciPy)
                func_lam = sp.lambdify((self.u, self.v), integrand, "numpy")
                u_mi, u_ma = float(sp.N(u_min_v)), float(sp.N(u_max_v))
                v_mi, v_ma = float(sp.N(v_min_v)), float(sp.N(v_max_v))
                
                res, err = scipy_integrate.dblquad(lambda v_v, u_v: func_lam(u_v, v_v), 
                                                   u_mi, u_ma, 
                                                   lambda u_v: v_mi, lambda u_v: v_ma)
                self.txt_result.insert("end", f"✅ KẾT QUẢ XẤP XỈ (SciPy): {res:.6f}\n")
                self.txt_result.insert("end", f"   Sai số: {err:.2e}\n")

            # 6. Vẽ đồ thị 3D trực quan
            self.ve_hinh(x_e, y_e, z_e, u_min_v, u_max_v, v_min_v, v_max_v)

        except Exception as e:
            self.txt_result.insert("end", f"\n❌ CÓ LỖI XẢY RA:\n{e}\n(Hãy kiểm tra lại cú pháp nhập liệu)")

    def ve_hinh(self, x_e, y_e, z_e, u_mi, u_ma, v_mi, v_ma):
        """Vẽ mặt cong S và hệ trục tọa độ Oxyz sử dụng Matplotlib"""
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        fig = Figure(figsize=(6, 5), dpi=100)
        ax = fig.add_subplot(111, projection='3d')

        try:
            # Tạo lưới giá trị cho u và v
            u_arr = np.linspace(float(sp.N(u_mi)), float(sp.N(u_ma)), 40)
            v_arr = np.linspace(float(sp.N(v_mi)), float(sp.N(v_ma)), 40)
            U, V = np.meshgrid(u_arr, v_arr)

            # Chuyển biểu thức SymPy sang hàm NumPy để tính toán mảng nhanh chóng
            xf = sp.lambdify((self.u, self.v), x_e, "numpy")
            yf = sp.lambdify((self.u, self.v), y_e, "numpy")
            zf = sp.lambdify((self.u, self.v), z_e, "numpy")

            X, Y, Z = xf(U, V), yf(U, V), zf(U, V)
            # Xử lý trường hợp hàm là hằng số
            if np.isscalar(X): X = np.full_like(U, X)
            if np.isscalar(Y): Y = np.full_like(U, Y)
            if np.isscalar(Z): Z = np.full_like(U, Z)

            # Vẽ bề mặt với màu sắc
            ax.plot_surface(X, Y, Z, cmap='plasma', alpha=0.8, edgecolor='black', linewidth=0.3)

            # Đánh dấu gốc tọa độ
            ax.scatter([0], [0], [0], color='black', s=50, zorder=5)
            ax.text(0, 0, 0, "  O(0,0,0)", color='black', fontweight='bold')

            axis_length = max(np.max(np.abs(X)), np.max(np.abs(Y)), np.max(np.abs(Z)), 2)

            # Vẽ 3 mũi tên trục X, Y, Z
            ax.quiver(0, 0, 0, axis_length, 0, 0, color='red', arrow_length_ratio=0.1, linewidth=2)
            ax.quiver(0, 0, 0, 0, axis_length, 0, color='green', arrow_length_ratio=0.1, linewidth=2)
            ax.quiver(0, 0, 0, 0, 0, axis_length, color='blue', arrow_length_ratio=0.1, linewidth=2)

            ax.text(axis_length, 0, 0, "X", color='red', fontweight='bold', fontsize=12)
            ax.text(0, axis_length, 0, "Y", color='green', fontweight='bold', fontsize=12)
            ax.text(0, 0, axis_length, "Z", color='blue', fontweight='bold', fontsize=12)

            ax.set_title("Đồ thị Mặt Cong S")

            # Nhúng đồ thị vào giao diện CustomTkinter
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
        except Exception as e:
            ctk.CTkLabel(self.canvas_frame, text=f"❌ Lỗi vẽ đồ thị: {e}", text_color="red").pack()
    
    def hien_thi_latex(self, ket_qua_sympy):
        """Chuyển đổi kết quả SymPy sang chuỗi LaTeX và hiển thị dưới dạng hình ảnh"""
        for widget in self.latex_frame.winfo_children():
            widget.destroy()
            
        fig = Figure(figsize=(6, 0.8), dpi=100)
        
        # Tự động điều chỉnh màu nền của ảnh LaTeX theo chế độ Dark/Light của App
        if ctk.get_appearance_mode() == "Dark":
            bg_color = "#2b2b2b" 
            text_color = "white"
        else:
            bg_color = "#dbdbdb" 
            text_color = "black"
            
        fig.patch.set_facecolor(bg_color)
        
        ax = fig.add_subplot(111)
        ax.axis('off') 
        
        # Chuyển kết quả toán học sang mã LaTeX
        latex_str = r"$Kết \ quả: \mathbf{I = " + sp.latex(ket_qua_sympy) + r"}$"
        ax.text(0.5, 0.5, latex_str, fontsize=18, ha='center', va='center', color=text_color)
        
        canvas = FigureCanvasTkAgg(fig, master=self.latex_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    app = AppGiaiTich()
    app.mainloop()