# Deployment Guide - Running on a Server

This guide covers different options for running the EEX CoT workflow automatically on a server and accessing results via the internet.

## Quick Comparison

| Option | Cost | Difficulty | Access | Best For |
|--------|------|------------|--------|----------|
| **GitHub Actions + Pages** | Free | Easy | Web browser | Most users |
| **Cloud VM** | $5-10/mo | Medium | SSH + Web | Full control |
| **Serverless** | Free-$5/mo | Easy | Web/API | Simple automation |
| **Home Server** | One-time | Medium | Dynamic DNS | Privacy/control |

---

## Option 1: GitHub Actions + GitHub Pages (RECOMMENDED) ⭐

**Perfect for**: Automated weekly reports accessible via web browser, no server management

### Features
- ✅ Runs every Tuesday automatically
- ✅ HTML reports accessible via URL (e.g., `https://yourusername.github.io/eex-cot/cot_report_20260123.html`)
- ✅ Historical data stored in Git
- ✅ Can be private or public
- ✅ Zero server maintenance

### Setup Instructions

#### 1. Create GitHub Repository
```bash
cd c:\Users\Henning\claudecode\eex-cot
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/eex-cot.git
git push -u origin main
```

#### 2. Enable GitHub Pages
1. Go to your repository on GitHub
2. Settings → Pages
3. Source: Deploy from a branch
4. Branch: `gh-pages` → `/root`
5. Click Save

#### 3. Configure GitHub Actions
The workflow file is already created at `.github/workflows/weekly_cot_report.yml`

It will:
- Run every Tuesday at 10:00 AM UTC
- Download latest reports
- Generate analysis and charts
- Create HTML report
- Commit results to the repository
- Deploy to GitHub Pages

#### 4. Manual Run (Optional)
- Go to Actions tab in your repo
- Select "Weekly EEX CoT Report"
- Click "Run workflow"

#### 5. Access Your Reports
After the first run, access reports at:
```
https://YOUR_USERNAME.github.io/eex-cot/cot_report_YYYYMMDD.html
```

### Customization

**Change schedule** (edit `.github/workflows/weekly_cot_report.yml`):
```yaml
schedule:
  - cron: '0 10 * * 2'  # Tuesday 10:00 AM UTC
  # Adjust: 'minute hour day month weekday'
```

**Add more contracts**:
```yaml
- name: Run EEX CoT Workflow
  run: |
    python eex_workflow.py DEBM DEPM F7BM ATBM --weeks 13
```

**Timezone conversion**:
- UTC 10:00 → CEST 12:00 (summer)
- UTC 10:00 → CET 11:00 (winter)
- Use https://crontab.guru/ to help with cron syntax

### Cost
- **Free** for public repositories
- **Free** for private repos (2000 minutes/month on free plan)
- This workflow uses ~2-3 minutes per run = ~50 runs/month max

---

## Option 2: Cloud VPS (DigitalOcean, AWS, etc.)

**Perfect for**: Full control, private deployment, additional customization

### Recommended Providers

**DigitalOcean Droplet**
- Cost: $6/month (basic)
- 1 vCPU, 1GB RAM (sufficient)
- Easy setup
- Good documentation

**AWS Lightsail**
- Cost: $3.50-5/month
- Similar to DigitalOcean
- Free tier: 750 hours/month for 3 months

**Hetzner Cloud**
- Cost: €4.15/month (~$4.50)
- Better specs than competitors
- European data centers

### Setup Steps

#### 1. Create Server
- Choose Ubuntu 22.04 LTS
- SSH key authentication
- Note the IP address

#### 2. Initial Server Setup
```bash
# SSH into server
ssh root@YOUR_SERVER_IP

# Update system
apt update && apt upgrade -y

# Install Python and dependencies
apt install python3 python3-pip git -y

# Create non-root user
adduser eexcot
usermod -aG sudo eexcot
su - eexcot
```

#### 3. Deploy Application
```bash
# Clone repository
cd ~
git clone https://github.com/YOUR_USERNAME/eex-cot.git
cd eex-cot

# Install Python packages
pip3 install -r requirements.txt

# Test workflow
python3 eex_workflow.py DEBM DEPM
```

#### 4. Setup Cron Job
```bash
# Edit crontab
crontab -e

# Add this line (runs every Tuesday at 9:00 AM)
0 9 * * 2 cd /home/eexcot/eex-cot && /usr/bin/python3 eex_workflow.py DEBM DEPM >> /home/eexcot/logs/cot_$(date +\%Y\%m\%d).log 2>&1
```

#### 5. Setup Web Server (Optional - for accessing reports via browser)

**Option A: Simple Python HTTP Server**
```bash
# Install screen to keep it running
sudo apt install screen -y

# Start HTTP server
screen -S webserver
cd ~/eex-cot/reports
python3 -m http.server 8080

# Detach: Ctrl+A, then D
# Reattach: screen -r webserver
```

Access: `http://YOUR_SERVER_IP:8080/cot_report_YYYYMMDD.html`

**Option B: Nginx (More professional)**
```bash
# Install nginx
sudo apt install nginx -y

# Configure nginx
sudo nano /etc/nginx/sites-available/eex-cot

# Add this configuration:
```

```nginx
server {
    listen 80;
    server_name YOUR_SERVER_IP;

    root /home/eexcot/eex-cot/reports;
    index cot_report_latest.html;

    location / {
        try_files $uri $uri/ =404;
        autoindex on;
    }

    location /plots {
        alias /home/eexcot/eex-cot/plots;
        autoindex on;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/eex-cot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

Access: `http://YOUR_SERVER_IP/`

