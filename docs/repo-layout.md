# HFF Repository Layout

This document explains the structure of the Human Flourishing Frameworks repository.

## Top-Level Modules

The following Python modules live at the repository root and can be imported directly:

- `app.py` - Main Flask application
- `world_model.py` - World model and intervention definitions
- `sensors.py` - Sensor registry and measurement types
- `live_sensors.py` - Live sensor polling and observation loop
- `agent_system.py` - Autonomous agent system
- `byzantine_consensus.py` - Byzantine consensus implementation
- `claim_safety.py` - Claim safety validation
- `cryptographic_proof.py` - Cryptographic verification
- `mesh_network.py` - Mesh network synchronization
- `data_sources.py` - Data source integrations
- `seed_data.py` - Seed data for testing
- `adoption_tracker.py` - Node adoption tracking
- `device_telemetry.py` - Device telemetry collection
- `phone_telemetry.py` - Phone-specific telemetry
- `live_observation_telemetry.py` - Live observation telemetry
- `bio_threat_source_registry.py` - Bio threat source registry
- `polymorphic_seed_registry.py` - Polymorphic seed registry
- `background_mode.py` - Background mode controller
- `deploy_identity.py` - Deployment identity management
- `operator_device_api.py` - Operator device API
- `health_probe.py` - Health check endpoints
- `task_queue.py` - Task queue management
- `wsgi.py` - WSGI entry point
- `safe_app.py` - Public-copy guard wrapper (deprecated, pending retirement)

## Namespaced Packages

The `src/` directory contains namespaced packages:

- `src/bettersafe/` - Safety policy and release gate modules
  - `sensor_policy.py` - Sensor request evaluation
  - `release_gate.py` - Release candidate evaluation

## Import Path Configuration

### For Tests

`tests/__init__.py` prepends `src/` to `sys.path` so tests can import packaged modules without `pip install -e .`.

### For Scripts Outside Tests

To run scripts that need packaged modules outside of tests, either:

1. Set `PYTHONPATH=src` when running:
   ```bash
   PYTHONPATH=src python your_script.py
   ```

2. Or install the package in editable mode (once a `pyproject.toml` lands):
   ```bash
   pip install -e .
   ```

## Directory Structure

```
.
├── app.py                    # Main Flask application
├── world_model.py            # World model
├── sensors.py                # Sensor registry
├── src/
│   └── bettersafe/           # Namespaced safety package
│       ├── __init__.py
│       ├── sensor_policy.py
│       └── release_gate.py
├── tests/                    # Test suite
│   ├── __init__.py          # Prepends src/ to sys.path
│   ├── test_*.py            # Test files
│   └── test_safe_public_copy.py
├── docs/                    # Documentation
├── configs/                 # Configuration files
├── data/                    # Data directories
├── apps/                    # Application modules
├── scripts/                 # Utility scripts
├── .github/workflows/       # CI/CD workflows
└── requirements.txt         # Python dependencies
```

## Test Coverage

- `tests/test_sensor_policy.py` - Tests for `bettersafe.sensor_policy` (pytest-style)
- `tests/test_release_gate.py` - Tests for `bettersafe.release_gate` (pytest-style)
- `tests/test_safe_public_copy.py` - Regression tests for public dashboard authority claims
- Other test files use `unittest.TestCase` classes

## CI Configuration

- `.github/workflows/tests.yml` - Main test workflow (runs unittest + pytest)
- `.github/workflows/convergence-validation.yml` - Convergence guardrail validation
