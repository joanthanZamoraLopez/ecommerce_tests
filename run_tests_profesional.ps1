# ----------------------------------------
# Script profesional para ejecutar tests
# ----------------------------------------

$venvPath = ".\venv"
$testsPath = ".\tests"
$cssPath = ".\custom_report.css"

# 1️⃣ Crear entorno virtual si no existe
if (-Not (Test-Path $venvPath)) {
    Write-Host "Creando entorno virtual..."
    python -m venv $venvPath
}

# 2️⃣ Activar entorno virtual
Write-Host "Activando entorno virtual..."
& "$venvPath\Scripts\Activate.ps1"

# 3️⃣ Instalar dependencias
Write-Host "Instalando dependencias necesarias..."
pip install --upgrade pip
pip install selenium pytest pytest-html pytest-dependency

# 4️⃣ Crear carpeta de reportes si no existe
if (-Not (Test-Path ".\reports")) {
    New-Item -ItemType Directory -Path ".\reports"
}

# 5️⃣ Crear nombre único de reporte con fecha y hora
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$reportPath = ".\reports\reporte_$timestamp.html"

# 6️⃣ Ejecutar tests con reporte HTML y CSS personalizado
Write-Host "Ejecutando tests con CSS profesional..."
if (Test-Path $cssPath) {
    pytest $testsPath --html=$reportPath --self-contained-html --css=$cssPath -v
} else {
    Write-Host "⚠️ CSS personalizado no encontrado en $cssPath. Usando estilo por defecto."
    pytest $testsPath --html=$reportPath --self-contained-html -v
}

# 7️⃣ Abrir reporte automáticamente
if (Test-Path $reportPath) {
    Write-Host "Abriendo reporte HTML..."
    Start-Process $reportPath
}
