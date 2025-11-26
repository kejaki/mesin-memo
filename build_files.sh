# build_files.sh
echo "Building project..."

# Create and activate virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
python3.12 -m pip install -r requirements.txt

# Create output directory
mkdir -p staticfiles_build

# Collect static files
python3.12 manage.py collectstatic --noinput --clear

echo "Build finished successfully"
