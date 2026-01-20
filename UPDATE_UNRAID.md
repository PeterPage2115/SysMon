# 🔄 Force Update SysMon in Unraid

## ⚡ NOWA WERSJA: v0.1.1 (commit 67a8cb7)

**WAŻNA POPRAWKA**: Całkowicie przepisany Docker SDK - używamy teraz `APIClient` zamiast `DockerClient` aby ominąć problemy z auto-detekcją w środowisku kontenerowym.

---

## Szybka aktualizacja

Użyj najnowszego tagu z wersją:

```
peterpage2115/sysmon:0.1
```

Lub konkretnego commit SHA:

```
peterpage2115/sysmon:main-67a8cb7
```

### Jak zaktualizować w Unraid:
1. **STOP** kontenera SysMon
2. Kliknij **EDIT**
3. Zmień **Repository** na: `peterpage2115/sysmon:0.1`
4. Kliknij **Apply** - wymusi pobranie nowego obrazu
5. Sprawdź logi

---

## Rozwiązanie 2: Ręczny pull przez terminal

Jeśli wolisz zostać przy tagu `latest`, wymuś pull ręcznie:

```bash
# 1. Zatrzymaj i usuń stary kontener
docker stop sysmon
docker rm sysmon

# 2. Usuń stary obraz z cache
docker rmi peterpage2115/sysmon:latest

# 3. Wymuś pobranie najnowszego obrazu
docker pull peterpage2115/sysmon:latest

# 4. Sprawdź czy obraz jest świeży
docker inspect peterpage2115/sysmon:latest | grep Created
```

**Oczekiwana data**: 2026-01-20 (dzisiejsza)

Po wykonaniu: Utwórz kontener ponownie przez Unraid UI.

---

## Rozwiązanie 3: Użyj digest obrazu

Sprawdź najnowszy digest na Docker Hub:
https://hub.docker.com/r/peterpage2115/sysmon/tags

Użyj formatu:
```
peterpage2115/sysmon@sha256:XXXXX
```

---

## ✅ Weryfikacja poprawki

Po uruchomieniu nowej wersji sprawdź logi:

```bash
docker logs sysmon | head -20
```

**v0.1.1 powinno pokazywać**:
```
🚀 Starting SysMon v0.1.1...
🔍 DOCKER_HOST environment: NOT_SET (lub inna wartość)
✓ Docker API connected - Docker v24.x.x    <-- TO!
✓ Started background stats broadcaster
```

**NIE powinno być**:
```
⚠ Docker API unavailable: Error while fetching server API version: Not supported URL scheme http+docker
```

---

## 📊 Sprawdź wersję przez API

```bash
curl http://TWOJ-UNRAID-IP:8001/api/health
```

Odpowiedź powinna zawierać:
```json
{
  "status": "healthy",
  "service": "SysMon",
  "version": "0.1.1",
  "docker_available": true    <-- TO musi być true!
}
```

---

## 🏷️ Dostępne wersje obrazów

- `latest` - zawsze najnowsza wersja (może być cache problem)
- `0.1` - semantic version (v0.1.x)
- `main-67a8cb7` - konkretny commit SHA
- `main-96b7d41` - poprzedni commit

**Zalecane**: Używaj `0.1` dla stabilności lub `main-XXXXX` dla najnowszych zmian.
