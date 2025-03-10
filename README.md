## 🖇️ VPS Deployment Guide

1. **Clone the Repository**

   ```bash
   git clone https://github.com/iamnolimit/mirai-streams-bot && cd mirai-streams-bot
   ```

2. **Run the setup**

   ```bash
   bash setup
   ```

3. **Install tmux**
   To keep your bot running after closing the terminal:

   ```bash
   sudo apt install tmux && tmux
   ```

4. **Run the Bot**

   ```bash
   python3 -m WinxMusic
   ```

5. **Detach from the tmux session**
   Press `Ctrl+b`, then `d` to exit the tmux session without stopping the bot.