#### 6. Add Domain (Optional)
- Point your domain DNS to server IP
- Update nginx configuration with domain name
- Add SSL with Let's Encrypt:
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### Security Considerations
```bash
# Setup firewall
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable

# Disable root SSH login
sudo nano /etc/ssh/sshd_config
# Set: PermitRootLogin no
sudo systemctl restart sshd
```

---

## Option 3: Serverless / Cloud Functions

**Perfect for**: Minimal cost, automatic scaling, no server management

### Railway.app (Easiest)

1. **Sign up**: https://railway.app/
2. **Connect GitHub**: Link your repository
3. **Deploy**: Click "New Project" → "Deploy from GitHub"
4. **Add Cron**: Use Railway's cron service
5. **Cost**: $5/month (includes 500 execution hours)

### Render.com

1. **Sign up**: https://render.com/
2. **Create Cron Job**:
   - New → Cron Job
   - Connect GitHub repo
   - Schedule: `0 9 * * 2` (Tuesday 9 AM)
   - Command: `python eex_workflow.py DEBM DEPM`
3. **Static Site** (for reports):
   - New → Static Site
   - Build: `echo "Reports"`
   - Publish: `reports`
4. **Cost**: Free tier available

### AWS Lambda + S3

More complex but scalable:
- Lambda function runs workflow
- Results stored in S3 bucket
- S3 static website for reports
- CloudWatch Events for scheduling
- Cost: ~$1-2/month

---

## Option 4: Home Server / Raspberry Pi

**Perfect for**: Privacy, one-time cost, learning

### Hardware Options

**Raspberry Pi 4**
- Cost: ~$50-75 one-time
- Low power consumption
- Sufficient for this task

**Old PC / Mini PC**
- Cost: Free (if you have one)
- More powerful
- Higher power consumption

### Setup Steps

1. **Install OS**: Ubuntu Server or Raspberry Pi OS
2. **Setup Dynamic DNS**: Use No-IP, DuckDNS, or DynDNS
3. **Port Forwarding**: Forward port 80/443 on router
4. **Install Application**: Same as VPS setup above
5. **Setup Cron**: Same as VPS

### Pros/Cons
✅ One-time cost
✅ Full control
✅ Private
❌ Requires home internet
❌ Need to manage hardware
❌ Static IP or dynamic DNS needed

---

## Option 5: Hybrid Approach

**Best of both worlds**: Run on home server, backup to cloud

### Setup
1. Run workflow on home server (free)
2. Upload results to GitHub (backup)
3. GitHub Pages serves reports (public access)

```bash
# Add to cron script
cd ~/eex-cot
python3 eex_workflow.py DEBM DEPM
git add data/ plots/ reports/
git commit -m "Weekly report $(date +%Y-%m-%d)"
git push origin main
```

---

## Recommended Setup by Use Case

### Personal Use, Low Maintenance
→ **GitHub Actions + Pages**
- Free, automated, web accessible
- No server to manage

### Professional / Team Use
→ **Cloud VPS with Nginx**
- Custom domain (e.g., cot.yourcompany.com)
- Private access control
- Full customization

### Learning / Experimentation
→ **Raspberry Pi at Home**
- Learn server administration
- One-time cost
- Full control

### Budget Conscious
→ **GitHub Actions** (Free)
- OR **Hetzner Cloud** ($4.50/mo)
- OR **Raspberry Pi** ($50 one-time)

### Maximum Privacy
→ **Home Server + VPN**
- Data never leaves your network
- Access via VPN only

---

## Monitoring & Alerts

### Email Notifications (for any server setup)

**Using SendGrid/MailGun**:
```python
# Add to eex_workflow.py
import smtplib
from email.mime.text import MIMEText

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'reports@yourdomain.com'
    msg['To'] = 'you@email.com'

    with smtplib.SMTP('smtp.sendgrid.net', 587) as server:
        server.starttls()
        server.login('apikey', 'YOUR_API_KEY')
        server.send_message(msg)

# Call after workflow completion
send_email('EEX CoT Report Ready', f'Report generated: {report_path}')
```

**Using GitHub Actions** (built-in):
```yaml
- name: Send notification on failure
  if: failure()
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: EEX CoT Report Failed
    to: you@email.com
    from: GitHub Actions
    body: Workflow failed. Check logs.
```

---

## Cost Summary

| Solution | Setup Time | Monthly Cost | Best For |
|----------|-----------|--------------|----------|
| GitHub Actions | 30 min | $0 | Most users |
| DigitalOcean | 1-2 hours | $6 | Professional use |
| Hetzner | 1-2 hours | $4.50 | Budget-conscious |
| Railway.app | 15 min | $5 | Simplicity |
| Raspberry Pi | 2-3 hours | $0* | DIY/Learning |
| AWS Lambda | 2-3 hours | $1-2 | Technical users |

*Electricity cost: ~$2-5/year

---

## My Recommendation

**For you**: Start with **GitHub Actions + GitHub Pages**

**Why**:
1. ✅ Free and reliable
2. ✅ Setup in 30 minutes
3. ✅ Access reports from anywhere via URL
4. ✅ Automatic weekly updates
5. ✅ No server maintenance
6. ✅ Git history of all data
7. ✅ Can make private if needed

**Next Steps**:
1. Push code to GitHub (see instructions above)
2. Enable GitHub Pages
3. Wait for Tuesday or trigger manually
4. Access your reports at the GitHub Pages URL

**Later, if needed**:
- Upgrade to VPS for custom domain
- Add authentication for private access
- Deploy additional services

---

## Questions?

Common questions addressed in specific guides:
- [README.md](README.md) - Main documentation
- [QUICKSTART.md](QUICKSTART.md) - Local setup
- [HTML_REPORT_GUIDE.md](HTML_REPORT_GUIDE.md) - Report details

---

**Ready to deploy?** Start with the GitHub Actions approach above! 🚀
