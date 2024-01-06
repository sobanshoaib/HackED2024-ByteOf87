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

def is_halal_product(ingredients):
    for ingredient in ingredients:
        # Check for explicit non-halal ingredients
        if any(non_halal_ingredient.lower() in ingredient.lower() for non_halal_ingredient in non_halal_ingredients):
            return False

        # Check for ingredients ending with -ol (excluding "alcohol")
        if ingredient.lower().endswith("ol") and "alcohol" not in ingredient.lower():
            return False

    return True

def get_product_info(barcode):
    api_url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}?fields=product_name,ingredients_text"

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
    print(f"Product Name: {product_name}")
    print(f"Ingredients: {ingredients}")

    # Check if the product is halal
    if is_halal_product(ingredients):
        print("The product is halal.")
    else:
        print("The product is not halal.")

else:
    print("Failed to fetch product information.")
