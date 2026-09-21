# Plano de implementação — Reconciliação e cobertura do engagement

Data: 2026-09-14. Destinatário: Claude Code, sessão de desenvolvimento do framework aisa.

Estado inicial (2026-09-14): plano para execução; o mecanismo descrito ainda não está implementado. Este documento não aprova o blueprint, não fecha requisitos e não autoriza alterações ao engagement real.

> **Estado em 2026-09-16 — as seis fases executadas, a entrega por confirmar.**
>
> | fase | entrega | relatório |
> |---|---|---|
> | 1 | contrato v1, 20 registos, fixture `fx-coverage-f06` | `coverage-phase-1-report.md` |
> | 2 | inventário independente, locators, fingerprints | `coverage-phase-2-report.md` |
> | 3 | motor, CLI, 13 códigos, `finalize` versionado | `coverage-phase-3-report.md` |
> | 4 | ligação ao desenho (`/blueprint` 1b/13b, `status.coverage`, hooks) | `coverage-phase-4-report.md` |
> | 5 | ligação aos deliverables (pré-render, revisão de projecção, autoridade de versão) | `coverage-phase-5-report.md` |
> | 6 | validação integrada: 40 cenários, percurso completo, revisão do diff, integridade | `coverage-phase-6-report.md` |
>
> Medições da fase 6: **40/40 cenários**, **10/10 passos** do percurso completo, **6/6**
> perguntas da revisão do diff, **0 mutações** no engagement real por comando read-only,
> suite de **39 ficheiros / 1906 testes** com as 2 falhas pré-existentes documentadas.
> O mecanismo foi também exercitado contra o engagement real
> (`coverage-real-pricing-bunkers-v2-2026-09-16.md`): 1054 unidades, 13/13 cenários sobre
> cópias, zero alterações no original.
>
> **Por confirmar, e por isso a entrega não se declara fechada:** 7 testes não correram
> neste checkout (6 pedem engagements não montados; 1 perdeu a premissa porque o engagement
> passou a ter registos). O plano é explícito — *«não declarar implementação concluída se
> houver fase/teste obrigatório pendente»*.
>
> **O que continua a não ser declarado:** o desenho de `pricing-bunkers-v2` não está
> aprovado por este trabalho, não está declarado completo por ele, e não está validado
> ponta-a-ponta. O E2E demonstrado é o **do protocolo do framework**, em fixture — nunca o
> da solução.

## 1. Mandato e resultado esperado

Implementar no framework uma passagem obrigatória de reconciliação entre fontes, pedido, esclarecimentos, SU e decisão antes da produção do blueprint; verificar a cobertura do desenho depois de o produzir e a preservação contratual antes de declarar os deliverables completos.

Conservar as quatro fases existentes. A reconciliação integra os comandos atuais; não criar nova fase, nova hierarquia de agentes, sistema externo, base de dados ou segunda fonte de requisitos.

O resultado deve permitir responder separadamente:

1. A estrutura do artefacto é válida?
2. As fontes foram revistas e os requisitos materiais receberam tratamento?
3. O desenho satisfaz esses requisitos, segundo uma revisão semântica registada?
4. O negócio aprovou esta versão concreta?
5. As provas necessárias para conclusão E2E foram executadas e aceites?

Um resultado positivo nos pontos 1–3 nunca produz automaticamente os pontos 4–5.

### Caso de origem obrigatório

Engagement: `projects/pricing-bunkers-v2`, blueprint v01. Na revisão, F06 demonstrou perda de requisito já conhecido:

- `answers.md`, U-010: Outputs BIOS fica disponível para consulta porque o ficheiro é gravado diariamente no SharePoint da Marinha.
- SU C-014 confirma o mecanismo de distribuição/consulta interna.
- O blueprint representa BlendBiocombustível, mas não concretiza a publicação/consulta BIOS.
- C-030 confirma Excel diário `product`/`price` para X-Author; não substitui nem revoga C-014 ou C-001.
- O verificador existente devolve `valid: yes (0 block, 0 warn)`.

A regressão obrigatória deve detetar a perda sem hardcode de `C-014`, BIOS, SharePoint ou do slug no motor.

Relatório de referência: `docs/review-evidence/pricing-bunkers-v2-review-2026-09-14.md`. Distinguir F06 deste relatório de identificadores F06 de outras campanhas.

## 2. Limites e regras de trabalho

- Executar como desenvolvimento do framework, fora de uma sessão de execução de engagement. Ler `CLAUDE.md`, eventuais `AGENTS.md` aplicáveis e `.claude/rules/library-readonly.md` antes de editar.
- O plano autoriza preparar a implementação do framework quando for passado como tarefa de execução; não autoriza inventar respostas ou aprovações do negócio.
- Não alterar ficheiros existentes de `projects/pricing-bunkers-v2`, nem gerar v02, corrigir a SU, reescrever decisões, executar macros ou contactar IT/auditoria.
- Testes e ensaios usam fixtures sintéticas ou cópias temporárias. O original serve para leitura/demonstração, nunca para completar artificialmente o cenário.
- Respeitar `library/` read-only durante runtime. Alterações administrativas ao kernel/packs seguem o processo de desenvolvimento documentado; não desligar permanentemente guards/deny, não usar shell como evasão de rejeição de permissões. Se a sessão não permitir desenvolvimento administrativo, entregar patch e bloqueio concreto.
- Não criar commits, publicar ou fazer merge sem instrução correspondente. Preservar alterações preexistentes do utilizador.
- Runtime novo em Python 3.11+, stdlib-only, conforme `requirements-dev.txt`. Não acrescentar dependência de pandas, PyYAML, jsonschema, serviço LLM ou pesquisa web ao motor.
- Não corrigir todos os 19 achados neste trabalho. F16 (alias da decisão) pode ser corrigido como dependência pequena; restantes defeitos não necessários ficam listados separadamente.
- Não acrescentar exigências específicas de pricing ao kernel. Pricing é fixture; requisitos de pacote e de engagement continuam nos respetivos donos.

## 3. Pontos de extensão existentes a confirmar

Ler seletivamente estes ficheiros, sem carregar o catálogo inteiro de conhecimento:

