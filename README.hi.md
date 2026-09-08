<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.md">English</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/accessibility-suite/readme.png" alt="Accessibility Suite" width="400">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/accessibility-suite/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/accessibility-suite/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/accessibility-suite/"><img src="https://img.shields.io/badge/Landing_Page-live-blue" alt="Landing Page"></a>
</p>

छह उपकरण। एक लक्ष्य: एक्सेसिबिलिटी परीक्षण को सत्यापित, स्वचालित और अनदेखा करना मुश्किल बनाना।

> **स्रोत से चलाएं।** इस सूट में कुछ भी अभी तक npm या PyPI पर प्रकाशित नहीं किया गया है। नीचे दिए गए प्रत्येक कमांड इस रिपॉजिटरी से इंस्टॉल करता है। प्रत्येक उपकरण के `package.json` और `pyproject.toml` में पैकेज के नाम इच्छित प्रकाशित नाम हैं, न कि ऐसे लिंक जिन्हें आप आज इंस्टॉल कर सकते हैं।

---

## एक नज़र में

अधिकांश एक्सेसिबिलिटी उपकरण "आपके पास 12 उल्लंघन हैं" पर रुक जाते हैं। एक्सेसिबिलिटी सूट आगे बढ़ता है: यह परीक्षण किए गए डेटा का छेड़छाड़-रोधी प्रमाण कैप्चर करता है, रिग्रेशन पर आपकी CI पाइपलाइन को नियंत्रित करता है, और कम दृष्टि, स्क्रीन-रीडर, डिस्लेक्सिया और संज्ञानात्मक-भार प्रोफाइल के लिए अनुकूलित सुधार मार्गदर्शन प्रदान करता है।

यह सूट पूरे जीवनचक्र को कवर करता है - एक्सेसिबल पैटर्न के लिए CLI आउटपुट को लिंट करें, क्रिप्टोग्राफ़िक उत्पत्ति के साथ WCAG उल्लंघनों के लिए HTML को स्कैन करें, CI में गुणवत्ता नियंत्रण लागू करें, और MCP के माध्यम से सब कुछ उजागर करें ताकि AI सहायक सुधार प्रक्रिया में भाग ले सकें।

**मुख्य सिद्धांत:**

- **दावों से अधिक प्रमाण** - प्रत्येक निष्कर्ष SHA-256 अखंडता डाइजेस्ट के साथ एक प्रोव-स्पेक उत्पत्ति रिकॉर्ड द्वारा समर्थित है
- **कम-दृष्टि-प्रथम आउटपुट** - सभी CLI उपकरण `[OK]/[WARN]/[FAIL] + What/Why/Fix` अनुबंध का उपयोग करते हैं
- **निर्धारित** - समान इनपुट हमेशा समान आउटपुट उत्पन्न करता है; कोई नेटवर्क कॉल नहीं, कोई यादृच्छिकता नहीं
- **CI-नेटिव** - स्वचालित पाइपलाइनों के लिए डिज़ाइन किए गए निकास कोड, स्कोरकार्ड JSON और PR टिप्पणियाँ

---

## परियोजनाएँ

| परियोजना | विवरण | स्टैक | वितरण |
|---------|-------------|-------|--------------|
| [a11y-lint](src/a11y-lint/) | CLI आउटपुट के लिए एक्सेसिबिलिटी लिंटर - यह सत्यापित करता है कि त्रुटि संदेश एक्सेसिबल पैटर्न का पालन करते हैं | Python 3.10+ | केवल स्रोत |
| [a11y-ci](src/a11y-ci/) | रिग्रेशन डिटेक्शन और अनुमति सूचियों के साथ एक्सेसिबिलिटी स्कोरकार्ड के लिए CI गेट | Python 3.10+ | केवल स्रोत |
| [a11y-assist](src/a11y-assist/) | पांच एक्सेसिबिलिटी प्रोफाइल के साथ कम-दृष्टि-प्रथम CLI सहायक | Python 3.10+ | केवल स्रोत |
| [a11y-evidence-engine](src/a11y-evidence-engine/) | हेडलेस HTML स्कैनर जिसमें प्रोव-स्पेक उत्पत्ति रिकॉर्ड होते हैं | Node.js 18+ | केवल स्रोत |
| [a11y-mcp-tools](src/a11y-mcp-tools/) | एक्सेसिबिलिटी प्रमाण कैप्चर और निदान के लिए MCP सर्वर | Node.js 18+ | केवल स्रोत |
| [a11y-demo-site](examples/a11y-demo-site/) | एंड-टू-एंड परीक्षण के लिए जानबूझकर उल्लंघनों के साथ डेमो साइट | HTML | -- |

