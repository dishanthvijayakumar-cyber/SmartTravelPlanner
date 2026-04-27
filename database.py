import sqlite3

with open('destinations.sql', 'r') as f: #according to the slides
    sql_script = f.read()

connection = sqlite3.connect('destinations.db')
connection.executescript(sql_script)
connection.commit()

connection = sqlite3.connect('destinations.db')


def get_destinations(): #AI-generated 
    # Connect to the SQLite database file
    conn = sqlite3.connect('destinations.db')
    #Allow accessing columns by name instead of index
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    #Report all destinations from the destinations table
    cursor.execute("SELECT * FROM destinations")
    destinations = cursor.fetchall() #AI-generated: report all rows as a list

    result = []
    for dest in destinations:
        #For each destination, it reports its associated tags (styles, interests, activities, accommodation)
        cursor.execute(
            "SELECT tag_type, tag_value FROM destination_tags WHERE destination_id = ?",
            (dest["id"],) #AI-generated: uses parameterized query to avoid SQL injection
        )
        tags = cursor.fetchall() 

        #Create empty lists for each tag type
        styles, interests, activities, accommodations = [], [], [], []

        #Sort each tag into the correct list based on its type
        for tag in tags:
            if tag["tag_type"] == "style":
                styles.append(tag["tag_value"])
            elif tag["tag_type"] == "interest":
                interests.append(tag["tag_value"])
            elif tag["tag_type"] == "activity":
                activities.append(tag["tag_value"])
            elif tag["tag_type"] == "accommodation":
                accommodations.append(tag["tag_value"])

        #Build a dictionary for this destination with all its data and tags and add it to the results list
        result.append({
            "id": dest["id"],
            "place": dest["place"],
            "country": dest["country"],
            "climate": dest["climate"],
            "budget_min": dest["budget_min"],
            "budget_max": dest["budget_max"],
            "description_sentence": dest["description_sentence"],
            "best_for": dest["best_for"],
            "pace": [dest["pace"]],
            "styles": styles,
            "interests": interests,
            "activities": activities,
            "accommodation": accommodations,
        })

    conn.close() #AI-generated: Close the database connection to free up resources
    return result
