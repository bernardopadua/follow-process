#DJANGO Core
from django.conf import settings

#CHANNELS Components
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async

#INTERNAL Components
from .tasks import get_user_processes, create_process, change_process, delete_process
from .models import UserAdditional

#PYTHON Components
import logging

class ProcessConsumer(AsyncJsonWebsocketConsumer):
    """
        Consumer class for the /home/ app.
    """

    async def connect(self):
        #DJANGO logging instance
        logger = logging.getLogger(__name__)

        user = self.scope["user"]
        if user.is_authenticated:
            
            #Controlling user connected
            # on .tasks > channel_layer.group_send
            await self.channel_layer.group_add(
                user.username,
                self.channel_name
            )

            await self.accept()
        else:
            await self.close()

    """
        Parses the communication through WebSockets.
    """
    async def receive_json(self, content):
        action = content.get("action")
        puser  = self.scope["user"].pk

        try:
            if action == 'list_processes':
                get_user_processes.delay(puser)
                await self.send_json({
                    "action": "request_ok"
                })

            elif action == 'create_process':
                create_process.delay(puser, content.get("nprocesso"), content.get("dprocesso"))
                await self.send_json({
                    "action": "request_ok"
                })

            elif action == 'change_process':
                change_process.delay(content["nprocesso"], content["dprocesso"])
                await self.send_json({
                    "action": "request_ok"
                })

            elif action == "delete_process":
                delete_process.delay(puser, content.get("nprocesso"))
                await self.send_json({
                    "action": "request_ok"
                })

            elif action == 'test_channel':
                task = task_time_resp.delay(self.channel_layer)
        except Exception as e:
            await self.send_json({"error": str(e)})
            logger.error(str(e))

    """
        Send to the /home/ app the list of processes.
    """
    async def process_respond(self, event):
        await self.send_json({
            "action": "list_processes",
            "processes": event['processes']
        })