---

## त्वरित शुरुआत

### एक्सेसिबल पैटर्न के लिए CLI आउटपुट को लिंट करें

```bash
pip install a11y-lint
a11y-lint scan output.txt
```

### एक्सेसिबिलिटी रिग्रेशन पर अपनी CI को नियंत्रित करें

```bash
pip install ./src/a11y-lint ./src/a11y-ci
a11y-lint scan . --artifact-dir .a11y_artifacts
a11y-ci gate --artifact-dir .a11y_artifacts
```

### HTML को स्कैन करें और उत्पत्ति को कैप्चर करें

```bash
npm --prefix src/a11y-evidence-engine install
node src/a11y-evidence-engine/bin/a11y-engine.js scan ./html --out ./results
```

### CLI विफलता के लिए सुधार मार्गदर्शन प्राप्त करें

```bash
pip install ./src/a11y-assist
a11y-assist explain --json error.json --profile screen-reader
```

### MCP के माध्यम से प्रमाण कैप्चर करें और निदान करें

```bash
npm --prefix src/a11y-mcp-tools install
node src/a11y-mcp-tools/bin/cli.js evidence --target page.html --dom-snapshot --out evidence.json
node src/a11y-mcp-tools/bin/cli.js diagnose --bundle evidence.json --verify-provenance --fix
```

### एंड-टू-एंड डेमो साइट चलाएं

```bash
cd examples/a11y-demo-site
./scripts/a11y.sh
```

### स्थानीय रूप से सभी परीक्षण चलाएं

```bash
npm test
# or
./scripts/verify.sh
```

यह तीन पायथन परियोजनाओं के लिए pytest, दो Node.js परियोजनाओं के लिए npm test चलाता है, और हैंडबुक को सत्यापित करता है।

---

## आर्किटेक्चर

छह उपकरण पहचान से लेकर सुधार तक एक पाइपलाइन बनाते हैं:

```
                        CLI output                HTML files
                            |                         |
                    +-------v-------+        +--------v---------+
                    |   a11y-lint   |        | a11y-evidence-   |
                    | (scan & score)|        | engine (scan +   |
                    +-------+-------+        | provenance)      |
                            |                +--------+---------+
                  scorecard.json                      |
                            |               evidence bundle
                    +-------v-------+                 |
                    |    a11y-ci    |        +---------v---------+
                    |  (CI gate +  |        |  a11y-mcp-tools   |
                    |  PR comment) |        | (MCP evidence +   |
                    +-------+-------+        |  diagnosis)      |
                            |                +---------+---------+
                    pass / fail                        |
                            |                  findings + fixes
                    +-------v-------+                 |
                    |  a11y-assist  |<----------------+
                    | (fix guidance |
                    |  5 profiles)  |
                    +---------------+
```

**डेटा प्रवाह:**

1. **a11y-lint** एक्सेसिबल त्रुटि संदेश पैटर्न के लिए CLI टेक्स्ट को स्कैन करता है और एक स्कोरकार्ड उत्पन्न करता है
2. **a11y-evidence-engine** HTML फ़ाइलों को स्कैन करता है और प्रोव-स्पेक उत्पत्ति रिकॉर्ड के साथ निष्कर्ष उत्पन्न करता है
3. **a11y-ci** स्कोरकार्ड का उपयोग करता है, थ्रेशोल्ड लागू करता है, रिग्रेशन का पता लगाता है और PR टिप्पणियाँ उत्पन्न करता है
4. **a11y-mcp-tools** AI सहायक एकीकरण के लिए MCP उपकरणों के रूप में प्रमाण कैप्चर और निदान को लपेटता है
5. **a11y-assist** निष्कर्ष (संरचित JSON या कच्चा पाठ) लेता है और पांच एक्सेसिबिलिटी प्रोफाइल में सुधार मार्गदर्शन उत्पन्न करता है
6. **a11y-demo-site** इसे जानबूझकर उल्लंघनों के साथ एक चलाने योग्य उदाहरण के रूप में एक साथ जोड़ता है

