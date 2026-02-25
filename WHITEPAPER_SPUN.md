# HugBot API: An Open Protocol for Governing Safe Physical Affection Between Robots and People

**Release 1.0 | February 2026**
**Israel Burns**

---

## Abstract

With humanoid machines rapidly entering healthcare facilities, assisted living communities, hospitality venues, and private homes, the demand for well-defined physical affection protocols has never been more pressing. HugBot API delivers an open-source REST interface that produces deterministic, safety-bounded instruction payloads enabling robotic platforms to perform human-compatible embraces. This document details the system design, embrace classification framework, biomechanical safety architecture, and real-time calibration engine that power the HugBot standard.

---

## 1. The Problem

Human beings are wired for physical contact. Decades of behavioral science confirm that embraces drive down cortisol, elevate oxytocin, and measurably reduce blood pressure (Cohen et al., 2015). Yet as machines migrate out of fenced-off factory floors and into rooms where people live and work, virtually every interaction framework on the market is engineered to do one thing: keep the robot away from the human.

HugBot flips that assumption on its head. Rather than avoiding contact, this protocol gives machines a structured, repeatable, and biomechanically safe pathway to *intentionally hold a person*.

Core tenets of the project:

- **Zero cost, fully open** — no API keys, no licensing fees, no gated access
- **Platform-independent** — logical step sequences, not vendor-locked motor commands
- **Safety as bedrock** — force ceilings, real-time abort triggers, and mandatory consent checks woven into every payload
- **Live adaptation** — on-the-fly parameter tuning driven by the physical characteristics of the person being hugged

---

## 2. How It Works

### 2.1 High-Level Flow

HugBot operates as a lightweight, stateless web service written in Python on Flask. It emits JSON instruction packets that any robotics middleware stack can ingest and convert into hardware-native motor signals.

```
[Onboard Sensors] → [Robot Middleware] → [HugBot API] → [JSON Payload] → [Middleware] → [Actuators]
```

### 2.2 Guiding Principles

1. **Predictable outputs** — Identical inputs always yield identical instruction sets. There is no stochastic behavior inside safety-critical paths.
2. **No stored state** — The service retains nothing between requests. Every call is independent and self-sufficient.
3. **Clean boundaries** — HugBot specifies the *intent* of each motion. Translating that intent into servo angles and torque curves is the job of the platform consuming the API.

### 2.3 Available Routes

| Verb | Route | Purpose |
|------|-------|---------|
| GET | `/` | Service metadata and route discovery |
| GET | `/hugs` | List every registered embrace type with quick summaries |
| GET | `/hugs/{type}` | Pull the complete instruction sequence for one embrace |
| GET | `/hugs/random` | Retrieve a randomly chosen embrace instruction set |
| GET | `/safety` | Fetch the full safety constraint document |
| POST | `/hugs/calibrate` | Submit human measurements and receive tuned parameters |

---

## 3. Embrace Classification Framework

Five canonical embrace categories form the foundation. Each one carries a difficulty rating that maps directly to the minimum sensor and actuator suite the consuming robot must have.

### 3.1 The Standard Embrace — Beginner

The default two-arm frontal hold. Eight ordered operations from initial detection through controlled release. Peak contact force capped at 5N. Target duration: three seconds. This is the recommended entry point for teams bringing robotic hugging online for the first time.

### 3.2 The Gentle Embrace — Beginner

Purpose-built for delicate scenarios: post-operative recovery, anxiety-prone individuals, or a person's very first physical interaction with a machine. Contact ceiling drops to 2N. Duration shortens to two seconds. Approach velocity is trimmed to 0.2 m/s.

### 3.3 The Bear Embrace — Intermediate

A vigorous, full-commitment hold with an optional micro-lift component. Gated behind an adult-verification check (height must exceed 1.4m). An audible announcement precedes the approach. Contact force rises to 10N. Hold time extends to four seconds and includes a gentle rocking oscillation.

### 3.4 The Side Embrace — Beginner

A single-arm lateral hold requiring the machine to detect the human's facing direction and position itself alongside. Reduced force envelope (4N ceiling) and a compact two-second hold. Well-suited for casual or public encounters.

### 3.5 The Group Embrace — Advanced

Multi-person hold demanding cluster detection, center-of-mass navigation, and distributed force management. At least two humans must be present. Contact force is spread across multiple points. Duration peaks at five seconds. Requires sophisticated spatial reasoning and simultaneous multi-body proximity monitoring.

---

## 4. Biomechanical Safety Architecture

In HugBot, safety is not layered on after the fact — it is the substrate everything else is built upon.

### 4.1 Contact Force Boundaries

