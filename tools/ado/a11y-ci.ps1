<#
.SYNOPSIS
    Runs the a11y-ci gate with unified artifact handling.
    Designed for Azure DevOps pipelines but can be run locally.

.DESCRIPTION
    Wrapper around a11y-ci CLI tools.
    Standardizes on the use of --artifact-dir (defaulting to .a11y_artifacts).
    Encourages "Convention over Configuration" by inferring scorecard paths.

.PARAMETER ArtifactDir
    Directory to output artifacts. Default: $(Build.SourcesDirectory)/.a11y_artifacts.

.PARAMETER Current
    Path to current scorecard. Optional if present in ArtifactDir.

.PARAMETER Baseline
    Path to baseline scorecard. Optional if present in ArtifactDir.

.PARAMETER Allowlist
    Path to allowlist. Optional if present in ArtifactDir.

.PARAMETER FailOn
    Minimum severity to fail the build. Default: serious.

.PARAMETER Top
    Limit blocking findings in output. Default: 10.

.PARAMETER Platform
    Markdown flavor for PR comments (github or ado). Default: ado.

.PARAMETER PostComment
    Whether to generate the PR comment file. Default: true.

.EXAMPLE
    .\a11y-ci.ps1
    (Infers everything from .a11y_artifacts/)

.EXAMPLE
    .\a11y-ci.ps1 -Current "custom.json" -FailOn "minor"
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [string]$ArtifactDir = "$(Build.SourcesDirectory)/.a11y_artifacts",

    [Parameter(Mandatory=$false)]
    [string]$Current,

    [Parameter(Mandatory=$false)]
    [string]$Baseline,

    [Parameter(Mandatory=$false)]
    [string]$Allowlist,

    [Parameter(Mandatory=$false)]
    [string]$FailOn = "serious",

    [Parameter(Mandatory=$false)]
    [int]$Top = 10,

    [Parameter(Mandatory=$false)]
    [string]$Platform = "ado",

    [Parameter(Mandatory=$false)]
    [switch]$PostComment
)

$ErrorActionPreference = "Stop"

function Log-Section {
    param([string]$Message)
    Write-Host "##[section]$Message"
}

function Log-Error {
    param([string]$Message)
    Write-Host "##[error]$Message"
}

function Log-Warning {
    param([string]$Message)
    Write-Host "##[warning]$Message"
}

# 1. Setup Artifacts
Log-Section "Setting up Artifacts"

# Clean path robustly
$ArtifactDir = $ArtifactDir.TrimEnd("\").TrimEnd("/")
Write-Host "Using artifact directory: $ArtifactDir"

if (-not (Test-Path $ArtifactDir)) {
    New-Item -ItemType Directory -Path $ArtifactDir -Force | Out-Null
}

$Global:ReportJson = Join-Path $ArtifactDir "report.json"
$Global:EvidenceJson = Join-Path $ArtifactDir "evidence.json"
$Global:CommentMd = Join-Path $ArtifactDir "comment.md"
$Global:GateResultJson = Join-Path $ArtifactDir "gate-result.json"

# 2. Resolve Inputs (Wrapper encourages standard paths)
Log-Section "Resolving Inputs"

# If Current is not provided, check the artifact dir
if (-not $Current -or $Current.Trim() -eq "") {
    $candidate = Join-Path $ArtifactDir "current.scorecard.json"
    if (Test-Path $candidate) {
        $Current = $candidate
        Write-Host "Defaulted Current to: $Current"
    } else {
        # Valid: a11y-ci will throw error if it can"t find it, or we rely on CLI inference
        Log-Warning "Current not provided and $candidate not found. CLI will attempt inference."
    }
}

# 3. Run Gate & Generate Evidence
Log-Section "Running Accessibility Gate"

# Build arguments favoring --artifact-dir
$gateArgs = @(
    "gate",
    "--artifact-dir", $ArtifactDir,
    "--fail-on", $FailOn,
    "--top", $Top
)

# Back-compat: Only pass explicit flags if provided (or inferred above)
if ($Current) { $gateArgs += "--current", $Current }
if ($Baseline) { $gateArgs += "--baseline", $Baseline }
if ($Allowlist) { $gateArgs += "--allowlist", $Allowlist }

Write-Host "Running: a11y-ci $($gateArgs -join " ")"

$exitCode = 0
try {
    # Execute a11y-ci using explicit call to ensure argument passing works
    # We use Start-Process to properly wait and capture exit code
    $proc = Start-Process -FilePath "a11y-ci" -ArgumentList $gateArgs -NoNewWindow -PassThru -Wait
    $exitCode = $proc.ExitCode
}
catch {
    Log-Error "Execution failed: $_"
    exit 1 # Internal error
}

# 4. Generate PR Comment (if requested and evidence exists)
if ($PostComment) {
    Log-Section "Generating PR Comment"

    if (Test-Path $Global:EvidenceJson) {
        try {
            # Use CLI to render comment using "comment" command
            # This ensures consistent formatting (Markdown, sticky markers, etc.)
            
            $commentArgs = "comment", "--mcp", $Global:EvidenceJson, "--platform", $Platform, "--top", $Top
            
            # Using call operator & for capturing output
            # Need to be careful with args array vs string
            $commentStart = & a11y-ci $commentArgs
            
            # Write to file
            $commentStart | Out-File -FilePath $Global:CommentMd -Encoding utf8
            Write-Host "Comment generated at $Global:CommentMd"
        }
        catch {
            Log-Warning "Failed to generate PR comment: $_"
        }
    }
    else {
        Log-Warning "Evidence file missing ($Global:EvidenceJson), cannot generate comment."
    }
}

Log-Section "Summary"
Write-Host "Gate Exit Code: $exitCode"
Write-Host "Artifacts location: $ArtifactDir"

# Set ADO output variables
if ($env:TF_BUILD) {
    Write-Host "##vso[task.setvariable variable=A11yExitCode]$exitCode"
    Write-Host "##vso[task.setvariable variable=A11yReportPath]$Global:EvidenceJson"
    Write-Host "##vso[task.setvariable variable=A11yCommentPath]$Global:CommentMd"
    Write-Host "##vso[task.setvariable variable=A11yGateResultPath]$Global:GateResultJson"
}

# Verify key artifacts exist for user visibility
$expectedArtifacts = @("gate-result.json", "evidence.json", "report.txt")
foreach ($f in $expectedArtifacts) {
    $p = Join-Path $ArtifactDir $f
    if (Test-Path $p) { Write-Host "Artifact present: $p" } else { Log-Warning "Artifact missing: $p" }
}

exit $exitCode