| Ficheiro | Papel nesta mudança |
|---|---|
| `library/kernel/phases.md` | Quatro fases e portões atuais; integração na fase Decision |
| `library/kernel/blueprint-contract.md` | Produção, validação e aprovação de versões |
| `library/kernel/render-contract.md` | Autoridade por deliverable e proibição de criar verdade downstream |
| `library/kernel/orchestration.md` | Comprehension survival; MAP/ADOPT/DISMISS |
| `library/kernel/states.md` | Estados e autoridade; não os redefinir no contrato de cobertura |
| `library/kernel/tools/dashboard.py` | `parse_su`, leitores de decisões/blueprint, `bp_validate`, `blueprint_state`, `synthesis_state`, `render_state`, modelo/status e CLI |
| `library/kernel/tools/fields_draft.py` | Inventário de colunas/aliases/entradas sem dados e disposições ainda nulas |
| `.claude/skills/aisa-{blueprint,answer,capture,synthesize,render,status}/SKILL.md` | Execução do novo protocolo |
| `.claude/hooks/{blueprint-validate,render-validate,on-su-change,phase-completeness}.py` | Integração de feedback e completude |
| `.claude/hooks/_common.py`, `HOOKS.md`, `.claude/settings.json` | Resolução de engagement, invocação e fronteira de escrita |
| `library/packs/pp/architecture-templates/architecture-core.md` | Obrigações de arquitetura já existentes |
| `library/packs/pp/deliverable-templates/*.template.md` | Seleção/aplicabilidade de conteúdo por deliverable |
| `.claude/tests/test_blueprint_yaml.py`, `test_synthesis_freshness.py`, `test_render_validate.py`, `test_status_model.py`, `test_hook_invocation.py` | Padrões de teste e contratos a preservar |

Factos observados na revisão, a confirmar contra o checkout atual:

- `bp_validate` aceita `concretizes_decision`, mas o leitor do blueprint procura apenas `decision_ref` (perto das linhas 3066/3274).
- `build_model` já calcula separadamente blueprint, síntese e render; integrar cobertura como dimensão irmã.
- `on-su-change.py` enumera diretórios observados; `_coverage/` ainda não está incluído.
- `render-validate.py` contém verificações de suficiência úteis, mas a sua seleção de blueprint não deve ser reutilizada cegamente para todos os deliverables: respeitar o contrato de cada um.
- Os hooks são complementares: a sessão que produziu v01 relata chamadas manuais porque nem todos dispararam.

## 4. Arquitetura da implementação

### 4.1 Componentes novos

1. `library/kernel/coverage-contract.md`: única definição normativa de esquema, estados de cobertura, atualidade, códigos, passagem e compatibilidade.
2. `library/kernel/tools/coverage.py`: funções puras de inventário, validação, hashes, seleção de revisões e projeção do relatório; CLI stdlib.
3. `_coverage/coverage_vNN.json`: revisão persistida, versionada e imutável por engagement.
4. `_coverage/coverage_vNN.md`: apresentação determinística do JSON e resultados; não é autoridade, não é editada manualmente.

Não criar nova skill pública `/coverage` na primeira entrega. O utilizador continua a usar `/blueprint`, `/answer`, `/render` e `/status`. A CLI técnica permite executar/depurar o verificador isoladamente.

Evitar imports circulares: `coverage.py` não importa `dashboard.py` no topo. O dashboard fornece leitores/resolvers aos métodos do módulo; a CLI pode carregar o dashboard de forma lazy via padrão existente, já depois de carregar o módulo, sem construir dashboard. Se a arquitetura de imports exigir extrair um pequeno helper comum, limitar a extração e preservar assinaturas públicas existentes. Não refatorar todo o motor.

### 4.2 Três etapas, um formato

`stage` admite:

- `reconciliation`: fontes → SU/requisitos/decisão; antes de desenhar.
- `blueprint`: requisitos/obrigações → versão concreta do desenho; depois de desenhar e antes de aprovar.
- `render`: autoridades permitidas pelo template → deliverable concreto.

Cada etapa produz novo registo no mesmo contador `coverage_vNN`; não editar a revisão anterior. `based_on` liga às revisões anteriores relevantes. Os IDs de cobertura são locais de revisão, nunca IDs de requisitos nem uma nova taxonomia epistémica.

O JSON transporta conclusões do agente; os vereditos computados são recalculados em cada leitura, nunca confiados a um `valid: true` persistido.

## 5. Esquema v1 a implementar

O contrato deve definir tipos, campos obrigatórios, enums, unicidade e condições por etapa. O exemplo seguinte é ilustrativo; hashes/locators devem ser calculados/obtidos do inventário, nunca copiados como valores reais.

```json
{
  "schema_version": 1,
  "version": "v02",
  "engagement": "pricing-bunkers-v2",
  "stage": "blueprint",
  "based_on": ["coverage_v01.json"],
  "target": {
    "file": "_blueprint/ux-blueprint_v01.yaml",
    "sha256": "<digest calculado pelo motor>"
  },
  "basis": {
    "inventory_sha256": "<digest calculado pelo motor>",
    "sources": [],
    "decision_ref": "D-002",
    "contract_version": "1",
    "pack": "pp"
  },
  "source_review": [],
  "coverage": [
    {
      "id": "item-001",
      "requirement_refs": ["C-014"],
      "source_unit_refs": ["<chave resolvida para a secção U-010>"],
      "disposition": "preserve",
      "scope_basis_refs": [],
      "targets": [],
      "assessment": {
        "status": "missing",
        "rationale": "Falta percurso de publicação e consulta BIOS.",
        "acceptance_basis_refs": ["C-014"]
      },
      "unresolved_refs": [],
      "required_action": "Concretizar saída e consulta no desenho.",
      "responsible_role": "arquitetura"
    }
  ],
  "semantic_review": {
    "status": "completed",
    "performed_by": {"kind": "agent", "name": "Claude"},
    "completed_at": "<data real>",
    "method": "source-to-target and target-to-source",
    "limitations": ["Revisão documental; não executa a solução."],
    "findings": ["item-001"]
  }
}
```

### 5.1 Regras dos campos

- `source_review`: uma entrada por unidade ou grupo explícito, com `unit_refs`, `assessment` (`reviewed`, `unverifiable`, `not_applicable`), `rationale` e links para SU/itens/obrigações. Não usar «reviewed» para declarar que um requisito está satisfeito.
- `coverage[].assessment.status`: `covered`, `partial`, `missing`, `excluded`. Campo ausente é revisão incompleta, não `missing` por default.
- `coverage[].disposition`: `preserve`, `change`, `retire`, `clarify`; descreve o tratamento requerido, não o nível de evidência.
- `scope_basis_refs`: decisão/declaração autorizada que suporta mudança de âmbito ou exclusão de requisito. Vazio legítimo para preservar requisito; obrigatório quando a disposição elimina/altera obrigação material.
- Exclusão de uma coluna mecânica de cálculo da UI pode ter fundamento de desenho; exclusão do cálculo/resultado de negócio exige decisão de âmbito. Não exigir sponsor para toda a coluna técnica descartada, nem permitir eliminar um output com a mesma justificação.
- `targets[]`: objetos com ficheiro, seletor estruturado, tipo e papel (`implementation`, `open_choice`, `proof_obligation`, `projection`). Uma referência a pergunta/prova não conta como implementação coberta.
- `acceptance_basis_refs`: liga ao requisito/critério existente. O texto de revisão pode explicar como verificar a cobertura, mas não inventar limiares ou políticas de aceitação do negócio.
- Estado epistémico vem da SU em cada leitura; não o duplicar em campos que possam ficar inconsistentes.
- Autor da revisão é o agente/executor efetivo, nunca o sponsor inferido. `semantic_review.completed` não é aprovação humana nem prova de verdade.
- Para etapa `reconciliation`, `target` é null; `coverage.targets` não é exigido. O resultado é reconciliação feita, não desenho completo.
- Para etapa `render`, exigir `deliverable`, identidade/hash do template e referências às autoridades permitidas, além do target.
- Base/target/based_on ausentes, malformados, duplicados ou incompatíveis com a etapa são erro de contrato.

