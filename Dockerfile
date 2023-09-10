FROM python:3.11.5-slim as base
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONFAULTHANDLER=1


FROM base as build
RUN  pip install --no-cache-dir pipenv
WORKDIR /opt 
RUN --mount=type=bind,source=./Pipfile,target=/opt/Pipfile \
    --mount=type=bind,source=./Pipfile.lock,target=/opt/Pipfile.lock \
    PIPENV_VENV_IN_PROJECT=1 pipenv sync &&\
    find . -type d -name __pycache__  -prune -exec rm -rf {} \;

FROM base
COPY --from=build /opt/.venv /opt/.venv
ENV PATH="/opt/.venv/bin:$PATH"
RUN useradd --system --uid 999 container
WORKDIR /opt
RUN ls -al /opt
COPY ./src/ /opt/
RUN ls -al /opt
#RUN find . -type d -name __pycache__  -prune -exec rm -rf {} \;
USER container
ENTRYPOINT ["python", "-B", "main.py"]
CMD ["/inventory.yml"]


