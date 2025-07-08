# Ratatouille's XO 
# 🐀 Ratatouille's XO – AI-Powered Tic Tac Toe Game 🎮🇪🇬

Welcome to **Ratatouille's XO**, an AI-enhanced Tic Tac Toe game reimagined with a *Ratatouille* cartoon theme—featuring **custom sound effects from the Egyptian-dubbed version (مدبلجة مصري)** of the film.

This isn't just a game—it's a fun, interactive blend of strategic AI logic, charming cartoon personality, and nostalgic Egyptian voiceovers. Whether you **win, lose, or draw**, you're met with iconic character sounds that bring the game to life.

---

## 🧠 AI Strategies Included

This game lets you play against **8 different AI strategies**, each representing a distinct way of thinking:

1. **Minimax** – Perfect play using full-depth game-tree evaluation  
2. **Fork Block** – Prevents multi-path win setups  
3. **Threat Block** – Detects and blocks two-in-a-row threats  
4. **Minimax + Fork Block** – Combines perfect foresight with tactical defense  
5. **Minimax + Threat Block** – Predicts while preventing  
6. **Minimax + Alpha-Beta Pruning** – Faster computation through search pruning  
7. **Heuristic Reduction** – Quick decisions using scoring rules  
8. **Symmetry Reduction** – Eliminates mirrored board states to reduce complexity

---

## 🎨 Project Files

- **`test.py`**  
  This is the main playable game file. It includes:
  - A full GUI built with `pygame`
  - Character-based **sound effects from Ratatouille (Egyptian dub)** using `pygame.mixer`
  - Player vs AI functionality with selectable strategies
  - Audio feedback based on the game's result (win, lose, draw)

- **`videos.py`**  
  A fun bonus feature: when you lose, a **Ratatouille character scene** plays with **sound and voice lines** taken from the dubbed cartoon version. It’s a lighthearted visual moment to emphasize defeat with a comic twist.

---

## 🛠️ Built With

The project uses the following Python libraries:

- `pygame` – GUI, event handling, rendering  
- `pygame.mixer` – Custom sound effect playback  
- `sys` – System-level controls  
- `os` – Path and file management  
- `copy` – Deep copy for board state management  
- `datetime` & `time` – For player timers and AI response tracking  

---

## 👥 Team Credits

This project was created with collaboration, creativity, and deep technical effort.
## 🎬 Inspiration

> *"Like Remy in Ratatouille, we believed greatness can come from anywhere—even from a cartoon, a childhood memory, and a few lines of Python code."*

---

## 📸 Screenshots & Demo

*Coming soon – gameplay GIFs and demo video will be uploaded here.*

---

## 🚀 How to Run

1. Install dependencies:
   ```bash
   pip install pygame