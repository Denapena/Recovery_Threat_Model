# Recovery Threat Model

Project where I created a logistic regression model to analyze recoveries and the likelihood of them ending in a shot or a goal. This project was based on Liverpool in the 2017/2018 season and I wanted to create a model to rate players and based on that model suggest two signings for Liverpool. Since Liverpool is a team oriented on high and intense press which leads to many recoveries I choose those recoveries as a starting point. Together with the code, there is the presentation which summarises my suggestions, and two reports. The technical report looks into the technical background of the model and code, analyzing the accuracy and significance of the p-values. In contrast, the Scout report is a two-page report describing the results in more detail than the presentation. Data used is free Wyscout data for the 2017/2018 season of the top 5 leagues (Premier League, La Liga, Serie A, Bundesliga, and Ligue 1).

## Main tools used

* Pandas, Matplotlib and Numpy
* Logistic Regression Model (statsmodels)

## Getting started

* To run this program, you need Jupyter Notebook, Visual Studio Code, and an intermediate knowledge of Python
* Event data needs to be provided for the code to work which can be downloaded from the link down below (Wyscout Data, Minutes_played)
* The main file is Recovery_Threat_Model.ipynb which has a step-by-step explanation of the coding process, it takes approximately 5-10 minutes for the whole Notebook to load and process all code
* File possession_chains.json is saved to speed up the process of using the main file by not having to isolate possession chains on each restart of the file
* File OtherLeagueRecoveries.py is used to generate numbers for the other 4 leagues which are saved in files sorted_goals.json and sorted_shots.json and used in the main file (it takes around 40 minutes to process). It follows the same structure as the main file, just the data is different.

## Author

Contributors names and contact info:
Denis Dervishi, denisdervishi@gmail.com

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [Soccermatics](https://soccermatics.readthedocs.io/en/latest/)
* [Stack Overflow](https://stackoverflow.com/)
* [Wyscout Glossary](https://dataglossary.wyscout.com/)
* [Wyscout API](https://apidocs.wyscout.com/)
* [Wyscout Data](https://figshare.com/collections/Soccer_match_event_dataset/4415000/2)
* [Minutes_played](https://github.com/soccermatics/Soccermatics/tree/main/course/lessons/minutes_played)
