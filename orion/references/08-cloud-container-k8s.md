# Cloud, Container & Kubernetes Security - Cloud-Native Infrastructure Hardening

## SECCIÓN 1: CONCEPTO FUNDAMENTAL

### ¿Por qué existe Cloud & Container Security?

Cloud-native infrastructure (AWS, Azure, GCP, Kubernetes) introduce una **superficie de ataque completamente nueva** diferentes from on-prem:
- **Shared responsibility model**: Cloud provider gestiona infraestructura; tú gestionas aplicaciones, identidades, secretos
- **Automated scaling + microservicios**: Mil instâncias pueden estar vivas en 5 minutos; la mayoría no revisadas
- **Identity explosion**: servicios, aplicaciones, usuarios; cada uno necesita credenciales únicas
- **Configuration-driven**: Código IaC (Terraform, CloudFormation) = misconfiguración = breach

**Objetivo crítico**: Auditar identidad (IAM), almacenamiento (buckets/blobs), compute (instancias, pods), redes (security groups, network policies) y pipes (CI/CD) para encontrar:
- ❌ Permisos amplios sin justificación ("Admin" cuando solo need read)
- ❌ Secretos hardcodeados en código o imágenes
- ❌ Servicios expuestos a internet sin autenticación
- ❌ Imágenes sin scanning de vulnerabilidades
- ❌ Logging disabled (ciego a ataques)

### 5 Principios Fundamentales de Cloud-Native Security

1. **"Publicly Accessible" ≠ "Intended"**
   - Bucket S3 público por defecto? NO. Pero muchos están (missing ACL update)
   - Security group "0.0.0.0/0" (anywhere) para DB port 5432? Accident
   - Kubernetes API exposé públicamente sin auth? VERY bad
   - **Action**: Cambio por defecto es: cierre todo, luego abre solo lo necesario

2. **Principio de Mínimo Privilegio: "Deny by Default"**
   - Rol IAM dice "s3:*" (everything) solo necesita "s3:GetObject" (lectura)
   - Service account en Kubernetes tiene ClusterAdmin pero solo needs get pods en 1 namespace
   - Aplicación tiene credenciales de "prod" pero solo toca "staging"
   - **Regla**: Si no sé qué específicamente necesitas, no te doy permisos amplios

3. **Secrets ≠ Code**
   - Credenciales, API keys, certs NUNCA hardcodeados en:
     - Repositorio (GitHub, GitLab)
     - Imágenes de Docker (Dockerfile ENV VARS, config files)
     - Logs o documentación
     - Terraform state (unencrypted)
   - **Opción correcta**: Vault, Secrets Manager, Sealed Secrets, credencial rotation automática

4. **Logging Habilitado SIEMPRE (o es ciego)**
   - Si no hay logs, no sabes qué pasó
   - CloudTrail, Container Runtime logs, Kubernetes audit logs = evidencia de ataques
   - Retención mínima: 90-365 días
   - **Alerta**: Si intenta acceso no autorizado y no hay logs, es escena perfecta para attacker

5. **Automatización de Seguridad = Consistencia**
   - Provisioning manual = errores (80% misconfigurations son manuales)
   - IaC (Terraform, Helm) + scanning automático (Checkov, Trivy, kubesec) = garantía
   - Admission controllers en Kubernetes = bloquea bad pictures antes de desplegar
   - **Patrón**: Code review → Automated security checks → Gradual rollout → Monitoring

---

## SECCIÓN 2: COMPONENTES TÉCNICOS

### Componente 1: Auditoría de Identidades y Acceso (IAM)

**Objetivo**: Mapear quién tiene acceso a qué, y si es justificado.

**Información técnica**:
- **Usuarios & Service Accounts**: Humanos vs máquinas (CI/CD, aplicaciones, herramientas)
- **Roles & Policies**: Qué permisos tiene cada usuario/servicio
- **Credential Age**: Cuánto tiempo han tenido esa credencial
- **MFA Status**: ¿Multi-factor authentication activado?
- **Últim acceso**: ¿Realmente lo usa o es inherited del anterior owner?

**Checklist - Auditoría IAM**:
- ✅ Listar TODOS los usuarios (humanos) y service accounts (máquinas)
- ✅ Para cada uno, documentar: Nombre, Rol(es), Permisos, Justificación, Última actividad
- ✅ Verificar MFA habilitado para TODOS los usuarios humanos (no opcional)
- ✅ Búsqueda de roles "wildcard" (Admin, *, s3:*, etc.) → estos son risk
- ✅ Verificar credential age: ¿Keys rotadas regularmente (< 90  días)?
- ✅ Identidad usuarios "huérfanos" (ex-empleado, inherited, no se usa)
- ✅ Revisar cross-account access (si aplica): ¿A quién le damos acceso a otra cuenta?)
- ✅ Políticaas de acceso temporal: ¿Cómo reviewamos/revocamos cuando proyecto termina?

