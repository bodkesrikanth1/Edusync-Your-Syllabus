# PlanetScale Database Setup - Complete Steps

## 📋 What to Select for Your Project

Based on your **EdusyncYourSyllabus** application, here are the recommended selections:

---

## ✅ RECOMMENDED CONFIGURATION

| Setting | Selection | Reason |
|---------|-----------|--------|
| **Database Name** | `edusync` | Matches your project |
| **Region** | `us-east-1` (N. Virginia) | Good for North America |
| **Database Engine** | **Vitess (MySQL)** | ✅ Your code uses MySQL |
| **Cluster Config** | **Single node** | ✅ Cheaper, good for learning |
| **Storage** | **Amazon EBS** | ✅ Cheaper option |
| **Cluster Size** | **PS-5 ($15/mo)** | ✅ Perfect for your needs |

---

## 🚀 COMPLETE STEP-BY-STEP SETUP

### STEP 1: Database Name
```
Field: Database name
Input: edusync
✓ Valid: lowercase, alphanumeric (matches PlanetScale rules)
```
**Screenshot location**: Top of the form

---

### STEP 2: Organization
```
Field: Organization
Selection: bodkesrikanth1 (you, the owner)
```
**This is pre-filled**, just verify it's correct

---

### STEP 3: Region Selection
```
Field: Region
Select: us-east-1 (N. Virginia)
✓ Good latency for most users
✓ Standard choice
```
**Click the region dropdown** if you want to change it later

---

### STEP 4: Database Engine (IMPORTANT!)
```
Field: Database engine
Options:
  - Postgres (PostgreSQL)
  - Vitess (MySQL) ← SELECT THIS ONE ✅

Reason: Your code uses MySQL, so Vitess is perfect
Vitess is MySQL at hyperscale - fully compatible
```

**Click on "Vitess" button**

---

### STEP 5: Cluster Configuration
```
Field: Cluster configuration
Options:
  - Primary + multi-replica (99.99% SLA) - $$$
  - Single node ← SELECT THIS ONE ✅

Reason: 
  ✓ Cheaper ($15/mo vs $30+)
  ✓ Good enough for learning/testing
  ✓ Can upgrade later if needed
```

**Click on "Single node"**

---

### STEP 6: Storage Options
```
Field: Storage options
Options:
  - Amazon EBS ← SELECT THIS ONE ✅
  - PlanetScale Metal ($$$$)

Reason:
  ✓ Much cheaper
  ✓ Good for your database size
  ✓ Sufficient for development
```

**Click on "Amazon Elastic Block Storage"**

---

### STEP 7: Cluster Size (Architecture)
```
Field: Choose architecture
Options:
  - aarch64 (ARM64) ← SELECT THIS ONE ✅
  - x86-64

Reason:
  ✓ Cheaper
  ✓ Better price-to-performance
  ✓ Works perfectly with your code
```

**Click on "aarch64" tab**

---

### STEP 8: Cluster Size (Plan) - MOST IMPORTANT!
```
Field: Select plan (on aarch64 tab)
Options:
  - PS-5: $15/mo, 512 MB RAM ← SELECT THIS ONE ✅
  - PS-10: $30/mo, 1 GB RAM
  - PS-20: $50/mo, 2 GB RAM
  - ... (larger options not needed)

WHY PS-5?
✓ $15/month (cheapest paid)
✓ 512 MB RAM is enough for your database
✓ Can upgrade anytime if needed
✓ Can scale automatically with autoscaling storage
✓ Perfect for testing and small production use
```

**Click on the PS-5 option**

---

## 📊 YOUR FINAL SELECTIONS

```
Database Name:     edusync
Organization:      bodkesrikanth1
Region:            us-east-1 (N. Virginia)
Database Engine:   Vitess (MySQL) ✅
Cluster Config:    Single node ✅
Storage Type:      Amazon EBS ✅
Architecture:      aarch64 (ARM64) ✅
Plan:              PS-5 ($15/mo) ✅
```

---

## 🎯 CLICK-BY-CLICK WALKTHROUGH

