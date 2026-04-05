# Cloud & Kubernetes Review Playbook (03)

## Visión Ejecutiva

Assessment de configuración cloud (AWS/Azure/GCP) y Kubernetes.
Cobertura: IAM, storage, networking, secrets, RBAC, admission controls.
Entrega: Configuration gaps, hardening guide, risk scores.

**Scope típico**: 2-5 días  

---

## Fase 1: Inventario (1-2 días)

### Cloud Enumeration

```bash
# AWS
aws ec2 describe-instances > ec2.json
aws s3 ls > s3-buckets.txt (check public)
aws iam list-users > users.json
aws iam list-roles > roles.json

# Azure
az vm list > vms.json
az storage account list > storage.json
az ad user list > users.json

# GCP
gcloud compute instances list > instances.json
gsutil ls > storage.json
gcloud iam service-accounts list > svc-accounts.json
```

**Deliverable**: `cloud-inventory.json`
```json
{
  "aws": {
    "accounts": ["prod", "staging"],
    "regions": ["us-east-1", "eu-west-1"],
    "ec2_instances": 45,
    "s3_buckets": 23,
    "iam_roles": 67
  }
}
```

### Kubernetes Enumeration

```bash
kubectl get all -A > k8s-all.json
kubectl get sa -A > svc-accounts.json
kubectl get pvc -A > storage.json
kubectl get networkpolicy -A > netpolicy.json
kubectl get roles,rolebindings -A > rbac.json
```

**Deliverable**: `k8s-inventory.json`
```json
{
  "namespaces": 12,
  "pods": 234,
  "services": 45,
  "rbac_rules": 89,
  "network_policies": 3,
  "admission_controllers": ["ValidatingWebhook", "MutatingWebhook"]
}
```

### IaC Discovery

```bash
# Encuentra Terraform, Helm, CloudFormation
find . -name "*.tf" > terraform-files.txt
find . -name "*.yaml" -path "*/helm/*" > helm-charts.txt
find . -name "*.json" -path "*/cloudformation/*" > cf-templates.txt
```

---

## Fase 2: IAM Audit (1-2 días)

### AWS Example

```bash
# Root account
aws iam get-account-summary
# Busca: AccessKeysPerUserQuota > 0 (root con access keys? ❌)

# Users
aws iam list-users
for user in $(aws iam list-users --query 'Users[*].[UserName]' --output text); do
  aws iam list-access-keys --user-name $user
  aws iam list-attached-user-policies --user-name $user
done

# Roles
aws iam list-roles | grep -i "wildcard\|admin" 

# Trust relationships
aws iam get-role --role-name RoleName | jq .Role.AssumeRolePolicyDocument
# Busca: Principal: "*"  →  PROBLEM ❌
```

### Risk Patterns

```
CRÍTICO:
- Root cuenta con access keys
- Wildcard (*) en Action
- Principal: "*" en trust
- Roles con FullAdmin

ALTO:
- No MFA en interactivos usuarios
- Cross-account access sin restricción
- Old unused roles (never accessed)
```

### Remediation Patterns

```hcl
# Least privilege IAM policy
resource "aws_iam_policy" "s3_read_only" {
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = ["s3:GetObject", "s3:ListBucket"]
      Resource = ["arn:aws:s3:::my-bucket", "arn:aws:s3:::my-bucket/*"]
      Condition = {
        StringEquals = { "aws:SourceVpc" = "vpc-12345" }
      }
    }]
  })
}
```

---

## Fase 3: Storage & Secrets (1 día)

### Public Access Check

```bash
# AWS S3
aws s3api list-buckets --query 'Buckets[*].Name' |
  while read bucket; do
    acl=$(aws s3api get-bucket-acl --bucket $bucket | grep -c "AllUsers\|AuthenticatedUsers")
    [ $acl -gt 0 ] && echo "PUBLIC: $bucket"
  done

# Azure Blobs
az storage account list |
  jq -r '.[] | .name' |
  while read account; do
    az storage container list --account-name $account |
    jq -r '.[] | select(.properties.publicAccess != null) | .name'
  done
```

### Encryption Check

```bash
# AWS
aws ec2 describe-volumes \
  --filters "Name=encrypted,Values=false" > unencrypted-ebs.json

aws rds describe-db-instances \
  --query 'DBInstances[?StorageEncrypted==`false`]' > unencrypted-rds.json
```

### Secrets Management

