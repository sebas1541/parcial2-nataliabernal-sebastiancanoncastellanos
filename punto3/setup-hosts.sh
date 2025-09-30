#!/bin/bash
set -e

API_DOMAIN="api.localhost"
OPS_DOMAIN="ops.localhost"

echo "🔧 Setting up /etc/hosts entries for Traefik assignment..."

# Verificar si ya están en /etc/hosts
if grep -q "$API_DOMAIN" /etc/hosts && grep -q "$OPS_DOMAIN" /etc/hosts; then
    echo "/etc/hosts entries already exist!"
else
    echo "Agregando entradas en /etc/hosts..."
    sudo sh -c "echo '127.0.0.1 $API_DOMAIN' >> /etc/hosts"
    sudo sh -c "echo '127.0.0.1 $OPS_DOMAIN' >> /etc/hosts"
    echo "✔ Entradas añadidas!"
fi

echo
echo "# local domains:"
grep -E "api.localhost|ops.localhost" /etc/hosts || true

echo
echo "Your local domains are ready:"
echo " • API: http://$API_DOMAIN"
echo " • Traefik Dashboard: http://$OPS_DOMAIN/dashboard/"
echo "   (username: admin, password: secret)"
echo
echo "👉 Now run: docker-compose up --build --scale flask_api=2 -d"

