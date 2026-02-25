# HugBot API: A Standardized Instruction Protocol for Safe Human-Robot Embraces

**Version 1.0 | February 2026**
**Author: Israel Burns**

---

## Abstract

As humanoid robots become increasingly present in healthcare, eldercare, hospitality, and domestic environments, the need for standardized physical affection protocols has become urgent. HugBot API is an open-source RESTful interface that provides deterministic, safety-constrained instruction sets for robotic systems to execute human-compatible embraces. This paper presents the architecture, hug taxonomy, biomechanical safety model, and adaptive calibration system that comprise the HugBot protocol.

---

## 1. Introduction

Physical touch is a fundamental human need. Research consistently demonstrates that hugs reduce cortisol levels, increase oxytocin production, and lower blood pressure (Cohen et al., 2015). As robots transition from industrial isolation into shared human spaces, the gap between mechanical capability and safe physical interaction remains a critical unsolved problem.

Existing robotic interaction frameworks focus primarily on collision avoidance — keeping robots *away* from humans. HugBot inverts this paradigm: it provides a structured protocol for robots to *intentionally make safe physical contact* with humans in a controlled, repeatable, and comfortable manner.

The HugBot API is:

- **Open and free** — publicly accessible, zero licensing cost
- **Hardware-agnostic** — provides logical instructions, not motor-specific commands
- **Safety-first** — every instruction set includes force ceilings, abort triggers, and consent verification
- **Adaptive** — real-time calibration based on human physical characteristics

---

## 2. System Architecture

### 2.1 Overview

HugBot is a stateless REST API built on Flask (Python). It serves JSON instruction payloads that any robotic middleware layer can parse and translate into hardware-specific motor commands.

```
[Robot Sensors] → [Middleware] → [HugBot API] → [JSON Instructions] → [Middleware] → [Motor Controllers]
```

### 2.2 Design Principles

1. **Deterministic outputs** — Given the same hug type and calibration inputs, the API always returns identical instruction sets. No randomness in safety-critical parameters.
2. **Stateless operation** — No session tracking, no stored user data. Each request is self-contained.
3. **Separation of concerns** — HugBot defines *what* to do, not *how*. Motor translation is the responsibility of the consuming robotics platform.

### 2.3 Endpoints

| Method | Path | Function |
|--------|------|----------|
| GET | `/` | API metadata and endpoint discovery |
| GET | `/hugs` | Enumerate available hug types with summaries |
| GET | `/hugs/{type}` | Retrieve full instruction set for a hug type |
| GET | `/hugs/random` | Return a randomly selected hug instruction set |
| GET | `/safety` | Retrieve complete safety ruleset |
| POST | `/hugs/calibrate` | Compute adjusted parameters for a target human |

---

## 3. Hug Taxonomy

HugBot classifies embraces into five canonical types, each assigned a difficulty tier that maps to the minimum sensor and actuator requirements of the consuming robot.

### 3.1 Standard Hug (Beginner)

The baseline two-arm frontal embrace. Eight sequential steps from detection through release. Maximum force: 5N. Duration: 3 seconds. This is the recommended starting point for any robotic hugging implementation.

### 3.2 Gentle Hug (Beginner)

A reduced-force variant designed for sensitive contexts — post-surgical patients, individuals with anxiety, or first-time robot interactions. Maximum force: 2N. Duration: 2 seconds. Approach speed reduced to 0.2 m/s.

### 3.3 Bear Hug (Intermediate)

A firm, enthusiastic embrace with optional vertical lift component. Requires adult verification via height sensor (>1.4m). Includes pre-hug audio announcement. Maximum force: 10N. Duration: 4 seconds. Includes oscillation pattern during hold phase.

### 3.4 Side Hug (Beginner)

A single-arm lateral embrace. Requires directional awareness to position beside the human. Lower force profile (4N max) and shorter duration (2 seconds). Ideal for casual or public-setting interactions.

### 3.5 Group Hug (Advanced)

A multi-target embrace requiring cluster detection and center-of-mass positioning. Minimum two humans required. Maximum force distributed across contact points. Duration: 5 seconds. Requires advanced spatial awareness and multi-body proximity tracking.

---

## 4. Biomechanical Safety Model

Safety is not an optional feature in HugBot — it is the foundational layer upon which all instruction sets are built.

### 4.1 Force Constraints

All hug types specify a maximum contact force in Newtons. These limits are derived from comfort thresholds documented in human-robot interaction literature:

