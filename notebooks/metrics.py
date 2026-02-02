#!/usr/bin/env python

import json
import numpy as np
from scipy.stats import shapiro, skew, kurtosis, pearsonr


def accuracy_to_error(accuracy_list):
    """
    Convert a list of percent accuracy values to percent error.

    Parameters:
    accuracy_list (list of float): A list containing accuracy values (as fractions, not percentages).

    Returns:
    list of float: A list containing the corresponding error values.
    """
    return [1 - acc for acc in accuracy_list]

def mean(data):
    """
    Calculate the mean of a list of numbers.

    Parameters:
    data (list of float): A list of numerical values.

    Returns:
    float: The mean of the input list.
    """
    return np.mean(data)

def range(data):
    """
    Calculate the range of a list of numbers.

    Parameters:
    data (list of float): A list of numerical values.

    Returns:
    float: The range of the input list.
    """
    return np.max(data) - np.min(data)


def standard_deviation(data):
    """
    Calculate the standard deviation of a list of numbers.

    Parameters:
    data (list of float): A list of numerical values.

    Returns:
    float: The standard deviation of the input list.
    """
    return np.std(data)


def shapiro_p(data):
    """
    Calculate the p-value of the Shapiro-Wilk test for normality, return 0 if the data is not normal.

    Parameters:
    data (list of float): A list of numerical values.

    Returns:
    int: 1 if the data is normal, 0 otherwise.
    """
    if shapiro(data)[1] < 0.05:
        return 0
    else:
        return 1

def shapiro_test(data):
    """
    Calculate the statistic of the Shapiro-Wilk test for normality.

    Parameters:
    data (list of float): A list of numerical values.

    Returns:
    float: The value of the statistic of the Shapiro-Wilk test.
    """
    return shapiro(data)

def skewness(data):
    """
    Calculate the skewness of a list of numbers.

    Parameters:
    data (list of float): A list of numerical values.

    Returns:
    float: The skewness of the input list.
    """
    return skew(data)

def absolute_value_skew(data):
    """
    Calculate the absolute value skewness of a list of numbers.

    Parameters:
    data (list of float): A list of numerical values.

    Returns:
    float: The absolute value skewness of the input list.
    """
    return abs(skew(data))

def correlation(list_a, list_b):
    """
    Calculate the Pearson correlation coefficient between two lists of numbers.

    Parameters:
    list_a (list of float): A list of numerical values.
    list_b (list of float): A list of numerical values.

    Returns:
    tuple: A tuple containing the Pearson correlation coefficient and the p-value.
    """

    return pearsonr(list_a, list_b)

def upper_fence_outliers(data):
    """
    Count the number of outliers above the upper fence.

    Parameters:
    data (list of float): A list of numerical values.

    Returns:
    int: Number of outliers.
    """
    if isinstance(data, list):  # Convert lists to NumPy arrays
        data = np.array(data)

    # Calculate the quartiles
    q_1 = np.quantile(data, 0.25)
    q_3 = np.quantile(data, 0.75)

    iqr = q_3 - q_1
    lower_bound = q_1 - 1.5 * iqr
    upper_bound = q_3 + 1.5 * iqr

    lower_outliers = np.sum(data < lower_bound)  # Sum boolean mask
    upper_outliers = np.sum(data > upper_bound)

    return upper_outliers


def lower_fence_outliers(data):
    """
    Count the number of outliers below the lower fence.

    Parameters:
    data (list of float): A list of numerical values.

    Returns:
    int: Number of outliers.
    """
    if isinstance(data, list):  # Convert lists to NumPy arrays
        data = np.array(data)

    # Calculate the quartiles
    q_1 = np.quantile(data, 0.25)
    q_3 = np.quantile(data, 0.75)

    iqr = q_3 - q_1
    lower_bound = q_1 - 1.5 * iqr
    upper_bound = q_3 + 1.5 * iqr

    lower_outliers = np.sum(data < lower_bound)  # Sum boolean mask
    upper_outliers = np.sum(data > upper_bound)

    return lower_outliers

def all_outliers(data):
    """
    Count the number of outliers list of numbers.

    Parameters:
    data (list of float): A list of numerical values.

    Returns:
    int: Number of outliers.
    """
    return upper_fence_outliers(data) + lower_fence_outliers(data)

def parameters(model, dataset=None, horizon=None):
    """
    Get the parameters for a specific model.

    Parameters:
    model (str): The name of the model, image classification and time series models.
    dataset (str): The dataset name, required for time series, optional for image classification.
    horizon (str): The horizon, required for time series, optional for image classification.
    
    Returns:
    float: The parameters for the specified model.
    """

    if dataset is None and horizon is None:
        image_classification_model_parameters = json.load(open("image_classification_model_parameters.json", "r")) 

        if "ResNet" in model:
            parameters = image_classification_model_parameters["ResNet"][model[6:]]
        elif "ViT" in model:
            parameters = image_classification_model_parameters["ViT"][model[3:]]
    else:
        time_series_model_parameters = json.load(open("time_series_model_parameters.json", "r"))

        parameters = time_series_model_parameters[model][dataset][horizon]

    return parameters

def safe_round(value, precision):
    """
    Safely round a value to a specified precision, handling edge cases.

    Parameters:
    value (float): The value to round.
    precision (int): The number of decimal places to round to.
    
    Returns:
    float: The rounded value, or scientific notation if the value is very small.
    """

    rounded = round(value, precision)

    if rounded == 0 and value != 0:
        return f"{value:.{2}e}"
    
    return rounded