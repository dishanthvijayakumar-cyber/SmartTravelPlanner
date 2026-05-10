import sqlite3 #Import the built-in SQLite library to interact with .db database files

with open('destinations.sql', 'r') as f: #According to the slides: open the SQL script file in read mode
    sql_script = f.read() #Read the entire SQL file content into a string variable

connection = sqlite3.connect('destinations.db') #Open the SQLite database file
connection.executescript(sql_script) #Run all SQL statements in the script to set up tables and data
connection.commit() #Save all changes made by the script to the database

connection = sqlite3.connect('destinations.db') #Reconnect to the database for subsequent use


#AI-generated: function that retrieves all destinations with their tags
def get_destinations():  
    conn = sqlite3.connect('destinations.db') #Connect to the SQLite database file
    conn.row_factory = sqlite3.Row #Allow accessing columns by name instead of index
    cursor = conn.cursor() #Create a cursor object used to execute SQL queries

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
