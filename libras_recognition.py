"""
Sistema Completo de Reconhecimento de Libras usando YOLOv8
Com construção de frases e normalização de sinais
"""

from ultralytics import YOLO
import cv2
import yaml
from pathlib import Path
import time
from collections import deque
import numpy as np

class LibrasRecognizer:
    def __init__(self):
        """Inicializa o reconhecedor"""
        self.model = None
        self.dataset_path = None
        
        # Sistema de construção de frases MELHORADO
        self.frase_atual = ""  # Agora é string, não lista
        self.ultimo_sinal = None
        self.tempo_ultimo_sinal = 0
        self.tempo_confirmacao = 4.0  # 4 segundos para confirmar (mais lento)
        self.historico_deteccoes = deque(maxlen=15)  # aumentado para 15
        self.confianca_minima_frase = 0.65  # confiança maior
        self.deteccoes_necessarias = 8  # precisa de 8 detecções (antes eram 5)
        
    def normalizar_sinal(self, sinal):
        """
        Normaliza sinais detectados (ex: d1, d2 -> d)
        """
        # Dicionário de normalizações
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
        """
        Adiciona um sinal à frase com sistema de confirmação MELHORADO
        """
        tempo_atual = time.time()
        sinal_normalizado = self.normalizar_sinal(sinal)
        
        # Adiciona ao histórico
        self.historico_deteccoes.append((sinal_normalizado, confianca, tempo_atual))
        
        # Verifica se o sinal está sendo detectado consistentemente
        sinais_recentes = [s for s, c, t in self.historico_deteccoes 
                          if tempo_atual - t < 1.5 and c >= self.confianca_minima_frase]
        
        if len(sinais_recentes) >= self.deteccoes_necessarias:  # Precisa de mais detecções
            sinal_mais_comum = max(set(sinais_recentes), key=sinais_recentes.count)
            
            # Verifica se é um sinal novo ou se passou tempo suficiente
            if (self.ultimo_sinal != sinal_mais_comum or 
                tempo_atual - self.tempo_ultimo_sinal > self.tempo_confirmacao):
                
                # Adiciona SEM ESPAÇO à string
                self.frase_atual += sinal_mais_comum
                self.ultimo_sinal = sinal_mais_comum
                self.tempo_ultimo_sinal = tempo_atual
                self.historico_deteccoes.clear()
                return True
        
        return False
    
    def limpar_frase(self):
        """Limpa a frase atual"""
        self.frase_atual = ""
        self.ultimo_sinal = None
        self.tempo_ultimo_sinal = 0
        self.historico_deteccoes.clear()
    
    def remover_ultimo_caractere(self):
        """Remove o último caractere da frase (backspace)"""
        if self.frase_atual:
            self.frase_atual = self.frase_atual[:-1]
            self.ultimo_sinal = None
            return True
        return False
    
    def adicionar_espaco(self):
        """Adiciona um espaço na frase"""
        if self.frase_atual and not self.frase_atual.endswith(' '):
            self.frase_atual += ' '
            return True
        return False
    
    def obter_frase(self):
        """Retorna a frase atual como string"""
        return self.frase_atual if self.frase_atual else "[Frase vazia]"
    
    def salvar_frase(self, arquivo='frases_libras.txt'):
        """Salva a frase em um arquivo"""
        if self.frase_atual and self.frase_atual != "":
            with open(arquivo, 'a', encoding='utf-8') as f:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] {self.frase_atual}\n")
            return True
        return False
        
    def verificar_dataset(self, dataset_path='dataset'):
        """
        Verifica se o dataset está na estrutura correta
        
        Estrutura esperada:
        dataset/
        ├── train/
        │   ├── images/
        │   └── labels/
        ├── valid/
        │   ├── images/
        │   └── labels/
        ├── test/ (opcional)
        │   ├── images/
        │   └── labels/
        └── data.yaml
        """
        dataset_path = Path(dataset_path)
        self.dataset_path = dataset_path
        
        print("=== Verificando estrutura do dataset ===\n")
        
        folders = ['train', 'valid']
        for folder in folders:
            folder_path = dataset_path / folder
            if folder_path.exists():
                print(f"✓ Pasta '{folder}' encontrada")
                
                images_path = folder_path / 'images'
                labels_path = folder_path / 'labels'
                
                if not images_path.exists():
                    print(f"  ⚠ AVISO: Pasta 'images' não encontrada em {folder}")
                    print(f"  → Verifique se as imagens estão em: {images_path}")
                else:
                    num_images = len(list(images_path.glob('*')))
                    print(f"  → {num_images} imagens em {folder}/images")
                
                if not labels_path.exists():
                    print(f"  ⚠ AVISO: Pasta 'labels' não encontrada em {folder}")
                    print(f"  → Verifique se os labels estão em: {labels_path}")
                else:
                    num_labels = len(list(labels_path.glob('*.txt')))
                    print(f"  → {num_labels} arquivos de label em {folder}/labels")
            else:
                print(f"✗ Pasta '{folder}' NÃO encontrada")
        
        yaml_path = dataset_path / 'data.yaml'
        if yaml_path.exists():
            print(f"\n✓ Arquivo 'data.yaml' encontrado")
            with open(yaml_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                print(f"  → Classes: {config.get('names', 'não especificado')}")
                print(f"  → Número de classes: {config.get('nc', 'não especificado')}")
        else:
            print(f"\n✗ Arquivo 'data.yaml' NÃO encontrado")
            print(f"  → Precisa estar em: {yaml_path}")
        
        print("\n" + "="*50 + "\n")
        return yaml_path if yaml_path.exists() else None
    
    def corrigir_yaml(self, yaml_path='dataset/data.yaml'):
        """
        Corrige os caminhos no data.yaml para funcionarem corretamente
        """
        yaml_path = Path(yaml_path)
        
        if not yaml_path.exists():
            print(f"❌ Arquivo {yaml_path} não encontrado!")
            return False
        
        print("📝 Lendo data.yaml...")
        with open(yaml_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        dataset_dir = yaml_path.parent.absolute()
        
        config['path'] = str(dataset_dir)
        config['train'] = 'train/images'
        config['val'] = 'valid/images'
        
        if (dataset_dir / 'test').exists():
            config['test'] = 'test/images'
        
        print("💾 Salvando correções no data.yaml...")
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
        
        print("✅ Arquivo data.yaml corrigido com sucesso!")
        print(f"   Path: {config['path']}")
        print(f"   Classes: {config.get('names', {})}")
        return True
    
    def treinar(self, yaml_path='dataset/data.yaml', epochs=100, imgsz=640, 
                batch=16, model_size='n', resume=False, device_choice=None):
        """
        Treina o modelo YOLOv8
        """
        print("="*50)
        print("🚀 INICIANDO TREINAMENTO")
        print("="*50)
        
        if resume:
            last_model = 'runs/detect/libras_yolo2/weights/last.pt'
            if Path(last_model).exists():
                print(f"\n♻️  CONTINUANDO treinamento anterior de: {last_model}")
                self.model = YOLO(last_model)
                model_name = last_model
            else:
                print(f"\n⚠️  Modelo anterior não encontrado em {last_model}")
                print("   Iniciando treinamento do zero...\n")
                model_name = f'yolov8{model_size}.pt'
                self.model = YOLO(model_name)
        else:
            model_name = f'yolov8{model_size}.pt'
            print(f"\n📦 Carregando modelo base: {model_name}")
            self.model = YOLO(model_name)
        
        print(f"\n⚙️  Configurações:")
        print(f"   - Épocas: {epochs}")
        print(f"   - Tamanho imagem: {imgsz}")
        print(f"   - Batch size: {batch}")
        print(f"   - Modelo: {model_name}")
        
        print(f"\n🏋️  Iniciando treinamento...\n")
        
        import torch
        if device_choice == 'cpu':
            device = 'cpu'
        elif device_choice == 'gpu':
            device = '0' if torch.cuda.is_available() else 'cpu'
        else:
            device = '0' if torch.cuda.is_available() else 'cpu'
        print(f"   - Dispositivo: {device} ({'GPU CUDA' if device == '0' else 'CPU'})")
        if device == 'cpu':
            print("\n⚠️  AVISO: Usando CPU (será mais lento)")
            print("   Para usar GPU, instale: pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118\n")
        
        try:
            results = self.model.train(
                data=yaml_path,
                epochs=epochs,
                imgsz=imgsz,
                batch=batch,
                name='libras_yolo',
                patience=50,
                save=True,
                device=device,
                verbose=True,
                pretrained=True,
                optimizer='auto',
                seed=42,
                plots=True
            )
            
            print("\n" + "="*50)
            print("✅ TREINAMENTO CONCLUÍDO!")
            print("="*50)
            print(f"\n📊 Resultados salvos em: runs/detect/libras_yolo2/")
            print(f"💾 Melhor modelo salvo em: runs/detect/libras_yolo2/weights/best.pt")
            
            return results
            
        except Exception as e:
            print(f"\n❌ Erro durante o treinamento: {e}")
            print("\n💡 Dicas:")
            print("   - Reduza o batch size se tiver erro de memória")
            print("   - Verifique se o data.yaml está correto")
            print("   - Confirme que as pastas train/valid existem")
            return None
    
    def validar(self, model_path='runs/detect/libras_yolo2/weights/best.pt'):
        """
        Valida o modelo treinado
        """
        print("🔍 Validando modelo...\n")
        
        if self.model is None:
            self.model = YOLO(model_path)
        
        results = self.model.val()
        
        print("\n📊 Métricas de Validação:")
        print(f"   - mAP50: {results.box.map50:.4f}")
        print(f"   - mAP50-95: {results.box.map:.4f}")
        print(f"   - Precisão: {results.box.mp:.4f}")
        print(f"   - Recall: {results.box.mr:.4f}")
        
        return results
    
    def testar_imagem(self, image_path, model_path='runs/detect/libras_yolo2/weights/best.pt',
                     conf_threshold=0.25, device_choice=None):
        """
        Testa o modelo em uma imagem
        """
        print(f"🖼️  Testando imagem: {image_path}")
        
        import torch
        if device_choice == 'cpu':
            device = 'cpu'
        elif device_choice == 'gpu':
            device = '0' if torch.cuda.is_available() else 'cpu'
        else:
            device = '0' if torch.cuda.is_available() else 'cpu'
        if self.model is None:
            self.model = YOLO(model_path)

        results = self.model.predict(
            source=image_path,
            conf=conf_threshold,
            save=True,
            show_labels=True,
            show_conf=True,
            device=device
        )
        
        for result in results:
            boxes = result.boxes
            if len(boxes) > 0:
                print(f"\n✅ Detectados {len(boxes)} sinais:")
                for box in boxes:
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    class_name = self.model.names[cls]
                    class_normalizado = self.normalizar_sinal(class_name)
                    print(f"   - {class_name} → {class_normalizado}: {conf*100:.1f}% confiança")
            else:
                print("\n❌ Nenhum sinal detectado")
        
        print(f"\n💾 Resultado salvo em: runs/detect/predict/")
        return results
    
    def reconhecer_webcam(self, model_path='runs/detect/libras_yolo2/weights/best.pt',
                         conf_threshold=0.5, device_choice=None, imgsz=320):
        """
        Reconhecimento em tempo real via webcam COM construção de frases
        OTIMIZADO para melhor performance
        """
        import torch
        if device_choice == 'cpu':
            device = 'cpu'
        elif device_choice == 'gpu':
            device = '0' if torch.cuda.is_available() else 'cpu'
        else:
            device = '0' if torch.cuda.is_available() else 'cpu'
        if self.model is None:
            self.model = YOLO(model_path)
        
        cap = cv2.VideoCapture(0)
        
        # Otimizações da webcam
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduz buffer
        
        print("\n" + "="*50)
        print("📹 RECONHECIMENTO EM TEMPO REAL COM CONSTRUÇÃO DE FRASES")
        print("="*50)
        print("CONTROLES:")
        print("  'q' - Sair")
        print("  's' - Salvar screenshot")
        print("  'c' - Limpar frase inteira")
        print("  'BACKSPACE' - Apagar último caractere")
        print("  'ESPAÇO' - Adicionar espaço entre palavras")
        print("  'f' - Salvar frase em arquivo")
        print("  '+' / '-' - Aumentar/diminuir tamanho processamento")
        print("="*50)
        print(f"⚙️  Tempo de confirmação: {self.tempo_confirmacao}s")
        print(f"⚙️  Detecções necessárias: {self.deteccoes_necessarias}")
        print(f"⚙️  Confiança mínima: {self.confianca_minima_frase}")
        print(f"💡 Dica: Segure o sinal por ~{self.tempo_confirmacao}s para confirmar")
        print("="*50 + "\n")
        
        screenshot_count = 0
        frame_count = 0
        fps_time = time.time()
        fps = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Erro ao capturar frame da webcam")
                break
            
            # Calcular FPS
            frame_count += 1
            if frame_count % 10 == 0:
                fps = 10 / (time.time() - fps_time)
                fps_time = time.time()
            
            # Fazer predição com tamanho reduzido
            results = self.model.predict(
                source=frame,
                conf=conf_threshold,
                verbose=False,
                stream=True,
                device=device,
                imgsz=imgsz,  # Tamanho menor = mais rápido
                half=True if device == '0' else False,  # FP16 na GPU
                agnostic_nms=True  # NMS mais rápido
            )
            
            # Processar e desenhar resultados
            for result in results:
                annotated_frame = result.plot()
                boxes = result.boxes
                
                # Processar detecções para construção de frase
                if len(boxes) > 0:
                    # Pega a detecção com maior confiança
                    confs = boxes.conf.cpu().numpy()
                    max_conf_idx = np.argmax(confs)
                    
                    cls = int(boxes.cls[max_conf_idx])
                    conf = float(boxes.conf[max_conf_idx])
                    class_name = self.model.names[cls]
                    
                    # Adiciona à frase se confirmado
                    if self.adicionar_sinal_frase(class_name, conf):
                        print(f"✅ Sinal confirmado: '{self.normalizar_sinal(class_name)}'")
                        print(f"📝 Frase atual: '{self.frase_atual}'")
                    
                    # Mostrar detecção atual e progresso
                    class_normalizado = self.normalizar_sinal(class_name)
                    
                    # Calcular progresso (quantas detecções faltam)
                    sinais_recentes = [s for s, c, t in self.historico_deteccoes 
                                      if time.time() - t < 1.5 and c >= self.confianca_minima_frase]
                    progresso = len(sinais_recentes)
                    
                    cv2.putText(
                        annotated_frame,
                        f"Detectando: {class_normalizado} ({conf*100:.1f}%)",
                        (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0,
                        (255, 255, 0),
                        2
                    )
                    
                    # Barra de progresso
                    cv2.putText(
                        annotated_frame,
                        f"Progresso: {progresso}/{self.deteccoes_necessarias}",
                        (10, 120),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (255, 165, 0),
                        2
                    )
                    
                    # Barra visual
                    barra_largura = int(200 * progresso / self.deteccoes_necessarias)
                    cv2.rectangle(annotated_frame, (10, 130), (210, 150), (100, 100, 100), 2)
                    if barra_largura > 0:
                        cv2.rectangle(annotated_frame, (10, 130), (10 + barra_largura, 150), 
                                    (0, 255, 0), -1)
                
                # Mostrar FPS
                cv2.putText(
                    annotated_frame,
                    f"FPS: {fps:.1f}",
                    (10, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )
                
                # Desenhar área de frase
                altura_frame = annotated_frame.shape[0]
                largura_frame = annotated_frame.shape[1]
                
                # Fundo para frase (semi-transparente)
                overlay = annotated_frame.copy()
                cv2.rectangle(overlay, (0, altura_frame - 120), (largura_frame, altura_frame), 
                             (0, 0, 0), -1)
                cv2.addWeighted(overlay, 0.7, annotated_frame, 0.3, 0, annotated_frame)
                
                # Texto da frase (com fonte maior e melhor visualização)
                frase = self.obter_frase()
                
                # Quebra a frase em linhas se for muito longa
                max_chars = 40
                if len(frase) > max_chars:
                    # Mostra os últimos caracteres
                    frase_display = "..." + frase[-max_chars:]
                else:
                    frase_display = frase
                
                cv2.putText(
                    annotated_frame,
                    "FRASE:",
                    (10, altura_frame - 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2
                )
                cv2.putText(
                    annotated_frame,
                    frase_display,
                    (10, altura_frame - 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2,
                    (0, 255, 0),
                    2
                )
                
                # Instruções
                cv2.putText(
                    annotated_frame,
                    f"BACKSPACE=apagar | ESPACO=espaco | c=limpar | f=salvar",
                    (10, altura_frame - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (200, 200, 200),
                    1
                )
                
                cv2.imshow('Reconhecimento Libras - YOLOv8', annotated_frame)
            
            # Controles
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                screenshot_path = f'screenshot_{screenshot_count}.jpg'
                cv2.imwrite(screenshot_path, annotated_frame)
                print(f"📸 Screenshot salvo: {screenshot_path}")
                screenshot_count += 1
            elif key == ord('c'):
                self.limpar_frase()
                print("🗑️  Frase limpa!")
            elif key == 8 or key == 127:  # BACKSPACE (funciona em Windows e Linux)
                if self.remover_ultimo_caractere():
                    print(f"⬅️  Caractere removido. Frase atual: '{self.frase_atual}'")
                else:
                    print("⚠️  Frase já está vazia")
            elif key == ord('f'):
                if self.salvar_frase():
                    print(f"💾 Frase salva: '{self.frase_atual}'")
                else:
                    print("⚠️  Frase vazia, nada para salvar")
            elif key == 32:  # ESPAÇO
                if self.adicionar_espaco():
                    print(f"⎵  Espaço adicionado. Frase atual: '{self.frase_atual}'")
                else:
                    print("⚠️  Não é possível adicionar espaço agora")
            elif key == ord('+') or key == ord('='):
                imgsz = min(imgsz + 32, 640)
                print(f"⬆️  Tamanho aumentado: {imgsz}")
            elif key == ord('-') or key == ord('_'):
                imgsz = max(imgsz - 32, 160)
                print(f"⬇️  Tamanho reduzido: {imgsz}")
        
        cap.release()
        cv2.destroyAllWindows()
        print("\n👋 Encerrando reconhecimento em tempo real")
        print(f"📝 Frase final: '{self.frase_atual}'")


# ==================== SCRIPT PRINCIPAL ====================

def main():
    print("\n" + "="*60)
    print("🤟 SISTEMA DE RECONHECIMENTO DE LIBRAS - YOLOv8")
    print("   Com Construção de Frases e Normalização de Sinais")
    print("="*60 + "\n")
    
    recognizer = LibrasRecognizer()
    
    # PASSO 1: Verificar estrutura do dataset
    print("📁 PASSO 1: Verificando estrutura do dataset...\n")
    yaml_path = recognizer.verificar_dataset('dataset')
    
    if yaml_path is None:
        print("❌ data.yaml não encontrado! Crie o arquivo primeiro.")
        return
    
    # PASSO 2: Corrigir caminhos no data.yaml
    print("\n🔧 PASSO 2: Corrigindo caminhos no data.yaml...\n")
    recognizer.corrigir_yaml(yaml_path)
    
    # PASSO 3: Menu de opções
    while True:
        print("\n" + "="*60)
        print("MENU PRINCIPAL")
        print("="*60)
        print("1. Treinar novo modelo")
        print("2. Validar modelo treinado")
        print("3. Testar em imagem")
        print("4. Reconhecimento em tempo real (webcam) COM FRASES ✨")
        print("5. Sair")
        print("="*60)
        
        escolha = input("\nEscolha uma opção (1-5): ").strip()
        
        if escolha == '1':
            print("\n🎓 TREINAMENTO")
            continuar = input("Continuar treinamento anterior? (s/n, padrão 'n'): ").strip().lower()
            resume = continuar == 's'
            epochs = input("Número de épocas (padrão 100): ").strip()
            epochs = int(epochs) if epochs else 100
            batch = input("Batch size (padrão 16): ").strip()
            batch = int(batch) if batch else 16
            size = input("Tamanho do modelo (n/s/m/l/x, padrão 'n'): ").strip()
            size = size if size in ['n', 's', 'm', 'l', 'x'] else 'n'
            device_choice = input("Usar GPU se disponível? (s/n, padrão 's'): ").strip().lower()
            if device_choice == 'n':
                device_choice = 'cpu'
            else:
                device_choice = 'gpu'
            recognizer.treinar(yaml_path, epochs=epochs, batch=batch, model_size=size, resume=resume, device_choice=device_choice)
        
        elif escolha == '2':
            print("\n📊 VALIDAÇÃO")
            model_path = input("Caminho do modelo (Enter para padrão): ").strip()
            model_path = model_path if model_path else 'runs/detect/libras_yolo2/weights/best.pt'
            recognizer.validar(model_path)
        
        elif escolha == '3':
            print("\n🖼️  TESTE EM IMAGEM")
            image_path = input("Caminho da imagem: ").strip()
            if image_path:
                device_choice = input("Usar GPU se disponível? (s/n, padrão 's'): ").strip().lower()
                if device_choice == 'n':
                    device_choice = 'cpu'
                else:
                    device_choice = 'gpu'
                recognizer.testar_imagem(image_path, device_choice=device_choice)
        
        elif escolha == '4':
            print("\n📹 TEMPO REAL COM CONSTRUÇÃO DE FRASES")
            device_choice = input("Usar GPU se disponível? (s/n, padrão 's'): ").strip().lower()
            if device_choice == 'n':
                device_choice = 'cpu'
            else:
                device_choice = 'gpu'
            recognizer.reconhecer_webcam(device_choice=device_choice)
        
        elif escolha == '5':
            print("\n👋 Até logo!")
            break
        
        else:
            print("\n❌ Opção inválida!")


if __name__ == "__main__":
    main()