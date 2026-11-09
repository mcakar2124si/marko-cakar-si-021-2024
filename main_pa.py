import contextlib
import io
import multiprocessing as mp
import os
import platform
import queue
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

import numpy as np

with contextlib.redirect_stdout(io.StringIO()):     # oceni.py prints two test lines on every import
    from oceni import oceni                         # (once per process with spawn) - silence them

POCETNA = "TEIYQAGSTPCNGVEGFNCYFPLQSYGFQPTN"  # starting sequence
ALFABET = "ACDEFGHIKLMNPQRSTVWY"              # 20 amino acids

TOPOLOGIJE = "prsten", "zvezda", "svi_svima", "nasumicno"

SEMENA = 25430, 97923, 2026  # every run is repeated with each seed

B = 5000  # total evaluation budget (started oceni calls, all processes, incl. initial population)
N = 50    # max population size (parent pool)
k = 3     # max changed positions in an initial mutant
M = 20    # new evaluated candidates per iteration
K = 5     # max candidates sent per exchange
G = 100   # consecutive duplicates before stopping (fixed in code by spec)

INF = float("inf")


@dataclass(frozen=True)
class Pokretanje:
    naziv: str
    B: int
    N: int
    k: int
    M: int
    lambde: tuple[float, ...]  # one λ per process
    T: int                     # threads per process (also ranking pool size)
    P: int                     # number of processes
    K: int
    E: int | None              # exchange every E iterations; None when P = 1
    topologija: str | None     # None when P = 1
    G: int = G


_shared = dict(B=B, N=N, k=k, M=M, K=K)
POKRETANJA: dict[str, Pokretanje] = {
    "P1": Pokretanje("P1", **_shared, P=1, T=1, E=None, lambde=(1.5,),                topologija=None),
    "P2": Pokretanje("P2", **_shared, P=1, T=8, E=None, lambde=(1.5,),                topologija=None),
    "P3": Pokretanje("P3", **_shared, P=4, T=1, E=5,    lambde=(1.5, 1.5, 1.5, 1.5),  topologija="prsten"),
    "P4": Pokretanje("P4", **_shared, P=4, T=1, E=5,    lambde=(0.8, 1.2, 1.9, 2.6),  topologija="prsten"),
    "P5": Pokretanje("P5", **_shared, P=4, T=1, E=5,    lambde=(0.8, 1.2, 1.9, 2.6),  topologija="zvezda"),
    "P6": Pokretanje("P6", **_shared, P=4, T=1, E=10,   lambde=(0.8, 1.2, 1.9, 2.6),  topologija="prsten"),
}


@dataclass
class Brojaci:
    potroseno: int = 0      # started evaluations (budget used)
    neuspesni: int = 0      # consecutive duplicates


def napravi_pocetnu_populaciju(rng, evidencija, budzet=None):
    # budzet: the initial population also spends budget, so it never grows past it
    velicina = N if budzet is None else max(1, min(N, budzet))

    evidencija[POCETNA] = None
    evidencija[POCETNA] = oceni(POCETNA)
    populacija = [POCETNA]

    neuspesni = 0
    while len(populacija) < velicina and neuspesni < G:
        slova = list(POCETNA)
        broj_izmena = rng.integers(1, min(k, len(POCETNA)) + 1)
        pozicije = rng.choice(len(POCETNA), size=broj_izmena, replace=False)
        for pozicija in pozicije:
            preostala = [a for a in ALFABET if a != slova[pozicija]]
            slova[pozicija] = preostala[rng.integers(len(preostala))]
        mutant = "".join(slova)

        if mutant in evidencija:
            neuspesni += 1
            continue
        neuspesni = 0

        evidencija[mutant] = None
        evidencija[mutant] = oceni(mutant)
        populacija.append(mutant)

    return populacija


def dominira(a, b):
    return all(x >= y for x, y in zip(a, b)) and any(x > y for x, y in zip(a, b))


