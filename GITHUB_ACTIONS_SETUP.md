# GitHub Actions Setup - Quick Guide

This guide will help you deploy your EEX CoT workflow to GitHub Actions in 10 minutes.

## What You'll Get

- ✅ Automated weekly reports (every Tuesday)
- ✅ Reports accessible via web browser
- ✅ No server to maintain
- ✅ Free hosting (GitHub Pages)
- ✅ Historical data tracked in Git

**Example URL**: `https://YOUR_USERNAME.github.io/eex-cot/cot_report_20260123.html`

---

## Step 1: Push to GitHub (5 minutes)

### Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `eex-cot` (or your choice)
3. Description: "EEX Commitment of Traders Analysis"
4. Choose **Public** or **Private**
5. **Don't** initialize with README (we already have one)
6. Click "Create repository"

### Push Your Code

Open terminal in your project directory and run:

```bash
# Navigate to project directory
cd c:\Users\Henning\claudecode\eex-cot

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit - EEX CoT workflow"

# Add GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/eex-cot.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Done!** Your code is now on GitHub.

---

## Step 2: Enable GitHub Actions (1 minute)

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. You should see "Weekly EEX CoT Report" workflow
4. If prompted to enable workflows, click **"I understand my workflows, go ahead and enable them"**

**That's it!** The workflow is now active.

---

## Step 3: Enable GitHub Pages (2 minutes)

1. In your repository, go to **Settings** → **Pages** (left sidebar)
2. Under "Source":
   - Branch: Select `gh-pages`
   - Folder: Select `/ (root)`
3. Click **Save**

You'll see a message: "Your site is ready to be published at https://YOUR_USERNAME.github.io/eex-cot/"

**Note**: The `gh-pages` branch will be created automatically after the first workflow run.

---

## Step 4: Run the Workflow (1 minute)

Don't wait until Tuesday! Run it now to test:

1. Go to **Actions** tab
2. Click "Weekly EEX CoT Report" (left sidebar)
3. Click **"Run workflow"** button (right side)
4. Click the green **"Run workflow"** button in the dropdown
5. Wait 2-3 minutes for completion

### Monitor Progress

- Click on the running workflow to see live logs
- Green checkmark = Success
- Red X = Failed (check logs for errors)

---

## Step 5: Access Your Reports (1 minute)

After the workflow completes:

### Option 1: GitHub Pages URL
```
https://YOUR_USERNAME.github.io/eex-cot/
```

This will show an index page with all available reports.

### Option 2: Direct Report URL
```
https://YOUR_USERNAME.github.io/eex-cot/cot_report_20260123.html
```

Replace the date with the actual report date.

### Option 3: View in Repository
1. Go to your repository
2. Click the `gh-pages` branch (branch selector, top left)
3. Click on any HTML file to download/view

---

## Verification Checklist

After setup, verify everything works:

- [ ] Code pushed to GitHub successfully
- [ ] Actions tab shows "Weekly EEX CoT Report" workflow
- [ ] Workflow runs successfully (green checkmark)
- [ ] `gh-pages` branch created
- [ ] GitHub Pages enabled and shows site URL
- [ ] Can access reports via browser
- [ ] Index page lists available reports

---

## Troubleshooting

### Workflow Fails

**Check the error logs:**
1. Actions tab → Click failed workflow
2. Click on the job name
3. Expand failed step to see error

**Common issues:**

**"ModuleNotFoundError"**
- Solution: Check `requirements.txt` includes all dependencies
- Verify `pip install -r requirements.txt` step runs

**"Permission denied"**
- Solution: Check repository settings → Actions → General → Workflow permissions
- Select "Read and write permissions"
- Save

**"gh-pages branch not found"**
- This is normal on first run
- The workflow creates it automatically
- If it persists, create manually: Settings → Branches → New branch: `gh-pages`

### GitHub Pages Not Working

**Site not found (404)**
- Wait 1-2 minutes after first workflow run
- Check Settings → Pages to confirm it's enabled
- Verify `gh-pages` branch exists

**Reports not showing**
- Check `gh-pages` branch contains HTML files
- Verify workflow completed successfully
- Check browser console for errors (F12)

### Workflow Doesn't Run on Schedule

**First run hasn't happened yet**
- GitHub Actions may delay first scheduled run
- Manually trigger once to "wake it up"

**Workflow disabled**
- Check Actions tab for any warnings
- Repository with no activity for 60 days disables workflows
- Re-enable: Actions → Workflow → "Enable workflow"

---

## Customization

### Change Schedule

Edit `.github/workflows/weekly_cot_report.yml`:

```yaml
schedule:
  - cron: '0 10 * * 2'  # Tuesday 10:00 AM UTC
