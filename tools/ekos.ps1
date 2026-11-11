param(
  [Parameter(Position=0)][ValidateSet("build","search","show","sources")][string]$Command = "build",
  [Parameter(Position=1)][string]$QueryOrId = ""
)
$ErrorActionPreference = "Stop"
if ($Command -eq "build") {
  python "$PSScriptRoot\build_index.py"
} elseif ($Command -eq "search") {
  if (-not $QueryOrId) { throw "Usage: .\tools\ekos.ps1 search <query>" }
  python "$PSScriptRoot\search.py" search $QueryOrId
} elseif ($Command -eq "show") {
  if (-not $QueryOrId) { throw "Usage: .\tools\ekos.ps1 show <document-id>" }
  python "$PSScriptRoot\search.py" show $QueryOrId
} else {
  python "$PSScriptRoot\search.py" sources --query $QueryOrId
}
