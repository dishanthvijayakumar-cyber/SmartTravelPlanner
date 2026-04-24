import sqlite3

with open('destinations.sql', 'r') as f:
    sql_script = f.read()

connection = sqlite3.connect('destinations.db')
connection.executescript(sql_script)
connection.commit()

connection = sqlite3.connect('destinations.db')

def get_destinations(): #AI-generated
    conn = sqlite3.connect('destinations.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM destinations")
    destinations = cursor.fetchall() #AI-generated

    result = []
    for dest in destinations:
        cursor.execute(
            "SELECT tag_type, tag_value FROM destination_tags WHERE destination_id = ?",
            (dest["id"],) #AI-generated
        )
        tags = cursor.fetchall() #AI-generated

        styles, interests, activities, accommodations = [], [], [], []
        for tag in tags:
            if tag["tag_type"] == "style":
                styles.append(tag["tag_value"])
            elif tag["tag_type"] == "interest":
                interests.append(tag["tag_value"])
            elif tag["tag_type"] == "activity":
                activities.append(tag["tag_value"])
            elif tag["tag_type"] == "accommodation":
                accommodations.append(tag["tag_value"])

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

    conn.close()
    return result