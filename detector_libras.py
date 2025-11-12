
"""
SISTEMA DE DETECÇÃO DE LINGUAGEM DE SINAIS LIBRAS
YOLOv11n + Webcam em Tempo Real

Instruções:
1. Execute este script
2. Posicione sua mão em frente à webcam
3. Faça gestos das letras do alfabeto LIBRAS
4. O sistema mostrará a letra detectada na tela
5. Pressione 'q' ou ESC para sair

"""

import cv2
import numpy as np
import os
import time
from typing import List, Tuple, Dict
from collections import Counter
from datetime import datetime

try:
    from ultralytics import YOLO
    USE_YOLO = True
except ImportError:
    print("Erro: Ultralytics não disponível. Instale com: pip install ultralytics")
    USE_YOLO = False
    exit(1)

class LibrasDetector:
    """Detector simplificado de LIBRAS usando YOLOv11"""
    
    def __init__(self, model_path: str, conf_threshold: float = 0.5):
        self.model_path = model_path
        self.conf_threshold = conf_threshold
        
        # 22 letras do alfabeto LIBRAS
        self.class_names = [
            'A', 'B', 'C', 'D1', 'D2', 'E', 'F', 'G', 
            'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 
            'R', 'S', 'T', 'U', 'V', 'W'
        ]
        
        # Carregar modelo
        self.model = YOLO(model_path)
        print(f"✓ Modelo carregado: {model_path}")
    
    def detect(self, image):
        """Detecta letras LIBRAS na imagem"""
        results = self.model(image, conf=self.conf_threshold, verbose=False)
        
        detections = []
        for result in results:
            if result.boxes is not None:
                boxes = result.boxes.xyxy.cpu().numpy()
                scores = result.boxes.conf.cpu().numpy()
                classes = result.boxes.cls.cpu().numpy().astype(int)
                
                for box, score, cls in zip(boxes, scores, classes):
                    x1, y1, x2, y2 = box.astype(int)
                    detections.append({
                        'letter': self.class_names[cls],
                        'confidence': float(score),
                        'bbox': (x1, y1, x2, y2)
                    })
        
        return detections
    
    def draw_detections(self, image, detections):
        """Desenha as detecções na imagem"""
        result_image = image.copy()
        
        for detection in detections:
            letter = detection['letter']
            confidence = detection['confidence']
            x1, y1, x2, y2 = detection['bbox']
            
            # Cor baseada na confiança (verde = alta, amarelo = média, vermelho = baixa)
            if confidence > 0.8:
                color = (0, 255, 0)  # Verde
            elif confidence > 0.6:
                color = (0, 255, 255)  # Amarelo
            else:
                color = (0, 100, 255)  # Laranja
            
            # Bounding box
            cv2.rectangle(result_image, (x1, y1), (x2, y2), color, 2)
            
            # Label
            label = f"{letter}: {confidence:.2f}"
            (text_width, text_height), baseline = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2
            )
            
            # Fundo do texto
            cv2.rectangle(
                result_image,
                (x1, y1 - text_height - baseline - 10),
                (x1 + text_width, y1),
                color,
                -1
            )
            
            # Texto
            cv2.putText(
                result_image,
                label,
                (x1, y1 - baseline - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )
        
        return result_image


class PhraseBuilder:
    """Constrói frases a partir das letras detectadas"""
    
    def __init__(self, stability_frames: int = 15, min_confidence: float = 0.7):
        self.phrase = ""
        self.candidate_letter = None
        self.candidate_count = 0
        self.stability_frames = stability_frames  # Quantos frames seguidos para confirmar
        self.min_confidence = min_confidence
        self.last_confirmed_time = 0
        self.cooldown_time = 1.5  # Segundos de espera após confirmar uma letra
        self.detection_history = []  # Histórico para votação
        
    def update(self, detections: List[Dict]) -> Tuple[str, bool, str]:
        """
        Atualiza o construtor de frases com novas detecções
        
        Returns:
            (letra_atual, letra_confirmada, progresso)
        """
        current_time = time.time()
        letra_confirmada = False
        current_letter = None
        
        # Filtrar detecções por confiança
        valid_detections = [d for d in detections if d['confidence'] >= self.min_confidence]
        
        if valid_detections and (current_time - self.last_confirmed_time) >= self.cooldown_time:
            # Pegar a letra com maior confiança
            best_detection = max(valid_detections, key=lambda x: x['confidence'])
            current_letter = best_detection['letter']
            
            # Adicionar ao histórico
            self.detection_history.append(current_letter)
            if len(self.detection_history) > self.stability_frames:
                self.detection_history.pop(0)
            
            # Verificar estabilidade usando votação
            if len(self.detection_history) >= self.stability_frames:
                # Contar ocorrências
                letter_counts = Counter(self.detection_history)
                most_common_letter, count = letter_counts.most_common(1)[0]
                
                # Se a letra mais comum aparece em pelo menos 80% dos frames
                if count >= int(self.stability_frames * 0.8):
                    if most_common_letter != self.candidate_letter:
                        self.candidate_letter = most_common_letter
                        self.candidate_count = count
                    else:
                        # Letra confirmada!
                        self.phrase += self.candidate_letter
                        letra_confirmada = True
                        self.last_confirmed_time = current_time
                        self.detection_history.clear()
                        self.candidate_letter = None
                        self.candidate_count = 0
        else:
            # Sem detecções válidas, resetar histórico
            if not valid_detections:
                self.detection_history.clear()
                self.candidate_letter = None
        
        # Calcular progresso
        progress = ""
        if self.candidate_letter and len(self.detection_history) > 0:
            progress_pct = int((len(self.detection_history) / self.stability_frames) * 100)
            progress = f"{self.candidate_letter} [{progress_pct}%]"
        
        return current_letter, letra_confirmada, progress
    
    def add_space(self):
        """Adiciona um espaço à frase"""
        if self.phrase and not self.phrase.endswith(" "):
            self.phrase += " "
    
    def backspace(self):
        """Remove o último caractere"""
        if self.phrase:
            self.phrase = self.phrase[:-1]
    
    def clear(self):
        """Limpa a frase inteira"""
        self.phrase = ""
        self.detection_history.clear()
        self.candidate_letter = None
    
    def save_to_file(self, filename: str = None) -> str:
        """Salva a frase em um arquivo"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"frase_libras_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.phrase)
        
        return filename

def main():
    """Função principal"""
    
    print("=" * 60)
    print("🤟 DETECTOR DE LIBRAS - CONSTRUTOR DE FRASES")
    print("=" * 60)
    
    # Encontrar modelo
    model_paths = ["best.pt", "runs/detect/train/weights/best.pt"]
    model_path = None
    
    for path in model_paths:
        if os.path.exists(path):
            model_path = path
            break
    
    if model_path is None:
        print("❌ Erro: Modelo não encontrado!")
        print("Execute primeiro: python train_model.py")
        return
    
    # Inicializar detector
    try:
        detector = LibrasDetector(model_path, conf_threshold=0.6)
    except Exception as e:
        print(f"❌ Erro ao carregar modelo: {e}")
        return
    
    # Inicializar construtor de frases
    phrase_builder = PhraseBuilder(stability_frames=15, min_confidence=0.7)
    
    # Inicializar webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Erro: Webcam não encontrada!")
        return
    
    # Configurar webcam
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    print("✓ Webcam conectada")
    print("✓ Sistema pronto!")
    print("\n📋 CONTROLES:")
    print("   ESPAÇO   - Adicionar espaço")
    print("   BACKSPACE - Apagar última letra")
    print("   C        - Limpar frase inteira")
    print("   S        - Salvar frase em arquivo")
    print("   Q ou ESC - Sair")
    print("\n🎯 COMO USAR:")
    print("   1. Faça o gesto da letra")
    print("   2. Mantenha o gesto estável por ~1 segundo")
    print("   3. A letra será adicionada automaticamente")
    print("=" * 60)
    
    # Variáveis para performance
    fps_counter = 0
    fps_time = time.time()
    fps_display = 0
    
    # Variáveis para feedback visual
    last_confirmed_letter = None
    confirmation_time = 0
    show_save_message = False
    save_message_time = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Espelhar horizontalmente
        frame = cv2.flip(frame, 1)
        
        # Detectar letras
        start_time = time.time()
        detections = detector.detect(frame)
        inference_time = (time.time() - start_time) * 1000
        
        # Atualizar construtor de frases
        current_letter, letra_confirmada, progress = phrase_builder.update(detections)
        
        # Feedback de confirmação
        if letra_confirmada:
            last_confirmed_letter = phrase_builder.phrase[-1] if phrase_builder.phrase else None
            confirmation_time = time.time()
        
        # Desenhar detecções
        result_frame = detector.draw_detections(frame, detections)
        
        # Calcular FPS
        fps_counter += 1
        if time.time() - fps_time >= 1.0:
            fps_display = fps_counter
            fps_counter = 0
            fps_time = time.time()
        
        # ==== INTERFACE NA TELA ====
        
        # Informações no topo
        info_y = 30
        info_texts = [
            f"FPS: {fps_display}",
            f"Deteccoes: {len(detections)}",
        ]
        
        for text in info_texts:
            cv2.putText(result_frame, text, (10, info_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            info_y += 25
        
        # Área de progresso (lado direito superior)
        if progress:
            progress_text = f"Capturando: {progress}"
            (text_w, text_h), _ = cv2.getTextSize(progress_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
            progress_x = result_frame.shape[1] - text_w - 20
            
            # Fundo laranja para destaque
            cv2.rectangle(result_frame, 
                         (progress_x - 10, 10),
                         (result_frame.shape[1] - 10, 50),
                         (0, 165, 255), -1)
            
            cv2.putText(result_frame, progress_text, (progress_x, 35),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Feedback de confirmação (flash verde quando confirma)
        if last_confirmed_letter and (time.time() - confirmation_time) < 0.5:
            confirm_text = f"✓ {last_confirmed_letter}"
            (text_w, text_h), _ = cv2.getTextSize(confirm_text, cv2.FONT_HERSHEY_SIMPLEX, 2, 3)
            confirm_x = (result_frame.shape[1] - text_w) // 2
            confirm_y = 150
            
            # Flash verde
            cv2.rectangle(result_frame,
                         (confirm_x - 20, confirm_y - text_h - 20),
                         (confirm_x + text_w + 20, confirm_y + 20),
                         (0, 255, 0), -1)
            
            cv2.putText(result_frame, confirm_text, (confirm_x, confirm_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        
        # Área da frase (parte inferior)
        phrase_area_height = 120
        phrase_area_y = result_frame.shape[0] - phrase_area_height
        
        # Fundo escuro semi-transparente
        overlay = result_frame.copy()
        cv2.rectangle(overlay, 
                     (0, phrase_area_y),
                     (result_frame.shape[1], result_frame.shape[0]),
                     (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, result_frame, 0.3, 0, result_frame)
        
        # Label "FRASE:"
        cv2.putText(result_frame, "FRASE:", (20, phrase_area_y + 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 100), 2)
        
        # Texto da frase
        phrase_text = phrase_builder.phrase if phrase_builder.phrase else "(vazia)"
        
        # Quebrar texto em múltiplas linhas se necessário
        max_chars_per_line = 50
        phrase_lines = []
        for i in range(0, len(phrase_text), max_chars_per_line):
            phrase_lines.append(phrase_text[i:i+max_chars_per_line])
        
        # Mostrar apenas as últimas 2 linhas
        phrase_lines = phrase_lines[-2:]
        
        phrase_y = phrase_area_y + 70
        for line in phrase_lines:
            cv2.putText(result_frame, line, (20, phrase_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 2)
            phrase_y += 35
        
        # Indicador de contagem de caracteres
        char_count = f"{len(phrase_builder.phrase)} letras"
        cv2.putText(result_frame, char_count, (result_frame.shape[1] - 150, phrase_area_y + 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1)
        
        # Mensagem de salvamento
        if show_save_message and (time.time() - save_message_time) < 2.0:
            save_text = "✓ Frase salva!"
            (text_w, text_h), _ = cv2.getTextSize(save_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
            save_x = (result_frame.shape[1] - text_w) // 2
            save_y = result_frame.shape[0] // 2
            
            cv2.rectangle(result_frame,
                         (save_x - 20, save_y - text_h - 20),
                         (save_x + text_w + 20, save_y + 20),
                         (0, 200, 0), -1)
            
            cv2.putText(result_frame, save_text, (save_x, save_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Controles na tela (canto inferior direito, acima da área da frase)
        controls_y = phrase_area_y - 100
        controls = [
            "ESPACO=espaco | BACK=apagar",
            "C=limpar | S=salvar | Q=sair"
        ]
        
        for i, control_text in enumerate(controls):
            (text_w, text_h), _ = cv2.getTextSize(control_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.putText(result_frame, control_text, 
                       (result_frame.shape[1] - text_w - 10, controls_y + i * 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # Mostrar resultado
        cv2.imshow("🤟 Detector LIBRAS - Construtor de Frases", result_frame)
        
        # Verificar teclas
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q') or key == 27:  # 'q' ou ESC
            break
        elif key == ord(' '):  # ESPAÇO
            phrase_builder.add_space()
        elif key == 8:  # BACKSPACE
            phrase_builder.backspace()
        elif key == ord('c') or key == ord('C'):  # C para limpar
            phrase_builder.clear()
        elif key == ord('s') or key == ord('S'):  # S para salvar
            if phrase_builder.phrase:
                filename = phrase_builder.save_to_file()
                print(f"\n✓ Frase salva em: {filename}")
                print(f"   Conteúdo: {phrase_builder.phrase}")
                show_save_message = True
                save_message_time = time.time()
    
    # Limpeza
    cap.release()
    cv2.destroyAllWindows()
    
    # Mostrar frase final
    print("\n" + "=" * 60)
    print("✓ Sistema finalizado!")
    if phrase_builder.phrase:
        print(f"\n📝 Frase final: {phrase_builder.phrase}")
        print(f"   ({len(phrase_builder.phrase)} caracteres)")
    else:
        print("\n(Nenhuma frase foi criada)")
    print("=" * 60)
   

if __name__ == "__main__":
    main()