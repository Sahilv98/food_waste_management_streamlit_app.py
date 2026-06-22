import sqlite3
import pandas as pd

conn = sqlite3.connect("database/food_waste.db")

# Category 1 Food Providers & Receivers

# Q1 How many food providers and receivers are there in each city?
print("--- Providers per City ---")
print(pd.read_sql("SELECT City, COUNT(*) AS Total_Providers FROM providers GROUP BY City", conn))

print("\n--- Receivers per City ---")
print(pd.read_sql("SELECT City, COUNT(*) AS Total_Receivers FROM receivers GROUP BY City", conn))

#Q2 Which type of food provider (restaurant, grocery store, etc.) contributes the most food?
print(pd.read_sql("SELECT Provider_Type, SUM(Quantity) as contribution_total FROM food_listings GROUP BY Provider_type ORDER BY contribution_total DESC",conn))

#Q3 What is the contact information of food providers in a specific city?
print("\nCity Wise Porvider Details")
print(pd.read_sql("""
    \nSELECT City, Name, Address, Contact,
    ROW_NUMBER() OVER (PARTITION BY City ORDER BY Name) AS Provider_Number
    FROM providers""",conn))

# print(pd.read_sql("""
#     SELECT City, Name, Address, Contact,
#            ROW_NUMBER() OVER (PARTITION BY City ORDER BY Name) AS Provider_Number
#     FROM providers
#     WHERE City IN ('New Carol', 'South Christopherborough')
# """, conn))

# Q4: Which receivers have claimed the most food?
print(pd.read_sql("""
    SELECT r.Name, SUM(f.Quantity) AS Total_Claimed
    FROM claims c
    JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
    JOIN food_listings f ON c.Food_ID = f.Food_ID
    GROUP BY r.Name
    ORDER BY Total_Claimed DESC
""", conn))

# Category 2 - Food Listings & Availability
# Q5 What is the total quantity of food available from all providers?
print(pd.read_sql("SELECT SUM(QUANTITY) from food_listings",conn))

# Q6: Which city has the highest number of food listings?
print(pd.read_sql("""
    \nSELECT Location, COUNT(Location) as total_listing from food_listings
    GROUP BY Location ORDER BY total_listing DESC""",
conn))

# Q7 What are the most commonly available food types?
print(pd.read_sql("""
    \nSELECT Food_Type, COUNT(*) as food_type_count from food_listings
    GROUP BY Food_Type ORDER BY food_type_count DESC""",
conn))

## Category 3 - Claims & Distribution
# Q8: How many food claims have been made for each food item?
print(pd.read_sql("""
    \nSELECT f.Food_Name, COUNT(c.Claim_ID) as Claims_count 
    FROM food_listings f 
    JOIN claims c on f.Food_ID = c.Claim_ID
    GROUP BY f.Food_Name ORDER BY Claims_count DESC""",
conn))

# Q9: Which provider has had the highest number of successful food claims?
print(pd.read_sql("""
    \nSELECT p.Name, COUNT(c.Claim_ID) as successful_claims
    FROM providers p 
    JOIN food_listings f on p.Provider_ID = f.Provider_ID
    JOIN claims c on f.Food_ID = c.Food_ID
    WHERE c.Status = "Completed"
    GROUP BY p.Name 
    ORDER BY successful_claims DESC""",
conn))

# Q10 What percentage of food claims are completed vs. pending vs. cancelled?
print(pd.read_sql("""
    \nSELECT
    ROUND(SUM(CASE WHEN Status="Completed" THEN 1 ELSE 0 END)*100/COUNT(*),2) AS COmplete_pct,
    ROUND(SUM(CASE WHEN Status="Pending" THEN 1 ELSE 0 END)*100/COUNT(*),2) AS Pending_pct,
    ROUND(SUM(CASE WHEN Status="Cancelled" THEN 1 ELSE 0 END)*100/COUNT(*),2) AS Cancelled_pct
    FROM claims""",
conn))

# Category 4 - Analysis & Insights
# Q11 What is the average quantity of food claimed per receiver?
print(pd.read_sql("""
    SELECT r.Name, AVG(f.Quantity) AS Avg_Quantity_Claimed
    FROM claims c
    JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
    JOIN food_listings f ON c.Food_ID = f.Food_ID
    GROUP BY r.Name
    ORDER BY Avg_Quantity_Claimed DESC
""", conn))

# Q12: Which meal type is claimed the most?
print(pd.read_sql("""
    \nSELECT f.Meal_Type, COUNT(c.Claim_ID) as Claims_count 
    FROM food_listings f 
    JOIN claims c on f.Food_ID = c.Claim_ID
    GROUP BY f.Meal_Type 
    ORDER BY Claims_count DESC""",
conn))

# Q13: What is the total quantity of food donated by each provider?
print(pd.read_sql("""
    \nSELECT p.Name, SUM(f.Quantity) as QTY_Donated
    FROM providers p 
    JOIN food_listings f on p.Provider_ID = f.Provider_ID
    GROUP BY p.Name
    ORDER BY QTY_Donated DESC""",
conn))

# Q14: Which food items are nearing expiry (within 2 days) and still unclaimed?
print(pd.read_sql("""
    SELECT f.Food_Name, f.Expiry_Date, f.Quantity, f.Location
    FROM food_listings f
    LEFT JOIN claims c ON f.Food_ID = c.Food_ID
    WHERE c.Food_ID IS NULL
    AND DATE(f.Expiry_Date) <= DATE('now', '+2 days')
    ORDER BY f.Expiry_Date ASC
""", conn))

# Q15: Which city has the highest food claim completion rate?

print(pd.read_sql("""
    SELECT f.Location,
    ROUND(SUM(CASE WHEN c.Status="Completed" THEN 1 ELSE 0 END) * 100 /COUNT(*),2) AS Completion_Rate
    FROM food_listings f
    JOIN claims c ON f.Food_ID = c.Food_ID
    GROUP BY f.Location
    ORDER BY Completion_Rate Desc
""", conn))