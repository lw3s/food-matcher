import pandas as pd

ingredient1 = 'Pumpkin'
ingredient2 = 'Mango'

tasteTrioDF = pd.read_csv('datasets/taste_trios.csv')
highlyCompatibleTrioDF = tasteTrioDF[tasteTrioDF['Classification Output'] == 'Highly Compatible']
moderatelyCompatibleTrioDF = tasteTrioDF[tasteTrioDF['Classification Output'] == 'Moderately Compatible']
compatibleTrioDF = tasteTrioDF[tasteTrioDF['Classification Output'] == 'Compatible']

def get_All_Compatible_Ingredients_Of_Ingredient(ingredient: str, compatibility):
    """
    Get all ingredients that are compatible of the given compatibility level with the input ingredient

    @param ingredient: one of the ingredients in the dataset
    @param compatibility: 'highly' or 'moderately' or 'compatible'
    @return: a set of strings representing the ingredients that are compatible with the input ingredient of the given compatibility level
    """
    #Get all rows where ingredient appears in any column
    if compatibility == 'highly':
        matchesWithIngredient = highlyCompatibleTrioDF[
            (highlyCompatibleTrioDF['Ingredient 1'] == ingredient) |
            (highlyCompatibleTrioDF['Ingredient 2'] == ingredient) |
            (highlyCompatibleTrioDF['Ingredient 3'] == ingredient)
        ]
    elif compatibility == 'moderately':
        matchesWithIngredient = moderatelyCompatibleTrioDF[
            (moderatelyCompatibleTrioDF['Ingredient 1'] == ingredient) |
            (moderatelyCompatibleTrioDF['Ingredient 2'] == ingredient) |
            (moderatelyCompatibleTrioDF['Ingredient 3'] == ingredient)
        ]
    elif compatibility == 'compatible':
        matchesWithIngredient = compatibleTrioDF[
            (compatibleTrioDF['Ingredient 1'] == ingredient) |
            (compatibleTrioDF['Ingredient 2'] == ingredient) |
            (compatibleTrioDF['Ingredient 3'] == ingredient)
        ]


    ingredients_set = set() #This set will store all ingredients that are compatible with ingredient1
    for _, row in matchesWithIngredient.iterrows():
        ingredients_set.update([row['Ingredient 1'], row['Ingredient 2'], row['Ingredient 3']])
    ingredients_set.remove(ingredient)  
    return ingredients_set
    

def check_for_connections(ingredient1: str, ingredient2: str, compatibilityLevel): 
    """
    Check if there is a connection between two ingredients of the given compatibility level by checking if there is a 3rd ingredient that is compatible with both ingredient1 and ingredient2

    @param ingredient1: one of the ingredients in the dataset
    @param ingredient2: another one of the ingredients in the dataset
    @param compatibilityLevel: 'highly' or 'moderately' or 'compatible'
    @return: Set of ingredients that are compatible with both ingredient1 and ingredient2
    """
    #Assuming it is NOT in the same taste trio, we will check if there is a connection between the two ingredients
    #Goal is to find a 3rd ingredient that is compatible with both ingredient1 and ingredient2, even though ingredient1 and ingredient2 are not in the same taste trio
    #Get all rows where ingredient1 appears in any column
    ingredients1_set = get_All_Compatible_Ingredients_Of_Ingredient(ingredient1, compatibilityLevel)    
    ingredients2_set = get_All_Compatible_Ingredients_Of_Ingredient(ingredient2, compatibilityLevel)
    
    #Find overlapping ingredients
    matchesWithBothIngredients = list(ingredients1_set.intersection(ingredients2_set))

    """ #Use this to print all the ingredients that are compatible with both ingredient1 and ingredient2
    print(f"{compatibilityLevel} compatible ingredients between {ingredient1} and {ingredient2}:")
    print(matchesWithBothIngredients)
    print('---------------------------------------------------------------------------')

    print(f"{compatibilityLevel} compatible ingredients that pair with {ingredient1}:")
    print(ingredients1_set)
    print('---------------------------------------------------------------------------')

    print(f"{compatibilityLevel} compatible ingredients that pair with {ingredient2}:")
    print(ingredients2_set)
    print('---------------------------------------------------------------------------')
    """
    return matchesWithBothIngredients

def BFS_Connections_Search(ingredient1: str, ingredient2: str, compatibilityLevel: str):
    """
    Perform a BFS search to find all possible connections between two ingredients of the given compatibility level

    @param ingredient1: one of the ingredients in the dataset
    @param ingredient2: another one of the ingredients in the dataset
    @param compatibilityLevel: 'highly' or 'moderately' or 'compatible'
    @return: Set of all intermediate ingredients found in paths between ingredient1 and ingredient2
    """
    
    MAX_DEPTH = 4 # Maximum number of "hops" to search through before giving up
    visited_paths = set()  
    queue = [(ingredient1, [ingredient1])]#Queue contains tuples of (current_ingredient, path_so_far), Each path_so_far is a list showing the sequence of ingredients from start to current
    all_paths = []    # Store all valid paths found from ingredient1 to ingredient2
    intermediate_ingredients = set()

    while queue:
        current_ingredient, path = queue.pop(0) #removes and returns the first element (FIFO queue behavior)
        if len(path) <= MAX_DEPTH:
            compatible_ingredients = get_All_Compatible_Ingredients_Of_Ingredient(current_ingredient, compatibilityLevel)
            
            # Check each compatible ingredient
            for next_ingredient in compatible_ingredients:
                new_path = path.copy()
                new_path.append(next_ingredient)
                path_key = tuple(new_path)  # Convert path to tuple for hashing
                
                if next_ingredient == ingredient2 and len(new_path) <= MAX_DEPTH :
                    if path_key not in visited_paths:
                        visited_paths.add(path_key)
                        all_paths.append(new_path)
                        intermediate_ingredients.update(new_path[1:-1])  # Add all intermediate ingredients (excluding start and end)
                
                if len(new_path) <= MAX_DEPTH and path_key not in visited_paths:
                    visited_paths.add(path_key)
                    queue.append((next_ingredient, new_path))

    
    """if all_paths: #Use this to print all paths
        print(f"\nFound {len(all_paths)} connections between {ingredient1} and {ingredient2}:")
        all_paths.sort(key=len)
        for path in all_paths:
            print(" -> ".join(path))

    else:
        print(f"\nNo connections found between {ingredient1} and {ingredient2} within {MAX_DEPTH} steps")
    """
    return intermediate_ingredients

ingredientsList1 = check_for_connections(ingredient1, ingredient2, 'highly')
#check_for_connections(ingredient1, ingredient2, 'moderately')
 #check_for_connections(ingredient1, ingredient2, 'compatible')

ingredientsList2 = BFS_Connections_Search(ingredient1, ingredient2, 'highly')

print("\n")
print(f"Check For Connections Function: {ingredientsList1}")
print('--------------------------------')
print(f"BFS Connections Search Function: {ingredientsList2}")
print("\n")

