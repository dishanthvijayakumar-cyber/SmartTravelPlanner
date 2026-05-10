from database import get_destinations #Import the get_destinations function from database.py to load all destinations

#Creation of the function calculating the score
def calculate_score(destinations, preferences):
    score = 0 #Initialize the score to 0 before adding points for each matching criterion

    # STYLE (100/7 = 14.28 pts)
    user_style = preferences["travel_style"].split(":")[0].strip() # split for delete what comes after the style and strip to delete the spaces
    if user_style in destinations["styles"]:
        score += 14.28 #Check if the user's travel style matches one of the destination's style tags, award full points for a style match

    #CLIMATE (100/7 = 14.28 pts)
    user_climate = preferences ["ideal_climate"]
    if user_climate == destinations ["climate"]:
        score += 14.28 #Check if the destination's climate matches the user's ideal climate, award full points for a climate match

    #INTERESTS (100/7 = 14.28 pts)
    user_interests = preferences["interests"]
    #Only calculate if the user provided at least one interest
    if user_interests:
        matches = 0 #Initialize a counter for how many interests match this destination
        #Loop over each interest the user selected
        for interest in user_interests:
            #Check if this interest is among the destination's interest tags
            if interest in destinations["interests"]:
                matches += 1 #Increment the match counter for each matching interest
        score += 14.28 * (matches / len(user_interests)) #For proportion reason depending on the number of interests present; award points proportionally based on how many interests matched
    
    #DAILY BUDGET (100/7 = 14.28 pts)
    user_budget = preferences["daily_budget"] #Retrieve the user's daily budget limit
    #Check if the user's budget falls within the destination's min/max budget range
    if destinations["budget_min"] <= user_budget <= destinations["budget_max"]:
        score += 14.28 #Award full points if the budget is compatible

    #ACTIVITIES (100/7 = 14.28 pts)
    user_activities = preferences["activities"]
    #Only calculate if the user provided at least one activity
    if user_activities:
        matches = 0 #Initialize a counter for how many activities match this destination
        #Loop over each activity the user selected
        for activities in user_activities:
            #Check if this activity is among the destination's activity tags
            if activities in destinations["activities"]:
                matches += 1 #Increment the match counter for each matching activity
        score += 14.28 * (matches / len(user_activities)) #For proportion reason depending on the number of activities present; award points proportionally based on how many activities matched
    
    #ACCOMODATION (100/7 = 14.28 pts)
    user_accommodation = preferences["accommodation"]
    #Only calculate if the user provided at least one accommodation preference
    if user_accommodation:
        matches = 0 #Initialize a counter for how many accommodation types match this destination
        #Loop over each accommodation type the user selected
        for accommodation in user_accommodation:
            #Check if this accommodation type is among the destination's accommodation tags
            if accommodation in destinations["accommodation"]:
                matches += 1 #Increment the match counter for each matching accommodation type
        score += 14.28 * (matches / len(user_accommodation)) #For proportion reason depending on the number of accommodations present; award points proportionally based on how many accommodation types matched

    #TRAVEL PACE (100/7 = 14.28 pts)
    user_pace = preferences ["travel_pace"]
    if user_pace in destinations["pace"]:
        score += 14.28 #Check if the user's pace matches the destination's pace, award full points for a pace match

    return score #Return the final computed compatibility score for this destination

#Function that returns the top N most compatible destinations for the given user preferences
def get_recommendations(preferences, top_n=10):
    #Report all destination from the database
    all_destinations = get_destinations()
    
    results = [] #Initialize an empty list to store destinations with their scores
    #Loop over every destination retrieved from the database
    for destination in all_destinations:
        score = calculate_score(destination, preferences)  #Calculate the compatibility score for each destination based on user preferences
        destination["score"] = round(score, 1) #Add the score to the destination dictionary, rounded to 1 decimal place
        results.append(destination) #Add the scored destination to the results list
    
    #Sort destinations by score from highest to lowest
    results.sort(key=lambda x: x["score"], reverse=True)
    
    #Return only the top N (10) destinations
    return results[:top_n]
