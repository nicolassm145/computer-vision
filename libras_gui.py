"""
Interface Gráfica Simples para Sistema de Reconhecimento de Libras
Usando Tkinter padrão (sem dependências extras)
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import threading
from ultralytics import YOLO
import time
from pathlib import Path
import numpy as np
from collections import deque

class LibrasGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Reconhecimento de Libras")
        self.root.geometry("1200x700")
        self.root.configure(bg='#2b2b2b')
        
        # Variáveis
        self.model = None
        self.cap = None
        self.is_recording = False
        self.frase_atual = ""
        self.ultimo_sinal = None
        self.tempo_ultimo_sinal = 0
        self.historico_deteccoes = deque(maxlen=15)
        
        # Configurações (ajustado para demorar mais)
        self.tempo_confirmacao = 6.0  # Aumentado de 4 para 6 segundos
        self.deteccoes_necessarias = 12  # Aumentado de 8 para 12 detecções
        self.confianca_minima = 0.70  # Aumentado de 0.65 para 0.70
        
        self.criar_interface()
        
    def criar_interface(self):
        """Cria a interface"""
        
        # Frame superior - Título
        frame_titulo = tk.Frame(self.root, bg='#1e1e1e', height=80)
        frame_titulo.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            frame_titulo,
            text="🤟 Sistema de Reconhecimento de Libras",
            font=('Arial', 20, 'bold'),
            bg='#1e1e1e',
            fg='white'
        ).pack(pady=20)
        
        # Frame principal
        frame_principal = tk.Frame(self.root, bg='#2b2b2b')
        frame_principal.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Coluna Esquerda - Vídeo
        frame_video = tk.LabelFrame(
            frame_principal,
            text="📹 Câmera",
            font=('Arial', 12, 'bold'),
            bg='#1e1e1e',
            fg='white',
            relief='ridge',
            bd=2
        )
        frame_video.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        self.label_video = tk.Label(
            frame_video,
            text="Câmera Desligada\nClique em 'Iniciar'",
            font=('Arial', 16),
            bg='#1e1e1e',
            fg='gray'
        )
        self.label_video.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Info do vídeo
        frame_info = tk.Frame(frame_video, bg='#1e1e1e')
        frame_info.pack(fill='x', padx=10, pady=5)
        
        self.label_fps = tk.Label(
            frame_info,
            text="FPS: --",
            font=('Arial', 10),
            bg='#1e1e1e',
            fg='lime'
        )
        self.label_fps.pack(side='left', padx=5)
        
        self.label_deteccao = tk.Label(
            frame_info,
            text="Detectando: ---",
            font=('Arial', 10),
            bg='#1e1e1e',
            fg='cyan'
        )
        self.label_deteccao.pack(side='left', padx=5)
        
        # Barra de progresso
        self.progress = ttk.Progressbar(
            frame_video,
            length=300,
            mode='determinate'
        )
        self.progress.pack(pady=5)
        
        self.label_progresso = tk.Label(
            frame_video,
            text="0/12 detecções",
            font=('Arial', 9),
            bg='#1e1e1e',
            fg='white'
        )
        self.label_progresso.pack(pady=2)
        
        # Coluna Direita - Controles e Frase
        frame_direita = tk.Frame(frame_principal, bg='#2b2b2b', width=400)
        frame_direita.pack(side='right', fill='both', padx=(5, 0))
        
        # Botões principais
        frame_botoes = tk.LabelFrame(
            frame_direita,
            text="Controles",
            font=('Arial', 12, 'bold'),
            bg='#1e1e1e',
            fg='white'
        )
        frame_botoes.pack(fill='x', pady=(0, 10))
        
        self.btn_modelo = tk.Button(
            frame_botoes,
            text="📂 Carregar Modelo",
            command=self.carregar_modelo,
            font=('Arial', 11),
            bg='#3a3a3a',
            fg='white',
            relief='raised',
            bd=2,
            padx=10,
            pady=8
        )
        self.btn_modelo.pack(fill='x', padx=10, pady=5)
        
        self.btn_camera = tk.Button(
            frame_botoes,
            text="▶ Iniciar Câmera",
            command=self.toggle_camera,
            font=('Arial', 11, 'bold'),
            bg='green',
            fg='white',
            relief='raised',
            bd=2,
            padx=10,
            pady=8
        )
        self.btn_camera.pack(fill='x', padx=10, pady=5)
        
        btn_testar = tk.Button(
            frame_botoes,
            text="🖼️ Testar Imagem",
            command=self.testar_imagem,
            font=('Arial', 11),
            bg='#3a3a3a',
            fg='white',
            relief='raised',
            bd=2,
            padx=10,
            pady=8
        )
        btn_testar.pack(fill='x', padx=10, pady=5)
        
        # Status
        self.label_status = tk.Label(
            frame_botoes,
            text="Status: Sem modelo carregado",
            font=('Arial', 9),
            bg='#1e1e1e',
            fg='orange'
        )
        self.label_status.pack(pady=5)
        
        frame_frase = tk.LabelFrame(
            frame_direita,
            text="📝 Frase Construída (Atalhos: ESPAÇO, BACKSPACE, Ctrl+S, Ctrl+L)",
            font=('Arial', 11, 'bold'),
            bg='#1e1e1e',
            fg='white'
        )
        frame_frase.pack(fill='both', expand=True, pady=(0, 10))
        
        # Caixa de texto (desabilitada para edição manual)
        self.text_frase = tk.Text(
            frame_frase,
            height=6,
            font=('Arial', 16),
            bg='#2d2d2d',
            fg='white',
            relief='sunken',
            bd=2,
            wrap='word',
            state='disabled'  # Desabilita edição manual
        )
        self.text_frase.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Botões da frase
        frame_controles_frase = tk.Frame(frame_frase, bg='#1e1e1e')
        frame_controles_frase.pack(fill='x', padx=10, pady=(0, 10))
        
        tk.Button(
            frame_controles_frase,
            text="⎵ Espaço",
            command=self.adicionar_espaco,
            bg='#3a7bc8',
            fg='white',
            font=('Arial', 10),
            relief='raised',
            bd=2,
            padx=10,
            pady=5
        ).pack(side='left', padx=2, expand=True, fill='x')
        
        tk.Button(
            frame_controles_frase,
            text="⌫ Apagar",
            command=self.backspace,
            bg='orange',
            fg='white',
            font=('Arial', 10),
            relief='raised',
            bd=2,
            padx=10,
            pady=5
        ).pack(side='left', padx=2, expand=True, fill='x')
        
        tk.Button(
            frame_controles_frase,
            text="🗑️ Limpar",
            command=self.limpar_frase,
            bg='red',
            fg='white',
            font=('Arial', 10),
            relief='raised',
            bd=2,
            padx=10,
            pady=5
        ).pack(side='left', padx=2, expand=True, fill='x')
        
        tk.Button(
            frame_controles_frase,
            text="💾 Salvar",
            command=self.salvar_frase,
            bg='green',
            fg='white',
            font=('Arial', 10),
            relief='raised',
            bd=2,
            padx=10,
            pady=5
        ).pack(side='left', padx=2, expand=True, fill='x')
        
        # Estatísticas
        frame_stats = tk.LabelFrame(
            frame_direita,
            text="📊 Estatísticas",
            font=('Arial', 12, 'bold'),
            bg='#1e1e1e',
            fg='white'
        )
        frame_stats.pack(fill='x')
        
        self.label_stats = tk.Label(
            frame_stats,
            text="Sinais detectados: 0\nFrases salvas: 0",
            font=('Arial', 10),
            bg='#1e1e1e',
            fg='white',
            justify='left'
        )
        self.label_stats.pack(padx=10, pady=10, anchor='w')
        
        # Teclas de atalho
        self.root.bind('<space>', lambda e: self.adicionar_espaco())
        self.root.bind('<BackSpace>', lambda e: self.backspace())
        self.root.bind('<Control-s>', lambda e: self.salvar_frase())
        self.root.bind('<Control-l>', lambda e: self.limpar_frase())
        self.root.bind('<Delete>', lambda e: self.limpar_frase())
        
    def carregar_modelo(self):
        """Carrega modelo"""
        arquivo = filedialog.askopenfilename(
            title="Selecione o modelo",
            filetypes=[("Modelo PyTorch", "*.pt")]
        )
        
        if arquivo:
            try:
                self.model = YOLO(arquivo)
                self.label_status.configure(
                    text=f"Status: Modelo carregado ✓",
                    fg='lime'
                )
                messagebox.showinfo("Sucesso", "Modelo carregado!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {str(e)}")
    
    def toggle_camera(self):
        """Liga/desliga câmera"""
        if not self.is_recording:
            if self.model is None:
                messagebox.showwarning("Aviso", "Carregue um modelo primeiro!")
                return
            
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Erro", "Não consegui abrir a câmera")
                return
            
            self.is_recording = True
            self.btn_camera.configure(text="⏸ Parar", bg='red')
            threading.Thread(target=self.processar_video, daemon=True).start()
        else:
            self.is_recording = False
            if self.cap:
                self.cap.release()
            self.btn_camera.configure(text="▶ Iniciar Câmera", bg='green')
            self.label_video.configure(text="Câmera Desligada")
    
    def processar_video(self):
        """Processa vídeo"""
        fps_time = time.time()
        frame_count = 0
        total_sinais = 0
        
        while self.is_recording:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            frame_count += 1
            if frame_count % 10 == 0:
                fps = 10 / (time.time() - fps_time)
                self.label_fps.configure(text=f"FPS: {fps:.1f}")
                fps_time = time.time()
            
            # Predição
            results = self.model.predict(
                source=frame,
                conf=0.5,
                verbose=False,
                imgsz=320
            )
            
            for result in results:
                annotated_frame = result.plot()
                boxes = result.boxes
                
                if len(boxes) > 0:
                    confs = boxes.conf.cpu().numpy()
                    max_conf_idx = np.argmax(confs)
                    
                    cls = int(boxes.cls[max_conf_idx])
                    conf = float(boxes.conf[max_conf_idx])
                    class_name = self.model.names[cls]
                    
                    self.label_deteccao.configure(
                        text=f"Detectando: {class_name} ({conf*100:.0f}%)"
                    )
                    
                    # Adiciona à frase
                    if self.adicionar_sinal_frase(class_name, conf):
                        self.atualizar_frase()
                        total_sinais += 1
                        self.label_stats.configure(
                            text=f"Sinais detectados: {total_sinais}\nFrases salvas: {len(self.frases_salvas) if hasattr(self, 'frases_salvas') else 0}"
                        )
                    
                    # Progresso
                    progresso = self.calcular_progresso()
                    self.progress['value'] = (progresso / self.deteccoes_necessarias) * 100
                    self.label_progresso.configure(
                        text=f"{progresso}/{self.deteccoes_necessarias} detecções"
                    )
                
                # Mostra frame
                frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                img = img.resize((640, 480), Image.Resampling.LANCZOS)
                imgtk = ImageTk.PhotoImage(image=img)
                
                self.label_video.configure(image=imgtk, text="")
                self.label_video.image = imgtk
    
    def normalizar_sinal(self, sinal):
        """Normaliza sinais detectados (ex: d1, d2 -> D)"""
        normalizacoes = {
            'd1': 'D',
            'd2': 'D',
            'D1': 'D',
            'D2': 'D',
            'd': 'D',
            # Adicione outras normalizações aqui se necessário
        }
        return normalizacoes.get(sinal, sinal)
    
    def adicionar_sinal_frase(self, sinal, confianca):
        """Adiciona sinal à frase"""
        tempo_atual = time.time()
        sinal_normalizado = self.normalizar_sinal(sinal)
        self.historico_deteccoes.append((sinal_normalizado, confianca, tempo_atual))
        
        sinais_recentes = [
            s for s, c, t in self.historico_deteccoes
            if tempo_atual - t < 2.0 and c >= self.confianca_minima  # Mudado de 1.5s para 2.0s
        ]
        
        if len(sinais_recentes) >= self.deteccoes_necessarias:
            sinal_mais_comum = max(set(sinais_recentes), key=sinais_recentes.count)
            
            if (self.ultimo_sinal != sinal_mais_comum or
                tempo_atual - self.tempo_ultimo_sinal > self.tempo_confirmacao):
                
                self.frase_atual += sinal_mais_comum
                self.ultimo_sinal = sinal_mais_comum
                self.tempo_ultimo_sinal = tempo_atual
                self.historico_deteccoes.clear()
                return True
        
        return False
    
    def calcular_progresso(self):
        """Calcula progresso"""
        tempo_atual = time.time()
        sinais_recentes = [
            s for s, c, t in self.historico_deteccoes
            if tempo_atual - t < 2.0 and c >= self.confianca_minima  # Mudado de 1.5s para 2.0s
        ]
        return len(sinais_recentes)
    
    def atualizar_frase(self):
        """Atualiza texto da frase"""
        self.text_frase.config(state='normal')  # Habilita edição
        self.text_frase.delete('1.0', 'end')
        self.text_frase.insert('1.0', self.frase_atual if self.frase_atual else "[Vazio]")
        self.text_frase.config(state='disabled')  # Desabilita edição manual
    
    def adicionar_espaco(self):
        """Adiciona espaço"""
        if self.frase_atual and not self.frase_atual.endswith(' '):
            self.frase_atual += ' '
            self.atualizar_frase()
        return 'break'  # Evita que o evento continue
    
    def backspace(self):
        """Remove último caractere"""
        if self.frase_atual:
            self.frase_atual = self.frase_atual[:-1]
            self.atualizar_frase()
        return 'break'  # Evita que o evento continue
    
    def limpar_frase(self):
        """Limpa frase"""
        self.frase_atual = ""
        self.ultimo_sinal = None
        self.historico_deteccoes.clear()
        self.atualizar_frase()
        return 'break'  # Evita que o evento continue
    
    def salvar_frase(self):
        """Salva frase"""
        if not self.frase_atual.strip():
            messagebox.showwarning("Aviso", "Frase vazia!")
            return
        
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open('frases_libras.txt', 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {self.frase_atual}\n")
        
        if not hasattr(self, 'frases_salvas'):
            self.frases_salvas = []
        self.frases_salvas.append(self.frase_atual)
        
        messagebox.showinfo("Sucesso", "Frase salva!")
        self.limpar_frase()
    
    def testar_imagem(self):
        """Testa em imagem"""
        if self.model is None:
            messagebox.showwarning("Aviso", "Carregue um modelo primeiro!")
            return
        
        arquivo = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png")]
        )
        
        if arquivo:
            self.model.predict(source=arquivo, conf=0.5, save=True)
            messagebox.showinfo("Teste", "Imagem processada!\nVeja: runs/detect/predict/")
    
    def run(self):
        """Inicia aplicação"""
        self.root.mainloop()


if __name__ == "__main__":
    app = LibrasGUI()
    app.run()