**Herramientas recomendadas**:
```bash
# AWS
aws iam list-users --output table | awk '{print $2, $3, $4}'
aws iam list-roles --output json | jq '.Roles[] | {RoleName: .RoleName, Path: .Path}'
aws iam list-attached-user-policies --user-name <username> --output json | jq '.AttachedPolicies'
# Para cada usuario
aws iam get-user --user-name <username>
aws iam list-access-keys --user-name <username>  # Age of keys
aws iam get-credential-report  # Bulk report (monthly)

# Azure
az ad user list --output table
az role assignment list --all --output table
az role assignment list --assignee <user-id> --output json | jq '.[] | {principalName, roleDefinitionName}'

# GCP
gcloud projects get-iam-policy <project-id> --flatten="bindings[].members" --format="table(bindings.role, bindings.members)"
gcloud iam service-accounts list --format="table(email, disabled)"

# Kubernetes
kubectl get serviceaccount --all-namespaces
kubectl get clusterrolebinding --output json | jq '.items[] | {name: .metadata.name, subjects: .subjects, roleRef: .roleRef}'
```

**Errores comunes**:
- ❌ Service accounts compartidos entre múltiples aplicaciones (imposible auditar quién hizo qué)
- ❌ Credenciales nunca rotadas ("key from 2019, still in use")
- ❌ Rol de "admin" dado como default ("just in case we need it")
- ❌ No revisar acceso después de terminar proyecto (ex-vendors, consultants aún tienen keys)

**Evidencia típica**:
```markdown
## IAM Misconfiguration: Overly Permissive Role
- **User**: Developers-group (25 personas)
- **Assigned Role**: Administrator (full AWS access to production account)
- **Justificación**: "necesitan provisionar recursos"
- **Realidad**: Solo 2 personas hacen provisioning; 23 no deberían tener Admin
- **Riesgo**: Cualquiera de los 25 puede borrar bases de datos, exponer secrets, crear backdoors
- **Remediación**: Crear rol específico "Developer-EC2-Deploy" con permisos mínimos; asignar solo a 2 personas
- **Verificación**: Auditar quién realmente accede con qué permisos (CloudTrail)
```

---

### Componente 2: Auditoría de Almacenamiento (Buckets/Blobs)

**Objetivo**: Verificar que archivos sensibles no son públicamente accesibles.

**Información técnica**:
- **Access Control Lists (ACLs)**: Público vs privado vs específica cuenta
- **Bucket Policies**: Quién puede hacer qué (read, write, delete)
- **Block Public Access**: Configuración para prevenir accidentes
- **Encryption**: En reposo (KMS) y en tránsito (HTTPS/TLS)
- **Versioning & MFA Delete**: Protección contra eliminación accidental
- **Logging**: Auditoría de quién accedió qué

**Checklist - Almacenamiento**:
- ✅ Listar todos los buckets/containers y su access level (público, privado, specific IPs)
- ✅ Buscar bucketss con "public read" o "public write" (peligro)
- ✅ Verificar archivos sensibles dentro (backups, logs con credenciales, source code)
- ✅ Revisar bucket policies: ¿Quién tiene acceso? ¿Es justificado?
- ✅ Encryption habilitada (KMS keys, managed by customer preferentemente)
- ✅ Versioning + MFA Delete (protección contra ransomware)
- ✅ Logging habilitado (S3 access logs, Azure blob auditing)
- ✅ Examinar "forgotten" buckets (creados años atrás, no en documentación)

**Herramientas recomendadas**:
```bash
# AWS S3
aws s3api list-buckets --output table
aws s3api get-bucket-acl --bucket <bucket-name>  # Public read/write?
aws s3api get-bucket-public-access-block --bucket <bucket-name>
aws s3api get-bucket-policy --bucket <bucket-name> | jq .
aws s3api get-bucket-encryption --bucket <bucket-name>
aws s3api get-bucket-versioning --bucket <bucket-name>
aws s3api get-bucket-logging --bucket <bucket-name>

# List all objects in bucket (NO DOWNLOAD unless needed)
aws s3 ls s3://<bucket-name>/ --recursive --summarize

# AWS config rules (automated)
aws configservice start-config-rules-evaluation --config-rule-names s3-bucket-public-read-prohibited s3-bucket-public-write-prohibited

# Azure Blob
az storage account list --output table
az storage account blob-service-properties show --account-name <account> --resource-group <rg>
az storage account network-rule list --account-name <account> --resource-group <rg>

# GCP Cloud Storage
gsutil ls -L <bucket-name>  # Listar con detalles
gsutil iam ch <bucket-name>  # Ver permissos
gsutil encryption get <bucket-name>
```