### 5.2 Locators resolvíveis

Usar seletores estruturados, sem JSONPath arbitrário/eval:

- Markdown: secção identificada pelo ID de domínio já existente; se cabeçalhos duplicados, discriminador explícito/hierarquia e digest. Nunca escolher o primeiro silenciosamente.
- SU/decisões: ID resolvido pelos leitores atuais.
- Excel capturado: ficheiro, folha, coluna ou entrada sem dados, aliases conforme formato real de `fields_draft.py`.
- Blueprint: caminho de mapas e seleção única de item por `name`, `key`, `component` ou `su_ref`; índices só quando não houver chave estável, protegidos por hash do target.
- Render: slot/seção que o template declara; target precisa resolver para conteúdo existente. Um ID num comentário não prova preservação semântica.

Recusar caminho fora do engagement salvo autoridades do repositório explicitamente permitidas (templates/contratos). Resolver e verificar caminho final, incluindo traversal/symlinks. Nunca executar texto de locator.

## 6. Inventário: denominador independente do registo

O motor constrói o denominador a partir do filesystem/fontes, não de `coverage[]` fornecido pelo agente. Caso contrário, o agente pode omitir simultaneamente requisito e linha de revisão e obter falso verde.

### 6.1 Fontes obrigatórias

- `context.json`: pedido literal e campos de contexto relevantes.
- `enquadramento.md`: T1–T7, invariantes M-n e conjuntos condicionais existentes.
- `answers.md`: todas as secções de resposta, incluindo respostas históricas posteriormente corrigidas.
- SU: todas as linhas; separar atuais de resolvidas, mas não apagar a cadeia de supersessão.
- Decisão-solução atual: âmbito, condições, pressupostos/riscos aceites e provas; preservar referências às anteriores quando dependências existam.
- `inputs/`: manifesto independente de todos os ficheiros, mesmo os não suportados.
- `_capture/`: extraction, fields-draft, process-model, evidence-index, replay e limitações relevantes, sem tratar logs como novos factos.
- `frame.md`, `options.md`, `premortem.md` e lens outputs: fontes auxiliares de obrigações/decisão; não podem criar verdade mais forte que SU/decisão. Material ainda só presente nelas é achado a reconciliar.

### 6.2 Granularidade e custo

- Excel: contabilizar todas as folhas e colunas do inventário, aliases/entradas sem dados e limitações de replay/macros/externos. Agrupar explicitamente colunas repetidas; expandir a lista de membros no snapshot. Não gerar uma pergunta por célula ou fórmula.
- Texto: inventariar secções/passagens determinísticas disponíveis. Se uma passagem contém três obrigações, cabe ao agente separá-las; o motor não afirma ter descoberto todas semanticamente.
- Ficheiro sem extrator: `unverifiable` com motivo, impacto e ação/prova quando material. Não desaparecer do denominador e não ser marcado `not_applicable` por falta de suporte.
- Múltiplos workbooks: chave inclui ficheiro e folha; duas folhas `Outputs` não colidem.
- Chave de unidade deriva do caminho relativo + seletor estável; hash do conteúdo é campo separado. Não mudar a identidade da unidade só porque o conteúdo mudou.
- Classificação de unidade como não material é julgamento explícito com razão; a falta de avaliação continua detetável.
- Mostrar contagens por tipo e por etapa. Não anunciar «100% requisitos cobertos» porque 774 colunas tiveram disposição.

### 6.3 Algoritmo

```text
1. Resolver engagement explicitamente e carregar contratos.
2. Construir manifesto atual e unidades a partir das fontes reais.
3. Validar esquema e unicidade do registo da revisão.
4. Comparar manifesto/unidades/basis com as fontes atuais.
5. Detetar unidades sem revisão, refs mortas, grupos ambíguos.
6. Resolver requisito/decisão e validar regras da disposição.
7. Resolver targets e papéis; detetar covered sem implementação/projeção adequada ao stage.
8. Verificar se a revisão semântica está completa e ligada aos hashes efetivos.
9. Calcular veredictos independentes e elegibilidade para a ação pedida.
10. Devolver JSON/texto; zero escrita por default.
```

O passo 7 verifica estrutura da ligação; o agente revê adequação e escreve rationale. O motor não usa contagem de palavras, simples procura de nomes ou semelhança textual como prova de satisfação.

## 7. Atualidade, versionamento e prevenção de ciclos

### 7.1 Política inicial

- Hash SHA-256 dos bytes de inputs e dos artefactos de conteúdo. Primeira entrega conservadora; mudanças de formatação podem exigir revisão, desde que se explique o motivo.
- Manifesto inclui conjunto de ficheiros, não só hashes dos já conhecidos: adição/remoção é detetada.
- Mudança de contrato/template/pack que define esta revisão invalida a revisão correspondente; não é preciso hashear todo o catálogo de Domain Knowledge. Registar unidades de conhecimento efetivamente consumidas quando sustentam o julgamento.
- Excluir dos inputs de conteúdo `dashboard.html`, `_coverage/`, council/gate/blueprint/render logs, checks e ficheiros temporários. Estes são histórico/derivados; lê-los para auditoria não os transforma em dependência autorreferencial.
- Escrita em log ou regeneração do dashboard não pode tornar cobertura stale.
- O inventário fornecido ao agente antes da revisão inclui o snapshot/hash da base. O draft devolvido pelo agente conserva esse snapshot. `finalize` compara-o com a base atual; nunca substitui silenciosamente os hashes antigos pelos atuais, pois isso carimbaria como revista uma fonte que mudou sem ser relida.

### 7.2 Aprovação não pode invalidar a própria revisão

Problema: aprovar acrescenta um bloco a `decisions.md` e linha D-nnn na SU. Hash bruto destes ficheiros invalidaria a revisão imediatamente.

Implementar fingerprints semânticos restritos para esses dois ficheiros, usando os leitores existentes:

- Hash da decisão-solução depende do bloco efetivamente selecionado e da sua identidade/estado de supersessão.
- Hash das linhas SU de conhecimento depende de ID, secção/estado, conteúdo, evidência, validade e resolução; exclui apenas linhas que o leitor consegue classificar positivamente como espelho de aprovação de blueprint.
- Não excluir todas as linhas `D-*`: mudança de decisão-solução deve invalidar.
- O registo de aprovação é lido separadamente como autoridade humana. Aprovação de outra versão não torna a revisão desta versão aplicável à outra.
- Cabeçalhos derivados de atualização/saúde não entram no fingerprint semântico da SU; conteúdo não reconhecido material deve gerar diagnóstico/conservadorismo, não ser descartado.
- Testar expressamente: acrescentar aprovação não invalida; mudar requisito, fonte, decisão-solução ou versão alvo invalida.

