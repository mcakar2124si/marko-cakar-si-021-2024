# Rezultati pokretanja

## Okruženje i postavka merenja

- **Procesor:** Intel64 Family 6 Model 165 Stepping 5, GenuineIntel
- **Logičkih jezgara:** 16
- **OS:** Windows-11-10.0.26200-SP0
- **Python:** CPython 3.14.7 (GIL uključen)
- **numpy:** 2.5.4
- **Semena:** 25430, 97923, 2026
- **Mereno:** zidno vreme (`time.perf_counter`) od početka pretrage do konačne arhive; upis rezultata i ispis nisu uključeni. Kod više procesa uključeno je i pokretanje procesa (spawn) i prikupljanje rezultata. Svako pokretanje izvršeno je jednom po semenu, bez zagrevanja.
- **Hipervolumen:** `hv3d` iz postavke, normalizacija lo = (0, 0, 0), hi = (10, 10, 10), ref = (-0.1, -0.1, -0.1).

## Zbirna tabela (prosek po semenima)

| Pokretanje | P×T | λ | Topologija | E | Vreme [s] | Ubrzanje prema P1 | Iteracija [ms] | Ažuriranje (rangiranje) [ms] | Evaluacija | Arhiva | Hipervolumen (± std) | Poslato kandidata |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 | 1×1 | 1.5 | - | - | 22.88 | 1.00× | 91.3 | 2.43 | 5000 | 5.3 | 0.4300 ± 0.1113 | - |
| P2 | 1×8 | 1.5 | - | - | 5.19 | 4.41× | 20.0 | 5.31 | 5000 | 5.3 | 0.4300 ± 0.1113 | - |
| P3 | 4×1 | 1.5, 1.5, 1.5, 1.5 | prsten | 5 | 6.06 | 3.78× | 92.6 | 2.70 | 5000 | 4.0 | 0.3354 ± 0.0501 | 99 |
| P4 | 4×1 | 0.8, 1.2, 1.9, 2.6 | prsten | 5 | 6.08 | 3.76× | 93.0 | 2.53 | 5000 | 3.0 | 0.2848 ± 0.0942 | 99 |
| P5 | 4×1 | 0.8, 1.2, 1.9, 2.6 | zvezda | 5 | 6.06 | 3.77× | 92.9 | 2.52 | 5000 | 3.3 | 0.2789 ± 0.0988 | 147 |
| P6 | 4×1 | 0.8, 1.2, 1.9, 2.6 | prsten | 10 | 6.05 | 3.78× | 92.4 | 2.59 | 5000 | 3.0 | 0.2726 ± 0.0599 | 56 |

## P1

Parametri: P×T = 1×1, λ = (1.5), topologija = -, E = -, B = 5000, N = 50, k = 3, M = 20, K = 5, G = 100

### P1, seme 25430

- Ukupno trajanje: 22.85 s
- Završenih evaluacija: 5000
- Iteracija: 248, prosečno trajanje iteracije: 91.2 ms (od toga ažuriranje populacije i rangiranje: 2.41 ms)
- Veličina konačne arhive: 4
- Rasponi ocena (zaraznost, virulentnost, imunoevazivnost): [4.50, 10.00] [1.80, 9.00] [3.00, 10.00]
- Hipervolumen: 0.5564

| Sekvenca | Zaraznost | Virulentnost | Imunoevazivnost | Poreklo (proces) |
|---|---|---|---|---|
| `NEIYQAGSTPCNGVAGPNCYHPLQSYGFQPTY` | 10 | 1.8 | 10 | 0 |
| `NEIYQAGSTPCNGVAGINCYHPLQSYGFQPTY` | 8.14 | 2.39 | 7.66 | 0 |
| `TEIYQAGSTPCNGVAGFNCYHPLQSYGFQPTY` | 7.5 | 3 | 6.5 | 0 |
| `TEIYQAGSKPCNGVEGFNCYFPLQSYGFQPTN` | 4.5 | 9 | 3 | 0 |

### P1, seme 97923

- Ukupno trajanje: 22.84 s
- Završenih evaluacija: 5000
- Iteracija: 248, prosečno trajanje iteracije: 91.2 ms (od toga ažuriranje populacije i rangiranje: 2.34 ms)
- Veličina konačne arhive: 10
- Rasponi ocena (zaraznost, virulentnost, imunoevazivnost): [2.00, 7.66] [1.43, 6.85] [2.24, 7.64]
- Hipervolumen: 0.3466

