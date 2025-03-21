import pandas as pd

ingredient1 = 'Pumpkin'
ingredient2 = 'Cinnamon'

tasteTrioDF = pd.read_csv('datasets/taste_trios.csv')
compatibleTrioDF = tasteTrioDF[tasteTrioDF['Classification Output'] == 'Highly Compatible']


def check_for_connections(ingredient1: str, ingredient2: str): 
    #Assuming it is NOT in the same taste trio, we will check if there is a connection between the two ingredients
    #Goal is to find a 3rd ingredient that is compatible with both ingredient1 and ingredient2, even though ingredient1 and ingredient2 are not in the same taste trio
    #Get all rows where ingredient1 appears in any column
    matchesWithIngredient1 = compatibleTrioDF[
        (compatibleTrioDF['Ingredient 1'] == ingredient1) | #The "|" is a logical OR operator which combines all three rows into one, just learnt it today lmao
        (compatibleTrioDF['Ingredient 2'] == ingredient1) |
        (compatibleTrioDF['Ingredient 3'] == ingredient1)
    ]
    
    #Get all rows where ingredient2 appears in any column
    matchesWithIngredient2 = compatibleTrioDF[
        (compatibleTrioDF['Ingredient 1'] == ingredient2) |
        (compatibleTrioDF['Ingredient 2'] == ingredient2) |
        (compatibleTrioDF['Ingredient 3'] == ingredient2)
    ]

    ingredients1_set = set() #This set will store all ingredients that are compatible with ingredient1
    for _, row in matchesWithIngredient1.iterrows():
        ingredients1_set.update([row['Ingredient 1'], row['Ingredient 2'], row['Ingredient 3']])
    ingredients1_set.remove(ingredient1)  
    
    ingredients2_set = set() #This set will store all ingredients that are compatible with ingredient2
    for _, row in matchesWithIngredient2.iterrows():
        ingredients2_set.update([row['Ingredient 1'], row['Ingredient 2'], row['Ingredient 3']])
    ingredients2_set.remove(ingredient2)
    
    #Find overlapping ingredients
    matchesWithBothIngredients = list(ingredients1_set.intersection(ingredients2_set))

    print(f"Common ingredients between {ingredient1} and {ingredient2}:")
    print(matchesWithBothIngredients)
    print('---------------------------------------------------------------------------')

    print(f"Ingredients that pair with {ingredient1}:")
    print(ingredients1_set)
    print('---------------------------------------------------------------------------')

    print(f"Ingredients that pair with {ingredient2}:")
    print(ingredients2_set)
    print('---------------------------------------------------------------------------')

check_for_connections(ingredient1, ingredient2)