**Errores comunes**:
- ❌ Parámetro default "público" (en algunos casos, sí es default)
- ❌ Bucket con backups + credenciales dentro (acceso público = database leak)
- ❌ Archivos históricos nunca limpiados (años de logs con información sensible)
- ❌ Encryption deshabilitada "por performance" (falsa trade-off)

**Evidencia típica**:
```markdown
## S3 Bucket Públicamente Accesible (Crítico)
- **Bucket**: stg-app-backups
- **Access Level**: PUBLIC READ (open to internet)
- **Contenido**: 15 backups de base de datos (archivos .sql.gz, 200 MB cada uno)
- **Datos expuestos**: 
  - 2M registros de usuarios (nombres, emails, hashes de contraseñas)
  - 5K transacciones de pago (credit card numbers partially masked, but útil)
  - API keys en comentarios de data dumps
- **Impacto**: Puede descargar y extraer sin credenciales
- **Causa Root**: CloudFormation template tenía `PublicReadAccess: true` (copy-paste error)
- **Remediación Inmediata**: 
  - (1) Remover public-read access
  - (2) Habilitar "block public access"
  - (3) Rotar todas las credenciales encontradas
  - (4) Breach notification si datos realmente sensibles
```

---

### Componente 3: Auditoría de Compute (Instancias, Funciones, Pods)

**Objetivo**: Verificación de que instancias & apps no exponen servicios peligrosos y están configuradas mínimamente.

**Information técnica**:
- **Instancia de entrada**: SSH, RDP, serial, debug ports
- **Security Groups / Network Security Groups**: Qué tráfico inbound/outbound allowido
- **MetadataService Exposure**: Instancia puede acceder a credenciales (SSRF risk)
- **IAM Role/Service Account**: Qué permisos tiene la instancia
- **Patching & AMI**: ¿Qué versión SO? ¿Cuándo fue last patched?
- **Secrets Storage**: ¿Cómo accede a credenciales? (usuario texto vs Vault)
- **Container Images**: Base image, vulnerabilidades, secrets in image

**Checklist - Compute**:
- ✅ Listar todas las instancias (EC2, VM, GKE nodes, etc.)
- ✅ Para cada una, revisar security groups: ¿Qué puertos están abiertos? ¿A dónde?
- ✅ Búsqueda de "0.0.0.0/0" en puertos peligrosos (22 SSH, 3389 RDP, 27017 MongoDB, etc.)
- ✅ Verificar IAM role/service account: ¿Qué permisos tiene?
- ✅ Revisar AMI/imagen: ¿Versión oficial? ¿Parcheada? ¿Cómo se creó?
- ✅ Buscar credenciales en userdata scripts (hardcodeadas = bad)
- ✅ Revisar tagging: ¿Está claramente etiquetada como prod/staging/test?
- ✅ Verificar lifecycle: ¿Instancia aún necesaria o es legacy?
- ✅ Para contenedores: ¿Root? ¿Readonly filesystem? ¿Secrets como ENV VAR?

**Herramientas recomendadas**:
```bash
# AWS EC2
aws ec2 describe-instances --output table | grep -E 'InstanceId|SecurityGroups|ImageId|InstanceType'
aws ec2 describe-security-groups --group-ids <sg-id> --output json | jq '.SecurityGroups[].IpPermissions'
# Find "0.0.0.0/0" rules (dangerous)
aws ec2 describe-security-groups --output json | jq '.SecurityGroups[] | select(.IpPermissions[].IpRanges[].CidrIp | select(. == "0.0.0.0/0" or . == "::/0"))'

# Check IAM role
aws ec2 describe-instances --instance-ids <id> --query 'Reservations[].Instances[].IamInstanceProfile'
aws iam get-role-policy --role-name <role-name> --policy-name <policy-name>

# Azure VMs
az vm list --output table
az network nsg rule list --resource-group <rg> --nsg-name <nsg-name> --output table

# GCP Instances
gcloud compute instances list --format="table(name, zone, machine_type, status, INTERNAL_IP, EXTERNAL_IP)"
gcloud compute firewall-rules list --format="table(name, direction, sourceRanges, targetTags, allowed)"

# Kubernetes (contenedores)
kubectl get pods --all-namespaces --output wide
kubectl get pod <pod-name> -o jsonpath='{.spec.securityContext}'  # RunAsRoot, etc.
kubectl exec <pod-name>-- env | grep -i "password\|secret\|key"  # secrets como ENV (bad)
```