Não acrescentar ao blueprint uma referência ao hash do relatório que por sua vez hasheia o blueprint. A ligação ao target vive no sidecar de cobertura. A aprovação pode referenciar a revisão de cobertura sem fazer parte do seu conteúdo-base.

### 7.3 Revisões e concorrência

- Nunca selecionar uma revisão mais antiga para esconder que a mais recente do mesmo stage/target falhou.
- Selecionar por stage + target/versão + autoridade exigida, e validar freshness; «último coverage global» não basta.
- Sem revisão → `not_evaluated`; schema desconhecido → `unsupported`, nunca válido; base alterada → `stale`; registo ilegível → `invalid`.
- Stale não prova que uma conclusão ficou falsa; obriga a rever os impactos e produzir nova revisão.
- Finalização explícita: draft em temporário → validação/recheck dos hashes → criação exclusiva do próximo vNN; nunca sobrescrever. Se concorrência ocupar a versão, falhar/repetir a reserva com informação clara. Não fazer `os.replace` sobre versão publicada.
- Não confiar em mtime como prova de atualidade. Pode otimizar leitura, mas o check decisivo compara conteúdo.

## 8. APIs e CLI

Assinaturas propostas, ajustáveis ao estilo local sem mudar a semântica:

```python
build_inventory(eng: Path, readers: ReaderAdapter) -> dict
compute_basis(eng: Path, inventory: dict, stage: str, target: dict | None) -> dict
validate_record(record: dict, inventory: dict, readers: ReaderAdapter) -> list[dict]
check_freshness(record: dict, current_basis: dict) -> dict
coverage_state(eng: Path, stage: str, target: dict | None, readers: ReaderAdapter) -> dict
render_report(record: dict, result: dict) -> str
```

`ReaderAdapter` pode ser um objeto/dicionário simples; não criar framework de plugins adicional. Funções sem escrita e sem subprocessos.

CLI nova do módulo (sintaxe a implementar e documentar):

```text
python library/kernel/tools/coverage.py inventory --engagement <slug|path> --json
python library/kernel/tools/coverage.py check --engagement <slug|path> --stage reconciliation --json
python library/kernel/tools/coverage.py check --engagement <slug|path> --stage blueprint --target <path> --json
python library/kernel/tools/coverage.py check --engagement <slug|path> --stage render --target <path> --deliverable <id> --json
python library/kernel/tools/coverage.py report --engagement <slug|path> --record <path>
python library/kernel/tools/coverage.py finalize --engagement <slug|path> --draft <temporary-json>
```

- `inventory`, `check`, `report`: stdout, sem geração de dashboard/log/cache. `finalize` é a única operação de escrita do módulo, explicitamente invocada pelo executor; recalcula basis para a comparar com o snapshot revisto, persiste JSON e projeção Markdown, nunca escreve SU/decisão.
- `finalize` pode persistir revisão com lacunas conhecidas (é evidência válida de incompletude); recusa schema inválido ou fontes alteradas durante a operação.
- Resolver `AISA_ENGAGEMENTS_ROOT`, caminhos com espaços/acentos e cwd arbitrário. Ambiguidade de engagement exige argumento, não escolher o primeiro.
- Exit codes documentados: 0 verificação executada sem lacunas impeditivas para a etapa; 2 argumentos/schema inválido; 3 engagement/ficheiro não encontrado; 4 revisão ausente/stale/incompleta ou lacunas que impedem a ação; 5 erro inesperado. stdout JSON mantém resultados/diagnósticos mesmo com exit 4.
- `exit 0` nunca significa aprovação ou E2E. Em reconciliation significa reconciliação completa com pendências explícitas, não blueprint completo.

### 8.1 Resultado computado

```text
contract_validity: valid | invalid | unsupported
freshness: current | stale | not_evaluated
source_review: complete | incomplete | not_evaluated
semantic_review: completed | pending | not_evaluated
coverage: complete | gaps | not_evaluated
action: produce_blueprint | approve_blueprint | complete_deliverable
eligible: true | false
reasons: [...]
diagnostics: [{code, severity, file, locator, item, message, resolves}]
```

`coverage.complete` só significa ausência de lacunas segundo uma revisão declarada atual e referências verificadas. A apresentação deve dizer «cobertura revista», nunca «correção garantida por código».

## 9. Códigos e regras de passagem

Uma tabela única no contrato e no motor, evitando variantes entre hooks e CLI:

| Código | Condição | Efeito |
|---|---|---|
| COV-SCHEMA | Schema/tipo/versionamento ilegível | Verificação inválida |
| COV-NO-REVIEW | Sem revisão para stage/target | Não avaliado |
| COV-STALE | Manifesto/base/target diferente | Rever antes de usar |
| COV-UNREVIEWED | Unidade sem tratamento | Reconciliação incompleta |
| COV-DEAD-REF | SU/fonte/decisão inexistente ou locator ambíguo | Corrigir ligação |
| COV-MISSING-TARGET | Covered sem target pertinente ao stage | Cobertura não demonstrada |
| COV-INVALID-TARGET | Campo/ação/entidade/secção não existe | Corrigir desenho/ligação |
| COV-EXCLUSION-NO-DECISION | Requisito material retirado sem autoridade | Não aceitar exclusão |
| COV-REVIEW-INCOMPLETE | Falta julgamento/rationale/autor/metodologia | Revisão pendente |
| COV-KNOWN-GAP | Partial/missing declarado | Lacuna visível; regra por ação |
| COV-CAPTURE-LIMIT | Fonte não verificável/limite de captura | Exibir impacto; nunca transformar em coberto |
| COV-AUTHORITY-MISMATCH | Target/revisão usa versão/autoridade errada | Bloquear consumo correspondente |
| COV-UNEXPECTED | Falha interna de avaliação | Não avaliado; nunca sucesso silencioso |

Separar severidade do achado de elegibilidade por ação. Produção para discussão é diferente de aprovação.

### 9.1 Entrada e saída do blueprint

- Antes de produzir: reconciliation completa/atual; toda a unidade tem tratamento e toda a perda identificada foi encaminhada. Perguntas abertas podem permanecer explícitas.
- Se faltam requisitos na SU, o executor reconcilia primeiro, preservando estados/autoridade. Depois captura novo snapshot. Não finalizar coverage antes das alterações upstream que ela descreve.
- Pode produzir uma versão incompleta para discussão com lacunas explícitas; não inventar `draft: true` para isso — esse campo já significa candidato pré-decisão.
- Depois de produzir: structural check atual + cobertura do target. Uma versão com lacunas continua disponível para revisão, mas não se anuncia pronta para aprovação.
- Para nova aprovação: exigir cobertura atual, revisão semântica concluída e ausência de requisitos materiais ausentes/parciais sem disposição de âmbito autorizada; manter os bloqueios estruturais existentes e pedido de aprovação explícita.
- Prova de implementação pendente não bloqueia automaticamente desenho: tem de estar corretamente modelada e atribuída ao momento exigido. «Aprovação independente desenhada, teste previsto antes de produção» difere de «não sabemos como impedir autoaprovação».
- Se opção/decisão deixa de estar sustentada, usar revalidação/revisit existente. Coverage não altera D-nnn nem emite novo outcome.