**साझा अनुबंध:**

- `cli.error.schema.v0.1.json` - सभी पायथन उपकरणों में संरचित त्रुटि प्रारूप
- `evidence.bundle.schema.v0.1.json` - उत्पत्ति श्रृंखलाओं के साथ प्रमाण बंडल
- `.a11y_artifacts/` - CI पाइपलाइनों के लिए एकीकृत कलाकृति निर्देशिका
- प्रोव-स्पेक विधि आईडी - प्रत्येक उत्पत्ति चरण के लिए स्थिर, संस्करणित पहचानकर्ता

---

## MCP क्लाइंट कॉन्फ़िगरेशन

a11y-mcp-tools को अपने MCP क्लाइंट (Claude Desktop, Cursor, VS Code, आदि) से कनेक्ट करने के लिए:

```json
{
  "mcpServers": {
    "a11y": {
      "command": "node",
      "args": ["/absolute/path/to/accessibility-suite/src/a11y-mcp-tools/bin/server.js"]
    }
  }
}
```

या, `npm --prefix src/a11y-mcp-tools link` के बाद:

```json
{
  "mcpServers": {
    "a11y": {
      "command": "a11y-mcp"
    }
  }
}
```

सर्वर दो उपकरण उजागर करता है:

| उपकरण | विवरण |
|------|-------------|
| `a11y.evidence` | HTML, CLI लॉग या अन्य इनपुट से छेड़छाड़-रोधी प्रमाण बंडल कैप्चर करें |
| `a11y.diagnose` | उत्पत्ति सत्यापन के साथ प्रमाण बंडलों पर WCAG नियम जांच चलाएं |

---

## CI एकीकरण (GitHub Actions)

```yaml
jobs:
  accessibility:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Scan code
        run: |
          pip install a11y-lint
          mkdir .a11y_artifacts
          a11y-lint scan . --artifact-dir .a11y_artifacts

      - uses: mcp-tool-shop-org/accessibility-suite/.github/actions/a11y-ci@main
        with:
          artifact-dir: .a11y_artifacts
          fail-on: serious
```

Azure DevOps उदाहरणों और समस्या निवारण के लिए [GETTING_STARTED.md](GETTING_STARTED.md) देखें।

---

## प्रलेखन

| दस्तावेज़ | विवरण |
|----------|-------------|
| [HANDBOOK.md](HANDBOOK.md) | आर्किटेक्चर गहन गोता, एकीकरण पैटर्न और विकास मार्गदर्शिका |
| [GETTING_STARTED.md](GETTING_STARTED.md) | तीन-कमांड स्थानीय सेटअप, CI टेम्पलेट और समस्या निवारण |
| [CHANGELOG.md](CHANGELOG.md) | कीप अ चेंजलॉग प्रारूप में रिलीज़ इतिहास |
| [docs/unified-artifacts.md](docs/unified-artifacts.md) | एकीकृत कलाकृति निर्देशिका रणनीति |
| [docs/prov-spec/](docs/prov-spec/) | उत्पत्ति विनिर्देश |

---

## सुरक्षा और डेटा दायरा

- **पहुंची गई डेटा:** एक्सेसिबिलिटी विश्लेषण के लिए HTML फ़ाइलों, CLI आउटपुट और स्कोरकार्ड JSON को पढ़ता है। DOM स्नैपशॉट कैप्चर करता है और प्रमाण बंडल उत्पन्न करता है।
- **पहुंची गई डेटा नहीं:** कोई नेटवर्क अनुरोध नहीं। कोई टेलीमेट्री नहीं। कोई उपयोगकर्ता डेटा संग्रहण नहीं। कोई क्रेडेंशियल या टोकन नहीं।
- **आवश्यक अनुमतियाँ:** लक्ष्य फ़ाइलों तक पढ़ने की पहुंच। प्रमाण/कलाकृति आउटपुट निर्देशिकाओं के लिए लिखने की पहुंच।

## स्कोरकार्ड

| गेट | स्थिति |
|------|--------|
| A. सुरक्षा आधारभूत | पास |
| B. त्रुटि प्रबंधन | पास |
| C. ऑपरेटर दस्तावेज़ | पास |
| D. शिपिंग स्वच्छता | पास |
| E. पहचान | पास |

## लाइसेंस

[MIT](LICENSE)

---

MCP टूल शॉप द्वारा निर्मित
