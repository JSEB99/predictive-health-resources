from google.cloud import bigquery, bigquery_storage
from google.oauth2.credentials import Credentials
import streamlit as st
import pandas as pd


@st.cache_resource
def connect():
    """
    Connection to BigQuery

    :return: client and storage client
    :rtype: tuple(client, bqstorage_client)
    """
    credentials = Credentials.from_authorized_user_info(
        st.secrets['gcp_credentials'])
    client = bigquery.Client(
        credentials=credentials,
        project=st.secrets['gcp_credentials']['quota_project_id'])
    bqstorage_client = bigquery_storage.BigQueryReadClient(
        credentials=credentials)
    return client, bqstorage_client


@st.cache_data
def query_data(query: str) -> pd.DataFrame:
    """
    Query data from BigQuery in form of DataFrame

    :param query: query in BigQuery
    :type query: str

    :return: table of your data
    :rtype: pandas DataFrame
    """
    client, bqstorage_client = connect()
    place_job = client.query(query)

    return place_job.to_dataframe(bqstorage_client=bqstorage_client)