| Sekvenca | Zaraznost | Virulentnost | Imunoevazivnost | Poreklo (proces) |
|---|---|---|---|---|
| `REIYQAGSTPCNGVAGPNCYHPLQSYGFQPTY` | 7.66 | 1.43 | 7.64 | 0 |
| `EEIYQAGSTPCNGVAGPNCYHPLQSYGFQPTY` | 7.66 | 1.43 | 7.64 | 0 |
| `TEIYQAGSTPCNGVAGPNCYHPLQSYGFQPTY` | 7.52 | 1.5 | 7.45 | 0 |
| `TEIYQAGSTPCNGVAGFNCYHPLQSYGFQPTY` | 7.5 | 3 | 6.5 | 0 |
| `TEIYQAGSQPCNGVEGFNCYFPLQSYGFQPTN` | 3.29 | 6.85 | 2.24 | 0 |
| `TEIYQAGSTPCNGVKGFNCYNPLQSYGFQPTY` | 2.24 | 3.13 | 2.83 | 0 |
| `TEIYQAGSTPCNGVAGFNCYFPLQSYGFQPTY` | 2.12 | 3.88 | 2.38 | 0 |
| `TEIYQAGSTPCNGVKGFNCYEPLQSYGFQPTY` | 2.06 | 3.2 | 2.72 | 0 |
| `TEIYQAGSTPCNGVKGFNCYRPLQSYGFQPTY` | 2.06 | 3.2 | 2.72 | 0 |
| `TEIYQAGSTPCNGVKGFNCYFPLQSYGFQPTY` | 2 | 5 | 4 | 0 |

### P1, seme 2026

- Ukupno trajanje: 22.95 s
- Završenih evaluacija: 5000
- Iteracija: 248, prosečno trajanje iteracije: 91.6 ms (od toga ažuriranje populacije i rangiranje: 2.55 ms)
- Veličina konačne arhive: 2
- Rasponi ocena (zaraznost, virulentnost, imunoevazivnost): [4.50, 7.50] [3.00, 9.00] [3.00, 6.50]
- Hipervolumen: 0.3870

| Sekvenca | Zaraznost | Virulentnost | Imunoevazivnost | Poreklo (proces) |
|---|---|---|---|---|
| `TEIYQAGSTPCNGVAGFNCYHPLQSYGFQPTY` | 7.5 | 3 | 6.5 | 0 |
| `TEIYQAGSKPCNGVEGFNCYFPLQSYGFQPTN` | 4.5 | 9 | 3 | 0 |

## P2

Parametri: P×T = 1×8, λ = (1.5), topologija = -, E = -, B = 5000, N = 50, k = 3, M = 20, K = 5, G = 100

### P2, seme 25430

- Ukupno trajanje: 5.20 s
- Završenih evaluacija: 5000
- Iteracija: 248, prosečno trajanje iteracije: 20.1 ms (od toga ažuriranje populacije i rangiranje: 5.37 ms)
- Veličina konačne arhive: 4
- Rasponi ocena (zaraznost, virulentnost, imunoevazivnost): [4.50, 10.00] [1.80, 9.00] [3.00, 10.00]
- Hipervolumen: 0.5564

| Sekvenca | Zaraznost | Virulentnost | Imunoevazivnost | Poreklo (proces) |
|---|---|---|---|---|
| `NEIYQAGSTPCNGVAGPNCYHPLQSYGFQPTY` | 10 | 1.8 | 10 | 0 |
| `NEIYQAGSTPCNGVAGINCYHPLQSYGFQPTY` | 8.14 | 2.39 | 7.66 | 0 |
| `TEIYQAGSTPCNGVAGFNCYHPLQSYGFQPTY` | 7.5 | 3 | 6.5 | 0 |
| `TEIYQAGSKPCNGVEGFNCYFPLQSYGFQPTN` | 4.5 | 9 | 3 | 0 |

### P2, seme 97923

- Ukupno trajanje: 5.13 s
- Završenih evaluacija: 5000
- Iteracija: 248, prosečno trajanje iteracije: 19.8 ms (od toga ažuriranje populacije i rangiranje: 5.07 ms)
- Veličina konačne arhive: 10
- Rasponi ocena (zaraznost, virulentnost, imunoevazivnost): [2.00, 7.66] [1.43, 6.85] [2.24, 7.64]
- Hipervolumen: 0.3466

