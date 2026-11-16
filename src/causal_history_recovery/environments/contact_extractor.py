"""Contact Extractor Module for MuJoCo Environments.

Provides structured extraction, identification, and filtering of contact manifolds,
forces, and collision pairs from MuJoCo mjData structures.
"""

from __future__ import annotations

import dataclasses
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import mujoco


@dataclasses.dataclass(frozen=True)
class ContactPoint:
    """Structured information for a single discrete contact point."""
    geom1_id: int
    geom2_id: int
    geom1_name: str
    geom2_name: str
    body1_id: int
    body2_id: int
    body1_name: str
    body2_name: str
    distance: float
    position: Tuple[float, float, float]
    frame: Tuple[float, ...]  # 3x3 contact frame flattened
    force_magnitude: float


class ContactExtractor:
    """Extracts and filters contact information from a MuJoCo model and data."""

    def __init__(self, model: mujoco.MjModel):
        self.model = model

    def extract_contacts(self, data: mujoco.MjData) -> List[ContactPoint]:
        """Extract all active contact points from mjData."""
        contacts: List[ContactPoint] = []
        ncon = data.ncon

        for i in range(ncon):
            c = data.contact[i]
            g1, g2 = int(c.geom1), int(c.geom2)
            b1 = int(self.model.geom_bodyid[g1])
            b2 = int(self.model.geom_bodyid[g2])

            name_g1 = self.model.geom(g1).name or f"geom_{g1}"
            name_g2 = self.model.geom(g2).name or f"geom_{g2}"
            name_b1 = self.model.body(b1).name or f"body_{b1}"
            name_b2 = self.model.body(b2).name or f"body_{b2}"

            # Calculate contact force (normal force)
            # In MuJoCo, contact forces are computed in efc_force if constraint solver ran
            # c.efc_address gives the index in data.efc_force
            force_mag = 0.0
            if c.efc_address >= 0 and c.efc_address < len(data.efc_force):
                force_mag = float(np.abs(data.efc_force[c.efc_address]))

            pos = (float(c.pos[0]), float(c.pos[1]), float(c.pos[2]))
            frame = tuple(float(x) for x in c.frame)

            contacts.append(
                ContactPoint(
                    geom1_id=g1,
                    geom2_id=g2,
                    geom1_name=name_g1,
                    geom2_name=name_g2,
                    body1_id=b1,
                    body2_id=b2,
                    body1_name=name_b1,
                    body2_name=name_b2,
                    distance=float(c.dist),
                    position=pos,
                    frame=frame,
                    force_magnitude=force_mag,
                )
            )

        return contacts

    def filter_contacts(
        self,
        contacts: List[ContactPoint],
        body_name_a: Optional[str] = None,
        body_name_b: Optional[str] = None,
    ) -> List[ContactPoint]:
        """Filter contact list for interactions between specific bodies."""
        filtered = []
        for c in contacts:
            match_a = body_name_a is None or (c.body1_name == body_name_a or c.body2_name == body_name_a)
            match_b = body_name_b is None or (c.body1_name == body_name_b or c.body2_name == body_name_b)
            if match_a and match_b:
                filtered.append(c)
        return filtered

    def get_contact_summary(self, data: mujoco.MjData) -> Dict[str, Any]:
        """Return a compact dictionary summary of contact state."""
        contacts = self.extract_contacts(data)
        total_force = sum(c.force_magnitude for c in contacts)
        body_pairs = [(c.body1_name, c.body2_name) for c in contacts]

        return {
            "total_contacts": len(contacts),
            "total_contact_force": float(total_force),
            "interacting_body_pairs": body_pairs,
        }

