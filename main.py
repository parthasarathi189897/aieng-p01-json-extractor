import json

from output_generator import ExtractionFailed, extract


# Step 6: batch runner over all 20 fixtures
def main():
    with open("data/test-inputs.json") as f:
        fixtures = json.load(f)

    passed = 0
    for fixture in fixtures:
        try:
            triage, attempts = extract(fixture["message"])
            ok = True
            detail = f"{triage.category}/{triage.sentiment}/urgency={triage.urgency}"
        except ExtractionFailed as e:
            attempts = e.attempts
            # empty input is supposed to be rejected, so that counts as a pass
            ok = fixture["case"] == "empty_input" and e.reason == "empty input"
            detail = e.reason
        passed += ok
        print(f"#{fixture['id']} {fixture['case']}: {'PASS' if ok else 'FAIL'} attempts={attempts} {detail}")

    print(f"Total: {passed}/{len(fixtures)} passed")


if __name__ == "__main__":
    main()
