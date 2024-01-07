# import re
# import requests


# # Updated list of non-halal ingredients
# non_halal_ingredients = [
#     # Alcoholic Fermentation
#     "alcohol", "bear", "bear flavor", "bear batters", "fermented cider", "hard cider", "rum",
#     "torula yeast grown on liquor", "soya sauce", "sherry wine", "vanilla extract", "wine", "wine vinegar",

#     # Human Body
#     "l-cysteine",

#     # Pig
#     "bacon", "ham", "gelatin", "enzymes", "rennin", "pepsin", "marshmallow containing pork gelatin", "pork",
#     "bacon bits",

#     # Pig Mixed with Grain & Plant-Based Ingredients
#     "beta-carotene", "cheese & dairy cultures", "enzyme modified soya lecithin", "tofu",

#     # Mineral, Chemical, and Synthetic Ingredients Mixed with Pork By-products
#     "artificial flavors", "bha & bht",

#     # Dairy Ingredients Made from Pork Enzymes or Cultures Grown on Pork Fat
#     "butter fat lipolyzed", "buttermilk solids", "caseinates (sodium & calcium)", "rennet casein", "cheese powder",
#     "cultured cream lipolyzed", "cultured milk", "lactose", "sour cream solids", "reduced mineral whey", "rennet",
#     "whey",
#     "whey protein concentrate",

#     # Pig Fat
#     "calcium stearate", "calcium stearoyl lactylate", "datem", "diglyceride", "ethoxylated mono- and diglycerides",
#     "glycerin", "glycerol ester", "glycerol monostearate", "hydroxylated lecithin", "lard", "margarine",
#     "mono- and diglycerides", "monoglyceride", "natural flavors", "polyglycerol esters of fatty acids",
#     "polyoxyethylene sorbitan monostearate", "polysorbate 60", "polysorbate 65", "polysorbate 80",
#     "propylene glycol monostearate", "sodium lauryl sulfate", "sodium stearoyl lactylate", "softener",
#     "sorbitan monostearate", "tocopherol",

#     # Vitamins from Pig's Liver & Other Pig Parts
#     "vitamin A", "vitamin B5", "vitamin B6", "vitamin B12", "vitamin E"
# ]


# def is_halal_product(ingredients):
#     # Remove special characters using regular expression
#     ingredients_clean = re.sub(r'[^a-zA-Z\s]', '', ingredients)

#     # Split the cleaned string into a list of words
#     ingredients_list = ingredients_clean.split()

#     for ingredient in ingredients_list:
#         # Check for explicit non-halal ingredients
#         if ingredient.lower() in non_halal_ingredients:
#             return False, ingredient

#         # Check for ingredients ending with -ol (excluding "alcohol")
#         if ingredient.lower().endswith("ol") and "alcohol" not in ingredient.lower():
#             return False, ingredient

#     return True, None


# def get_product_info(barcode):
#     api_url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}?fields=product_name,ingredients_text,allergens_from_ingredients"

#     try:
#         response = requests.get(api_url)
#         response.raise_for_status()

#         product_data = response.json()
#         return product_data

#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching product information: {e}")
#         return None



import re
import requests

# Updated list of non-halal ingredients
non_halal_ingredients = [
    # Alcoholic Fermentation
    "alcohol", "bear", "bear flavor", "bear batters", "fermented cider", "hard cider", "rum",
    "torula yeast grown on liquor", "soya sauce", "sherry wine", "vanilla extract", "wine", "wine vinegar",
    
    # Human Body
    "l-cysteine",
    
    # Pig
    "bacon", "ham", "gelatin", "enzymes", "rennin", "pepsin", "marshmallow containing pork gelatin", "pork", "bacon bits",
    
    # Pig Mixed with Grain & Plant-Based Ingredients
    "beta-carotene", "cheese & dairy cultures", "enzyme modified soya lecithin", "tofu",
    
    # Mineral, Chemical, and Synthetic Ingredients Mixed with Pork By-products
    "artificial flavors", "bha & bht",
    
    # Dairy Ingredients Made from Pork Enzymes or Cultures Grown on Pork Fat
    "butter fat lipolyzed", "buttermilk solids", "caseinates (sodium & calcium)", "rennet casein", "cheese powder",
    "cultured cream lipolyzed", "cultured milk", "lactose", "sour cream solids", "reduced mineral whey", "rennet", "whey",
    "whey protein concentrate",
    
    # Pig Fat
    "calcium stearate", "calcium stearoyl lactylate", "datem", "diglyceride", "ethoxylated mono- and diglycerides",
    "glycerin", "glycerol ester", "glycerol monostearate", "hydroxylated lecithin", "lard", "margarine",
    "mono- and diglycerides", "monoglyceride", "natural flavors", "polyglycerol esters of fatty acids",
    "polyoxyethylene sorbitan monostearate", "polysorbate 60", "polysorbate 65", "polysorbate 80",
    "propylene glycol monostearate", "sodium lauryl sulfate", "sodium stearoyl lactylate", "softener",
    "sorbitan monostearate", "tocopherol",
    
    # Vitamins from Pig's Liver & Other Pig Parts
    "vitamin A", "vitamin B5", "vitamin B6", "vitamin B12", "vitamin E"
]

