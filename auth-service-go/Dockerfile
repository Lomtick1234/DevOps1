FROM golang:1.22-alpine AS builder

WORKDIR /app

COPY go.mod go.sum* ./
RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux go build -o /auth-service ./cmd/auth-service/main.go

FROM alpine:latest

RUN apk --no-cache add ca-certificates tzdata

WORKDIR /app

COPY --from=builder /auth-service .
COPY config.yml ./config.yml

EXPOSE 8081

ENTRYPOINT ["./auth-service"]
