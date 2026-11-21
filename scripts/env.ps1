# Dot-source from the repo root:  . .\scripts\env.ps1
# Redirects every heavy cache into .\cache (git-ignored) so nothing lands on C:.
$root = (Get-Location).Path
$env:PIP_CACHE_DIR       = Join-Path $root "cache\pip"
$env:HF_HOME             = Join-Path $root "cache\huggingface"
$env:TORCH_HOME          = Join-Path $root "cache\torch"
$env:TEMP                = Join-Path $root "cache\tmp"
$env:TMP                 = $env:TEMP
$env:PYTHONDONTWRITEBYTECODE = "1"
Write-Host "Caches redirected to $root\cache"
