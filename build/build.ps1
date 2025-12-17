# Remove old archive if it exists
if (Test-Path buckshotroulette.apworld) {
    Remove-Item buckshotroulette.apworld
}

# Zip the Buckshot Roulette folder into a .apworld
Compress-Archive -Path "BuckshotRoulette\*" -DestinationPath "buckshotroulette.zip"
Rename-Item "buckshotroulette.zip" "BuckshotRoulette.apworld"
Invoke-Item "BuckshotRoulette.apworld"
