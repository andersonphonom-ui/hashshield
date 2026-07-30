# 🐙 HashShield

**HashShield** is a Python-based hash analysis tool that identifies hash types, cracks them using wordlist or brute force attacks, and generates hashes from plain text — all from your terminal.

> ⚠️ **Disclaimer:** This tool is for educational purposes only. Only use it on hashes you own or have permission to test.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 Hash Identification | Detects MD5, SHA1, SHA256, SHA512, bcrypt, NTLM, and more |
| 💪 Strength Rating | Rates hash algorithm strength (Weak / Medium / Strong) |
| ⚔️ Wordlist Attack | Crack hashes using wordlists like rockyou.txt |
| 🔢 Brute Force | Try all combinations up to a specified length |
| ⚙️ Hash Generator | Generate hashes from plain text |

---

## 📦 Installation

```bash
git clone https://github.com/andersonphonom-ui/hashshield.git
cd hashshield
pip install -r requirements.txt --break-system-packages
sudo cp main.py identifier.py cracker.py generator.py banner.py /usr/local/bin/
sudo mv /usr/local/bin/main.py /usr/local/bin/hashshield
sudo chmod +x /usr/local/bin/hashshield
```

---

## 🚀 Usage

```bash
# Help
hashshield -h

# Version
hashshield -v

# Identify hash type
hashshield identify <hash>

# Crack with wordlist
hashshield crack <hash> -w /usr/share/wordlists/rockyou.txt

# Crack with brute force
hashshield crack <hash> -b --max 4

# Generate hash
hashshield generate "password" -t md5
hashshield generate "password" -t sha256
```

---

## 📊 Example Output

```
🔍 Hash Identification
╔═══════════════╤════════╤═══════════════╤════════════╗
║ Type          │ Length │ Strength      │ Crackable  ║
╟───────────────┼────────┼───────────────┼────────────╢
║ MD5           │ 32     │ Weak 🔴       │ Yes ✅     ║
║ NTLM          │ 32     │ Weak 🔴       │ Yes ✅     ║
╚═══════════════╧════════╧═══════════════╧════════════╝

🔓 Hash Cracked!
╔═══════════════╤══════════════════════╗
║ Hash          │ 5f4dcc3b5aa765d61... ║
╟───────────────┼──────────────────────╢
║ Password      │ password             ║
╟───────────────┼──────────────────────╢
║ Attempts      │ 1247                 ║
╟───────────────┼──────────────────────╢
║ Time          │ 0.43s                ║
╚═══════════════╧══════════════════════╝
```

---

## 🔐 Supported Hash Types

| Hash | Length | Strength |
|---|---|---|
| MD5 | 32 | Weak 🔴 |
| SHA1 | 40 | Weak 🔴 |
| SHA224 | 56 | Medium 🟡 |
| SHA256 | 64 | Medium 🟡 |
| SHA384 | 96 | Strong 🟢 |
| SHA512 | 128 | Strong 🟢 |
| bcrypt | variable | Strong 🟢 |
| NTLM | 32 | Weak 🔴 |
| MySQL4 | 16 | Weak 🔴 |

---

## 📁 Project Structure

```
hashshield/
├── main.py          # CLI entry point
├── identifier.py    # Hash type detection engine
├── cracker.py       # Wordlist & brute force engine
├── generator.py     # Hash generator
├── banner.py        # ASCII art banner
└── requirements.txt
```

---

## 👨‍💻 Author

**Youssef Mediouni**
- YouTube: [PH4nt0m CYber](https://youtube.com/@PH4nt0mCYber)
- GitHub: [@andersonphonom-ui](https://github.com/andersonphonom-ui)

---

## 📄 License

MIT License — free to use, modify, and distribute.
