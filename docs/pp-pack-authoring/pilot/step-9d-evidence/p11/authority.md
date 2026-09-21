# Fonte A — architecture record: record_authority[] (ux-blueprint_v05.yaml, versão APROVADA)

  record_authority:
    - domain: "Dados-mestre de pricing (dicionário contraparte × combustível × métrica)"
      authority: "external system of record (SQL Server partilhado de pricing)"
      access_mode: keep-in-place
      su_refs: [C-017, C-057, C-058, C-062]
    - domain: "Margens-alvo e custos logísticos diários"
      authority: "external system of record (SQL Server partilhado de pricing)"
      access_mode: keep-in-place
      su_refs: [C-006, C-016, C-057, C-062]
    - domain: "Histórico de preços diários"
      authority: "external system of record (SQL Server partilhado de pricing)"
      access_mode: keep-in-place
      su_refs: [C-018, R-004, C-057, C-060, C-062]
    - domain: "Termos comerciais de cliente (segmento de contrato a termo)"
      authority: "external system of record (SAP)"
      access_mode: virtualized
      su_refs: [C-052, C-003]


# Fonte B — ux-blueprint#entities (v05 remete para v01)

entities:
  - name: DadosMestrePricing
    label: "Dados-Mestre de Pricing"
    description: "Dicionário contraparte × combustível × métrica (hoje 291 named ranges no Excel)"
    su_refs: [C-017, C-035, R-006]
    fields_itemized: false
    open_choice_ref: "ver open_architecture_choices — decomposição dos ~85 campos manuais"
    state_machine: [proposta, aprovada, activa]
    approval: true
  - name: CustosLogisticos
    label: "Custos Logísticos"
    description: "Custos por porto e modo de transporte (carro-tanque, barcaça, pipeline), actualizados mensalmente"
    su_refs: [C-016, C-006]
    fields_itemized: false
  - name: MargensAlvo
    label: "Margens-Alvo"
    description: "Margem por produto, tipo de cliente e data, decidida no comité diário"
    su_refs: [C-002, C-008, C-039, C-046]
    fields_itemized: false
  - name: PrecoDiarioConsolidado
    label: "Preço Diário Consolidado"
    description: "Output único, substituindo as 6 folhas hoje divergentes (C-041); alimenta o carregamento em X-ALT"
    su_refs: [C-041, C-001, R-007]
    readonly: true
    feeds_output: true
  - name: AprovacaoCarregamento
    label: "Aprovação de Carregamento"
    description: "Passo de aprovação do superior hierárquico antes do carregamento (resolução de SoD)"
    su_refs: [C-026, C-043]
    state_machine: [pendente, aprovado, carregado]
    approval: true
  - name: HistoricoPrecos
    label: "Histórico de Preços"
    description: "Registo estruturado e consultável do histórico diário, substituindo o arquivo de ficheiros soltos"
    su_refs: [C-018, R-004]
    readonly: true
  - name: TermosComerciaisCliente
    label: "Termos Comerciais de Cliente (contrato a termo)"
    description: "Não gerido nesta app — referenciado apenas para leitura; SAP é a fonte de verdade"
    su_refs: [C-052, C-003]
    external: true
    owned_here: false

