"""Manual credential type creation script"""

def create_vault_static_credential_type():
    """Create the Vault Static Secrets credential type"""
    try:
        from awx.main.models.credential import CredentialType
        
        existing = CredentialType.objects.filter(name="Vault Static Secrets").first()
        if existing:
            print(f"Vault Static Secrets credential type already exists (ID: {existing.id})")
            return existing
        
        credential_type = CredentialType.objects.create(
            name="Vault Static Secrets",
            description="Retrieve static secrets from HashiCorp Vault KV store",
            kind="cloud",
            namespace=None,
            inputs={"plugin_name": "vault_static_secrets"},
            injectors={"env": {"VAULT_SECRET": "{{ secret_value }}"}},
            managed=True
        )
        
        print(f"Created Vault Static Secrets credential type (ID: {credential_type.id})")
        return credential_type
        
    except Exception as e:
        print(f"Error creating Vault Static Secrets credential type: {e}")
        return None

def create_vault_dynamic_credential_type():
    """Create the Vault Dynamic Secrets credential type"""
    try:
        from awx.main.models.credential import CredentialType
        
        existing = CredentialType.objects.filter(name="Vault Dynamic Secrets").first()
        if existing:
            print(f"Vault Dynamic Secrets credential type already exists (ID: {existing.id})")
            return existing
        
        credential_type = CredentialType.objects.create(
            name="Vault Dynamic Secrets",
            description="Generate dynamic secrets from HashiCorp Vault",
            kind="cloud",
            namespace=None,
            inputs={"plugin_name": "vault_dynamic_secrets"},
            injectors={"env": {"VAULT_CREDENTIAL": "{{ credential_value }}"}},
            managed=True
        )
        
        print(f"Created Vault Dynamic Secrets credential type (ID: {credential_type.id})")
        return credential_type
        
    except Exception as e:
        print(f"Error creating Vault Dynamic Secrets credential type: {e}")
        return None

def main():
    """Create both credential types"""
    print("Creating Vault credential types...")
    
    static_type = create_vault_static_credential_type()
    dynamic_type = create_vault_dynamic_credential_type()
    
    if static_type and dynamic_type:
        print("\n✅ All credential types created successfully!")
    else:
        print("\n❌ Some credential types failed to create. Check logs for details.")

if __name__ == '__main__':
    main()
