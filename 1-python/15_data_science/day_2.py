import numpy as np
import pandas as pd

np.random.seed(42)

years = np.random.uniform(0.5, 10, 100).round(2)

salaries = (30_000 + years * 6_000 + np.random.normal(0, 4000, size=100)).round(2)

df = pd.DataFrame({"YearsExperience": years, "Salary": salaries})

df.to_csv("experience_salary.csv", index=False)
print("Data saved in file ✅")
