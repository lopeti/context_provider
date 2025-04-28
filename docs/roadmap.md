# 🛣️ Home Assistant Context Provider – Roadmap

## ✅ Done (Kész)

| Funkció | Részletek |
| :-- | :-- |
| Projekt alapdefiníció | AI-alapú dinamikus tudáskezelő rendszer Home Assistant Conversation Agenthez |
| CRUD műveletek | `InsertFact`, `EditFact`, `DeleteFact` intentek első verziója |
| Új téma létrehozás | `CreateTopic` intent alapműködés |
| Pending Fact Capture | `CapturePendingFact` intent első implementációja |
| Modular Prompt Builder | Jinja-alapú, dinamikusan bővíthető promptstruktúra |
| Projektinstrukciók dokumentálása | `docs/` mappa létrehozása verziózott dokumentációval |

---

## 🚧 In Progress (Folyamatban)

| Funkció | Részletek |
| :-- | :-- |
| `CapturePendingFactIntentHandler` éles tesztelése | Új tények sikeres begyűjtése a rendszerbe |
| History Management Workflow | Event aggregator tervezése, napi összefoglalók AI-val való generálása |
| Special Instructions kezelés | Tudásfájlokból származó utasítások injektálása a session promptba |
| Projekt Roadmap és Changelog bővítése | Dokumentáció frissítése, verziózás bevezetése |

---

## 🛠 Planned (Tervezett)

| Funkció | Részletek |
| :-- | :-- |
| Event Aggregator modul (`event_aggregator.py`) | Home Assistant események összegyűjtése és előfeldolgozása napi szinten |
| AI alapú napi összefoglaló generálás | Napi eseményekből rövid összefoglaló szöveg írása Google Gemini API segítségével |
| Daily History File Writer | `/data/history/YYYY-MM-DD.md` fájlok automatikus létrehozása naponta |
| Daily Summaries Topic Updater | `daily_summaries.md` fact topik rendszeres frissítése fontosabb eseményekkel |
| Pending Facts konszolidációs workflow | Nap végén a pending tények rendszerezése meglévő vagy új topikokba |
| Dynamic Topic Loading Optimization | Session promptba betöltendő tudás dinamikus szűrése kérdés alapján |
| Auto-setup első user élmény javítása | Alap prompt és template illesztés automatizálása új telepítéseknél |
| AI Backend Flexibility | Alap Google Gemini API támogatás mellett felkészülés más modellek integrációjára (pl. OpenAI, Claude, open-source modellek) |

---

## 📈 Roadmap Frissítési Szabályok

- Minden nagyobb funkció elkészültekor → "Done" oszlopba kerül.
- Minden új stratégiai irány vagy nagyobb terv → "Planned" szekcióba kerül.
- Verziófrissítéssel együtt a Roadmap is frissül (`roadmap.md` és `changelog.md` szinkronban).
- Mindig a `docs/` könyvtárban található a naprakész dokumentáció.

---

## 🚀 Aktuális Projektállapot

| Állapot | Verzió | Státusz |
| :-- | :-- | :-- |
| Projektverzió | 0.2 | Frissítve |
| Roadmap státusz | Naprakész | ✔️ |

---

## 🧩 Megjegyzés

A roadmap **rugalmas**, az aktuális fejlesztési prioritások szerint frissülhet.

A fő fókusz jelenleg:
- CapturePendingFactIntentHandler validálása
- History Management első verziója
- Pending Facts konszolidációs workflow elindítása
