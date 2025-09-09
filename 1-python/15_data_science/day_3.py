import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Load data set
data = pd.read_csv("experience_salary.csv")

x = data[["YearsExperience"]]  # independent variable
y = data[["Salary"]]  # dependent variable

model = LinearRegression()
model.fit(x, y)

data["PredictedSalary"] = model.predict(x)

print("Model Coefficient (slope)", round(float(model.coef_[0]), 2))
print("Model INtercept (base salary)", round(float(model.intercept_), 2))

plt.scatter(x, y, color="blue", label="Actual Data")
plt.plot(x, data["PredictedSalary"], color="red", label="Regression Line")
plt.xlabel("Years of Experience")
plt.ylabel("Salary")
plt.title("Salary vs Experience")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
