# 🔄 Force Update SysMon in Unraid

Unraid może pokazywać "up-to-date" mimo że są nowe zmiany w obrazie `latest`. To jest problem cache Docker Hub.

## Rozwiązanie 1: Użyj konkretnego commit SHA

Zamiast `peterpage2115/sysmon:latest`, użyj najnowszego commit SHA:

```
peterpage2115/sysmon:main-6f284f1
```

### Jak zmienić w Unraid:
1. Idź do Docker tab
2. Kliknij **EDIT** przy kontenerze SysMon
3. W polu **Repository** zmień na: `peterpage2115/sysmon:main-6f284f1`
4. Kliknij **Apply**
5. Unraid wymusi pobranie nowego obrazu

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

## Weryfikacja poprawki

Po uruchomieniu nowego obrazu sprawdź logi:

```bash
docker logs sysmon | head -20
```

**Oczekiwany output** (powinno być):
```
✓ Docker SDK connected
✓ Started background stats broadcaster
```

**NIE powinno być**:
```
⚠ Docker SDK unavailable: Error while fetching server API version: Not supported URL scheme http+docker
```

---

## Debug: Sprawdź wersję obrazu

```bash
# Sprawdź kiedy obraz został stworzony
docker inspect peterpage2115/sysmon:latest | grep -A 5 Created

# Sprawdź labels (powinny być webui i icon)
docker inspect peterpage2115/sysmon:latest | grep net.unraid

# Sprawdź warstwy obrazu
docker history peterpage2115/sysmon:latest | head -10
```

---

## Najnowsze zmiany (commit 6f284f1):

- ✅ Poprawiono Docker SDK: `unix:///var/run/docker.sock` (3 slashe)
- ✅ Dodano Unraid labels (webui + icon) do Dockerfile
- ✅ Wszystkie 19 testów przechodzą
- ✅ Frontend działający poprawnie

---

## Pomoc

Jeśli nadal widzisz błąd "Not supported URL scheme", to znaczy że używasz **starego obrazu**.

Najszybsze rozwiązanie: **Użyj Rozwiązania 1** (commit SHA tag).
