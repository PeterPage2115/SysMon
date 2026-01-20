# Force Update - Unraid Cache Issue

## Problem
Unraid używa starego obrazu z cache mimo ustawienia nowego tagu `0.1.1`.

## Rozwiązanie 1: Usuń stary obraz i force pull

1. **STOP kontener sysmon**

2. **Usuń stary obraz** (przez terminal Unraid):
   ```bash
   docker images | grep sysmon
   docker rmi peterpage2115/sysmon:0.1.1
   docker rmi peterpage2115/sysmon:latest
   docker rmi peterpage2115/sysmon:0.1
   ```

3. **Force pull nowego obrazu**:
   ```bash
   docker pull peterpage2115/sysmon:0.1.1
   ```

4. **START kontener**

## Rozwiązanie 2: Użyj tagu SHA (gwarantowane nowy)

1. **STOP kontener**

2. **EDIT kontener**:
   - Zmień Repository na: `peterpage2115/sysmon:main-736c9c3`
   - Ten tag jest unikalny i na pewno pobierze nowy obraz

3. **Apply**

## Weryfikacja po starcie:

```bash
# Sprawdź logi - powinno być:
docker logs sysmon | head -20
# 🚀 Starting SysMon v0.1.1...
# ✓ Docker API connected - Docker v24.x.x

# Sprawdź health:
curl http://192.168.1.164:8001/api/health
# Powinno być: "version":"0.1.1","docker_available":true
```

## Dlaczego to się stało?

Docker Hub utworzył nowy obraz z tagiem `0.1.1`, ale Unraid miał już lokalnie obraz z tym samym tagiem (stary). Docker nie sprawdza automatycznie czy tag się zmienił - trzeba wymusić pobranie nowego.

Tag SHA (`main-736c9c3`) jest unikalny dla każdego commita, więc zawsze pobierze dokładnie ten obraz.
