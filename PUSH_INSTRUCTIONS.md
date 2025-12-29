# How to Push with Entropix Account

## The Problem
Git is using GitHub CLI (`gh`) which is authenticated as `franciscohumarang`, but you need to push as `entropixai`.

## Solution: Use HTTPS with Personal Access Token

### Step 1: Create a Personal Access Token (if you don't have one)
1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Name it: "FlakeStorm Repo Access"
4. Select scopes: `repo` (full control of private repositories)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again!)

### Step 2: Push with the token
Run this command in your terminal:

```bash
cd /Users/imac-frank/etropix
git push origin main
```

When prompted:
- **Username**: `entropixai`
- **Password**: Paste your Personal Access Token (NOT your GitHub password)

The credentials will be saved in macOS Keychain for future use.

### Alternative: Use GitHub CLI with Entropix Account

If you want to use GitHub CLI instead:

```bash
# Logout from current account
gh auth logout

# Login with entropix account
gh auth login
# Follow prompts, select:
# - GitHub.com
# - HTTPS
# - Login with a web browser
# - Authenticate as entropixai

# Then push
git push origin main
```

### Verify Configuration

Check your current setup:
```bash
cd /Users/imac-frank/etropix
git config --local --list | grep -E "(user|credential|remote)"
```

You should see:
- `user.name=Entropix`
- `user.email=entropixai@icloud.com`
- `remote.origin.url=https://github.com/entropixai/entropix.git`
- `credential.helper=osxkeychain`

## Current Status
✅ Repository configured to use HTTPS
✅ Local user set to Entropix account
✅ Credential helper set to osxkeychain
✅ GitHub CLI credential bypassed for this repo

You're ready to push! Just run `git push origin main` and enter your PAT when prompted.
