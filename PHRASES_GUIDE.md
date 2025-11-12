# 📝 Sistema de Formação de Frases - LIBRAS

## 🎯 O Que É?

Um sistema inteligente que detecta letras em LIBRAS e forma frases **automaticamente**!

Quando você mantém uma letra por tempo suficiente (ex: 2 segundos) com alta confiança, ela é adicionada automaticamente à frase que você está construindo.

---

## 🚀 Como Usar

### Passo 1: Executar o Script

```powershell
.\venv\Scripts\Activate.ps1
python src/detect_webcam_phrases.py
```

### Passo 2: Formar sua Primeira Palavra

1. **Faça a primeira letra** em LIBRAS (ex: "O")
2. **Mantenha por 2 segundos** - você verá uma barra de progresso
3. **Letra adicionada!** - Aparece na tela: "O"
4. **Continue com as próximas letras** - "L", "A"
5. **Pressione ESPAÇO** para separar palavras
6. **Continue formando a frase** - "OLA MUNDO"

---

## 🎮 Controles Completos

| Tecla | Ação |
|-------|------|
| `Mantenha a letra` | Adiciona automaticamente após 2s |
| `ESPAÇO` | Adicionar espaço entre palavras |
| `BACKSPACE` | Apagar última letra |
| `C` | Limpar frase inteira |
| `S` | Salvar frase em arquivo .txt |
| `Q` | Sair do programa |
| `+` | Aumentar confiança mínima (mais rigoroso) |
| `-` | Diminuir confiança mínima (mais permissivo) |
| `]` | Aumentar tempo de hold (mais lento) |
| `[` | Diminuir tempo de hold (mais rápido) |

---

## 📊 Interface na Tela

### Área Superior - Frase
```
┌─────────────────────────────────────┐
│ FRASE:                              │
│ OLA MUNDO                           │
└─────────────────────────────────────┘
```

### Centro - Detecção em Tempo Real
- Mostra as detecções do YOLO
- Bounding boxes nas mãos
- Confiança de cada detecção

### Área Inferior - Status
```
┌─────────────────────────────────────┐
│ Detectando: A                       │
│ ████████░░░░░░░░░░░ 40%            │
│ Estabilidade: 85%                   │
└─────────────────────────────────────┘
```

---

## ⚙️ Como Funciona (Tecnicamente)

### 1. **Detecção Contínua**
- O modelo YOLO detecta a letra em cada frame (~30 fps)
- Cada detecção tem uma confiança (0-1)

### 2. **Histórico de Detecções**
- Mantém últimos 30 frames (~1 segundo)
- Calcula qual letra aparece mais frequentemente
- Calcula estabilidade (% de vezes que a letra aparece)

### 3. **Critérios para Adicionar Letra**
Para uma letra ser adicionada, TODOS esses critérios devem ser atendidos:

```python
✅ Confiança >= 0.65 (65%)
✅ Estabilidade >= 0.75 (75% dos frames)
✅ Tempo mantido >= 2.0 segundos
✅ Não está em cooldown (0.5s após última adição)
```

### 4. **Adição Automática**
- Quando todos os critérios são atendidos, a letra é adicionada
- Um feedback visual aparece: "LETRA ADICIONADA!"
- Sistema entra em cooldown de 0.5s
- Pronto para próxima letra!

---

## 🎯 Parâmetros Ajustáveis

### Confiança Mínima (confidence_threshold)
```python
Padrão: 0.65 (65%)
Faixa: 0.30 - 0.95

Baixo (0.4): Detecta mais, mas pode ter erros
Médio (0.65): Balanceado ✅
Alto (0.85): Muito preciso, mas pode perder detecções
```

### Tempo de Hold (hold_time)
```python
Padrão: 2.0 segundos
Faixa: 0.5 - 5.0 segundos

Rápido (1.0s): Forma frases mais rápido
Médio (2.0s): Balanceado ✅
Lento (3.0s): Mais tempo para posicionar
```

### Estabilidade (stability_threshold)
```python
Padrão: 0.75 (75%)
Fixo no código (pode editar se quiser)

Alta (0.9): Letra deve aparecer quase sempre
Média (0.75): Balanceado ✅
Baixa (0.6): Aceita mais variação
```