| Sekvenca | Zaraznost | Virulentnost | Imunoevazivnost | Poreklo (proces) |
|---|---|---|---|---|
| `REIYQAGSTPCNGVAGPNCYHPLQSYGFQPTY` | 7.66 | 1.43 | 7.64 | 0 |
| `EEIYQAGSTPCNGVAGPNCYHPLQSYGFQPTY` | 7.66 | 1.43 | 7.64 | 0 |
| `TEIYQAGSTPCNGVAGPNCYHPLQSYGFQPTY` | 7.52 | 1.5 | 7.45 | 0 |
| `TEIYQAGSTPCNGVAGFNCYHPLQSYGFQPTY` | 7.5 | 3 | 6.5 | 0 |
| `TEIYQAGSQPCNGVEGFNCYFPLQSYGFQPTN` | 3.29 | 6.85 | 2.24 | 0 |
| `TEIYQAGSTPCNGVKGFNCYNPLQSYGFQPTY` | 2.24 | 3.13 | 2.83 | 0 |
| `TEIYQAGSTPCNGVAGFNCYFPLQSYGFQPTY` | 2.12 | 3.88 | 2.38 | 0 |
| `TEIYQAGSTPCNGVKGFNCYEPLQSYGFQPTY` | 2.06 | 3.2 | 2.72 | 0 |
| `TEIYQAGSTPCNGVKGFNCYRPLQSYGFQPTY` | 2.06 | 3.2 | 2.72 | 0 |
| `TEIYQAGSTPCNGVKGFNCYFPLQSYGFQPTY` | 2 | 5 | 4 | 0 |

### P2, seme 2026

- Ukupno trajanje: 5.23 s
- Završenih evaluacija: 5000
- Iteracija: 248, prosečno trajanje iteracije: 20.2 ms (od toga ažuriranje populacije i rangiranje: 5.50 ms)
- Veličina konačne arhive: 2
- Rasponi ocena (zaraznost, virulentnost, imunoevazivnost): [4.50, 7.50] [3.00, 9.00] [3.00, 6.50]
- Hipervolumen: 0.3870

| Sekvenca | Zaraznost | Virulentnost | Imunoevazivnost | Poreklo (proces) |
|---|---|---|---|---|
| `TEIYQAGSTPCNGVAGFNCYHPLQSYGFQPTY` | 7.5 | 3 | 6.5 | 0 |
| `TEIYQAGSKPCNGVEGFNCYFPLQSYGFQPTN` | 4.5 | 9 | 3 | 0 |

## P3

Parametri: P×T = 4×1, λ = (1.5, 1.5, 1.5, 1.5), topologija = prsten, E = 5, B = 5000, N = 50, k = 3, M = 20, K = 5, G = 100

### P3, seme 25430

- Ukupno trajanje: 6.12 s
- Završenih evaluacija: 5000
- Iteracija: 60, prosečno trajanje iteracije: 93.1 ms (od toga ažuriranje populacije i rangiranje: 3.01 ms)
- Veličina konačne arhive: 3
- Rasponi ocena (zaraznost, virulentnost, imunoevazivnost): [2.00, 7.50] [3.00, 9.00] [3.00, 6.50]
- Hipervolumen: 0.3930
- Poreklo tačaka konačne arhive (proces: broj): 2: 1, 3: 2
- Sekvenci ocenjenih u više procesa (ponovljen rad): 63
- Procesi koji su pali: nijedan

| Proces | λ | Evaluacija | Iteracija | Iteracija [ms] | Poslato | Primljeno | Primljeno novih | Lokalna arhiva | Iz drugih procesa | Ostalo u redu |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1.5 | 1250 | 60 | 93.0 | 33 | 23 | 7 | 3 | 3 | 3 |
| 1 | 1.5 | 1250 | 60 | 93.0 | 36 | 30 | 13 | 3 | 3 | 3 |
| 2 | 1.5 | 1250 | 60 | 93.2 | 30 | 33 | 16 | 3 | 2 | 3 |
| 3 | 1.5 | 1250 | 60 | 93.3 | 26 | 27 | 12 | 3 | 1 | 3 |

| Sekvenca | Zaraznost | Virulentnost | Imunoevazivnost | Poreklo (proces) |
|---|---|---|---|---|
| `TEIYQAGSTPCNGVAGFNCYHPLQSYGFQPTY` | 7.5 | 3 | 6.5 | 3 |
| `TEIYQAGSKPCNGVEGFNCYFPLQSYGFQPTN` | 4.5 | 9 | 3 | 2 |
| `TEIYQAGSTPCNGVKGFNCYFPLQSYGFQPTY` | 2 | 5 | 4 | 3 |

### P3, seme 97923

