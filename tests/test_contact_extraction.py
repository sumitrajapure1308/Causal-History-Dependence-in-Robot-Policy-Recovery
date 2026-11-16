"""Contact Extraction Unit Tests.

Validates that contact manifold extraction, geom identification, and force logging
are accurate, repeatable, and free of phantom impulses.
"""

import sys
import os
import numpy as np
import pytest

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from causal_history_recovery.environments.mujoco_wrapper import MuJoCoWrapperEnv


def test_contact_extraction_repeatability():
    """Verify that contact extraction produces identical contacts on the same state."""
    env = MuJoCoWrapperEnv("Pusher-v5")
    env.reset(seed=42)

    contacts1 = env.get_contacts()
    contacts2 = env.get_contacts()

    assert len(contacts1) == len(contacts2)
    for c1, c2 in zip(contacts1, contacts2):
        assert c1.geom1_id == c2.geom1_id
        assert c1.geom2_id == c2.geom2_id
        assert np.isclose(c1.distance, c2.distance, atol=1e-10)
        assert np.isclose(c1.force_magnitude, c2.force_magnitude, atol=1e-10)


def test_contact_filtering_table_and_object():
    """Verify filtering contacts between table and object body."""
    env = MuJoCoWrapperEnv("Pusher-v5")
    env.reset(seed=42)

    contacts = env.get_contacts()
    table_obj_contacts = env.contact_extractor.filter_contacts(
        contacts, body_name_a="world", body_name_b="object"
    )

    # In Pusher-v5, table is part of world body and object rests on table
    assert len(table_obj_contacts) > 0, "Expected table-object contact points upon reset!"
    for c in table_obj_contacts:
        assert "world" in (c.body1_name, c.body2_name)
        assert "object" in (c.body1_name, c.body2_name)
        assert c.distance <= 1e-4, "Resting contact distance should be zero or negative penetration"


def test_restoration_no_unreported_impulses():
    """Verify that snapshot restoration reproduces exact contact state without impulse spikes."""
    env = MuJoCoWrapperEnv("Pusher-v5")
    env.reset(seed=99)

    for _ in range(8):
        env.step(np.zeros(env.action_space.shape))

    contacts_before = env.get_contacts()
    snap = env.get_state_snapshot()

    # Step away
    for _ in range(5):
        env.step(np.ones(env.action_space.shape) * 0.2)

    # Restore snapshot
    env.restore_state_snapshot(snap)
    contacts_after = env.get_contacts()

    assert len(contacts_before) == len(contacts_after), "Contact count differed after restoration!"
    for cb, ca in zip(contacts_before, contacts_after):
        assert cb.geom1_id == ca.geom1_id
        assert cb.geom2_id == ca.geom2_id
        assert np.isclose(cb.distance, ca.distance, atol=1e-8)
        assert np.isclose(cb.force_magnitude, ca.force_magnitude, atol=1e-4)

