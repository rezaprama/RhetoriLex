# RhetoriLex

**Gerakan retoris untuk tulisan akademik yang dikalibrasi terhadap bukti. Offline, transparan, dan dibangun secara clean-room.**

[![CI](https://github.com/rezaprama/RhetoriLex/actions/workflows/ci.yml/badge.svg)](https://github.com/rezaprama/RhetoriLex/actions/workflows/ci.yml)
[![Pages](https://github.com/rezaprama/RhetoriLex/actions/workflows/pages.yml/badge.svg)](https://github.com/rezaprama/RhetoriLex/actions/workflows/pages.yml)
[![Lisensi kode: Apache-2.0](https://img.shields.io/badge/kode-Apache--2.0-0f766e.svg)](LICENSE)
[![Lisensi data: CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-0f766e.svg)](LICENSES/CC-BY-4.0.txt)

[Buka katalog](https://rezaprama.github.io/RhetoriLex/) · [English](README.md) · [Agent Skill](skills/rhetorilex/SKILL.md) · [Provenance](PROVENANCE.md)

RhetoriLex membantu penulis memilih bahasa berdasarkan tujuan komunikasi dan kekuatan bukti, bukan sekadar kesan “akademik”. Rilis awal berisi 48 pola original untuk 12 fungsi retoris. Setiap pola mencatat tingkat klaim, kebutuhan bukti, syarat desain kausal, risiko, slot, dan provenance.

RhetoriLex tidak membuat bukti atau sitasi. RhetoriLex juga tidak mengubah asosiasi menjadi sebab-akibat.

## Nilai utama

- **Bukti lebih dulu.** Pola menyatakan bukti minimum dan klaim terkuat yang kompatibel.
- **Makna terlindungi.** Skill menjaga sitasi, angka, unit, populasi, negasi, ketidakpastian, dan status kausal saat menulis ulang.
- **Katalog clean-room.** Semua pola rilis ditulis mandiri dengan `source_reuse: false`.
- **Core offline.** Pencarian, filter, validasi, build, dan helper Skill hanya memakai pustaka standar Python.
- **Satu sumber data.** JSONL kanonis membangun JSON, CSV, SQLite, Markdown, resource Python, asset Skill, dan checksum secara deterministik.
- **Tiga cara pakai.** CLI/API Python, Agent Skill/plugin, atau explorer web statis.

## Coba cepat

```bash
git clone https://github.com/rezaprama/RhetoriLex.git
cd RhetoriLex
python -m pip install -e .
rhetorilex search "cautious interpretation" --stage discussion --limit 3
```

Pencarian terstruktur dengan batas kekuatan klaim:

```bash
rhetorilex --json search "observational result" \
  --evidence observational \
  --max-claim-strength bounded \
  --risk low
```

Validasi katalog:

```bash
rhetorilex inspect --validate
python scripts/validate_data.py
python scripts/build_data.py
python -m unittest discover -s tests -v
```

## Pasang sebagai Agent Skill

Untuk satu repo, salin `skills/rhetorilex` ke `.agents/skills/rhetorilex`. Untuk penggunaan pribadi lintas proyek, salin ke `~/.codex/skills/rhetorilex`.

Contoh permintaan:

- “Berikan tiga cara hati-hati untuk menafsirkan hasil observasional ini.”
- “Tulis ulang paragraf ini tanpa mengubah sitasi, angka, atau kekuatan klaim.”
- “Bandingkan pilihan untuk menyatakan research gap yang terbatas.”
- “Audit kalimat ini untuk causal overclaim.”

Skill menolak fabrikasi sitasi, penyamaran plagiarisme, synonym spinning, pengelakan detektor, dan peningkatan klaim tanpa dukungan.

## Batas workbook dan hak penggunaan

Workbook privat yang diberikan untuk proyek ini memiliki ketentuan penggunaan akademik dan larangan distribusi. File hanya diaudit lokal untuk statistik struktur non-ekspresif. File diabaikan Git; isi sel, label, dan formatnya tidak masuk repo; semua kandidat migrasi tetap unresolved; dan **nol item turunan dipromosikan**.

Manchester Academic Phrasebank hanya menjadi konteks konseptual dan sitasi; inventaris frasanya tidak diimpor atau ditulis ulang. BAWE dikecualikan. Elsevier OA CC-BY Corpus v3 hanya terdaftar sebagai kemungkinan sumber validasi agregat di masa depan dan belum diingest. Baca [PROVENANCE.md](PROVENANCE.md), [source registry](data/sources/source-registry.yaml), dan [laporan audit](reports/xlsx-audit.md).

## Kontribusi dan lisensi

Pola baru harus original, evidence-safe, memiliki slot bernama, metadata bukti, provenance, review orisinalitas, dan tes. Panduan lengkap: [CONTRIBUTING.md](CONTRIBUTING.md). Jangan unggah workbook terbatas, inventaris sumber, manuskrip, atau kutipan corpus ke issue/PR.

Kode, konfigurasi, tes, dan Agent Skill memakai Apache-2.0. Data original, laporan, benchmark, aset, dan dokumentasi memakai CC BY 4.0. Pemetaan path tersedia di [REUSE.toml](REUSE.toml). Metadata sitasi tersedia di [CITATION.cff](CITATION.cff).
