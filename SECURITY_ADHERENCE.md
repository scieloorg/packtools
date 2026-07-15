# Aderência à Segurança da Informação

Este documento declara como este repositório atende às diretrizes da **NSI.04 – Norma de Desenvolvimento Seguro** (SciELO/FapUNIFESP), alinhada à NBR ISO/IEC 27.001:2022 e à LGPD.

> Preencher e manter atualizado a cada mudança relevante de arquitetura, dependências críticas ou classificação de dados. Revisar no mínimo a cada release maior.

## 1. Identificação

| Campo | Valor |
|---|---|
| Nome do sistema | packtools (scielo.packtools) |
| Responsável técnico | Luciano Rossi |
| Classificação da informação tratada | Pública |
| Dados pessoais tratados (LGPD)? | Sim — nomes e afiliações de autores, presentes nos metadados do XML do artigo. É dado já público (consta no artigo publicado); a biblioteca não coleta nem armazena dado pessoal por conta própria |
| Ambiente de produção | N/A — distribuído como biblioteca Python (PyPI/GitHub release), executada dentro do ambiente de cada sistema consumidor (ex.: SPS Validator, Core, Upload) |

## 2. Controles de segurança aplicados (NSI.04 §3)

- [ ] Segregação entre ambientes de dev, teste e produção (§3.1) — N/A: biblioteca sem ambiente de implantação próprio
- [ ] Controle de acesso ao banco de dados com permissões mínimas necessárias, sem uso de usuário root (§3.2) — N/A: não possui banco de dados
- [x] Senhas e segredos gerenciados fora do código-fonte (§3.3) — nenhum segredo é usado pela biblioteca; commits são verificados pelo GitGuardian a cada PR
- [x] Comunicação via HTTPS/TLS em todas as interfaces expostas (§3.4) — chamadas HTTP feitas por `packtools.sps.libs.requester.fetch_data` usam `verify=True` por padrão (validação de certificado TLS)
- [x] Prevenção a SQL Injection, XSS e quebra de autenticação/sessão (§3.5) — não há SQL (sem banco de dados); parsing de XML usa `lxml.etree.XMLParser(no_network=True)` por padrão, bloqueando resolução de DTD/entidades externas via rede; geração de HTML (`HTMLGenerator`) usa transformação XSLT, sem concatenação manual de strings
- [ ] Logs de auditoria implementados conforme criticidade do sistema (§3.6) — não aplicável no nível de biblioteca; uso de `logging` padrão do Python para diagnóstico, não para auditoria
- [ ] Procedimento de backup e teste de restauração definido (§3.7) — N/A: não persiste dados
- [ ] Dados sensíveis criptografados em trânsito e em repouso, sem algoritmos obsoletos (MD5, SHA1, DES/3DES, RC2/RC4, MD4) (§3.8) — N/A: não armazena nem criptografa dados; responsabilidade do sistema consumidor

## 3. Pipeline de CI/CD e verificação automatizada

| Ferramenta | Finalidade | Gate obrigatório? |
|---|---|---|
| GitGuardian | Detecção de segredos commitados | Sim |
| Snyk (security/snyk) | Vulnerabilidades em dependências | Sim |
| CodeQL | SAST (análise estática) | Não — executa via GitHub code scanning, não aparece como check obrigatório de PR |
| SonarQube | Qualidade de código e SAST | Não configurado |
| Trivy / SBOM | Vulnerabilidades de imagem de container / inventário de dependências | Não aplicável — não há imagem de container (biblioteca, não serviço) |
| ArgoCD | Deploy controlado em homologação/produção | Não aplicável — sem deploy próprio |

Critério de aprovação do gate: GitGuardian e Snyk devem passar (status "pass") antes do merge; sem vulnerabilidade crítica/alta em dependências sem exceção documentada.

## 4. Ciclo de vida (NSI.04 §4)

- [x] Requisitos de segurança levantados junto às partes interessadas (§4.1) — via issues/PRs no GitHub
- [ ] Riscos de segurança avaliados no planejamento (§4.2) — avaliação pontual, não formalizada por processo
- [ ] Separação de ambientes validada na análise (§4.3) — N/A: sem ambientes de implantação
- [x] Revisão de código por membro qualificado antes do merge (§4.4) — revisão obrigatória de PR, com apoio de Copilot code review
- [x] Testes com dados fictícios/anonimizados, ambiente de teste isolado (§4.5) — suíte de testes usa pacotes/XML de amostra sintéticos (`tests/fixtures`), sem dado pessoal real
- [ ] Plano de implantação com procedimento de rollback (§4.6) — N/A: distribuição via release/tag no GitHub, rollback = fixar versão anterior
- [x] Processo de manutenção com aplicação de patches e gestão de mudanças — GMUD (§4.7) — dependências monitoradas pelo Snyk; releases versionadas via tags GitHub

## 5. Desenvolvimento terceirizado (se aplicável, NSI.04 §6)

Aplicável — o responsável técnico atua como colaborador terceirizado.

- [x] Contrato prevê cláusulas de confidencialidade e propriedade intelectual
- [ ] Acesso do terceiro limitado ao estritamente necessário — permissão atual no GitHub é `write` no repositório completo (`scieloorg/packtools`), não escopada a uma área específica; não configura acesso mínimo estrito
- [x] Revisões de código e auditorias técnicas realizadas — todo PR passa por revisão obrigatória e pelos checks automatizados (GitGuardian, Snyk), independentemente de quem contribui

## 6. Exceções e riscos aceitos

Registrar aqui qualquer desvio das diretrizes acima, com justificativa técnica, aprovação e prazo de mitigação, conforme previsto na NSI.04 (seção 3, introdução).

| Desvio | Justificativa | Aprovado por | Prazo de mitigação |
|---|---|---|---|
| Nem todo parsing de XML do repositório força `no_network=True`/`resolve_entities=False` explicitamente (ex.: `pid_provider/xml_loader.py`) | Levantado durante este preenchimento; não foi auditado/aceito formalmente ainda | *(pendente)* | *(pendente — recomenda-se revisão)* |
| Colaborador terceirizado com permissão `write` no repositório completo, em vez de acesso escopado ao estritamente necessário | Modelo de colaboração atual do projeto (GitHub write access a colaboradores externos); mitigado por revisão obrigatória de PR e checks automatizados (GitGuardian, Snyk) | *(pendente)* | *(pendente — avaliar redução de escopo ou aceite formal do risco)* |

## 7. Histórico

| Data | Alteração | Responsável |
|---|---|---|
| 2026-07-15 | Criação do documento (adoção do padrão NSI.04) | Luciano Rossi |

---
*Referência normativa: NSI.04 - Norma de Desenvolvimento Seguro, v3.2 (07/07/2025).*