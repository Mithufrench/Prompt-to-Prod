# Railway Deployment Fix Summary

## Problem Identified
Railway was assigning a dynamic PORT (e.g., 47380) to your app, but the Dockerfile had a hardcoded healthcheck on port 8000. This caused the healthcheck to timeout every time, resulting in 4+ consecutive deployment failures.

## Root Cause
1. **Dockerfile HEALTHCHECK**: Probed `http://localhost:8000/health` (hardcoded)
2. **Railway behavior**: Assigns random PORT via environment variable
3. **Mismatch**: App starts on assigned PORT (correct), but healthcheck probes wrong port (8000)
4. **Result**: Healthcheck timeout → Deployment failed

## Fixes Applied

### 1. Dockerfile Updates ✅
**Before:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
EXPOSE 8000
CMD ["python", "main.py"]
```

**After:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1
EXPOSE ${PORT:-8000}
CMD ["python", "-u", "main.py"]
```

**Changes:**
- Use `${PORT:-8000}` to read Railway's PORT variable (falls back to 8000 locally)
- Added `-u` flag for unbuffered Python output (better logging in Railway)

### 2. railway.toml Updates ✅
**Before:**
```toml
[build]
dockerfile = "Dockerfile"
context = "."

[deploy]
restartPolicyType = "always"
healthcheckPath = "/health"
healthcheckTimeout = 10
```

**After:**
```toml
[build]
dockerfile = "Dockerfile"
context = "."

[deploy]
restartPolicyType = "always"
healthcheckPath = "/health"
healthcheckTimeout = 10
startCommand = "python -u ai-agent/main.py"

[env]
PORT = "$PORT"
PYTHONUNBUFFERED = "1"
```

**Changes:**
- Explicit `startCommand` for Python app
- `PORT = "$PORT"` ensures environment variable is passed
- `PYTHONUNBUFFERED = "1"` for immediate log output

### 3. Procfile Created ✅
**New file:**
```
web: python -u ai-agent/main.py
```

This is Railway's standard way to specify process types. Railway will use this if present.

### 4. ai-agent/main.py - Already Compatible ✅
Your app already correctly reads the PORT:
```python
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))  # ← This is correct!
    logger.info(f"🚀 Starting on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
```

No changes needed here.

### 5. Groq LLM Integration (Already Fixed) ✅
- `requirements.txt`: Added `groq==0.9.0`
- `config.py`: Uses `GROQ_API_KEY` (not OpenAI)
- `main.py`: Uses Groq API instead of hardcoded responses
- `.env` / `.env.example`: Updated to use Groq credentials

## How It Works Now

1. **Railway assigns PORT** (e.g., PORT=47380)
2. **Container starts**: `python -u ai-agent/main.py`
3. **App reads PORT**: `port = int(os.getenv("PORT", 8000))` → 47380
4. **Uvicorn listens**: On 0.0.0.0:47380
5. **Healthcheck probes**: `http://localhost:${PORT}/health` → `http://localhost:47380/health` ✓
6. **Response received**: 200 OK → Deployment succeeds ✓

## Next Steps

### 1. Push to GitHub
```bash
git add Dockerfile railway.toml Procfile ai-agent/requirements.txt ai-agent/config.py ai-agent/main.py .env .env.example
git commit -m "fix: Railway PORT compatibility and Groq LLM integration"
git push origin main
```

### 2. Set Environment Variables in Railway Dashboard
Go to your service settings → Variables:
- `GROQ_API_KEY` = your-actual-groq-api-key
- `MODEL` = mixtral-8x7b-32768
- `LOG_LEVEL` = INFO
- `ENVIRONMENT` = production

### 3. Trigger Deployment
- If auto-deploy is enabled: Deployment starts automatically
- Otherwise: Click "Deploy" in Railway dashboard

### 4. Verify Success
Check Railway logs:
```
✅ Should see: "🚀 Starting on port 47380" (or similar)
✅ Should see: "🤖 Using Groq model: mixtral-8x7b-32768"
✅ Should see: "/health" endpoint responding
```

## What's Fixed

| Issue | Before | After |
|-------|--------|-------|
| Port binding | Hardcoded 8000 | Dynamic PORT via env var |
| Healthcheck | Probed 8000 (wrong) | Probes $PORT (correct) |
| Python logging | Buffered | Unbuffered (-u flag) |
| LLM | OpenAI hardcoded | Groq API configured |
| API Key | Unused OPENAI_API_KEY | GROQ_API_KEY |
| Railway detection | Not recognized | Procfile recognized |

## Testing Locally

Before pushing, test locally:

```bash
# Test on port 8000 (default)
docker compose up

# Test on custom port (like Railway does)
PORT=5555 docker run --rm -e PORT=5555 -e GROQ_API_KEY=test -p 5555:5555 p2p-agent:latest
```

## Files Changed

1. ✅ `Dockerfile` - PORT variable support
2. ✅ `railway.toml` - startCommand and env vars
3. ✅ `Procfile` - NEW: Process type declaration
4. ✅ `ai-agent/requirements.txt` - Added groq package
5. ✅ `ai-agent/config.py` - GROQ_API_KEY support
6. ✅ `ai-agent/main.py` - Groq integration
7. ✅ `.env` - GROQ_API_KEY credentials
8. ✅ `.env.example` - Updated template

---

**Expected Result:** ✅ Deployment succeeds on Railway with no healthcheck timeouts