Esta é uma alteração explícita ao contrato de prontidão para aprovação, não fingir que já existe. Atualizar os contratos conflitantes no mesmo incremento. Não transformar os portões soft entre fases em bloqueios globais.

### 9.2 Deliverables

- Pré-render: revisão atual das autoridades exigidas pelo deliverable e aplicabilidade dos slots. Não exigir todos os requisitos em todos os documentos.
- Pós-render: registo stage render liga itens/obrigações selecionados pelo contrato a secções/slots do documento. Verificar referência e julgamento de preservação; se falhou, registar render-gap e não declarar completo.
- Reutilizar applicability/authority_sources/slot_sources/sufficiency existentes. Só acrescentar campo ao template quando necessário e com definição normativa; não criar nova tabela kernel «requisito → deliverable».
- Architecture Blueprint continua a poder mostrar versão autorizada não aprovada, com escolhas/lacunas explícitas. Spec/Design Brief continuam a exigir a versão aprovada. Estimate conserva autoridade sobre o cálculo e as duas arestas entre deliverables existentes.
- Render nunca reabre Excel para preencher campo em falta. Devolve o gap ao dono upstream; não altera factos, decisões, âmbito, epistemics nem prova.
- Não reter Discovery/Executive de um caso sem arquitetura só porque não há coverage de blueprint. Aplicar revisão de reconciliação/projeção às fontes que o contrato usa; ausência legítima é not applicable, não gap.

## 10. Alterações por ficheiro

| Ficheiro/grupo | Alteração |
|---|---|
| Novo `library/kernel/coverage-contract.md` | Contrato completo acima, exemplos positivos/negativos |
| Novo `library/kernel/tools/coverage.py` | Motor/CLI e relatório determinístico |
| `library/kernel/blueprint-contract.md` | Referir reconciliation/target review e condição de nova aprovação; distinguir produção |
| `library/kernel/render-contract.md` | Preservação por contrato/autoridade e tratamento de gaps |
| `library/kernel/phases.md` | Integrar na Decision sem quinta fase; distinguir prontidão de aprovação |
| `library/kernel/orchestration.md` | Ligar comprehension survival ao registo, sem duplicar definições |
| `library/kernel/tools/dashboard.py` | Importar/adaptar motor, expor `status.coverage`, mostrar limitações, integrar prontidão sem misturar `bp.valid`; alias `concretizes_decision` |
| `.claude/skills/aisa-blueprint/SKILL.md` | Executar preflight, revisão semântica bidirecional, postcheck, finalize e check antes de aprovação |
| `.claude/skills/aisa-answer/SKILL.md` | Mostrar impacto/staleness calculado após resposta; não escrever flag manual |
| `.claude/skills/aisa-capture/SKILL.md` | Explicitar inventário/limites e recheck após fonte/extrator mudar |
| `.claude/skills/aisa-synthesize/SKILL.md` | Preservar pendências; não usar coverage como arquitetura authority |
| `.claude/skills/aisa-render/SKILL.md` | Precheck/postcheck por template, revisar preservação, reportar gaps sem reparar upstream |
| `.claude/skills/aisa-status/SKILL.md` | Mostrar dimensão coverage e ações humanas necessárias |
| `.claude/commands/{blueprint,render,status}.md` | Atualizar apenas onde invocação/descrição precise refletir protocolo; não duplicar algoritmo |
| `.claude/hooks/blueprint-validate.py` | Reportar coverage separadamente da estrutura, read-only |
| `.claude/hooks/render-validate.py` | Chamar núcleo coverage sem duplicar regras; preservar modos dry-run e escrita explícita de gaps |
| `.claude/hooks/on-su-change.py` | Incluir `_coverage/` e fontes novas nos triggers relevantes; manter debounce/sem loop |
| Watch/freshness do dashboard | Capturar alterações por editores/scripts, não só Write/Edit; incluir inputs e coverage sem autoreload infinito |
| `.claude/hooks/phase-completeness.py` | Verificar outputs só quando blueprint/render efetivamente executados; não exigir coverage logo após `/decide` |
| `.claude/hooks/HOOKS.md`, `docs/COMO-USAR.md`, `docs/ARCHITECTURE.md` | Documentar responsabilidade e limites; sem afirmar checks não implementados |

Manter as regras de pack no pack: referências/campos de blueprint PP e suficiência dos seus templates. O motor genérico não contém nomes de produtos, serviços, folhas ou campos do caso real.

## 11. Revisão semântica executada pelo agente

Atualizar o procedimento do executor para duas passagens explícitas:

**Fonte → destino:** pedido, invariantes, esclarecimentos, outputs/consumidores, percurso normal, exceções, permissões/segregação, dados/cálculos, integrações, falhas/recuperação e provas. Para cada obrigação material, indicar o tratamento e ponto concreto no desenho.

**Destino → fonte:** para cada mecanismo/regra/ação material proposta, mostrar se vem de requisito confirmado, pressuposto explícito ou decisão de desenho dentro do âmbito; detetar invenção, ampliação de autoridade e exclusão implícita.

O agente pode concluir que uma unidade é observação sem requisito novo. Deve justificar; não criar artificialmente centenas de Unknowns. Novos Unknowns continuam sujeitos às regras de admissão já existentes; insuficiência de desenho pode ser lacuna de execução, não pergunta ao negócio.

Uma ligação a `open_questions` não transforma `partial` em `covered`. Uma declaração de risco aceite não elimina automaticamente obrigação de negócio. Um `su_ref` válido num ecrã não demonstra que existe o percurso de publicação.

## 12. Implementação faseada e critérios de saída

Estas são **seis fases de desenvolvimento da mudança**, não novas fases do engagement. Substituem os três incrementos A/B/C da primeira redação deste plano. As quatro fases de negócio do aisa mantêm-se.

Executar uma fase por passagem ao Claude, usando os prompts da secção 16. Cada passagem termina com alterações, testes, limitações e evidência da fase; não começa automaticamente a seguinte. Isto delimita o trabalho atribuído e permite rever o diff antes de aumentar o âmbito. Não exige autorização para cada edição interna da fase nem representa aprovação do negócio.

Dependências: **1 → 2 → 3 → 4 → 5 → 6**. Não avançar sobre critérios de saída por cumprir. Uma fase pode corrigir defeitos da anterior necessários ao seu objetivo, documentando-os; alterações ao contrato devem atualizar testes e evidência afetados. Não antecipar alterações de fases seguintes para contornar uma dependência.