| Context | Maximum Force |
|---------|--------------|
| Child / Elderly | 2N |
| Gentle interaction | 2N |
| Standard adult | 5N |
| Firm (bear hug) | 10N |
| Absolute system ceiling | 10N |

For reference, a firm human handshake exerts approximately 30-50N. HugBot's ceiling of 10N ensures that even the most vigorous programmed embrace remains well within comfort thresholds.

### 4.2 Consent Protocol

Every hug instruction set begins with a `detect_human` step. The API specification mandates that the consuming system must implement consent verification before proceeding past this step. The `require_consent` flag in the safety ruleset is permanently set to `true` and cannot be overridden.

### 4.3 Abort Conditions

Four real-time abort triggers are defined:

1. **Retreat detection** — Human steps backward during approach
2. **Gesture recognition** — Human raises hands in stop gesture
3. **Audio keyword** — System detects "stop" or "no" via microphone
4. **Force feedback** — Resistance exceeding 2N in the opposite direction of embrace

Any single trigger causes immediate arm release and 0.5m retreat.

### 4.4 Fragile Human Mode

When the system estimates the human is under 1.2m tall or under 12 years of age, all force parameters are automatically reduced by 60%. Approach speed drops to minimum. This mode is non-negotiable and cannot be disabled.

---

## 5. Adaptive Calibration System

The `/hugs/calibrate` endpoint accepts human physical parameters and returns adjusted instruction values.

### 5.1 Input Parameters

```json
{
  "human_height_m": 1.1,
  "human_age_estimate": 8,
  "hug_type": "gentle"
}
```

### 5.2 Calibration Logic

The system applies a force multiplier based on detected vulnerability:

| Condition | Force Multiplier |
|-----------|-----------------|
| Height < 1.2m OR Age < 12 | 0.4x |
| Age > 70 | 0.6x |
| Default adult | 1.0x |

Arm target height adjusts based on human stature: mid-torso for humans under 1.4m, shoulder height otherwise. Approach speed reduces proportionally with the force multiplier.

### 5.3 Output

```json
{
  "adjusted_parameters": {
    "pressure_limit_newtons": 0.8,
    "force_multiplier": 0.4,
    "arm_target_height": "mid-torso",
    "approach_speed_ms": 0.2
  }
}
```

---

## 6. Integration Guide

### 6.1 For Robotics Developers

1. Query `/hugs/{type}` for your desired embrace style
2. Parse the `steps` array — each step includes an `action` key and `description`
3. Map each `action` to your platform's motor control API
4. Implement the abort conditions from `/safety` as interrupt handlers
5. Use `/hugs/calibrate` with sensor data before each hug to get adjusted parameters

### 6.2 Hardware Requirements by Tier

| Tier | Sensors | Actuators |
|------|---------|-----------|
| Beginner | Proximity, force feedback | 2-axis arms, wheels/legs |
| Intermediate | + Height estimation, audio I/O | + Vertical lift, oscillation |
| Advanced | + Multi-body tracking, cluster detection | + Independent arm control |

---

## 7. Future Work

- **Emotional state detection** — Adjust hug type and duration based on detected human mood via facial expression analysis
- **Cultural calibration** — Region-specific defaults (greeting customs, personal space norms)
- **Multi-robot coordination** — Synchronized group hugs with multiple robotic units
- **Haptic feedback loops** — Real-time pressure adjustment during embrace based on human muscle tension
- **Wearable integration** — Heart rate and galvanic skin response data to optimize hug duration

---

## 8. Conclusion

HugBot API represents a first step toward standardizing safe physical affection in human-robot interaction. By providing an open, free, hardware-agnostic instruction protocol with safety as its foundation, HugBot enables any robotics developer to implement comfortable, consent-driven embraces without reinventing the biomechanical safety wheel.

The API is open-source and publicly available at: **https://github.com/israelburns/hug-bot-api**

---

## References

- Cohen, S., et al. (2015). "Does Hugging Provide Stress-Buffering Social Support?" *Psychological Science*, 26(2), 135-147.
- Strabala, K., et al. (2013). "Toward Seamless Human-Robot Handovers." *Journal of Human-Robot Interaction*, 2(1), 112-132.
- ISO 13482:2014. "Robots and robotic devices — Safety requirements for personal care robots."
- Haddadin, S., et al. (2017). "Robot Collisions: A Survey on Detection, Isolation, and Identification." *IEEE Transactions on Robotics*, 33(6), 1292-1312.

---

*HugBot API v1.0 — Because every robot should know how to give a good hug.*
