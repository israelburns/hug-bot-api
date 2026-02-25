from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# Hug instruction database for robots
HUG_TYPES = {
    "standard": {
        "name": "Standard Hug",
        "difficulty": "beginner",
        "steps": [
            {"step": 1, "action": "detect_human", "description": "Use proximity sensors to detect human within 1.5m radius"},
            {"step": 2, "action": "approach", "description": "Move toward human at 0.3 m/s max speed"},
            {"step": 3, "action": "stop", "description": "Halt at 0.4m distance from human torso"},
            {"step": 4, "action": "extend_arms", "description": "Extend both arms outward at shoulder height, palms facing inward"},
            {"step": 5, "action": "wrap", "description": "Gently close arms around human upper body with 2-5 N of force"},
            {"step": 6, "action": "hold", "description": "Maintain embrace for 3 seconds"},
            {"step": 7, "action": "release", "description": "Slowly open arms and retract to neutral position"},
            {"step": 8, "action": "step_back", "description": "Reverse 0.3m to restore personal space"}
        ],
        "pressure_limit_newtons": 5,
        "duration_seconds": 3
    },
    "gentle": {
        "name": "Gentle Hug",
        "difficulty": "beginner",
        "steps": [
            {"step": 1, "action": "detect_human", "description": "Use proximity sensors to detect human within 1.5m radius"},
            {"step": 2, "action": "approach", "description": "Move toward human at 0.2 m/s"},
            {"step": 3, "action": "stop", "description": "Halt at 0.5m distance"},
            {"step": 4, "action": "extend_arms", "description": "Slowly raise arms to mid-torso height"},
            {"step": 5, "action": "wrap", "description": "Lightly place arms around human with 1-2 N of force"},
            {"step": 6, "action": "hold", "description": "Hold for 2 seconds"},
            {"step": 7, "action": "release", "description": "Gently release and lower arms"},
            {"step": 8, "action": "step_back", "description": "Reverse 0.3m"}
        ],
        "pressure_limit_newtons": 2,
        "duration_seconds": 2
    },
    "bear": {
        "name": "Bear Hug",
        "difficulty": "intermediate",
        "steps": [
            {"step": 1, "action": "detect_human", "description": "Confirm human is adult via height sensor (must be > 1.4m)"},
            {"step": 2, "action": "announce", "description": "Play audio: 'Incoming bear hug!'"},
            {"step": 3, "action": "approach", "description": "Move toward human at 0.4 m/s"},
            {"step": 4, "action": "stop", "description": "Halt at 0.3m distance"},
            {"step": 5, "action": "extend_arms", "description": "Open arms wide at full wingspan"},
            {"step": 6, "action": "wrap", "description": "Firmly close arms around human with 5-10 N of force"},
            {"step": 7, "action": "lift_check", "description": "Optional: engage vertical actuators for slight 2cm lift"},
            {"step": 8, "action": "hold", "description": "Maintain for 4 seconds with slight sway pattern"},
            {"step": 9, "action": "release", "description": "Gradually reduce pressure over 1 second, then open arms"},
            {"step": 10, "action": "step_back", "description": "Reverse 0.4m"}
        ],
        "pressure_limit_newtons": 10,
        "duration_seconds": 4
    },
    "side": {
        "name": "Side Hug",
        "difficulty": "beginner",
        "steps": [
            {"step": 1, "action": "detect_human", "description": "Detect human and determine their facing direction"},
            {"step": 2, "action": "position", "description": "Navigate to stand beside human (left or right)"},
            {"step": 3, "action": "extend_arm", "description": "Extend nearest arm around human shoulders"},
            {"step": 4, "action": "squeeze", "description": "Apply 2-4 N lateral squeeze"},
            {"step": 5, "action": "hold", "description": "Hold for 2 seconds"},
            {"step": 6, "action": "release", "description": "Retract arm to neutral"},
            {"step": 7, "action": "step_away", "description": "Shift 0.3m laterally to restore space"}
        ],
        "pressure_limit_newtons": 4,
        "duration_seconds": 2
    },
    "group": {
        "name": "Group Hug",
        "difficulty": "advanced",
        "steps": [
            {"step": 1, "action": "scan_group", "description": "Count humans in 2m radius, require minimum 2"},
            {"step": 2, "action": "announce", "description": "Play audio: 'Group hug time!'"},
            {"step": 3, "action": "center", "description": "Move to center of detected human cluster"},
            {"step": 4, "action": "extend_arms", "description": "Open arms to maximum wingspan"},
            {"step": 5, "action": "wrap", "description": "Gently draw nearest humans inward with 3-5 N per arm"},
            {"step": 6, "action": "hold", "description": "Hold for 5 seconds"},
            {"step": 7, "action": "release", "description": "Open arms slowly"},
            {"step": 8, "action": "step_back", "description": "Reverse 0.5m from group center"}
        ],
        "pressure_limit_newtons": 5,
        "duration_seconds": 5
    }
}

