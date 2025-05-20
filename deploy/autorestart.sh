#!/bin/bash
while true; do
    echo "🔁 Démarrage de l'application..."
    docker-compose up --build
    echo "💥 L'application a crashé. Redémarrage dans 5 secondes..."
    sleep 5
done