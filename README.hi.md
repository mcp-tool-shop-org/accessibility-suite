<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.md">English</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/accessibility-suite/readme.png" alt="Accessibility Suite" width="400">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/accessibility-suite/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/accessibility-suite/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://www.npmjs.com/package/@mcptoolshop/accessibility-suite"><img src="https://img.shields.io/npm/v/@mcptoolshop/accessibility-suite" alt="npm"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/accessibility-suite/"><img src="https://img.shields.io/badge/Landing_Page-live-blue" alt="Landing Page"></a>
</p>

छह उपकरण। एक लक्ष्य: पहुंच परीक्षण को सत्यापन योग्य, स्वचालित और अनदेखा करने में मुश्किल बनाना।

---

## एक नज़र में

अधिकांश पहुंच उपकरण "आपके पास 12 उल्लंघन हैं" तक ही सीमित रहते हैं। एक्सेसिबिलिटी सूट इससे आगे जाता है: यह परीक्षण किए गए डेटा का छेड़छाड़-रोधी प्रमाण एकत्र करता है, आपके CI पाइपलाइन में प्रतिगमन (regression) को रोकता है, और कम दृष्टि वाले, स्क्रीन रीडर, डिस्लेक्सिया (dyslexia) और संज्ञानात्मक भार (cognitive-load) प्रोफाइल के लिए अनुकूलित समाधान प्रदान करता है।

यह सूट पूरे जीवनचक्र को कवर करता है - सुलभ पैटर्न के लिए CLI आउटपुट का विश्लेषण करता है, WCAG उल्लंघनों के लिए HTML को स्कैन करता है जिसमें क्रिप्टोग्राफिक प्रमाण होता है, CI में गुणवत्ता नियंत्रण लागू करता है, और सब कुछ MCP के माध्यम से प्रदर्शित करता है ताकि AI सहायक इसमें भाग ले सकें।

**मुख्य सिद्धांत:**

- **दावों से अधिक प्रमाण:** प्रत्येक निष्कर्ष एक SHA-256 अखंडता डाइजेस्ट (integrity digests) के साथ एक प्रामाणिक रिकॉर्ड द्वारा समर्थित है।
- **कम दृष्टि वाले उपयोगकर्ताओं के लिए प्राथमिकता:** सभी CLI उपकरण `[OK]/[WARN]/[FAIL] + What/Why/Fix` प्रारूप का उपयोग करते हैं।
- **निश्चित:** समान इनपुट हमेशा समान आउटपुट उत्पन्न करता है; कोई नेटवर्क कॉल नहीं, कोई यादृच्छिकता नहीं।
- **CI-अनुकूल:** स्वचालित पाइपलाइन के लिए डिज़ाइन किए गए एग्जिट कोड, स्कोरकार्ड JSON और PR टिप्पणियां।

---

## परियोजनाएं

