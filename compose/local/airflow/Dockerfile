FROM apache/airflow:2.0.1

COPY ./requirements/airflow_requirements.txt /requirements/airflow_requirements.txt
RUN pip install -r /requirements/airflow_requirements.txt
# Fix airflow warning
RUN pip uninstall  --yes azure-storage \
    && pip install -U azure-storage-blob apache-airflow-providers-microsoft-azure==1.1.0
ENTRYPOINT ["/entrypoint"]
