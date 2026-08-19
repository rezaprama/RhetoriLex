# RhetoriLex

**Gerakan retoris dan pola tulisan akademik offline yang dikalibrasi terhadap bukti, untuk peneliti, editor, dan agen AI.**

[![CI](https://github.com/rezaprama/RhetoriLex/actions/workflows/ci.yml/badge.svg)](https://github.com/rezaprama/RhetoriLex/actions/workflows/ci.yml)
[![Pages](https://github.com/rezaprama/RhetoriLex/actions/workflows/pages.yml/badge.svg)](https://github.com/rezaprama/RhetoriLex/actions/workflows/pages.yml)
[![Lisensi kode: Apache-2.0](https://img.shields.io/badge/kode-Apache--2.0-0f766e.svg)](LICENSE)
[![Lisensi data: CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-0f766e.svg)](LICENSES/CC-BY-4.0.txt)

[Buka katalog](https://rezaprama.github.io/RhetoriLex/) · [English](README.md) · [Agent Skill](skills/rhetorilex/SKILL.md) · [Riset](docs/discovery-research.md) · [Provenance](PROVENANCE.md)

RhetoriLex membantu penulis memilih bahasa berdasarkan tujuan komunikasi dan bukti,
bukan sekadar kesan akademik. Versi 0.2.0 berisi 96 pola yang ditulis mandiri untuk 24
fungsi retoris, dengan tingkat klaim, kebutuhan bukti, guard desain kausal, risiko, slot
bernama, dan provenance yang eksplisit.

RhetoriLex tidak membuat bukti atau sitasi. RhetoriLex juga tidak mengubah asosiasi
menjadi sebab-akibat.

## Mengapa berbeda

- **Bukti lebih dulu.** Setiap pola menyatakan bukti minimum dan klaim terkuat yang
  kompatibel.
- **Makna terlindungi.** Agent Skill menjaga sitasi, angka, unit, populasi, negasi,
  ketidakpastian, dan status kausal saat menulis ulang.
- **Katalog clean-room.** Semua pola rilis merupakan karya editorial original dengan
  `source_reuse: false`; inventaris sumber terbatas dikecualikan.
- **Core offline.** Pencarian, filter, validasi, build, dan helper Skill hanya memakai
  pustaka standar Python.
- **Satu sumber data.** JSONL kanonis membangun JSON, CSV, SQLite, Markdown, resource
  paket, aset Skill, dan checksum secara deterministik.
- **Empat cara pakai.** Gunakan API/CLI Python, Agent Skill/plugin portabel, explorer web
  statis, atau artefak data hasil build.

## Coba cepat

```bash
git clone https://github.com/rezaprama/RhetoriLex.git
cd RhetoriLex
python -m pip install -e .
rhetorilex search "cautious interpretation" --stage discussion --limit 3
```

Output machine-readable dan filter bukti ketat:

```bash
rhetorilex --json search "observational result" \
  --evidence observational \
  --max-claim-strength bounded \
  --risk low
```

Periksa satu pola atau kesehatan kontrak lengkap:

```bash
rhetorilex explain RLX-QUA-001
rhetorilex inspect --validate
rhetorilex taxonomy
```

API Python:

```python
from rhetorilex import Catalog

catalog = Catalog.load()
results = catalog.search(
    "state a limitation",
    stage="discussion",
    max_claim_strength="bounded",
    limit=3,
)

for result in results:
    print(result.entry.template, result.entry.evidence_requirement)
```

## Pasang sebagai Agent Skill

Untuk satu repo, salin `skills/rhetorilex` ke `.agents/skills/rhetorilex`. Untuk pemakaian
pribadi lintas proyek, salin ke `~/.codex/skills/rhetorilex`.

Contoh permintaan:

- “Berikan tiga cara hati-hati untuk menafsirkan hasil observasional ini.”
- “Tulis ulang paragraf ini tanpa mengubah sitasi, angka, atau kekuatan klaim.”
- “Bandingkan pilihan untuk menyatakan research gap yang terbatas.”
- “Audit kalimat ini untuk causal overclaim.”

Skill sengaja menolak fabrikasi sitasi, penyamaran plagiarisme, synonym spinning,
pengelakan detektor, dan peningkatan klaim tanpa dukungan. Arsip plugin siap rilis dapat
dibangun dari [.codex-plugin/plugin.json](.codex-plugin/plugin.json).

## Model katalog

Setiap entri kanonis memuat:

| Field | Fungsi |
| --- | --- |
| `function` | Tujuan komunikasi stabil seperti `identify_gap` atau `state_limitation` |
| `template` | Kalimat original dengan slot bernama yang eksplisit |
| `stage` | Tahap manuskrip yang kompatibel |
| `claim_strength` | `tentative`, `bounded`, `assertive`, atau `causal` |
| `evidence_requirement` | `none`, `contextual`, `observational`, `direct`, atau `convergent` |
| `causal_design_required` | Mencegah pola kausal dipakai sebagai prosa umum |
| `risk` | Tingkat review editorial: `low`, `medium`, atau `high` |
| `provenance` | Catatan wajib `original_editorial` dan `source_reuse: false` |

Lihat [data/taxonomy/taxonomy.v1.json](data/taxonomy/taxonomy.v1.json),
[data/contracts/evidence-claim.v1.json](data/contracts/evidence-claim.v1.json), dan
[docs/data-model.md](docs/data-model.md).

## Riset dan discovery

Model ini berorientasi pada riset tentang genre dan gerakan retoris
([10.1017/CBO9781139524827](https://doi.org/10.1017/CBO9781139524827)), stance dan
interaksi pembaca ([10.1177/1461445605050365](https://doi.org/10.1177/1461445605050365)),
serta fraseologi korpus dan variasi disiplin
([10.1016/j.jeap.2019.01.003](https://doi.org/10.1016/j.jeap.2019.01.003)). Sumber ini
mengarahkan desain original; prosa, contoh, dan inventarisnya tidak diambil. Provenance
riset lengkap tersedia di [PROVENANCE.md](PROVENANCE.md).

Positioning publik juga diukur, bukan ditebak. [Studi discovery](docs/discovery-research.md)
dan [landscape GitHub](docs/github-landscape.md) merekam query, metrik, timestamp, batas
interpretasi, dan bukti terstruktur dalam [data/discovery](data/discovery/). Jumlah repo
GitHub adalah sinyal suplai/indeks—bukan volume pencarian web, permintaan pengguna,
adopsi, atau kualitas. Pengukuran langsung Google Trends tidak tersedia, sehingga
nilainya dicatat sebagai `null`; tidak ada volume proxy yang dikarang.

## Build dan verifikasi

```bash
python scripts/validate_data.py
python scripts/build_data.py
python -m unittest discover -s tests -v
python scripts/package_plugin.py --output dist/rhetorilex-plugin.zip
```

Test suite memeriksa schema, provenance, kesamaan slot, kebutuhan bukti, guard kausal,
build deterministik, perilaku retrieval, routing benchmark beku, perilaku CLI, dan
keamanan kontrak. Continuous integration mengulang build dan membandingkan checksum.

## Arsitektur

```text
data/canonical/catalog.v1.jsonl
          |
          +--> data/dist/*                    artefak data portabel
          +--> src/rhetorilex/resources/*     paket Python
          +--> skills/rhetorilex/assets/*     Agent Skill offline
          +--> docs/data/phrases.json          artefak Pages hasil assembly

taxonomy + JSON Schema + kontrak bukti
          |
          +--> validator --> tests --> gate rilis deterministik
```

Explorer browser berupa HTML, CSS, dan JavaScript statis. Tidak ada akun, backend,
dependensi CDN, atau telemetry.

## Batas sumber dan hak penggunaan

Workbook privat yang diberikan untuk proyek ini memiliki ketentuan penggunaan akademik
dan larangan distribusi. File hanya diaudit lokal untuk struktur agregat non-ekspresif
dan sinyal kualitas. File diabaikan Git; isi sel dan labelnya tidak masuk repo; semua
kandidat migrasi tetap unresolved; dan **nol item turunan sumber dipromosikan**.

Manchester Academic Phrasebank hanya menjadi konteks konseptual dan sitasi; inventaris
frasanya tidak diimpor atau ditulis ulang. BAWE dikecualikan. Elsevier OA CC-BY Corpus
v3 hanya terdaftar sebagai kemungkinan sumber validasi agregat di masa depan dan belum
diingest. Baca [PROVENANCE.md](PROVENANCE.md),
[source registry](data/sources/source-registry.yaml), dan
[laporan audit](reports/xlsx-audit.md).

## Kontribusi

Kontribusi diterima jika kalimat ditulis mandiri dan aman terhadap bukti. Mulai dari
[CONTRIBUTING.md](CONTRIBUTING.md). Pola baru membutuhkan provenance, slot bernama,
kompatibilitas taxonomy, metadata bukti, review orisinalitas, dan tes. Jangan unggah
workbook terbatas, inventaris sumber, manuskrip, atau kutipan korpus ke issue atau pull
request.

Masalah keamanan, draft rahasia, provenance, dan hak penggunaan dilaporkan lewat proses
privat di [SECURITY.md](SECURITY.md). Keputusan proyek dicatat di
[GOVERNANCE.md](GOVERNANCE.md) dan [IMPLEMENTATION_LOG.md](IMPLEMENTATION_LOG.md).

## Proyek dan pembuat

RhetoriLex dibuat dan dikelola oleh
[Reza Prama Arviandi](https://rezaprama.com). Riwayat rilis tersedia di
[CHANGELOG.md](CHANGELOG.md); rencana publik tersedia di [ROADMAP.md](ROADMAP.md).

## Lisensi dan sitasi

Kode, konfigurasi, tes, dan Agent Skill memakai Apache-2.0. Data original, laporan,
benchmark, aset, dan dokumentasi memakai CC BY 4.0. Pemetaan path machine-readable
tersedia di [REUSE.toml](REUSE.toml); status pihak ketiga tersedia di
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Metadata sitasi versi 0.2.0 tersedia di [CITATION.cff](CITATION.cff). Dokumen lisensi
menyatakan kebijakan proyek, bukan nasihat hukum.