SAFETY_RULES = {
    "max_force_newtons": 10,
    "max_approach_speed_ms": 0.5,
    "min_personal_space_m": 0.3,
    "require_consent": True,
    "emergency_stop": "Any resistance detected > 2N in opposite direction triggers immediate release",
    "fragile_human_mode": "If human height < 1.2m or age_estimate < 12, reduce all forces by 60%",
    "abort_conditions": [
        "Human steps backward",
        "Human raises hands in stop gesture",
        "Audio keyword 'stop' or 'no' detected",
        "Force feedback exceeds pressure limit"
    ]
}


@app.route("/")
def index():
    return jsonify({
        "name": "HugBot API",
        "version": "1.0.0",
        "description": "Instructions for robots on how to give safe, comfortable hugs",
        "endpoints": {
            "GET /hugs": "List all available hug types",
            "GET /hugs/<type>": "Get step-by-step instructions for a specific hug",
            "GET /hugs/random": "Get a random hug instruction set",
            "GET /safety": "Get safety rules all hugging robots must follow",
            "POST /hugs/calibrate": "Calculate adjusted parameters for a specific human"
        }
    })


@app.route("/hugs")
def list_hugs():
    summary = []
    for key, hug in HUG_TYPES.items():
        summary.append({
            "type": key,
            "name": hug["name"],
            "difficulty": hug["difficulty"],
            "steps_count": len(hug["steps"]),
            "duration_seconds": hug["duration_seconds"],
            "url": f"/hugs/{key}"
        })
    return jsonify({"hug_types": summary})


@app.route("/hugs/random")
def random_hug():
    key = random.choice(list(HUG_TYPES.keys()))
    hug = HUG_TYPES[key]
    return jsonify({"type": key, **hug})


@app.route("/hugs/<hug_type>")
def get_hug(hug_type):
    if hug_type not in HUG_TYPES:
        return jsonify({"error": f"Unknown hug type: {hug_type}", "available": list(HUG_TYPES.keys())}), 404
    return jsonify({"type": hug_type, **HUG_TYPES[hug_type]})


@app.route("/safety")
def safety():
    return jsonify({"safety_rules": SAFETY_RULES})


@app.route("/hugs/calibrate", methods=["POST"])
def calibrate():
    data = request.get_json() or {}
    human_height_m = data.get("human_height_m", 1.7)
    human_age_estimate = data.get("human_age_estimate", 30)
    hug_type = data.get("hug_type", "standard")

    if hug_type not in HUG_TYPES:
        return jsonify({"error": f"Unknown hug type: {hug_type}"}), 404

    hug = HUG_TYPES[hug_type]
    force_multiplier = 1.0

    if human_height_m < 1.2 or human_age_estimate < 12:
        force_multiplier = 0.4
    elif human_age_estimate > 70:
        force_multiplier = 0.6

    adjusted_pressure = round(hug["pressure_limit_newtons"] * force_multiplier, 1)
    arm_height = "mid-torso" if human_height_m < 1.4 else "shoulder"

    return jsonify({
        "hug_type": hug_type,
        "input": {"human_height_m": human_height_m, "human_age_estimate": human_age_estimate},
        "adjusted_parameters": {
            "pressure_limit_newtons": adjusted_pressure,
            "force_multiplier": force_multiplier,
            "arm_target_height": arm_height,
            "approach_speed_ms": 0.2 if force_multiplier < 1.0 else 0.3
        }
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
