# Rule: no vendor/product before Options phase

Lenses in Discovery (`business`, `operations`, `user`, `data`, `governance`, `financial`) MUST NOT name specific technology vendors or products. Examples of forbidden mentions in Discovery:

- "Power Platform", "Canvas Apps", "Model-driven Apps", "Power Automate", "Dataverse"
- "OutSystems", "Mendix"
- Specific connectors, services, products

What IS allowed in Discovery: identifying **digitalizable needs** without naming the digitalization technology. Examples:

- "Process requires mobile access" ✓
- "Process requires audit trail" ✓
- "Data lives in SharePoint today" ✓ (current state, not solution)
- "Process needs to integrate with SAP" ✓ (existing constraint)
- "Implement in Canvas Apps" ✗ (forbidden — premature solution naming)

Lens `technology` enters in the Options phase only. It is the one and only place to name vendors/products.
