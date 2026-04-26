"use client";

import React, { createContext, useContext, useState, useEffect } from "react";

type Language = "id" | "en";

interface LanguageContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: (key: string) => string;
}

const translations = {
  id: {
    "nav.home": "Beranda",
    "nav.stats": "Statistik",
    "nav.map": "Peta Sebaran",
    "nav.media": "Media & YouTube",
    "nav.upload": "Analisis Mandiri",
    "nav.cta": "Input Data",
    
    "hero.badge": "Laporan Eksklusif - Data Terverifikasi",
    "hero.title": "Krisis Tersembunyi di Perguruan Tinggi Indonesia",
    "hero.subtitle": "Sebuah manifestasi krisis sistemik dalam ekosistem akademik Indonesia, dipetakan melalui metode scraping media nasional, kanal digital, dan dokumen resmi yang menunjukkan urgensi reformasi institusional.",
    "hero.cta.stats": "Bedah Data Lengkap",
    "hero.cta.map": "Peta Interaktif",
    "hero.scroll": "Eksplorasi Lebih Lanjut",
    
    "stats.total_reports": "Total Laporan Terdokumentasi",
    "stats.universities": "Institusi Pendidikan Terlibat",
    "stats.provinces": "Provinsi Sebaran Kasus",
    "stats.growth": "Eskalasi Laporan Tahunan",
    
    "stats.title": "Disertasi Data & Analisis Yuridis",
    "stats.subtitle": "Dekomposisi data kekerasan seksual sebagai instrumen kritik terhadap kebijakan pencegahan yang belum optimal di level pendidikan tinggi.",
    
    "story.trend.title": "Eskalasi Krisis: Paradoks 'Kampus Aman'",
    "story.trend.p1": "Analisis temporal menunjukkan lonjakan signifikan dalam pelaporan, yang mengindikasikan bukan sekadar peningkatan kasus, melainkan pecahnya budaya bungkam yang selama ini dipelihara oleh birokrasi kampus.",
    "story.trend.p2": "Secara kritis, tren ini mencerminkan kegagalan sistem pengawasan internal. Lonjakan tajam di periode tertentu membuktikan bahwa instrumen hukum kampus seringkali bersifat reaktif, bukan preventif. Data ini menuntut dekonstruksi total terhadap cara institusi memandang integritas moral di atas perlindungan korban.",
    "story.trend.cta": "Lihat Analisis Tren Selengkapnya",
    
    "story.spectrum.title": "Tipologi Kekerasan: Spektrum Pelanggaran Hak",
    "story.spectrum.p1": "Visualisasi ini membedah berbagai manifestasi kekerasan seksual, mulai dari pelecehan verbal hingga tindakan fisik yang traumatis. Dominasi kategori tertentu menunjukkan bahwa kekerasan seksual bukan hanya insiden tunggal, melainkan spektrum pelanggaran hak yang seringkali luput dari pengawasan birokrasi kampus karena dianggap sebagai 'dinamika sosial' biasa.",
    "story.spectrum.p2": "Secara analitik, pertumbuhan kasus di ranah digital (KBGO) menandakan adanya pergeseran pola pelaku dalam mengeksploitasi celah teknologi. Kegagalan institusi dalam mengakui kekerasan non-fisik sebagai pelanggaran serius menciptakan impunitas bagi pelaku dan memperpanjang trauma bagi korban yang tidak mendapatkan perlindungan yuridis yang memadai.",
    
    "story.perpetrator.title": "Disfungsi Relasi Kuasa: Hegemoni Otoritas",
    "story.perpetrator.p1": "Statistik ini mengungkap sisi gelap dari hierarki akademik, di mana pelaku seringkali berasal dari kalangan yang memiliki otoritas intelektual dan administratif. Relasi kuasa yang asimetris ini menjadi inkubator utama kekerasan, di mana korban seringkali berada dalam posisi terjepit antara keinginan untuk mencari keadilan dan ketakutan akan hambatan terhadap keberlangsungan studi mereka.",
    "story.perpetrator.p2": "Dominasi pelaku dari staf pengajar dan birokrat kampus adalah tamparan bagi integritas moral perguruan tinggi. Penanganan kasus yang seringkali lebih mementingkan 'reputasi institusi' daripada pemulihan korban membuktikan bahwa feodalisme akademik masih sangat kental, menciptakan perisai impunitas bagi mereka yang berlindung di balik gelar dan jabatan.",

    "story.geography.title": "Episentrum Krisis di Kota Pendidikan",
    "story.geography.p1": "Pemetaan spasial ini mengidentifikasi bahwa pusat-pusat populasi akademik di kota-kota besar seringkali menjadi episentrum krisis. Infrastruktur fisik yang megah dan status sebagai 'Kota Pelajar' ternyata tidak linear dengan jaminan keamanan psikologis dan fisik bagi civitas akademika, terutama bagi kelompok rentan.",
    "story.geography.p2": "Konsentrasi kasus di wilayah tertentu menuntut adanya pemerataan instrumen perlindungan di tingkat nasional. Ketimpangan akses terhadap layanan pendampingan dan lambatnya respons Satgas PPKS di daerah-daerah luar pusat menunjukkan bahwa reformasi kebijakan perlindungan korban harus dilakukan secara holistik tanpa diskriminasi teritorial.",

    "story.escalation.title": "Eskalasi Eksponensial: Fenomena Gunung Es",
    "story.escalation.p1": "Lonjakan data dari tahun 2019 hingga 2026 menggambarkan 'Fenomena Gunung Es' yang akhirnya mulai mencair. Peningkatan angka laporan ini bukan sekadar menunjukkan krisis yang semakin parah, melainkan keberhasilan dari mekanisme pelaporan baru yang mulai memberikan ruang aman bagi korban untuk berbicara setelah bertahun-tahun bungkam.",
    "story.escalation.p2": "Puncaknya pada tahun 2026, di mana hampir separuh dari tindak kekerasan di lingkungan pendidikan adalah kekerasan seksual, menjadi sinyal darurat bagi pemerintah. Statistik ini adalah bukti empiris bahwa kebijakan yang ada saat ini harus ditingkatkan dari sekadar 'penanganan pasca-kejadian' menjadi sistem mitigasi yang mampu memutus rantai kekerasan secara preventif dan sistemik.",

    "story.temporal.title": "Siklus Krisis: Anomali Tahunan",
    "story.temporal.p1": "Analisis fluktuasi waktu menunjukkan adanya pola-pola kritis yang berkaitan dengan siklus akademik tahunan. Masa-masa transisi atau periode kegiatan ekstrakurikuler tertentu seringkali menjadi titik nadir di mana pengawasan institusional melemah, memberikan celah bagi terjadinya pelanggaran hak yang terstruktur.",
    "story.temporal.p2": "Pemetaan waktu ini adalah instrumen krusial bagi manajemen kampus untuk merancang kalender mitigasi yang lebih cerdas. Dengan memahami kapan krisis cenderung memuncak, perguruan tinggi dapat mengalokasikan sumber daya perlindungan secara lebih efektif, memastikan bahwa setiap detik di lingkungan kampus adalah waktu yang aman bagi seluruh mahasiswanya.",
    
    "media.title": "Kanal Investigasi & Resonansi Publik",
    "media.subtitle": "Kompilasi narasi publik dan pemberitaan media massa sebagai bentuk pengawasan eksternal terhadap penanganan kasus di lingkungan kampus.",
    "media.tab.yt": "Kanal Digital",
    "media.tab.news": "Liputan Media",
    
    "map.title": "Peta Sebaran & Distribusi Regional",
    "map.subtitle": "Pemetaan spasial untuk mengidentifikasi episentrum krisis dan urgensi pemerataan instrumen perlindungan di seluruh wilayah Indonesia.",
    "map.description": "Pemetaan spasial institusi pendidikan tinggi.",
    "map.legend.total": "Total Laporan",
    "map.legend.high": "Risiko Tinggi",
    "map.legend.low": "Risiko Rendah",
    "map.legend.none": "Tanpa Laporan",
    "map.search": "Cari Provinsi/Wilayah...",
    "map.popup.total": "DOKUMENTASI LAPORAN",
    "map.popup.report_count": "DOKUMENTASI LAPORAN",
    "map.popup.decomposition": "DEKOMPOSISI WILAYAH GEOGRAFIS",
    "map.popup.clusters": "KLASTER INSTITUSI TERPAPAR",
    "map.popup.institution_label": "INSTITUSI TERLAPOR",
    "map.popup.reported": "INSTITUSI TERLAPOR",
    "map.popup.no_data": "Data belum teridentifikasi",
    "map.sidebar.jurisdiction": "Yurisdiksi Geografis",
    "map.sidebar.mapping": "Pemetaan spasial institusi pendidikan tinggi.",
    "map.sidebar.region": "WILAYAH",
    "map.sidebar.epicenter": "EPISENTRUM",

    "stats.badge.dissertation": "DISERTASI DATA ANALITIK",
    "stats.badge.typology": "TIPOLOGI TINDAK",
    "stats.badge.power": "DISFUNGSI RELASI KUASA",
    "stats.badge.geography": "YURISDIKSI GEOGRAFIS",
    "stats.badge.escalation": "ESKALASI KRISIS (2019 - 2026)",
    "stats.badge.temporal": "ANALISIS TEMPORAL",
    "stats.cta.title": "AKSES YURISDIKSI WILAYAH",
    "stats.cta.subtitle": "Pemetaan spasial secara real-time untuk dekonstruksi wilayah berisiko tinggi di tingkat nasional.",
    "stats.cta.button": "BUKA PETA INTERAKTIF",
    "stats.unit.reports": "Laporan",
    "stats.unit.cases": "Kasus",
    "stats.unit.total": "Jumlah",
    "stats.unit.escalation": "Eskalasi",

    "upload.title": "Engine Analisis Mandiri",
    "upload.subtitle": "Dekonstruksi dataset Anda secara privat melalui algoritma deduksi narasi SIGAP.",
    "upload.back": "KEMBALI KE BERANDA"
  },
  en: {
    "nav.home": "Home",
    "nav.stats": "Statistics",
    "nav.map": "Distribution Map",
    "nav.media": "Media & YouTube",
    "nav.upload": "Self Analysis",
    "nav.cta": "Input Data",
    
    "hero.badge": "Exclusive Report - Verified Data",
    "hero.title": "The Hidden Crisis in Indonesian Higher Education",
    "hero.subtitle": "A manifestation of systemic crisis within the Indonesian academic ecosystem, mapped through scraping national media, digital channels, and official documents, highlighting the urgency of institutional reform.",
    "hero.cta.stats": "Full Data Breakdown",
    "hero.cta.map": "Interactive Map",
    "hero.scroll": "Explore Further",
    
    "stats.total_reports": "Total Documented Reports",
    "stats.universities": "Involved Educational Institutions",
    "stats.provinces": "Provinces with Case Spreads",
    "stats.growth": "Annual Report Escalation",
    
    "stats.title": "Data Dissertation & Juridical Analysis",
    "stats.subtitle": "Decomposition of sexual violence data as a critical instrument against suboptimal prevention policies at the higher education level.",
    
    "story.trend.title": "Crisis Escalation: The 'Safe Campus' Paradox",
    "story.trend.p1": "Temporal analysis shows a significant surge in reporting, indicating not just an increase in cases, but the breaking of the culture of silence maintained by campus bureaucracies.",
    "story.trend.p2": "Critically, this trend reflects the failure of internal oversight systems. Sharp spikes in specific periods prove that campus legal instruments are often reactive rather than preventive. This data demands a total deconstruction of how institutions prioritize moral integrity over victim protection.",
    "story.trend.cta": "View Full Trend Analysis",
    
    "story.spectrum.title": "Typology of Violence: Spectrum of Rights Violations",
    "story.spectrum.p1": "This visualization dissects various manifestations of sexual violence, ranging from verbal harassment to traumatic physical acts. The dominance of specific categories shows that sexual violence is not just a single incident, but a spectrum of rights violations that often escapes campus bureaucratic oversight because it is dismissed as common 'social dynamics'.",
    "story.spectrum.p2": "Analytically, the growth of cases in the digital realm (OCBV) indicates a shift in perpetrator patterns exploiting technological loopholes. The failure of institutions to recognize non-physical violence as a serious violation creates impunity for perpetrators and prolongs trauma for victims who do not receive adequate juridical protection.",
    
    "story.perpetrator.title": "Power Relation Dysfunction: Authority Hegemony",
    "story.perpetrator.p1": "These statistics reveal the dark side of the academic hierarchy, where perpetrators often come from circles possessing intellectual and administrative authority. This asymmetric power relationship becomes the primary incubator of violence, where victims are often trapped between the desire for justice and the fear of obstacles to their academic continuity.",
    "story.perpetrator.p2": "The dominance of perpetrators from faculty and campus bureaucrats is a slap to the moral integrity of higher education. Case handling that often prioritizes 'institutional reputation' over victim recovery proves that academic feudalism is still prevalent, creating a shield of impunity for those hiding behind degrees and titles.",

    "story.geography.title": "Crisis Epicenter in Education Cities",
    "story.geography.p1": "This spatial mapping identifies that academic population centers in major cities often become crisis epicenters. Grand physical infrastructure and status as a 'Student City' turn out not to be linear with guarantees of psychological and physical safety for the academic community, especially for vulnerable groups.",
    "story.geography.p2": "The concentration of cases in specific regions demands the equalization of protection instruments at the national level. Disparities in access to advocacy services and the slow response of PPKS Task Forces in outlying areas indicate that victim protection policy reform must be carried out holistically without territorial discrimination.",

    "story.escalation.title": "Exponential Escalation: The Iceberg Phenomenon",
    "story.escalation.p1": "The surge in data from 2019 to 2026 illustrates the 'Iceberg Phenomenon' that is finally beginning to melt. This increase in reporting numbers does not merely show a worsening crisis, but rather the success of new reporting mechanisms that have started to provide a safe space for victims to speak out after years of silence.",
    "story.escalation.p2": "Peak year 2026, where nearly half of violence in educational environments is sexual violence, serves as an emergency signal for the government. These statistics are empirical evidence that existing policies must be upgraded from mere 'post-incident handling' to a mitigation system capable of breaking the chain of violence preventively and systemically.",

    "story.temporal.title": "Crisis Cycle: Annual Anomalies",
    "story.temporal.p1": "Time fluctuation analysis shows critical patterns related to annual academic cycles. Transition periods or specific extracurricular activity periods often become nadir points where institutional oversight weakens, providing gaps for structured rights violations to occur.",
    "story.temporal.p2": "This time mapping is a crucial instrument for campus management to design smarter mitigation calendars. By understanding when crises tend to peak, universities can allocate protection resources more effectively, ensuring that every second in the campus environment is a safe time for all students.",

    "media.title": "Investigation Channels & Public Resonance",
    "media.subtitle": "Compilation of public narratives and mass media reports as an external oversight of case handling within campus environments.",
    "media.tab.yt": "Digital Channels",
    "media.tab.news": "Media Coverage",
    
    "map.title": "Spatial Mapping & Regional Distribution",
    "map.subtitle": "Spatial mapping to identify crisis epicenters and the urgency of equalizing protection instruments across all regions of Indonesia.",
    "map.description": "Spatial mapping of higher education institutions.",
    "map.legend.total": "Total Reports",
    "map.legend.high": "High Risk",
    "map.legend.low": "Low Risk",
    "map.legend.none": "No Reports",
    "map.search": "Search Province/Region...",
    "map.popup.total": "TOTAL REPORTS",
    "map.popup.report_count": "TOTAL REPORTS",
    "map.popup.decomposition": "REGIONAL DECOMPOSITION",
    "map.popup.clusters": "INSTITUTION CLUSTERS",
    "map.popup.institution_label": "REPORTED",
    "map.popup.reported": "REPORTED",
    "map.popup.no_data": "Data not identified",
    "map.sidebar.jurisdiction": "Geographical Jurisdiction",
    "map.sidebar.mapping": "Spatial mapping of higher education institutions.",
    "map.sidebar.region": "REGION",
    "map.sidebar.epicenter": "EPICENTER",

    "stats.badge.dissertation": "DATA ANALYTIC DISSERTATION",
    "stats.badge.typology": "TYPOLOGY OF VIOLENCE",
    "stats.badge.power": "POWER RELATION DYSFUNCTION",
    "stats.badge.geography": "GEOGRAPHICAL JURISDICTION",
    "stats.badge.escalation": "CRISIS ESCALATION (2019 - 2026)",
    "stats.badge.temporal": "TEMPORAL ANALYSIS",
    "stats.cta.title": "ACCESS REGIONAL JURISDICTION",
    "stats.cta.subtitle": "Real-time spatial mapping for deconstruction of high-risk regions at the national level.",
    "stats.cta.button": "OPEN INTERACTIVE MAP",
    "stats.unit.reports": "Reports",
    "stats.unit.cases": "Cases",
    "stats.unit.total": "Total",
    "stats.unit.escalation": "Escalation",

    "upload.title": "Self-Analysis Engine",
    "upload.subtitle": "Privately deconstruct your dataset through SIGAP's narrative deduction algorithm.",
    "upload.back": "BACK TO HOME"
  }
};

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [language, setLanguage] = useState<Language>("id");

  useEffect(() => {
    const saved = localStorage.getItem("language") as Language;
    if (saved) setLanguage(saved);
  }, []);

  const handleSetLanguage = (lang: Language) => {
    setLanguage(lang);
    localStorage.setItem("language", lang);
  };

  const t = (key: string) => {
    const langData = translations[language];
    return (langData as any)[key] || key;
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage: handleSetLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
}

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) throw new Error("useLanguage must be used within LanguageProvider");
  return context;
};
