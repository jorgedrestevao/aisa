# anonymization — Anonymisation Rules and Synthetic-Data Generation

**Source:** transplanted 2026-05-28 from the previous-aisa references (`ref-07-anonymization.md`).
**Consulted by:** `data-steward` lens (when discussing sensitive-column handling); `lens-technology`, `solution-architect` (when designing test environments); `implementation-spec` deliverable template (when listing test-data preparation tasks).
**Phase eligibility:** mostly Options + Decision, but the **detection signals** are also useful in Discovery to surface Risky or Confirmed rows about data sensitivity (those signals do not name vendors/products).
**Locale:** the pools below are Portuguese / English bilingual; adapt per engagement.

The 11 enumerated sensitivity types align with [`dataverse-reference.md`](dataverse-reference.md) § Schema-Rigor Validation Matrix.

---

## ANONYMISATION METHODS BY DATA TYPE

### Type 1 — Person Names
**Detection signals:** column name contains: name, nome, primeiro, apelido, contacto, responsavel, gestor, owner, contact
**Method:** Replace with fictional name from same language pool. Match word count (2→2, 3→3).
**Never reuse** the same generated name twice in the same entity file.

**Portuguese name pool:**
- First (M): Rui, André, Miguel, João, Pedro, Luís, Carlos, Paulo, Tiago, Nuno, Filipe, Diogo, Hugo, Bruno, Ricardo, Henrique, Gonçalo, Sérgio, Marco, Vasco
- First (F): Ana, Margarida, Inês, Sofia, Catarina, Beatriz, Joana, Marta, Sara, Filipa, Raquel, Daniela, Rita, Carla, Vera, Mónica, Susana, Cláudia, Helena, Patrícia
- Surnames: Silva, Santos, Ferreira, Costa, Oliveira, Rodrigues, Martins, Sousa, Carvalho, Pereira, Alves, Lopes, Ribeiro, Pinto, Gomes, Nunes, Fernandes, Jesus, Fonseca, Azevedo

**English name pool:**
- First (M): James, Oliver, William, Thomas, George, Harry, Jack, Noah, Charlie, Henry, Edward, Arthur, Leo, Freddie, Oscar, Ethan, Lucas, Mason, Logan, Elijah
- First (F): Olivia, Emily, Sophie, Isla, Amelia, Grace, Jessica, Lucy, Charlotte, Ella, Mia, Lily, Hannah, Zoe, Eleanor, Ava, Isabella, Sophia, Chloe, Evelyn
- Surnames: Smith, Jones, Williams, Brown, Taylor, Davies, Evans, Wilson, Thomas, Roberts, Johnson, Walker, Wright, Robinson, Thompson, White, Harris, Martin, Garcia, Lee

---

### Type 2 — Emails
**Detection:** column name contains: email, mail, e-mail, correio, contact
**Content hint:** contains @ symbol
**Method:** `[firstname].[lastname]@demo.com` (lowercase, no accents)
**Never reuse** same email in same entity.

---

### Type 3 — Phone Numbers
**Detection:** column name contains: phone, tel, telef, mobile, telem, fax, contact
**Content hint:** digit strings 9-15 chars
**Method:** Preserve format (length, separators, country code), replace all digits after country code.

**PT mobile format:** `9[1|2|3|6][random 7 digits]` — e.g., 912345678
**PT landline format:** `2[1-9][random 7 digits]` — e.g., 212345678
**International:** `+[code] [preserve grouping, replace digits]`

---

### Type 4 — NIFs / Tax IDs
**Detection:** column name contains: nif, vat, tax, fiscal, contribuinte, nipc, niss
**Content hint:** 9 digits (PT)

**Portuguese NIF generation (individual — starts with 1 or 2):**
```
digits[0-7] = random digits (first digit: 1 or 2)
sum = d[0]*9 + d[1]*8 + d[2]*7 + d[3]*6 + d[4]*5 + d[5]*4 + d[6]*3 + d[7]*2
rem = sum % 11
check = 0 if rem < 2 else 11 - rem
NIF = concat(digits, check)
```

**Portuguese NIPC (company — starts with 5):**
Same algorithm, first digit = 5.

**Never use** real PT bank codes or known company NIFs.

---

### Type 5 — Addresses / Moradas
**Detection:** column name contains: morada, address, rua, street, av, avenida, largo, praca, cidade, city, cp, postal, zip, localidade
**Method:** Fictional street + real city (same region if detectable) + fictional postal code (format preserved).

**PT street pool:** Rua das Flores, Avenida da Liberdade, Rua do Comércio, Travessa da Saudade, Largo do Município, Rua de Santo António, Avenida de Roma, Rua dos Anjos, Travessa do Carmo, Rua da Prata, Avenida Almirante Reis, Rua Augusta, Rua do Ouro, Praça do Comércio, Rua da Conceição
**PT cities:** Lisboa, Porto, Coimbra, Braga, Aveiro, Setúbal, Faro, Évora, Viseu, Leiria, Santarém, Viana do Castelo, Castelo Branco, Beja, Portalegre
**PT postal code format:** `XXXX-XXX` (generate: 1000-9999 for first part, 001-999 for second)

---

### Type 6 — Financial Values
**Detection:** column name contains: valor, value, amount, preco, price, total, saldo, margin, margem, receita, revenue, custo, cost, desconto, discount, orcamento, budget, fee, taxa
**Method:** `anonymised = original × (0.80 + random × 0.40)` — ±20% variation
**Rules:**
- Preserve sign (positive stays positive)
- Preserve decimal places format
- Preserve order of magnitude (100s stay in 100s, millions stay in millions)
- 0 stays 0
- Never round to suspiciously clean number

