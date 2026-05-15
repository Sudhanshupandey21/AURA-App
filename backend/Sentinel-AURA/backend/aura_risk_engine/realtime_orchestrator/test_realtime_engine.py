"""Tests for realtime orchestrator components."""

import asyncio
import logging
import unittest
from datetime import datetime, timezone

from aura_risk_engine.realtime_orchestrator import (
    AdaptiveIntelligenceCoordinator,
    BroadcastEngine,
    EventQueueEngine,
    EnvironmentState,
    RealtimeEvent,
    RealtimeRiskRecalculator,
    TimeScheduler,
    WebSocketAdapter,
    WebSocketConnection,
    listen_for_events,
    start_scheduler,
)
from aura_risk_engine.realtime_orchestrator.utils import EventType, current_timestamp

logging.basicConfig(level=logging.ERROR)


class TestRealtimeUtils(unittest.IsolatedAsyncioTestCase):
    async def test_realtime_event_from_raw(self):
        raw = {
            "event_type": "incident_update",
            "timestamp": current_timestamp(),
            "payload": {"severity": 0.8, "source": "sensor-1"},
        }
        event = RealtimeEvent.from_raw(raw)
        self.assertEqual(event.event_type, EventType.INCIDENT_UPDATE)
        self.assertGreaterEqual(event.priority, 0)

    async def test_invalid_event_payload(self):
        raw = {"timestamp": current_timestamp(), "payload": {}}
        with self.assertRaises(ValueError):
            RealtimeEvent.from_raw(raw)


class TestEventQueueEngine(unittest.IsolatedAsyncioTestCase):
    async def test_enqueue_priority_and_dedup(self):
        queue_engine = EventQueueEngine()
        event = RealtimeEvent(
            event_type=EventType.INCIDENT_UPDATE,
            timestamp=current_timestamp(),
            payload={"severity": 0.9, "source": "sensor-1"},
        )

        await queue_engine.enqueue(event)
        await queue_engine.enqueue(event)

        self.assertEqual(queue_engine._queue.qsize(), 1)

    async def test_process_event_queue_runs(self):
        queue_engine = EventQueueEngine()
        state_manager = EnvironmentState()
        broadcaster = BroadcastEngine()
        recalculator = RealtimeRiskRecalculator(state_manager, broadcaster)
        stop_event = asyncio.Event()

        listener = asyncio.Queue()
        await broadcaster.register_listener(listener)

        event = RealtimeEvent(
            event_type=EventType.LIGHT_UPDATE,
            timestamp=current_timestamp(),
            payload={"light_risk": 0.7, "source": "sensor-2"},
        )
        await queue_engine.enqueue(event)

        task = asyncio.create_task(
            queue_engine.process_event_queue(state_manager, recalculator, broadcaster, stop_event)
        )
        output = await asyncio.wait_for(listener.get(), timeout=2.0)
        self.assertEqual(output["risk_level"], "SAFE")
        self.assertLess(output["risk_score"], 40)
        stop_event.set()
        await task


class TestEnvironmentState(unittest.TestCase):
    def test_state_updates_and_snapshot(self):
        state = EnvironmentState()
        state.update_time_risk(0.3)
        state.update_crowd_risk(0.4)
        state.update_light_risk(0.2)
        state.update_incident_risk(0.5)
        state.update_area_risk(0.6)

        snapshot = state.get_snapshot()
        self.assertEqual(snapshot["current_time_risk"], 0.3)
        self.assertEqual(snapshot["current_incident_risk"], 0.5)


class TestBroadcastEngine(unittest.IsolatedAsyncioTestCase):
    async def test_broadcast_to_listener(self):
        broadcaster = BroadcastEngine()
        listener = asyncio.Queue()
        await broadcaster.register_listener(listener)

        payload = {"risk_score": 72, "risk_level": "HIGH", "trend": "increasing"}
        await broadcaster.broadcast_risk_update(payload)

        received = await asyncio.wait_for(listener.get(), timeout=1.0)
        self.assertEqual(received["risk_score"], 72)


class TestTimeScheduler(unittest.IsolatedAsyncioTestCase):
    async def test_scheduler_creates_time_update_event(self):
        queue_engine = EventQueueEngine()
        stop_event = asyncio.Event()

        task = asyncio.create_task(start_scheduler(queue_engine, stop_event, interval_seconds=0.5))
        raw_event = await asyncio.wait_for(queue_engine._queue.get(), timeout=2.0)
        priority, timestamp, event = raw_event
        self.assertEqual(event.event_type, EventType.TIME_UPDATE)
        stop_event.set()
        await task


class TestRealtimeRiskRecalculator(unittest.IsolatedAsyncioTestCase):
    async def test_handle_incident_event_recalculates(self):
        state_manager = EnvironmentState()
        broadcaster = BroadcastEngine()
        recalculator = RealtimeRiskRecalculator(state_manager, broadcaster)

        listener = asyncio.Queue()
        await broadcaster.register_listener(listener)

        event = RealtimeEvent(
            event_type=EventType.INCIDENT_UPDATE,
            timestamp=current_timestamp(),
            payload={"severity": 0.9, "source": "police-report"},
        )

        output = await recalculator.handle_event(event)
        self.assertEqual(output["risk_level"], "SAFE")
        self.assertLess(output["risk_score"], 40)
        received = await asyncio.wait_for(listener.get(), timeout=1.0)
        self.assertEqual(received["risk_score"], output["risk_score"])


class TestWebSocketAdapter(unittest.IsolatedAsyncioTestCase):
    async def test_websocket_broadcast(self):
        adapter = WebSocketAdapter()
        connection = WebSocketConnection("client-1")
        await adapter.register_connection(connection)

        payload = {"risk_score": 65, "risk_level": "MEDIUM", "trend": "stable"}
        await adapter.broadcast(payload)

        received = await asyncio.wait_for(connection.receive(), timeout=1.0)
        self.assertEqual(received["risk_level"], "MEDIUM")


class TestAdaptiveIntelligenceCoordinator(unittest.IsolatedAsyncioTestCase):
    async def test_coordinator_runs_and_processes_event(self):
        coordinator = AdaptiveIntelligenceCoordinator()
        await coordinator.start()

        listener = asyncio.Queue()
        await coordinator.register_frontend_listener(listener)

        raw_event = {
            "event_type": "crowd_update",
            "timestamp": current_timestamp(),
            "payload": {"crowd_risk": 0.8, "source": "camera-1"},
        }
        await coordinator.submit_event(raw_event)

        output = await asyncio.wait_for(listener.get(), timeout=2.0)
        self.assertEqual(output["risk_level"], "SAFE")
        self.assertLess(output["risk_score"], 40)

        await coordinator.stop()


if __name__ == "__main__":
    unittest.main()
