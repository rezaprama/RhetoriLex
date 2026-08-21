"""Konten utama Bahasa Indonesia untuk situs RhetoriLex."""

PAGES_ID = {
    "home": {
        "kind": "home",
        "title": "Skill Parafrasa Akademik Lokal Gratis | RhetoriLex",
        "description": "Gunakan skill parafrasa akademik local-first yang gratis, dengan workbench web, dukungan ramah Indonesia, dan pola penulisan orisinal.",
        "h1": "Skill parafrasa akademik lokal dan gratis.",
        "lede": "Parafrasakan, audit, dan revisi tulisan akademik, ilmiah, teknis, dan Indonesia-Inggris dengan kontrol local-first, cek bukti eksplisit, dan tanpa kewajiban SaaS berbayar.",
        "body": """
<section class="section-block" aria-labelledby="purpose-index-title">
  <div class="section-heading">
    <h2 id="purpose-index-title">Mulai dari masalah penulisan</h2>
    <p>Pilih tugas parafrasa, audit, penulisan, atau revisi. RhetoriLex menghubungkan tujuan, bukti, makna terlindungi, dan pemeriksaan akhir.</p>
  </div>
  <ul class="purpose-index">
    <li><a href="{{link:paraphrase_workbench}}"><strong>Alat Parafrasa</strong><span>Tool local-first yang bisa dipasang dengan endpoint, token, atau model lokal milik sendiri.</span></a></li>
    <li><a href="{{link:academic_writing}}"><strong>Penulisan Akademik</strong><span>Bangun argumen, sintesis, transisi, dan simpulan yang terbatasi.</span></a></li>
    <li><a href="{{link:scientific_writing}}"><strong>Penulisan Ilmiah</strong><span>Laporkan metode, hasil, ketidakpastian, dan batas kausal secara tepat.</span></a></li>
    <li><a href="{{link:phrase_explorer}}"><strong>Penjelajah Frasa</strong><span>Cari katalog orisinal dengan bahasa alami dan filter berdasarkan bukti.</span></a></li>
    <li><a href="{{link:paraphrasing}}"><strong>Parafrasa</strong><span>Pertahankan sitasi, angka, negasi, cakupan, dan daya inferensi.</span></a></li>
    <li><a href="{{link:rhetorical_moves}}"><strong>Gerakan Retoris</strong><span>Rencanakan fungsi paragraf sebelum memilih bunyinya.</span></a></li>
    <li><a href="{{link:research_writing_guides}}"><strong>Panduan Penulisan Riset</strong><span>Gunakan panduan terarah untuk tinjauan, metode, hasil, dan diskusi.</span></a></li>
    <li><a href="{{link:agent_skills}}"><strong>Skill Agen</strong><span>Gunakan RhetoriLex secara lokal dengan pemeriksaan keselamatan yang eksplisit.</span></a></li>
    <li><a href="{{link:about}}"><strong>Tentang</strong><span>Baca catatan clean-room, kepengarangan, lisensi, dan tata kelola.</span></a></li>
  </ul>
</section>
<section class="section-block" aria-labelledby="popular-moves-title">
  <div class="section-heading">
    <h2 id="popular-moves-title">Tugas penulisan populer</h2>
    <p>Buka panduan terarah ketika masalah kalimat sudah jelas.</p>
  </div>
  <ul class="compact-link-index">
    <li><a href="{{link:research_gap}}"><strong>Tetapkan kesenjangan riset</strong><span>Tentukan persoalan spesifik tanpa mengklaim bahwa penelitian tidak ada.</span></a></li>
    <li><a href="{{link:literature_review}}"><strong>Sintesis literatur</strong><span>Bandingkan bukti berdasarkan dasar analitik yang eksplisit.</span></a></li>
    <li><a href="{{link:hedging}}"><strong>Kalibrasi ketidakpastian</strong><span>Pilih hedge yang menandai batas bukti nyata.</span></a></li>
    <li><a href="{{link:association_vs_causation}}"><strong>Pisahkan asosiasi dan kausalitas</strong><span>Gunakan relasi yang didukung desain studi.</span></a></li>
    <li><a href="{{link:reviewer_response}}"><strong>Tanggapi reviewer</strong><span>Buat jawaban dan revisi dapat ditelusuri.</span></a></li>
    <li><a href="{{link:preserve_claim_strength}}"><strong>Pertahankan kekuatan klaim</strong><span>Lindungi daya inferensi saat menyunting atau memparafrasakan.</span></a></li>
  </ul>
</section>
<section class="section-block" aria-labelledby="paper-section-title">
  <div class="section-heading">
    <h2 id="paper-section-title">Telusuri berdasarkan bagian tulisan</h2>
    <p>Gunakan panduan bagian ketika Anda tahu lokasi kalimat tetapi belum mengetahui gerakannya.</p>
  </div>
  <nav class="section-links" aria-label="Bagian tulisan">
    <a href="{{link:research_gap}}">Pendahuluan</a>
    <a href="{{link:literature_review}}">Tinjauan pustaka</a>
    <a href="{{link:methods}}">Metode</a>
    <a href="{{link:results}}">Hasil</a>
    <a href="{{link:discussion}}">Diskusi</a>
    <a href="{{link:thesis}}">Tesis</a>
  </nav>
</section>
<section class="section-block comparison-block" aria-labelledby="evidence-title">
  <div class="section-heading">
    <h2 id="evidence-title">Gaya mengikuti bukti</h2>
    <p>Kalimat yang lancar tetap dapat menyalahartikan studi. Selaraskan relasi bukti sebelum memoles prosa.</p>
  </div>
  <div class="comparison-lines">
    <div><strong>Klaim kausal tanpa dukungan</strong><p>Our observational analysis proves that exposure X causes outcome Y.</p></div>
    <div><strong>Klaim yang selaras dengan bukti</strong><p>In this observational analysis, exposure X was associated with outcome Y.</p></div>
  </div>
</section>
<section class="section-block install-block" aria-labelledby="install-home-title">
  <div>
    <h2 id="install-home-title">Gratis, lokal, bisa dipasang</h2>
    <p>Buka workbench, unduh katalog JSON rilis, tinjau provenans clean-room, atau pasang Skill Agen lokal.</p>
  </div>
  <pre><code>$skill-installer https://github.com/rezaprama/RhetoriLex/tree/main/skills/rhetorilex</code></pre>
  <ul class="resource-links">
    <li><a href="{{link:paraphrase_workbench}}">Buka Alat Parafrasa</a></li>
    <li><a href="https://rezaprama.github.io/RhetoriLex/data/phrases.json">Buka dataset</a></li>
    <li><a href="https://github.com/rezaprama/RhetoriLex/blob/main/PROVENANCE.md">Baca metodologi dan provenans</a></li>
    <li><a href="{{link:agent_skills}}">Baca instalasi dan contoh prompt</a></li>
  </ul>
</section>
""",
    },
    "academic_writing": {
        "kind": "article",
        "title": "Penulisan Akademik: Tujuan, Struktur, dan Bukti | RhetoriLex",
        "description": "Panduan praktis penulisan akademik berdasarkan tujuan retoris, dengan gerakan paragraf, kontrol sikap, sintesis, dan pemeriksaan revisi.",
        "h1": "Penulisan akademik dimulai dari tujuan retoris",
        "lede": "Rencanakan fungsi setiap kalimat, lalu pilih bahasa yang sesuai dengan bukti dan argumen.",
        "body": """
<section>
  <h2>Bergerak dari tugas ke fungsi retoris</h2>
  <p>Penulisan akademik lebih mudah direvisi ketika setiap kalimat memiliki pekerjaan. Tinjauan pustaka dapat mendefinisikan bidang, mengatur posisi, membandingkan temuan, menunjukkan ketidakpastian, atau menetapkan kesenjangan riset. Diskusi dapat menafsirkan hasil, menghubungkannya dengan penelitian terdahulu, membatasi cakupan, dan menjelaskan implikasi. Fungsi tersebut berhubungan, tetapi tidak dapat saling menggantikan.</p>
  <p>Sebelum menulis, beri label sederhana pada setiap paragraf: konteks, masalah, bukti, interpretasi, keterbatasan, atau kontribusi. Jika satu paragraf memerlukan tiga label, logikanya mungkin perlu dipisah. Setelah urutan jelas, gunakan <a href="{{link:phrase_explorer}}">Penjelajah Frasa</a> untuk mencari pola bagi gerakan tertentu.</p>
</section>
<section>
  <h2>Kendalikan sikap dalam satu paragraf</h2>
  <p>Sikap ilmiah bukan satu kata peredam yang ditambahkan di dekat verba. Sikap merupakan relasi antara mutu bukti, kekuatan klaim, cakupan, dan kepastian. Bukti langsung dapat mendukung klaim deskriptif yang tegas. Bukti observasional dapat mendukung asosiasi, tetapi biasanya tidak mendukung pernyataan kausal tanpa batas. Bukti kontekstual dapat memotivasi pertanyaan tanpa menyelesaikannya.</p>
  <div class="reference-table" role="region" aria-label="Keputusan penulisan akademik" tabindex="0">
    <table>
      <thead><tr><th>Kebutuhan</th><th>Gerakan berguna</th><th>Periksa sebelum digunakan</th></tr></thead>
      <tbody>
        <tr><td>Menghubungkan studi</td><td>Sintesis kesepakatan dan perbedaan</td><td>Apakah studi yang disitasi mendukung cakupan yang sama?</td></tr>
        <tr><td>Menyatakan kesenjangan</td><td>Tentukan persoalan yang belum selesai</td><td>Apakah kesenjangan spesifik dan dapat dibuktikan?</td></tr>
        <tr><td>Menafsirkan hasil</td><td>Ajukan penjelasan yang terbatasi</td><td>Apakah mekanisme lain juga sesuai dengan bukti?</td></tr>
        <tr><td>Menyimpulkan</td><td>Kembali ke kontribusi dan batas</td><td>Apakah simpulan melampaui analisis?</td></tr>
      </tbody>
    </table>
  </div>
</section>
<section>
  <h2>Revisi untuk kesinambungan dan ketepatan</h2>
  <p>Baca kalimat pertama setiap paragraf sebagai satu urutan. Urutan itu harus menampakkan argumen tulisan tanpa bergantung pada transisi formulaik. Lalu periksa jangkar bukti setiap klaim. Sitasi harus tetap mendukung proposisi yang sama setelah penulisan ulang. Angka harus mempertahankan satuan, kelompok pembanding, interval, dan arah. Negasi serta kata pembatas seperti hanya, mungkin, dalam, dan pada kondisi tertentu harus diperlakukan sebagai makna yang dilindungi.</p>
  <p>Akhiri dengan pemadatan. Hapus frasa yang mengulang klaim tanpa menambah logika. Gunakan subjek dan verba yang tepat ketika pelaku atau proses penting. Pertahankan istilah teknis bila sinonim yang lebih pendek mengubah makna disipliner.</p>
</section>
<aside class="article-note">
  <h2>Pemeriksaan revisi cepat</h2>
  <p>Dapatkah Anda menamai gerakan, menunjukkan bukti, menyatakan cakupan, dan menjelaskan mengapa tingkat kepastian dapat dibenarkan? Jika tidak, revisi penalaran sebelum kata-katanya.</p>
</aside>
""",
    },
    "scientific_writing": {
        "kind": "article",
        "title": "Penulisan Ilmiah: Metode, Hasil, dan Batas Kausal | RhetoriLex",
        "description": "Tulis metode, hasil, dan interpretasi ilmiah dengan desain, ketidakpastian, ukuran efek, serta pengaman kausal yang eksplisit.",
        "h1": "Penulisan ilmiah menghubungkan bahasa dengan desain studi",
        "lede": "Laporkan apa yang diukur, diestimasi, dan didukung tanpa membiarkan prosa melampaui analisis.",
        "body": """
<section>
  <h2>Jaga metode agar dapat ditelusuri dan direproduksi</h2>
  <p>Bagian metode harus membantu pembaca yang kompeten memahami populasi, bahan, variabel, prosedur, eksklusi, estimand, dan analisis. Nyatakan pilihan yang memengaruhi interpretasi. Bentuk pasif dapat berguna ketika prosedur lebih penting daripada pelaku, tetapi jangan gunakan bentuk itu untuk menyembunyikan siapa yang membuat keputusan atau bagaimana klasifikasi ditetapkan.</p>
  <p>Hubungkan setiap estimasi yang dilaporkan dengan metode yang sesuai. Jika model berubah antar-analisis, nyatakan himpunan penyesuaian dan tujuannya. Jika data hilang, pengujian majemuk, kesalahan pengukuran, atau analisis sensitivitas memengaruhi hasil, laporkan agar pembaca dapat mengaitkan masalah dengan estimasi.</p>
</section>
<section>
  <h2>Pisahkan observasi dari interpretasi</h2>
  <p>Bagian hasil sebaiknya melaporkan arah, magnitudo, ketidakpastian, dan perbandingan yang dilakukan. Signifikansi statistik saja bukan interpretasi kepentingan praktis atau ilmiah. Berikan estimasi dan interval bila sesuai, pertahankan satuan, dan jangan mengubah hasil yang tidak signifikan menjadi bukti ketiadaan efek.</p>
  <div class="reference-table" role="region" aria-label="Tanggung jawab bagian ilmiah" tabindex="0">
    <table>
      <thead><tr><th>Bagian</th><th>Tanggung jawab utama</th><th>Risiko umum</th></tr></thead>
      <tbody>
        <tr><td>Metode</td><td>Jelaskan desain dan keputusan analitik</td><td>Menghilangkan pilihan yang membentuk estimand</td></tr>
        <tr><td>Hasil</td><td>Laporkan estimasi dan ketidakpastian</td><td>Mengganti magnitudo dengan label signifikansi</td></tr>
        <tr><td>Diskusi</td><td>Tafsirkan dalam batas desain</td><td>Menyajikan asosiasi sebagai sebab</td></tr>
        <tr><td>Simpulan</td><td>Nyatakan kontribusi yang terbatasi</td><td>Menggeneralisasi di luar populasi atau konteks</td></tr>
      </tbody>
    </table>
  </div>
</section>
<section>
  <h2>Perlakukan bahasa kausal sebagai klaim desain</h2>
  <p>Kata caused, led to, reduced, improved, dan prevented membuat klaim tentang perubahan kontrafaktual. Klaim ini memerlukan lebih dari asosiasi kuat. Pernyataan kausal yang kredibel bergantung pada desain, asumsi identifikasi, urutan waktu, pengendalian perancu, pengukuran, dan analisis. Bila kondisi itu tidak terpenuhi, gunakan bahasa deskriptif atau asosiatif dan nyatakan ketidakpastian yang tersisa.</p>
  <p>Cari <a href="{{link:phrase_explorer}}?q=interpretasi%20hati-hati">interpretasi hati-hati</a> atau <a href="{{link:phrase_explorer}}?q=asosiasi%20observasional">asosiasi observasional</a>. Penjelajah menampilkan pola bahasa Inggris beserta kebutuhan buktinya.</p>
</section>
<aside class="article-note">
  <h2>Sebelum mengirim naskah</h2>
  <p>Cocokkan setiap angka dengan keluaran analisis, setiap rujukan tabel dengan tata letak final, dan setiap verba kausal dengan desain studi. Minta ahli bidang meninjau klaim yang bergantung pada asumsi khusus.</p>
</aside>
""",
    },
    "phrase_explorer": {
        "kind": "explorer",
        "title": "Penjelajah Frasa Akademik Berdasarkan Tujuan Retoris | RhetoriLex",
        "description": "Cari pola akademik bahasa Inggris yang orisinal berdasarkan tujuan alami, bagian, fungsi, kekuatan klaim, kebutuhan bukti, dan risiko.",
        "h1": "Temukan frasa akademik berdasarkan tujuan retoris",
        "lede": "Jelaskan fungsi kalimat. Hasil menampilkan kebutuhan bukti dan risiko klaim sebelum pola disalin.",
        "body": """
<section class="language-notice" aria-labelledby="pattern-language-title">
  <h2 id="pattern-language-title">Bahasa antarmuka dan bahasa pola dipisahkan</h2>
  <p>Pola frasa tetap dalam bahasa Inggris. Label, panduan, dan bantuan pencarian tersedia dalam Bahasa Indonesia. Mengganti locale tidak menerjemahkan atau mengubah pola katalog.</p>
</section>
<section class="explainer-grid" aria-labelledby="read-entry-title">
  <div>
    <h2 id="read-entry-title">Cara membaca referensi frasa</h2>
    <p>Template adalah struktur awal, bukan kalimat yang ditempel tanpa perubahan. Fungsi menjelaskan pekerjaan retoris. Kekuatan klaim dan kebutuhan bukti menunjukkan kondisi sebelum pola layak dipakai. Catatan serta pengaman kausal menandai hal yang memerlukan tinjauan manusia.</p>
  </div>
  <div>
    <h2>Adaptasi, lalu verifikasi</h2>
    <p>Ganti setiap placeholder dengan isi khusus naskah. Bandingkan hasilnya dengan klaim dan bukti sumber. Pertahankan sitasi, angka, satuan, negasi, arah perbandingan, populasi, waktu, dan ketidakpastian. Menyalin pola tidak memindahkan dukungan dari studi lain.</p>
  </div>
</section>
<section class="reference-anatomy" aria-labelledby="anatomy-title">
  <h2 id="anatomy-title">Anatomi entri referensi</h2>
  <article class="phrase-entry static-entry">
    <div class="entry-meta"><code>EXAMPLE-BOUNDING</code><span>Diskusi</span><span>Klaim tentatif</span></div>
    <h3>Membatasi interpretasi</h3>
    <p class="phrase-template">Taken together, these findings suggest that [bounded interpretation], although [limitation] constrains conclusions about [scope].</p>
    <button class="copy-button" type="button" data-copy-value="Taken together, these findings suggest that [bounded interpretation], although [limitation] constrains conclusions about [scope].">Salin pola</button>
    <dl class="entry-facts"><div><dt>Kebutuhan bukti</dt><dd>Konvergen</dd></div><div><dt>Risiko</dt><dd>Rendah bila keterbatasan dinyatakan</dd></div><div><dt>Pengaman kausal</dt><dd>Tidak diperlukan untuk pola tentatif ini</dd></div></dl>
  </article>
</section>
""",
    },
    "paraphrasing": {
        "kind": "article",
        "title": "Parafrasa Akademik Tanpa Pergeseran Makna | RhetoriLex",
        "description": "Parafrasakan prosa akademik sambil mempertahankan sitasi, angka, satuan, negasi, cakupan, arah perbandingan, dan ketidakpastian.",
        "h1": "Parafrasa adalah tugas mempertahankan makna",
        "lede": "Ubah kata-kata setelah mengidentifikasi fakta, logika, cakupan, dan daya inferensi yang harus tetap sama.",
        "body": """
<section>
  <h2>Lindungi makna sebelum mengubah bentuk</h2>
  <p>Keberhasilan parafrasa tidak diukur dari jumlah sinonim atau perbedaan permukaan. Ukurannya adalah apakah kalimat baru membuat klaim yang sama dan tetap didukung. Mulailah dengan menandai unsur yang dilindungi: sitasi, nama, angka, satuan, interval, istilah teknis, negasi, arah perbandingan, populasi, konteks, waktu, modalitas, dan status kausal.</p>
  <p>Perhatikan pernyataan sumber: Study A reported no increase in outcome Y after 12 weeks (Lee, 2024). Parafrasa yang aman harus mempertahankan temuan negatif, outcome, periode 12 minggu, dan sitasi. Mengubah no increase menjadi reduced, atau menghapus periode waktu, mengubah klaim.</p>
</section>
<section>
  <h2>Gunakan alur berbasis batasan</h2>
  <ol class="workflow-list compact">
    <li><strong>Ekstrak invarian</strong><span>Daftar bukti, angka, relasi, dan kata pembatas yang tidak boleh berubah.</span></li>
    <li><strong>Nyatakan proposisi dengan lugas</strong><span>Tulis makna yang didukung tanpa berusaha terdengar lebih indah.</span></li>
    <li><strong>Bangun ulang kalimat</strong><span>Ubah struktur dan penekanan sambil mempertahankan istilah disipliner yang bermakna tepat.</span></li>
    <li><strong>Periksa dua arah</strong><span>Tanyakan apakah sumber mencakup parafrasa dan apakah parafrasa menambah proposisi tanpa dukungan.</span></li>
  </ol>
</section>
<section>
  <h2>Waspadai pergeseran yang halus</h2>
  <p>Makna sering berubah melalui suntingan kecil. May menjadi will. Associated with menjadi led to. Some participants menjadi participants. Higher than menjadi different from. Hasil pada satu konteks menjadi klaim umum. Sitasi berpindah ke kalimat yang berisi proposisi baru yang tidak didukung sumber.</p>
  <p>Jika suatu bagian sudah ringkas, sangat teknis, atau memiliki bentuk hukum tetap, parafrasa mungkin bukan tujuan yang tepat. Kutip secara singkat bila beralasan dan diizinkan, berikan sitasi, atau pertahankan istilah teknis sambil menulis ulang penjelasan di sekitarnya. Jangan melakukan parafrasa untuk menyamarkan ketergantungan pada sumber.</p>
</section>
<aside class="article-note">
  <h2>Gunakan RhetoriLex dengan aman</h2>
  <p>Minta Skill Agen melindungi sitasi, angka, dan negasi secara eksplisit. Setelah itu, verifikasi keluaran terhadap sumber. Baca pola prompt di <a href="{{link:agent_skills}}">Skill Agen</a>.</p>
</aside>
""",
    },
    "paraphrase_workbench": {
        "kind": "workbench",
        "title": "Alat Parafrasa Lokal Gratis | RhetoriLex",
        "description": "Gunakan alat parafrasa local-first yang bisa dipasang, memakai endpoint OpenAI-compatible milik sendiri, batas harian browser, dan cek bukti.",
        "h1": "Alat parafrasa lokal gratis.",
        "lede": "Gunakan endpoint AI atau model lokal milik sendiri untuk menulis ulang teks akademik, ilmiah, teknis, dan Indonesia-Inggris sambil menjaga bukti dan makna.",
        "body": """
<section>
  <h2>Mengapa local-first penting</h2>
  <p>Banyak layanan parafrasa meminta penulis menempel draft ke form remote dan membayar untuk batas yang lebih longgar. RhetoriLex memilih jalur berbeda. Aplikasi publik ini statis, bisa dipasang, dan gratis. Aplikasi dapat membuat prompt aman tanpa endpoint, atau memanggil hanya endpoint OpenAI-compatible yang dimasukkan pengguna.</p>
  <p>Dengan cara ini, alat tetap berguna bagi peneliti, mahasiswa, dosen pembimbing, editor, dan penulis Indonesia yang membutuhkan bahasa Inggris hati-hati tanpa menjadikan setiap kalimat sebagai request berbayar. Aplikasi tidak menyimpan naskah di server RhetoriLex karena versi web saat ini tidak punya database naskah server-side.</p>
</section>
<section>
  <h2>Pilihan setup aman</h2>
  <div class="reference-table" role="region" aria-label="Pilihan setup alat parafrasa" tabindex="0">
    <table>
      <thead><tr><th>Pilihan</th><th>Cara kerja</th><th>Pemeriksaan privasi</th></tr></thead>
      <tbody>
        <tr><td>Prompt saja</td><td>RhetoriLex membuat instruksi dan checklist invarian.</td><td>Tidak ada panggilan AI keluar dari browser.</td></tr>
        <tr><td>Endpoint lokal</td><td>Gunakan server lokal OpenAI-compatible seperti gateway model lokal.</td><td>Jaga endpoint tetap di mesin atau jaringan sendiri.</td></tr>
        <tr><td>Endpoint provider</td><td>Masukkan endpoint, model, dan token sendiri bila provider mengizinkan panggilan browser.</td><td>Teks dikirim ke provider itu, bukan ke RhetoriLex.</td></tr>
      </tbody>
    </table>
  </div>
</section>
<section>
  <h2>Mengapa batas web hosted bersifat lokal</h2>
  <p>Halaman publik menerapkan batas tiga panggilan harian di storage browser. Ini batas pemakaian ringan, bukan keamanan akun. Tujuannya mencegah pemakaian berlebihan tanpa membuat situs statis kehilangan sifat gratis dan mudah deploy di GitHub Pages.</p>
  <p>Layanan hosted dengan shared key sungguhan membutuhkan backend. Desain yang direncanakan adalah Worker API kecil, tabel D1 untuk kuota harian anonim, cache KV untuk keputusan rate-limit, Turnstile untuk menahan abuse, token provider hanya sebagai server secret, dan logging naskah mati secara default. Backend itu sengaja dipisahkan dari aplikasi statis saat ini.</p>
</section>
<aside class="article-note">
  <h2>Gunakan hasil sebagai draft</h2>
  <p>Selalu bandingkan keluaran dengan sumber. Verifikasi sitasi, angka, istilah, negasi, ketidakpastian, kekuatan klaim, dan aturan jurnal atau kampus sebelum dikumpulkan.</p>
</aside>
""",
    },
}