### STEP 1: Enter Database Name
```
1. Look for "Database name" field at the top
2. Clear any existing text
3. Type: edusync
4. ✓ Verify: shows green checkmark (valid name)
```

### STEP 2: Verify Organization
```
1. Look for "Organization" dropdown
2. Should show: bodkesrikanth1
3. If not, click dropdown and select it
```

### STEP 3: Select Region
```
1. Look for "Region" section
2. Current: us-east-1 (N. Virginia) - KEEP THIS
3. If you want different, click dropdown and choose
```

### STEP 4: SELECT VITESS (MySQL) - CRITICAL!
```
1. Look for "Database engine" section
2. See two buttons: "Postgres" and "Vitess"
3. CLICK ON "Vitess" button ← THIS IS IMPORTANT
4. It should highlight/change color (selected)
```

### STEP 5: Select Single Node
```
1. Look for "Cluster configuration" section
2. See two options:
   - Primary + multi-replica
   - Single node
3. CLICK ON "Single node" button
4. It should get highlighted
```

### STEP 6: Select Amazon EBS
```
1. Look for "Storage options" section
2. See two options:
   - Amazon Elastic Block Storage
   - PlanetScale Metal
3. CLICK ON "Amazon Elastic Block Storage"
4. It should get highlighted
```

### STEP 7: Select aarch64
```
1. Look for "Cluster size" section
2. See two tabs: "aarch64" and "x86-64"
3. CLICK ON "aarch64" tab
4. Tab should become active
```

### STEP 8: SELECT PS-5 PLAN
```
1. In the aarch64 section, see pricing cards
2. First card shows: "PS-5 $15/mo"
3. Details: 1/16 vCPU, 512 MB Memory
4. CLICK ON THIS CARD or the "Select" button
5. It should highlight (selected)
```

### STEP 9: CREATE DATABASE
```
1. Scroll to bottom of form
2. Look for blue "Create database" button
3. CLICK IT
4. Wait for creation (takes 2-5 minutes)
```

---

## ⏳ What Happens Next

### After You Click "Create Database"

```
Status: Creating...
├─ Database initialization: 1-2 min
├─ Network setup: 30 sec
├─ SSL certificates: 30 sec
└─ Ready for connection: Total ~3-5 minutes
```

**You'll see:**
1. Loading spinner
2. "Your database is being created..."
3. Progress indicators
4. Success message with connection details

---

## 📝 After Creation - Get Your Credentials

Once your database is created, you'll see a screen with:

```
Connection Details:
├─ Hostname: xxx.ap-west-1.psdb.cloud
├─ Username: xxxxx
├─ Password: xxxxx
├─ Port: 3306
└─ Database Name: edusync
```

**Copy these and add to your .env file:**

```bash
DB_HOST=xxx.ap-west-1.psdb.cloud
DB_USER=xxxxx
DB_PASSWORD=xxxxx
DB_NAME=edusync
DB_TYPE=mysql
```

---

## 🔐 Important: Copy Your Password

⚠️ **The password only shows once!**

```
Steps:
1. See the password field
2. Click "Copy to clipboard" button
3. Paste it in your .env file immediately
4. Save your .env file
5. If you lose it, you can reset in PlanetScale settings
```

---

## ✅ Next Steps After Database Created

### Step 1: Import Your Data
```bash
# Use your backup file
mysql -h YOUR_HOST -u YOUR_USER -p"YOUR_PASSWORD" edusync < edusync_backup.sql

# You'll be prompted for password, press Enter (already in command)
```

### Step 2: Verify Connection
```bash
# Test the connection
mysql -h YOUR_HOST -u YOUR_USER -p"YOUR_PASSWORD" edusync -e "SELECT COUNT(*) FROM users;"

# Should return: 12 (your user count)
```

### Step 3: Update .env File
```
DB_HOST=your-planetscale-host.psdb.cloud
DB_USER=your-username
DB_PASSWORD=your-password
DB_NAME=edusync
```

### Step 4: Test Locally
```bash
# Run your Flask app
python app.py

# Visit http://localhost:5000
# Test: Register, Login, Upload, Parse
```

