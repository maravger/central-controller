#!/usr/bin/env bash

# Trap ctrl-c (INT) and call cleanup()
trap cleanup INT

function cleanup() {
    echo
	echo "** Terminating Controller and cleaning up..."

	# Stop redis server
	echo "Step 1/2: Shutting redis server down..."
	redis-cli shutdown

	# Kill celery worker
	echo "Step 2/2: Killing celery worker..."
	pkill -9 -f 'celery worker'
}

# Perform migrations
echo "Step 1/4: Performing migrations..."
python manage.py migrate
echo

# Start redis server in background
echo "Step 2/4: Starting redis server in the background..."
redis-server --daemonize yes
echo

# Start celery in background
echo "Step 3/4: Starting celery in the background..."
celery -A central_controller worker -l warning -B --detach
echo

# Finally, initiate controller (TODO: GET OUT OF DEV MODE)
echo "Step 4/4: Starting server in dev mode..."
python manage.py runserver 0.0.0.0:8002