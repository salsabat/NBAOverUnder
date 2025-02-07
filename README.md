# NBA Over/Under Prediction 

An NBA Over/Under prediction model built using machine learning techniques to predict a statistic of 
an NBA player based on past statistics and other game-related data. This project uses logistic regression to classify 
whether the player's target statistic in his next game will go over or under a given betting line. It is intended for sports analysts, bettors,
and anyone interested in analyzing NBA games.

## Getting Started 

**Prerequisites:** 
- Python 3.7+
- Java 21.x+ (if using the GUI)

**Installation:**
1. Clone this repository: `git clone https://github.com/yourusername/projectname.git` 
2. Navigate to the project directory: `cd projectname`
3. Create a virtual environment to isolate dependencies: `python3 -m venv venv`
4. Activate the virtual environment:
   - For Linux/macOS: `source venv/bin/activate`
   - For Windows: `venv\Scripts\activate`
5. Install the required dependencies: `pip install -r requirements.txt`

## Usage

### **Key Parameters**
1. **First Name**: The first name of the player (as found at https://www.nba.com/players)
2. **Last Name**: The last name of the player (as found at https://www.nba.com/players)
3. **Target Stat**: The statistical category you want to predict for (MIN, FGM, FGA, FG3M, FG3A, FTM, FTA, OREB, DREB, REB, AST, TOV, STL, BLK, PTS, PLUS_MINUS).
4. **Money Line**: The betting line (e.g., 25.5).

### **Through GUI**
1. **Start the server** in the `backend` folder. From the root project directory, run:

   - **For Linux/macOS/Windows**:
     ```bash
     fastapi dev backend/main.py
     ```
   - **For Windows**:
     ```bash
     fastapi dev backend\main.py
     ```
     
2. **Compile the Java file** in the `GUI/MoneyLinePredictor/src` folder. From the root project directory, run:

   - **For Linux/macOS/Windows**:
     ```bash
     javac GUI/MoneyLinePredictor/src/PredictorApp.java
     ```
   - **For Windows**:
     ```bash
     javac GUI\MoneyLinePredictor\src\PredictorApp.java
     ```

3. **Run the Java GUI application** by executing the following command from the root project directory:
   
   - **For Linux/macOS**:
     ```bash
     java -cp GUI/MoneyLinePredictor/src PredictorApp
     ```
   - **For Windows**:
     ```bash
     java -cp GUI\MoneyLinePredictor\src PredictorApp
     ```

5. In the **name box**: enter the first name and last name of the player.
6. In the **target stat box**: enter the desired statistic.
7. In the **money line box**: enter the betting line.
8. Click the **predict button** to see the prediction.
   

## Troubleshooting
If you encounter any issues, here are a few things to check:
1. Ensure that you've activated the virtual environment and installed the dependencies using `pip install -r requirements.txt`
2. Ensure you're using Python 3.x. Verify the version by running `python --version`
3. Make sure you have Java 21.x+ installed for the GUI. If there are issues compiling and running the `.java` file, try reinstalling Java.

## Acknowledgments

This project uses the following libraries and resources:

- **scikit-learn**: A machine learning library for Python. (https://scikit-learn.org/)
- **pandas**: A data manipulation and analysis library. (https://pandas.pydata.org/)
- **nba_api**: Python API client for accessing NBA.com data. (https://github.com/swar/nba_api/)
