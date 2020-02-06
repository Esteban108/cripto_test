FROM python:3.7

EXPOSE 5000


COPY requirements.txt /tmp/
RUN pip install \
  --no-cache-dir \
  -r /tmp/requirements.txt

RUN useradd appuser
WORKDIR /home/appuser
RUN chown appuser:appuser /home/appuser
USER appuser

COPY . ./back_end

ENTRYPOINT [ "uvicorn" ]
CMD [ "back_end.api.main:app", "--port","8000","--host","0.0.0.0"]
