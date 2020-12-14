FROM tiangolo/uwsgi-nginx-flask:python3.8
COPY . .
RUN pip install -r ./requirements.txt
WORKDIR ./lib
CMD ["python", "main.py"]