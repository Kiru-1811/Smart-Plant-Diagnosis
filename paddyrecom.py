import json

def get_solution(disease_name):
    
    try:
        # Open JSON file
        with open("data/paddy_recommendation.json", "r") as file:
            data = json.load(file)

        # Search for matching disease
        for item in data:
            if item["disease_name"].lower() == disease_name.lower():
                return item

        # If disease not found
        return {"error": "No recommendation found for this disease."}

    except FileNotFoundError:
        return {"error": "JSON file not found."}

    except Exception as e:
        return {"error": str(e)}