FROM alpine:3.17.1

ENV APPDIR /opt/rpilocator/

RUN apk add --update --no-cache python3; \
    mkdir -p $APPDIR; \
    adduser -D mort; \
    chown mort:mort $APPDIR;

USER mort
WORKDIR $APPDIR

COPY ./requirements.txt ./run.py $APPDIR
RUN python -m ensurepip; \
    python -m pip install --no-cache --upgrade pip; \
    python -m pip install --no-cache -r requirements.txt

ENTRYPOINT ["python", "run.py"]
CMD ["-t"]

