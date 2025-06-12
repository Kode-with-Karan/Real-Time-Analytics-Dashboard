import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .models import PageView, Conversion
import asyncio

class AnalyticsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("analytics", self.channel_name)
        await self.accept()
        # Start sending periodic updates
        asyncio.create_task(self.send_updates())

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("analytics", self.channel_name)

    async def send_updates(self):
        while True:
            stats = await self.get_stats()
            await self.send(text_data=json.dumps(stats))
            await asyncio.sleep(5)  # Update every 5 seconds

    async def get_stats(self):
        time_threshold = timezone.now() - timedelta(minutes=30)
        
        # Active users (distinct sessions in last 30 minutes)
        active_users = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: PageView.objects.filter(timestamp__gte=time_threshold)
                    .values('session_id').distinct().count()
        )

        # Page views in last 30 minutes
        page_views = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: PageView.objects.filter(timestamp__gte=time_threshold).count()
        )

        # Conversion rate
        conversions = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: Conversion.objects.filter(timestamp__gte=time_threshold).count()
        )
        
        conversion_rate = (conversions / page_views * 100) if page_views > 0 else 0

        return {
            'active_users': active_users,
            'page_views': page_views,
            'conversions': conversions,
            'conversion_rate': round(conversion_rate, 2)
        }

    async def receive(self, text_data):
        # Handle incoming messages if needed
        pass

    async def analytics_update(self, event):
        # Send updates to WebSocket clients
        await self.send(text_data=json.dumps(event['data']))