- Ukupno trajanje: 6.01 s
- Završenih evaluacija: 5000
- Iteracija: 60, prosečno trajanje iteracije: 92.1 ms (od toga ažuriranje populacije i rangiranje: 2.54 ms)
- Veličina konačne arhive: 5
- Rasponi ocena (zaraznost, virulentnost, imunoevazivnost): [4.50, 6.01] [1.25, 9.00] [3.00, 5.97]
- Hipervolumen: 0.3025
- Poreklo tačaka konačne arhive (proces: broj): 0: 1, 3: 4
- Sekvenci ocenjenih u više procesa (ponovljen rad): 52
- Procesi koji su pali: nijedan

| Proces | λ | Evaluacija | Iteracija | Iteracija [ms] | Poslato | Primljeno | Primljeno novih | Lokalna arhiva | Iz drugih procesa | Ostalo u redu |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1.5 | 1250 | 60 | 91.9 | 22 | 20 | 6 | 4 | 3 | 4 |
| 1 | 1.5 | 1250 | 60 | 92.2 | 19 | 18 | 7 | 4 | 3 | 4 |
| 2 | 1.5 | 1250 | 60 | 92.1 | 24 | 15 | 5 | 3 | 2 | 4 |
| 3 | 1.5 | 1250 | 60 | 92.0 | 24 | 21 | 4 | 4 | 0 | 3 |

| Sekvenca | Zaraznost | Virulentnost | Imunoevazivnost | Poreklo (proces) |
|---|---|---|---|---|
| `NEIYQAGSTPCNGVEGPNCYHPLQSYGFQPIY` | 6.01 | 1.25 | 5.97 | 3 |
| `NEIYQAGSTPCNGVYGVNCYHPLQSYGFQPTY` | 5.8 | 1.7 | 5.49 | 3 |
| `TEIYQAGSTPCNGVMGFNCYHPLQSYGFQPTY` | 5.63 | 2.39 | 4.92 | 0 |
| `NEIYQAGSTPCNGVEGLNCYHPLQSYGFQPTY` | 5.54 | 1.81 | 5.23 | 3 |
| `TEIYQAGSKPCNGVEGFNCYFPLQSYGFQPTN` | 4.5 | 9 | 3 | 3 |

### P3, seme 2026

- Ukupno trajanje: 6.04 s
- Završenih evaluacija: 5000
- Iteracija: 60, prosečno trajanje iteracije: 92.5 ms (od toga ažuriranje populacije i rangiranje: 2.55 ms)
- Veličina konačne arhive: 4
- Rasponi ocena (zaraznost, virulentnost, imunoevazivnost): [4.50, 6.30] [2.53, 9.00] [3.00, 5.46]
- Hipervolumen: 0.3106
- Poreklo tačaka konačne arhive (proces: broj): 0: 2, 1: 1, 2: 1
- Sekvenci ocenjenih u više procesa (ponovljen rad): 50
- Procesi koji su pali: nijedan

| Proces | λ | Evaluacija | Iteracija | Iteracija [ms] | Poslato | Primljeno | Primljeno novih | Lokalna arhiva | Iz drugih procesa | Ostalo u redu |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1.5 | 1250 | 60 | 92.3 | 25 | 15 | 7 | 4 | 1 | 2 |
| 1 | 1.5 | 1250 | 60 | 92.6 | 26 | 21 | 9 | 4 | 3 | 4 |
| 2 | 1.5 | 1250 | 60 | 92.5 | 16 | 22 | 8 | 2 | 1 | 4 |
| 3 | 1.5 | 1250 | 60 | 92.5 | 17 | 14 | 5 | 2 | 2 | 2 |

| Sekvenca | Zaraznost | Virulentnost | Imunoevazivnost | Poreklo (proces) |
|---|---|---|---|---|
| `TEIYQAGSTPCNGAAGFNCYHPLQSYGFQPTY` | 6.3 | 2.53 | 5.46 | 1 |
| `TEIYQAGSTPCNGVEGFNCYHPLQSYGFQPTY` | 5.01 | 2.69 | 4.34 | 0 |
| `TEIYQAGSTPCNGVKGFNCYHPLQSYGFQPTY` | 4.99 | 2.63 | 4.59 | 0 |
| `TEIYQAGSKPCNGVEGFNCYFPLQSYGFQPTN` | 4.5 | 9 | 3 | 2 |

## P4

Parametri: P×T = 4×1, λ = (0.8, 1.2, 1.9, 2.6), topologija = prsten, E = 5, B = 5000, N = 50, k = 3, M = 20, K = 5, G = 100

### P4, seme 25430

