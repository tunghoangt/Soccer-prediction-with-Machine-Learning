
# Predicting English Premier League match results with Machine Learning
#### Tony Hoang and Thomas Duffy


# Introduction <a name="introduction"></a>
The English Premier League is the most-watched professional soccer league on the planet, with an estimated audience figure of 12 million people per game. In comparison, its closest rival, Spain’s La Liga draws an average of just over 2 million fans per game.

In EPL, there are 20 teams that contest for the first place. The winner is the team that has the most points at the end of the season, with 3 points are awarded for a win, one point for a draw and none for a defeat. The bottom three teams are relegated and replaced by other teams from lower leagues who perform better. Each team plays every other team twice, once at home and once away. Thus, there are a total of 380 games per season. A season runs from August to May of the following year. 

In this project, we want to predict the results of soccer matches using machine learning algorithms. First, it is crucial to choose features that seem to be significant and analyze their influence on match outcomes. From literature reference and our own intuition, we create a set of 17 features that includes individual match statistics like `Score`, `Corners`, `Shots on target`, `Posessions`, etc., and season long statistics for teams such as `Expenditures`, `Income`, `Departure` and `Arrival`, which reflect their investment and squad change every year. `Score` (goal) is an obvious choice as they determine which team wins, and is used to create our target variable. As for other features, they are indicators for how well a team play and can translate to a high probability of goals being scored. Based on the data that we have, we also develop a new feature `Form`, which is a measure of the “streakiness” of a team. Each feature is available for both teams, home and away.

The predicting features will be fed as inputs to Machine Learning classifier algorithms such as `Logistic Regression` (LR), `K-Nearest Neighbors` (KNN), `Gradient Boosting` (GB), `Support Vector Machine` (SVM) and `Random Forest` (RF). The prediction is in one of three classes for each game, with respective to the home team: win, draw, or loss. To improve model performance, we implement various techniques such as `Sequential Backward Selection` (SBS) for features selection, or `Principal Component Analysis` (PCA) for feature extractions, and cross-validation for model evaluation & selection.  

After our model analysis and selection, we take a step further and simulate the last season (`2018`) using data from the previous 9 seasons. Instead of just predicting the outcome each game for the home team with a classifier, we build a model to generated synthetic match statistics, and use those to calculate expected goal for both teams per match. Our prediction of the final team standing has a good accuracy when comparing to the final official result, which can be found [here](https://www.skysports.com/premier-league-table/2017). We correctly pick the league winner, and strongly believe that investment money has a significant influence in the league outcome of a team.

**References**
* [Premier league official website (2007-2018](https://www.premierleague.com/results?co=1&se=23&cl=-1)
* [Team investment spending data](https://www.transfermarkt.us/premier-league/einnahmenausgaben/wettbewerb/GB1)
* [Kaggle EPL data (1993 - 2018)](https://www.kaggle.com/thefc17/epl-results-19932018/kernels)
* [Official EPL standing in 2018](https://www.skysports.com/premier-league-table/2017)
* [Albina Yezus - Predicting the outcome of English Premier League games using machine learning](https://pdfs.semanticscholar.org/7d1f/8ff04a87b29eddc8eb84300d98d7dd3ffe30.pdf)
* [Ben Ulmer & Matthew Fernandez - Predicting Soccer Match Results in the English
Premier League](http://cs229.stanford.edu/proj2014/Ben%20Ulmer,%20Matt%20Fernandez,%20Predicting%20Soccer%20Results%20in%20the%20English%20Premier%20League.pdf)
* [Sourabh Swain & Shriya Mishra - Data Science Approach to Predict the Outcome of a Football Match](https://www.ijcseonline.org/pdf_paper_view.php?paper_id=1857&20-IJCSE-02970.pdf)

Please see our presentation [here](https://github.com/tunghoangt/MLproject/blob/master/models/Presentation.ipynb)