| Fase | Entrega principal | Limite da entrega |
|---|---|---|
| 1 — Contrato e cenários | Contrato v1, exemplos e fixtures F06 | Sem alterar comportamento dos comandos |
| 2 — Inventário e atualidade | Denominador independente, locators e fingerprints | Sem escrita em engagements nem gates novos |
| 3 — Verificador e registos | CLI, diagnósticos, finalize e relatórios | Mecanismo standalone; sem ativação nos comandos |
| 4 — Blueprint e estado | Reconciliação, revisão do desenho e prontidão | Ainda sem revisão de projeção dos deliverables |
| 5 — Síntese e deliverables | Preservação por contrato e autoridade | Sem alegação de E2E da solução de negócio |
| 6 — Validação integrada | Regressão completa e ensaio isolado do percurso | Nenhuma migração/alteração do engagement real |

### Fase 1 — Contrato, decisões técnicas e fixtures

**Entrada:** plano e checkout atual; nenhuma fase anterior necessária.

**Trabalho:**

1. Inspecionar instruções, alterações locais, leitores e contratos da secção 3. Registar baseline sem modificar engagements.
2. Criar `coverage-contract.md`, inicialmente identificado como contrato em implementação, sem anunciar ativação no runtime.
3. Fechar o esquema, seletores, estados, códigos, política de passagem, compatibilidade e fingerprint de aprovação. Resolver ambiguidades técnicas deste plano por escrito.
4. Criar exemplos JSON válidos e inválidos e fixtures sintéticas do F06: fonte/resposta, SU/decisão, desenho incompleto, destino decorativo e desenho que realmente cobre a saída.
5. Documentar expectativas dos testes da secção 13 e a fase que os implementa. Não deixar testes novos deliberadamente vermelhos na suite principal; casos ainda sem motor ficam como fixtures/especificações de aceitação.

**Ficheiros principais:** novo contrato; fixtures de coverage; relatório da fase. Não alterar skills, hooks, gates ou políticas ativas de aprovação.

**Critérios de saída:** esquema e exemplos coerentes; definição inequívoca do denominador, limites do julgamento semântico e comportamento de cada etapa; caso F06 reproduzível documentalmente; zero mutações nos engagements.

**Evidência:** `docs/runtime-hardening/coverage-phase-1-report.md`, com decisões técnicas, fixtures, lacunas ainda reais e âmbito entregue. Não declarar motor implementado.

### Fase 2 — Inventário, resolução de referências e atualidade

**Entrada:** contrato/fixtures da fase 1 revistos e sem ambiguidades impeditivas.

**Trabalho:**

1. Implementar núcleo de `coverage.py`: inventário independente, unidades/grupos, locators, manifesto e fingerprints.
2. Reutilizar os leitores existentes através de adapter sem imports circulares. Corrigir o alias `concretizes_decision` com teste próprio se a dependência se confirmar.
3. Implementar CLI `inventory`; operações exclusivamente read-only.
4. Cobrir inputs novos/removidos, fontes não suportadas, múltiplos Excel, secções ambíguas, limites de captura e proteção de caminhos.
5. Provar que mudanças materiais invalidam a base, mas append de aprovação e alterações de logs/derivados não causam ciclos.

**Ficheiros principais:** `coverage.py`, testes inventory/freshness, ajuste mínimo do leitor se necessário. Ainda sem integração em `build_model`/skills/hooks.

**Testes prioritários:** T05–T11, T16–T20, T26–T28, T36, T38–T39, nas partes relativas a inventário/referências/fingerprints.

**Critérios de saída:** inventário não controlado pelo registo fornecido pelo agente; nenhuma unidade omitida silenciosamente; hashes/locators reproduzíveis; approval append não invalida; execução em cwd externo funciona; zero escrita em read-only. Testes já existentes afetados continuam a passar.

**Evidência:** `coverage-phase-2-report.md`, outputs de inventory e testes. Não declarar cobertura de blueprint avaliada nesta fase.

### Fase 3 — Validador, CLI e persistência versionada

**Entrada:** inventário e política de atualidade da fase 2 testados.

**Trabalho:**

1. Implementar validação de schema, disposições, targets, revisão semântica declarada e diagnósticos.
2. Implementar seleção de revisão por etapa/target/autoridade e veredictos separados.
3. Implementar CLI `check`, `report`, `finalize`, códigos de saída e JSON estável.
4. Implementar finalização exclusiva e relatório Markdown determinístico. Comparar snapshot revisto com base atual; não atualizar hashes para disfarçar revisão stale.
5. Demonstrar F06 por fixtures: covered sem destino falha; a revisão com destino decorativo permanece partial/missing; uma revisão fundamentada do percurso completo pode ter cobertura completa sem aprovação.

**Ficheiros principais:** módulo/CLI, testes contract/integration e fixtures. Não ativar condições novas nos comandos de engagement.

**Testes prioritários:** T01–T04, T11–T15, T21–T24, T29–T30, T37–T40. Completar testes parcialmente implementados na fase 2.

**Critérios de saída:** verificação standalone funciona do inventário ao diagnóstico; registo incompleto nunca produz falso verde; finalize não sobrescreve nem escreve SU/decisões; relatório é derivado do JSON; fontes alteradas durante revisão impedem finalização. Ausência de revisão em engagement real produz not_evaluated, não aprovação implícita.

**Evidência:** `coverage-phase-3-report.md`, comandos/resultados e demonstração F06. O núcleo está funcional; integração nos comandos continua pendente.

### Fase 4 — Integração em blueprint, respostas e status

**Entrada:** CLI/motor da fase 3 concluídos e testados.

**Trabalho:**

1. Integrar reconciliação antes de `/blueprint` e avaliação da versão produzida, com chamadas explícitas ao motor.
2. Integrar revalidação após `/answer`/`capture`; calcular staleness, sem booleano manual em `_state.json`.
3. Atualizar contrato de blueprint/phases/orchestration para a condição de nova aprovação. Produção para discussão continua possível; preservar significado de `draft`.
4. Expor `status.coverage` e prontidão com estrutura, cobertura, aprovação e E2E separados.
5. Integrar feedback no hook de blueprint, triggers/watch e completude apenas quando o comando correspondente foi executado.
6. Testar legacy, ausência de hooks, nova resposta, mudança de decisão e ausência de aprovação humana.

**Ficheiros principais:** dashboard/status, skills blueprint/answer/capture/status, contratos, hooks e documentação correspondentes. Não alterar ainda a seleção/projeção dos deliverables.

**Testes prioritários:** T01–T04 via percurso do executor; T17–T25, T30, T35–T38; suites blueprint, status, freshness e hooks.

**Critérios de saída:** nova resposta invalida revisão aplicável; versão com gaps pode existir mas não é anunciada pronta para aprovação; checks funcionam explicitamente sem hooks; aprovação histórica não é revogada; o motor nunca escreve nova aprovação. A observação do status não gera ciclos de escrita.