- Ukupno trajanje: 6.03 s
- Završenih evaluacija: 5000
- Iteracija: 60, prosečno trajanje iteracije: 92.3 ms (od toga ažuriranje populacije i rangiranje: 2.50 ms)
- Veličina konačne arhive: 4
- Rasponi ocena (zaraznost, virulentnost, imunoevazivnost): [2.00, 4.50] [2.44, 9.00] [3.00, 4.00]
- Hipervolumen: 0.2404
- Poreklo tačaka konačne arhive (proces: broj): 0: 2, 1: 1, 2: 1
- Sekvenci ocenjenih u više procesa (ponovljen rad): 45
- Procesi koji su pali: nijedan

| Proces | λ | Evaluacija | Iteracija | Iteracija [ms] | Poslato | Primljeno | Primljeno novih | Lokalna arhiva | Iz drugih procesa | Ostalo u redu |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0.8 | 1250 | 60 | 92.5 | 22 | 25 | 9 | 4 | 2 | 4 |
| 1 | 1.2 | 1250 | 60 | 92.3 | 26 | 18 | 4 | 4 | 1 | 4 |
| 2 | 1.9 | 1250 | 60 | 92.2 | 28 | 22 | 7 | 4 | 3 | 4 |
| 3 | 2.6 | 1250 | 60 | 92.3 | 29 | 24 | 9 | 4 | 4 | 4 |

| Sekvenca | Zaraznost | Virulentnost | Imunoevazivnost | Poreklo (proces) |
|---|---|---|---|---|
| `TEIYQAGSKPCNGVEGFNCYFPLQSYGFQPTN` | 4.5 | 9 | 3 | 0 |
| `TEIYQAGSTPCNGVSGFNCYNPLQSYGFQPTY` | 3.73 | 2.44 | 3.41 | 2 |
| `TEIYQAGSTPCNGVSGFNCYQPLQSYGFQPTY` | 3.29 | 2.46 | 3.06 | 1 |
| `TEIYQAGSTPCNGVKGFNCYFPLQSYGFQPTY` | 2 | 5 | 4 | 0 |

### P4, seme 97923

- Ukupno trajanje: 6.07 s
- Završenih evaluacija: 5000
- Iteracija: 60, prosečno trajanje iteracije: 92.9 ms (od toga ažuriranje populacije i rangiranje: 2.59 ms)
- Veličina konačne arhive: 2
- Rasponi ocena (zaraznost, virulentnost, imunoevazivnost): [3.31, 4.50] [2.12, 9.00] [3.00, 3.07]
- Hipervolumen: 0.2209
- Poreklo tačaka konačne arhive (proces: broj): 1: 1, 2: 1
- Sekvenci ocenjenih u više procesa (ponovljen rad): 29
- Procesi koji su pali: nijedan

| Proces | λ | Evaluacija | Iteracija | Iteracija [ms] | Poslato | Primljeno | Primljeno novih | Lokalna arhiva | Iz drugih procesa | Ostalo u redu |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0.8 | 1250 | 60 | 92.9 | 18 | 13 | 3 | 1 | 1 | 1 |
| 1 | 1.2 | 1250 | 60 | 92.9 | 14 | 17 | 3 | 1 | 0 | 1 |
| 2 | 1.9 | 1250 | 60 | 92.9 | 17 | 13 | 5 | 2 | 1 | 1 |
| 3 | 2.6 | 1250 | 60 | 93.0 | 14 | 15 | 6 | 1 | 1 | 2 |

| Sekvenca | Zaraznost | Virulentnost | Imunoevazivnost | Poreklo (proces) |
|---|---|---|---|---|
| `TEIYQAGSKPCNGVEGFNCYFPLQSYGFQPTN` | 4.5 | 9 | 3 | 1 |
| `TEIYQAGSTPCNGVRGFNCYHPLQSYGFQPTV` | 3.31 | 2.12 | 3.07 | 2 |

### P4, seme 2026

- Ukupno trajanje: 6.14 s
- Završenih evaluacija: 5000
- Iteracija: 60, prosečno trajanje iteracije: 93.8 ms (od toga ažuriranje populacije i rangiranje: 2.50 ms)
- Veličina konačne arhive: 3
- Rasponi ocena (zaraznost, virulentnost, imunoevazivnost): [2.00, 7.50] [3.00, 9.00] [3.00, 6.50]
- Hipervolumen: 0.3930
- Poreklo tačaka konačne arhive (proces: broj): 0: 2, 2: 1
- Sekvenci ocenjenih u više procesa (ponovljen rad): 63
- Procesi koji su pali: nijedan

