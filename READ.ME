
# Simulink Bionics Controller – User Guide

## Overview

This project provides a **socket-based control system** for a robotic hand. It abstracts communication between high-level controllers (CLI, EMG data, user input) and low-level hardware endpoints (simulation, real UDP network endpoints, or mock devices).

The system uses a **message-passing architecture** where control commands are routed through a central hub to one or more active targets.

---

## Architecture

### High Level (Your Application)
- Your controller or data source generates `{finger, curl}` messages

### Mid Level (Message Routing)
- **ControlHub** – Routes messages to enabled interfaces
- **BisonicsInterface** – Abstract base class defining the contract for all endpoints

### Low Level (Communication Targets)
- **MockInterface** – Prints messages for testing
- **UDPInterface** – Sends messages over UDP to a network device
- **Custom Interfaces** – Inherit from `BisonicsInterface` to create your own

---

## Quick Start

1. **Define your targets:** Pass a dict of named interfaces to `ControlHub`
2. **Enable what you need:** Call `hub.enable('name')` for each interface you want active
3. **Connect:** Call `hub.connect_all()` to prepare all enabled interfaces
4. **Send messages:** Create `{'finger': 0-4, 'curl': -180 to 180}` dicts and call `hub.send(message)`
5. **Cleanup:** Call `hub.disconnect_all()` when done

See `example/program.py` for a complete working implementation.

## How Controllers Should Behave

- Use `message_util.Message.parse_string()` to safely parse user input into valid messages
- Check that both `finger` and `curl` are not `None` before sending
- Always wrap your hub lifecycle in a try/finally to ensure `disconnect_all()` runs
- Your controller is responsible for message validation before calling `hub.send()`



