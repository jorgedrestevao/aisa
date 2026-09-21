# Anonymisation Rules and Synthetic-Data Generation

<!--
provenance: RUNTIME (domain knowledge) · class: CRAFT
authored: 2026-09-04 (Step 4B) · design authority: Step 4A — Domain Knowledge Runtime Model
Not an Options D3 pull target.
-->

Engagement and delivery practice. No independent research authority. This file must not state a platform
limit, threshold or comparative claim as fact; where one is required it refers to the RESEARCH unit that
owns it.

**Where it is used:** test-data preparation for non-production environments, and synthetic-data support for
prototypes and demos. The **detection signals** are also useful earlier, when surfacing Risky or Confirmed
rows about data sensitivity — they name no vendors or products.

**Locale:** the pools below are Portuguese / English bilingual; adapt per engagement.

The 11 sensitivity types enumerated here are this pack's own typing. Which roles may see which typed column
is a separate artefact: [`security-craft.md`](security-craft.md) § Matrix 3. Whether a given class of data
may leave production at all is a compliance input to the engagement, not a decision this file makes.

---

## ANONYMISATION METHODS BY DATA TYPE

### Type 1 — Person names
**Detection signals:** column name contains: name, nome, primeiro, apelido, contacto, responsavel, gestor, owner, contact
**Method:** Replace with a fictional name from the same language pool. Match word count (2→2, 3→3).
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
**Content hint:** contains the @ symbol
**Method:** `[firstname].[lastname]@demo.com` (lowercase, no accents)
**Never reuse** the same email in the same entity.

---

### Type 3 — Phone numbers
**Detection:** column name contains: phone, tel, telef, mobile, telem, fax, contact
**Content hint:** digit strings 9–15 chars
**Method:** Preserve format (length, separators, country code), replace all digits after the country code.

**PT mobile format:** `9[1|2|3|6][random 7 digits]` — e.g. 912345678
**PT landline format:** `2[1-9][random 7 digits]` — e.g. 212345678
**International:** `+[code] [preserve grouping, replace digits]`

---

### Type 4 — NIFs / tax IDs
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

**Portuguese NIPC (company — starts with 5):** same algorithm, first digit = 5.

**Never use** real bank codes or known company NIFs.

---

### Type 5 — Addresses / moradas
**Detection:** column name contains: morada, address, rua, street, av, avenida, largo, praca, cidade, city, cp, postal, zip, localidade
**Method:** Fictional street + real city (same region if detectable) + fictional postal code (format preserved).

**PT street pool:** Rua das Flores, Avenida da Liberdade, Rua do Comércio, Travessa da Saudade, Largo do Município, Rua de Santo António, Avenida de Roma, Rua dos Anjos, Travessa do Carmo, Rua da Prata, Avenida Almirante Reis, Rua Augusta, Rua do Ouro, Praça do Comércio, Rua da Conceição
**PT cities:** Lisboa, Porto, Coimbra, Braga, Aveiro, Setúbal, Faro, Évora, Viseu, Leiria, Santarém, Viana do Castelo, Castelo Branco, Beja, Portalegre
**PT postal code format:** `XXXX-XXX` (generate: 1000–9999 for the first part, 001–999 for the second)

---

### Type 6 — Financial values
**Detection:** column name contains: valor, value, amount, preco, price, total, saldo, margin, margem, receita, revenue, custo, cost, desconto, discount, orcamento, budget, fee, taxa
**Method:** `anonymised = original × (0.80 + random × 0.40)` — ±20% variation
**Rules:**
- Preserve sign (positive stays positive)
- Preserve the decimal-place format
- Preserve order of magnitude (hundreds stay in hundreds, millions stay in millions)
- 0 stays 0
- Never round to a suspiciously clean number

---

### Type 7 — Company names
**Detection:** column name contains: empresa, company, cliente, customer, fornecedor, supplier, parceiro, partner, organizacao, entidade
**Method:** [Prefix] + [Word] + [Suffix]

