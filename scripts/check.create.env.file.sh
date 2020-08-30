#!/bin/bash

echo "PORT $REDIS_PORT"


if [ ! -f "./.env" ]; then
    echo "" > .env
else
    rm .env
    echo "" > .env
fi

if [ -z "$REDIS_SERVER" ]; then
    echo "Missing ENV var REDIS_SERVER..."
fi

if [ -z "$REDIS_PORT" ]; then
    echo "Missing ENV var REDIS_PORT..."
    exit 130
fi

if [ -z "$REDIS_USER" ]; then
    echo "Missing ENV var REDIS_USER..."
    exit 130
fi

if [ -z "$REDIS_PASSWORD" ]; then
    echo "Missing ENV var REDIS_PASSWORD..."
    exit 130
fi

if [ -z "$REDIS_HOST" ]; then
    echo "Missing ENV var REDIS_HOST..."
    exit 130
fi

if [ -z "$RABBITMQ_SERVER" ]; then
    echo "Missing ENV var RABBITMQ_SERVER..."
    exit 130
fi

if [ -z "$RABBITMQ_USER" ]; then
    echo "Missing ENV var RABBITMQ_USER..."
    exit 130
fi

if [ -z "$RABBITMQ_PASS" ]; then
    echo "Missing ENV var RABBITMQ_PASS..."
    exit 130
fi

if [ -z "$RABBITMQ_VHOST" ]; then
    echo "Missing ENV var RABBITMQ_VHOST..."
    exit 130
fi

if [ -z "$IS_DOCKER" ]; then
    echo "Missing ENV var IS_DOCKER..."
    exit 130
fi

if [ -z "$FP_DB_HOST" ]; then
    echo "Missing ENV var FP_DB_HOST..."
    exit 130
fi

if [ -z "$FP_DB_PORT" ]; then
    echo "Missing ENV var FP_DB_PORT..."
    exit 130
fi

if [ -z "$FP_DB_NAME" ]; then
    echo "Missing ENV var FP_DB_NAME..."
    exit 130
fi

if [ -z "$FP_DB_USER" ]; then
    echo "Missing ENV var FP_DB_USER..."
    exit 130
fi

if [ -z "$FP_DB_PASSWORD" ]; then
    echo "Missing ENV var FP_DB_PASSWORD..."
    exit 130
fi


echo "REDIS_SERVER=$REDIS_SERVER" >> ./.env
echo "REDIS_PORT=$REDIS_PORT" >> ./.env
echo "REDIS_USER=$REDIS_USER" >> ./.env
echo "REDIS_PASSWORD=$REDIS_PASSWORD" >> ./.env
echo "REDIS_HOST=$REDIS_HOST" >> ./.env
echo "RABBITMQ_SERVER=$RABBITMQ_SERVER" >> ./.env
echo "RABBITMQ_USER=$RABBITMQ_USER" >> ./.env
echo "RABBITMQ_PASS=$RABBITMQ_PASS" >> ./.env
echo "RABBITMQ_VHOST=$RABBITMQ_VHOST" >> ./.env
echo " " >> ./.env
echo "IS_DOCKER=$IS_DOCKER" >> ./.env
echo " " >> ./.env
echo "FP_DB_HOST=$FP_DB_HOST" >> ./.env
echo "FP_DB_PORT=$FP_DB_PORT" >> ./.env
echo "FP_DB_NAME=$FP_DB_NAME" >> ./.env
echo "FP_DB_USER=$FP_DB_USER" >> ./.env
echo "FP_DB_PASSWORD=$FP_DB_PASSWORD" >> ./.env