class RangPool(ThreadPoolExecutor):
    # Thread pool used only for Pareto ranking; remembers its size to split the work.
    def __init__(self, broj_niti):
        super().__init__(max_workers=broj_niti, thread_name_prefix="rang")
        self.broj_niti = broj_niti


def napravi_rang_pool(T):
    return RangPool(T) if T > 1 else None           # T = 1: plain sequential ranking, no pool overhead


def _dominacija_redova(ocene, od, do):
    # One independent job of the parallel ranking: rows od..do-1 of the dominance "matrix".
    # For each i in the range: whom i dominates and how many dominate i.
    # It compares i with ALL j (not only j > i), so every job writes only its own rows:
    # no shared writes, no locks. The price is 2x more comparisons than the sequential version.
    n = len(ocene)
    dominira_nad, broj_dominatora = [], []
    for i in range(od, do):
        oi = ocene[i]
        moji, broj = [], 0
        for j in range(n):
            if j == i:
                continue
            if dominira(oi, ocene[j]):
                moji.append(j)
            elif dominira(ocene[j], oi):
                broj += 1
        dominira_nad.append(moji)
        broj_dominatora.append(broj)
    return dominira_nad, broj_dominatora


def pareto_slojevi(kandidati, evidencija, pool=None):
    # pool: ThreadPoolExecutor for the ranking (separate from the threads that evaluate).
    # None -> sequential version (P1 and processes with T = 1).
    n = len(kandidati)
    ocene = [evidencija[s] for s in kandidati]

    if pool is None or n < 2:
        broj_dominatora = [0] * n
        dominira_nad = [[] for _ in range(n)]
        for i in range(n):                      # every pair exactly once
            for j in range(i + 1, n):
                if dominira(ocene[i], ocene[j]):
                    dominira_nad[i].append(j)
                    broj_dominatora[j] += 1
                elif dominira(ocene[j], ocene[i]):
                    dominira_nad[j].append(i)
                    broj_dominatora[i] += 1
    else:
        # split rows into contiguous chunks, one job per chunk (all rows cost the same: n - 1 comparisons)
        broj_poslova = min(pool.broj_niti, n)
        granice = [n * p // broj_poslova for p in range(broj_poslova + 1)]
        poslovi = [pool.submit(_dominacija_redova, ocene, granice[p], granice[p + 1])
                   for p in range(broj_poslova)]
        dominira_nad, broj_dominatora = [], []
        for posao in poslovi:                   # in submission order -> rows stay in order
            d, b = posao.result()
            dominira_nad.extend(d)
            broj_dominatora.extend(b)

    # Peeling layers off is inherently sequential (layer r+1 depends on layer r): main thread.
    slojevi = []
    trenutni = [i for i in range(n) if broj_dominatora[i] == 0]
    while trenutni:
        slojevi.append([kandidati[i] for i in trenutni])
        sledeci = []
        for i in trenutni:
            for j in dominira_nad[i]:
                broj_dominatora[j] -= 1
                if broj_dominatora[j] == 0:
                    sledeci.append(j)
        trenutni = sledeci

    return slojevi


def mera_razredjenosti(sloj, evidencija):
    # sloj: one Pareto layer (list of sequences).
    # Returns a dict: sequence -> crowding. Bigger = in a sparser area = preferred.

    mera = {s: 0.0 for s in sloj}                     # running sum per sequence
    broj_kriterijuma = len(evidencija[sloj[0]])       # 3 for us, but not hard-coded

    for c in range(broj_kriterijuma):
        # Sort the layer by criterion c (the key is that sequence's c-th score).
        sortirani = sorted(sloj, key=lambda s: evidencija[s][c])

        najmanja = evidencija[sortirani[0]][c]
        najveca = evidencija[sortirani[-1]][c]
        raspon = najveca - najmanja
        if raspon == 0:                               # all equal on c: skip c entirely
            continue

        # The extremes on this criterion are always kept: infinite crowding.
        mera[sortirani[0]] = INF
        mera[sortirani[-1]] = INF

        # Everyone in between: gap between the neighbors, scaled by the range.
        for i in range(1, len(sortirani) - 1):
            prethodni = evidencija[sortirani[i - 1]][c]
            sledeci = evidencija[sortirani[i + 1]][c]
            mera[sortirani[i]] += (sledeci - prethodni) / raspon

    return mera


def popuni_populaciju(slojevi, mera):
    populacija = []
    for sloj in slojevi:
        mesta = N - len(populacija)                 # free spots left
        if len(sloj) <= mesta:
            populacija.extend(sloj)                 # whole layer fits
        else:
            po_meri = sorted(sloj, key=lambda s: mera[s], reverse=True)
            populacija.extend(po_meri[:mesta])      # cut the layer: highest crowding first
            break
    return populacija


def napravi_dete(populacija, lam, rng):
    i, j = rng.choice(len(populacija), size=2, replace=False)   # two different parents
    prvi, drugi = populacija[i], populacija[j]

    presek = rng.integers(1, len(prvi))                         # cut between letters: 1..L-1
    slova = list(prvi[:presek] + drugi[presek:])                # start of first + end of second

    broj_mutacija = min(rng.poisson(lam), len(slova))           # s ~ Poisson(λ), capped at length
    if broj_mutacija > 0:
        pozicije = rng.choice(len(slova), size=broj_mutacija, replace=False)
        for pozicija in pozicije:
            druga = [a for a in ALFABET if a != slova[pozicija]]
            slova[pozicija] = druga[rng.integers(len(druga))]

    return "".join(slova)


def sakupi_kandidate(populacija, lam, rng, evidencija, brojaci, budzet):
    novi = []
    while len(novi) < M:
        if brojaci.potroseno >= budzet or brojaci.neuspesni >= G:
            break                                       # search is over

        kandidat = napravi_dete(populacija, lam, rng)
        if kandidat in evidencija:                      # already known: doesn't cost budget
            brojaci.neuspesni += 1
            continue

        brojaci.neuspesni = 0                           # success resets the streak
        evidencija[kandidat] = None                     # reserved
        brojaci.potroseno += 1                          # counted at START of evaluation
        evidencija[kandidat] = oceni(kandidat)
        novi.append(kandidat)

    return novi


def sakupi_kandidate_niti(populacija, lam, rng, evidencija, brojaci, budzet, T):
    novi = []
    rezervisano = 0                                     # evaluations STARTED in this iteration
    brava = threading.Lock()                            # guards evidencija, novi, brojaci and rng

    def radnik():
        nonlocal rezervisano
        while True:
            with brava:
                if rezervisano >= M or brojaci.potroseno >= budzet or brojaci.neuspesni >= G:
                    return

                kandidat = napravi_dete(populacija, lam, rng)   # rng is not thread-safe
                if kandidat in evidencija:
                    brojaci.neuspesni += 1
                    continue

                brojaci.neuspesni = 0
                evidencija[kandidat] = None             # reserved: no other thread can take it
                brojaci.potroseno += 1
                rezervisano += 1
                novi.append(kandidat)

            ocene = oceni(kandidat)                     # OUTSIDE the lock: this is what runs in parallel

            with brava:
                evidencija[kandidat] = ocene

    niti = [threading.Thread(target=radnik) for _ in range(T)]
    for nit in niti:
        nit.start()
    for nit in niti:
        nit.join()                                      # waits for evaluations still in progress
    return novi


def azuriraj(populacija, arhiva, novi, evidencija, pool=None):
    kandidati = list(dict.fromkeys(populacija + arhiva + novi))   # merge, no duplicates, stable order
    slojevi = pareto_slojevi(kandidati, evidencija, pool)         # only this part uses the pool
    mera = {}
    for sloj in slojevi:
        mera.update(mera_razredjenosti(sloj, evidencija))
    return popuni_populaciju(slojevi, mera), slojevi[0], mera     # new population, new archive, crowding


def pretraga(lam, rng, budzet, T=1):
    evidencija = {}
    brojaci = Brojaci()
    pool = napravi_rang_pool(T)                                   # created once, reused every iteration

    try:
        populacija = napravi_pocetnu_populaciju(rng, evidencija, budzet)
        brojaci.potroseno = len(evidencija)                       # initial population spent budget
        populacija, arhiva, _ = azuriraj(populacija, [], [], evidencija, pool)

        trajanja = []
        trajanja_rangiranja = []
        while brojaci.potroseno < budzet and brojaci.neuspesni < G:
            t0 = time.perf_counter()
            if T == 1:
                novi = sakupi_kandidate(populacija, lam, rng, evidencija, brojaci, budzet)
            else:
                novi = sakupi_kandidate_niti(populacija, lam, rng, evidencija, brojaci, budzet, T)
            t1 = time.perf_counter()
            populacija, arhiva, _ = azuriraj(populacija, arhiva, novi, evidencija, pool)
            t2 = time.perf_counter()
            trajanja.append(t2 - t0)
            trajanja_rangiranja.append(t2 - t1)
    finally:
        if pool is not None:
            pool.shutdown()

    return arhiva, evidencija, brojaci, trajanja, trajanja_rangiranja


# ---------------------------------------------------------------- processes

def susedi(moj_id, P, topologija, rng):
    ostali = [j for j in range(P) if j != moj_id]
    if topologija == "prsten":
        return [(moj_id + 1) % P]
    if topologija == "zvezda":
        return ostali if moj_id == 0 else [0]
    if topologija == "svi_svima":
        return ostali
    if topologija == "nasumicno":
        return [ostali[rng.integers(len(ostali))]]
    raise ValueError(f"nepoznata topologija: {topologija}")


def isprazni(red):
    broj = 0                                            # candidates thrown away
    while True:
        try:
            _, kandidati = red.get_nowait()
        except queue.Empty:
            return broj
        broj += len(kandidati)


def primi_poruke(red, evidencija, poreklo):
    # Empties the inbox WITHOUT waiting. Known sequences are discarded; new ones go into the
    # record with the received scores (no oceni call, no budget) and become this iteration's new candidates.
    primljeni, broj = [], 0
    while True:
        try:
            _, kandidati = red.get_nowait()
        except queue.Empty:
            return primljeni, broj
        for s, ocene, izvor in kandidati:
            broj += 1
            if s in evidencija:                         # already known: discard
                continue
            evidencija[s] = ocene                       # no oceni call, no budget
            poreklo[s] = izvor
            primljeni.append(s)


def proces_pretrage(moj_id, pokretanje, seme_procesa, redovi, red_rezultata):
    rng = np.random.default_rng(seme_procesa)
    lam = pokretanje.lambde[moj_id]
    budzet = pokretanje.B // pokretanje.P
    moj_red = redovi[moj_id]

    evidencija = {}
    poreklo = {}                                        # sequence -> id of the process that evaluated it
    brojaci = Brojaci()
    poslato = primljeno = primljeno_novih = 0

    pool = napravi_rang_pool(pokretanje.T)              # ranking pool of this process (None when T = 1)

    populacija = napravi_pocetnu_populaciju(rng, evidencija, budzet)
    brojaci.potroseno = len(evidencija)
    for s in evidencija:
        poreklo[s] = moj_id
    populacija, arhiva, mera = azuriraj(populacija, [], [], evidencija, pool)

    trajanja = []
    trajanja_rangiranja = []
    iteracija = 0
    while brojaci.potroseno < budzet and brojaci.neuspesni < G:
        t0 = time.perf_counter()
        iteracija += 1

        # receive: empty the inbox without waiting
        primljeni, broj = primi_poruke(moj_red, evidencija, poreklo)
        primljeno += broj
        primljeno_novih += len(primljeni)

        # collect M of our own
        if pokretanje.T == 1:
            novi = sakupi_kandidate(populacija, lam, rng, evidencija, brojaci, budzet)
        else:
            novi = sakupi_kandidate_niti(populacija, lam, rng, evidencija, brojaci, budzet, pokretanje.T)
        for s in novi:
            poreklo[s] = moj_id

        t1 = time.perf_counter()
        populacija, arhiva, mera = azuriraj(populacija, arhiva, novi + primljeni, evidencija, pool)
        trajanja_rangiranja.append(time.perf_counter() - t1)

        # send: every E-th iteration, top K of the archive by crowding
        if iteracija % pokretanje.E == 0:
            izbor = sorted(arhiva, key=lambda s: mera[s], reverse=True)[:pokretanje.K]
            poruka = (moj_id, [(s, evidencija[s], poreklo[s]) for s in izbor])
            for j in susedi(moj_id, pokretanje.P, pokretanje.topologija, rng):
                redovi[j].put(poruka)
                poslato += len(izbor)

        trajanja.append(time.perf_counter() - t0)

    if pool is not None:
        pool.shutdown()

    red_rezultata.put(dict(
        id=moj_id,
        arhiva=[(s, evidencija[s], poreklo[s]) for s in arhiva],
        evaluacija=brojaci.potroseno,
        trajanja=trajanja,
        trajanja_rangiranja=trajanja_rangiranja,
        poslato=poslato,
        primljeno=primljeno,
        primljeno_novih=primljeno_novih,
        lokalno_ocenjene=[s for s in evidencija if poreklo[s] == moj_id],
    ))


def spoji_arhive(arhive):
    # Merge: union of local archives [(seq, scores, origin), ...], no duplicates, only non-dominated
    # (the same dominance/ranking function as in the local search).
    sve = {}
    for arhiva in arhive:
        for s, ocene, izvor in arhiva:
            sve.setdefault(s, (ocene, izvor))
    ocene_svih = {s: o for s, (o, _) in sve.items()}
    konacna = pareto_slojevi(list(sve), ocene_svih)[0] if sve else []
    return [(s, *sve[s]) for s in konacna]


def pokreni_procese(pokretanje, seme, rok=600):
    ctx = mp.get_context("spawn")
    P = pokretanje.P
    redovi = [ctx.Queue() for _ in range(P)]            # one inbox per process
    red_rezultata = ctx.Queue()
    semena = np.random.SeedSequence(seme).spawn(P)      # independent random stream per process

    procesi = [ctx.Process(target=proces_pretrage, args=(i, pokretanje, semena[i], redovi, red_rezultata))
               for i in range(P)]
    for p in procesi:
        p.start()

    rezultati = {}
    pali = set()
    u_prenosu = [0] * P                                 # candidates still in an inbox after its owner finished
    kraj = time.monotonic() + rok

    while len(rezultati) + len(pali) < P and time.monotonic() < kraj:
        try:
            r = red_rezultata.get(timeout=0.2)          # results first, then join (never the other way)
            rezultati[r["id"]] = r
        except queue.Empty:
            pass
        for i, p in enumerate(procesi):
            if i not in rezultati and not p.is_alive() and p.exitcode != 0:
                pali.add(i)                             # crashed: its result will never come
        for i in set(rezultati) | pali:
            u_prenosu[i] += isprazni(redovi[i])         # nobody reads it anymore: we do

    kraj_cekanja = time.monotonic() + 10
    while any(p.is_alive() for p in procesi) and time.monotonic() < kraj_cekanja:
        for i in range(P):
            u_prenosu[i] += isprazni(redovi[i])
        for p in procesi:
            p.join(timeout=0.1)
    for i, p in enumerate(procesi):
        if p.is_alive():
            p.terminate()                               # hung past the deadline
            p.join()
            pali.add(i)
    for i in range(P):
        u_prenosu[i] += isprazni(redovi[i])

    ocenjene = [set(r["lokalno_ocenjene"]) for r in rezultati.values()]
    ponovljeno = sum(map(len, ocenjene)) - len(set().union(*ocenjene))

    return dict(
        arhiva=spoji_arhive([rezultati[i]["arhiva"] for i in sorted(rezultati)]),
        rezultati=rezultati,
        pali=sorted(pali),
        u_prenosu=u_prenosu,
        ponovljeno=ponovljeno,
    )


# ---------------------------------------------------------------- archive quality (hypervolume, from the spec)

def hv2d(tacke, ref):
    """Area dominated by points (x, y) w.r.t. ref; maximization."""
    povrsina, najbolji_y = 0.0, ref[1]
    for x, y in sorted(tacke, reverse=True):            # from the largest x
        if y > najbolji_y:
            povrsina += (x - ref[0]) * (y - najbolji_y)
            najbolji_y = y
    return povrsina


def hv3d(tacke, ref):
    """Volume dominated by points (x, y, z) w.r.t. ref; maximization."""
    tacke = sorted(tacke, key=lambda t: t[2], reverse=True)    # by z, descending
    zapremina = 0.0
    for i, (_, _, z) in enumerate(tacke):
        sledeci_z = tacke[i + 1][2] if i + 1 < len(tacke) else ref[2]
        visina = z - sledeci_z
        if visina > 0:
            sloj = [(x, y) for x, y, _ in tacke[: i + 1]]       # all points with z >= current
            zapremina += hv2d(sloj, ref[:2]) * visina
    return zapremina


def normalizuj(tacke, lo, hi):
    """lo, hi: fixed bounds per criterion, the same for all runs."""
    return [tuple((v - l) / (h - l) for v, l, h in zip(t, lo, hi)) for t in tacke]


HV_LO, HV_HI, HV_REF = (0, 0, 0), (10, 10, 10), (-0.1, -0.1, -0.1)   # oceni() returns values in [0, 10]


def hipervolumen(ocene):
    return hv3d(normalizuj(ocene, HV_LO, HV_HI), HV_REF) if ocene else 0.0


# ---------------------------------------------------------------- runs and the report

IZLAZ = "rezultati.md"


def prosek(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else 0.0


def std(xs):
    xs = list(xs)
    if len(xs) < 2:
        return 0.0
    m = prosek(xs)
    return (sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) ** 0.5


def rasponi(ocene):
    if not ocene:
        return "-"
    return " ".join(f"[{min(o[c] for o in ocene):.2f}, {max(o[c] for o in ocene):.2f}]"
                    for c in range(len(ocene[0])))


def okruzenje():
    cpu = platform.processor()
    if not cpu or cpu == platform.machine():
        try:                                            # Linux: platform.processor() is often empty
            with open("/proc/cpuinfo") as f:
                cpu = next(l.split(":", 1)[1].strip() for l in f if l.startswith("model name"))
        except (OSError, StopIteration):
            cpu = cpu or platform.machine()
    gil = getattr(sys, "_is_gil_enabled", lambda: True)()
    return [
        ("Procesor", cpu),
        ("Logičkih jezgara", os.cpu_count()),
        ("OS", platform.platform()),
        ("Python", f"{platform.python_implementation()} {platform.python_version()}"
                   f" ({'GIL uključen' if gil else 'free-threading, bez GIL-a'})"),
        ("numpy", np.__version__),
    ]


def pokreni_jedan(pokretanje, seme):
    """One run with one seed. Wall time measured with perf_counter, no I/O inside the measured part."""
    t0 = time.perf_counter()

    if pokretanje.P == 1:
        rng = np.random.default_rng(seme)
        arhiva, evidencija, brojaci, trajanja, trajanja_rang = pretraga(
            pokretanje.lambde[0], rng, pokretanje.B, pokretanje.T)
        ukupno = time.perf_counter() - t0
        tacke = [(s, tuple(evidencija[s]), 0) for s in arhiva]
        return dict(seme=seme, ukupno=ukupno, evaluacija=brojaci.potroseno, iteracija=len(trajanja),
                    iteracija_ms=prosek(trajanja) * 1000, rang_ms=prosek(trajanja_rang) * 1000,
                    arhiva=tacke, hv=hipervolumen([o for _, o, _ in tacke]),
                    procesi=[], ponovljeno=None, pali=[])

    r = pokreni_procese(pokretanje, seme)
    ukupno = time.perf_counter() - t0
    procesi = []
    for i, x in sorted(r["rezultati"].items()):
        procesi.append(dict(
            id=i, lam=pokretanje.lambde[i], evaluacija=x["evaluacija"], iteracija=len(x["trajanja"]),
            iteracija_ms=prosek(x["trajanja"]) * 1000, rang_ms=prosek(x["trajanja_rangiranja"]) * 1000,
            poslato=x["poslato"], primljeno=x["primljeno"], novih=x["primljeno_novih"],
            arhiva=len(x["arhiva"]), iz_drugih=sum(1 for _, _, izvor in x["arhiva"] if izvor != i),
            u_prenosu=r["u_prenosu"][i]))
    tacke = [(s, tuple(o), izvor) for s, o, izvor in r["arhiva"]]
    return dict(seme=seme, ukupno=ukupno, evaluacija=sum(p["evaluacija"] for p in procesi),
                iteracija=prosek(p["iteracija"] for p in procesi),
                iteracija_ms=prosek(p["iteracija_ms"] for p in procesi),
                rang_ms=prosek(p["rang_ms"] for p in procesi),
                arhiva=tacke, hv=hipervolumen([o for _, o, _ in tacke]),
                procesi=procesi, ponovljeno=r["ponovljeno"], pali=r["pali"])


def opis(p):
    lam = ", ".join(f"{x:g}" for x in p.lambde)
    return (f"P×T = {p.P}×{p.T}, λ = ({lam}), topologija = {p.topologija or '-'}, E = {p.E or '-'}, "
            f"B = {p.B}, N = {p.N}, k = {p.k}, M = {p.M}, K = {p.K}, G = {p.G}")


def napisi_izvestaj(svi, putanja=IZLAZ):
    L = ["# Rezultati pokretanja", ""]

    L += ["## Okruženje i postavka merenja", ""]
    L += [f"- **{k}:** {v}" for k, v in okruzenje()]
    L += [f"- **Semena:** {', '.join(map(str, SEMENA))}",
          "- **Mereno:** zidno vreme (`time.perf_counter`) od početka pretrage do konačne arhive; "
          "upis rezultata i ispis nisu uključeni. Kod više procesa uključeno je i pokretanje procesa "
          "(spawn) i prikupljanje rezultata. Svako pokretanje izvršeno je jednom po semenu, bez zagrevanja.",
          f"- **Hipervolumen:** `hv3d` iz postavke, normalizacija lo = {HV_LO}, hi = {HV_HI}, ref = {HV_REF}.",
          ""]

    # summary table: mean over seeds
    vreme_p1 = prosek(r["ukupno"] for r in svi["P1"][1]) if "P1" in svi else None
    L += ["## Zbirna tabela (prosek po semenima)", "",
          "| Pokretanje | P×T | λ | Topologija | E | Vreme [s] | Ubrzanje prema P1 | Iteracija [ms] "
          "| Ažuriranje (rangiranje) [ms] | Evaluacija | Arhiva | Hipervolumen (± std) | Poslato kandidata |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for naziv, (p, rez) in svi.items():
        vreme = prosek(r["ukupno"] for r in rez)
        ubrzanje = f"{vreme_p1 / vreme:.2f}×" if vreme_p1 else "-"
        poslato = prosek(sum(x["poslato"] for x in r["procesi"]) for r in rez) if p.P > 1 else None
        L.append(f"| {naziv} | {p.P}×{p.T} | {', '.join(f'{x:g}' for x in p.lambde)} | {p.topologija or '-'} "
                 f"| {p.E or '-'} | {vreme:.2f} | {ubrzanje} | {prosek(r['iteracija_ms'] for r in rez):.1f} "
                 f"| {prosek(r['rang_ms'] for r in rez):.2f} | {prosek(r['evaluacija'] for r in rez):.0f} "
                 f"| {prosek(len(r['arhiva']) for r in rez):.1f} "
                 f"| {prosek(r['hv'] for r in rez):.4f} ± {std(r['hv'] for r in rez):.4f} "
                 f"| {'-' if poslato is None else f'{poslato:.0f}'} |")
    L.append("")

    for naziv, (p, rez) in svi.items():
        L += [f"## {naziv}", "", f"Parametri: {opis(p)}", ""]
        for r in rez:
            L += [f"### {naziv}, seme {r['seme']}", "",
                  f"- Ukupno trajanje: {r['ukupno']:.2f} s",
                  f"- Završenih evaluacija: {r['evaluacija']}",
                  f"- Iteracija: {r['iteracija']:g}, prosečno trajanje iteracije: {r['iteracija_ms']:.1f} ms "
                  f"(od toga ažuriranje populacije i rangiranje: {r['rang_ms']:.2f} ms)",
                  f"- Veličina konačne arhive: {len(r['arhiva'])}",
                  f"- Rasponi ocena (zaraznost, virulentnost, imunoevazivnost): "
                  f"{rasponi([o for _, o, _ in r['arhiva']])}",
                  f"- Hipervolumen: {r['hv']:.4f}"]
            if p.P > 1:
                po_poreklu = {}
                for _, _, izvor in r["arhiva"]:
                    po_poreklu[izvor] = po_poreklu.get(izvor, 0) + 1
                L += [f"- Poreklo tačaka konačne arhive (proces: broj): "
                      f"{', '.join(f'{i}: {n}' for i, n in sorted(po_poreklu.items()))}",
                      f"- Sekvenci ocenjenih u više procesa (ponovljen rad): {r['ponovljeno']}",
                      f"- Procesi koji su pali: {r['pali'] or 'nijedan'}",
                      "",
                      "| Proces | λ | Evaluacija | Iteracija | Iteracija [ms] | Poslato | Primljeno "
                      "| Primljeno novih | Lokalna arhiva | Iz drugih procesa | Ostalo u redu |",
                      "|---|---|---|---|---|---|---|---|---|---|---|"]
                L += [f"| {x['id']} | {x['lam']:g} | {x['evaluacija']} | {x['iteracija']} | {x['iteracija_ms']:.1f} "
                      f"| {x['poslato']} | {x['primljeno']} | {x['novih']} | {x['arhiva']} | {x['iz_drugih']} "
                      f"| {x['u_prenosu']} |" for x in r["procesi"]]
            L += ["", "| Sekvenca | Zaraznost | Virulentnost | Imunoevazivnost | Poreklo (proces) |",
                  "|---|---|---|---|---|"]
            for s, o, izvor in sorted(r["arhiva"], key=lambda t: t[1], reverse=True):
                L.append(f"| `{s}` | {o[0]:g} | {o[1]:g} | {o[2]:g} | {izvor} |")
            L.append("")

    with open(putanja, "w", encoding="utf-8") as f:
        f.write("\n".join(L))


def main():
    # optional: run only some configurations, e.g.  python main_pa.py P1 P2
    izabrani = [a.upper() for a in sys.argv[1:]] or list(POKRETANJA)
    nepoznati = [a for a in izabrani if a not in POKRETANJA]
    if nepoznati:
        sys.exit(f"nepoznata pokretanja: {nepoznati}; dostupna: {list(POKRETANJA)}")

    svi = {}
    for naziv in izabrani:
        pokretanje = POKRETANJA[naziv]
        rezultati = []
        for seme in SEMENA:
            r = pokreni_jedan(pokretanje, seme)
            rezultati.append(r)
            print(f"{naziv} seme {seme}: {r['ukupno']:.2f} s, evaluacija={r['evaluacija']}, "
                  f"arhiva={len(r['arhiva'])}, hv={r['hv']:.4f}", flush=True)
        svi[naziv] = (pokretanje, rezultati)

    napisi_izvestaj(svi)
    print(f"\nRezultati su upisani u {IZLAZ}")


if __name__ == "__main__":
    main()