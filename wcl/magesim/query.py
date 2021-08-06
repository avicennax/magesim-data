def extract(data):
    reports = {}
    dlq = []
    for i, report in enumerate(data):
        events_to_keep = []
        sources = {}
        mages = set()
        targets = set()
        events = report["events"]["data"]
        try:
            for event in events:
                # Save sourceID so we can grab later if they summon elemental.
                if event["type"] == "combatantinfo":
                    sources[event["sourceID"]] = event
                elif event["type"] == "summon" and event["abilityGameID"] == 31687:
                    events_to_keep.append(event)
                    events_to_keep.append(sources[event["sourceID"]])
                    targets.add(event["targetID"])
                    mages.add(event["sourceID"])
                # Waterbolt
                elif event["type"] == "damage" and event["abilityGameID"] == 31707:
                    events_to_keep.append(event)
                # Track buffs - especially drums and hero for elemental and mage.
                elif event["type"] in ["applybuff", "removebuff"] and (
                        event["targetID"] in targets or event["sourceID"] in mages):
                    events_to_keep.append(event)
        except Exception as err:
            code = report["code"]
            print(f"Error in {code}: {err}")
            dlq.append(code)
        else:
            reports[i] = events_to_keep

        
    return reports, dlq