**PT company name pool:**
- Prefixes: Ibero, Luso, Euro, Trans, Inter, Global, Nova, Primeira, Central, Atlântico, Digital, Smart, Prime, Core, Next
- Words: Soluções, Sistemas, Serviços, Tecnologia, Indústria, Comércio, Consultoria, Logística, Distribuição, Engenharia, Gestão, Capital, Parceiros
- Suffixes: Lda, SA, Unipessoal Lda, SRL, (leave blank for informal)

**Never** generate a name matching a real registered company.

---

### Type 8 — IBANs / bank accounts
**Detection:** column name contains: iban, conta, account, bic, swift, nib
**Method:** Generate a PT IBAN with valid check digits using fictional bank codes (the unallocated
`0000`–`0009` range — never a real bank's code).

**PT IBAN structure:** `PT50 + 4-digit bank + 4-digit branch + 11-digit account + 2 check`
**Rule:** verify the code you use is unallocated before generating a batch; never reuse a code you have seen
on a real statement.
**Use:** 0000, 0001, 0002, 0003, 0004, 0005.

---

### Types 9–11 — Free-text PII risk, date of birth, health data

**Free-text PII risk** (any free-text column where users may paste sensitive info — `notes`, `description`, `comments`):
- Detection: multiline text, free-form, no validation.
- Method: regex sweep against the 8 patterns above; if matches are found, anonymise inline; otherwise
  replace the block with a `[NOTAS REDIGIDAS]` placeholder of similar length.

**Date of birth** (`dob`, `data_nascimento`, `birthday`):
- Method: preserve the year (where the year itself is not sensitive) but randomise month/day; OR shift the
  whole date by ±30 days deterministically per record id.

**Health data** (any medical / clinical column):
- Method: replace with a placeholder. Health data is typically out of scope for this pack — escalate to the
  data-steward and compliance-officer lenses if encountered.

---

## SYNTHETIC DATA GENERATION — value patterns

### Auto-number / sequential codes
Format: `[PREFIX]-[YEAR]-[4-digit zero-padded sequence]`
Examples: QT-2024-0001, ORD-2024-0042, PRD-2024-0103
Prefix = first 2–3 letters of the entity name (QT = Quote, ORD = Order, PRD = Product)

### Business entity names (for records, not companies)
Format: `[EntityPrefix] [Type] [Sequence]`
Examples: "Proposta Standard A", "Produto Premium 001", "Serviço Base Plus"

### Dates distribution
Normal records: spread over the last 12 months (bias toward the recent 3 months)
Historical records: spread over the last 36 months
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
Range: 1–500, skewed low (most records have 1–20 units)
```javascript
function randomQty(max = 500) {
 return Math.ceil(Math.pow(Math.random, 2) * max) || 1;
}
```

### Monetary amounts (synthetic ranges)
Domain-appropriate ranges, dimensionless:
- Unit values: 10.00–50,000.00 (2 decimal places)
- Percentages/rates: 0.01–1.00 as decimal, 1–100 for percentage display
- Totals: derive from `unit_value × quantity` wherever possible, so the arithmetic still reconciles

### Boolean fields
Active/valid/enabled flags: 85% True, 15% False
Approval flags: 60% True, 40% False
Deleted/archived flags: 5% True, 95% False

### Choice/status fields (normal distribution)
Distribute proportionally, most common first.
Example 4-state workflow: 40% Draft, 30% Submitted, 20% Approved, 10% Rejected.
Ensure at least 2 records per valid state — an unrepresented state is an untested state.

### FK columns
60% of child records reference the top 30% of parent records (realistic skew).
40% distributed across the remaining parents.
Never generate an FK value that does not exist in the parent entity.

### GUID fields (for import correlation only)
Format: `00000000-0000-0000-0000-[12-digit zero-padded sequence]`
Example: `00000000-0000-0000-0000-000000000001`
Note: treat these as correlation keys for the import only — the target store may assign its own identifiers,
so never carry a generated GUID into a spec as if it were the record's real key.

---

## ANONYMISATION LOG FORMAT

When anonymisation is applied, log each transformation:

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

The log names the *pattern*, never a real value — a log that quotes the original defeats the exercise.

These logs feed the `risks-and-assumptions` and `as-is` topic packs when the engagement handles sensitive
data that the team must work with in dev/test environments.
