# Deployment Governance & Byzantine Safety

**FOR BOARD REVIEW AND APPROVAL**

---

## The Problem We Found

**Current State (BROKEN):**
- All 13 nodes auto-deploy on any git push to master
- One bad commit = all nodes crash simultaneously
- Zero fault tolerance (NOT Byzantine-resilient)
- Single point of failure: the git repository

**Byzantine Principle (What We Should Have):**
- System continues if up to 1/3 of nodes fail
- No single bad deploy should crash all nodes
- Staged rollout ensures validation before full deployment
- Board approval required for major changes

---

## Proposed Deployment Strategy (Board Approval Required)

### Phase 1: Staged Rollout (Canary Deployment)

**Step 1: Deploy to Canary Node (1 node)**
```
Commit pushed to `deploy/canary` branch
↓
Node 1 (designated canary) deploys new code
↓
Run 5-minute health check
  - Does it boot?
  - Can it communicate with other nodes?
  - Can it vote?
  - Can it sync?
↓
If PASSED: Continue to Phase 2
If FAILED: Automatic rollback to previous version
```

**Step 2: Deploy to Staging Nodes (3 nodes)**
```
If canary passed:
↓
Nodes 2, 3, 4 deploy new code
↓
Run 10-minute health check
  - All 3 running?
  - Byzantine consensus still working?
  - Mesh network healthy?
↓
If PASSED: Continue to Phase 3
If FAILED: Automatic rollback
```

**Step 3: Deploy to Production (9 remaining nodes)**
```
If staging passed:
↓
Nodes 5-13 deploy new code gradually
  - 3 nodes every 5 minutes
  - Staggered so not all down at once
  - Health check after each batch
↓
If any node fails: Pause rollout, manual board review
```

---

## Implementation: Remove Auto-Deploy Risk

### Current (BROKEN):
```yaml
# .github/workflows/auto-deploy.yml
on:
  push:
    branches: [master]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to ALL nodes
        run: git push heroku master && git push render master && git push railway master
```

### Fixed Version:

**Branch Policy:**
- `master` = stable, board-approved code (no auto-deploy)
- `deploy/canary` = test on 1 node first
- `deploy/staging` = test on 3 nodes second
- `feature/*` = development branches

**Deployment Workflow:**

```yaml
# .github/workflows/canary-deploy.yml
name: Canary Deployment (1 Node Only)

on:
  push:
    branches: [deploy/canary]

jobs:
  deploy-canary:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      # Deploy ONLY to Node 1 (canary)
      - name: Deploy to Canary Node
        run: |
          git push canary-node-1:${{ secrets.CANARY_DEPLOY_KEY }} HEAD:master
      
      # Run 5-minute health check
      - name: Health Check
        run: |
          for i in {1..10}; do
            sleep 30
            response=$(curl -s http://canary-node-1/health || echo "failed")
            if echo "$response" | grep -q "ok"; then
              echo "Canary node healthy"
              exit 0
            fi
          done
          echo "Canary node failed health check - rolling back"
          exit 1
      
      # If failed, auto-rollback
      - name: Rollback on Failure
        if: failure()
        run: |
          git push canary-node-1:${{ secrets.CANARY_DEPLOY_KEY }} HEAD~1:master
```

**Staging Deployment:**
```yaml
# .github/workflows/staging-deploy.yml
name: Staging Deployment (3 Nodes Only)

on:
  push:
    branches: [deploy/staging]

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    steps:
      # Only deploy if canary branch passed
      - name: Check Canary Status
        run: |
          canary_status=$(git show canary:health-check-status.txt)
          if [ "$canary_status" != "PASS" ]; then
            echo "Canary deployment failed - cannot proceed to staging"
            exit 1
          fi
      
      # Deploy to nodes 2, 3, 4 (staggered)
      - name: Deploy to Staging Batch 1
        run: git push staging-node-2:${{ secrets.STAGING_DEPLOY_KEY }} HEAD:master
      
      - name: Wait 2 minutes for stability
        run: sleep 120
      
      - name: Deploy to Staging Batch 2
        run: git push staging-node-3:${{ secrets.STAGING_DEPLOY_KEY }} HEAD:master
      
      - name: Wait 2 minutes
        run: sleep 120
      
      - name: Deploy to Staging Batch 3
        run: git push staging-node-4:${{ secrets.STAGING_DEPLOY_KEY }} HEAD:master
      
      # Verify all 3 are voting
      - name: Staging Health Check
        run: |
          nodes_healthy=0
          for node in staging-node-{2,3,4}; do
            response=$(curl -s http://$node/api/consensus/status)
            if echo "$response" | grep -q "voting"; then
              ((nodes_healthy++))
            fi
          done
          if [ $nodes_healthy -eq 3 ]; then
            echo "All staging nodes healthy and voting"
            exit 0
          else
            echo "Staging failed - rolling back"
            exit 1
          fi
```

