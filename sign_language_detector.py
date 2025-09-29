import cv2
import numpy as np
import os
import time
from typing import List, Tuple

# Verificar bibliotecas disponíveis
USE_ONNX = False
USE_ULTRALYTICS = False

try:
    import onnxruntime as ort
    USE_ONNX = True
    print("ONNX Runtime disponível")
except ImportError:
    print("ONNX Runtime não disponível")

try:
    from ultralytics import YOLO
    USE_ULTRALYTICS = True
    print("Ultralytics disponível")
except ImportError:
    print("Ultralytics não disponível")

class YOLOv11SignLanguageDetector:
    """
    Detector de linguagem de sinais usando YOLOv11 convertido para ONNX
    """
    
    def __init__(self, model_path: str, conf_threshold: float = 0.5, iou_threshold: float = 0.4):
        """
        Inicializa o detector
        
        Args:
            model_path: Caminho para o modelo (ONNX ou PyTorch)
            conf_threshold: Threshold de confiança para as detecções
            iou_threshold: Threshold de IoU para Non-Maximum Suppression
        """
        self.model_path = model_path
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        
        # Classes do dataset LIBRAS
        self.class_names = [
            'A', 'B', 'C', 'D1', 'D2', 'E', 'F', 'G', 
            'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 
            'R', 'S', 'T', 'U', 'V', 'W'
        ]
        
        # Cores para cada classe (BGR)
        self.colors = self._generate_colors(len(self.class_names))
        
        # Determinar qual tipo de modelo usar
        self.use_onnx = model_path.endswith('.onnx') and USE_ONNX
        self.use_ultralytics = model_path.endswith('.pt') and USE_ULTRALYTICS
        
        if self.use_onnx:
            self._init_onnx_session()
        elif self.use_ultralytics:
            self._init_ultralytics_model()
        else:
            raise ValueError("Modelo não suportado ou bibliotecas não disponíveis")
        
    def _generate_colors(self, num_classes: int) -> List[Tuple[int, int, int]]:
        """Gera cores únicas para cada classe"""
        colors = []
        for i in range(num_classes):
            hue = int(180 * i / num_classes)
            color = cv2.cvtColor(np.uint8([[[hue, 255, 255]]]), cv2.COLOR_HSV2BGR)[0][0]
            colors.append((int(color[0]), int(color[1]), int(color[2])))
        return colors
    
    def _init_ultralytics_model(self):
        """Inicializa modelo Ultralytics YOLO"""
        try:
            self.model = YOLO(self.model_path)
            print(f"Modelo Ultralytics carregado com sucesso!")
            print(f"Modelo: {self.model_path}")
        except Exception as e:
            print(f"Erro ao carregar modelo Ultralytics: {e}")
            raise
    
    def _init_onnx_session(self):
        """Inicializa a sessão ONNX Runtime"""
        try:
            # Configurar providers (CPU ou GPU)
            providers = ['CPUExecutionProvider']
            
            # Tentar usar GPU se disponível
            if ort.get_device() == 'GPU':
                providers.insert(0, 'CUDAExecutionProvider')
            
            self.session = ort.InferenceSession(self.model_path, providers=providers)
            
            # Obter informações do modelo
            self.input_name = self.session.get_inputs()[0].name
            self.input_shape = self.session.get_inputs()[0].shape
            self.output_name = self.session.get_outputs()[0].name
            
            print(f"Modelo ONNX carregado com sucesso!")
            print(f"Input shape: {self.input_shape}")
            print(f"Provider ativo: {self.session.get_providers()}")
            
        except Exception as e:
            print(f"Erro ao carregar modelo ONNX: {e}")
            raise
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Pré-processa a imagem para o modelo
        
        Args:
            image: Imagem original (BGR)
            
        Returns:
            Imagem pré-processada para o modelo
        """
        # Redimensionar mantendo aspect ratio
        input_height, input_width = self.input_shape[2], self.input_shape[3]
        
        # Calcular padding
        h, w = image.shape[:2]
        scale = min(input_width / w, input_height / h)
        new_w, new_h = int(w * scale), int(h * scale)
        
        # Redimensionar
        resized = cv2.resize(image, (new_w, new_h))
        
        # Padding
        padded = np.full((input_height, input_width, 3), 114, dtype=np.uint8)
        padded[:new_h, :new_w] = resized
        
        # Converter para RGB e normalizar
        padded = cv2.cvtColor(padded, cv2.COLOR_BGR2RGB)
        padded = padded.astype(np.float32) / 255.0
        
        # Transpor para formato do modelo (1, 3, H, W)
        padded = np.transpose(padded, (2, 0, 1))
        padded = np.expand_dims(padded, axis=0)
        
        return padded, scale, (new_w, new_h)
    
    def postprocess_detections(self, outputs: np.ndarray, scale: float, 
                             original_shape: Tuple[int, int]) -> List[dict]:
        """
        Pós-processa as detecções do modelo
        
        Args:
            outputs: Saídas do modelo
            scale: Escala usada no pré-processamento
            original_shape: Forma original da imagem (w, h)
            
        Returns:
            Lista de detecções processadas
        """
        detections = []
        
        # outputs shape: (1, num_detections, 5 + num_classes)
        predictions = outputs[0]  # Remove batch dimension
        
        for detection in predictions:
            # Extrair coordenadas e confiança
            x_center, y_center, width, height = detection[:4]
            confidence_scores = detection[4:]
            
            # Encontrar a classe com maior confiança
            class_id = np.argmax(confidence_scores)
            confidence = confidence_scores[class_id]
            
            if confidence >= self.conf_threshold:
                # Converter coordenadas para formato original
                x_center /= scale
                y_center /= scale
                width /= scale
                height /= scale
                
                # Calcular coordenadas da bounding box
                x1 = int(x_center - width / 2)
                y1 = int(y_center - height / 2)
                x2 = int(x_center + width / 2)
                y2 = int(y_center + height / 2)
                
                # Garantir que as coordenadas estão dentro dos limites
                x1 = max(0, min(x1, original_shape[0]))
                y1 = max(0, min(y1, original_shape[1]))
                x2 = max(0, min(x2, original_shape[0]))
                y2 = max(0, min(y2, original_shape[1]))
                
                detections.append({
                    'class_id': int(class_id),
                    'class_name': self.class_names[class_id],
                    'confidence': float(confidence),
                    'bbox': (x1, y1, x2, y2)
                })
        
        # Aplicar Non-Maximum Suppression
        return self._apply_nms(detections)
    
    def _apply_nms(self, detections: List[dict]) -> List[dict]:
        """Aplica Non-Maximum Suppression"""
        if not detections:
            return []
        
        # Converter para formato OpenCV
        boxes = []
        scores = []
        
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            boxes.append([x1, y1, x2 - x1, y2 - y1])
            scores.append(det['confidence'])
        
        boxes = np.array(boxes, dtype=np.float32)
        scores = np.array(scores, dtype=np.float32)
        
        # Aplicar NMS
        indices = cv2.dnn.NMSBoxes(boxes, scores, self.conf_threshold, self.iou_threshold)
        
        if len(indices) > 0:
            indices = indices.flatten()
            return [detections[i] for i in indices]
        
        return []
    
    def detect(self, image: np.ndarray) -> List[dict]:
        """
        Realiza detecção na imagem
        
        Args:
            image: Imagem de entrada (BGR)
            
        Returns:
            Lista de detecções
        """
        if self.use_ultralytics:
            return self._detect_ultralytics(image)
        elif self.use_onnx:
            return self._detect_onnx(image)
        else:
            raise ValueError("Nenhum modelo disponível")
    
    def _detect_ultralytics(self, image: np.ndarray) -> List[dict]:
        """Detecção usando Ultralytics YOLO"""
        results = self.model(image, conf=self.conf_threshold, iou=self.iou_threshold, verbose=False)
        
        detections = []
        for result in results:
            if result.boxes is not None:
                boxes = result.boxes.xyxy.cpu().numpy()  # x1, y1, x2, y2
                scores = result.boxes.conf.cpu().numpy()
                classes = result.boxes.cls.cpu().numpy().astype(int)
                
                for box, score, cls in zip(boxes, scores, classes):
                    if score >= self.conf_threshold:
                        x1, y1, x2, y2 = box.astype(int)
                        detections.append({
                            'class_id': int(cls),
                            'class_name': self.class_names[cls],
                            'confidence': float(score),
                            'bbox': (x1, y1, x2, y2)
                        })
        
        return detections
    
    def _detect_onnx(self, image: np.ndarray) -> List[dict]:
        """Detecção usando ONNX"""
        # Pré-processamento
        processed_image, scale, _ = self.preprocess_image(image)
        
        # Inferência
        outputs = self.session.run([self.output_name], {self.input_name: processed_image})
        
        # Pós-processamento
        detections = self.postprocess_detections(outputs[0], scale, image.shape[1::-1])
        
        return detections
    
    def draw_detections(self, image: np.ndarray, detections: List[dict]) -> np.ndarray:
        """
        Desenha as detecções na imagem
        
        Args:
            image: Imagem original
            detections: Lista de detecções
            
        Returns:
            Imagem com detecções desenhadas
        """
        result_image = image.copy()
        
        for detection in detections:
            class_id = detection['class_id']
            class_name = detection['class_name']
            confidence = detection['confidence']
            x1, y1, x2, y2 = detection['bbox']
            
            # Cor da classe
            color = self.colors[class_id]
            
            # Desenhar bounding box
            cv2.rectangle(result_image, (x1, y1), (x2, y2), color, 2)
            
            # Preparar texto
            label = f"{class_name}: {confidence:.2f}"
            
            # Calcular tamanho do texto
            (text_width, text_height), baseline = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
            )
            
            # Desenhar fundo do texto
            cv2.rectangle(
                result_image,
                (x1, y1 - text_height - baseline - 10),
                (x1 + text_width, y1),
                color,
                -1
            )
            
            # Desenhar texto
            cv2.putText(
                result_image,
                label,
                (x1, y1 - baseline - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )
        
        return result_image


def main():
    """Função principal para teste do detector"""
    
    # Configurações - tentar modelos disponíveis
    model_paths = [
        "best.onnx",
        "best.pt", 
        "runs/detect/train/weights/best.pt"
    ]
    
    model_path = None
    for path in model_paths:
        if os.path.exists(path):
            model_path = path
            break
    
    if model_path is None:
        print("Erro: Nenhum modelo encontrado!")
        print("Modelos procurados:")
        for path in model_paths:
            print(f"  - {path}")
        print("\nExecute primeiro o script train_model.py para treinar o modelo.")
        return
    
    print(f"Usando modelo: {model_path}")
    
    # Inicializar detector
    try:
        detector = YOLOv11SignLanguageDetector(model_path)
    except Exception as e:
        print(f"Erro ao inicializar detector: {e}")
        return
    
    # Inicializar webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Erro: Não foi possível abrir a webcam!")
        return
    
    # Configurar webcam
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    print("Pressione 'q' para sair ou 'ESC' para fechar")
    print("Detector de Linguagem de Sinais - LIBRAS iniciado!")
    
    # Variáveis para FPS
    fps_counter = 0
    fps_time = time.time()
    fps_display = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar frame da webcam!")
            break
        
        # Espelhar horizontalmente (mais natural para o usuário)
        frame = cv2.flip(frame, 1)
        
        # Detectar sinais
        start_time = time.time()
        detections = detector.detect(frame)
        inference_time = time.time() - start_time
        
        # Desenhar detecções
        result_frame = detector.draw_detections(frame, detections)
        
        # Calcular FPS
        fps_counter += 1
        if time.time() - fps_time >= 1.0:
            fps_display = fps_counter
            fps_counter = 0
            fps_time = time.time()
        
        # Adicionar informações na tela
        info_text = [
            f"FPS: {fps_display}",
            f"Inferencia: {inference_time*1000:.1f}ms",
            f"Deteccoes: {len(detections)}",
            "Pressione 'q' para sair"
        ]
        
        for i, text in enumerate(info_text):
            cv2.putText(
                result_frame,
                text,
                (10, 30 + i * 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )
        
        # Exibir letras detectadas em destaque
        if detections:
            detected_letters = [det['class_name'] for det in detections]
            letters_text = f"Letras: {', '.join(detected_letters)}"
            
            # Fundo para o texto das letras
            (text_width, text_height), baseline = cv2.getTextSize(
                letters_text, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3
            )
            
            cv2.rectangle(
                result_frame,
                (10, result_frame.shape[0] - text_height - baseline - 20),
                (text_width + 20, result_frame.shape[0] - 10),
                (0, 0, 0),
                -1
            )
            
            cv2.putText(
                result_frame,
                letters_text,
                (15, result_frame.shape[0] - baseline - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0, 255, 255),
                3
            )
        
        # Exibir frame
        cv2.imshow("Detector de Linguagem de Sinais - LIBRAS", result_frame)
        
        # Verificar teclas
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:  # 'q' ou ESC
            break
    
    # Limpeza
    cap.release()
    cv2.destroyAllWindows()
    print("Detector finalizado!")


if __name__ == "__main__":
    import os
    main()