# Non-vegan ingredients
non_vegan_ingredients = [
    "animal-derived", "butter", "casein", "cheese", "cream", "egg", "honey", "lactose", "meat", "milk", "non-vegan",
    "non-vegetarian", "non-veg", "non-veg ingredients", "non-vegan ingredients", "non-vegetarian ingredients",
    "non-veg items", "non-vegetarian items", "non-veg product", "non-vegetarian product", "non-veg food",
    "non-vegetarian food", "non-veg dish", "non-vegetarian dish", "non-veg recipe", "non-vegetarian recipe",
    "non-veg menu", "non-vegetarian menu", "non-veg category", "non-vegetarian category", "non-veg dish",
    "non-vegetarian dish", "non-veg menu", "non-vegetarian menu", "non-veg category", "non-vegetarian category"
]

def is_halal_product(ingredients):
    # Remove special characters using regular expression
    ingredients_clean = re.sub(r'[^a-zA-Z\s]', '', ingredients)

    # Split the cleaned string into a list of words
    ingredients_list = ingredients_clean.split()

    for ingredient in ingredients_list:
        # Check for explicit non-halal ingredients
        if ingredient.lower() in non_halal_ingredients:
            return False, ingredient

        # Check for ingredients ending with -ol (excluding "alcohol")
        if ingredient.lower().endswith("ol") and "alcohol" not in ingredient.lower():
            return False, ingredient

    return True, None

def analyze_dietary_restrictions(ingredients, labels_tags):
    # Check if any non-vegan ingredients are present
    vegan_friendly = not any(ingredient.lower() in non_vegan_ingredients for ingredient in ingredients)

    # Check if the product is suitable for a vegan diet
    vegan = 'vegan' in labels_tags and labels_tags['vegan'] == 'yes'

    # Check if the product is suitable for a vegetarian diet
    vegetarian = 'vegetarian' in labels_tags and labels_tags['vegetarian'] == 'yes'

    return vegan_friendly, vegetarian, vegan

def get_product_info(barcode):
    api_url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}?fields=product_name,ingredients_text,labels_tags"

    try:
        response = requests.get(api_url)
        response.raise_for_status()

        product_data = response.json()
        return product_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching product information: {e}")
        return None

# Example usage:
barcode = "3017624010701"
product_info = get_product_info(barcode)

if product_info:
    # Process and display the product information as needed
    product_name = product_info['product']['product_name']
    ingredients = product_info['product']['ingredients_text']
    labels_tags = product_info['product']['labels_tags']

    print(f"Product Name: {product_name}")
    print(f"Ingredients: {ingredients}")
    print(f"Labels: {labels_tags}")

    # Check if the product is halal
    halal_status, non_halal_ingredient = is_halal_product(ingredients)
    if halal_status:
        print("The product is halal.")
    else:
        print(f"The product is not halal. Non-halal ingredient found: {non_halal_ingredient}")

    # Check for vegan and vegetarian friendliness
    vegan_friendly, vegetarian, vegan = analyze_dietary_restrictions(ingredients, labels_tags)

    if vegan_friendly:
        print("The product is suitable for a vegan diet.")
    else:
        print("The product is not suitable for a vegan diet.")

    if vegetarian:
        print("The product is suitable for a vegetarian diet.")
    else:
        print("The product is not suitable for a vegetarian diet.")

    # Additional information based on vegan and vegetarian labels
    if 'vegan' in labels_tags:
        if vegan:
            print("The product is explicitly labeled as suitable for a vegan diet.")
        else:
            print("The product is not explicitly labeled as suitable for a vegan diet.")
    else:
        print("The product information does not specify if it")
