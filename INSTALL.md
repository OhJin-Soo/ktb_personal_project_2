# Installation Guide

## Dependencies

Install all required packages using:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install fastapi uvicorn sqlmodel "passlib[bcrypt]" "bcrypt<5.0.0" python-multipart
```

## Important Notes

- **bcrypt version**: Use bcrypt 4.x (not 5.0.0) for compatibility with passlib
- **Environment**: Make sure you're in the correct conda/virtual environment when running the server

## Running the Server

```bash
cd backend
uvicorn main:app --reload
```

The server will start on `http://localhost:8000`
'http://localhost:8000/static/index.html'

## Troubleshooting

If you see "bcrypt: no backends available":
1. Activate your conda environment: `conda activate env_ai`
2. Install bcrypt: `pip install "bcrypt<5.0.0"`
3. Verify: `python -c "from passlib.context import CryptContext; CryptContext(schemes=['bcrypt'])`

