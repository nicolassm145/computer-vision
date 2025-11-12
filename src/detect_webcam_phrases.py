"""
Script de Detecção de LIBRAS com Formação de Frases
Autor: Nicolas
Data: 2025-11-12

Este script detecta letras LIBRAS em tempo real e forma frases automaticamente
quando uma letra é mantida por tempo suficiente com confiança alta.
"""

from ultralytics import YOLO
import cv2
from pathlib import Path
import numpy as np
import time
from collections import deque

class PhraseBuilder:
    """
    Classe para construir frases a partir de detecções de letras
    """
    
    def __init__(self, hold_time=2.0, confidence_threshold=0.65, stability_threshold=0.8):
        """
        Args:
            hold_time: Tempo em segundos que a letra deve ser mantida
            confidence_threshold: Confiança mínima para considerar detecção
            stability_threshold: Porcentagem de tempo que a letra deve aparecer
        """
        self.hold_time = hold_time
        self.confidence_threshold = confidence_threshold
        self.stability_threshold = stability_threshold
        
        # Estado atual
        self.current_letter = None
        self.detection_start_time = None
        self.detection_history = deque(maxlen=30)  # Últimos 30 frames (~1 segundo a 30fps)
        
        # Frase sendo construída
        self.phrase = ""
        self.last_added_time = 0
        self.cooldown = 0.5  # Tempo de espera após adicionar uma letra
        
    def reset_detection(self):
        """Reseta a detecção atual"""
        self.current_letter = None
        self.detection_start_time = None
        self.detection_history.clear()
    
    def update(self, detected_letter, confidence):
        """
        Atualiza o estado com uma nova detecção
        
        Args:
            detected_letter: Letra detectada (ou None)
            confidence: Confiança da detecção
            
        Returns:
            dict com informações do estado atual
        """
        current_time = time.time()
        
        # Adicionar à história
        if detected_letter and confidence >= self.confidence_threshold:
            self.detection_history.append(detected_letter)
        else:
            self.detection_history.append(None)
        
        # Verificar se estamos em cooldown
        if current_time - self.last_added_time < self.cooldown:
            return self._get_state()
        
        # Contar ocorrências na história recente
        if len(self.detection_history) > 0:
            letter_counts = {}
            for letter in self.detection_history:
                if letter:
                    letter_counts[letter] = letter_counts.get(letter, 0) + 1
            
            if letter_counts:
                # Letra mais comum na história recente
                most_common_letter = max(letter_counts, key=letter_counts.get)
                stability = letter_counts[most_common_letter] / len(self.detection_history)
                
                # Verificar estabilidade
                if stability >= self.stability_threshold:
                    # Se é uma nova letra, iniciar contagem
                    if self.current_letter != most_common_letter:
                        self.current_letter = most_common_letter
                        self.detection_start_time = current_time
                    
                    # Verificar se manteve tempo suficiente
                    if self.detection_start_time:
                        hold_duration = current_time - self.detection_start_time
                        
                        if hold_duration >= self.hold_time:
                            # Adicionar letra à frase
                            self.phrase += most_common_letter
                            self.last_added_time = current_time
                            self.reset_detection()
                            return self._get_state(letter_added=True)
                else:
                    # Não está estável, resetar
                    if self.current_letter != most_common_letter:
                        self.reset_detection()
            else:
                # Nenhuma detecção válida
                self.reset_detection()
        
        return self._get_state()
    
    def _get_state(self, letter_added=False):
        """Retorna o estado atual"""
        current_time = time.time()
        
        progress = 0.0
        if self.detection_start_time and self.current_letter:
            hold_duration = current_time - self.detection_start_time
            progress = min(hold_duration / self.hold_time, 1.0)
        
        stability = 0.0
        if len(self.detection_history) > 0:
            valid_count = sum(1 for x in self.detection_history if x == self.current_letter)
            stability = valid_count / len(self.detection_history)
        
        return {
            'phrase': self.phrase,
            'current_letter': self.current_letter,
            'progress': progress,
            'stability': stability,
            'letter_added': letter_added,
            'in_cooldown': (current_time - self.last_added_time) < self.cooldown
        }
    
    def add_space(self):
        """Adiciona um espaço à frase"""
        if self.phrase and not self.phrase.endswith(' '):
            self.phrase += ' '
            self.reset_detection()
    
    def backspace(self):
        """Remove a última letra"""
        if self.phrase:
            self.phrase = self.phrase[:-1]
            self.reset_detection()
    
    def clear(self):
        """Limpa a frase"""
        self.phrase = ""
        self.reset_detection()


