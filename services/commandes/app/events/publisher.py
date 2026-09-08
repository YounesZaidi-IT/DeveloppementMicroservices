"""Publication d'événements — squelette à compléter au TP6."""
import json
import os
import uuid

import aio_pika

RABBITMQ_URL = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")


async def publier(routing_key: str, payload: dict) -> None:
    # TODO (TP6) : se connecter (aio_pika.connect_robust), déclarer l'exchange
    # topic "events", construire le message JSON (avec un message_id unique
    # via uuid.uuid4()) et le publier avec la routing_key.
    raise NotImplementedError("À implémenter au TP6")