```
❌ NEVER:
- Hardcoded en Terraform
- Hardcoded en Docker images
- Hardcoded en environment variables (visible in `env`)

✅ USE:
- AWS Secrets Manager / Parameter Store
- Azure Key Vault
- GCP Secret Manager
- Kubernetes Secrets (con RBAC)
- Vault (open source)
```

---

## Fase 4: Networking (1 día)

### Security Groups / NSGs

```bash
# AWS: todas las rules de ingreso
aws ec2 describe-security-groups \
  --query 'SecurityGroups[*].[GroupId,GroupName,IpPermissions[*].[FromPort,IpRange]]' |
  grep -i "0.0.0.0/0"  # PROBLEM: open to world

# Remediation: ¿Por qué 0.0.0.0/0 es necesario?
# Generalmente: no. Restringir a IPs específicas / security groups
```

### Network Policies (Kubernetes)

```yaml
# Default deny, then allow
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
---
# Luego allowlist tráfico específico
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-api
spec:
  podSelector:
    matchLabels:
      tier: api
  ingress:
  - from:
    - podSelector:
        matchLabels:
          tier: frontend
```

### VPC Segmentation

```
No debería haber:
- 1 subnet para "todo"
- Subnets públicas con DBs
- NAT gateway sin logging
- VPN sin MFA

Debería haber:
- Public tier (web servers, NAT, bastion)
- Private tier (apps)
- Isolated tier (DBs, secrets)
- VPC Flow Logs habilitado
```

---

## Fase 5: Workload Security (1 día)

### Kubernetes RBAC

```bash
# Encontrar permisos excesivos
kubectl get rolebindings -A -o json | jq '.items[] | select(.roleRef.kind=="Role" and (.roleRef.rules[] | select(.verbs[] == "*")))'

# Encontrar ClusterAdmin
kubectl get clusterrolebindings | grep cluster-admin
# Debería ser: system:masters, system:kube-controller-manager (no usuarios)
```

### Pod Security

```yaml
# Pod Security Policy (deprecated) / Pod Security Standards
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted
spec:
  privileged: false
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'MustRunAs'
    seLinuxOptions:
      level: "s0:c123,c456"
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
  - ALL
```

### Image Security

```bash
# Scan imágenes por vulnerabilidades
trivy image myregistry.azurecr.io/app:latest
grype myregistry.azurecr.io/app:latest

# Verificar image signing (Cosign)
cosign verify myregistry.azurecr.io/app:latest --key cosign.pub

# No: imágenes `latest`, imágenes de terceros sin scan
```

---

## Fase 6: IaC Review (1-2 días)

### Terraform Audit

```bash
# Automated scanning
checkov -d . --framework terraform

# Manual review patterns
grep -n "default_db_password" *.tf
grep -n "0.0.0.0/0" *.tf
grep -n "publicly_accessible = true" *.tf

# Busca: hardcoded values, public resources, weak policies
```

### Helm Charts

```bash
# Validation
helm lint ./mychart
helm template ./mychart | kubectl apply --dry-run=client -f -

# Security checks
kubesec scan mychart/templates/*.yaml
```

---

## Fase 7: Compliance & Hardening (1 día)

### CIS Benchmarks

```
AWS Foundational Security Best Practices:
- [ ] IAM policies restrict root account
- [ ] MFA enabled for console access
- [ ] CloudTrail enabled and logging
- [ ] No root access keys
- [ ] S3 bucket server-side encryption enabled
- [ ] RDS encryption at rest enabled
- [ ] ECR image scanning enabled
- [ ] API Gateway logging enabled

Kubernetes CIS:
- [ ] Minimize RBAC roles
- [ ] Minimize use of wildcards in RBAC roles
- [ ] Ensure network policies are created
- [ ] Encrypt secrets at rest
- [ ] Audit logging enabled
```

---

## Salida Esperada

1. **Cloud Inventory**: JSON con recursos
2. **Findings**: JSON normalizado
3. **Hardening Scripts**: Terraform/YAML fixes
4. **Compliance Checklist**: CIS gaps
5. **Roadmap**: 30-90-180 días

---

## Herramientas

| Herramienta | Propósito |
|---|---|
| Prowler | AWS audit |
| Checkov | IaC scanning |
| Kubesec | Kubernetes config |
| Trivy | Container image scan |
| Terraform | IaC |
| Helm | Kubernetes |

