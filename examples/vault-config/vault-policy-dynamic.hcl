# Policy for dynamic secrets generation
path "database/creds/dba-readonly" {
  capabilities = ["read"]
}

path "database/creds/dba-readwrite" {
  capabilities = ["read"]
}

path "database/creds/app-user" {
  capabilities = ["read"]
}
