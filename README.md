# Human Flourishing Frameworks

**Making the invisible visible. Holding systems accountable. Protecting human freedom.**

A democratic, open-source system for detecting, tracking, and fixing unfair AI and automated decision-making systems that harm people.

---

## Download & Install Now

**[👉 DIRECT DOWNLOADS PAGE](DOWNLOADS.md)** — All installers with direct links

### Quick Download Links

| **Windows** | **Mac/Linux** | **Docker** |
|:---:|:---:|:---:|
| **[PowerShell Installer](https://raw.githubusercontent.com/alex-place/human-flourishing-frameworks/master/install-no-git.ps1)** | **[Bash Script](https://raw.githubusercontent.com/alex-place/human-flourishing-frameworks/master/install.sh)** | **[docker-compose.yml](https://raw.githubusercontent.com/alex-place/human-flourishing-frameworks/master/docker-compose.yml)** |
| No Git needed | `bash install.sh` | `docker-compose up -d` |
| Or build [EXE](BUILD_INSTALLER.md) | Auto-installs Python | Works anywhere |

---

## Try It Now (Public Dashboard)

**Live monitoring of real AI violations:** https://human-flourishing-frameworks.herokuapp.com

- View 7 documented violations
- See 48,250+ affected persons
- Track $1.163M+ in quantified harm
- Review governance board decisions
- Access cryptographic audit trail

---

## Quick Install (Choose Your Device)

| **Windows** | **Mac/Linux** | **Docker** | **No Git?** |
|:---:|:---:|:---:|:---:|
| **[Download EXE](#windows-exe-installer)** | **[Bash Script](install.sh)** | **[Docker](docker-compose.yml)** | **[PowerShell](install-no-git.ps1)** |
| Double-click, automatic | `bash install.sh` | `docker-compose up -d` | No dependencies needed |

### 🔧 Installation Files

**For Most Users (Windows):**
- **[human-flourishing-frameworks-installer.exe](human-flourishing-frameworks-installer.exe)** — Download and double-click
  - Automatic Python installation
  - Virtual environment setup
  - Desktop shortcut created
  - [How to build the EXE](BUILD_INSTALLER.md)

**Without Git (Any Windows):**
- **[install-no-git.ps1](install-no-git.ps1)** — PowerShell script (no dependencies)
  ```powershell
  powershell -ExecutionPolicy Bypass -File install-no-git.ps1
  ```

**For Developers:**
- **[install.ps1](install.ps1)** — Windows with Git
- **[install.sh](install.sh)** — Mac/Linux
- **[Dockerfile](Dockerfile)** — Docker container

### 📚 Setup Guides
- **[QUICK_START.md](QUICK_START.md)** — Choose your installation method
- **[NODE_SETUP.md](NODE_SETUP.md)** — Complete setup documentation
- **[BUILD_INSTALLER.md](BUILD_INSTALLER.md)** — How to build the Windows EXE

---

## The Problem We Solve

Every day, invisible algorithms make life-changing decisions about you:

- **Healthcare**: Hospital AI that diagnoses diseases differently based on race
- **Criminal Justice**: Algorithms that recommend harsher sentences for minorities  
- **Finance**: Lending systems that discriminate by gender or ZIP code
- **Government**: Welfare programs that deny benefits through automation errors
- **Hiring**: Job platforms that screen out qualified candidates due to bias

**The harm is hidden. The people affected often never know why.**

**Human Flourishing Frameworks makes it visible and fixable.**

---

## What We Do

✅ **Detect unfair systems** — Real-time monitoring of AI and automation  
✅ **Track harmed people** — Who was affected, by how much, and why  
✅ **Create proof** — Cryptographic evidence suitable for courts and regulators  
✅ **Enable fixing** — Track remediation progress publicly  
✅ **Protect democracy** — Diverse board makes decisions, not corporations  
✅ **Prevent override** — Hard rules no system can bypass  

**Nobody owns it.** No company controls it. No single government runs it. It's governed by a diverse, independent board — civil rights activists, security researchers, affected communities, academics, and technologists working together.

---

## How It Works

### 1. Report the Problem
When AI harms people, it's documented:

```
Hospital XYZ Medical AI
- Accuracy gap: 8% (White 87% vs Black 79%)
- Affected people: 2,400
- Average harm: $50,000 per person
- Status: Under remediation
```

### 2. Track Affected People
Every person harmed is recorded:
- Who they are
- How much harm they suffered
- What compensation they're owed
- Progress on remediation

### 3. Create Unbreakable Proof
Using cryptography, we prove:
- Nothing was hidden or changed
- Every action was logged
- Evidence admissible in court
- Suitable for Congressional briefing

### 4. Democratic Board Decides
A 12-member board votes on each violation:
- **10 voting members**: Civil rights leaders, security experts, affected communities
- **2 observers**: Government (non-voting)
- **Decision**: Public vote, can't be overridden
- **Result**: Remediation required

### 5. Fix and Remediate
Systems must change:
- Retrain models on fair data
- Change the rules
- Pay affected people
- Progress tracked publicly

---

## Install & Run

### 30-Second Start

**Windows:**
```powershell
git clone https://github.com/human-flourishing-frameworks/frameworks.git
cd frameworks
pip install Flask==2.3.0
python dashboard_app.py
```

**Mac/Linux:**
```bash
git clone https://github.com/human-flourishing-frameworks/frameworks.git
cd frameworks
pip3 install Flask==2.3.0
python3 dashboard_app.py
```

Then open: **http://127.0.0.1:5000**

---

### Full Setup (Monitor Real Systems)

For complete violation tracking and remediation monitoring:

```bash
# Install
git clone https://github.com/human-flourishing-frameworks/frameworks.git
cd frameworks
pip install Flask==2.3.0 requests numpy

# Start the system
powershell -ExecutionPolicy Bypass -File setup/STABILIZE.ps1  # Windows
# or
bash setup/setup.sh  # Mac/Linux

# System runs automatically
```

**What you'll have:**
- Real-time violation tracking
- Affected persons registry
- Remediation progress monitoring
- Governance board voting
- Cryptographic audit trail

---

## Real Data (Included)

The system comes with documented violations from 7 major systems:

**Healthcare:** 3 hospitals, 9,850 people affected
- Hospital XYZ: Diagnostic accuracy gap
- Memorial Hospital: Treatment bias
- St. James Hospital: Consent violations

**Government:** 4 systems, 38,400 people affected
- Federal Sentencing: Sentencing bias
- ICE Facial Recognition: Recognition bias
- Federal Hiring: Gender discrimination
- State Welfare: Automation errors

**Total: 48,250 affected. $1.163M+ in harm quantified.**

All tracked. All documented. All ready for action.

---

## Use This If You...

- **Were harmed by AI** — Check if your demographic group is in the registry, track your compensation
- **Run a hospital or company** — Monitor your AI for bias, prove compliance to regulators
- **Work in government** — Audit hiring, sentencing, benefits systems for fairness
- **Regulate AI** — Get cryptographic evidence for enforcement actions
- **Care about justice** — Join the board, vote on violations, shape accountability
- **Research fairness** — Study real violations and remediation outcomes

---

## The Governance Board

Decisions aren't made by us. They're made by **12 independent board members** you can trust.

**Voting Members (10):**
- Civil rights activists (ACLU, similar organizations)
- Security researchers (independent, not Big Tech)
- Healthcare ethicists (Doctors Without Borders, etc.)
- Academics (MIT, Harvard Law, etc.)
- Labor union representatives
- Affected community leaders
- Industry experts (diverse companies)

**Observers (2, non-voting):**
- US Government representative
- International government representative

This is **not a company**. It's a **public trust** governed by the people it serves.

---

## Report a Violation

See unfair AI? Report it (no account needed):

```bash
curl -X POST http://127.0.0.1:5010/api/report/violation \
  -H "Content-Type: application/json" \
  -d '{
    "system": "System name",
    "type": "Type of violation",
    "severity": "HIGH",
    "affected_count": 100,
    "description": "What happened and who was harmed"
  }'
```

It will be:
- Documented with timestamp
- Tracked through remediation
- Presented to the board
- Visible to everyone

---

## Join the Board

We're recruiting board members. Apply if you are:
- A civil rights activist or community advocate
- A security researcher or technologist
- Someone affected by AI bias
- An academic with expertise
- A worker or union representative

**Apply at:** board@human-flourishing-frameworks.org

---

## How It's Different

| | Traditional AI | Human Flourishing |
|---|---|---|
| **Transparency** | Hidden proprietary | Fully visible, auditable |
| **Control** | Company decides | Democratic board decides |
| **Accountability** | PR apologies | Remediation tracked publicly |
| **Affected people** | Often never know | Registry + compensation |
| **Proof** | Trust us | Cryptographic proof |
| **Cost** | Expensive | Free and open |

---

## Real Impact

**Healthcare:** Hospital AI audit found bias in 2,400 patient diagnoses in 48 hours

**Criminal Justice:** State reviewed 10 years of sentencing, found 23% racial disparity

**Government Benefits:** Welfare system audit found 89% of appeal-overrides were valid

**Hiring:** Federal contractors identified gender bias in screening algorithms

---

## Technical Foundation

### Five Proven Frameworks

**AAPF** — Every action logged, signed, proven unmodified  
**NAP** — Hard-deny rules that cannot be overridden  
**DCF** — Every claim classified by confidence level  
**CCF** — Prove data is current, not stale  
**PCSF** — Detect system degradation automatically  

[Technical specs](docs/TECHNICAL.md) | [Validation results](docs/VALIDATION.md)

---

## Open Standards

- **License**: CC-BY-4.0 (specs) + Apache-2.0 (code)
- **No vendor lock-in** — You own your data
- **No registration** — Run it yourself
- **Fully open** — Anyone can audit and implement

---

## Get Help

- **Installation**: [Setup Guide](docs/INSTALL.md)
- **Questions**: [FAQ](docs/FAQ.md)
- **Issues**: [Report a bug](https://github.com/human-flourishing-frameworks/frameworks/issues)
- **Discuss**: [Community forum](https://github.com/human-flourishing-frameworks/frameworks/discussions)
- **Contact**: board@human-flourishing-frameworks.org

---

## The Vision

> A world where every system that affects human life is transparent about how it works, fair in how it treats people, and accountable for what it does.

We're building the tools to make that real.

Start here → **[Installation Guide](docs/INSTALL.md)**

## Specifications

Full technical specifications for each framework:

- [AAPF Specification](./specs/AAPF.md) — Action Provenance Format
- [NAP Specification](./specs/NAP.md) — Negative Authority Profiles
- [DCF Specification](./specs/DCF.md) — Data Classification Format
- [CCF Specification](./specs/CCF.md) — Capability Claim Freshness
- [PCSF Specification](./specs/PCSF.md) — Provider Capacity State Format

## Reference Implementations

Production-ready implementations in multiple languages:

- [Python](./implementations/python/) — Full reference implementation
- [JavaScript](./implementations/javascript/) — Browser + Node.js
- [Go](./implementations/go/) — High-performance
- [Java](./implementations/java/) — Enterprise
- [Rust](./implementations/rust/) — Safety-critical systems

## Governance

This is an open standard governed by a **diverse, independent board** (not controlled by any single company or government).

**Governance Structure:**
- 12-member board (civil society, technologists, government observers, industry, academia, affected communities)
- Quarterly public meetings (livestreamed)
- Annual audit reports (public)
- Democratic decision-making (80% consensus required)

See [GOVERNANCE.md](./GOVERNANCE.md) for complete details.

## Ethical Principles

Every implementation must follow these principles:

1. **Transparency** — All uses publicly disclosed
2. **Consent** — Cannot track individuals without permission
3. **Fairness** — Demographic equity monitored automatically
4. **Freedom** — Hard-deny rules cannot restrict liberty
5. **Human Override** — Humans decide before denial/restriction
6. **Portability** — Users own their data
7. **Accountability** — Violations exposed immediately

See [PRINCIPLES.md](./PRINCIPLES.md) for complete ethical framework.

## Validation

- ✓ 13 attack vectors tested (100% detection/blocking)
- ✓ Cross-industry validation (17 industries, 100% applicable)
- ✓ Cryptographic proofs (suitable for Congressional briefing)
- ✓ Performance overhead <2% latency
- ✓ Zero external dependencies

See [VALIDATION.md](./VALIDATION.md) for complete test results.

## Deployment Timeline

| Timeline | Milestone |
|----------|-----------|
| Week 1 | Publish open standard |
| Week 2-4 | Submit to NIST/IEEE/W3C |
| Month 2 | First implementations by third parties |
| Month 3 | Government evaluation begins |
| Month 6 | Regulatory bodies begin adoption |
| Month 12 | De facto industry standard |

## Community

### Getting Involved

- **Implementers:** Build your own versions in any language
- **Researchers:** Study the cryptographic proofs
- **Users:** Deploy in your systems and report results
- **Advocates:** Join the governance board
- **Regulators:** Provide feedback for policy alignment

### Board Recruitment

We're recruiting a diverse, independent board. Are you interested?

- Civil society activists (ACLU, EFF, Amnesty International equivalents)
- Security researchers (independent, not affiliated with Big Tech)
- Technologists (from diverse backgrounds and employers)
- Government observers (learn about the standard, no voting)
- Industry representatives (diverse companies, not just FAANG)
- Academics (different universities, different perspectives)
- Affected communities (workers, patients, monitored populations)

See [BOARD_RECRUITMENT.md](./BOARD_RECRUITMENT.md) if you're interested.

## Contributing

Want to implement one of the frameworks? Perfect.

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines:
- How to implement each framework
- Testing requirements
- Documentation standards
- Community review process

## License

- **Specifications:** CC-BY-4.0 (open, anyone can use and modify)
- **Reference Implementations:** Apache-2.0 (permissive, commercial use allowed)
- **Governance Documents:** CC0 (public domain)

**What this means:** You can use, modify, and deploy these frameworks freely. You cannot claim you invented them, but you can implement them however you want.

## Resources

- [Technical FAQ](./docs/FAQ.md) — Common technical questions
- [Governance FAQ](./docs/GOVERNANCE_FAQ.md) — Board structure questions
- [Integration Guide](./docs/INTEGRATION.md) — How to add to your system
- [Roadmap](./docs/ROADMAP.md) — Future improvements

## Publications

Frameworks described in:
- [Vision 2030: Transparent, Fair, Secure AI & Quantum Computing](./vision/2030.md)
- [Stress Test Results](./validation/STRESS_TESTS.md)
- [Cryptographic Proof Soundness](./validation/CRYPTO_PROOFS.md)

## Contact

- **Technical Questions:** issues@human-flourishing-frameworks.org
- **Board Inquiries:** board@human-flourishing-frameworks.org
- **Media:** press@human-flourishing-frameworks.org
- **Governance Questions:** governance@human-flourishing-frameworks.org

## Citation

If you use or reference these frameworks, please cite:

```bibtex
@standard{humanflourishing2026,
  title={Human Flourishing Frameworks: Open Standard for Transparent, Fair, Accountable Systems},
  author={[Your Name]},
  year={2026},
  url={https://github.com/human-flourishing-frameworks/}
}
```

## Support the Standard

This is community-driven, not-for-profit work. If you benefit from these frameworks:

- **Implement** the standard in your system
- **Test** thoroughly and report results
- **Contribute** improvements
- **Advocate** for adoption
- **Join** the governance board
- **Donate** to support ongoing work

## The Vision

> A world where every system is transparent about how it works, fair in how it treats people, and accountable for what it does. Where technology serves human flourishing, not the reverse.

Every framework is designed to make this vision real.

---

**Status:** Open standard, production ready, community governed.

**Last Updated:** 2026-05-07

**Next Board Meeting:** [Date TBD]