---

### Type 7 — Company Names
**Detection:** column name contains: empresa, company, cliente, customer, fornecedor, supplier, parceiro, partner, organizacao, entidade
**Method:** [Prefix] + [Word] + [Suffix]

**PT company name pool:**
- Prefixes: Ibero, Luso, Euro, Trans, Inter, Global, Nova, Primeira, Central, Atlântico, Digital, Smart, Prime, Core, Next
- Words: Soluções, Sistemas, Serviços, Tecnologia, Indústria, Comércio, Consultoria, Logística, Distribuição, Engenharia, Gestão, Capital, Parceiros
- Suffixes: Lda, SA, Unipessoal Lda, SRL, (leave blank for informal)

**Never** generate name matching a real registered company.

---

### Type 8 — IBANs / Bank Accounts
**Detection:** column name contains: iban, conta, account, bic, swift, nib
**Method:** Generate PT IBAN with valid check digits using fictional bank codes (0000-0009 range — not real PT banks).

**PT IBAN structure:** `PT50 + 4-digit bank + 4-digit branch + 11-digit account + 2 check`
**Real PT bank codes to NEVER use:** 0010 (CGD), 0033 (BPI), 0018 (Santander), 0036 (BCP/Millennium), 0019 (BIC/UBS), 0007 (Crédito Agrícola)
**Use:** 0000, 0001, 0002, 0003, 0004, 0005 (not allocated)

---

### Types 9–11 — Free-text PII risk, Date of birth, Health data

**Free-text PII risk** (any free-text column where users may paste sensitive info — `notes`, `description`, `comments`):
- Detection: type = Multiline Text, free-form, no validation.
- Method: regex sweep against the 8 patterns above; if matches found, anonymise inline; otherwise replace block with `[NOTAS REDIGIDAS]` placeholder of similar length.

**Date of birth** (`dob`, `data_nascimento`, `birthday`):
- Method: preserve year (if non-sensitive) but randomise month/day; OR shift entire date by ±30 days deterministically per record id.

**Health data** (any medical / clinical column):
- Method: replace with placeholder. Health data is typically out-of-scope for this pack — escalate to data-steward + compliance-officer if encountered.

---

## SYNTHETIC DATA GENERATION — Value Patterns

### Auto-number / Sequential codes
Format: `[PREFIX]-[YEAR]-[4-digit zero-padded sequence]`
Examples: QT-2024-0001, ORD-2024-0042, PRD-2024-0103
Prefix = first 2-3 letters of entity name (QT = Quote, ORD = Order, PRD = Product)

### Business entity names (for records, not companies)
Format: `[EntityPrefix] [Type] [Sequence]`
Examples: "Proposta Standard A", "Produto Premium 001", "Serviço Base Plus"

### Dates distribution
Normal records: spread over last 12 months (bias toward recent 3 months)
Historical records: spread over last 36 months
```javascript
function randomDate(daysBack = 365, recentBias = true) {
 const bias = recentBias ? Math.pow(Math.random, 2) : Math.random;
 const offset = Math.floor(bias * daysBack);
 const d = new Date;
 d.setDate(d.getDate - offset);
 return d.toISOString.split('T')[0];
}
```

### Integer quantities
Range: 1-500, skewed low (most records have 1-20 units)
```javascript
function randomQty(max = 500) {
 return Math.ceil(Math.pow(Math.random, 2) * max) || 1;
}
```

### Currency amounts
Domain-appropriate ranges:
- Unit prices: 10.00–50,000.00 (2 decimal places)
- Percentages/rates: 0.01–1.00 for decimal, 1–100 for percentage display
- Totals: derive from `unit_price × quantity` where possible

### Boolean fields
Active/valid/enabled flags: 85% True, 15% False
Approval flags: 60% True, 40% False
Deleted/archived flags: 5% True, 95% False

### Choice/status fields (normal data distribution)
Distribute proportionally: most common first
Example 4-state workflow: 40% Draft, 30% Submitted, 20% Approved, 10% Rejected
Ensure at least 2 records per valid state.

### FK columns
60% of child records reference top 30% of parent records (realistic distribution).
40% distributed across remaining parents.
Never generate FK value that doesn't exist in parent entity.

### GUID fields (for import reference only)
Format: `00000000-0000-0000-0000-[12-digit zero-padded sequence]`
Example: `00000000-0000-0000-0000-000000000001`
Note: Dataverse will replace on import.

---

## ANONYMISATION LOG FORMAT

When anonymisation is applied (typically during test-data preparation or in support of synthetic-data deliverables), log each transformation:

```
Entity: [schema_name]
Column: [schema_column_name] ([Display Name])
Sensitivity type: [Person Name / Email / Phone / NIF / Address / Financial / Company / IBAN / Free-text PII / DOB / Health]
Method applied: [brief description]
Records affected: [N]
Sample transformation (structure only, not actual values):
 Before: [pattern description, e.g., "Portuguese full name, 2 words"]
 After: [pattern description, e.g., "Fictional PT name from pool"]
 Example generated value: [one sample, e.g., "Rui Ferreira"]
```

These logs feed the `risks-and-assumptions` and `as-is` topic packs when the engagement deals with sensitive data that the team needs to handle in dev/test environments.