### Step 5: Deploy to Hugging Face
```bash
# Once tested, push to Hugging Face Spaces with these credentials
git add .
git commit -m "Add PlanetScale database credentials"
git push
```

---

## 💰 PRICING SUMMARY

```
Plan Feature        | PS-5 ($15/mo) | Notes
─────────────────────────────────────────────
vCPU               | 1/16          | Plenty for your needs
Memory             | 512 MB        | More than enough
Storage            | Autoscaling   | Grows with your data
Nodes              | 1 Primary     | Single node (simple)
Backups            | Included      | Automatic daily
Support            | Community     | Good enough
Monthly Cost       | $15           | Affordable

Alternative Pricing:
├─ Free (if available): $0/mo → Check if they have free tier
├─ PS-5 (current): $15/mo
├─ PS-10 (upgrade): $30/mo
└─ Higher: $50+/mo
```

---

## 🎯 WHY THESE SELECTIONS?

```
✅ Vitess (not Postgres)
   Because your code uses MySQL syntax
   Vitess is MySQL-compatible at hyperscale

✅ Single Node (not Primary + Replicas)
   Because it's cheaper ($15 vs $30+)
   Good enough for development
   Can upgrade later if needed

✅ Amazon EBS (not Metal)
   Because it's cheaper
   Metal is for extreme performance needs
   EBS is perfect for your needs

✅ aarch64 (not x86-64)
   Because it's cheaper
   Better price-to-performance ratio
   Fully compatible with your app

✅ PS-5 ($15/mo)
   Because 512 MB RAM is enough
   Can upgrade to PS-10 if needed
   Good balance of cost and performance
```

---

## ❓ COMMON QUESTIONS

### Q: Will my data fit in 512 MB?
**A:** YES! Your database is small (~50-100 MB based on current data). Plenty of room.

### Q: Can I upgrade later?
**A:** YES! Click "Scale" button anytime to upgrade to PS-10, PS-20, etc.

### Q: Can I downgrade?
**A:** Not to free, but you can cancel and create a new one.

### Q: Is it secure?
**A:** YES! PlanetScale uses SSL, firewalls, and password protection. Very secure.

### Q: Will my app work the same?
**A:** YES! Vitess is 100% MySQL compatible. No code changes needed.

### Q: Can I export my data later?
**A:** YES! Full backups, can export anytime.

---

## 📱 SELECTION SUMMARY (Copy This)

```
CREATE YOUR DATABASE WITH THESE SETTINGS:

Database Name: edusync
Organization: bodkesrikanth1
Region: us-east-1 (N. Virginia)
Engine: Vitess (MySQL) ← CLICK THIS
Cluster: Single node ← CLICK THIS
Storage: Amazon EBS ← CLICK THIS
Architecture: aarch64 ← CLICK THIS TAB
Plan: PS-5 ($15/mo) ← CLICK THIS

THEN: Click "Create database" button
```

---

## 🆘 IF SOMETHING GOES WRONG

```
Too expensive costs?
→ Use free tier when it's available
→ Look for promo codes

Can't find Vitess option?
→ Select database engine at top
→ Make sure you're on main page

Wrong selections?
→ Don't worry, can create another one
→ Delete this one from settings

Connection fails?
→ Copy credentials again carefully
→ Check firewall settings
→ Verify credentials in .env file
```

---

## ✅ FINAL CHECKLIST

- [ ] Database name: edusync
- [ ] Organization: bodkesrikanth1
- [ ] Region: us-east-1
- [ ] Engine: **Vitess** (MySQL)
- [ ] Cluster: **Single node**
- [ ] Storage: **Amazon EBS**
- [ ] Architecture: **aarch64**
- [ ] Plan: **PS-5 ($15/mo)**
- [ ] Click "Create database"
- [ ] Wait for creation (3-5 min) ✅
- [ ] Copy credentials
- [ ] Add to .env file
- [ ] Import your backup
- [ ] Test connection
- [ ] Ready to deploy!

---

**Good luck with your deployment! 🚀**

If you get stuck on any step, let me know!