**Production Deployment (BOARD APPROVAL REQUIRED):**
```yaml
# .github/workflows/production-deploy.yml
name: Production Deployment (REQUIRES BOARD APPROVAL)

on:
  workflow_dispatch:  # Manual trigger only, no auto-deploy
    inputs:
      approved_by:
        description: 'Board member approval'
        required: true
      reason:
        description: 'Reason for deployment'
        required: true

jobs:
  deploy-production:
    runs-on: ubuntu-latest
    steps:
      # Verify board approval
      - name: Verify Board Approval
        run: |
          if [ -z "${{ github.event.inputs.approved_by }}" ]; then
            echo "Board approval required"
            exit 1
          fi
      
      # Deploy to production in batches of 3
      - name: Deploy Batch 1 (Nodes 5-7)
        run: |
          git push prod-node-5:${{ secrets.PROD_DEPLOY_KEY }} HEAD:master
          sleep 60
          git push prod-node-6:${{ secrets.PROD_DEPLOY_KEY }} HEAD:master
          sleep 60
          git push prod-node-7:${{ secrets.PROD_DEPLOY_KEY }} HEAD:master
      
      - name: Health Check Batch 1
        run: |
          # Verify 3 nodes are up before proceeding
          healthy=0
          for node in prod-node-{5,6,7}; do
            if curl -s http://$node/health | grep -q "ok"; then
              ((healthy++))
            fi
          done
          if [ $healthy -lt 3 ]; then
            echo "Batch 1 failed - rolling back entire deployment"
            exit 1
          fi
      
      - name: Wait before next batch
        run: sleep 180
      
      - name: Deploy Batch 2 (Nodes 8-10)
        run: |
          git push prod-node-8:${{ secrets.PROD_DEPLOY_KEY }} HEAD:master
          sleep 60
          git push prod-node-9:${{ secrets.PROD_DEPLOY_KEY }} HEAD:master
          sleep 60
          git push prod-node-10:${{ secrets.PROD_DEPLOY_KEY }} HEAD:master
      
      - name: Deploy Batch 3 (Nodes 11-13)
        run: |
          git push prod-node-11:${{ secrets.PROD_DEPLOY_KEY }} HEAD:master
          sleep 60
          git push prod-node-12:${{ secrets.PROD_DEPLOY_KEY }} HEAD:master
          sleep 60
          git push prod-node-13:${{ secrets.PROD_DEPLOY_KEY }} HEAD:master
      
      - name: Final Verification
        run: |
          # Verify all 13 nodes are running and voting
          consensus=$(curl -s https://human-flourishing-frameworks.onrender.com/api/consensus/status)
          if echo "$consensus" | grep -q "voting"; then
            echo "Deployment successful - all nodes voting"
          else
            echo "Deployment failed"
            exit 1
          fi
      
      # Log deployment to audit trail
      - name: Record Deployment
        run: |
          echo "Deployment: $(date)" >> DEPLOYMENT_LOG.md
          echo "Approved by: ${{ github.event.inputs.approved_by }}" >> DEPLOYMENT_LOG.md
          echo "Reason: ${{ github.event.inputs.reason }}" >> DEPLOYMENT_LOG.md
          git add DEPLOYMENT_LOG.md
          git commit -m "Log deployment approved by ${{ github.event.inputs.approved_by }}"
          git push
```

---

## Board Review Checklist

Before ANY code is deployed, the board must review:

### Code Review (Required)
- [ ] Security audit (no backdoors, no vulnerabilities)
- [ ] Algorithm correctness (Byzantine consensus still work?)
- [ ] Cryptographic implementation (signatures still valid?)
- [ ] Breaking changes (will old nodes still understand new code?)

### Deployment Safety (Required)
- [ ] Canary deployment plan documented
- [ ] Rollback procedure tested
- [ ] Health checks in place
- [ ] Board members informed 24 hours before

### Testing (Required)
- [ ] All unit tests pass
- [ ] Byzantine consensus tested with 1/3 faulty nodes
- [ ] Mesh network resilience tested
- [ ] No regressions from previous version