| Proces | λ | Evaluacija | Iteracija | Iteracija [ms] | Poslato | Primljeno | Primljeno novih | Lokalna arhiva | Iz drugih procesa | Ostalo u redu |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0.8 | 1250 | 60 | 93.7 | 42 | 20 | 7 | 3 | 1 | 2 |
| 1 | 1.2 | 1250 | 60 | 93.7 | 41 | 39 | 19 | 3 | 2 | 3 |
| 2 | 1.9 | 1250 | 60 | 93.7 | 23 | 38 | 17 | 3 | 2 | 3 |
| 3 | 2.6 | 1250 | 60 | 93.9 | 22 | 20 | 8 | 2 | 2 | 3 |

| Sekvenca | Zaraznost | Virulentnost | Imunoevazivnost | Poreklo (proces) |
|---|---|---|---|---|
| `TEIYQAGSTPCNGVAGFNCYHPLQSYGFQPTY` | 7.5 | 3 | 6.5 | 0 |
| `TEIYQAGSKPCNGVEGFNCYFPLQSYGFQPTN` | 4.5 | 9 | 3 | 2 |
| `TEIYQAGSTPCNGVKGFNCYFPLQSYGFQPTY` | 2 | 5 | 4 | 0 |

## P5

Parametri: P×T = 4×1, λ = (0.8, 1.2, 1.9, 2.6), topologija = zvezda, E = 5, B = 5000, N = 50, k = 3, M = 20, K = 5, G = 100

### P5, seme 25430

- Ukupno trajanje: 6.11 s
- Završenih evaluacija: 5000
- Iteracija: 60, prosečno trajanje iteracije: 93.7 ms (od toga ažuriranje populacije i rangiranje: 2.57 ms)
- Veličina konačne arhive: 3
- Rasponi ocena (zaraznost, virulentnost, imunoevazivnost): [3.29, 4.50] [2.46, 9.00] [3.00, 3.06]
- Hipervolumen: 0.2209
- Poreklo tačaka konačne arhive (proces: broj): 0: 2, 2: 1
- Sekvenci ocenjenih u više procesa (ponovljen rad): 58
- Procesi koji su pali: nijedan

| Proces | λ | Evaluacija | Iteracija | Iteracija [ms] | Poslato | Primljeno | Primljeno novih | Lokalna arhiva | Iz drugih procesa | Ostalo u redu |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0.8 | 1250 | 60 | 93.6 | 51 | 39 | 6 | 3 | 1 | 6 |
| 1 | 1.2 | 1250 | 60 | 93.5 | 14 | 14 | 6 | 2 | 2 | 3 |
| 2 | 1.9 | 1250 | 60 | 93.7 | 14 | 14 | 5 | 2 | 1 | 3 |
| 3 | 2.6 | 1250 | 60 | 93.7 | 17 | 14 | 6 | 2 | 2 | 3 |

| Sekvenca | Zaraznost | Virulentnost | Imunoevazivnost | Poreklo (proces) |
|---|---|---|---|---|
| `TEIYQAGSKPCNGVEGFNCYFPLQSYGFQPTN` | 4.5 | 9 | 3 | 2 |
| `TEIYQAGSTPCNGVSGFNCYEPLQSYGFQPTY` | 3.29 | 2.46 | 3.06 | 0 |
| `TEIYQAGSTPCNGVSGFNCYRPLQSYGFQPTY` | 3.29 | 2.46 | 3.06 | 0 |

### P5, seme 97923

- Ukupno trajanje: 6.05 s
- Završenih evaluacija: 5000
- Iteracija: 60, prosečno trajanje iteracije: 92.8 ms (od toga ažuriranje populacije i rangiranje: 2.55 ms)
- Veličina konačne arhive: 4
- Rasponi ocena (zaraznost, virulentnost, imunoevazivnost): [3.30, 4.50] [1.97, 9.00] [3.00, 3.20]
- Hipervolumen: 0.2228
- Poreklo tačaka konačne arhive (proces: broj): 0: 2, 1: 2
- Sekvenci ocenjenih u više procesa (ponovljen rad): 45
- Procesi koji su pali: nijedan

| Proces | λ | Evaluacija | Iteracija | Iteracija [ms] | Poslato | Primljeno | Primljeno novih | Lokalna arhiva | Iz drugih procesa | Ostalo u redu |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0.8 | 1250 | 60 | 92.8 | 51 | 47 | 6 | 2 | 0 | 8 |
| 1 | 1.2 | 1250 | 60 | 92.6 | 21 | 15 | 4 | 4 | 1 | 2 |
| 2 | 1.9 | 1250 | 60 | 92.9 | 18 | 15 | 5 | 2 | 2 | 2 |
| 3 | 2.6 | 1250 | 60 | 92.8 | 16 | 15 | 4 | 2 | 2 | 2 |