**Errores comunes**:
- ❌ SSH abierto a "0.0.0.0" ("We're in private network so it's OK" ← nope, lateral movement risk)
- ❌ Metadata service muy permisivo (SSRF puede obtener credenciales)
- ❌ Instancia con rol "Admin" cuando solo necesita "read logs"
- ❌ Userdata script con contraseñas en claro
- ❌ Contenedor corriendo como root (compromiso = full container)

**Evidencia típica**:
```markdown
## Security Group Misconfiguration: SSH Publicly Exposed
- **EC2 Instance**: prod-db-primary-1
- **Security Group**: prod-internal-sg
- **Inbound Rule**: Port 22 (SSH), CIDR 0.0.0.0/0 (anyone on internet)
- **Justificación**: "For emergency access" (desde DevOps)
- **Riesgo**: Brute-force SSH, credential stuffing, direct access a database server
- **Verificación**: Revisé security group; regla está activa; SSH servicio responding
- **Impacto**: Si credenciales débiles → full database compromise
- **Remediación**: 
  - (1) Cambiar SSH rule a VPN subnet only
  - (2) Usar SSM Session Manager o bastion host
  - (3) Deshabilitar password auth (keys only)
  - (4) Revisar audit logs por acceso SSH no autorizado
```

---

### Componente 4: Auditoría de Contenedores e Imágenes

**Objetivo**: Verificar que imágenes están sin vulnerabilidades conocidas y no contienen secrets.

**Information técnica**:
- **Base Images**: ¿Usas oficial image (ubuntu, node, python) o custom?
- **Vulnerabilidades**: Análisis de CVEnumerator/ CVSS scores
- **Secrets in Image**: Hardcoded API keys, contraseñas, certificados
- **Permissions**: ¿Corre como root? (90% no necesitan)
- **Network Context**: ¿Puede conectarse a internet? ¿Es necessary?
- **Filesystem**: ¿Read-only posible? (hermetic execution)

**Checklist - Contenedores**:
- ✅ Listar todos los registros (Docker Hub, ECR, GCR, ACR)
- ✅ Para cada imagen, ejecutar vulnerability scanner (Trivy, Grype, Clair, etc.)
- ✅ Revisar Dockerfile: ¿Base image tiene vulnerabilidades? ¿Secrets hardcodeados?
- ✅ Verificar: ¿Corre como root? (use baseado en uid no-root)
- ✅ Buscar: ENV variables con secrets (move a Secret object in k8s)
- ✅ Verificar: ¿Filesystem readonly? ¿Capabilities mínimas?
- ✅ Examinar image layers: `docker history <image>` para ver quién lo cre y cambios

**Herramientas recomendadas**:
```bash
# Scanning local images
trivy image alpine:3.18  # Rápido, muestra CVEs
grype alpine:3.18        # Similar, diferente formato
docker scan alpine:3.18  # Docker nativo

# Scanning en registry (ECR, GCR, etc.)
trivy image --registry-username <user> --registry-password <pass> <registry>/<image>:<tag>

# Dockerfile análisis
hadolint Dockerfile  # Comunes errores en Dockerfile
dive <image>:<tag>   # Inspeccionar capas, tamaño, archivos

# Buscar secrets en imagen  
strings <image-tar> | grep -i "password\|api_key\|secret"
docker history <image> | grep -i "password\|secret\|key"

# Descargar y buscar en image
docker save <image>:<tag> | tar -x
find . -name "*.env" -o -name "secrets.yml" -o -name ".aws/credentials"

# Verificar credenciales en ECR (AWS)
aws ecr describe-images --repository-name <repo> --image-ids imageTag=<tag> --output json | jq
```

**Errores comunes**:
- ❌ Base image vieja (ubuntu:14.04 con 100+ CVEs)
- ❌ Hardcodeado credenciales en Dockerfile (COPY .env file o ENV PASSWORD=xxx)
- ❌ Multi-stage build no usado (resultando image gig grandes con herramientas innecesarias)
- ❌ No scanning de dependencias (npm, pip, maven con vulnerabilities)
- ❌ Corriendo como root (USER root o ausencia de USER directive)

**Evidencia típica**:
```markdown
## Contenedor con secretos hardcodeados
- **Imagen**: myapp:v1.2.3 (en ECR)
- **Dockerfile**: RUN echo "API_KEY=abc-def-123 > /etc/config.env
- **Problema**: Secret visible en image history
- **Descubrimiento**: docker history myapp:v1.2.3 muestra el comando
- **Extracción**: docker save + tar + grep find la clave
- **Impacto**: Cualquiera con acceso image tiene credencial
- **Remediación**: 
  - (1) Usar build args + secret mounts (Docker buildkit)
  - (2) Rotar clave
  - (3) Implementar CI/CD scanning (prevent commits sin secrets)
  - (4) Use HashiCorp Vault o AWS Secrets Manager en runtime
```

