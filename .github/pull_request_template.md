## O que esse PR faz?

Fale sobre o propósito do pull request, como por exemplo: quais problemas ele soluciona ou quais features ele adiciona.

## Onde a revisão poderia começar?

Indique o caminho do arquivo e o arquivo onde o revisor deve iniciar a leitura do código.

## Como este poderia ser testado manualmente?

Estabeleça os passos necessários para que a funcionalidade seja testada manualmente pelo revisor.

## Algum cenário de contexto que queira dar?

Indique um contexto onde as modificações se fazem necessárias ou passe informações que contextualizam o revisor a fim de facilitar o entendimento da funcionalidade.

## Screenshots

Quando aplicável e se fizer possível, adicione screenshots que remetem à situação gráfica do problema que o pull request resolve.

## Quais são os tickets relevantes?

Indique uma issue à qual o pull request faz relacionamento.

## Referências

Indique as referências utilizadas para a elaboração do pull request.

---

## Segurança da informação (NSI.04)

> Seção obrigatória. Marque as opções aplicáveis e justifique quando necessário. Referência: NSI.04 - Norma de Desenvolvimento Seguro.

**Este PR manipula dados sensíveis ou pessoais (LGPD)?**
- [ ] Sim — descreva os controles de proteção aplicados (criptografia, mascaramento, anonimização, etc.):
- [ ] Não

**Este PR altera autenticação, autorização, controle de acesso ou gerenciamento de sessão?**
- [ ] Sim — descreva o que mudou e por quê:
- [ ] Não

**Este PR introduz, atualiza ou remove dependências de terceiros?**
- [ ] Sim — as novas dependências foram verificadas no SBOM/Trivy sem vulnerabilidades críticas/altas em aberto?
  - [ ] Verificado e aprovado
  - [ ] Pendente / vulnerabilidade aceita com justificativa: 
- [ ] Não

**Este PR foi validado pelo pipeline de segurança (SonarQube / Trivy)?**
- [ ] Sim — link do job:
- [ ] Não aplicável a este PR (justifique):

**Este PR concatena, monta ou executa comandos SQL, HTML ou JavaScript a partir de entrada externa?**
- [ ] Sim — confirme que há sanitização/parametrização (prepared statements, escaping, etc.):
- [ ] Não

**Este PR expõe novos endpoints, telas ou serviços?**
- [ ] Sim — HTTPS obrigatório está garantido e o acesso segue o princípio de menor privilégio?
- [ ] Não

**Algum segredo, senha, chave ou token está sendo adicionado ao código-fonte?**
- [ ] Não, nenhum segredo foi commitado
- [ ] Sim (bloquear merge e corrigir antes de prosseguir)