| Sekvenca | Zaraznost | Virulentnost | Imunoevazivnost | Poreklo (proces) |
|---|---|---|---|---|
| `TEIYQAGSKPCNGVEGFNCYFPLQSYGFQPTN` | 4.5 | 9 | 3 | 0 |
| `TEIYQAGSKPCNGVVGFNCYHPLQSFGFQPTY` | 3.58 | 1.97 | 3.2 | 1 |
| `TEIYQAGSTPCNGVCGFNCYQPLQSYGFQPTY` | 3.31 | 2.01 | 3.04 | 1 |
| `TEIYQAGSTPCNGVAGFNCYCPLQSYGFQPTY` | 3.3 | 2.31 | 3.05 | 0 |

### P5, seme 2026

- Ukupno trajanje: 6.03 s
- Završenih evaluacija: 5000
- Iteracija: 60, prosečno trajanje iteracije: 92.2 ms (od toga ažuriranje populacije i rangiranje: 2.46 ms)
- Veličina konačne arhive: 3
- Rasponi ocena (zaraznost, virulentnost, imunoevazivnost): [2.00, 7.50] [3.00, 9.00] [3.00, 6.50]
- Hipervolumen: 0.3930
- Poreklo tačaka konačne arhive (proces: broj): 0: 3
- Sekvenci ocenjenih u više procesa (ponovljen rad): 60
- Procesi koji su pali: nijedan

| Proces | λ | Evaluacija | Iteracija | Iteracija [ms] | Poslato | Primljeno | Primljeno novih | Lokalna arhiva | Iz drugih procesa | Ostalo u redu |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0.8 | 1250 | 60 | 92.1 | 120 | 109 | 15 | 3 | 0 | 9 |
| 1 | 1.2 | 1250 | 60 | 92.1 | 37 | 37 | 15 | 3 | 2 | 3 |
| 2 | 1.9 | 1250 | 60 | 92.3 | 42 | 37 | 21 | 3 | 3 | 3 |
| 3 | 2.6 | 1250 | 60 | 92.3 | 39 | 37 | 20 | 3 | 3 | 3 |

| Sekvenca | Zaraznost | Virulentnost | Imunoevazivnost | Poreklo (proces) |
|---|---|---|---|---|
| `TEIYQAGSTPCNGVAGFNCYHPLQSYGFQPTY` | 7.5 | 3 | 6.5 | 0 |
| `TEIYQAGSKPCNGVEGFNCYFPLQSYGFQPTN` | 4.5 | 9 | 3 | 0 |
| `TEIYQAGSTPCNGVKGFNCYFPLQSYGFQPTY` | 2 | 5 | 4 | 0 |

## P6

Parametri: P×T = 4×1, λ = (0.8, 1.2, 1.9, 2.6), topologija = prsten, E = 10, B = 5000, N = 50, k = 3, M = 20, K = 5, G = 100

### P6, seme 25430

- Ukupno trajanje: 6.06 s
- Završenih evaluacija: 5000
- Iteracija: 60, prosečno trajanje iteracije: 92.8 ms (od toga ažuriranje populacije i rangiranje: 2.71 ms)
- Veličina konačne arhive: 2
- Rasponi ocena (zaraznost, virulentnost, imunoevazivnost): [2.00, 4.50] [5.00, 9.00] [3.00, 4.00]
- Hipervolumen: 0.2380
- Poreklo tačaka konačne arhive (proces: broj): 0: 1, 1: 1
- Sekvenci ocenjenih u više procesa (ponovljen rad): 44
- Procesi koji su pali: nijedan

| Proces | λ | Evaluacija | Iteracija | Iteracija [ms] | Poslato | Primljeno | Primljeno novih | Lokalna arhiva | Iz drugih procesa | Ostalo u redu |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0.8 | 1250 | 60 | 92.8 | 8 | 8 | 3 | 2 | 1 | 2 |
| 1 | 1.2 | 1250 | 60 | 92.8 | 12 | 6 | 2 | 2 | 1 | 2 |
| 2 | 1.9 | 1250 | 60 | 92.8 | 10 | 10 | 5 | 2 | 2 | 2 |
| 3 | 2.6 | 1250 | 60 | 92.7 | 10 | 8 | 3 | 2 | 2 | 2 |

