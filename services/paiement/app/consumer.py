"""Service Paiement (simulateur) — squelette (TP7).

Consomme `stock.reserved` et simule un paiement :
  - REFUSÉ si le total dépasse SEUIL_REFUS (1 000 par défaut)
  - ACCEPTÉ sinon
Vous complétez la publication du résultat (payment.processed / payment.failed).
"""
import asyncio
import contextlib
import json
import logging
import os

import aio_pika

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("paiement")

# Positionné à l'arrêt du service : la boucle de reconnexion s'interrompt proprement.
arret = asyncio.Event()

RABBITMQ_URL = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")
SEUIL_REFUS = float(os.environ.get("SEUIL_REFUS", "1000"))


async def traiter(message: aio_pika.abc.AbstractIncomingMessage) -> None:
    async with message.process():
        evenement = json.loads(message.body)
        total = float(evenement.get("total", 0))
        accepte = total <= SEUIL_REFUS
        logger.info("paiement commande %s (total=%s) : %s",
                    evenement.get("order_id"), total, "accepté" if accepte else "REFUSÉ")
        # TODO (TP7) : publier le résultat sur l'exchange "events" :
        #   - accepté → routing_key "payment.processed", payload {"order_id": ...}
        #   - refusé  → routing_key "payment.failed",    payload {"order_id": ...}
        # (réutilisez le publisher du TP6)


async def consommer() -> None:
    while not arret.is_set():
        try:
            connexion = await aio_pika.connect(RABBITMQ_URL)
            async with connexion:
                canal = await connexion.channel()
                exchange = await canal.declare_exchange("events", aio_pika.ExchangeType.TOPIC)
                file = await canal.declare_queue("paiement", durable=True)
                await file.bind(exchange, routing_key="stock.reserved")
                logger.info("connecté à RabbitMQ, en attente de réservations…")
                await file.consume(traiter)
                # tourne jusqu'à l'arrêt du service ou la perte de la connexion
                while not arret.is_set() and not connexion.is_closed:
                    with contextlib.suppress(asyncio.TimeoutError):
                        await asyncio.wait_for(arret.wait(), timeout=5)
        except asyncio.CancelledError:
            return
        except Exception as exc:
            logger.warning("RabbitMQ injoignable (%s), nouvel essai dans 5 s", exc)
            with contextlib.suppress(asyncio.TimeoutError):
                await asyncio.wait_for(arret.wait(), timeout=5)