---

### Componente 5: Auditoría de Kubernetes & Orquestación

**Objetivo**: Verificar Kubernetes manifests, RBAC, network policies, y seguridad general del cluster.

**Information técnica**:
- **API Server**: ¿Públicamente accesible? (debería estar restricted)
- **RBAC**: Role-based access control; quién puede hacer qué
- **Pod Security Policies/Standards**: Restricciones en qué pods pueden iniciar
- **Network Policies**: Microsegmentación de tráfico entre pods
- **Secrets Management**: Cómo se almacenan credenciales
- **Logging & Auditing**: ¿Qué eventos se loggean?
- **Admission Controllers**: Validación/mutación de manifests antes de deploy

**Checklist - Kubernetes**:
- ✅ Verificar Kuberenetes API server: ¿Públicamente accesible? (grep por "6443")
- ✅ Listar service accounts: ¿Todos son necesarios? (default es muy permisivo)
- ✅ Revisar RBAC: `kubectl get clusterroles, rolebindings` → detectar wildcards
- ✅ Buscar privileged pods (`securityContext.privileged: true`)
- ✅ Revisar runAsRoot: ¿Hay pods corriendo como root?
- ✅ Network policies: ¿Existen? (si no, todo pod puede hablar con todo)
- ✅ Secrets cifrados: ¿Están en reposo (etcd encryption) o solo en tránsito?
- ✅ Revisar Helm charts: ¿Hay defaults peligrosos?
- ✅ Examinar service types: ¿LoadBalancer directamente acesible? (debería ser internal)
- ✅ Auditing: ¿Kubernetes audit logs habilitados?

**Herramientas recomendadas**:
```bash
# Reconocimiento Kubernetes
kubectl cluster-info
kubectl api-resources
kubectl get nodes --show-labels

# RBAC
kubectl get clusterroles --all-namespaces
kubectl get clusterrolebindings | grep -v system:
kubectl get roles --all-namespaces
kubectl get rolebindings --all-namespaces
# Verificar quién puede hacer qué
kubectl auth can-i create pods --as=system:serviceaccount:default:default
kubectl auth can-i delete deployments --as=system:serviceaccount:prod:analyzer

# Pods
kubectl get pods --all-namespaces -o wide
kubectl get pods --all-namespaces -o json | jq '.items[] | {name: .metadata.name, privileged: .spec.containers[].securityContext.privileged, runAsRoot: .spec.containers[].securityContext.runAsUser}'

#Secrets (encrypted?)
kubectl get secret -A
kubectl get secret <name> -o jsonpath='{.data}' | base64 -d  # DECODE (cuidado!)

# Network Policies
kubectl get networkpolicies --all-namespaces
kubectl describe networkpolicy <policy-name>

# Security checks (automated tools)
kubesec scan pod.yaml
kubebench  # CIS Kubernetes Benchmark
kube-score score deployment.yaml
polaris audit  # comprehensive


# Auditing
kubectl logs -n kube-system -l component=audit  # Si existe
# Or check audit logs on master: /var/log/kubernetes/audit.log (si es self-hosted)
```

**Errores comunes**:
- ❌ Kubernetes API abierto a "0.0.0.0" (cualquiera puede administrar cluster)
- ❌ Rol "ClusterAdmin" otorgado como default
- ❌ Secrets almacenados sin encripción (etcd sin encryption)
- ❌ Pods privilegiados que no necesitan (corre como root, monta host filesystem)
- ❌ Sin network policies (segmentación 0)
- ❌ Service type LoadBalancer permanentemente (debería ser Internal o Ingress)

**Evidencia típica**:
```markdown
## Kubernetes RBAC Overly Permissiv

e
- **Service Account**: scanner (namespace: security-tools)
- **Roles Assigned**: ClusterAdmin (via clusterrolebinding)
- **Justificación**: "Necesita acceso a todos los recursos"
- **Realidad**: Solo necesita `get/list pods, get services, exec into pods`
- **Riesgo**: Si app compromised, attacker tiene acceso total a cluster
- **Remediación**:
  - (1) Crear custom Role con solo get/list/exec
  - (2) RoleBinding específico al service account
  - (3) Verificar: kubectl auth can-i delete nodes --as=system:serviceaccount:security-tools:scanner
```

---

## SECCIÓN 3: METODOLOGÍA Cloud Audit Paso a Paso

### Paso 1: Acceso y Reconocimiento (30 min)

