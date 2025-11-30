# 👽 Alien Strike

Um jogo de plataforma 2D desenvolvido em Python com `pygame-zero`, onde você controla um alien em uma jornada emocionante para alcançar a bandeira final enquanto evita inimigos!

![Python](https://img.shields.io/badge/Python-3.7+-blue)
![Game Status](https://img.shields.io/badge/Status-Completo-brightgreen)

---

## 📋 Características

✨ **Gameplay Dinâmico**
- Controle fluido do personagem principal com movimento horizontal e saltos
- Sistema de plataformas variadas para desafios progressivos
- Mecânica de gravidade realista

👾 **Inimigos Desafiadores**
- **Inimigos em Terra**: Patrulham plataformas específicas
- **Inimigos Voadores**: Movem-se em padrão ondulatório pela tela
- Sistema de detecção de colisão com perda de vida

🎵 **Experiência Imersiva**
- Música de fundo retrô (arcade style)
- Efeitos sonoros para saltos
- Controle de som on/off no menu

🎯 **Interface Completa**
- Menu principal com opções
- Sistema de vidas (HUD visual)
- Tela de pausa
- Tela de vitória e game over
- Créditos

---

## 🎮 Controles

| Controle            | Ação                                            |
| ------------------- | ----------------------------------------------- |
| **← Seta Esquerda** | Mover para esquerda                             |
| **→ Seta Direita**  | Mover para direita                              |
| **↑ Seta Acima**    | Pular (enquanto no chão)                        |
| **ESC**             | Pausar/Retomar jogo                             |
| **SPACE**           | Retornar ao menu (na tela de vitória/game over) |
| **Click**           | Selecionar opções no menu                       |

---

## 🚀 Como Jogar

1. **Inicie o jogo**: Execute `main.py` com pygame-zero
2. **No Menu**:
   - Clique em "START" para começar
   - Use "SOUND" para ativar/desativar áudio
   - Acesse "CREDITS" para ver os créditos
3. **Durante o Jogo**:
   - Navegue pelas plataformas usando as setas
   - Evite os inimigos - você tem 2 vidas
   - Atinja a bandeira no topo para vencer!

---

## 📦 Requisitos

- Python 3.7+
- pygame-zero
- pygame

### Instalação de Dependências

```bash
pip install pygame-zero pygame
```

---

## 📁 Estrutura do Projeto

```
alienStrike/
├── main.py              # Arquivo principal do jogo
├── images/              # Sprites e assets visuais
├── sounds/              # Efeitos sonoros
├── music/               # Trilha sonora
├── fonts/               # Fontes customizadas
└── README.md            # Este arquivo
```

---

## 🎮 Mecânicas de Jogo

### Sistema de Plataformas

O jogo possui 8 plataformas dispostas em diferentes alturas, criando um desafio progressivo. Você deve pular de plataforma em plataforma para alcançar o objetivo.

### Colisão e Física

- **Gravidade**: Força constante puxa o player para baixo (0.6 unidades/frame)
- **Atrito**: Reduz a velocidade horizontal quando o player não está se movimentando
- **Colisão**: Detecção baseada em hitbox (AABB)

### Sistema de Vidas

Você começa com **2 vidas**:
- Colidindo com um inimigo: Perde 1 vida e retorna à posição inicial
- Sem vidas: Game Over

---

## 🛠️ Desenvolvimento

### Classes Principais

#### `Alien`

Classe que representa o personagem controlável do jogador.
- Movimento horizontal com velocidade e atrito
- Sistema de pulo com gravidade
- Animações de idle, corrida e pulo
- Detecção de colisão com plataformas

#### `Enemy`

Inimigos que patrulham as plataformas.
- Movimento linear entre dois pontos
- Reversão automática de direção ao atingir limites
- Animações de caminhada

#### `FlyingEnemy`

Inimigos voadores com movimento ondulatório.
- Movimento em onda senoidal (padrão oscilante)
- Velocidade horizontal configurável
- Animations para voo

#### `Flag`

Representa o objetivo final do jogo.
- Animação de bandeira fluindo
- Localização dinâmica baseada na plataforma mais alta

#### `SpriteAnimator`

Sistema de animação reutilizável.
- Suporta múltiplos frames
- Velocidade de animação configurável

---

## 🎨 Estados do Jogo

| Estado    | Descrição               |
| --------- | ----------------------- |
| MENU      | Tela inicial com opções |
| PLAYING   | Jogo em andamento       |
| PAUSED    | Jogo pausado (ESC)      |
| CREDITS   | Tela de créditos        |
| VICTORY   | Tela de vitória         |
| GAME_OVER | Tela de game over       |

---

## 🎵 Áudio

### Música
- **retro_arcade**: Trilha sonora principal loopada durante todo o jogo

### Efeitos Sonoros
- **jump.play()**: Som ao pular (quando som está ativado)

---

## 📝 Créditos

**Desenvolvimento**
- Game Design & Programming: Dante Lopes

**Assets**
- Sprites & Sound Design: Kenney
- Soundtrack Music: Viacheslav 'original_soundtrack' Starostin

---

## 🔮 Melhorias Futuras

Possíveis adições ao projeto:
- [ ] Diferentes níveis com dificuldade progressiva
- [ ] Power-ups (escudo, velocidade, pulo duplo)
- [ ] Highscore/Sistema de pontuação
- [ ] Mais tipos de inimigos
- [ ] Animações aprimoradas
- [ ] Efeitos visuais (partículas, explosões)
- [ ] Suporte a gamepad

---

## 🐛 Solução de Problemas

**Erro: "ModuleNotFoundError: No module named 'pgzero'"**

```bash
pip install pygame-zero pygame
```

**Sprites não aparecem**
- Verifique se os arquivos de imagem estão em `images/`
- Verifique se os nomes dos sprites correspondem ao código

**Música não toca**
- Confirme que `retro_arcade` está em `music/`
- Verifique se o som está ativado no menu

---

## 📄 Licença
Este projeto utiliza assets de Kenney (kenney.nl) que são de domínio público.

---

## 👤 Autor
**Dante Lopes**

---

**Divirta-se jogando! 🚀👽**