def create_vault_credential_types():
    """Create all three Vault credential types with Option A implementation"""
    from awx.main.models.credential import CredentialType
    
    print("Creating Vault credential types with reference field approach...")
    
    # Clean up existing types
    existing = CredentialType.objects.filter(
        name__in=["Vault Authentication", "Vault Static Secrets", "Vault Dynamic Secrets"]
    )
    if existing.exists():
        print(f"Cleaning up {existing.count()} existing credential types...")
        existing.delete()
    
    # 1. Vault Authentication
    auth_type = CredentialType.objects.create(
        name="Vault Authentication",
        description="HashiCorp Vault authentication credentials",
        kind="external",
        namespace=None,
        inputs={"plugin_name": "vault_auth"},
        injectors={"env": {"VAULT_AUTH_DATA": "{{ auth_data }}"}},
        managed=True
    )
    print(f"✅ Created Vault Authentication credential type (ID: {auth_type.id})")
    
    # 2. Vault Static Secrets
    static_type = CredentialType.objects.create(
        name="Vault Static Secrets",
        description="Retrieve static secrets from HashiCorp Vault KV store",
        kind="external",
        namespace=None,
        inputs={"plugin_name": "vault_static_secrets"},
        injectors={"env": {"VAULT_SECRET": "{{ secret_value }}"}},
        managed=True
    )
    print(f"✅ Created Vault Static Secrets credential type (ID: {static_type.id})")
    
    # 3. Vault Dynamic Secrets
    dynamic_type = CredentialType.objects.create(
        name="Vault Dynamic Secrets",
        description="Generate dynamic secrets from HashiCorp Vault",
        kind="external",
        namespace=None,
        inputs={"plugin_name": "vault_dynamic_secrets"},
        injectors={"env": {"VAULT_CREDENTIAL": "{{ credential_value }}"}},
        managed=True
    )
    print(f"✅ Created Vault Dynamic Secrets credential type (ID: {dynamic_type.id})")
    
    print("\n🎉 All credential types created successfully!")
    print("\nUsage with Option A (Reference Field Approach):")
    print("1. Create Vault Authentication credentials (stores auth details)")
    print("2. Create Vault Static/Dynamic credentials that reference auth by name")
    print("3. Only attach Static/Dynamic credentials to job templates")
    print("4. Auth credentials are automatically used via reference")
    
    return auth_type, static_type, dynamic_type

if __name__ == '__main__':
    create_vault_credential_types()