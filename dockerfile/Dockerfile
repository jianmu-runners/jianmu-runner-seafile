FROM python:3.8-slim-buster
ADD python/seafile_uploads.py /usr/local/bin/
RUN pip install requests
ENTRYPOINT ["python"]
CMD ["/usr/local/bin/seafile_uploads.py"]