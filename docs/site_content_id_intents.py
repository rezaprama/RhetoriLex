"""Halaman tujuan khusus Bahasa Indonesia untuk pencarian dan Skill Agen."""

PAGES_ID = {
    "research_gap": {
        "kind": "article",
        "title": "Cara Menulis Kesenjangan Riset Tanpa Overclaim | RhetoriLex",
        "description": "Tentukan kesenjangan riset yang spesifik dari bukti yang ditinjau tanpa mengklaim bahwa penelitian terdahulu tidak ada.",
        "h1": "Tulis kesenjangan riset yang didukung literatur",
        "lede": "Kesenjangan yang dapat dipertahankan menamai persoalan terbuka, cakupan, dan bukti yang menetapkannya.",
        "body": """
<section>
  <h2>Apa yang dimaksud kesenjangan riset</h2>
  <p>Kesenjangan riset bukan pernyataan dramatis bahwa suatu topik belum pernah diteliti. Kesenjangan adalah uraian terbatasi mengenai hal yang belum ditetapkan oleh bukti yang tersedia. Fokusnya dapat berupa populasi, konteks, mekanisme, ukuran, metode, waktu, ketidakkonsistenan, atau perbandingan yang belum dijawab. Kesenjangan perlu mengarah langsung pada pertanyaan yang dapat ditangani studi.</p>
  <p>Bangun klaim dari <a href="{{link:literature_review}}">tinjauan pustaka</a>. Catat cakupan pencarian, bedakan bukti yang hilang dari bukti yang bercampur, dan sitasi studi yang menentukan batas.</p>
</section>
<section>
  <h2>Pola untuk kesenjangan yang spesifik</h2>
  <p class="phrase-template">Although [established finding] has been documented in [studied context], evidence regarding [specific unresolved issue] remains limited in [target context].</p>
  <p class="phrase-template">Studies differ in their estimates of [relation], leaving the role of [specific source of uncertainty] unresolved.</p>
  <p>Pola pertama sesuai untuk kekurangan cakupan. Pola kedua sesuai untuk temuan yang tidak konsisten. Ganti setiap placeholder dengan fakta dari tinjauan.</p>
</section>
<section>
  <h2>Hubungkan kesenjangan dengan studi</h2>
  <p>Jelaskan mengapa persoalan penting dan bagaimana tujuan riset menanggapinya. Namai keputusan ilmiah, teoretis, metodologis, klinis, atau kebijakan yang dipengaruhi ketidakpastian. Lalu nyatakan tujuan yang dapat dijawab oleh desain, sampel, dan pengukuran.</p>
  <p>Cari pola lain di <a href="{{link:phrase_explorer}}?q=kesenjangan%20riset">Penjelajah Frasa</a> dan periksa kebutuhan buktinya.</p>
</section>
<aside class="article-note"><h2>Peringatan</h2><p>Sitasi yang tidak ditemukan bukan bukti bahwa studi tidak ada. Hindari first, never, dan no research kecuali tinjauan komprehensif mendukungnya.</p></aside>
""",
    },
    "literature_review": {
        "kind": "article",
        "title": "Cara Menulis Tinjauan Pustaka yang Menyintesis | RhetoriLex",
        "description": "Tulis tinjauan pustaka yang mengatur, membandingkan, dan mengevaluasi bukti, bukan mendaftar studi satu per satu.",
        "h1": "Tinjauan pustaka perlu menyintesis, bukan menginventarisasi",
        "lede": "Atur sumber di sekitar pertanyaan dan tampilkan dasar perbandingan kepada pembaca.",
        "body": """
<section>
  <h2>Tentukan kerangka analitik tinjauan</h2>
  <p>Tinjauan pustaka menjelaskan keadaan pengetahuan yang relevan dengan keputusan riset. Pilih kerangka sebelum menulis: teori yang bersaing, kelompok metode, populasi, konteks, outcome, waktu, atau pola kesepakatan dan pertentangan. Kerangka harus membantu pembaca memahami alasan studi dapat atau tidak dapat dibandingkan.</p>
  <p>Buat tabel bukti berisi desain, sampel, ukuran, estimasi, keterbatasan, dan relevansi. Langkah ini mencegah sintesis yang rapi mencampur hasil dari pertanyaan berbeda.</p>
</section>
<section>
  <h2>Tulis relasi antar-studi</h2>
  <p class="phrase-template">Across [group of studies], estimates consistently indicate [shared pattern], although [design or population difference] limits direct comparison.</p>
  <p class="phrase-template">Whereas [study group A] reports [finding], studies using [method B] find [contrasting finding], suggesting that [bounded source of variation] warrants examination.</p>
  <p>Studi yang disitasi harus mendukung relasi dalam across, consistently, whereas, atau contrasting. Gunakan <a href="{{link:hedging}}">hedging akademik</a> untuk bukti yang bercampur atau tidak langsung.</p>
</section>
<section>
  <h2>Bergerak dari sintesis ke masalah riset</h2>
  <p>Akhiri unit tematik dengan hal yang telah ditetapkan dan yang masih tidak pasti. Kesenjangan harus mengikuti bukti yang ditinjau. Hubungkan keterbatasan dengan tujuan studi hanya bila desain dapat menanganinya.</p>
  <p>Temukan pola sintesis di <a href="{{link:phrase_explorer}}?q=sintesis%20literatur">Penjelajah Frasa</a>. Pertahankan setiap sitasi pada proposisi yang didukungnya.</p>
</section>
<aside class="article-note"><h2>Peringatan</h2><p>Jangan memberikan label kesepakatan, kontradiksi, mutu, atau konsensus tanpa kriteria. Daftar abstrak serupa tidak membuktikan bukti konvergen.</p></aside>
""",
    },
    "thesis": {
        "kind": "article",
        "title": "Penulisan Tesis: Argumen, Bab, dan Kontribusi | RhetoriLex",
        "description": "Rencanakan dan revisi tesis sebagai satu argumen berbasis bukti dari pendahuluan hingga diskusi.",
        "h1": "Tulis tesis sebagai satu argumen yang dapat ditelusuri",
        "lede": "Setiap bab memajukan masalah riset yang sama sambil memenuhi fungsi retorisnya sendiri.",
        "body": """
<section>
  <h2>Bangun tulang punggung tesis</h2>
  <p>Tulis empat pernyataan lugas sebelum memoles bab: masalah, pertanyaan riset, desain untuk menjawabnya, dan kontribusi yang terbatasi. Keempatnya membentuk tulang punggung tesis. Setiap bab perlu menetapkan premis, mencatat respons, melaporkan bukti, atau menafsirkan apa yang didukung bukti.</p>
  <p>Petakan hubungan antar-bab. <a href="{{link:research_gap}}">Kesenjangan riset</a> harus mengarah pada tujuan. Metode mengoperasionalkan tujuan. Hasil menjawab analisis. Diskusi tidak boleh memperkenalkan pertanyaan yang lebih kuat atau populasi yang lebih luas.</p>
</section>
<section>
  <h2>Gunakan penunjuk fungsi bab</h2>
  <p class="phrase-template">This chapter establishes [specific premise] by examining [evidence or analysis], providing the basis for [next chapter function].</p>
  <p class="phrase-template">Taken together, Chapters [X-Y] support [bounded contribution] within [population, setting, or methodological scope].</p>
  <p>Penunjuk perlu menampilkan relasi logis, bukan sekadar menjelaskan mekanik dokumen. Nyatakan pertanyaan atau klaim secara langsung.</p>
</section>
<section>
  <h2>Revisi lintas batas bab</h2>
  <p>Bandingkan istilah, variabel, label populasi, dan kekuatan klaim dalam abstrak, pendahuluan, hasil, diskusi, serta simpulan. Telusuri simpulan ke hasil dan metode. Telusuri pertanyaan menuju jawaban atau pernyataan bahwa pertanyaan tetap terbuka.</p>
  <p>Gunakan <a href="{{link:preserve_claim_strength}}">Pertahankan Kekuatan Klaim</a> saat memadatkan abstrak dan simpulan.</p>
</section>
<aside class="article-note"><h2>Peringatan</h2><p>Kontribusi tesis tidak harus mengklaim kebaruan untuk seluruh bidang. Nyatakan tambahan yang tepat, penerima manfaat, desain, dan ketidakpastian tersisa.</p></aside>
""",
    },
    "methods": {
        "kind": "article",
        "title": "Cara Menulis Bagian Metode yang Reproduktif | RhetoriLex",
        "description": "Tulis metode yang membuat desain, sampel, ukuran, prosedur, eksklusi, dan pilihan analisis dapat ditelusuri.",
        "h1": "Penulisan metode menampilkan keputusan analitik",
        "lede": "Metode yang jelas menunjukkan apa yang dilakukan, alasannya, dan dampak pilihan terhadap interpretasi.",
        "body": """
<section>
  <h2>Laporkan desain sebelum detail prosedur</h2>
  <p>Namai desain studi, konteks, tanggal, populasi, proses sampling, kriteria inklusi, dan unit analisis. Lalu jelaskan pengukuran, intervensi atau paparan, outcome, prosedur, eksklusi, serta pilihan analisis. Urutan mengikuti logika untuk menafsirkan estimasi, bukan hanya kronologi administrasi.</p>
  <p>Jelaskan siapa yang membuat penilaian subjektif, apakah penilai dibutakan, dan cara menyelesaikan perbedaan. Bentuk pasif dapat dipakai untuk prosedur rutin, tetapi tidak untuk menyembunyikan tanggung jawab.</p>
</section>
<section>
  <h2>Hubungkan pilihan dengan tujuannya</h2>
  <p class="phrase-template">We used [method] to estimate [target quantity] because [design-relevant reason], with [assumption or limitation] considered in interpretation.</p>
  <p class="phrase-template">Observations were excluded according to the prespecified criterion [criterion]; [number or proportion] were removed before [analysis stage].</p>
  <p>Nyatakan apakah keputusan ditentukan sebelumnya atau dipengaruhi data. Laporkan perangkat lunak dan versi ketika relevan dengan reproduksibilitas.</p>
</section>
<section>
  <h2>Audit metode terhadap hasil</h2>
  <p>Setiap jumlah populasi, model, subkelompok, analisis sensitivitas, dan outcome yang dilaporkan harus memiliki dasar metode. Setiap metode yang dijelaskan harus menghasilkan hasil atau memiliki peran jelas. Gunakan <a href="{{link:results}}">panduan hasil</a> untuk memeriksa kesesuaian.</p>
</section>
<aside class="article-note"><h2>Peringatan</h2><p>Jangan gunakan reproducible sebagai klaim hiasan. Sediakan data, kode, protokol, bahan, atau detail yang diperlukan, dengan tetap mematuhi batas etika dan hukum.</p></aside>
""",
    },
    "results": {
        "kind": "article",
        "title": "Cara Menulis Hasil dengan Estimasi dan Ketidakpastian | RhetoriLex",
        "description": "Tulis hasil yang melaporkan perbandingan, magnitudo, arah, ketidakpastian, dan data hilang tanpa overclaim kausal.",
        "h1": "Penulisan hasil melaporkan apa yang diestimasi analisis",
        "lede": "Mulai dari perbandingan dan estimasi, pertahankan ketidakpastian, dan sesuaikan interpretasi dengan desain.",
        "body": """
<section>
  <h2>Berikan kerangka referensi yang lengkap</h2>
  <p>Hasil memerlukan outcome, kelompok atau kondisi pembanding, arah, magnitudo, satuan, dan ketidakpastian. Nyatakan populasi analisis serta waktu bila belum jelas. Gunakan tabel untuk estimasi padat, tetapi teks perlu mengidentifikasi temuan yang menjawab pertanyaan riset.</p>
  <p>Jangan mengganti estimasi dengan label signifikansi. Nilai p kecil tidak menunjukkan kepentingan praktis, sedangkan nilai p besar tidak membuktikan ketiadaan efek. Laporkan interval dan nilai yang masih sesuai dengan data.</p>
</section>
<section>
  <h2>Pola untuk pelaporan tepat</h2>
  <p class="phrase-template">Outcome Y was [estimate and unit] higher in [group A] than in [group B] ([interval]), with [relevant adjustment or analysis population].</p>
  <p class="phrase-template">The estimate was imprecise ([interval]), leaving both [scientifically relevant possibility A] and [possibility B] compatible with the data.</p>
  <p>Pola pertama membutuhkan perbandingan dan arah yang benar. Pola kedua menjelaskan ketidakpastian tanpa mengubah hasil yang tidak meyakinkan menjadi bukti ketiadaan.</p>
</section>
<section>
  <h2>Jaga batas desain</h2>
  <p>Hasil observasional umumnya menggunakan associated with, differed, atau was related to, bukan caused, improved, atau prevented. Baca <a href="{{link:association_vs_causation}}">Asosiasi vs Kausalitas</a>. Verifikasi angka, satuan, rujukan tabel, label subkelompok, dan tanda terhadap keluaran final.</p>
</section>
<aside class="article-note"><h2>Peringatan</h2><p>Jangan menyimpulkan perubahan dalam kelompok dari uji signifikansi terpisah, atau perbedaan kelompok dari satu hasil signifikan dan satu tidak signifikan. Laporkan perbandingan langsung.</p></aside>
""",
    },
    "discussion": {
        "kind": "article",
        "title": "Cara Menulis Diskusi Tanpa Overclaim | RhetoriLex",
        "description": "Tulis diskusi yang menjawab pertanyaan, menghubungkan bukti terdahulu, mempertimbangkan penjelasan, dan menyatakan batas.",
        "h1": "Diskusi menafsirkan temuan dalam batasnya",
        "lede": "Jawab pertanyaan riset, lalu jelaskan relasi, ketidakpastian, alternatif, implikasi, dan cakupan.",
        "body": """
<section>
  <h2>Mulai dengan jawaban yang terbatasi</h2>
  <p>Awali dengan temuan yang paling langsung menjawab pertanyaan riset. Nyatakan pada kekuatan yang didukung desain dan analisis. Jangan mengulang semua hasil atau memulai dengan klaim kebaruan. Jelaskan cara temuan mengubah, memperinci, atau tidak mengubah pemahaman terkait.</p>
  <p class="phrase-template">In [population and setting], the findings support [bounded interpretation], while uncertainty regarding [specific issue] remains.</p>
</section>
<section>
  <h2>Hubungkan bukti tanpa menciptakan kesepakatan</h2>
  <p>Bandingkan hasil dengan studi terdahulu berdasarkan arah efek, magnitudo, ukuran, populasi, desain, atau mekanisme. Perbedaan dapat muncul dari sampling, pengukuran, konteks, analisis, atau kebetulan. Sajikan penjelasan sebagai kemungkinan kecuali diuji langsung.</p>
  <p>Gunakan <a href="{{link:hedging}}">hedging akademik</a> untuk mengalibrasi alternatif, bukan membuat semua kalimat samar.</p>
</section>
<section>
  <h2>Buat keterbatasan memiliki konsekuensi</h2>
  <p>Keterbatasan penting karena mengubah interpretasi, presisi, validitas, transferabilitas, atau identifikasi kausal. Nyatakan akibat dan mitigasinya. Akhiri dengan membedakan hal yang ditetapkan, disarankan, dan perlu diuji selanjutnya.</p>
  <p>Cari pola diskusi di <a href="{{link:phrase_explorer}}?q=interpretasi%20diskusi%20terbatasi">Penjelajah Frasa</a>.</p>
</section>
<aside class="article-note"><h2>Peringatan</h2><p>Jangan memperkuat bahasa karena hasil menarik. Kekuatan klaim mengikuti bukti, bukan kepentingan narasi.</p></aside>
""",
    },
    "hedging": {
        "kind": "article",
        "title": "Hedging Akademik untuk Menyelaraskan Klaim | RhetoriLex",
        "description": "Gunakan hedging akademik untuk menyatakan ketidakpastian, cakupan, frekuensi, dan penjelasan alternatif tanpa membuat prosa samar.",
        "h1": "Hedging akademik mengalibrasi klaim",
        "lede": "Pilih hedge untuk alasan bukti tertentu, lalu tempatkan pada proposisi yang hendak dibatasi.",
        "body": """
<section>
  <h2>Hedging bukan kehati-hatian otomatis</h2>
  <p>Hedge menandai batas pengetahuan: probabilitas, frekuensi, cakupan, pengukuran, desain, atau penjelasan. May menyatakan kemungkinan. Tends to menyatakan pola yang tidak universal. In this sample membatasi populasi. Consistent with menyatakan kompatibilitas tanpa membuktikan mekanisme. Setiap frasa memiliki komitmen berbeda.</p>
  <p>Mulailah dari klaim terkuat yang didukung bukti. Identifikasi unsur yang tidak pasti, lalu batasi unsur itu secara spesifik.</p>
</section>
<section>
  <h2>Cocokkan kata dengan daya inferensi</h2>
  <p class="phrase-template">The findings indicate [descriptive result] within [scope].</p>
  <p class="phrase-template">The findings suggest that [interpretation], although [alternative explanation or limitation] cannot be excluded.</p>
  <p class="phrase-template">The results are consistent with [mechanism], but do not distinguish it from [credible alternative].</p>
  <p>Indicate umumnya lebih kuat daripada suggest. Consistent with menyatakan kesesuaian, bukan konfirmasi.</p>
</section>
<section>
  <h2>Hapus overclaim dan pelemahan yang tidak perlu</h2>
  <p>Periksa setiap modal, adverbia, kuantifier, dan frasa cakupan. Tanyakan bukti yang mendasarinya. Hapus perhaps, possibly, atau may yang menumpuk tanpa fungsi. Perkuat kalimat bila bukti langsung jelas mendukungnya. Gunakan <a href="{{link:preserve_claim_strength}}">Pertahankan Kekuatan Klaim</a>.</p>
</section>
<aside class="article-note"><h2>Peringatan</h2><p>Hedge tidak memperbaiki klaim kausal dari desain yang tidak memadai. May cause tetap merupakan proposisi kausal. Gunakan bahasa asosiasi bila kausalitas tidak teridentifikasi.</p></aside>
""",
    },
    "reviewer_response": {
        "kind": "article",
        "title": "Cara Menulis Tanggapan Reviewer yang Jelas | RhetoriLex",
        "description": "Tulis tanggapan reviewer yang mengidentifikasi masalah, mencatat revisi, menyebut lokasi, dan menyatakan ketidaksetujuan dengan bukti.",
        "h1": "Tanggapan reviewer perlu membuat revisi dapat ditelusuri",
        "lede": "Jawab substansi, nyatakan perubahan, tunjukkan lokasi, dan jelaskan alasan tanpa menciptakan pekerjaan.",
        "body": """
<section>
  <h2>Pisahkan komentar menjadi keputusan</h2>
  <p>Komentar reviewer dapat memuat pertanyaan, permintaan analisis, masalah kata, dan kekhawatiran luas. Pecah menjadi poin yang dapat dijawab. Tentukan apakah perlu merevisi, mengklarifikasi, menambah bukti, menjelaskan pilihan, atau tidak setuju. Jawab kekhawatiran sebelum menjelaskan suntingan kosmetik.</p>
  <p class="phrase-template">We revised [section and location] to clarify [specific issue]. The revised text now states [bounded summary of change].</p>
</section>
<section>
  <h2>Catat perubahan dengan tepat</h2>
  <p>Kutip hanya teks revisi yang diperlukan dan berikan rujukan halaman, baris, bagian, tabel, atau gambar yang sesuai naskah final. Jika analisis ditambah, nyatakan metode dan lokasi hasil. Jika pekerjaan tidak dapat dilakukan, jelaskan batas dan revisi klaim yang terpengaruh.</p>
  <p class="phrase-template">We agree that [shared concern] required clarification. Because [methodological reason], we did not [requested action]; instead, we [bounded revision] and now state [remaining limitation].</p>
</section>
<section>
  <h2>Nyatakan ketidaksetujuan secara metodologis</h2>
  <p>Identifikasi titik kesepakatan, berikan alasan berbasis bukti atau desain, dan jelaskan revisi yang mencegah salah paham. Gunakan standar, sitasi, analisis, atau pedoman pelaporan bila tersedia.</p>
  <p>Temukan pola tanggapan di <a href="{{link:phrase_explorer}}?q=tanggapan%20reviewer">Penjelajah Frasa</a>.</p>
</section>
<aside class="article-note"><h2>Peringatan</h2><p>Jangan mengklaim teks, data, analisis, persetujuan, atau sitasi telah ditambah bila tidak ada dalam revisi. Periksa lokasi setelah paginasi berubah.</p></aside>
""",
    },
    "association_vs_causation": {
        "kind": "article",
        "title": "Asosiasi vs Kausalitas dalam Penulisan Ilmiah | RhetoriLex",
        "description": "Bedakan asosiasi dari kausalitas dan pilih verba yang sesuai dengan bukti observasional, eksperimental, dan kausal.",
        "h1": "Asosiasi dan kausalitas membuat klaim berbeda",
        "lede": "Asosiasi menjelaskan relasi pada data teramati. Klaim kausal menjelaskan perubahan di bawah intervensi.",
        "body": """
<section>
  <h2>Identifikasi proposisi di dalam verba</h2>
  <p>Associated with, correlated with, differed, dan predicted dapat menjelaskan relasi statistik tanpa menyatakan bahwa perubahan satu variabel mengubah variabel lain. Caused, led to, improved, reduced, prevented, dan affected umumnya menyatakan perubahan kausal. Urutan waktu serta penyesuaian saja tidak mengubah asosiasi menjadi efek kausal.</p>
  <p>Interpretasi kausal bergantung pada desain dan asumsi mengenai intervensi, exchangeability, positivity, consistency, urutan waktu, pengukuran, interference, attrition, dan analisis target efek.</p>
</section>
<section>
  <h2>Tulis ulang overclaim observasional</h2>
  <p class="phrase-template">In this observational analysis, exposure X was associated with outcome Y after adjustment for [measured covariates].</p>
  <p class="phrase-template">Participants with [exposure] had [difference] in outcome Y; unmeasured confounding and reverse causation remain possible.</p>
  <p>Pola ini melaporkan relasi dan batas. Penyesuaian variabel terukur tidak otomatis menghapus semua bias.</p>
</section>
<section>
  <h2>Gunakan bahasa kausal dengan kontrak kausal</h2>
  <p>Nyatakan desain, target efek, asumsi identifikasi, dan diagnostik. Jelaskan pelanggaran serta analisis sensitivitas. Studi acak pun perlu memperhatikan kepatuhan, outcome hilang, interference, dan estimand. Cari pola asosiasi di <a href="{{link:phrase_explorer}}?q=asosiasi%20observasional">Penjelajah Frasa</a>.</p>
</section>
<aside class="article-note"><h2>Peringatan</h2><p>Mengganti causes dengan may cause tidak menghapus klaim kausal. Jika desain hanya mendukung asosiasi, ubah relasinya.</p></aside>
""",
    },
    "preserve_claim_strength": {
        "kind": "article",
        "title": "Pertahankan Kekuatan Klaim Saat Menulis Ulang | RhetoriLex",
        "description": "Pertahankan daya tentatif, terbatasi, tegas, dan kausal saat memparafrasakan, menyunting, meringkas, atau menerjemahkan klaim.",
        "h1": "Pertahankan kekuatan klaim ketika kata berubah",
        "lede": "Penulisan ulang hanya setia bila menjaga komitmen sumber dan ketidakpastian yang tersisa.",
        "body": """
<section>
  <h2>Petakan komitmen sumber</h2>
  <p>Kekuatan klaim mencakup relasi bukti, modalitas, frekuensi, cakupan, perbandingan, dan status kausal. Suggests tidak setara dengan demonstrates. In this sample tidak setara dengan generally. Was associated with tidak setara dengan reduced. No increase tidak setara dengan penurunan.</p>
  <p>Sebelum menyunting, tandai proposisi utama dan setiap pembatas. Catat sitasi, angka, satuan, interval, negasi, arah, populasi, konteks, waktu, dan penjelasan alternatif.</p>
</section>
<section>
  <h2>Gunakan tangga kekuatan yang eksplisit</h2>
  <div class="move-sequence">
    <div><strong>Tentatif</strong><p>The findings may reflect [interpretation].</p></div>
    <div><strong>Terbatasi</strong><p>Within [scope], the findings support [interpretation].</p></div>
    <div><strong>Tegas</strong><p>The analysis demonstrates [directly established result].</p></div>
    <div><strong>Kausal</strong><p>Under [identified design and assumptions], exposure X changed outcome Y.</p></div>
  </div>
  <p>Jangan bergerak naik demi kelancaran. Bergerak turun juga dapat mendistorsi hasil yang didukung kuat.</p>
</section>
<section>
  <h2>Verifikasi dalam dua arah</h2>
  <p>Tanyakan apakah sumber mencakup penulisan ulang. Lalu periksa apakah penulisan ulang menambah proposisi yang tidak dicakup sumber. Bandingkan semua unsur dilindungi. Gunakan <a href="{{link:paraphrasing}}">panduan parafrasa</a> dan cari <a href="{{link:phrase_explorer}}?q=klaim%20terbatasi">klaim terbatasi</a>.</p>
</section>
<aside class="article-note"><h2>Peringatan</h2><p>Ringkasan pendek rawan menggeser kekuatan karena pembatas dihapus terlebih dahulu. Bila keterbatasan mengubah simpulan, unsur itu bukan detail opsional.</p></aside>
""",
    },
}
