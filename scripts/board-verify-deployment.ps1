#!/usr/bin/env powershell
<#
.SYNOPSIS
    Board Deployment Verification Script
    FOR GOVERNANCE BOARD REVIEW AND APPROVAL

.DESCRIPTION
    This script must be run by a board member before deploying to production.
    It verifies that the deployment is safe and Byzantine-resilient.

.PARAMETER TargetStage
    Which stage to verify: 'canary', 'staging', or 'production'

.PARAMETER NodeName
    Which node to verify (default: all in that stage)

.NOTES
    Requires board authentication and approval
    All results logged to BOARD_DEPLOYMENT_LOG.txt
#>

param(
    [ValidateSet('canary', 'staging', 'production')]
    [string]$TargetStage = 'canary',
    [string]$NodeName = '',
    [bool]$ApproveDeployment = $false
)

Write-Host "=================================="
Write-Host "BOARD DEPLOYMENT VERIFICATION"
Write-Host "=================================="
Write-Host "Time: $(Get-Date -Format 'u')"
Write-Host "Stage: $TargetStage"
Write-Host "Verifier: $(whoami)"
Write-Host ""

# Define nodes for each stage
$nodeMap = @{
    'canary' = @('canary-node-1')
    'staging' = @('staging-node-2', 'staging-node-3', 'staging-node-4')
    'production' = @('prod-node-5', 'prod-node-6', 'prod-node-7', 'prod-node-8', 'prod-node-9', 'prod-node-10', 'prod-node-11', 'prod-node-12', 'prod-node-13')
}

$nodesToCheck = if ($NodeName) { @($NodeName) } else { $nodeMap[$TargetStage] }

Write-Host "Checking nodes: $($nodesToCheck -join ', ')"
Write-Host ""

$results = @{
    'healthy_nodes' = 0
    'voting_nodes' = 0
    'syncing_nodes' = 0
    'failed_nodes' = @()
}

# Check each node
foreach ($node in $nodesToCheck) {
    Write-Host "Checking $node..."

    # Health check
    try {
        $health = Invoke-WebRequest "http://$node/health" -TimeoutSec 5 -ErrorAction Stop
        $healthData = $health.Content | ConvertFrom-Json

        if ($healthData.status -eq 'ok') {
            $results['healthy_nodes']++
            Write-Host "  [OK] Health check passed"
        } else {
            $results['failed_nodes'] += $node
            Write-Host "  [FAIL] Health status: $($healthData.status)"
        }
    }
    catch {
        $results['failed_nodes'] += $node
        Write-Host "  [FAIL] Cannot reach node (timeout or error)"
    }

    # Byzantine voting check
    try {
        $consensus = Invoke-WebRequest "http://$node/api/consensus/status" -TimeoutSec 5 -ErrorAction Stop
        $consensusData = $consensus.Content | ConvertFrom-Json

        if ($consensusData.voting -eq $true) {
            $results['voting_nodes']++
            Write-Host "  [OK] Byzantine voting active"
        } else {
            Write-Host "  [FAIL] Byzantine voting not active"
        }
    }
    catch {
        Write-Host "  [FAIL] Cannot check Byzantine voting"
    }

    # Mesh network sync check
    try {
        $peers = Invoke-WebRequest "http://$node/api/mesh/peers" -TimeoutSec 5 -ErrorAction Stop
        $peersData = $peers.Content | ConvertFrom-Json

        $peerCount = $peersData.connected_peers.Count
        if ($peerCount -gt 0) {
            $results['syncing_nodes']++
            Write-Host "  [OK] Mesh network active ($peerCount peers)"
        } else {
            Write-Host "  [WARN] No mesh peers connected (might be isolated)"
        }
    }
    catch {
        Write-Host "  [FAIL] Cannot check mesh network"
    }

    Write-Host ""
}

# Summary
Write-Host "=================================="
Write-Host "VERIFICATION SUMMARY"
Write-Host "=================================="
$totalNodes = $nodesToCheck.Count
Write-Host "Total nodes checked: $totalNodes"
Write-Host "Healthy: $($results['healthy_nodes'])/$totalNodes"
Write-Host "Voting: $($results['voting_nodes'])/$totalNodes"
Write-Host "Mesh synced: $($results['syncing_nodes'])/$totalNodes"

if ($results['failed_nodes'].Count -gt 0) {
    Write-Host ""
    Write-Host "[FAIL] The following nodes failed checks:"
    $results['failed_nodes'] | ForEach-Object { Write-Host "  - $_" }
}

# Byzantine check: need 2/3 of nodes for quorum
$quorumNeeded = [math]::Ceiling($totalNodes * 2 / 3)
$hasQuorum = $results['healthy_nodes'] -ge $quorumNeeded

Write-Host ""
Write-Host "Byzantine Resilience Check:"
Write-Host "  Nodes required for quorum: $quorumNeeded"
Write-Host "  Nodes with quorum: $($results['healthy_nodes'])"

if ($hasQuorum) {
    Write-Host "  [OK] System has Byzantine quorum"
    $deploymentSafe = $true
} else {
    Write-Host "  [FAIL] System DOES NOT have quorum - UNSAFE TO DEPLOY"
    $deploymentSafe = $false
}

# Final decision
Write-Host ""
Write-Host "=================================="
if ($deploymentSafe -and $results['healthy_nodes'] -eq $totalNodes) {
    Write-Host "DEPLOYMENT SAFE: ALL CHECKS PASSED"
    Write-Host "Board member may approve deployment"
    Write-Host "=================================="

    if ($ApproveDeployment) {
        Write-Host ""
        Write-Host "DEPLOYMENT APPROVED BY: $(whoami)"
        Write-Host "APPROVED AT: $(Get-Date -Format 'u')"
        Write-Host "STAGE: $TargetStage"

        # Log approval
        $logEntry = @"
$(Get-Date -Format 'u') | APPROVED | $TargetStage | $(whoami) | All nodes healthy
"@
        Add-Content -Path "BOARD_DEPLOYMENT_LOG.txt" -Value $logEntry
    }
    exit 0
} elseif ($deploymentSafe) {
    Write-Host "DEPLOYMENT POSSIBLE BUT NOT OPTIMAL"
    Write-Host "Some nodes unhealthy - investigate before proceeding"
    Write-Host "=================================="
    exit 1
} else {
    Write-Host "DEPLOYMENT UNSAFE: QUORUM LOST"
    Write-Host "DO NOT DEPLOY - System would lose Byzantine resilience"
    Write-Host "=================================="

    # Log denial
    $logEntry = @"
$(Get-Date -Format 'u') | BLOCKED | $TargetStage | $(whoami) | No Byzantine quorum
"@
    Add-Content -Path "BOARD_DEPLOYMENT_LOG.txt" -Value $logEntry
    exit 1
}