**Evidência:** `coverage-phase-4-report.md`, snapshots de status e ensaio do percurso blueprint em fixture. Revisão de render continua pendente.

### Fase 5 — Preservação em síntese e deliverables

**Entrada:** fluxo de blueprint e autoridade de cobertura disponíveis na fase 4.

**Trabalho:**

1. Integrar aisa-synthesize/render e contrato de render sem criar verdade downstream.
2. Selecionar a versão correta por deliverable: latest authorized vs. approved, conforme contrato existente.
3. Implementar revisão stage render por slots/obrigações exigidos, precheck/postcheck, registo de gaps e reutilização da suficiência existente.
4. Mostrar perdas de conteúdo sem exigir todos os requisitos em todos os documentos.
5. Exercitar casos sem arquitetura, headless, legacy e deliverables não aplicáveis; atualizar documentação e hook render.

**Ficheiros principais:** render-contract, skills synthesize/render, render-validate, template metadata apenas se indispensável, testes de projeção e documentação.

**Testes prioritários:** T22–T24, T31–T35, T39–T40; suites render, síntese e applicability.

**Critérios de saída:** saída exigida perdida no deliverable gera gap; o renderer não a inventa; comentário com ID não substitui revisão semântica; autoridade/versionamento corretos; casos sem UI/arquitetura não são bloqueados por requisito inaplicável.

**Evidência:** `coverage-phase-5-report.md`, exemplo JSON/Markdown de projeção e resultados de seleção de autoridade. Ainda falta validação integrada completa.

### Fase 6 — Validação integrada e entrega

**Entrada:** fases 1–5 concluídas com respetiva evidência.

**Trabalho:**

1. Executar os 40 cenários, testes novos e suite completa requerida pelo repositório. Documentar qualquer teste não executado como inconclusivo.
2. Executar ensaio isolado do fluxo: fontes → reconciliação → blueprint com perda → revisão corretiva → cobertura atual → ausência de aprovação → aprovação simulada apenas em fixture → render com perda → render corrigido → nova resposta que invalida cobertura.
3. Rever o diff quanto a estados/autoridades duplicados, hardcodes do caso real, imports circulares, hashes autorreferenciais, fallback para revisão antiga e alterações excessivas ao framework.
4. Verificar integridade do engagement real por manifesto/hashes antes/depois do ensaio e ausência de mutações produzidas pelos comandos read-only.
5. Consolidar instruções de uso, limitações, compatibilidade e evidência final da secção 15.

**Critérios de saída:** regressões relevantes e suite exigida aprovadas; F06 demonstrado nos dois sentidos; comandos/status/render integrados; nenhuma resposta/aprovação inventada; nenhuma alteração ao engagement original. O E2E aqui demonstrado é o do protocolo do framework em fixture, nunca o E2E da solução de pricing.

**Evidência:** `coverage-phase-6-report.md` e relatório final com ligação às seis fases. Não declarar implementação concluída se houver fase/teste obrigatório pendente.

### Registo de passagem entre fases

Cada relatório deve conter: âmbito entregue; ficheiros alterados; decisões técnicas; comandos e resultados; critérios de saída satisfeitos/não satisfeitos; limitações; dependências concretas para a próxima fase. Usar os nomes acima dentro de `docs/runtime-hardening/`.

Não usar o relatório de uma fase como prova de funcionalidades das seguintes. A fase 1 pode estar completa com o motor ainda inexistente; a entrega global só termina na fase 6.

## 13. Plano de testes obrigatório

Usar unittest e fixtures temporárias segundo os padrões existentes. Criar `test_coverage_contract.py`, `test_coverage_inventory.py`, `test_coverage_freshness.py`, `test_coverage_integration.py` e fixtures sob `.claude/tests/fixtures/coverage/`, ou organização equivalente coerente.

| ID | Caso | Resultado esperado |
|---|---|---|
| T01 | F06: C-014 sem destino no desenho | Missing; estrutura BP continua independente |
| T02 | C-014 citado só na entidade blend | Não declarar satisfação automaticamente; fixture semântica mantém partial/missing |
| T03 | Percurso BIOS completo com fonte e revisão | Cobertura revista para este requisito; aprovação continua ausente |
| T04 | Resposta contém obrigação ausente da SU | Unidade exige reconciliação; omissão da linha coverage não dá verde |
| T05 | Apagar uma folha/coluna do source_review | COV-UNREVIEWED |
| T06 | Nova fonte em inputs após revisão | Stale/unreviewed |
| T07 | Workbook alterado, captura antiga | Captura/base stale; não reutilizar conclusão |
| T08 | Fonte não suportada/macros não capturadas | Limitação explícita; não covered por default |
| T09 | Dois workbooks com Outputs | Sem colisão de unidades |
| T10 | Grupo de colunas repetidas com membros enumerados | Revisão aceita; membro omitido é detetado |
| T11 | Su_ref/locator/target inexistente ou ambíguo | Código correspondente, nunca fallback silencioso |
| T12 | Campo de ecrã inexistente | COV-INVALID-TARGET; não depender apenas de BP check |
| T13 | Excluir requisito material sem decisão | COV-EXCLUSION-NO-DECISION |
| T14 | Excluir coluna de implementação da UI com fundamento válido | Não exigir indevidamente aprovação de âmbito |
| T15 | Covered aponta apenas a pergunta/prova futura | COV-MISSING-TARGET ou gap por tipo |
| T16 | Estado Assumed com referência válida | Continua Assumed; nenhum upgrade |
| T17 | Correção de resposta substitui regra antiga | Stale e cadeia de supersessão preservada |
| T18 | Alterar logs/dashboard/Markdown gerado | Não invalida basis |
| T19 | Acrescentar aprovação legítima de blueprint | Não invalida a própria revisão; não aprova outra versão |
| T20 | Mudar decisão-solução ou requisito SU | Invalida, mesmo que ID seja o mesmo |
| T21 | Blueprint modificado após revisão | Stale pelo hash do target |
| T22 | Rever v01, tentar consumir v02 | Autoridade/target mismatch |
| T23 | Nova revisão com gaps e antiga completa | Não escolher antiga para esconder gaps |
| T24 | Registo ausente, JSON inválido ou schema futuro | Not evaluated/invalid/unsupported; nunca verde |
| T25 | Hooks não dispararam | Checks explícitos dos comandos continuam disponíveis e documentados |
| T26 | CLI em cwd externo, path com espaços/acentos | Resolve corretamente, sem escrita inesperada |
| T27 | Engagements múltiplos sem seleção | Falha explícita, não escolher arbitrariamente |
| T28 | Traversal/symlink externo em target | Recusado sem leitura/escrita indevida |
| T29 | Finalize concorrente ou versão existente | Não sobrescreve histórico |
| T30 | Apenas revisão semântica pending | Não completa por referências válidas |
| T31 | Spec/brief pedem aprovada; architecture report pede latest authorized | Seleção correta por contrato |
| T32 | Render omite conteúdo selecionado e mantém ID em comentário | Referência não basta; revisão de projeção acusa omissão |
| T33 | Render com lacuna | Gaps explícitos; não reescreve SU/blueprint nem resolve Unknown |
| T34 | Caso sem UI/headless/sem arquitetura autorizada | Aplicabilidade correta; não inventa screens/blueprint |
| T35 | Legacy sem coverage e com aprovação histórica | Aprovação preservada; coverage not_evaluated |
| T36 | `concretizes_decision: D-002` | Leitor devolve D-002 como decision_ref normalizado |
| T37 | Apenas perguntas/provas não bloqueantes de implementação pendentes | Reconciliação pode completar; E2E continua não provado |
| T38 | Verificação read-only repetida | Mesmo resultado e zero mutações no engagement |
| T39 | Template/contrato relevante alterado | Projeção/revisão correspondente stale |
| T40 | Relatório Markdown alterado manualmente | Não muda autoridade JSON nem produz falsa aprovação |

