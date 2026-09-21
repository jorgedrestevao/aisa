# Power Platform Governance Framework

Generated: 2026-09-03  
Status: Draft for organisational approval  

This folder contains ten production-formatted, editable Word documents generated from the canonical Power Platform research evidence. The `.docx` files are policy drafts, not approved organisational policy. Review all named roles, approval authorities, SLAs, retention periods, licensing assumptions, and volatile platform behaviour before adoption.

## Documents

1. Governance Charter
2. Engineering Standards
3. Mandatory Control Policy
4. Delivery and Release Process
5. Environment and Access Standard
6. Application Lifecycle Standard
7. Governance Exception Process
8. Governance Operations Runbook
9. Architecture Decision Record Template
10. Application Architecture Standard

## Regeneration

The documents are generated with JavaScript and the pinned `docx` package.

```powershell
npm install
npm run build
npm run validate
```

`generate-governance-docs.js` contains the content and visual design system. Existing generated `.docx` files with the listed names are replaced.