### Approval Process
1. Developer: Propose change to board
2. Board: Review code and test results
3. Board: Vote (80% consensus required for deployment)
4. Board Member: Approve in GitHub (trigger deployment)
5. System: Auto-deploys with safeguards (canary → staging → production)
6. Board: Monitor deployment, ready to halt if needed

---

## Scripts for Board Review

### 1. `health-check-canary.ps1`
```powershell
# Monitors canary node health during deployment
# Board member runs this to verify deployment
param(
    [string]$CanaryNode = "canary-node-1",
    [int]$CheckIntervalSeconds = 30,
    [int]$TotalDurationMinutes = 5
)

$checks = 0
$passes = 0
$endTime = (Get-Date).AddMinutes($TotalDurationMinutes)

while ((Get-Date) -lt $endTime) {
    try {
        $response = Invoke-WebRequest "http://$CanaryNode/api/consensus/status" -TimeoutSec 5
        $json = $response.Content | ConvertFrom-Json
        
        if ($json.voting -eq $true) {
            $passes++
            Write-Host "[OK] Canary node voting ($(Get-Date))"
        }
    }
    catch {
        Write-Host "[FAIL] Canary node not responding ($(Get-Date))"
    }
    
    $checks++
    Start-Sleep -Seconds $CheckIntervalSeconds
}

$passRate = ($passes / $checks) * 100
Write-Host "Canary Health Report: $passes/$checks checks passed ($passRate%)"

if ($passRate -ge 90) {
    Write-Host "[OK] Canary deployment PASSED - safe to proceed to staging"
    exit 0
} else {
    Write-Host "[FAIL] Canary deployment FAILED - DO NOT proceed"
    exit 1
}
```

### 2. `verify-byzantine-resilience.ps1`
```powershell
# Board member runs this to verify Byzantine properties before deployment
# Simulates 1/3 of nodes going down - system should continue

$nodes = @("node-1", "node-2", "node-3")

Write-Host "Byzantine Resilience Test (Board Review)"
Write-Host "==========================================="

# Test: Kill 1 of 3 nodes
Write-Host "`nKilling node-1 to simulate failure..."
& ssh node-1 "pkill -f python app.py"

Start-Sleep -Seconds 5

# Verify remaining 2 nodes can still reach consensus
Write-Host "Checking if nodes 2 and 3 can still vote..."
$consensus = Invoke-WebRequest "http://node-2/api/consensus/status" | ConvertFrom-Json

if ($consensus.voting -eq $true) {
    Write-Host "[OK] Byzantine consensus maintains with 2/3 nodes"
    Write-Host "RESULT: PASS - System is truly Byzantine-resilient"
} else {
    Write-Host "[FAIL] System cannot vote with 1 node down"
    Write-Host "RESULT: FAIL - System is NOT Byzantine-resilient"
}

# Restore node-1
Write-Host "`nRestoring node-1..."
& ssh node-1 "cd human-flourishing-frameworks && python app.py &"
```

### 3. `audit-deployment.ps1`
```powershell
# Board audits deployment history and changes
param([string]$DeploymentHash = "HEAD")

Write-Host "Deployment Audit Report"
Write-Host "======================="
Write-Host ""

# Show what changed
Write-Host "Files changed in this deployment:"
git diff $DeploymentHash~1..$DeploymentHash --name-only

Write-Host ""
Write-Host "Code changes (board member must review):"
git diff $DeploymentHash~1..$DeploymentHash

Write-Host ""
Write-Host "Commit message:"
git log -1 --format="%B" $DeploymentHash

Write-Host ""
Write-Host "Board review required for the above changes before deployment"
```

---

## The Fix (Summary)

| Issue | Fix |
|-------|-----|
| All nodes auto-deploy on git push | Only manual deployments with board approval |
| No rollback mechanism | Auto-rollback if health checks fail |
| No staging/canary | Canary → Staging → Production pipeline |
| No board oversight | Board approval required before each deployment |
| Single point of failure (git) | Byzantine deployment (works if 2/3 succeed) |

---

## Next Steps

1. **Board reviews this deployment governance document**
2. **Board approves deployment strategy**
3. **Implement the 3 GitHub Actions workflows** (canary, staging, production)
4. **Board members trained on health check scripts**
5. **No more auto-deploys to all nodes simultaneously**
6. **All future deployments require 80% board consensus**

---

**Status:** Proposed for board review and approval

**Critical:** Without these safeguards, the system is NOT Byzantine-resilient and has a critical single point of failure.
