# HugBot API

A REST API that provides step-by-step instructions for robots on how to give safe, comfortable hugs to humans.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info and endpoint list |
| GET | `/hugs` | List all available hug types |
| GET | `/hugs/<type>` | Get instructions for a specific hug type |
| GET | `/hugs/random` | Get a random hug instruction set |
| GET | `/safety` | Safety rules all hugging robots must follow |
| POST | `/hugs/calibrate` | Calculate adjusted parameters for a specific human |

## Hug Types

- **standard** - Classic two-arm embrace (beginner)
- **gentle** - Light, soft hug for sensitive situations (beginner)
- **bear** - Firm, enthusiastic hug (intermediate)
- **side** - One-arm side hug (beginner)
- **group** - Multi-human group hug (advanced)

## Quick Start

```bash
pip install -r requirements.txt
python app.py
```

API runs at `http://localhost:5000`

## Example

```bash
curl http://localhost:5000/hugs/bear
```

Returns step-by-step motor instructions, pressure limits, and timing for a bear hug.

## Safety

Every hug instruction set includes force limits (in Newtons), approach speed caps, and abort conditions. The `/safety` endpoint returns the full safety ruleset including emergency stop triggers and fragile-human detection.

## Calibration

POST to `/hugs/calibrate` with human parameters to get adjusted instructions:

```bash
curl -X POST http://localhost:5000/hugs/calibrate \
  -H "Content-Type: application/json" \
  -d '{"human_height_m": 1.1, "human_age_estimate": 8, "hug_type": "gentle"}'
```

This auto-reduces force for children, elderly, and smaller humans.
