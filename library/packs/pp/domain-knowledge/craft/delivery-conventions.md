# delivery-conventions — Convenções de Entrega da Equipa (Power Platform)

<!--
provenance: RUNTIME (domain knowledge) · class: CRAFT
authored: 2026-09-04 (Step 4B) · design authority: Step 4A — Domain Knowledge Runtime Model
Not an Options D3 pull target.
-->

Prática de engagement e de entrega. Sem autoridade própria de investigação. Este ficheiro não pode afirmar
como facto um limite de plataforma, um limiar ou uma comparação; onde isso for necessário, remete para a
unidade RESEARCH que é dona da matéria — em particular `alm/release-and-lifecycle.md` (solutions, pipelines,
promoção entre ambientes) e `governance/governance-and-environments.md` (ambientes, DLP, políticas de
tenant).

**Status:** defaults sensatos — **ajustar à prática da equipa** (secções marcadas `TODO(team)` esperam
captura na retro do pilot).
**Natureza do que está aqui:** Convenção da equipa, não limite de plataforma: é uma **proposta explícita e substituível** — o engagement pode adoptar outra, e a que adoptar fica registada com a sua razão. Onde uma linha diz «sempre», o que a activa é um
**requisito técnico** nomeado ao lado; sem requisito, é proposta com o seu custo, nunca obrigação.
**Consultado por:** `implementation-spec` e `claude-design-brief` (build-time), `aisa-blueprint` (naming),
camada de traceability (stamping).
**Elegibilidade:** Options + Decision + build (nunca Discovery/Framing).

---

## 1. Naming

| Artefacto | Convenção | Exemplo |
|---|---|---|
| Solution | `<Org>_<Domínio>_<App>` (publisher prefix próprio da org) | `Galp_Procurement_AdvanceApprovals` |
| Canvas App | `[<Domínio>] <Nome funcional>` | `[Procurement] Advance Approvals` |
| Cloud flow | `FLW-<Entidade>-<Ação>` | `FLW-AdvanceRequest-NotifyApprover` |
| Tabela Dataverse | prefixo do publisher + singular PascalCase | `galp_AdvanceRequest` |
| Lista SharePoint | PascalCase singular, sem espaços | `AdvanceRequest` |
| Environment variables | `env_<Área>_<Nome>` | `env_SAP_BaseUrl` |
| Screens / controls / variáveis Power FX | ver `screen-consolidation-rules.md` (screens) e `powerfx.md` (var/gbl/col/err) | `AdvanceRequestListScreen`, `varSelectedRequest` |

`TODO(team)`: confirmar publisher prefix e idioma dos display names (PT vs EN).

## 2. Traceability stamping

**Regra:** todo o componente criado a partir de um implementation-spec/blueprint aisa carrega os ids de
origem na sua **description**:

```
su: C-014, D-002 | bp: v02/PricingRequestListScreen
```

- Tabelas e colunas Dataverse → campo Description.
- Screens Canvas → comentário no OnVisible ou App description por screen (índice).
- Flows → campo Description do flow.
- A linha `su:` é machine-parseable: é a join key para o diff futuro spec-vs-implementação ("que requisitos
  ainda não estão implementados?" torna-se um scan da solution).

`TODO(team)`: confirmar que campos de description sobrevivem ao processo de export/import usado no
engagement — se algum não sobreviver, o stamping desse tipo de componente muda de sítio.

## 3. Environments e ALM

- Estratégia mínima: `DEV → UAT → PROD`; solutions **unmanaged em DEV, managed em UAT/PROD**.
- Deploy só por pipeline ou export/import documentado — nunca edição direta em PROD.
- Connection references sempre (nunca connections embutidas); ownership por **service account**, nunca
  conta pessoal.
- Configuração por environment variable — nunca valores hardcoded no flow ou no app.
- O que a plataforma permite ou exige nesta matéria (tipos de solution, pipelines, dependências, promoção)
  é de `alm/release-and-lifecycle.md`; políticas de tenant e de environment são de
  `governance/governance-and-environments.md`. As linhas acima são a *convenção da equipa*.
- `TODO(team)`: nomes reais dos environments, quem aprova deploy para PROD, janela de deploy.

## 4. Segurança e dados

- RBAC conforme `security-craft.md`: a matriz ecrã × entidade×CRUD entra no implementation-spec **onde o
  alvo tem papéis distintos com acessos distintos**; onde há um só perfil, o spec di-lo e não gera matriz.
  Cada célula sai de um requisito (`security-craft.md` § enquadramento), e a imposição é do lado dos
  dados/API — esconder ecrã não satisfaz autorização.
- Auditoria: onde um requisito cobre a acção (regulador, contrato, política, ou o próprio processo a ler o
  histórico), os eventos levam padrão de audit (`powerfx.md` §3.5 e `security-craft.md` § audit patterns),
  com o requisito citado. Sem requisito que a cubra, a trilha é proposta com o seu custo — não default.
- Dados de teste em DEV/UAT: **anonimizados** onde os dados são pessoais, financeiros ou confidenciais
  (`anonymization.md` classifica). Dados reais de PROD fora de PROD é o piso que não se negoceia — esse não
  espera requisito, porque o requisito é a classificação que os dados já têm.
- Que controlos existem e onde são efetivamente aplicados: `security/security-controls.md`.

## 5. Go-live checklist

1. Política de DLP do environment verificada contra os connectors usados (regras e âmbito:
   `governance/governance-and-environments.md`).
2. RBAC testado por role real (não só o maker).
3. Comportamento de query testado com volume realista (≥ volume esperado do 1.º ano). O que é ou não
   delegável, e a partir de onde, é de `data/query-and-delegation.md` — testar contra o dono, não contra
   memória.
4. Flows com error-handling + owner em service account + alertas de run configurados
   (`flow-craft.md` §3).
5. Descriptions com stamping `su:` presentes (secção 2) — amostragem de 10 componentes.
6. Documentação de handoff entregue (implementation-spec renderizado + contactos).
7. Janela de hypercare definida (default: 2 semanas). `TODO(team)`: confirmar duração e SLA.
8. Manutenção agendada com **papel** responsável, destino de alerta e procedimento de recuperação
   (índices, statistics, jobs de limpeza quando aplicável — `sql-delivery-conventions.md` §13). O papel e o
   mecanismo é o que a arquitectura precisa; o nome de quem o ocupa é da organização, e a sua ausência não
   bloqueia nada.

## 6. Pós-go-live

- Alterações ao que foi decidido re-entram pelo aisa (`/answer` + nova ronda), nunca só no código — o SU é
  a fonte de verdade também na manutenção.
- Incidentes que revelem um Assumed errado → transição no SU + lição para agent-memory na retro.
- Operação e suporte corrente (monitorização, alertas, quem responde): `operations/operability-and-support.md`.