Every embrace type ships with a hard Newton ceiling. These thresholds are grounded in published human-robot interaction comfort data:

| Scenario | Ceiling |
|----------|---------|
| Child or elderly person | 2N |
| Gentle-class interaction | 2N |
| Typical adult | 5N |
| Bear-class (firm hold) | 10N |
| Absolute system maximum | 10N |

Context: a firm handshake between two adults lands somewhere between 30 and 50 Newtons. HugBot's hard cap of 10N keeps even the most energetic programmed embrace far inside the comfort zone.

### 4.2 Mandatory Consent Gate

Every instruction sequence opens with a `detect_human` operation. The specification requires that the host system confirm human consent before any subsequent step executes. The `require_consent` flag inside the safety document is hardcoded to `true`. There is no override mechanism.

### 4.3 Real-Time Abort Triggers

Four independent conditions cause the machine to instantly drop its arms and retreat 0.5 meters:

1. **Retreat** — the person moves backward at any point during the approach
2. **Stop gesture** — raised palms detected via vision system
3. **Verbal refusal** — microphone picks up "stop" or "no"
4. **Resistive force** — opposing pressure exceeds 2N at any contact surface

A single trigger is sufficient. All four run concurrently.

### 4.4 Vulnerable-Person Mode

When onboard sensors estimate the person is shorter than 1.2 meters or younger than twelve years old, all force values drop by 60 percent automatically. Approach speed falls to its minimum setting. This behavior is mandatory across every embrace type and cannot be switched off.

---

## 5. Real-Time Calibration Engine

The `/hugs/calibrate` route ingests physical measurements and returns a tuned parameter set the robot applies before initiating contact.

### 5.1 What Goes In

```json
{
  "human_height_m": 1.1,
  "human_age_estimate": 8,
  "hug_type": "gentle"
}
```

### 5.2 How Adjustment Works

A force multiplier scales every pressure value in the selected embrace:

| Detected Condition | Multiplier |
|--------------------|-----------|
| Height below 1.2m OR estimated age under 12 | 0.4× |
| Estimated age above 70 | 0.6× |
| Standard adult | 1.0× |

Arm targeting pivots on stature: mid-torso for anyone under 1.4m, shoulder height otherwise. Approach velocity scales down in lockstep with the force multiplier.

### 5.3 What Comes Back

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

## 6. Getting Started

### 6.1 Robotics Integration Path

1. Hit `/hugs/{type}` to pull the embrace you want
2. Walk through the `steps` array — each entry carries an `action` identifier and a human-readable `description`
3. Wire each `action` to the corresponding call inside your motor control layer
4. Implement every abort condition from `/safety` as a high-priority interrupt
5. Before each embrace, feed live sensor data into `/hugs/calibrate` and apply the returned adjustments

### 6.2 Minimum Hardware by Difficulty Tier

| Tier | Sensors Needed | Actuators Needed |
|------|---------------|-----------------|
| Beginner | Proximity detection, force feedback | Two-axis articulated arms, mobile base |
| Intermediate | + Height estimation, audio input/output | + Vertical lift mechanism, oscillation driver |
| Advanced | + Multi-body tracking, spatial clustering | + Independently controlled arm segments |

---

## 7. What Comes Next

- **Mood-aware selection** — Choose embrace type and hold duration by reading facial expressions in real time
- **Cultural defaults** — Region-tuned presets reflecting local greeting customs and personal-space expectations
- **Swarm coordination** — Multiple robots executing a synchronized group embrace
- **Continuous pressure tuning** — Adjust grip force mid-embrace based on live muscle-tension feedback
- **Biometric integration** — Pull heart rate and skin conductance data from wearables to optimize when to let go

---

## 8. Final Word

HugBot API is a foundational step toward normalizing safe, consensual physical affection in human-robot interaction. By publishing an open, free, platform-neutral instruction protocol with safety engineered into its core, the project removes the need for every robotics team to independently solve the same biomechanical puzzle.

Source code and full documentation live at: **https://github.com/israelburns/hug-bot-api**

---

## References

- Cohen, S., et al. (2015). "Does Hugging Provide Stress-Buffering Social Support?" *Psychological Science*, 26(2), 135-147.
- Strabala, K., et al. (2013). "Toward Seamless Human-Robot Handovers." *Journal of Human-Robot Interaction*, 2(1), 112-132.
- ISO 13482:2014. "Robots and robotic devices — Safety requirements for personal care robots."
- Haddadin, S., et al. (2017). "Robot Collisions: A Survey on Detection, Isolation, and Identification." *IEEE Transactions on Robotics*, 33(6), 1292-1312.

---

*HugBot API v1.0 — Teaching machines the art of a proper embrace.*
