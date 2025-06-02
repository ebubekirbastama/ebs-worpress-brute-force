# 🔐 WP Brute Force GUI Tool

> 🧪 **Educational WordPress Login Brute Force Tool with GUI, Emojis, and Multi-Target Support**  
> 🛠 Built with Python + PyQt5 and Threads to avoid freezing the interface.

---

## 🚀 Features

- 🔁 **Multi-target scanning** (load 50+ WordPress sites from a .txt file)
- 🔐 Bruteforce login with user-defined username and wordlist
- 📊 Live statistics panel (attempts, success count, success rate, duration)
- 🧵 Threaded backend (no GUI freezing)
- 📝 Real-time logging with emojis (colored and intuitive)
- 📂 Load wordlist and targets via GUI buttons
- ✅ Simple, lightweight, and open source

---

## 🖥️ Screenshots

![screenshot](https://raw.githubusercontent.com/ebubekirbastama/ebs-worpress-brute-force/refs/heads/main/syhmhfz.png)

---

## 📦 Requirements

- Python 3.8+
- PyQt5
- requests

```bash
pip install -r requirements.txt
```

`requirements.txt`:
```
PyQt5
requests
```

---

## 📁 Files

| File | Description |
|------|-------------|
| `brute_gui.py` | Main GUI tool |
| `targets.txt` | List of target WordPress login URLs |
| `wordlist.txt` | List of passwords to test |
| `README.txt` | This file |

---

## ▶️ How to Use

1. Run the GUI:

```bash
python EBSWordpress-Brute-force.py
```

2. Fill in:
   - 👤 Username (`admin`, `editor`, etc.)
   - 📂 Select a wordlist (.txt)
   - 🌐 Select a target list (.txt)

3. Click 🚀 `Start Attack`

4. Watch the 📋 log panel and 📊 statistics as the process runs.

---

## ⚠️ Disclaimer & Legal

> ❗ This tool is created **for educational and ethical hacking purposes only**.  
> ❌ **Do not** use this tool on websites without **explicit authorization**.  
> 🧑‍🏫 It was designed for **cybersecurity awareness training** in controlled lab environments.  
> ⚖️ The author takes **no responsibility** for any misuse.

---

## 👨‍💻 Author

**Ebubekir Bastama** – *Security Researcher / Instructor*  
📧 Contact: www.ebubekirbastama.com

---

## 🌟 License

MIT License