---

## 💡 Dicas para Melhor Resultado

### 1. **Iluminação**
- ✅ Luz natural de frente ou lateral
- ✅ Evite sombras na mão
- ❌ Não fique de costas para a janela

### 2. **Posicionamento**
- ✅ Mão centralizada na câmera
- ✅ Distância de ~50cm
- ✅ Mantenha a mão estável
- ❌ Evite movimentos bruscos

### 3. **Fundo**
- ✅ Parede clara e neutra
- ✅ Fundo uniforme
- ❌ Evite fundos com muitos detalhes

### 4. **Formação de Letras**
- ✅ Faça a letra de forma clara
- ✅ Mantenha a posição fixa
- ✅ Aguarde a barra de progresso completar
- ❌ Não mude para outra letra antes de completar

### 5. **Ajuste de Parâmetros**
- **Se adiciona letras erradas:** Aumente confiança (`+`)
- **Se não detecta letras:** Diminua confiança (`-`)
- **Se é muito lento:** Diminua tempo de hold (`[`)
- **Se adiciona rápido demais:** Aumente tempo de hold (`]`)

---

## 📝 Exemplos de Uso

### Exemplo 1: Formar uma Palavra Simples
```
Objetivo: "OLA"

1. Faça "O" → Aguarde 2s → "O" adicionado
2. Faça "L" → Aguarde 2s → "OL" 
3. Faça "A" → Aguarde 2s → "OLA"
4. Pressione S para salvar!
```

### Exemplo 2: Formar uma Frase
```
Objetivo: "OLA MUNDO"

1-3. [Forme "OLA" como acima]
4. Pressione ESPAÇO → "OLA "
5. Faça "M" → Aguarde → "OLA M"
6. Faça "U" → Aguarde → "OLA MU"
7. Faça "N" → Aguarde → "OLA MUN"
8. Faça "D" → Aguarde → "OLA MUND"
9. Faça "O" → Aguarde → "OLA MUNDO"
10. Pressione S para salvar!
```

### Exemplo 3: Corrigir Erros
```
Frase atual: "OLHA"
Deveria ser: "OLA"

1. Pressione BACKSPACE → "OLH"
2. Pressione BACKSPACE → "OL"
3. Faça "A" → Aguarde → "OLA"
```

---

## 🔧 Troubleshooting

### ❌ "Letras erradas sendo adicionadas"

**Causas:**
- Confiança muito baixa
- Movimentos da mão durante detecção
- Iluminação ruim

**Soluções:**
```powershell
# Aumentar confiança (pressione +)
# Aumentar tempo de hold (pressione ])
# Melhorar iluminação
# Manter mão mais estável
```

### ❌ "Não adiciona nenhuma letra"

**Causas:**
- Confiança muito alta
- Modelo não detecta a letra
- Tempo de hold muito curto

**Soluções:**
```powershell
# Diminuir confiança (pressione -)
# Verificar se o modelo foi treinado
# Melhorar posição da mão
# Aguardar mais tempo
```

### ❌ "Adiciona letras muito rápido"

**Causas:**
- Tempo de hold muito curto

**Soluções:**
```powershell
# Aumentar tempo de hold (pressione ])
# Padrão: 2.0s
# Recomendado: 2.5-3.0s
```

### ❌ "Adiciona letras muito devagar"

**Causas:**
- Tempo de hold muito longo
- Estabilidade não atingida

**Soluções:**
```powershell
# Diminuir tempo de hold (pressione [)
# Manter mão mais estável
# Melhorar iluminação
```

---

## 📊 Arquivos Gerados

### Frases Salvas
```
Localização: c:\Users\Nicolas\Desktop\computer-vision\
Formato: frase_YYYYMMDD_HHMMSS.txt
Exemplo: frase_20251112_143022.txt

Conteúdo: Texto simples com a frase
```

### Como Salvar
```
1. Forme sua frase na webcam
2. Pressione S
3. Arquivo é criado com timestamp
4. Confirmação aparece no terminal
```

