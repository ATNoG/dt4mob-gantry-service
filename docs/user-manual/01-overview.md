# Gantry Service - User Guide

## Overview

The Gantry Service is a bridge application that collects vehicle detection data from road sensors (cameras, LiDARs) and forwards it to Eclipse Ditto via Eclipse Hono, enabling digital twin representations of real-world toll gantry traffic. It consumes sensor-specific message formats, normalizes them, wraps them in the Eclipse Ditto protocol, and delivers them to your IoT backend.