```bash
# Verificar acceso a cloud accounts
aws sts get-caller-identity  # AWS
az account show  # Azure
gcloud config list  # GCP

# Identificar accounts/projects/subscriptions
aws ec2 describe-regions --query 'Regions[].RegionName' --output table
az account list --output table
gcloud projects list

# Preparar documento: Account audit scope
```

### Paso 2: Auditoría IAM (1-2 horas)

```bash
# Obtener credential report completo
aws iam get-credential-report  # genera CSV
# Analyza: Password last changed, Access key age, MFA, etc.

# Listar todos los usuarios y acceso
aws iam list-users --query 'Users[].[UserName, CreateDate]' --output table
aws iam list-roles --query 'Roles[].[RoleName, CreateDate]' --output table

# Para cada usuario/rol, revisar policies
aws iam list-attached-user-policies --user-name <username>
aws iam list-user-policies --user-name <username>
```

### Paso 3: Auditoría Almacenamiento (1-2 horas)

```bash
# Listar buckets
aws s3 ls

# Para cada bucket
aws s3api get-bucket-acl --bucket <bucket> | grep "Grant" 
aws s3api get-bucket-public-access-block --bucket <bucket>

# Revisar contenido si es público (cuidado legal!)
aws s3 ls s3://<bucket> --recursive --summarize
```

### Paso 4: Auditoría Compute & Contenedores (1-2 horas)

```bash
# Instancias
aws ec2 describe-instances --output json | jq '.Reservations[].Instances[]'

# Imágenes en registry
aws ecr describe-images --repository-name <repo>

# Scan imágenes
trivy image --severity CRITICAL <image>
```

### Paso 5: Auditoría Kubernetes (1-2 horas)

```bash
# Configuración general
kubectl cluster-info
kubectl get nodes -o wide
kubectl top nodes

# RBAC audit
kubectl get clusterrolebindings -o wide | grep -v "system:"
```

### Paso 6: Reporteo (1-2 horas)

---

## SECCIÓN 4: CASOS DE ESTUDIO REALES

### Caso 1: AWS Default VPC + No Firewall = Public Database (Crítico)

**Contexto**:
Startup utilizó AWS default VPC y no aplicó security groups. Base de dados PostgreSQL creada sin especificar security group customizado.

**Descubrimiento**:
```bash
aws rds describe-db-instances | grep Endpoint, VpcSecurityGroups
# → vpc-123456 (default), security group: default
aws ec2 describe-security-groups --group-ids sg-default | grep IpPermissions
# → No inbound rules = default allow all from same security group only
# BUT default security group has... everyone on network?
```

**Problema Root**:
- Default security group en default VPC hereda comportamiento:
  - Inbound: Solo desde mismo security group
  - Outbound: A cualquier lugar
- PERO database accesible vía AWS RDS endpoint (DNS público) desde internet
- Attacker puede hacer: `nmap -p5432 172.x.x.x` desde casa, intenta acceso

**Cadena de Ataque**:
1. Shodan buscar PostgreSQL expuesto: `"AWS RDS"`
2. Encontrar endpoint público de database
3. Intentar default credentials: postgres/postgres
4. Acceso a toda base de datos (millones de registros)

**Impacto**:
- 5M registros de usuarios (emails, nombres, direcciones)
- 50K credenciales (hashes, pero algunos crackables)
- PII exposure → GDPR fine, lawsuits, reputacional damage

**Prevención**:
```bash
# Correct: RDS en VPC private subnet, securidad group restrictivo
aws rds create-db-instance \
  --db-instance-identifier mydb \
  --db-subnet-group-name <private-subnet-group> \
  --vpc-security-group-ids sg-<custom-restrict> \
  --publicly_accessible false  # Never true for production

# Security group should only allow from app tier
aws ec2 authorize-security-group-ingress \
  --group-id sg-<custom> \
  --protocol tcp \
  --port 5432 \
  --source-security-group-id sg-<app-tier>
```

---

### Caso 2: Container Image with Hardcoded API Key (Crítico)

**Contexto**:
Desarrollador agregó API key a `.env.example` en repositorio, luego incluido en Dockerfile.

**Descubrimiento**:
```bash
# Dockerfile contiene
COPY .env /app/.env

# Durante container build
docker inspect <image>:<tag> | jq '.Config.Env'
# Encuentra: API_KEY=sk_live_abc123xyz

# O via docker history
docker history <image> | grep COPY
docker save <image> | tar -x && find . -name ".env" -exec cat {} \;
```

**Problema Root**:
- `.env` archivos nunca deberían commiterse
- Si committed, `.gitignore` debería prevenir
- Si in Dockerfile, COPY statement lo hardcodea en image layer

