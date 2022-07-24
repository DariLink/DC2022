import mariadb
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors
from dython.nominal import associations
from scipy.stats import chi2_contingency
from scipy.stats.contingency import association
from scipy.stats import chi2
from scipy.stats import pointbiserialr
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.preprocessing import LabelBinarizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.metrics import roc_curve, precision_recall_curve, auc, make_scorer, recall_score, accuracy_score, precision_score, confusion_matrix

"""
This script processes the analysis for the H3 & H4. The objective is to test whether the price decrease had
negative or positive effect on the sentiment.
Variables:
9 Euro Subject: was 9-euro ticket subject or not, dependent on the time period
Price Gas: average gas price per day as retrieved from https://dev.azure.com/tankerkoenig/_git/tankerkoenig-data?path=/prices/2022/01
Weigheting: 0,67 benzin, 0,33 Diesel Source ->  https://de.statista.com/statistik/daten/studie/4270/umfrage/pkw-bestand-in-deutschland-nach-kraftstoffarten/
Time of day: time of posting in hours
Regio (is regio or RE[0-9] mentioned?), 
holiday (is the post_date weekend or public holiday?)
likes: how many likes has this post?

"""

conn_params= {
    "user" : "user1",
    "password" : "karten",
    "host" : "localhost",
    "database" : "dc"
}


connection= mariadb.connect(**conn_params)
cursor= connection.cursor()

def grid_search_wrapper(refit_score='precision_score'):
    """
    fits a GridSearchCV classifier using refit_score for optimization
    prints classifier performance metrics
    """
    skf = StratifiedKFold(n_splits=10)
    grid_search = GridSearchCV(clf, param_grid, scoring=scorers, refit=refit_score,
                           cv=skf, return_train_score=True, n_jobs=-1)
    grid_search.fit(X_train, y_train)

    # make the predictions
    y_pred = grid_search.predict(X_test)

    print('Best params for {}'.format(refit_score))
    print(grid_search.best_params_)

    # confusion matrix on the test data.
    print('\nConfusion matrix of Random Forest optimized for {} on the test data:'.format(refit_score))
    print(pd.DataFrame(confusion_matrix(y_test, y_pred),
                 columns=['pred_neg', 'pred_pos'], index=['neg', 'pos']))
    return grid_search

def get_p_value(contigency_df):
    stat, p, dof, expected = chi2_contingency(contigency_df)
    prob = 0.99
    critical = chi2.ppf(prob, dof)
    if abs(stat) >= critical:
        print('Dependent (reject H0)')
    else:
        print('Independent (fail to reject H0)')


def get_stats(data, df_gas):
    df_gas.post_date = df_gas.post_date.astype(str)
    data.post_date = data.post_date.astype(str)
    df_all = pd.merge(data, df_gas, how='left', on='post_date')

    # replace empty gas prices with previous value
    df_all['gas_price'] = df_all['gas_price'].fillna(method='ffill')
    df_all.drop(['post_date', 'E10', 'E5', 'Diesel'], axis=1, inplace=True)

    fig, ax = plt.subplots(figsize=(16, 8))
    # custom db colours
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["red", "white"])
    r = associations(df_all, ax=ax, cmap=cmap, filename='heatmap_h4.png')

    observed = pd.crosstab(index=df_all['neun_euro'], columns=df_all['sentiment'])
    # double check the strenght of association
    print(association(observed, method="cramer"))
    # p-values of 9-euro (chi-square)
    get_p_value(observed)

    ## stats for variable frei
    observed = pd.crosstab(index=df_all['frei'], columns=df_all['sentiment'])
    print(association(observed, method="cramer"))
    get_p_value(observed)

    # same for post_hour
    pbc = pointbiserialr(df_all['post_hour'], df_all['sentiment'])
    print(pbc)



data = pd.read_sql("select case when sentiment_final = -1 then 0 else 1 end as sentiment, "
                   "case when likes is null then 0 else likes end as likes, "
                   "case when regio is null then 0 else 1 end as regio"
                   ", date(post_date) as post_date,"
                   " case when post_date between '2019-04-01' and '2019-07-01' then 0 else 1 end as neun_euro, "
                   "hour(post_date) as post_hour, "
                   "case when weekday(post_date) in (5,6) or cast(post_date as date)  "
                   "in (select holiday from holidays) then 1 else 0 end as frei "
                   "from text_all t "
                   "where (post_date between '2019-04-01' and '2019-07-01') "
                   "or (post_date between '2022-04-01' and '2022-07-01') and sentiment_final <> 0 "
                   ";", connection, index_col=None)

# add gas prices
df_gas = pd.read_csv('output_gas_prices.csv')
df_gas['gas_price'] = df_gas['Diesel']*0.33 + df_gas['E10']*0.67
df_gas.rename(columns={"Date": "post_date"}, inplace=True)
#get_stats(data, df_gas)

# use for binary classification the variables frei, 9-euro and post_hour
X = data[['neun_euro','post_hour','frei', 'likes' , 'regio']]
y = data['sentiment']
X_train, X_test, y_train, y_test = train_test_split(X, y , test_size=0.25, random_state=0, stratify=y)

ss_train = StandardScaler()
X_train = ss_train.fit_transform(X_train)

ss_test = StandardScaler()
X_test = ss_test.fit_transform(X_test)

clf = RandomForestClassifier(n_estimators=100,
                       max_depth=3,
                       random_state=0,
                       max_features=3,
                       min_samples_split=19)

clf.fit(X_train, y_train)
predictions = clf.predict(X_test)

print(accuracy_score(predictions, y_test))
print(precision_score(predictions, y_test))
print(recall_score(predictions, y_test))

"""
param_grid = {
    'min_samples_split': [3, 5, 10],
    'n_estimators' : [100, 300],
    'max_depth': [3, 5, 15, 25],
    'max_features': [3, 5, 10, 20]
}

scorers = {
    'precision_score': make_scorer(precision_score),
    'recall_score': make_scorer(recall_score),
    'accuracy_score': make_scorer(accuracy_score)
}

grid_search_clf = grid_search_wrapper(refit_score='precision_score')
results = pd.DataFrame(grid_search_clf.cv_results_)
results = results.sort_values(by='mean_test_precision_score', ascending=False)
results[['mean_test_precision_score', 'mean_test_recall_score', 'mean_test_accuracy_score',
         'param_max_depth', 'param_max_features', 'param_min_samples_split',
         'param_n_estimators']].head()


# test different models
models = {}
models['Logistic Regression'] = LogisticRegression(random_state=0, solver='lbfgs')
models['Support Vector Machines'] = LinearSVC()
models['Decision Trees'] = DecisionTreeClassifier()
models['Random Forest'] = RandomForestClassifier(n_estimators=100, max_depth=2, random_state=0)
models['Naive Bayes'] = GaussianNB()

accuracy, precision, recall = {}, {}, {}
for key in models.keys():
    # Fit the classifier
    models[key].fit(X_train, y_train)

    # Make predictions
    predictions = models[key].predict(X_test)


    # Calculate metrics
    accuracy[key] = accuracy_score(predictions, y_test)
    precision[key] = precision_score(predictions, y_test)
    recall[key] = recall_score(predictions, y_test)


df_model = pd.DataFrame(index=models.keys(), columns=['Accuracy', 'Precision', 'Recall'])
df_model['Accuracy'] = accuracy.values()
df_model['Precision'] = precision.values()
df_model['Recall'] = recall.values()

print(df_model)
"""

