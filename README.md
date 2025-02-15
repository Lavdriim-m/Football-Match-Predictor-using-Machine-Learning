# **Football Match Predictor - AI-Based Match Outcome Prediction**
🔮 **An AI-powered web application that predicts football match results and key statistics.**  
📚 **Built for:** Introduction to Artificial Intelligence Class  

---

## **📌 Project Contributors**
- **👨‍💻 Built By: Lavdrim Mustafi**
- **🎓 Professor: Dr. Azir Aliu**
- **📅 Course: Introduction to Artificial Intelligence**
- **🏫 University: SouthEast European University (SEEU)**

---

## **📌 Project Overview**
Football match prediction is a challenging task due to the complexity of team performance, player form, and match conditions.  
This project uses **Machine Learning (Gradient Boosting Regression)** to **predict match scores and key stats** such as:  
✔ Ball Possession  
✔ Goal Attempts  
✔ Shots on Goal  
✔ Corner Kicks  
✔ Free Kicks  
✔ Offsides  
✔ Yellow Cards  

🏆 **Objective:** Provide accurate, data-driven match predictions for football enthusiasts, analysts, and sports bettors.  
📡 **Final Output:** A **web-based application** where users can select teams and get AI-generated match insights.  

---

## **🛠 Technologies Used**
### **Backend**
- Python  
- Flask (Web Framework)  
- Scikit-learn (Machine Learning Library)  
- Pandas (Data Processing)  

### **Machine Learning Model**
- **Algorithm:** **Gradient Boosting Regressor**
- **Why?** It efficiently predicts **continuous numerical values** (match scores, possession, etc.).
- **Training Data:** Historical football match records (preprocessed and encoded).

### **Frontend**
- HTML  
- CSS (Custom Styling)  
- JavaScript (Dynamic UI Interactions)  

---

## **📌 How It Works**
1️⃣ **User selects** a home and away team from a dropdown list.  
2️⃣ **Flask Backend fetches** the encoded team data and passes it to the trained AI model.  
3️⃣ **Gradient Boosting Regressor predicts** match score and key game statistics.  
4️⃣ **Results are displayed** with an interactive UI, showing progress bars that **fill outward from the center** for a better comparison.  

---

## **📌 Setup Instructions**
### **1️⃣ Install Dependencies**
Make sure you have Python installed, then run:
```sh
pip install flask pandas scikit-learn
```

### **2️⃣ Clone This Repository**
```sh
git clone https://github.com/Lavdriim-m/Football-Match-Predictor-using-Machine-Learning.git
cd Football-Match-Predictor-using-Machine-Learning
```

### **3️⃣ Run the Application**
For Windows, run:
```sh
python app.py
```

For MacOS, run:
```sh
python3 app.py
```
Your web app should now be running at http://127.0.0.1:5000/ 🎉

---

## **📌 Usage Instructions**
- 1️⃣ Open the Web App in your browser (http://127.0.0.1:5000/).
- 2️⃣ Select a League for both home and away teams.
- 3️⃣ Choose Teams from the dropdown menus.
- 4️⃣ Click "Predict" to generate AI-based match insights.
- 5️⃣ View Results:
  - Predicted Score
  - Ball Possession %
  - Goal Attempts, Shots on Goal, etc.

**⚡ Try predicting matches from different leagues and compare stats!**

---

## **📌 App Screenshots**

### **Initial Look**
![Football Match Predictor](https://raw.githubusercontent.com/your-username/your-repo/main/screenshot.png](https://github.com/Lavdriim-m/Football-Match-Predictor-using-Machine-Learning/blob/main/FMP01.png?raw=true))

### **Match: Barcelona vs. Real Madrid**
![Football Match Predictor]([https://raw.githubusercontent.com/your-username/your-repo/main/screenshot.png](https://github.com/Lavdriim-m/Football-Match-Predictor-using-Machine-Learning/blob/main/FMP01.png?raw=true)](https://github.com/Lavdriim-m/Football-Match-Predictor-using-Machine-Learning/blob/main/FMP02.png?raw=true))

---

## **📌 License**

📄 This project is licensed under the **MIT License** – free to use and modify.
