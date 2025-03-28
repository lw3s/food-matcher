import pandas as pd

ingredient1 = 'Pumpkin'
ingredient2 = 'Cinnamon'

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
    Check if there is a connection between two ingredients of the given compatibility level

    @param ingredient1: one of the ingredients in the dataset
    @param ingredient2: one of the ingredients in the dataset
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

    print(f"{compatibilityLevel} compatible ingredients between {ingredient1} and {ingredient2}:")
    print(matchesWithBothIngredients)
    print('---------------------------------------------------------------------------')

    print(f"{compatibilityLevel} compatible ingredients that pair with {ingredient1}:")
    print(ingredients1_set)
    print('---------------------------------------------------------------------------')

    print(f"{compatibilityLevel} compatible ingredients that pair with {ingredient2}:")
    print(ingredients2_set)
    print('---------------------------------------------------------------------------')
    
check_for_connections(ingredient1, ingredient2, 'highly')
check_for_connections(ingredient1, ingredient2, 'moderately')
check_for_connections(ingredient1, ingredient2, 'compatible')