```

**Cron syntax**: `minute hour day-of-month month day-of-week`

**Examples:**
- `0 9 * * 2` - Tuesday 9 AM UTC
- `30 14 * * 2` - Tuesday 2:30 PM UTC
- `0 8 * * 1-5` - Weekdays 8 AM UTC

**Timezone converter**: https://www.worldtimebuddy.com/

### Add More Contracts

Edit `.github/workflows/weekly_cot_report.yml`:

```yaml
- name: Run EEX CoT Workflow
  run: |
    python eex_workflow.py DEBM DEPM F7BM ATBM --weeks 13
```

### Change Number of Weeks

```yaml
- name: Run EEX CoT Workflow
  run: |
    python eex_workflow.py DEBM DEPM --weeks 26
```

### Make Repository Private

1. Settings → General (scroll down)
2. Danger Zone → Change visibility → Make private
3. Confirm

**Note**: GitHub Pages on free tier:
- Public repos: Pages are always public
- Private repos: Pages public (or private with GitHub Pro)

---

## Advanced: Private Reports with Authentication

If you need truly private reports:

### Option 1: Use Private Repo + GitHub Pro
- Upgrade to GitHub Pro ($4/month)
- Private repository + private GitHub Pages

### Option 2: Deploy to Password-Protected Site
- Use Cloudflare Pages with Cloudflare Access
- Use Netlify with password protection
- Deploy to private VPS (see DEPLOYMENT_GUIDE.md)

### Option 3: Email Reports
Add email notification to workflow:

```yaml
- name: Send Report Email
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: Weekly EEX CoT Report
    to: your-email@example.com
    from: GitHub Actions
    attachments: reports/cot_report_*.html
```

---

## Monitoring

### Email Notifications

**Get notified on workflow completion:**

1. Go to repository → Watch → Custom
2. Check "Actions" notifications
3. You'll receive emails on workflow runs

**Or add to workflow** (see Advanced section above)

### Workflow Status Badge

Add to your README.md:

```markdown
![Workflow Status](https://github.com/YOUR_USERNAME/eex-cot/actions/workflows/weekly_cot_report.yml/badge.svg)
```

Shows green badge if workflow is passing.

---

## Costs

**GitHub Free Tier:**
- 2000 Actions minutes/month
- This workflow uses ~3 minutes/run
- = ~660 runs/month available
- You only need 4-5 runs/month (weekly)

**Result**: Completely free! 🎉

**If you exceed limits:**
- Public repos: Always free for Actions
- Private repos: $0.008 per minute after free tier

---

## Next Steps

After successful setup:

1. **Test it works**: Run manually and verify reports appear
2. **Schedule confirmation**: Wait for Tuesday to confirm scheduled run
3. **Bookmark URL**: Save your GitHub Pages URL
4. **Share with team**: Send report URL to colleagues
5. **Monitor weekly**: Check reports are generated each week

---

## Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Review [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for alternatives
3. Check [README.md](README.md) for project documentation
4. View GitHub Actions logs for specific errors

---

## Summary

✅ Push code to GitHub
✅ Enable GitHub Actions
✅ Enable GitHub Pages
✅ Run workflow manually
✅ Access reports via browser

**Time investment**: 10 minutes setup
**Result**: Automatic weekly reports forever!

---

**Congratulations!** 🎉 You now have a fully automated, web-accessible CoT reporting system!
