"""SOS escalation and emergency notification system."""

import logging
import uuid
from datetime import datetime
from typing import Dict, List, Optional

from aura_risk_engine.alert_response_engine.utils import SOSEvent, validate_coordinate

logger = logging.getLogger(__name__)


class SOSEngine:
    """Manages SOS emergency escalation and notifications."""

    def __init__(self) -> None:
        self._sos_active: bool = False
        self._current_sos: Optional[SOSEvent] = None
        self._notification_log: List[str] = []

    def handle_sos_activation(
        self,
        location: Dict[str, float],
        manual_activation: bool = False,
        reason: Optional[str] = None,
    ) -> SOSEvent:
        """Activate SOS mode."""
        if self._sos_active:
            logger.warning("SOS already active.")
            return self._current_sos

        lat = location.get("latitude") or location.get("lat")
        lng = location.get("longitude") or location.get("lng")
        validate_coordinate(lat, lng)

        sos_id = str(uuid.uuid4())
        timestamp = datetime.now().timestamp()

        self._current_sos = SOSEvent(
            sos_id=sos_id,
            active=True,
            timestamp=timestamp,
            location={"lat": lat, "lng": lng},
            location_shared=True,
            emergency_contacts_notified=True,
            authorities_alerted=True,
            reason=reason or ("manual" if manual_activation else "automatic"),
        )

        self._sos_active = True
        self._notification_log.append(f"SOS activated: {reason or 'emergency'}")

        logger.critical(f"SOS ACTIVATED: {sos_id} at ({lat}, {lng})")
        return self._current_sos

    def handle_sos_deactivation(self) -> bool:
        """Deactivate SOS mode."""
        if not self._sos_active:
            logger.info("SOS not active.")
            return False

        self._sos_active = False
        self._notification_log.append("SOS deactivated")
        logger.info("SOS deactivated.")
        return True

    def is_sos_active(self) -> bool:
        """Check if SOS mode is currently active."""
        return self._sos_active

    def get_sos_status(self) -> Optional[SOSEvent]:
        """Get current SOS status."""
        return self._current_sos if self._sos_active else None

    def generate_emergency_payload(self) -> Dict:
        """Generate an emergency notification payload."""
        if not self._current_sos:
            raise ValueError("No active SOS event.")

        return {
            "sos_id": self._current_sos.sos_id,
            "timestamp": self._current_sos.timestamp,
            "location": self._current_sos.location,
            "location_shared": self._current_sos.location_shared,
            "emergency_contacts_notified": self._current_sos.emergency_contacts_notified,
            "authorities_alerted": self._current_sos.authorities_alerted,
            "reason": self._current_sos.reason,
        }

    def notify_emergency_contacts(self, contact_list: List[str]) -> bool:
        """Notify emergency contacts (hook for external system)."""
        if not self._sos_active:
            logger.warning("Cannot notify contacts: SOS not active.")
            return False

        logger.info(f"Notifying {len(contact_list)} emergency contacts.")
        self._notification_log.append(f"Notified {len(contact_list)} emergency contacts")
        return True

    def alert_authorities(self, authority_type: str = "police") -> bool:
        """Alert emergency authorities (hook for external system)."""
        if not self._sos_active:
            logger.warning("Cannot alert authorities: SOS not active.")
            return False

        logger.critical(f"Alerting {authority_type} authorities.")
        self._notification_log.append(f"Alerted {authority_type}")
        return True

    def get_notification_log(self) -> List[str]:
        """Get log of all notifications sent."""
        return self._notification_log.copy()


_default_sos_engine = SOSEngine()


def handle_sos(
    location: Dict[str, float],
    manual_activation: bool = False,
    reason: Optional[str] = None,
) -> SOSEvent:
    """Activate SOS mode."""
    return _default_sos_engine.handle_sos_activation(location, manual_activation, reason)


def is_sos_active() -> bool:
    """Check if SOS is currently active."""
    return _default_sos_engine.is_sos_active()


def get_sos_status() -> Optional[SOSEvent]:
    """Get current SOS status."""
    return _default_sos_engine.get_sos_status()
