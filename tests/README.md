# Test Suite

## Running Tests

### Backend Tests
```powershell
# Run all backend tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_auth.py -v

# Run with coverage
python -m pytest tests/ --cov=. --cov-report=html
```

### Frontend Tests
```powershell
cd frontend
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage
```

## Test Files

### Backend
- `tests/test_auth.py` - Authentication endpoints tests
- `tests/test_contracts.py` - Contract generation tests
- `tests/test_retrieval.py` - Knowledge retrieval tests

### Frontend
- `frontend/src/contexts/__tests__/AuthContext.test.tsx` - Auth context tests
- `frontend/src/__tests__/App.test.tsx` - App component tests

## Test Coverage Goals
- Backend: 70%+ coverage
- Frontend: 60%+ coverage

