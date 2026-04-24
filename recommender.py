from database import get_destinations

def calculate_score(destinations, preferences):
    score = 0

    # STYLE (100/7 = 14.28 pts)
    user_style = preferences["travel_style"].split(":")[0].strip() # split for delete what comes after the style and strip to delete the spaces
    if user_style in destinations["styles"]:
        score += 14.28

    #CLIMATE (100/7 = 14.28 pts)
    user_climate = preferences ["ideal_climate"]
    if user_climate == destinations ["climate"]:
        score += 14.28

    #INTERESTS (100/7 = 14.28 pts)
    user_interests = preferences["interests"]
    if user_interests:
        matches = 0
        for interest in user_interests:
            if interest in destinations["interests"]:
                matches += 1
        score += 14.28 * (matches / len(user_interests))

    #DAILY BUDGET (100/7 = 14.28 pts)
    user_budget = preferences["daily_budget"]
    if destinations["budget_min"] <= user_budget <= destinations["budget_max"]:
        score += 14.28

    #ACTIVITIES (100/7 = 14.28 pts)
    user_activities = preferences["activities"]
    if user_activities:
        matches = 0
        for activities in user_activities:
            if activities in destinations["activities"]:
                matches += 1
        score += 14.28 * (matches / len(user_activities))

    #ACCOMODATION (100/7 = 14.28 pts)
    user_accommodation = preferences["accommodation"]
    if user_accommodation:
        matches = 0
        for accommodation in user_accommodation:
            if accommodation in destinations["accommodation"]:
                matches += 1
        score += 14.28 * (matches / len(user_accommodation))

    #TRAVEL PACE (100/7 = 14.28 pts)
    user_pace = preferences ["travel_pace"]
    if user_pace in destinations["pace"]:
        score += 14.28

    return score


def get_recommendations(preferences, top_n=10):
    all_destinations = get_destinations()
    results = []
    for destination in all_destinations:
        score = calculate_score(destination, preferences)
        destination["score"] = round(score, 1)
        results.append(destination)
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]