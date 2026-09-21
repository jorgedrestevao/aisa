# delivery-conventions — Team Delivery Conventions (Power Platform)

**Status:** defaults sensatos, criados 2026-08-31 — **ajustar à prática da equipa** (secções marcadas `TODO(team)` esperam captura na retro do pilot).
**Consulted by:** `implementation-spec` e `claude-design-brief` (build-time), `aisa-blueprint` (naming), futura camada de traceability (stamping).
**Phase eligibility:** Options + Decision + build (nunca Discovery/Framing).

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
| Screens / controls / variáveis Power FX | ver `screen-consolidation-rules.md` (screens) e `powerfx-patterns.md` (var/gbl/col/err) | `AdvanceRequestListScreen`, `varSelectedRequest` |

`TODO(team)`: confirmar publisher prefix e idioma dos display names (PT vs EN).

## 2. Traceability stamping (preparação da camada de rastreabilidade)

**Regra:** todo o componente criado a partir de um implementation-spec/blueprint aisa carrega os ids de origem na sua **description**:

```
su: C-014, D-002 | bp: v02/PricingRequestListScreen
```

- Tabelas e colunas Dataverse → campo Description.
- Screens Canvas → comentário no OnVisible ou App description por screen (índice).
- Flows → campo Description do flow.
- A linha `su:` é machine-parseable: é a join key para o diff futuro spec-vs-implementação ("que requisitos ainda não estão implementados?" torna-se um scan da solution).

## 3. Environments e ALM

- Estratégia mínima: `DEV → UAT → PROD`; solutions **unmanaged em DEV, managed em UAT/PROD**.
- Deploy só por pipeline ou export/import documentado — nunca edição direta em PROD.
- Connection references sempre (nunca connections embutidas); ownership por **service account**, nunca conta pessoal.
- `TODO(team)`: nomes reais dos environments, quem aprova deploy para PROD, janela de deploy.

## 4. Segurança e dados

- RBAC conforme `security-patterns.md` (matriz ecrã × entidade×CRUD no implementation-spec, sempre).
- Auditoria: eventos Approve/Delete/Export sempre com padrão de audit (ver `powerfx-patterns.md § Audit Log`).
- Dados de teste em DEV/UAT: **sempre anonimizados** (ver `anonymization.md`); nunca dados reais de PROD fora de PROD.

## 5. Go-live checklist

1. DLP policy do environment verificada contra os connectors usados.
2. RBAC testado por role real (não só o maker).
3. Delegation testada com volume realista (≥ volume esperado do 1.º ano; ver `delegation-matrix.md`).
4. Flows com error-handling + owner em service account + run alerts configurados.
5. Descriptions com stamping `su:` presentes (secção 2) — amostragem de 10 componentes.
6. Documentação de handoff entregue (implementation-spec renderizado + contactos).
7. Janela de hypercare definida (default: 2 semanas). `TODO(team)`: confirmar duração e SLA.

## 6. Pós-go-live

- Alterações ao que foi decidido re-entram pelo aisa (`/answer` + nova ronda), nunca só no código — o SU é a fonte de verdade também na manutenção.
- Incidentes que revelem um Assumed errado → transição no SU + lição para agent-memory na retro.
