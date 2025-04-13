$PROJECT_NAME = "CourtCaseMonitor"
$MODE = $args[0]

if ($MODE -ne "dev" -and $MODE -ne "prod") {
    Write-Host "Invalid mode. Use: dev or prod"
    Write-Host "Example: .\manage.ps1 dev"
    exit 1
}

if ($MODE -eq "dev") {
    Write-Host "Starting $PROJECT_NAME in development mode..."
    docker compose up --build
}
else {
    Write-Host "Starting $PROJECT_NAME in production mode..."
    docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
}
