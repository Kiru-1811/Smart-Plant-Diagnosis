import json

def get_solution(disease_name):
    try:
        with open("data/maize_recommendation.json", "r") as file:
            data = json.load(file)

        for item in data:
            if item["disease_name"].lower() == disease_name.lower():
                return item

        return {"error": "No recommendation found for this disease."}

    except FileNotFoundError:
        return {"error": "Maize recommendation file not found."}