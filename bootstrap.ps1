#requires -Version 5.1
# bootstrap.ps1 — first-time setup for an aisa installation on Windows.
#
# What this does (idempotent — re-runnable):
#  1. Verifies `aisa/` is in the expected location.
#  2. Verifies (and reports) jq presence — informational only.
#  3. Marks the hook scripts executable (not needed on Windows but kept for parity).
#  4. Reads or asks for the engagement-repo path (`aisa-engagements-galp/` or other).
#  5. Sets `AISA_ENGAGEMENTS_ROOT` for the current shell + writes a `.env.local` hint.
#  6. Optionally creates a directory junction `projects/` → engagement repo.
#  7. Reports the final state and the next command (`claude .` then `/start`).
#
# This script does NOT create the engagement repo itself — that is a deliberate
# manual git operation (Phase 11 of the implementation plan defers it to the user).

[CmdletBinding()]
param(
  [string]$EngagementRoot = "",
  [switch]$NoJunction
)

$ErrorActionPreference = "Stop"

Write-Host "aisa — bootstrap" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan
Write-Host ""

# 1. location check
$root = (Get-Location).Path
if (-not (Test-Path "$root/CLAUDE.md") -or -not (Test-Path "$root/library/kernel")) {
  Write-Host "[ERROR] This script must be run from the aisa/ root (where CLAUDE.md lives)." -ForegroundColor Red
  exit 1
}
Write-Host "[OK] aisa root: $root"

# 2. jq presence
$jq = Get-Command jq -ErrorAction SilentlyContinue
if ($jq) {
  Write-Host "[OK] jq found at $($jq.Source)"
} else {
  Write-Host "[WARN] jq not found — hook scripts will no-op (log only)." -ForegroundColor Yellow
  Write-Host "       Install with: winget install jqlang.jq   (or:  choco install jq)"
}

# 3. hook scripts (parity with Unix)
if (Test-Path "$root/.claude/hooks") {
  Get-ChildItem "$root/.claude/hooks/*.sh" | ForEach-Object {
    # Windows does not need chmod, but record we touched them
  }
  Write-Host "[OK] Hook scripts present in .claude/hooks/"
}

# 4. engagement-repo path
if (-not $EngagementRoot) {
  $defaultRoot = (Resolve-Path "$root/..").Path + "\aisa-engagements-galp"
  Write-Host ""
  Write-Host "Where should engagement folders live?"
  Write-Host "  (sibling of aisa/, gitignored from aisa/, mounted at projects/)" -ForegroundColor DarkGray
  $input = Read-Host "Engagement root [$defaultRoot]"
  if ([string]::IsNullOrWhiteSpace($input)) {
    $EngagementRoot = $defaultRoot
  } else {
    $EngagementRoot = $input
  }
}
if (-not (Test-Path $EngagementRoot)) {
  Write-Host "[NOTE] Engagement root does not exist: $EngagementRoot"
  Write-Host "        Create it manually (it usually wants to be its own private git repo)."
}

# 5. env var
$env:AISA_ENGAGEMENTS_ROOT = $EngagementRoot
Write-Host "[OK] AISA_ENGAGEMENTS_ROOT set for this shell: $EngagementRoot"

$envFile = "$root/.env.local"
$envBlock = "AISA_ENGAGEMENTS_ROOT=$EngagementRoot"
if (Test-Path $envFile) {
  $existing = Get-Content $envFile -Raw
  if ($existing -notmatch "AISA_ENGAGEMENTS_ROOT=") {
    Add-Content -Path $envFile -Value $envBlock
    Write-Host "[OK] Appended to .env.local"
  } else {
    Write-Host "[OK] .env.local already has AISA_ENGAGEMENTS_ROOT — left untouched."
  }
} else {
  Set-Content -Path $envFile -Value $envBlock -Encoding utf8
  Write-Host "[OK] Wrote .env.local"
}

# 6. optional junction
if (-not $NoJunction) {
  $junction = "$root/projects"
  if (Test-Path $junction) {
    $item = Get-Item $junction
    if ($item.Attributes -match "ReparsePoint") {
      Write-Host "[OK] projects/ junction already in place"
    } else {
      Write-Host "[WARN] projects/ is a real directory, not a junction. Leaving as-is." -ForegroundColor Yellow
      Write-Host "        Move its contents to $EngagementRoot if you want to switch."
    }
  } elseif (Test-Path $EngagementRoot) {
    try {
      New-Item -ItemType Junction -Path $junction -Target $EngagementRoot | Out-Null
      Write-Host "[OK] Created projects/ junction → $EngagementRoot"
    } catch {
      Write-Host "[WARN] Could not create junction (need admin shell?): $_" -ForegroundColor Yellow
      Write-Host "        Falling back to AISA_ENGAGEMENTS_ROOT env var only."
    }
  } else {
    Write-Host "[SKIP] Junction not created — engagement root not present yet."
  }
}

# 7. summary
Write-Host ""
Write-Host "Setup complete." -ForegroundColor Green
Write-Host ""
Write-Host "Next:"
Write-Host "  1. Open a new shell or run: . .\.env.local  (loads AISA_ENGAGEMENTS_ROOT)"
Write-Host "  2. Launch:                   claude ."
Write-Host "  3. Start an engagement:     /start <slug> [pack]"
Write-Host ""
