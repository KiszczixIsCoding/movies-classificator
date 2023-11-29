from sklearn.preprocessing import MinMaxScaler


def normalize_column(data_from_df):
    column_data = data_from_df.values.reshape(-1, 1)
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(column_data)
    return normalized_data
