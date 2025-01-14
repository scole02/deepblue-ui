# deepblue-ui

Steps to Run App
```
# With python 3.10 virtual environment
python -m pip install -r requirements.txt

# Install other dependencies for spatial database
# Spatialite and GDAL installs may differ for MACOS
sudo apt-get install -y libgdal-dev gdal-bin python3-gdal
sudo apt-get install -y libsqlite3-mod-spatialite

# Make migrations for database (Optional)
python manage.py makemigrations
python manage.py migrate

# Run Dev server
python manage.py runserver

# Navigate to 127.0.0.1:8000/map
```