**Cadena de Ataque**:
1. Attacker obtiene container image (leak, registró público, theft)
2. Extrae layer con API key
3. Usa API key contra terceros (payment processor, cloud service, etc.)
4. Bills $50K antes de detectar

**Impacto**:
- Unexpected charges
- Malicious API calls (DoS, data exfiltration)
- Breach discovery delayed (no logs correlating key)

**Prevención**:
```bash
# Multi-stage build (secretos NO end up en final image)
FROM node:18 as builder
COPY . /src
RUN npm ci

FROM node:18-alpine
COPY --from=builder /src/node_modules /app/node_modules
COPY --from=builder /src/dist /app/dist
# Nota: secretos NO copiados

# Secretos en runtime via environment variables
# (passed by orchestrator, not in image)
```

---

### Caso 3: Kubernetes RBAC Too Loose = Lateral Movement (Alto)

**Contexto**:
Equipo de DevOps creó genérico service account para CI/CD con amplio acceso a "todos los recursos" para "simplificar".

**Descubrimiento**:
```bash
kubectl get clusterrolebindings | grep ci-cd
# → Result: ci-cd-sa → clusterrole: admin

kubectl auth can-i delete nodes --as=system:serviceaccount:kube-system:ci-cd
# → Yes
kubectl auth can-i delete secrets --as=system:serviceaccount:kube-system:ci-cd
# → Yes (BAD! secrets contienen credenciales)
```

**Problema Root**:
- Service account con ClusterAdmin
- SI una app en uno de los pods es compromised, attacker tiene cluster access
- Puede crear backdoor pods, exfiltrate credentials, delete audition logs

**Cadena de Ataque**:
1. Attacker entitles web app vulnerability
2. Executes code en pod con service account CI-CD
3. Lee `/var/run/secrets/kubernetes.io/serviceaccount/token` (automáticamente mounted)
4. Usa token para acceso API (kubectl API calls) desde pod
5. Ejecuta: `kubectl get secrets --all-namespaces` → obtiene credenciales guardadas
6. Escala acceso a otros clusters (some companies federan clusters)

**Impacto**:
- Full cluster compromise
- Lateral movement a otros systems
- Data exfiltration

**Remediación**:
```bash
# Role specific para CI/CD
kubectl create role ci-cd-role \
  --verb=get,list,create,update,patch \
  --resource=deployments,services,configmaps

# RoleBinding a namespace específico
kubectl create rolebinding ci-cd-binding \
  --role=ci-cd-role \
  --serviceaccount=default:ci-cd \
  --namespace=production

# Verify
kubectl auth can-i delete secrets --as=system:serviceaccount:default:ci-cd --namespace=prod
# → No (esperado)
```

---

## SECCIÓN 5: TEMPLATES Y CHECKLISTS

### Template 1: Cloud Security Assessment Checklist

```markdown
# Cloud Security Assessment Checklist

## Pre-Engagement
- [ ] Cloud providers identificados (AWS, Azure, GCP, hybrid)
- [ ] Scope definido: "Audit all accounts or specific teams?"
- [ ] Acceso concedido (read-only roles)
- [ ] Documentación de arquitectura disponible
- [ ] Contacto técnico identificado

## IAM Audit (Target: 2-4 horas)
- [ ] Listar todos los usuarios humanos (Active Directory integration?)
- [ ] Listar todos los service accounts (aplicaciones, CI/CD, herramientas)
- [ ] Para cada usuario/service account:
  - [ ] Roles y políticas asignadas
  - [ ] Credencial age (último cambio)
  - [ ] MFA status (si es humano)
  - [ ] Último acceso registrado (si available)
- [ ] Buscar roles "wildcard" o "admin"
- [ ] Revisar cross-account access (si aplica)
- [ ] Documentar anomalías (huérfanos, unused, excessively powerful)

## Almacenamiento Audit (Target: 2-4 horas)
- [ ] Listar todos los buckets/containers
- [ ] Para cada:
  - [ ] Access level (public/private)
  - [ ] Encryption status
  - [ ] Versioning + MFA Delete (si disponible)
  - [ ] Logging habilitado
  - [ ] Contenido muestreado (qué clase de data)
- [ ] Buscar buckets públicos (potencial leak)
- [ ] Revisar storage lifecycle policies (data retention, deletion)

## Compute Audit (Target: 2-4 horas)
- [ ] Listar todas las instancias
- [ ] Para cada:
  - [ ] Security groups/NSGs revisados
  - [ ] Inbound rules para puertos peligrosos
  - [ ] IAM role asignado
  - [ ] OS version y parches
  - [ ] Servicios corriendo (ssh, rdp, debug, etc.)
- [ ] Buscar "0.0.0.0/0" en reglas críticas
- [ ] Revisar startup/userdata scripts (secrets hardcodeados?)

## Container/Image Audit (Target: 2-4 horas)
- [ ] Listar todos los registries
- [ ] Para cada imagen significativa:
  - [ ] Ejecutar scanner de vulnerabilidades (Trivy, Grype)
  - [ ] Revisar historicos de capas
  - [ ] Buscar secrets (hardcodeados credenciales, API keys)
  - [ ] Base image version (old = vulnerable)
- [ ] Revisar Dockerfiles en repos (mala práctica)

## Kubernetes/Orquestación Audit (Target: 3-5 horas)
- [ ] Cluster info (versión, tamaño, nodos)
- [ ] API server accessibility
- [ ] RBAC: Listar clusterroles/rolebindings sin "system:"
- [ ] Buscar privileged pods
- [ ] Network policies revisado (existen?)
- [ ] Secrets management (encryptado?)
- [ ] Logging/auditing (habilitado?)
- [ ] Admission controllers (qué validaciones existen?)

## Post-Audit (Target: 2-4 horas)
- [ ] Compilar hallazgos en tabla master
- [ ] Priorizar por severidad
- [ ] Obtener confirmación de cliente (falsos positivos?)
- [ ] Documentar remediaciones recomendadas
- [ ] Tiempo estimado para fix cada hallazgo
```

