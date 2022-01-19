FROM apache/airflow:2.2.3

USER root
RUN groupadd --gid 999 docker \
   && usermod -aG docker airflow
RUN chown -R airflow:docker /var/run/
USER airflow

COPY ./requirements/airflow_requirements.txt /requirements/airflow_requirements.txt
RUN pip install -r /requirements/airflow_requirements.txt
# Fix airflow warning
RUN pip uninstall  --yes azure-storage \
    && pip install -U azure-storage-blob apache-airflow-providers-microsoft-azure==1.1.0
ENTRYPOINT ["/entrypoint"]
