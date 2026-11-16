#!/usr/bin/env python3
"""Safe Environment & Dependency Audit Script for Causal-History-Recovery.

Verifies that all scientific dependencies, MuJoCo physics, and PyTorch runtime
are properly installed and functioning without side-effects.
"""

import sys
import platform

def run_checks() -> bool:
    print("=" * 60)
    print("CAUSAL-HISTORY-RECOVERY ENVIRONMENT AUDIT")
    print("=" * 60)
    
    # 1. Python runtime
    print(f"[1/6] Python Version: {sys.version.split()[0]} on {platform.system()} ({platform.machine()})")
    if sys.version_info < (3, 10):
        print("[-] ERROR: Python 3.10+ required.")
        return False
    print("      -> OK")

    # 2. Core math & data libraries
    print("[2/6] Verifying core scientific libraries...")
    try:
        import numpy as np
        import scipy
        import pandas as pd
        import sklearn
        import yaml
        import pydantic
        print(f"      - numpy: {np.__version__}")
        print(f"      - scipy: {scipy.__version__}")
        print(f"      - pandas: {pd.__version__}")
        print(f"      - scikit-learn: {sklearn.__version__}")
        print(f"      - PyYAML: {yaml.__version__}")
        print(f"      - pydantic: {pydantic.__version__}")
        print("      -> OK")
    except ImportError as e:
        print(f"[-] ERROR importing core libraries: {e}")
        return False

    # 3. PyTorch runtime
    print("[3/6] Verifying PyTorch...")
    try:
        import torch
        print(f"      - PyTorch version: {torch.__version__}")
        print(f"      - CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"      - CUDA Device: {torch.cuda.get_device_name(0)}")
        t = torch.randn(4, 4)
        t_out = t @ t.T
        print("      -> PyTorch CPU tensor math operational.")
    except Exception as e:
        print(f"[-] ERROR verifying PyTorch: {e}")
        return False

    # 4. Gymnasium
    print("[4/6] Verifying Gymnasium...")
    try:
        import gymnasium as gym
        print(f"      - Gymnasium version: {gym.__version__}")
        print("      -> OK")
    except ImportError as e:
        print(f"[-] ERROR importing gymnasium: {e}")
        return False

    # 5. MuJoCo Physics
    print("[5/6] Verifying MuJoCo physics engine...")
    try:
        import mujoco
        print(f"      - MuJoCo library version: {mujoco.__version__}")
        
        # Test minimal model compilation and simulation step
        xml = """
        <mujoco model="minimal_check">
            <worldbody>
                <light diffuse=".5 .5 .5" pos="0 0 3" dir="0 0 -1"/>
                <geom type="plane" size="1 1 0.1"/>
                <body pos="0 0 1">
                    <joint type="free"/>
                    <geom type="sphere" size="0.1" mass="1"/>
                </body>
            </worldbody>
        </mujoco>
        """
        model = mujoco.MjModel.from_xml_string(xml)
        data = mujoco.MjData(model)
        mujoco.mj_step(model, data)
        print(f"      - Test simulation step successful: z-pos = {data.qpos[2]:.4f}")
        print("      -> MuJoCo physics engine operational.")
    except Exception as e:
        print(f"[-] ERROR verifying MuJoCo: {e}")
        return False

    # 6. Package Import
    print("[6/6] Verifying causal_history_recovery package import...")
    try:
        # Add src to sys.path
        import os
        src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
        import causal_history_recovery
        print(f"      - Package loaded: {causal_history_recovery.__name__} (v{causal_history_recovery.__version__})")
        print("      -> OK")
    except Exception as e:
        print(f"[-] ERROR importing causal_history_recovery: {e}")
        return False

    print("=" * 60)
    print("ALL ENVIRONMENT & DEPENDENCY CHECKS PASSED SUCCESSFULLY.")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = run_checks()
    sys.exit(0 if success else 1)