---

## 🎓 Algoritmo Detalhado

```python
Para cada frame da webcam:
    1. Detectar letra com YOLO
    2. Se confiança >= threshold:
        - Adicionar letra ao histórico (últimos 30 frames)
    3. Calcular letra mais frequente no histórico
    4. Calcular estabilidade (% de ocorrências)
    5. Se estabilidade >= 75%:
        - Se é letra diferente da anterior:
            * Resetar timer
            * Iniciar contagem
        - Se é a mesma letra:
            * Continuar contagem
            * Atualizar barra de progresso
        - Se tempo >= hold_time:
            * Adicionar letra à frase
            * Mostrar feedback
            * Resetar para próxima letra
    6. Senão:
        - Resetar contagem
```

---

## 🚀 Personalização Avançada

### Editar Parâmetros no Código

Abra `src/detect_webcam_phrases.py` e encontre:

```python
phrase_builder = PhraseBuilder(
    hold_time=2.0,              # ← Tempo de hold
    confidence_threshold=0.65,   # ← Confiança mínima
    stability_threshold=0.75     # ← Estabilidade mínima
)
```

### Exemplo: Sistema Mais Rápido
```python
phrase_builder = PhraseBuilder(
    hold_time=1.0,              # 1 segundo
    confidence_threshold=0.60,   # 60%
    stability_threshold=0.70     # 70%
)
```

### Exemplo: Sistema Mais Preciso
```python
phrase_builder = PhraseBuilder(
    hold_time=3.0,              # 3 segundos
    confidence_threshold=0.80,   # 80%
    stability_threshold=0.85     # 85%
)
```

---

## 📈 Comparação: Webcam Normal vs Frases

| Aspecto | detect_webcam.py | detect_webcam_phrases.py |
|---------|------------------|--------------------------|
| **Objetivo** | Visualizar detecções | Formar frases |
| **Interação** | Passiva | Ativa |
| **Output** | Visual apenas | Texto (frases) |
| **Uso** | Demo/Teste | Comunicação real |
| **Complexidade** | Simples | Avançado |
| **Feedback** | Tempo real | Progressivo |

---

## 💡 Casos de Uso

### 1. **Educação**
- Ensinar LIBRAS
- Praticar alfabeto
- Testar conhecimento

### 2. **Comunicação**
- Formar mensagens
- Comunicação básica
- Transcrição de sinais

### 3. **Demonstração**
- Mostrar capacidades do modelo
- Apresentações
- Feiras de ciência

### 4. **Desenvolvimento**
- Testar modelo
- Validar detecções
- Ajustar parâmetros

---

## 🎯 Limitações e Melhorias Futuras

### Limitações Atuais
- ❌ Apenas letras (não palavras completas)
- ❌ Uma letra por vez
- ❌ Requer tempo de hold
- ❌ Sensível a iluminação

### Melhorias Futuras (v2.0)
- ✅ Dicionário de palavras comuns
- ✅ Auto-complete
- ✅ Sugestões de próxima letra
- ✅ Histórico de frases
- ✅ Export para diferentes formatos
- ✅ Interface gráfica (GUI)
- ✅ Múltiplas mãos simultâneas

---

## 📚 Recursos Adicionais

### Documentos Relacionados
- `README.md` - Documentação geral
- `QUICK_START.md` - Início rápido
- `GUIA_PT.md` - Tutorial completo
- `detect_webcam.py` - Versão simples

### Scripts Relacionados
- `train.py` - Treinar modelo
- `validate.py` - Validar modelo
- `detect_image.py` - Detectar em imagens

---

## 🎉 Comece Agora!

```powershell
# 1. Ativar ambiente
.\venv\Scripts\Activate.ps1

# 2. Executar script de frases
python src/detect_webcam_phrases.py

# 3. Formar sua primeira palavra!
# Dica: Comece com algo simples como "OLA" ou "OI"
```

---

**Autor:** Nicolas  
**Data:** 12/11/2025  
**Versão:** 1.0  
**Feature:** Sistema de Formação de Frases Automático

**🤟 Boa comunicação!**
