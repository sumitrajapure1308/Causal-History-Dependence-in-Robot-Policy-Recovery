"""Unit tests verifying causal_history_recovery package import and module integrity."""

import sys
import os

# Add src to python path for testing
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

def test_main_package_import():
    import causal_history_recovery
    assert causal_history_recovery.__version__ == "0.1.0"

def test_submodule_imports():
    from causal_history_recovery import environments
    from causal_history_recovery import policies
    from causal_history_recovery import rollout
    from causal_history_recovery import deviations
    from causal_history_recovery import matching
    from causal_history_recovery import counterfactuals
    from causal_history_recovery import metrics
    from causal_history_recovery import statistics
    from causal_history_recovery import visualization
    from causal_history_recovery import utils

    assert environments is not None
    assert policies is not None
    assert rollout is not None
    assert deviations is not None
    assert matching is not None
    assert counterfactuals is not None
    assert metrics is not None
    assert statistics is not None
    assert visualization is not None
    assert utils is not None

