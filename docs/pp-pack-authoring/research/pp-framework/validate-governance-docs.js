const fs = require("fs");
const path = require("path");
const JSZip = require("jszip");

const required = ["[Content_Types].xml", "_rels/.rels", "word/document.xml", "word/styles.xml"];

(async () => {
  const files = fs.readdirSync(__dirname).filter(f => /^\d\d-.*\.docx$/i.test(f)).sort();
  if (files.length !== 10) throw new Error(`Expected 10 documents, found ${files.length}`);
  for (const file of files) {
    const data = fs.readFileSync(path.join(__dirname, file));
    const zip = await JSZip.loadAsync(data);
    for (const part of required) if (!zip.file(part)) throw new Error(`${file}: missing ${part}`);
    const xml = await zip.file("word/document.xml").async("string");
    if (!xml.includes("Governance") && !xml.includes("Power Platform")) throw new Error(`${file}: expected content absent`);
    if (!xml.includes("Draft for organisational approval")) throw new Error(`${file}: status absent`);
    console.log(`VALID  ${file}  ${(data.length / 1024).toFixed(1)} KB`);
  }
})().catch(err => { console.error(err); process.exit(1); });
