FROM python:3.12-slim


RUN apt-get update && apt-get install -y --no-install-recommends \
    texlive-latex-base \
    texlive-fonts-recommended \
    texlive-lang-cyrillic \
    texlive-latex-extra \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app


RUN pip install latex-generator-itmo-kulyaskin


COPY hw_2/generate_example.py /app/hw_2/


RUN mkdir -p /app/hw_2/artifacts


CMD ["python", "hw_2/generate_example.py"]


VOLUME ["/app/hw_2/artifacts"] 