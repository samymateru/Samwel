from typing import Dict
from services.connections.postgres.connections import AsyncDBPoolSingleton
from services.connections.postgres.insert import InsertQueryBuilder
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from services.connections.postgres.read import ReadBuilder


class Payload(BaseModel):
    queue_id: str
    module_id: Optional[str] = None
    data: Dict
    created_at: Optional[datetime] = datetime.now()



async def publish(channel: str, payload: Payload):
    """
    Publishes a notification to a PostgreSQL channel using LISTEN/NOTIFY.

    Args:
        channel (str): The PostgreSQL notification channel (e.g., 'user_updates').
        data (Dict): The data payload to publish as JSON.
        :param channel:
        :param payload:
    """
    pool = await AsyncDBPoolSingleton.get_instance().get_pool()


    async with pool.connection() as conn:
        builder = await (
            InsertQueryBuilder(connection=conn)
            .into_table("notification_queue")
            .values(payload)
            .returning("queue_id")
            .execute()
        )

        print(f"✅ Published to channel '{channel}': {payload}")

        return builder





async def load_message():
    pool = await AsyncDBPoolSingleton.get_instance().get_pool()


    async with pool.connection() as conn:
        builder = await (
            ReadBuilder(connection=conn)
            .from_table("notification_queue")
            .fetch_one()
        )






