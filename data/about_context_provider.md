---
summary: Bemutatkozó tudás a Context Provider integrációról, működéséről és céljáról a Home Assistant környezetben.
keywords:
  - context provider
  - asszisztens
  - integráció
  - önreflexió
  - home assistant
  - tudásbázis
---

- A Context Provider egy lokálisan futó Home Assistant integráció.
- Feladata, hogy tematikusan rendszerezze és az AI számára elérhetővé tegye az otthon működéséről szóló tudást.
- A tudás fájlokban van tárolva, YAML alapú `frontmatter` és Markdown `pontok` formájában.
- Minden fájl tartalmaz egy rövid `summary` leírást, és kulcsszavakat (`keywords`), hogy könnyebben beazonosítható és indexelhető legyen.
- Az asszisztens (AI) kérdés esetén csak a legrelevánsabb tudásfájlokat tölti be, hogy optimalizálja a kontextust.
- A rendszer képes felismerni, ha egy kérdés több témakört is érint, és ilyenkor bővíti a kontextust (pl. „bojler” + „energia”).
- A beszélgetés során az asszisztens új tényeket is felismerhet, és automatikusan bejegyezheti a megfelelő témába.
- Mindez teljesen helyben, az otthoni hálózaton történik – semmilyen tudás nem kerül ki külső szerverre.
- A cél: egy intelligens, magát folyamatosan tanító otthoni asszisztens, amely valódi kontextusban gond
