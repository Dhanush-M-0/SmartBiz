# SmartBiz Production Deployment Guide

This guide covers deploying SmartBiz to various cloud platforms and production environments.

## Quick Start: Local Production Testing

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up production environment
cp .env.production .env.prod
# Edit .env.prod with your actual values

# 3. Run with Gunicorn (4 workers)
FLASK_ENV=production gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:app

# 4. Test health endpoints
curl http://localhost:5000/health
curl http://localhost:5000/ready
```

## Using Docker

### Local Development with Docker Compose

```bash
# Build and run with automatic reload
docker-compose up --build

# The app will be accessible at http://localhost:5000
# Changes to files will trigger automatic reload
```

### Production Docker Image

```bash
# Build the image
docker build -t smartbiz:latest .

# Run in production
docker run \
  -d \
  --name smartbiz \
  -p 5000:5000 \
  --env-file .env.production \
  --restart unless-stopped \
  smartbiz:latest

# Check logs
docker logs -f smartbiz

# Stop the container
docker stop smartbiz
docker rm smartbiz
```

## Cloud Platform Deployment

### Heroku

1. **Install Heroku CLI**
   ```bash
   brew tap heroku/brew && brew install heroku
   heroku login
   ```

2. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

3. **Set environment variables**
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set FLASK_SECRET_KEY="your-very-long-random-key-here"
   heroku config:set SUPABASE_URL="your-supabase-url"
   heroku config:set SUPABASE_KEY="your-supabase-key"
   heroku config:set EMAIL_SENDER="your-email@gmail.com"
   heroku config:set EMAIL_PASSWORD="your-app-password"
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **View logs**
   ```bash
   heroku logs --tail
   ```

### Railway.app

1. **Connect your GitHub repository**
   - Go to [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub"
   - Select your repository

2. **Add environment variables**
   - In Railway dashboard, go to Variables
   - Add all variables from `.env.production`

3. **Configure the start command**
   - Service settings → "Start Command"
   - Set to: `gunicorn --bind 0.0.0.0:$PORT wsgi:app`

4. **Deploy**
   - Push to GitHub, Railway automatically deploys

### Render.com

1. **Connect your GitHub repository**
   - Go to [render.com](https://render.com)
   - Click "New Web Service"
   - Connect GitHub repository

2. **Configure deployment**
   - Name: `smartbiz`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:5000 wsgi:app`

3. **Add environment variables**
   - In Render dashboard, go to Environment
   - Add all variables from `.env.production`

4. **Deploy**
   - Render automatically deploys on git push

### AWS (Elastic Beanstalk)

1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize and create environment**
   ```bash
   eb init -p python-3.11 smartbiz --region us-east-1
   eb create smartbiz-env
   ```

3. **Set environment variables**
   ```bash
   eb setenv FLASK_ENV=production FLASK_SECRET_KEY="..." SUPABASE_URL="..." ...
   ```

4. **Deploy**
   ```bash
   eb deploy
   ```

5. **View logs**
   ```bash
   eb logs
   ```

### DigitalOcean App Platform

1. **Connect your GitHub repository**
   - Go to DigitalOcean App Platform
   - Click "Create App"
   - Select GitHub repository

2. **Configure as Python service**
   - Name: `smartbiz`
   - Source: GitHub
   - Build command: `pip install -r requirements.txt`
   - Run command: `gunicorn --bind 0.0.0.0:8080 wsgi:app`

3. **Add environment variables**
   - Add all variables from `.env.production`

4. **Deploy**
   - DigitalOcean handles deployment

## Environment Variables Reference

### Required
- `SUPABASE_URL` - Your Supabase project URL (from dashboard)
- `SUPABASE_KEY` - Your Supabase public/anon key (from API settings)
- `FLASK_SECRET_KEY` - A long random string (minimum 32 characters, use: `python -c "import secrets; print(secrets.token_urlsafe(32))"`)

### Required for Email Notifications
- `EMAIL_SENDER` - Gmail address (or another SMTP email)
- `EMAIL_PASSWORD` - App-specific password (not regular password)