| परियोजना | विवरण | स्टैक | पैकेज |
|---------|-------------|-------|---------|
| [a11y-lint](src/a11y-lint/) | CLI आउटपुट के लिए एक्सेसिबिलिटी लिंटर - त्रुटि संदेशों को मान्य करता है ताकि वे सुलभ पैटर्न का पालन करें। | Python 3.10+ | [PyPI](https://pypi.org/project/a11y-lint/) |
| [a11y-ci](src/a11y-ci/) | एक्सेसिबिलिटी स्कोरकार्ड के लिए CI गेट, जिसमें प्रतिगमन का पता लगाना और अनुमति सूची शामिल है। | Python 3.10+ | [PyPI](https://pypi.org/project/a11y-ci/) / [npm](https://www.npmjs.com/package/@mcptoolshop/a11y-ci) |
| [a11y-assist](src/a11y-assist/) | पांच एक्सेसिबिलिटी प्रोफाइल के साथ कम दृष्टि वाले उपयोगकर्ताओं के लिए CLI सहायक। | Python 3.10+ | [PyPI](https://pypi.org/project/a11y-assist/) |
| [a11y-evidence-engine](src/a11y-evidence-engine/) | प्रमाण-आधारित रिकॉर्ड के साथ हेडलेस HTML स्कैनर। | Node.js 18+ | [npm](https://www.npmjs.com/package/@mcptoolshop/a11y-evidence-engine) |
| [a11y-mcp-tools](src/a11y-mcp-tools/) | एक्सेसिबिलिटी प्रमाण कैप्चर और निदान के लिए MCP सर्वर। | Node.js 18+ | [npm](https://www.npmjs.com/package/@mcptoolshop/a11y-mcp-tools) |
| [a11y-demo-site](examples/a11y-demo-site/) | एंड-टू-एंड परीक्षण के लिए जानबूझकर उल्लंघनों वाली डेमो साइट। | HTML | -- |

---

## शुरुआत कैसे करें

### सुलभ पैटर्न के लिए CLI आउटपुट का विश्लेषण करें।

```bash
pip install a11y-lint
a11y-lint scan output.txt
```

### एक्सेसिबिलिटी प्रतिगमन पर अपने CI को रोकें।

```bash
pip install a11y-ci
a11y-lint scan . --artifact-dir .a11y_artifacts
a11y-ci gate --artifact-dir .a11y_artifacts
```

### HTML को स्कैन करें और प्रमाण कैप्चर करें।

```bash
npm install -g @mcptoolshop/a11y-evidence-engine
a11y-engine scan ./html --out ./results
```

### CLI विफलता के लिए समाधान प्राप्त करें।

```bash
pip install a11y-assist
a11y-assist explain --json error.json --profile screen-reader
```

### MCP के माध्यम से प्रमाण कैप्चर करें और निदान करें।

```bash
npm install -g @mcptoolshop/a11y-mcp-tools
a11y evidence --target page.html --dom-snapshot --out evidence.json
a11y diagnose --bundle evidence.json --verify-provenance --fix
```

### डेमो साइट को एंड-टू-एंड चलाएं।

```bash
cd examples/a11y-demo-site
./scripts/a11y.sh
```

---

## आर्किटेक्चर

ये छह उपकरण एक पाइपलाइन का निर्माण करते हैं जो पता लगाने से लेकर समाधान तक है:

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

1. **a11y-lint** CLI टेक्स्ट को स्कैन करता है ताकि सुलभ त्रुटि संदेश पैटर्न का पता चल सके और एक स्कोरकार्ड उत्पन्न करता है।
2. **a11y-evidence-engine** HTML फ़ाइलों को स्कैन करता है और प्रमाण-आधारित रिकॉर्ड के साथ निष्कर्ष जारी करता है।
3. **a11y-ci** स्कोरकार्ड का उपयोग करता है, सीमाएं लागू करता है, प्रतिगमन का पता लगाता है और PR टिप्पणियां उत्पन्न करता है।
4. **a11y-mcp-tools** प्रमाण कैप्चर और निदान को MCP उपकरणों के रूप में लपेटता है ताकि AI सहायक को एकीकृत किया जा सके।
5. **a11y-assist** निष्कर्षों (संरचित JSON या कच्चे पाठ) को लेता है और पांच एक्सेसिबिलिटी प्रोफाइल में समाधान प्रदान करता है।
6. **a11y-demo-site** इसे एक रननेबल उदाहरण के रूप में जोड़ता है जिसमें जानबूझकर उल्लंघन शामिल हैं।

**साझा अनुबंध:**

- `cli.error.schema.v0.1.json` - सभी Python उपकरणों में संरचित त्रुटि प्रारूप।
- `evidence.bundle.schema.v0.1.json` - प्रमाण श्रृंखला के साथ प्रमाण बंडल।
- `.a11y_artifacts/` - CI पाइपलाइन के लिए एकीकृत आर्टिफैक्ट निर्देशिका।
- prov-spec विधि आईडी - प्रत्येक प्रमाण चरण के लिए स्थिर, संस्करणित पहचानकर्ता।

---

## MCP क्लाइंट कॉन्फ़िगरेशन

अपने MCP क्लाइंट (क्लाउड डेस्कटॉप, कर्सर, VS कोड, आदि) से a11y-mcp-tools को कनेक्ट करने के लिए:

```json
{
  "mcpServers": {
    "a11y": {
      "command": "npx",
      "args": ["-y", "@mcptoolshop/a11y-mcp-tools"]
    }
  }
}
```

या यदि इसे वैश्विक रूप से स्थापित किया गया है:

```json
{
  "mcpServers": {
    "a11y": {
      "command": "a11y-mcp"
    }
  }
}
```

सर्वर दो उपकरण प्रदान करता है:

| उपकरण | विवरण |
|------|-------------|
| `a11y.evidence` | HTML, CLI लॉग या अन्य इनपुट से छेड़छाड़-रोधी प्रमाण बंडल कैप्चर करें। |
| `a11y.diagnose` | प्रमाण सत्यापन के साथ प्रमाण बंडल पर WCAG नियमों की जांच करें। |

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

Azure DevOps के उदाहरणों और समस्या निवारण के लिए, [GETTING_STARTED.md](GETTING_STARTED.md) देखें।

---

## दस्तावेज़

| दस्तावेज़ | विवरण |
|----------|-------------|
| [HANDBOOK.md](HANDBOOK.md) | आर्किटेक्चर की गहन जानकारी, एकीकरण पैटर्न और विकास गाइड। |
| [GETTING_STARTED.md](GETTING_STARTED.md) | तीन कमांड के साथ स्थानीय सेटअप, CI टेम्प्लेट और समस्या निवारण। |
| [CHANGELOG.md](CHANGELOG.md) | 'कीप अ चेंजलॉग' प्रारूप में रिलीज़ इतिहास। |
| [docs/unified-artifacts.md](docs/unified-artifacts.md) | एकीकृत आर्टिफैक्ट निर्देशिका रणनीति। |
| [docs/prov-spec/](docs/prov-spec/) | उत्पत्ति विनिर्देश। |

---

## सुरक्षा और डेटा दायरा।

- **पहुंचे जाने वाले डेटा:** पहुंच विश्लेषण के लिए HTML फ़ाइलें, CLI आउटपुट और स्कोरकार्ड JSON पढ़े जाते हैं। DOM स्नैपशॉट कैप्चर किए जाते हैं और साक्ष्य बंडल उत्पन्न किए जाते हैं।
- **पहुंचे जाने वाले डेटा नहीं:** कोई नेटवर्क अनुरोध नहीं। कोई टेलीमेट्री नहीं। कोई उपयोगकर्ता डेटा भंडारण नहीं। कोई क्रेडेंशियल या टोकन नहीं।
- **आवश्यक अनुमतियाँ:** लक्षित फ़ाइलों तक पढ़ने की पहुंच। साक्ष्य/आर्टिफैक्ट आउटपुट निर्देशिकाओं के लिए लिखने की पहुंच।

## स्कोरकार्ड

| गेट | स्थिति |
|------|--------|
| ए. सुरक्षा आधारभूत संरचना | पास |
| बी. त्रुटि प्रबंधन | पास |
| सी. ऑपरेटर दस्तावेज़ | पास |
| डी. शिपिंग स्वच्छता | पास |
| ई. पहचान | पास |

## लाइसेंस

[MIT](LICENSE)

---

<a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a> द्वारा निर्मित।