def draw_ui(frame, state, confidence_threshold, hold_time):
    """
    Desenha a interface do usuário no frame
    
    Args:
        frame: Frame do vídeo
        state: Estado atual do PhraseBuilder
        confidence_threshold: Threshold de confiança
        hold_time: Tempo de hold necessário
    """
    height, width = frame.shape[:2]
    
    # Fundo semi-transparente para a UI
    overlay = frame.copy()
    
    # Área da frase (topo)
    cv2.rectangle(overlay, (10, 10), (width - 10, 120), (0, 0, 0), -1)
    
    # Área de status (meio-baixo)
    cv2.rectangle(overlay, (10, height - 150), (width - 10, height - 10), (0, 0, 0), -1)
    
    # Aplicar transparência
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    
    # Desenhar frase
    phrase_text = state['phrase'] if state['phrase'] else "[Comece a fazer sinais...]"
    cv2.putText(frame, "FRASE:", (20, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Quebrar frase em linhas se for muito longa
    max_chars_per_line = 40
    if len(phrase_text) > max_chars_per_line:
        line1 = phrase_text[:max_chars_per_line]
        line2 = phrase_text[max_chars_per_line:]
        cv2.putText(frame, line1, (20, 75), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
        cv2.putText(frame, line2, (20, 105), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
    else:
        cv2.putText(frame, phrase_text, (20, 75), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
    
    # Status atual
    y_pos = height - 130
    
    if state['current_letter']:
        # Letra sendo detectada
        letter_text = f"Detectando: {state['current_letter']}"
        cv2.putText(frame, letter_text, (20, y_pos), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), 2)
        
        # Barra de progresso
        progress = state['progress']
        bar_width = 400
        bar_height = 30
        bar_x = 20
        bar_y = y_pos + 15
        
        # Fundo da barra
        cv2.rectangle(frame, (bar_x, bar_y), 
                     (bar_x + bar_width, bar_y + bar_height), 
                     (100, 100, 100), -1)
        
        # Progresso
        progress_width = int(bar_width * progress)
        color = (0, 255, 0) if progress >= 1.0 else (0, 165, 255)  # Verde se completo, laranja se em progresso
        cv2.rectangle(frame, (bar_x, bar_y), 
                     (bar_x + progress_width, bar_y + bar_height), 
                     color, -1)
        
        # Texto do progresso
        progress_text = f"{progress*100:.0f}%"
        cv2.putText(frame, progress_text, (bar_x + bar_width + 10, bar_y + 22), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Estabilidade
        stability_text = f"Estabilidade: {state['stability']*100:.0f}%"
        cv2.putText(frame, stability_text, (20, bar_y + bar_height + 25), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Indicador de letra adicionada
    if state['letter_added']:
        cv2.putText(frame, "LETRA ADICIONADA!", (width // 2 - 150, height // 2), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)
    
    # Instruções (canto inferior direito)
    instructions = [
        "ESPACO - Adicionar espaco",
        "BACKSPACE - Apagar letra",
        "C - Limpar frase",
        "S - Salvar frase",
        "Q - Sair",
        f"+ /- Ajustar confianca ({confidence_threshold:.2f})",
        f"[ /] Ajustar tempo ({hold_time:.1f}s)"
    ]
    
    y = height - 130
    for i, instruction in enumerate(instructions):
        cv2.putText(frame, instruction, (width - 350, y + i * 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)


def detect_webcam_phrases(model_path=None, confidence=0.65, hold_time=2.0):
    """
    Detecta letras LIBRAS e forma frases automaticamente
    
    Args:
        model_path: Caminho para o modelo treinado
        confidence: Threshold de confiança para detecções (0-1)
        hold_time: Tempo em segundos para confirmar letra
    """
    print("=" * 60)
    print("DETECÇÃO DE LIBRAS COM FORMAÇÃO DE FRASES")
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
    
    # Criar construtor de frases
    phrase_builder = PhraseBuilder(
        hold_time=hold_time,
        confidence_threshold=confidence,
        stability_threshold=0.75
    )
    
    print("\n📹 Abrindo webcam...")
    # Abrir webcam (0 = webcam padrão)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ ERRO: Não foi possível abrir a webcam!")
        return
    
    # Configurar resolução da webcam
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    print("\n✅ Sistema ativado!")
    print("\n📝 Como usar:")
    print("   1. Faça uma letra em LIBRAS")
    print(f"   2. Mantenha por {hold_time}s com confiança > {confidence*100}%")
    print("   3. A letra será adicionada automaticamente à frase")
    print("   4. Continue para formar palavras e frases!")
    print("\n🎮 Controles:")
    print("   ESPAÇO    - Adicionar espaço (separar palavras)")
    print("   BACKSPACE - Apagar última letra")
    print("   C         - Limpar frase inteira")
    print("   S         - Salvar frase em arquivo")
    print("   Q         - Sair")
    print("   +/-       - Ajustar confiança mínima")
    print("   [/]       - Ajustar tempo de hold")
    print("\n" + "=" * 60)
    
    try:
        while True:
            # Ler frame da webcam
            ret, frame = cap.read()
            
            if not ret:
                print("❌ Erro ao capturar frame")
                break
            
            # Fazer predição
            results = model(frame, conf=confidence, verbose=False)
            
            # Processar detecção
            detected_letter = None
            max_confidence = 0
            
            if len(results[0].boxes) > 0:
                boxes = results[0].boxes
                confidences = boxes.conf.cpu().numpy()
                
                if len(confidences) > 0:
                    # Pegar a detecção com maior confiança
                    max_conf_idx = np.argmax(confidences)
                    max_confidence = confidences[max_conf_idx]
                    class_id = int(boxes.cls[max_conf_idx].cpu().numpy())
                    detected_letter = model.names[class_id]
            
            # Atualizar construtor de frases
            state = phrase_builder.update(detected_letter, max_confidence)
            
            # Desenhar detecções no frame
            annotated_frame = results[0].plot()
            
            # Desenhar UI
            draw_ui(annotated_frame, state, confidence, hold_time)
            
            # Mostrar frame
            cv2.imshow('LIBRAS - Formacao de Frases (Pressione Q para sair)', annotated_frame)
            
            # Processar teclas
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("\n👋 Encerrando...")
                break
            
            elif key == ord(' '):
                # Adicionar espaço
                phrase_builder.add_space()
                print(f"\n➕ Espaço adicionado: '{phrase_builder.phrase}'")
            
            elif key == 8 or key == 127:  # BACKSPACE
                # Apagar última letra
                phrase_builder.backspace()
                print(f"\n⌫ Letra apagada: '{phrase_builder.phrase}'")
            
            elif key == ord('c') or key == ord('C'):
                # Limpar frase
                phrase_builder.clear()
                print("\n🗑️  Frase limpa")
            
            elif key == ord('s') or key == ord('S'):
                # Salvar frase
                if phrase_builder.phrase:
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    filename = project_root / f"frase_{timestamp}.txt"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(phrase_builder.phrase)
                    print(f"\n💾 Frase salva: {filename}")
                    print(f"   Conteúdo: '{phrase_builder.phrase}'")
                else:
                    print("\n⚠️  Nenhuma frase para salvar")
            
            elif key == ord('+') or key == ord('='):
                # Aumentar confiança
                confidence = min(0.95, confidence + 0.05)
                phrase_builder.confidence_threshold = confidence
                print(f"\n🎯 Confiança: {confidence:.2f}")
            
            elif key == ord('-') or key == ord('_'):
                # Diminuir confiança
                confidence = max(0.3, confidence - 0.05)
                phrase_builder.confidence_threshold = confidence
                print(f"\n🎯 Confiança: {confidence:.2f}")
            
            elif key == ord('['):
                # Diminuir tempo de hold
                hold_time = max(0.5, hold_time - 0.5)
                phrase_builder.hold_time = hold_time
                print(f"\n⏱️  Tempo de hold: {hold_time:.1f}s")
            
            elif key == ord(']'):
                # Aumentar tempo de hold
                hold_time = min(5.0, hold_time + 0.5)
                phrase_builder.hold_time = hold_time
                print(f"\n⏱️  Tempo de hold: {hold_time:.1f}s")
            
            # Mostrar quando uma letra é adicionada
            if state['letter_added']:
                print(f"\n✅ Letra adicionada: {state['current_letter']}")
                print(f"   Frase atual: '{state['phrase']}'")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrompido pelo usuário")
    
    finally:
        # Liberar recursos
        cap.release()
        cv2.destroyAllWindows()
        
        # Mostrar frase final
        if phrase_builder.phrase:
            print("\n" + "=" * 60)
            print("📝 FRASE FINAL:")
            print("=" * 60)
            print(f"\n   {phrase_builder.phrase}\n")
            print("=" * 60)
        
        print("\n✅ Recursos liberados. Programa encerrado.")


if __name__ == "__main__":
    try:
        detect_webcam_phrases(confidence=0.65, hold_time=2.0)
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