### Template 2: Cloud Security Report

```markdown
# Cloud Security Assessment Report

## Executive Summary
**Assessment Period**: Dec 15 - Dec 22, 2024  
**Scope**: AWS Production/Staging, GCP sandbox  
**Findings**: 3 Critical, 5 High, 7 Medium, 12 Low  
**Rating**: 4.2/10 (below industry average for cloud-native organizations)

---

## Critical Findings

### #1: RDS Instance Publicly Accessible (Severity: Critical)
- **Asset**: prod-database-primary (us-east-1)
- **Issue**: Security group allows 0.0.0.0/0 inbound on port 5432
- **Evidence**: `aws ec2 describe-security-groups --group-id sg-xxx | grep "IpPermissions"`
- **Impact**: Unauthenticated access to production database (2M customer records exposed)
- **Remediation**: Immediately restrict SG to app tier private subnet only
- **Timeline**: URGENT (within 24 hours)

### #2: S3 Bucket Publicly Readable with Backups (Severity: Critical)
- **Asset**: stg-database-backups (us-west-2)
- **Issue**: ACL set to public-read; contains unencrypted database backup
- **Evidence**: `aws s3api get-bucket-acl --bucket stg-database-backups`
- **Impact**: Unauthorized download of 50K customer credentials
- **Remediation**: Block public access, enable encryption, rotate all exposed credentials
- **Timeline**: URGENT (within 12 hours)

---

## High Findings
### #3: Overly Permissive IAM Role (Severity: High)
[Details...]

### #4: Docker Image with Hardcoded API Key (Severity: High)
[Details...]

---

## Recommendations Summary
| Priority | Category | Count |
|----------|----------|-------|
| Critical | Immediate Fix (24 hrs) | 2 |
| High | This Week | 5 |
| Medium | This Month | 7 |
| Low | Backlog | 12 |
```

### Template 3: Remediation Checklist

```markdown
# Remediation Tracking

## Critical Findings Remediation

### Finding #1: RDS Public Access
- [ ] Update security group: Remove 0.0.0.0/0
- [ ] Add rule: Allow only from app tier (10.0.1.0/24)
- [ ] Test: Verify connection from app tier; verify denied from internet
- [ ] Audit logs: Review CloudTrail for unauthorized access attempts
- [ ] Timeline:Changed by: [Name], Date: [Date] ✅

### Finding #2: S3 Bucket Public
- [ ] Block all public access
- [ ] Update bucket policy: Remove public statements
- [ ] Enable encryption (KMS)
- [ ] Rotate ALL exposed credentials
- [ ] Notify security team (breach notification?)
- [ ] Timeline: Completed by: [Name], Date: [Date] ✅
```

---

## CONCLUSIÓN

Cloud-native security es **fundamentalmente diferente** de on-prem:
- **Responsabilidad compartida**: Provider gestiona nube; tú gestionas apps
- **Automatización = Consistencia**: IaC + scanning automático > reviews manuales
- **Identidad es nuevo perimetro**: Millones de service accounts, cada uno con permisos
- **Secretos en código = breach automático**: Nunca hardcodees
- **Logging todo o segarás ciego**

**Patrones clave**:
✅ Deny by default → Allow specific  
✅ Rotate credentials < 90 días  
✅ MFA para humans, encryption for data  
✅ Scan imágenes, audit roles, monitor acceso  
✅ IaC + linting automático = menos errores
