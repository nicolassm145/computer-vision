
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
from typing import List, Tuple

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

def main():
    """Função principal"""
    
    
    # Encontrar modelo
    model_paths = ["best.pt", "runs/detect/train/weights/best.pt"]
    model_path = None
    
    for path in model_paths:
        if os.path.exists(path):
            model_path = path
            break
    
    if model_path is None:
      
        print(" Execute primeiro: python train_model.py")
        return
    
    # Inicializar detector
    try:
        detector = LibrasDetector(model_path)
    except Exception as e:
        print(f" Erro ao carregar modelo: {e}")
        return
    
    # Inicializar webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print(" Erro: Webcam não encontrada!")
        return
    
    # Configurar webcam
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    print("✓ Webcam conectada")
    print("✓ Sistema pronto!")
    print("\n📋 INSTRUÇÕES:")
    print("   • Posicione sua mão em frente à webcam")
    print("   • Faça gestos das letras LIBRAS")
    print("   • Pressione 'q' ou ESC para sair")
   
    
    # Variáveis para performance
    fps_counter = 0
    fps_time = time.time()
    fps_display = 0
    
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
        
        # Desenhar detecções
        result_frame = detector.draw_detections(frame, detections)
        
        # Calcular FPS
        fps_counter += 1
        if time.time() - fps_time >= 1.0:
            fps_display = fps_counter
            fps_counter = 0
            fps_time = time.time()
        
        # Informações na tela
        info_y = 30
        info_texts = [
            f"FPS: {fps_display}",
            f"Tempo: {inference_time:.1f}ms",
            f"Deteccoes: {len(detections)}",
            "Pressione 'q' para sair"
        ]
        
        for text in info_texts:
            cv2.putText(result_frame, text, (10, info_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            info_y += 25
        
        # Letras detectadas em destaque
        if detections:
            letters = [det['letter'] for det in detections]
            letters_text = f"LETRAS: {' | '.join(letters)}"
            
            # Posição na parte inferior
            text_size = cv2.getTextSize(letters_text, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)[0]
            text_x = (result_frame.shape[1] - text_size[0]) // 2
            text_y = result_frame.shape[0] - 30
            
            # Fundo preto para destaque
            cv2.rectangle(result_frame, 
                         (text_x - 10, text_y - text_size[1] - 10),
                         (text_x + text_size[0] + 10, text_y + 10),
                         (0, 0, 0), -1)
            
            # Texto em amarelo
            cv2.putText(result_frame, letters_text, (text_x, text_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)
        
        # Mostrar resultado
        cv2.imshow(" Detector LIBRAS - YOLOv11", result_frame)
        
        # Verificar teclas
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:  # 'q' ou ESC
            break
    
    # Limpeza
    cap.release()
    cv2.destroyAllWindows()
    print("\n✓ Sistema finalizado!")
   

if __name__ == "__main__":
    main()