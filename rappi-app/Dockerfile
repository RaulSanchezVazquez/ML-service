FROM continuumio/miniconda3

MAINTAINER Luis Raul Sanchez Vazquez "luisraulsv@gmail.com"

COPY . /app

WORKDIR /app

RUN conda create --name rappi python=3.7.3

SHELL ["conda", "run", "-n", "rappi", "/bin/bash", "-c"]

RUN conda activate rappi
RUN conda install numpy pandas -y
RUN conda install -c conda-forge xgboost==1.2.0 -y
RUN pip install -r requirements.txt

EXPOSE 5000

ENV RAPPI_DB_PORT 5001
ENV RAPPI_DB_HOST '0.0.0.0'
ENV RAPPI_DB_USER 'root'
ENV RAPPI_DB_PASSW 'rappi-secret'
ENV RAPPI_DB_NAME 'rappi'

ENTRYPOINT ["conda", "run", "-n", "rappi", "python", "app.py", "2>server.log"]
