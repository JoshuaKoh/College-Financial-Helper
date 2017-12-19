import pandas as pd
from dataStore import filterForDropout
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn import preprocessing
from sklearn.decomposition import PCA
import time
import matplotlib.pyplot as plt
import dataOperations
from flask import Flask
import logging

log = logging.getLogger(__name__)
app = Flask(__name__)


def run(df):
    lb = LabelEncoder()

    df = filterForDropout(df)

    # TODO NORMALIZE DATA WITHIN NUMERICAL SCALE
    for column in df.columns:
        if df[column].dtype == type(object):
            df[column] = lb.fit_transform(df[column])
    log.info("Fit transform completed.")

    vals = df.values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(vals)
    df = pd.DataFrame(x_scaled)
    log.info("Value scaling completed.")

    # TODO DIMENSIONALITY REDUCTION

    # TODO UNSUPERVISED: K-MEANS
    vals = range(0, len(df.columns.tolist()))
    X = df.values[:, vals]   # predictors

    MAX_CLUSTERS = 6
    ITERATIONS = 1
    for iteration in range(0, ITERATIONS):
        # Prepare visualization
        fig = plt.figure()
        title = 'Vanilla K-Means clusters on filtered data'
        fig.suptitle(title)

        start_time = time.time()
        for cluster in range(2, MAX_CLUSTERS + 1):
            # Train the model
            model = KMeans(n_clusters=cluster, random_state=100)
            model_data = model.fit_transform(X)
            reduced_data = PCA(n_components=2).fit_transform(model_data)

            # Plot the decision boundary. For that, we will assign a color to each
            x_min, x_max = min(reduced_data[x][0] for x in range(len(reduced_data))) - .1, max(reduced_data[x][0] for x in range(len(reduced_data))) + .1
            y_min, y_max = min(reduced_data[x][1] for x in range(len(reduced_data))) - .1, max(reduced_data[x][1] for x in range(len(reduced_data))) + .1

            # Plot graphs based on k value and cluster identity
            labels = model.labels_
            colors = ['red', 'blue', 'yellow', 'green', 'purple', 'orange', 'black']
            for i in range(labels.min(), labels.max() + 1):
                x = []
                for index in range(len(reduced_data)):
                    if labels[index] == i:
                        x.append(reduced_data[index][0])
                y = []
                for index in range(len(reduced_data)):
                    if labels[index] == i:
                        y.append(reduced_data[index][1])
                plt.subplot(3, 2, cluster-1)
                plt.xlim(x_min, x_max)
                plt.ylim(y_min, y_max)
                plt.xticks(())
                plt.yticks(())
                subtitle = "k=%s" % cluster
                plt.title(subtitle, fontsize='small')
                plt.plot(x, y, 'k.', color=colors[i], markersize=4)

            end_time = time.time()
            runtime = end_time - start_time
            app.logger.info("Model took %.3f" % runtime)

        log.info("Ready to show model.")
        plt.savefig("static/dropout.png")
        log.info("Showed model.")

    # TODO CLUSTER ANALYSIS

    # TODO GROUP RETENTION INTO DISCRETE BUCKETS

    # TODO DECISION TREE PREDICTOR

    # TODO NEURAL NET PREDICTOR

    # TODO SVM PREDICTOR

    return True
