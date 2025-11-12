"""
Script de Detecção em Tempo Real com Webcam
Autor: Nicolas
Data: 2025-11-11

Este script usa o modelo treinado para detectar letras LIBRAS
em tempo real através da webcam.
"""

from ultralytics import YOLO
import cv2
from pathlib import Path
import numpy as np

def detect_webcam(model_path=None, confidence=0.5):
    """
    Detecta letras LIBRAS em tempo real usando a webcam
    
    Args:
        model_path: Caminho para o modelo treinado
        confidence: Threshold de confiança para detecções (0-1)
    """
    print("=" * 60)
    print("DETECÇÃO EM TEMPO REAL - LIBRAS")
    print("=" * 60)
    
    project_root = Path(__file__).parent.parent
    
    # Se não foi especificado um modelo, usar o melhor modelo do treinamento
    if model_path is None:
        model_path = project_root / "runs" / "train" / "libras_yolo11n" / "weights" / "best.pt"
    
    print(f"\n💾 Carregando modelo: {model_path}")
    
    # Verificar se o modelo existe
    if not Path(model_path).exists():
        print(f"\n❌ ERRO: Modelo não encontrado!")
        print(f"   Esperado em: {model_path}")
        print("   Execute primeiro train.py para treinar o modelo.")
        return
    
    # Carregar modelo
    model = YOLO(str(model_path))
    
    print("\n📹 Abrindo webcam...")
    # Abrir webcam (0 = webcam padrão)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ ERRO: Não foi possível abrir a webcam!")
        return
    
    # Configurar resolução da webcam
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    print("\n✅ Webcam ativada!")
    print("\n📝 Instruções:")
    print("   - Mostre as letras em LIBRAS para a câmera")
    print("   - Pressione 'q' para sair")
    print("   - Pressione 's' para salvar um frame")
    print("   - Pressione '+' para aumentar confiança")
    print("   - Pressione '-' para diminuir confiança")
    print(f"\n🎯 Confiança atual: {confidence:.2f}")
    print("\n" + "=" * 60)
    
    frame_count = 0
    
    try:
        while True:
            # Ler frame da webcam
            ret, frame = cap.read()
            
            if not ret:
                print("❌ Erro ao capturar frame")
                break
            
            # Fazer predição
            results = model(frame, conf=confidence, verbose=False)
            
            # Desenhar resultados no frame
            annotated_frame = results[0].plot()
            
            # Adicionar informações no frame
            info_text = f"Confianca: {confidence:.2f} | FPS: {1000/(results[0].speed['inference']+results[0].speed['preprocess']+results[0].speed['postprocess']):.1f}"
            cv2.putText(annotated_frame, info_text, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Mostrar detecções
            if len(results[0].boxes) > 0:
                detections_text = f"Deteccoes: {len(results[0].boxes)}"
                cv2.putText(annotated_frame, detections_text, (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Mostrar a letra detectada com maior confiança
                boxes = results[0].boxes
                if len(boxes) > 0:
                    # Pegar a detecção com maior confiança
                    confidences = boxes.conf.cpu().numpy()
                    max_conf_idx = np.argmax(confidences)
                    class_id = int(boxes.cls[max_conf_idx].cpu().numpy())
                    conf_value = confidences[max_conf_idx]
                    letter = model.names[class_id]
                    
                    # Mostrar letra grande na tela
                    letter_text = f"Letra: {letter} ({conf_value:.2f})"
                    cv2.putText(annotated_frame, letter_text, (10, 100),
                               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
            
            # Mostrar frame
            cv2.imshow('LIBRAS Detection - Pressione Q para sair', annotated_frame)
            
            # Processar teclas
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("\n👋 Encerrando...")
                break
            elif key == ord('s'):
                # Salvar frame
                filename = f"detection_{frame_count}.jpg"
                cv2.imwrite(str(project_root / filename), annotated_frame)
                print(f"\n📸 Frame salvo: {filename}")
                frame_count += 1
            elif key == ord('+') or key == ord('='):
                # Aumentar confiança
                confidence = min(0.95, confidence + 0.05)
                print(f"\n🎯 Confiança: {confidence:.2f}")
            elif key == ord('-') or key == ord('_'):
                # Diminuir confiança
                confidence = max(0.05, confidence - 0.05)
                print(f"\n🎯 Confiança: {confidence:.2f}")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrompido pelo usuário")
    
    finally:
        # Liberar recursos
        cap.release()
        cv2.destroyAllWindows()
        print("\n✅ Recursos liberados. Programa encerrado.")

if __name__ == "__main__":
    try:
        detect_webcam(confidence=0.5)
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
