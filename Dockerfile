FROM python
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
ADD App /app/App
ADD tests /app/tests
RUN pip freeze
RUN ls /app -a -R