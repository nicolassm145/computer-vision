# Sistema de Reconhecimento de Libras com YOLOv8

Este projeto realiza o reconhecimento de sinais de Libras (Língua Brasileira de Sinais) utilizando modelos YOLOv8.

## Estrutura do Projeto

```
libras_recognition.py         # Script principal
config/                      # Configurações
runs/detect/                 # Resultados dos treinamentos
  libras_yolo/               # Experimentos/modelos
  libras_yolo2/              # Experimentos/modelos alternativos
archive/                     # Dados originais por classe (A, B, ...)
  train/, test/, valid/      # Imagens separadas por classe
dataset/                     # Dataset no formato YOLO
  train/images, labels/      # Imagens e labels de treino
  valid/images, labels/      # Imagens e labels de validação
  test/images, labels/       # Imagens e labels de teste (opcional)
  data.yaml                  # Configuração do dataset
gerar_labels_archive.py      # Script para gerar labels YOLO a partir do archive
```

## Como usar

1. **Instale as dependências**

   ```powershell
   pip install -r requirements.txt
   ```

   (ou instale manualmente: ultralytics, opencv-python, pyyaml)


2. **Prepare os dados do archive**

   - Coloque suas imagens nas pastas de classe em `archive/train`, `archive/test`, `archive/valid`.
   - Se não houver labels, use o script `gerar_labels_archive.py` para gerar labels genéricos (bounding box cobre toda a imagem, útil para classificação simples).

   ```powershell
   python gerar_labels_archive.py
   ```

   - Os labels serão criados em `dataset/train/labels`, `dataset/test/labels`, `dataset/valid/labels`.
   - As imagens devem ser copiadas para `dataset/train/images`, `dataset/test/images`, `dataset/valid/images` (faça isso manualmente ou peça um script).
   - Edite o arquivo `dataset/data.yaml` com suas classes e caminhos.

3. **Execute o script principal**

   ```powershell
   python libras_recognition.py
   ```

4. **Menu de opções**

   - Treinar novo modelo
   - Validar modelo treinado
   - Testar em imagem
   - Reconhecimento em tempo real (webcam)
   - Sair

5. **Escolha entre CPU ou GPU**
   - O script permite escolher o dispositivo para treino e reconhecimento.

## Resultados

- Os modelos treinados ficam em `runs/detect/libras_yolo/weights/best.pt` ou `runs/detect/libras_yolo2/weights/best.pt`.
- Resultados de predição são salvos em `runs/detect/predict/`.

## Requisitos

- Python 3.8+
- ultralytics
- opencv-python
- pyyaml

## Observações

- Para melhor desempenho, utilize GPU (CUDA).
- O script permite continuar treinamentos anteriores ou iniciar do zero.
- Para usar outro modelo, informe o caminho desejado no menu.
- Se você possui labels reais (bounding boxes), coloque-os em `dataset/train/labels` etc. e não use o script de geração automática.
- Para classificação simples, o script de geração cobre toda a imagem como bounding box.
- Para detecção, use ferramentas de rotulagem (LabelImg, Roboflow, CVAT) para criar labels precisos.

---

Dúvidas ou sugestões? Abra uma issue ou entre em contato!
