"""Consommateur d'événements du service Notifications — squelette (TP6).

Lancé automatiquement au démarrage du service. Il se (re)connecte tout seul
à RabbitMQ ; vous n'avez qu'à compléter la fonction `traiter`.
"""
import asyncio
import contextlib
import json
import logging
import os

import aio_pika

# Positionné à l'arrêt du service : la boucle de reconnexion s'interrompt proprement.
arret = asyncio.Event()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("notifications")

RABBITMQ_URL = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")

# TP6 (idempotence) : mémorisez ici les message_id déjà traités.
_messages_traites: set[str] = set()


async def traiter(message: aio_pika.abc.AbstractIncomingMessage) -> None:
    async with message.process():  # ack automatique si aucune exception
        evenement = json.loads(message.body)
        # TODO (TP6) : journaliser la notification, par exemple :
        #   logger.info("notification envoyée : commande %s", evenement["order_id"])
        # TODO (TP6, idempotence) : ignorer le message si son message_id a déjà été traité.
        logger.info("événement reçu (traitement à implémenter au TP6) : %s", evenement)


async def consommer() -> None:
    while not arret.is_set():
        try:
            connexion = await aio_pika.connect(RABBITMQ_URL)
            async with connexion:
                canal = await connexion.channel()
                exchange = await canal.declare_exchange("events", aio_pika.ExchangeType.TOPIC)
                file = await canal.declare_queue("notifications", durable=True)
                await file.bind(exchange, routing_key="order.*")
                logger.info("connecté à RabbitMQ, en attente de messages…")
                await file.consume(traiter)
                # tourne jusqu'à l'arrêt du service ou la perte de la connexion
                while not arret.is_set() and not connexion.is_closed:
                    with contextlib.suppress(asyncio.TimeoutError):
                        await asyncio.wait_for(arret.wait(), timeout=5)
        except asyncio.CancelledError:  # arrêt du service
            return
        except Exception as exc:  # broker indisponible : on réessaie
            logger.warning("RabbitMQ injoignable (%s), nouvel essai dans 5 s", exc)
            with contextlib.suppress(asyncio.TimeoutError):
                await asyncio.wait_for(arret.wait(), timeout=5)
