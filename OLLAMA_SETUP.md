# 🧠 OLLAMA Setup Guide

**Make Your AI Code Agent SMART with OLLAMA!**

OLLAMA er en lokal AI-modell-runtime som kjører 100% offline på din maskin.

---

## 🚀 Quick Start

### Windows, macOS, eller Linux:

1. **Download OLLAMA:**
   ```
   https://ollama.ai
   ```
   Klikk "Download" og installer

2. **Open Terminal/Command Prompt og kjør:**
   ```bash
   ollama serve
   ```

3. **I et annet Terminal-vindu, kjør:**
   ```bash
   ollama pull neural-chat
   ```
   eller
   ```bash
   ollama pull codellama
   ```

4. **Kjør din Code Agent Dashboard:**
   ```bash
   ./run.sh  # macOS/Linux
   run.bat   # Windows
   ```

5. **Åpne http://localhost:8000**
   - Agenten vil nå være SMART!
   - Snakk naturlig med den
   - Den forstår og svarer

---

## 📋 Detaljerte Instruksjoner

### Windows

**1. Download og installer OLLAMA:**
- Gå til https://ollama.ai
- Klikk "Download for Windows"
- Installer som normal Windows-app
- Restart datamasinen

**2. Åpne Command Prompt eller PowerShell:**
```cmd
ollama serve
```
Du skal se:
```
Serving models on http://localhost:11434
```

**3. I et annet vindu, last ned modell:**
```cmd
ollama pull neural-chat
```
eller for kodegenerering:
```cmd
ollama pull codellama
```

**4. Lag dashboard:**
```cmd
run.bat
```

**5. Test det:**
- Åpne http://localhost:8000
- Prøv å snakke: "Lag en Python funksjon som..."
- Agenten skal svare!

---

### macOS

**1. Install med Homebrew (anbefalt):**
```bash
brew install ollama
```

Eller download fra https://ollama.ai

**2. Start OLLAMA:**
```bash
ollama serve
```

**3. I annet terminal, last ned modell:**
```bash
ollama pull neural-chat
```

**4. Kjør dashboard:**
```bash
./run.sh
```

**5. Test:**
- http://localhost:8000
- "Fix this Python code..."
- Agenten svarer!

---

### Linux

**1. Install (apt/Ubuntu):**
```bash
curl https://ollama.ai/install.sh | sh
```

**2. Start serveren:**
```bash
ollama serve
```

**3. Last ned modell:**
```bash
ollama pull neural-chat
```

**4. Kjør dashboard:**
```bash
./run.sh
```

**5. Test:**
- http://localhost:8000
- Snakk med agenten!

---

## 🤖 Modeller - Velg Rett

### Anbefalte Modeller

**neural-chat (DEFAULT - BEST)**
```bash
ollama pull neural-chat
```
- ✅ Balansert
- ✅ Rask
- ✅ Smart
- ✅ Bra for kode

**codellama (FOR KODEGENERERING)**
```bash
ollama pull codellama
```
- ✅ Spesialisert på kode
- ✅ Genererer bedre kode
- ✅ Litt sløere
- ✅ Bra for kompleks kode

**mistral (LITEN & RASK)**
```bash
ollama pull mistral
```
- ✅ Veldig rask
- ✅ Lite minne
- ✅ Ikke like smart
- ✅ Bra for gamle PCer

**llama2 (KRAFTIG)**
```bash
ollama pull llama2
```
- ✅ Veldig smart
- ✅ Trenger mer RAM
- ✅ Sløere
- ✅ Bra for beregningskraft

---

## 🔧 Troubleshooting

### "OLLAMA not available" i dashboard

**Problem:** Agenten sier den kan ikke finne OLLAMA

**Løsning:**
1. Sjekk at `ollama serve` kjører i terminal
2. Sjekk at port 11434 er ledig
3. Sjekk at du har lastet ned minst en modell:
   ```bash
   ollama list
   ```

### "Cannot connect to OLLAMA"

**Problem:** Dashboard kan ikke koble til

**Løsning:**
```bash
# Terminal 1:
ollama serve

# Terminal 2:
curl http://localhost:11434/api/tags
# Skal vise JSON med modeller
```

### Liten modell? Laster langt?

**Problem:** Modellen er stor (3-10GB)

**Løsning:**
1. Bruk `mistral` i stedet (mindre)
2. Sjekk internett-hastighet
3. Vent - det tar tid første gang

### Memory/RAM error

**Problem:** "Out of memory"

**Løsning:**
1. Lukk andre programmer
2. Bruk mindre modell (mistral)
3. Øk virtual memory
4. Kjøp mer RAM 😅

### CPU helt full?

**Problem:** Datamasinen frøs mens agenten tenker

**Løsning:**
1. Bruk mindre modell
2. Omstart agenten
3. Kjør ikke andre tunge programmer
4. Vent på respons

---

## 📊 Modellstørrelse & Minne

| Modell | Size | RAM |
|--------|------|-----|
| mistral | 4.1GB | 4GB |
| neural-chat | 4.7GB | 4GB |
| codellama | 3.8GB | 4GB |
| llama2 | 3.8GB | 6GB |
| llama2-13b | 7.3GB | 8GB |

**Anbefaling:**
- 4GB RAM → mistral eller neural-chat
- 8GB RAM → codellama eller llama2
- 16GB+ RAM → llama2-13b

---

## 🚀 Optimization Tips

### Raskere Respons

```bash
# Lagre modell i minne (forhåndslast)
ollama pull neural-chat

# Bruk raskere modell
ollama pull mistral
```

### Bedre Koderespons

```bash
# Spesialisert kodemodell
ollama pull codellama
```

### Offline Modus

OLLAMA kjører 100% offline - ingen internett nødvendig!

```bash
ollama serve
# Nå kan du arbeide uten internet
```

---

## 🔄 Bytting av Modell

**1. Sett miljøvariabel:**

Windows:
```cmd
set OLLAMA_MODEL=codellama
run.bat
```

macOS/Linux:
```bash
export OLLAMA_MODEL=codellama
./run.sh
```

**2. Eller endre i `config/settings.yaml`:**
```yaml
agent:
  model: "codellama"
```

**3. Restart agenten**

---

## ❓ FAQ

**Q: Er OLLAMA gratis?**
A: Ja! 100% gratis og open source

**Q: Trenger jeg internet?**
A: Kun for å laste ned modellen første gangen. Etter det: 100% offline

**Q: Hvor mye RAM trenger jeg?**
A: Min 4GB, anbefalt 8GB+

**Q: Kan jeg bruke GPU?**
A: Ja! OLLAMA bruker GPU automatisk hvis tilgjengelig

**Q: Hvor lagres modellene?**
A: ~/.ollama/models (Linux/macOS) eller %USERPROFILE%\.ollama (Windows)

**Q: Kan jeg slette en modell?**
A: `ollama rm neural-chat`

**Q: Hvilken modell er best?**
A: neural-chat for balanse, codellama for kode

---

## 🎯 Neste Steg

1. ✅ Install OLLAMA
2. ✅ Download modell
3. ✅ Start `ollama serve`
4. ✅ Kjør dashboard
5. ✅ Test agenten!

**Done! Du har en SMART AI Code Agent!** 🎉

---

## 📚 Ressurser

- OLLAMA: https://ollama.ai
- Modeller: https://ollama.ai/models
- Dokumentasjon: https://github.com/ollama/ollama

---

**Lykke til! 🚀**
