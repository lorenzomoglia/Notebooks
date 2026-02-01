"""
Programmazione asincrona in Python: guida didattica
==================================================

Obiettivo
---------
Spiegare i concetti base di asyncio con esempi pratici.

Cosa imparerai
--------------
- Differenza tra codice sincrono e asincrono
- Event loop, coroutine, await
- Eseguire task in parallelo (concorrenza, non vero parallelismo)
- Timeout e cancellazione

Requisiti
---------
Python 3.11+ (va bene anche 3.8+ con poche differenze)

Esecuzione
----------
python async_python_didattico.py
"""

from __future__ import annotations

import asyncio
import time


def sezione(titolo: str) -> None:
    print("\n" + "=" * 72)
    print(titolo)
    print("=" * 72)


# 1) SINCRONO: tutto in fila

def lavoro_bloccante(nome: str, secondi: float) -> str:
    """Funzione sincrona: blocca il thread per `secondi`."""
    print(f"[{nome}] start (bloccante) per {secondi}s")
    time.sleep(secondi)
    print(f"[{nome}] end")
    return f"{nome} finito"


def demo_sincrono() -> None:
    sezione("1) Esecuzione SINCRONA")
    start = time.perf_counter()
    lavoro_bloccante("A", 1.5)
    lavoro_bloccante("B", 1.5)
    lavoro_bloccante("C", 1.5)
    durata = time.perf_counter() - start
    print(f"Tempo totale (sincrono): {durata:.2f}s")


# 2) ASINCRONO: coroutine e await

async def lavoro_async(nome: str, secondi: float) -> str:
    """Coroutine: non blocca il thread, cede il controllo con await."""
    print(f"[{nome}] start (async) per {secondi}s")
    await asyncio.sleep(secondi)
    print(f"[{nome}] end")
    return f"{nome} finito"


async def demo_async_sequenziale() -> None:
    sezione("2) ASINCRONO ma SEQUENZIALE (await uno per volta)")
    start = time.perf_counter()
    await lavoro_async("A", 1.5)
    await lavoro_async("B", 1.5)
    await lavoro_async("C", 1.5)
    durata = time.perf_counter() - start
    print(f"Tempo totale (await sequenziale): {durata:.2f}s")


# 3) ASINCRONO: concorrenza con gather

async def demo_async_concorrenza() -> None:
    sezione("3) ASINCRONO con CONCORRENZA (asyncio.gather)")
    start = time.perf_counter()
    risultati = await asyncio.gather(
        lavoro_async("A", 1.5),
        lavoro_async("B", 1.5),
        lavoro_async("C", 1.5),
    )
    durata = time.perf_counter() - start
    print(f"Risultati: {risultati}")
    print(f"Tempo totale (concorrenza): {durata:.2f}s")


# 4) Timeout e cancellazione

async def demo_timeout() -> None:
    sezione("4) Timeout e cancellazione")

    async def lavoro_lungo():
        try:
            print("[LONG] start")
            await asyncio.sleep(5)
            print("[LONG] end")
        except asyncio.CancelledError:
            print("[LONG] cancellato")
            raise

    task = asyncio.create_task(lavoro_lungo())
    try:
        await asyncio.wait_for(task, timeout=1.0)
    except asyncio.TimeoutError:
        print("Timeout! Cancello il task...")
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            print("Task cancellato correttamente")


# 5) Note finali

def note_finali() -> None:
    sezione("5) Note finali")
    print(
        "- asyncio è per I/O-bound (rete, file, DB), non per CPU-bound.\n"
        "- Per CPU-bound usa multiprocessing o librerie native.\n"
        "- La concorrenza asincrona non è parallelismo vero: cedi il controllo\n"
        "  con await per far avanzare altre coroutine."
    )


async def main() -> None:
    demo_sincrono()
    await demo_async_sequenziale()
    await demo_async_concorrenza()
    await demo_timeout()
    note_finali()


if __name__ == "__main__":
    asyncio.run(main())
