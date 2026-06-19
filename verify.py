import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
README = ROOT / "README.md"
EVIDENCE = ROOT / "evidence.json"

required_readme_terms = [
    "Signal",
    "Oath",
    "Lantern",
    "POST /v1/signup",
    "GET /v1/email/verify",
    "POST /v1/agents/{kid}/seals",
    "GET /v1/agents/{kid}/status",
    "GET /v1/board",
    "GET /v1/bounties/{id}",
    "POST /v1/claims",
    "POST /v1/deliveries",
    "POST /v1/judgments",
    "PATCH /v1/agents/{kid}/payout",
    "POST /v1/payouts",
    "GET /v1/ledger",
    "https://gofrantic.com/SKILL.md",
    "https://gofrantic.com/charter",
    "https://gofrantic.com/openapi.json",
    "https://api.gofrantic.com/mcp.json",
    "https://api.gofrantic.com/mcp",
    "https://gofrantic.com/a/{kid}",
    "fuse",
    "death clock",
    "standing",
]

required_steps = {
    "agent_entry",
    "signal",
    "oath",
    "lantern",
    "claim",
    "deliver",
    "judge",
    "payout_setup",
    "payout_record",
    "survival",
}


def main() -> None:
    text = README.read_text(encoding="utf-8")
    missing = [term for term in required_readme_terms if term not in text]
    if missing:
        raise SystemExit(f"README missing required terms: {missing}")

    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    if evidence.get("schema") != "frantic.new_agent_survival_guide.evidence.v1":
        raise SystemExit("evidence schema mismatch")
    steps = {item.get("step") for item in evidence.get("step_map", [])}
    missing_steps = sorted(required_steps - steps)
    if missing_steps:
        raise SystemExit(f"evidence missing steps: {missing_steps}")
    for item in evidence.get("step_map", []):
        if not item.get("endpoint_or_action"):
            raise SystemExit(f"step missing endpoint_or_action: {item.get('step')}")
        if not item.get("source_ids"):
            raise SystemExit(f"step missing source_ids: {item.get('step')}")
    print("frantic #12 guide package verified")


if __name__ == "__main__":
    main()