T02/T32 não devem fingir que código entende semântica. Exercitam a declaração semântica e impedem que a existência da referência substitua essa avaliação. No ensaio manual com o agente, pedir explicitamente que reconheça a insuficiência do target decorativo.

### Regressão existente

Executar testes novos e suites de blueprint, A5, render, síntese/freshness, status, locator resolution e hook invocation. Antes de declarar implementação validada, executar todos os testes requeridos por `requirements-dev.txt`/instruções do repo. Dependência ausente ou teste não executado é inconclusivo, nunca OK. Não adicionar testes que só reproduzem o código sem verificar uma falha observável.

## 14. Compatibilidade e ativação

- Sem registos de coverage: apresentar `not_evaluated`, não «completo» nem «reprovado retroativamente».
- Não apagar, superseder ou reescrever aprovações históricas por introdução do mecanismo.
- Novas execuções de blueprint/render seguem o contrato novo e criam registos; para nova aprovação exige-se revisão aplicável, mesmo quando o engagement começou antes.
- Render de autoridade legacy pode exigir reconciliação/revisão nova antes de ser declarado completo, sem revogar a aprovação histórica. Exibir diferença entre «aprovação existente» e «cobertura ainda não verificada».
- Schema de coverage versionado; desconhecido não é interpretado por aproximação.
- Não acrescentar booleanos de verdade em `_state.json`; estado de cobertura é derivado dos registos/fontes.
- Não regenerar em lote dashboards ou deliverables reais para demonstrar migração. Usar fixtures e amostra read-only.

## 15. Evidência final que o Claude deve entregar

1. Lista de ficheiros alterados e decisões de implementação que diferem deste plano, com justificação.
2. Comandos e resultados dos testes, incluindo falhas/limitações.
3. Demonstração F06 em fixture: antes missing; após desenho correto covered por revisão, mantendo aprovação/E2E separados.
4. Demonstração de invalidação por nova resposta/fonte e ausência de invalidação por append de aprovação.
5. Exemplo real de CLI JSON e relatório Markdown, gerados por código, sem editar engagement original.
6. Confirmação de que o código não contém identificadores específicos do caso real e de que checks read-only não escrevem.
7. Limites remanescentes: compreensão semântica não provada por código, fontes não capturáveis e dependência de julgamento do agente.
8. Nenhuma declaração de que o blueprint real está aprovado, completo ou validado E2E.

## 16. Prompts de passagem ao Claude — uma fase de cada vez

Usar o prompt da fase atribuída, juntamente com o bloco de regras comum abaixo. Não enviar «implementa todas as fases» quando o objetivo é rever cada entrega antes de atribuir a seguinte.

**Regras comuns a todos os prompts:**

> Trabalha neste repositório como desenvolvimento do framework. Lê `docs/runtime-hardening/coverage-reconciliation-implementation-plan.md` e as instruções aplicáveis. Executa integralmente apenas a fase atribuída, incluindo os testes e o relatório exigidos; não comeces a seguinte. Mantém `projects/pricing-bunkers-v2` intacto e usa fixtures/cópias temporárias. Não respondas a Unknowns, não alteres âmbito de negócio e não registes aprovações em nome do utilizador. Resolve escolhas técnicas dentro do âmbito e documenta desvios fundamentados; informação de negócio continua pendente. Preserva a separação entre estrutura, cobertura, aprovação e E2E. Não desatives proteções do runtime nem publiques/commites sem autorização correspondente. No fim entrega o diff resumido, comandos/resultados, critérios de saída e limitações. Não declares a fase concluída com critérios obrigatórios por cumprir.

**Fase 1:**

> Executa a fase 1 — Contrato, decisões técnicas e fixtures — da secção 12. Define o contrato v1 e os exemplos/fixtures necessários, incluindo F06 e o destino decorativo. Não alteres comportamento de comandos, hooks ou gates. Entrega `docs/runtime-hardening/coverage-phase-1-report.md` e termina esta passagem.

**Fase 2:**

> Executa a fase 2 — Inventário, resolução de referências e atualidade. Lê primeiro `coverage-phase-1-report.md` e verifica os pré-requisitos. Implementa o núcleo read-only e CLI inventory, com testes de denominador independente, fontes novas, locators e hashes sem ciclos de aprovação. Não integres ainda nos comandos. Entrega `docs/runtime-hardening/coverage-phase-2-report.md`.

**Fase 3:**

> Executa a fase 3 — Validador, CLI e persistência versionada. Lê os relatórios das fases anteriores e verifica os pré-requisitos. Entrega check/report/finalize, diagnósticos e revisão por etapa/target, com provas F06 e proteção contra carimbar fontes alteradas como revistas. Não atives ainda novas regras nos comandos. Entrega `docs/runtime-hardening/coverage-phase-3-report.md`.

**Fase 4:**

> Executa a fase 4 — Integração em blueprint, respostas e status. Confirma o núcleo entregue nas fases 1–3. Integra chamadas explícitas, feedback de hooks e regras de nova aprovação, sem alterar o significado de draft nem revogar aprovações históricas. Mantém render fora deste âmbito. Entrega `docs/runtime-hardening/coverage-phase-4-report.md`.

**Fase 5:**

> Executa a fase 5 — Preservação em síntese e deliverables. Confirma a fase 4. Integra revisão de projeção por contrato e versão de autoridade, com gaps explícitos e sem criar verdade downstream. Testa casos headless, sem arquitetura e legacy. Entrega `docs/runtime-hardening/coverage-phase-5-report.md`.

**Fase 6:**

> Executa a fase 6 — Validação integrada e entrega. Lê os relatórios das cinco fases, executa o ensaio completo em fixture e a suite requerida, revê regressões e integridade do engagement real. Corrige defeitos encontrados dentro do âmbito da implementação. Entrega `docs/runtime-hardening/coverage-phase-6-report.md` e a evidência final da secção 15. Distingue E2E do protocolo em teste de E2E da solução de pricing, que não estás a validar.