| Sekvenca | Zaraznost | Virulentnost | Imunoevazivnost | Poreklo (proces) |
|---|---|---|---|---|
| `TEIYQAGSKPCNGVEGFNCYFPLQSYGFQPTN` | 4.5 | 9 | 3 | 0 |
| `TEIYQAGSTPCNGVKGFNCYFPLQSYGFQPTY` | 2 | 5 | 4 | 1 |

### P6, seme 97923

- Ukupno trajanje: 6.04 s
- Završenih evaluacija: 5000
- Iteracija: 60, prosečno trajanje iteracije: 92.3 ms (od toga ažuriranje populacije i rangiranje: 2.57 ms)
- Veličina konačne arhive: 3
- Rasponi ocena (zaraznost, virulentnost, imunoevazivnost): [2.00, 4.50] [1.83, 9.00] [3.00, 4.00]
- Hipervolumen: 0.2381
- Poreklo tačaka konačne arhive (proces: broj): 0: 1, 1: 2
- Sekvenci ocenjenih u više procesa (ponovljen rad): 38
- Procesi koji su pali: nijedan

| Proces | λ | Evaluacija | Iteracija | Iteracija [ms] | Poslato | Primljeno | Primljeno novih | Lokalna arhiva | Iz drugih procesa | Ostalo u redu |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0.8 | 1250 | 60 | 92.4 | 7 | 5 | 2 | 1 | 0 | 1 |
| 1 | 1.2 | 1250 | 60 | 92.3 | 10 | 6 | 3 | 3 | 0 | 1 |
| 2 | 1.9 | 1250 | 60 | 92.2 | 10 | 7 | 5 | 3 | 3 | 3 |
| 3 | 2.6 | 1250 | 60 | 92.3 | 6 | 7 | 5 | 1 | 1 | 3 |

| Sekvenca | Zaraznost | Virulentnost | Imunoevazivnost | Poreklo (proces) |
|---|---|---|---|---|
| `TEIYQAGSKPCNGVEGFNCYFPLQSYGFQPTN` | 4.5 | 9 | 3 | 0 |
| `TEIYQAGSTPCNHVAGFNCYNPLQSYGFQPTY` | 3.34 | 1.83 | 3.02 | 1 |
| `TEIYQAGSTPCNGVKGFNCYFPLQSYGFQPTY` | 2 | 5 | 4 | 1 |

### P6, seme 2026

- Ukupno trajanje: 6.04 s
- Završenih evaluacija: 5000
- Iteracija: 60, prosečno trajanje iteracije: 92.2 ms (od toga ažuriranje populacije i rangiranje: 2.50 ms)
- Veličina konačne arhive: 4
- Rasponi ocena (zaraznost, virulentnost, imunoevazivnost): [2.00, 7.50] [3.00, 7.63] [2.53, 6.50]
- Hipervolumen: 0.3418
- Poreklo tačaka konačne arhive (proces: broj): 0: 3, 2: 1
- Sekvenci ocenjenih u više procesa (ponovljen rad): 50
- Procesi koji su pali: nijedan

| Proces | λ | Evaluacija | Iteracija | Iteracija [ms] | Poslato | Primljeno | Primljeno novih | Lokalna arhiva | Iz drugih procesa | Ostalo u redu |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0.8 | 1250 | 60 | 92.1 | 25 | 18 | 15 | 5 | 1 | 5 |
| 1 | 1.2 | 1250 | 60 | 92.3 | 25 | 20 | 12 | 5 | 4 | 5 |
| 2 | 1.9 | 1250 | 60 | 92.1 | 22 | 20 | 13 | 3 | 1 | 5 |
| 3 | 2.6 | 1250 | 60 | 92.3 | 23 | 19 | 14 | 5 | 4 | 3 |

| Sekvenca | Zaraznost | Virulentnost | Imunoevazivnost | Poreklo (proces) |
|---|---|---|---|---|
| `TEIYQAGSTPCNGVAGFNCYHPLQSYGFQPTY` | 7.5 | 3 | 6.5 | 0 |
| `TEIYQAGSRPCNGVEGFNCYFPLQSYGFQPTN` | 3.77 | 7.63 | 2.53 | 2 |
| `TEIYQAGSTPCNGVRGFNCYYPLQSYGFQPTY` | 2.05 | 3.58 | 2.86 | 0 |
| `TEIYQAGSTPCNGVKGFNCYFPLQSYGFQPTY` | 2 | 5 | 4 | 0 |
