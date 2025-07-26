# FinWiseAI
FinWise AI enables users to experience hedge fund–style decision-making with complete transparency, empowering them to learn, experiment, and invest smarter.

## Running the ML Service

### 1. Install dependencies
Ensure you have Python 3.13 or compatible and install requirements:
```bash
pip install -r ml_service/requirements.txt
```

> **Note:** Upgrade `pymongo` to the latest version to avoid compatibility issues with Python 3.13:
```bash
pip install --upgrade pymongo
```

### 2. Train the LSTM model
```bash
python3 -m ml_service.trainers.train_lstm
```

### 3. Start the ML API
```bash
python3 -m uvicorn ml_service.api.main:app --reload --port 9091
```


### 4. Test the API
- **Ping endpoint:** [http://localhost:9091/ml/ping](http://localhost:9091/ml/ping)  
- **Test DB connection:** [http://localhost:9091/ml/test-db](http://localhost:9091/ml/test-db)


## Running the Application

Follow these steps to run the backend, ML service, and frontend components together.

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd finwiseai
```

### 2. Start services with Docker
Build and start MongoDB, Redis, backend, and ML service containers:
```bash
docker compose up --build
```

### 3. Train the ML model (if not already trained)
```bash
python3 -m ml_service.trainers.train_lstm
```

### 4. Start the ML API locally (optional if not using Docker for ML service)
```bash
python3 -m uvicorn ml_service.api.main:app --reload --port 9091
```

### 5. Start the frontend (React with Vite)
Navigate to the frontend directory and run the development server:
```bash
cd frontend/app
npm install   # only first time
npm run dev
```

The frontend will be available at [http://localhost:5173](http://localhost:5173).

### 6. Access the backend API
Backend runs at [http://localhost:9090](http://localhost:9090). Use Postman or the frontend app to test endpoints.

### 7. API Testing
- **Register user:** `POST /api/register`
- **Login:** `POST /api/login`
- **Get user info:** `GET /api/user` (with `Authorization: Bearer <token>` header)
- **ML prediction:** `GET /ml/predict` from ML API
