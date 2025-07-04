Add-Type -AssemblyName System.Windows.Forms

# Download-Links
$downloadLinks = @{
    "1" = @{
        Name = "Basic Modpack"
        Url  = "https://github.com/realrdbr/TerraEight-V2/releases/download/v1.0.0-basic/TerraEight-V2.zip"
    }
    "2" = @{
        Name = "Enhanced Modpack"
        Url  = "https://github.com/realrdbr/TerraEight-V2/releases/download/v1.0.0-enhanced/TerraEightV2-Enhance.zip"
    }
}

Write-Host "Bitte wählen Sie das gewünschte Modpack aus:"
foreach ($key in $downloadLinks.Keys) {
    Write-Host "{$key}: $($downloadLinks[$key].Name)"
}

do {
    $choice = Read-Host "Ihre Wahl (1 oder 2)"
    if (-not $downloadLinks.ContainsKey($choice)) {
        Write-Host "Ungültige Eingabe. Bitte geben Sie '1' oder '2' ein."
    }
} until ($downloadLinks.ContainsKey($choice))

$modpackName = $downloadLinks[$choice].Name
$zipUrl = $downloadLinks[$choice].Url
Write-Host "Sie haben '$modpackName' gewählt."
Write-Host "Der Download-Link ist: $zipUrl"

# choose target directory
$folderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
$defaultPath = [System.IO.Path]::Combine($env:USERPROFILE, "Documents", "My Games", "Terraria", "tModLoader", "Mods", "ModPacks")
$folderBrowser.SelectedPath = $defaultPath
$folderBrowser.Description = "Wählen Sie den Zielordner für das Modpack aus."
if ($folderBrowser.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
    $targetDirectory = $folderBrowser.SelectedPath
} else {
    Write-Host "Kein Zielordner ausgewählt. Vorgang abgebrochen."
    exit
}

if (-not (Test-Path $targetDirectory)) {
    Write-Host "Zielordner '$targetDirectory' existiert nicht. Erstelle ihn..."
    New-Item -ItemType Directory -Path $targetDirectory -Force | Out-Null
    Write-Host "Zielordner erfolgreich erstellt."
}

# temporäre ZIP-File
$zipFilename = Join-Path $targetDirectory "downloaded_modpack.zip"

# Progressbar + Download
Write-Host "Starte Download..."
try {
    Invoke-WebRequest -Uri $zipUrl -OutFile $zipFilename
    Write-Host "ZIP-Datei erfolgreich nach '$zipFilename' heruntergeladen."
} catch {
    Write-Host "Fehler beim Herunterladen der Datei: $_"
    exit
}

# extract
Write-Host "Entpacke die ZIP-Datei nach '$targetDirectory'..."
try {
    Expand-Archive -LiteralPath $zipFilename -DestinationPath $targetDirectory -Force
    Write-Host "ZIP-Datei erfolgreich entpackt."
} catch {
    Write-Host "Fehler beim Entpacken: $_"
    exit
}

# cleanup
Remove-Item $zipFilename -Force -ErrorAction SilentlyContinue
Write-Host "Heruntergeladene ZIP-Datei gelöscht."
Write-Host "Vorgang abgeschlossen."
Read-Host -Prompt "Druecke [Enter], um das Skript zu beenden."

exit
# End of script