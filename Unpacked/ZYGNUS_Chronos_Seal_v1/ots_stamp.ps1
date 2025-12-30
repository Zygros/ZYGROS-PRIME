Param([string]$hash="139B2A40E53F81C9DB7841B914A6E82F708362D55C75A3841C09E0D462F81D63351C7E924B6A3102434E5728C91F2610")
$hash | Out-File -Encoding ascii seal.txt
ots stamp seal.txt
Write-Host "Stamped: seal.txt.ots"
