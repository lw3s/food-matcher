import pandas as pd
df = pd.read_csv('datasets/taste_trios.csv')
print(df)
flavorOne = input("Enter the first flavor: ")
flavorTwo = input("Enter the second flavor: ")

# Convert compatibility levels to numeric scores
compatibility_scores = {
    'Highly Compatible': 3,
    'Moderately Compatible': 2,
    'Compatible': 1
}

# Search for combinations with the input flavors
matches = df[
    ((df['Ingredient 1'] == flavorOne) & (df['Ingredient 2'] == flavorTwo)) |
    ((df['Ingredient 1'] == flavorTwo) & (df['Ingredient 2'] == flavorOne))
]

if len(matches) == 0:
    print(f"No matches found for {flavorOne} and {flavorTwo}")
else:
    # Add compatibility scores
    matches['Score'] = matches['Classification Output'].map(compatibility_scores)
    
    # Sort by score and get the best match
    best_match = matches.sort_values('Score', ascending=False).iloc[0]
    
    print(f"\nBest matching third ingredient: {best_match['Ingredient 3']}")
    print(f"Compatibility: {best_match['Classification Output']}")
    
    # Show all possible matches
    print("\nAll possible matches:")
    for _, row in matches.sort_values('Score', ascending=False).iterrows():
        print(f"- {row['Ingredient 3']} ({row['Classification Output']})")


