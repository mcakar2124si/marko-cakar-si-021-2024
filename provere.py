"""Provere ispravnosti (odeljak 7 postavke).  Pokretanje:  python provere.py

Evaluator se u većini provera zamenjuje lažnim (brzim, determinističkim) koji broji pozive,
da bi se mogle proveriti duplikati i budžet. Na kraju se sa pravim evaluatorom
pokreće i višeprocesna pretraga u kojoj jedan proces namerno pada.
"""
import queue
import random
import threading
import time

import numpy as np

import main_pa as mp_


# ---------------------------------------------------------------- helpers

class LaznaOcena:
    """Fake oceni: deterministic scores from the sequence, counts calls (thread-safe)."""

    def __init__(self, kasnjenje=0.0):
        self.kasnjenje = kasnjenje
        self.pozivi = []
        self.brava = threading.Lock()

    def __call__(self, s):
        with self.brava:
            self.pozivi.append(s)
        if self.kasnjenje:
            time.sleep(self.kasnjenje)                  # makes thread interleavings likely
        h = sum(ord(c) * (i + 1) for i, c in enumerate(s))
        return (h % 11, (h // 11) % 11, (h // 121) % 11)


def postavi(**vrednosti):
    """Temporarily change module globals of main_pa (N, M, k, oceni...); returns the old values."""
    stare = {ime: getattr(mp_, ime) for ime in vrednosti}
    for ime, v in vrednosti.items():
        setattr(mp_, ime, v)
    return stare


PROVERE = []


def provera(f):
    PROVERE.append(f)
    return f


# ---------------------------------------------------------------- single thread

@provera
def dominacija():
    assert mp_.dominira((5, 4), (3, 4))                 # example from the spec
    assert not mp_.dominira((5, 4), (6, 2)) and not mp_.dominira((6, 2), (5, 4))
    assert not mp_.dominira((3, 3, 3), (3, 3, 3))       # equal: nobody dominates
    assert mp_.dominira((3, 3, 4), (3, 3, 3))


@provera
def rangovi_na_malom_primeru():
    ocene = {"a": (5, 6), "b": (4, 4), "c": (1, 9), "d": (9, 1), "e": (3, 3), "f": (4, 4), "g": (1, 1)}
    slojevi = [set(s) for s in mp_.pareto_slojevi(list(ocene), ocene)]
    assert slojevi == [{"a", "c", "d"}, {"b", "f"}, {"e"}, {"g"}], slojevi


@provera
def paralelno_rangiranje_isto_kao_sekvencijalno():
    rnd = random.Random(1)
    for T in (2, 3, 4, 8):
        pool = mp_.napravi_rang_pool(T)
        try:
            for n in (0, 1, 2, 3, 7, 50, 120):
                # small value range -> many ties and equal scores
                ocene = {f"s{i}": tuple(rnd.randint(0, 4) for _ in range(3)) for i in range(n)}
                kandidati = list(ocene)
                sekv = mp_.pareto_slojevi(kandidati, ocene)
                par = mp_.pareto_slojevi(kandidati, ocene, pool)
                assert [set(s) for s in sekv] == [set(s) for s in par], (T, n)
        finally:
            if pool is not None:
                pool.shutdown()


@provera
def mera_razredjenosti():
    # 3rd criterion has zero range -> skipped; middle points get 0.5 + 0.5
    ocene = {"a": (1, 5, 7), "b": (2, 4, 7), "c": (3, 3, 7), "d": (4, 2, 7), "e": (5, 1, 7)}
    mera = mp_.mera_razredjenosti(list(ocene), ocene)
    assert mera["a"] == mera["e"] == float("inf")
    assert all(abs(mera[s] - 1.0) < 1e-12 for s in "bcd"), mera
    # one candidate / all equal: no range anywhere -> 0
    assert mp_.mera_razredjenosti(["x"], {"x": (1, 1, 1)}) == {"x": 0.0}


@provera
def popuni_populaciju_sece_po_meri():
    stare = postavi(N=3)
    try:
        slojevi = [["a", "b"], ["c", "d", "e"]]
        mera = {"a": 0, "b": 0, "c": 0.2, "d": 5.0, "e": 1.0}
        assert mp_.popuni_populaciju(slojevi, mera) == ["a", "b", "d"]
    finally:
        postavi(**stare)


@provera
def generisanje_kandidata():
    rng = np.random.default_rng(0)
    populacija = ["AAAAAAAA", "CCCCCCCC"]
    for _ in range(500):
        dete = mp_.napravi_dete(populacija, 0, rng)     # λ = 0: crossover only
        assert len(dete) == 8
        presek = dete.index("C") if dete[0] == "A" else dete.index("A")
        assert 1 <= presek <= 7 and dete == dete[0] * presek + dete[-1] * (8 - presek)
    for lam in (1, 3, 50):                              # λ = 50 > length: all positions change
        for _ in range(200):
            dete = mp_.napravi_dete(populacija, lam, rng)
            assert len(dete) == 8 and set(dete) <= set(mp_.ALFABET)


@provera
def pocetna_populacija_postuje_budzet():
    stare = postavi(oceni=LaznaOcena())
    try:
        ev = {}
        pop = mp_.napravi_pocetnu_populaciju(np.random.default_rng(0), ev, budzet=10)
        assert len(ev) == len(pop) == 10 and len(mp_.oceni.pozivi) == 10
        assert pop[0] == mp_.POCETNA and len(set(pop)) == 10
    finally:
        postavi(**stare)


@provera
def mali_budzet_i_kraj_po_budzetu():
    lazna = LaznaOcena()
    stare = postavi(oceni=lazna)
    try:
        for T in (1, 4):
            lazna.pozivi.clear()
            arhiva, ev, brojaci, trajanja, _ = mp_.pretraga(1.5, np.random.default_rng(3), 137, T)
            assert brojaci.potroseno == len(lazna.pozivi) == 137, (T, brojaci, len(lazna.pozivi))
            assert len(set(lazna.pozivi)) == 137            # nothing evaluated twice
            assert None not in ev.values()
            assert set(arhiva) <= set(ev)
    finally:
        postavi(**stare)


@provera
def kraj_kada_nema_novih_kandidata():
    # tiny search space: N = 4, k = 1, λ = 0 (crossover only) -> runs out of new sequences
    lazna = LaznaOcena()
    stare = postavi(oceni=lazna, N=4, k=1)
    try:
        for T in (1, 4):
            lazna.pozivi.clear()
            _, ev, brojaci, _, _ = mp_.pretraga(0, np.random.default_rng(5), 10**6, T)
            assert brojaci.neuspesni >= mp_.G and brojaci.potroseno < 10**6
            assert len(lazna.pozivi) == len(set(lazna.pozivi)) == len(ev)
    finally:
        postavi(**stare)


@provera
def azuriranje_populacije_i_arhive():
    ocene = {"a": (5, 6), "b": (4, 4), "c": (1, 9), "d": (9, 1), "e": (3, 3)}
    stare = postavi(N=3)
    try:
        pop, arhiva, _ = mp_.azuriraj(["a", "b"], ["c"], ["d", "e", "a"], ocene)
        assert set(arhiva) == {"a", "c", "d"} and set(pop) == {"a", "c", "d"}
        assert len(pop) == len(set(pop))                    # no duplicates after merge
    finally:
        postavi(**stare)


# ---------------------------------------------------------------- threads

@provera
def niti_bez_duplikata_u_malom_prostoru():
    # 2 parents, λ = 0 -> exactly 14 distinct children; 16 threads compete for them
    lazna = LaznaOcena(kasnjenje=0.002)
    stare = postavi(oceni=lazna, M=20)
    try:
        populacija = ["AAAAAAAA", "CCCCCCCC"]
        kopija = list(populacija)
        ev, br = {}, mp_.Brojaci()
        novi = mp_.sakupi_kandidate_niti(populacija, 0, np.random.default_rng(1), ev, br, 10**6, 16)
        assert populacija == kopija                          # population untouched during collection
        assert len(lazna.pozivi) == len(set(lazna.pozivi)) == 14, len(lazna.pozivi)
        assert sorted(novi) == sorted(ev) and None not in ev.values()
        assert br.neuspesni >= mp_.G                         # stopped because of G
    finally:
        postavi(**stare)


@provera
def niti_ne_prelaze_M_ni_budzet():
    lazna = LaznaOcena(kasnjenje=0.001)
    stare = postavi(oceni=lazna, M=20)
    try:
        rng = np.random.default_rng(2)
        populacija = [mp_.POCETNA, "NEIYQAGSTPCNGVAGPNCYHPLQSYGFQPTY"]
        for T in (3, 7, 16):                                 # M not divisible by T
            lazna.pozivi.clear()
            ev, br = {}, mp_.Brojaci()
            novi = mp_.sakupi_kandidate_niti(populacija, 3, rng, ev, br, 10**6, T)
            assert len(novi) == len(lazna.pozivi) == 20, (T, len(novi), len(lazna.pozivi))
        lazna.pozivi.clear()                                 # budget smaller than M
        ev, br = {}, mp_.Brojaci(potroseno=95)
        novi = mp_.sakupi_kandidate_niti(populacija, 3, rng, ev, br, 100, 8)
        assert len(novi) == len(lazna.pozivi) == 5 and br.potroseno == 100
    finally:
        postavi(**stare)


@provera
def evaluacija_upisuje_ocene_tek_posle():
    # while an evaluation runs, its sequence is already in the record with None
    vidjeno_none = []

    def spora(s):
        vidjeno_none.append(ev.get(s, "nema") is None)
        time.sleep(0.001)
        return (1, 1, 1)

    stare = postavi(oceni=spora, M=10)
    try:
        ev, br = {}, mp_.Brojaci()
        mp_.sakupi_kandidate_niti([mp_.POCETNA, "A" * 32], 2, np.random.default_rng(4), ev, br, 10**6, 4)
        assert vidjeno_none and all(vidjeno_none) and None not in ev.values()
    finally:
        postavi(**stare)


# ---------------------------------------------------------------- processes

@provera
def susedi_po_topologijama():
    rng = np.random.default_rng(0)
    assert [mp_.susedi(i, 4, "prsten", rng) for i in range(4)] == [[1], [2], [3], [0]]
    assert [mp_.susedi(i, 4, "zvezda", rng) for i in range(4)] == [[1, 2, 3], [0], [0], [0]]
    assert [mp_.susedi(i, 4, "svi_svima", rng) for i in range(4)] == [[1, 2, 3], [0, 2, 3], [0, 1, 3], [0, 1, 2]]
    for i in range(4):
        for _ in range(50):
            s = mp_.susedi(i, 4, "nasumicno", rng)
            assert len(s) == 1 and s[0] != i and 0 <= s[0] < 4


@provera
def prijem_poznatog_dominiranog_i_nedominiranog():
    lazna = LaznaOcena()
    stare = postavi(oceni=lazna, N=10)
    try:
        ev = {"a": (5, 5, 5), "b": (1, 1, 1)}
        poreklo = {"a": 0, "b": 0}
        red = queue.Queue()
        red.put((2, [("a", (9, 9, 9), 2),                    # known: discarded, local scores stay
                     ("los", (0, 0, 0), 2),                  # new but dominated
                     ("dobar", (9, 0, 9), 2)]))              # new and non-dominated
        primljeni, broj = mp_.primi_poruke(red, ev, poreklo)
        assert broj == 3 and primljeni == ["los", "dobar"]
        assert ev["a"] == (5, 5, 5) and poreklo["dobar"] == 2
        assert lazna.pozivi == []                             # no evaluator calls, no budget
        assert mp_.primi_poruke(red, ev, poreklo) == ([], 0)  # empty inbox: returns immediately
        _, arhiva, _ = mp_.azuriraj(["a", "b"], ["a"], primljeni, ev)
        assert set(arhiva) == {"a", "dobar"}
    finally:
        postavi(**stare)


@provera
def spajanje_arhiva_isto_kao_direktna_obrada():
    rnd = random.Random(7)
    for _ in range(30):
        ocene = {f"s{i}": tuple(rnd.randint(0, 6) for _ in range(3)) for i in range(60)}
        sve = list(ocene)
        grupe = [rnd.sample(sve, 25) for _ in range(3)]       # overlapping groups -> duplicates
        lokalne = []
        for g in grupe:
            front = mp_.pareto_slojevi(g, ocene)[0]
            lokalne.append([(s, ocene[s], 0) for s in front])
        spojeno = {s for s, _, _ in mp_.spoji_arhive(lokalne)}
        unija = list(dict.fromkeys(s for g in grupe for s in g))
        assert spojeno == set(mp_.pareto_slojevi(unija, ocene)[0])


@provera
def hipervolumen():
    assert abs(mp_.hv3d([(1, 1, 1)], (0, 0, 0)) - 1.0) < 1e-12
    assert abs(mp_.hv3d([(1, 0.5, 1), (0.5, 1, 1)], (0, 0, 0)) - 0.75) < 1e-12
    # a dominated point does not change the volume
    assert mp_.hv3d([(1, 0.5, 1), (0.5, 1, 1), (0.4, 0.4, 0.4)], (0, 0, 0)) == \
        mp_.hv3d([(1, 0.5, 1), (0.5, 1, 1)], (0, 0, 0))


@provera
def procesi_podela_budzeta_i_pad_jednog_procesa():
    # real processes and the real evaluator; λ has only 3 values -> process 3 crashes (IndexError)
    pokretanje = mp_.Pokretanje("test", B=400, N=20, k=3, M=10, lambde=(0.8, 1.5, 2.5),
                                T=2, P=4, K=5, E=1, topologija="svi_svima")
    t0 = time.perf_counter()
    r = mp_.pokreni_procese(pokretanje, seme=1, rok=60)
    assert r["pali"] == [3], r["pali"]
    assert sorted(r["rezultati"]) == [0, 1, 2]
    assert all(x["evaluacija"] == 100 for x in r["rezultati"].values())   # B / P each
    assert time.perf_counter() - t0 < 30                 # did not wait forever for process 3
    assert r["arhiva"]


# ---------------------------------------------------------------- runner

if __name__ == "__main__":
    pala = 0
    for f in PROVERE:
        t0 = time.perf_counter()
        try:
            f()
            print(f"OK    {f.__name__}  ({time.perf_counter() - t0:.2f} s)")
        except Exception as e:
            pala += 1
            print(f"PALA  {f.__name__}: {type(e).__name__}: {e}")
    print(f"\n{len(PROVERE) - pala}/{len(PROVERE)} provera prošlo")