### Optional
- `FLASK_ENV` - Set to `production` (default)
- `FLASK_DEBUG` - Set to `False` in production (default)
- `REPORTS_OUTPUT_DIR` - Directory for generated reports (default: `reports_output`)
- `DATABASE_TIMEZONE` - Timezone for dates (default: `UTC`)

## Health Checks

SmartBiz provides two health check endpoints:

```bash
# Liveness probe (just check if app is running)
curl http://your-app-url/health
# Returns: {"status": "healthy"} (200 OK)

# Readiness probe (check if database is accessible)
curl http://your-app-url/ready
# Returns: {"status": "ready"} (200 OK)
# Returns: {"status": "not_ready", "error": "..."} (503 Service Unavailable) if DB is down
```

## Logging

In production, logs are:
- Written to stdout (captured by Docker/platform)
- Written to `logs/smartbiz.log` (with rotation)
- Formatted as JSON for easy parsing

View logs:
```bash
# Local
tail -f logs/smartbiz.log

# Docker
docker logs -f smartbiz

# Platform-specific
heroku logs --tail
railway logs
```

## Monitoring & Alerts

### Recommended: Sentry (Error Tracking)

1. Create account at [sentry.io](https://sentry.io)
2. Create project for Python/Flask
3. Add to requirements.txt: `sentry-sdk[flask]==1.40.0`
4. Set `SENTRY_DSN` environment variable

### Recommended: Uptime Monitoring

Use services like:
- [UptimeRobot](https://uptimerobot.com)
- [StatusPage.io](https://www.statuspage.io)
- [Datadog](https://www.datadoghq.com)

Configure to check: `https://your-app-url/ready`

## Troubleshooting

### App crashes on startup

**Error: "Invalid URL"**
- Check `SUPABASE_URL` is correctly set
- Check `SUPABASE_KEY` is correctly set

**Error: "SUPABASE_URL and SUPABASE_KEY must be set"**
- Ensure environment variables are loaded
- Check `.env` or platform-specific env config

### Database connection issues

**Error: "Connection refused"**
- Check Supabase project is running
- Check `SUPABASE_URL` matches your project
- Test connection: `curl https://your-supabase-url`

### Email notifications not working

**Error: "Failed to send email"**
- Check `EMAIL_SENDER` and `EMAIL_PASSWORD` are correct
- For Gmail: enable "Less secure apps" or use App Password
- Check firewall allows SMTP on port 587

### High memory usage

- Increase worker count: `--workers 2` (start with low worker count)
- Add memory limit: `--max-requests 1000` to recycle workers

### Slow responses

- Check database query logs: `SELECT * FROM pg_stat_statements;`
- Monitor CPU/memory in platform dashboard
- Scale to multiple dynos/instances if needed

## Security Checklist

Before deploying to production:

- [ ] Set `FLASK_ENV=production`
- [ ] Set `FLASK_DEBUG=False`
- [ ] Generate and set a strong `FLASK_SECRET_KEY`
- [ ] Use HTTPS/SSL (enabled by default in production config)
- [ ] Restrict CORS origins (update in `app/__init__.py`)
- [ ] Set email credentials securely (use platform's secret manager)
- [ ] Enable monitoring and error tracking
- [ ] Set up regular backups (Supabase has built-in backups)
- [ ] Enable rate limiting if needed
- [ ] Test security headers: `curl -I https://your-app-url`

## Useful Commands

```bash
# Generate a secure SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Test app locally with production config
export FLASK_ENV=production
gunicorn wsgi:app

# Build and test Docker image locally
docker build -t smartbiz:test .
docker run -p 5000:5000 --env-file .env.production smartbiz:test

# Generate requirements with versions
pip freeze > requirements.txt
```

## Support

For issues:
1. Check application logs
2. Check health endpoints (`/health`, `/ready`)
3. Verify environment variables are set
4. Check Supabase dashboard for database issues
5. Review cloud platform documentation
