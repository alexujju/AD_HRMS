param (
    [string]$username,
    [string]$email,
    [string]$department,
    [string]$emp_id,
    [string]$display_name,
    [string]$first_name,
    [string]$last_name,
#    [string]$line_manager,
    [string]$laptop_status,
    [string]$phone_number,
    [string]$designation
)

# Import the Active Directory module
Import-Module ActiveDirectory
#Set-ADServerSettings -PreferredServer $domainController

# Get a list of domain controllers
try {
    $domainControllers = Get-ADDomainController -Filter * | Select-Object -ExpandProperty HostName
} catch {
    Write-Error "Failed to retrieve domain controllers: $_"
    exit 1
}

# Use the first domain controller from the list
if ($domainControllers.Count -gt 0) {
    $domainController = $domainControllers[0]
} else {
    Write-Error "No domain controllers found"
    exit 1
}

# Your code to create user in Active Directory using PowerShell
# Example:
# Path to the log file
$logFile = "user_creation_log.txt"

# Redirect all output to the log file
Start-Transcript -Path $logFile -Append

try {

    # Set the properties for the new user
$userProperties = @{
    'Name' = $username
    'GivenName' = $first_name
    'Surname' = $last_name
    'SamAccountName' = $username
    'EmailAddress' = $email
    'Department' = $department
    'EmployeeID' = $emp_id
    'DisplayName' = $display_name
#    'Manager' = $line_manager
    'OfficePhone' = $phone_number
    'Title' = $designation
}
    
New-ADUser @userProperties -Server $domainController -PassThru

Write-Output "User '$username' created successfully in Active Directory $domainController."
}
catch {
    Write-Output "Failed to create user '$username' in Active Directory: $_"
}

# Stop transcript logging
Stop-Transcript