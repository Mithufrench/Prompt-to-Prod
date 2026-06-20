# Push Changes to GitHub - Step by Step Guide

## Quick Push (Recommended)

### Windows Users
Simply double-click: `PUSH_TO_GITHUB_RAILWAY_FIX.bat`

This will automatically:
1. ✅ Stage all modified files
2. ✅ Create a commit with detailed message
3. ✅ Push to GitHub main branch

---

## Manual Push Steps

### 1. Verify Git Configuration
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 2. Check Git Status
```bash
git status
```

You should see changes in:
- `Dockerfile`
- `railway.toml`
- `Procfile` (new file)
- `ai-agent/requirements.txt`
- `ai-agent/config.py`
- `ai-agent/main.py`
- `.env`
- `.env.example`

### 3. Stage All Changes
```bash
git add Dockerfile railway.toml Procfile ai-agent/requirements.txt ai-agent/config.py ai-agent/main.py .env .env.example
```

Or stage everything:
```bash
git add .
```

### 4. Commit Changes
```bash
git commit -m "fix: Railway PORT compatibility and Groq LLM integration

- Update Dockerfile to use dynamic PORT variable for healthchecks
- Add railway.toml with startCommand and env config
- Create Procfile for explicit Railway process type
- Add groq package to requirements.txt
- Update config.py to use GROQ_API_KEY
- Update main.py to use Groq API instead of hardcoded responses
- Update .env and .env.example with Groq credentials

Fixes: Deployment failures caused by healthcheck probing wrong port
This ensures healthchecks probe the correct dynamically-assigned PORT"
```

### 5. Push to GitHub
```bash
git push origin main
```

If you get authentication errors, see **Troubleshooting** section below.

---

## Verify Push Succeeded

After pushing, verify on GitHub:

1. Go to https://github.com/Mithufrench/Prompt-to-Prod
2. Check the commit history - your new commit should be there
3. Verify all 8 files were updated
4. Check Railway dashboard for auto-deployment

---

## What Gets Pushed

### Modified Files (8 total)
| File | Change | Reason |
|------|--------|--------|
| `Dockerfile` | Use `${PORT:-8000}` | Railway compatibility |
| `railway.toml` | Add startCommand + env | Explicit process config |
| `Procfile` | NEW | Railway process declaration |
| `ai-agent/requirements.txt` | Add `groq==0.9.0` | LLM package |
| `ai-agent/config.py` | Use GROQ_API_KEY | Groq credentials |
| `ai-agent/main.py` | Groq API integration | Dynamic LLM responses |
| `.env` | GROQ_API_KEY | Local development |
| `.env.example` | GROQ_API_KEY | Documentation template |

---

## Troubleshooting

### Error: "Git is not recognized"
**Solution:** Install Git from https://git-scm.com/
- Download Git for Windows
- Run installer with default options
- Restart terminal/command prompt

### Error: "fatal: not a git repository"
**Solution:** Initialize git first
```bash
git init
git remote add origin https://github.com/Mithufrench/Prompt-to-Prod.git
git branch -M main
```

### Error: "Permission denied" or "Authentication failed"
**Solutions:**

**Option A: SSH Key (Recommended)**
```bash
# Check if you have SSH configured
ssh -T git@github.com

# If not, generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Add key to GitHub: https://github.com/settings/keys
```

**Option B: Personal Access Token**
1. Go to https://github.com/settings/tokens
2. Create new token (Settings → Developer settings → Personal access tokens)
3. Copy token
4. When pushing, use token as password:
```bash
git push origin main
# Username: your-username
# Password: paste-your-token-here
```

**Option C: Configure Git Credentials Manager**
```bash
git config --global credential.helper manager
git push origin main
# Browser will open for GitHub login
```

### Error: "rejected - non-fast-forward"
This means remote has changes. Pull first:
```bash
git pull origin main
git push origin main
```

### Error: "nothing to commit"
All files might already be staged. Check:
```bash
git status
```

If you see "nothing to commit", all changes are already in repo.

---

## After Successful Push

### 1. Verify on GitHub
Visit: https://github.com/Mithufrench/Prompt-to-Prod
- Check commit history
- Verify files were updated

### 2. Set Railway Environment Variables
Go to Railway Dashboard → Your Service → Variables:

```
GROQ_API_KEY = your-actual-groq-api-key
MODEL = mixtral-8x7b-32768
LOG_LEVEL = INFO
ENVIRONMENT = production
```

### 3. Trigger Deployment
- **Auto-deploy enabled:** Deployment starts automatically
- **Manual:** Click "Deploy" in Railway dashboard

### 4. Monitor Deployment
Check Railway logs for:
```
✅ "🚀 Starting on port XXXXX" (dynamic port)
✅ "🤖 Using Groq model: mixtral-8x7b-32768"
✅ "✅ Static files mounted at /"
```

### 5. Test the App
Once deployed:
```
curl https://your-railway-app.up.railway.app/health
```

Should return:
```json
{
  "status": "healthy",
  "service": "ai-devops-platform",
  "version": "2.0.0",
  "llm": "groq",
  "model": "mixtral-8x7b-32768"
}
```

---

## Quick Commands Reference

```bash
# Check what changed
git status
git diff

# Stage changes
git add Dockerfile railway.toml Procfile ai-agent/requirements.txt ai-agent/config.py ai-agent/main.py .env .env.example

# Commit
git commit -m "fix: Railway PORT compatibility and Groq LLM integration"

# Push
git push origin main

# View commit history
git log --oneline -5
```

---

## Still Having Issues?

1. **Can't run the .bat file?**
   - Right-click PUSH_TO_GITHUB_RAILWAY_FIX.bat → Run as Administrator

2. **Need to undo a push?**
   ```bash
   git revert HEAD
   git push origin main
   ```

3. **Want to see what will be pushed?**
   ```bash
   git diff --cached
   ```

4. **Check remote URL**
   ```bash
   git remote -v
   # Should show:
   # origin  https://github.com/Mithufrench/Prompt-to-Prod.git (fetch)
   # origin  https://github.com/Mithufrench/Prompt-to-Prod.git (push)
   ```

---

**✅ Ready to push? Run `PUSH_TO_GITHUB_RAILWAY_FIX.bat` or follow the manual steps above.**
