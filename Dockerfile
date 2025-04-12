FROM golang:1.22 as builder

ENV GOTOOLCHAIN=auto

RUN git clone https://github.com/go-gost/gost.git /gost
WORKDIR /gost
RUN go build -o /usr/bin/gost ./cmd/gost

FROM python:3.11-slim

RUN apt update && apt install -y curl && pip install requests pyyaml

COPY --from=builder /usr/bin/gost /usr/bin/gost
COPY entrypoint.sh /entrypoint.sh
COPY generate_gost_config.py /generate_gost_config.py

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
