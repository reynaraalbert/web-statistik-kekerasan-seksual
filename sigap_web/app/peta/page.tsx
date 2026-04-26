"use client";

import React, { useEffect, useState } from "react";
import dynamic from "next/dynamic";
import Navbar from "@/components/navbar";
import { motion, AnimatePresence } from "framer-motion";
import { useTheme } from "next-themes";
import { Info, Map as MapIcon, Layers, Maximize2, X, ChevronUp } from "lucide-react";
import { cn, formatNumber } from "@/lib/utils";
import { useLanguage } from "@/components/language-provider";

// Dynamic import for the entire Map component (client-side only)
const MapView = dynamic(() => import("@/components/map-view"), { 
  ssr: false,
  loading: () => (
    <div className="h-full w-full flex items-center justify-center bg-background/50 backdrop-blur-sm">
      <div className="flex flex-col items-center gap-4">
        <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin" />
        <p className="text-[10px] font-black tracking-widest text-foreground/40 uppercase">Sinkronisasi Geospasial...</p>
      </div>
    </div>
  )
});

export default function Peta() {
  const { theme } = useTheme();
  const { t, language } = useLanguage();
  const [data, setData] = useState<any>(null);
  const [selectedProv, setSelectedProv] = useState<any>(null);
  const [mounted, setMounted] = useState(false);

  const regionMap: Record<string, string> = {
    "Jawa Barat": "West Java",
    "Jawa Tengah": "Central Java",
    "Jawa Timur": "East Java",
    "DKI Jakarta": "Jakarta Capital Region",
    "DI Yogyakarta": "Yogyakarta Special Region",
    "Sumatera Utara": "North Sumatra",
    "Sumatera Barat": "West Sumatra",
    "Sulawesi Selatan": "South Sulawesi",
    "Sulawesi Utara": "North Sulawesi",
    "Kalimantan Timur": "East Kalimantan",
    "Kalimantan Barat": "West Kalimantan"
  };

  const tlr = (name: string) => {
    if (language === 'id') return name;
    return regionMap[name] || name;
  };

  const campusMap: Record<string, string> = {
    "Universitas Indonesia": "University of Indonesia",
    "Universitas Gadjah Mada": "Gadjah Mada University",
    "Universitas Negeri Yogyakarta": "Yogyakarta State University",
    "Universitas Pendidikan Indonesia": "Indonesia University of Education",
    "Institut Teknologi Bandung": "Bandung Institute of Technology",
    "Universitas Padjadjaran": "Padjadjaran University",
    "Universitas Brawijaya": "Brawijaya University",
    "Universitas Airlangga": "Airlangga University",
    "Universitas Diponegoro": "Diponegoro University",
    "Universitas Sebelas Maret": "Sebelas Maret University",
    "Universitas Hasanuddin": "Hasanuddin University",
    "Universitas Sumatera Utara": "University of North Sumatra",
    "Universitas Andalas": "Andalas University",
    "Universitas Sriwijaya": "Sriwijaya University",
    "Universitas Lampung": "Lampung University",
    "Universitas Negeri Jakarta": "Jakarta State University",
    "Universitas Negeri Semarang": "Semarang State University",
    "Universitas Negeri Malang": "Malang State University",
    "Universitas Negeri Surabaya": "Surabaya State University",
    "Universitas Riau": "University of Riau",
    "Universitas Jember": "University of Jember",
    "Universitas Udayana": "Udayana University",
    "Universitas Pelita Harapan": "Pelita Harapan University",
    "Universitas Gunadarma": "Gunadarma University",
    "Universitas Muhammadiyah Malang": "Muhammadiyah University of Malang",
    "Universitas Muhammadiyah Yogyakarta": "Muhammadiyah University of Yogyakarta",
    "Universitas Palangka Raya": "University of Palangka Raya",
    "Universitas Pancasila": "Pancasila University",
    "Universitas Pattimura": "Pattimura University",
    "Universitas Tanjungpura": "Tanjungpura University",
    "Universitas Bina Nusantara": "Binus University",
    "Universitas Telkom": "Telkom University",
    "Universitas Trisakti": "Trisakti University",
    "Universitas Tarumanagara": "Tarumanagara University",
    "Universitas Atma Jaya Yogyakarta": "Atma Jaya University Yogyakarta",
    "Universitas Katolik Parahyangan": "Parahyangan Catholic University",
    "Universitas Kristen Satya Wacana": "Satya Wacana Christian University"
  };

  const tlc = (name: string) => {
    if (language === 'id') return name;
    return campusMap[name] || name;
  };

  useEffect(() => {
    setMounted(true);
    fetch("/data/sigap.json")
      .then(res => res.json())
      .then(d => setData(d));
  }, []);

  if (!data || !mounted) return null;

  return (
    <main className="h-screen w-full relative overflow-hidden bg-background grainy-bg transition-all duration-700">
      <Navbar />

      {/* Map Implementation */}
      <div className="absolute inset-0 z-0">
        <MapView 
          data={data} 
          theme={theme} 
          setSelectedProv={setSelectedProv} 
        />
      </div>

      {/* UI Overlays - Responsive Position */}
      <div className="absolute top-20 md:top-32 left-4 md:left-8 z-10 pointer-events-none right-4 md:right-auto">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-card p-4 md:p-8 rounded-[24px] md:rounded-[32px] max-w-sm pointer-events-auto w-full"
        >
          <div className="flex items-center gap-2 md:gap-3 mb-1 md:mb-2">
            <div className="p-1.5 md:p-3 bg-primary/10 text-primary rounded-lg md:rounded-2xl">
              <MapIcon className="w-3.5 h-3.5 md:w-6 md:h-6" />
            </div>
            <div>
              <h1 className="text-sm md:text-2xl font-black tracking-tighter text-primary leading-tight">{t("map.title")}</h1>
            </div>
          </div>
          <p className={cn("text-[10px] md:text-sm font-medium leading-relaxed mb-4 md:mb-6", theme === 'dark' ? "text-white" : "text-black")}>
            {t("map.description")}
          </p>
          <div className="grid grid-cols-2 gap-2 md:gap-3">
             <div className="p-2 md:p-3 bg-secondary rounded-lg md:rounded-xl border border-border">
                <span className="text-[7px] md:text-[9px] font-bold uppercase tracking-widest text-black/60 dark:text-white/60">{t("map.sidebar.region")}</span>
                <div className="text-xs md:text-base font-black text-black dark:text-white">{data.overview.total_provinsi}</div>
             </div>
             <div className="p-2 md:p-3 bg-secondary rounded-lg md:rounded-xl border border-border">
                <span className="text-[7px] md:text-[9px] font-bold uppercase tracking-widest text-black/60 dark:text-white/60">{t("map.sidebar.epicenter")}</span>
                <div className="text-xs md:text-base font-black text-[#8B0000] dark:text-white truncate">{tlr(data.provinsi_geo[0]?.name)}</div>
             </div>
          </div>
        </motion.div>
      </div>

      {/* Sidebar / Bottom Sheet for Details */}
      <AnimatePresence>
        {selectedProv && (
          <motion.div
            initial={{ opacity: 0, y: 100, x: 0 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 100 }}
            className={cn(
              "absolute z-30 glass-card p-8 md:p-10 flex flex-col transition-all duration-500 overflow-hidden",
              "bottom-0 left-0 right-0 rounded-t-[50px] h-[80vh] md:h-auto md:max-h-[calc(100vh-160px)] md:top-32 md:right-10 md:left-auto md:w-[480px] md:rounded-[50px] shadow-[0_32px_64px_-12px_rgba(0,0,0,0.3)] border-white/20"
            )}
          >
            {/* Mobile handle */}
            <div className="w-16 h-2 bg-black/10 dark:bg-white/20 rounded-full mx-auto mb-8 md:hidden flex-shrink-0" />

            <div className="flex justify-between items-start mb-4 md:mb-6 flex-shrink-0">
               <div className={cn(
                 "p-5 rounded-[25px] shadow-2xl border border-white/10 transition-colors",
                 theme === 'dark' ? "bg-white text-[#8B0000]" : "bg-primary text-white"
               )}>
                  <div className="text-3xl md:text-4xl font-black tracking-tighter leading-none mb-1">{selectedProv.count}</div>
                  <div className={cn(
                    "text-[10px] font-black uppercase tracking-[0.2em]",
                    theme === 'dark' ? "text-[#8B0000]/80" : "text-white/80"
                  )}>{t("map.popup.report_count")}</div>
               </div>
               <button 
                 onClick={() => setSelectedProv(null)}
                 className="p-3 hover:bg-secondary rounded-full transition-all hover:rotate-90"
               >
                 <X className="w-8 h-8" />
               </button>
            </div>

            <div className="flex-shrink-0 mb-4">
              <h2 className={cn(
                "font-black tracking-tighter mb-1 font-serif leading-[0.9]",
                theme === 'dark' ? "text-white" : "text-[#8B0000]",
                tlr(selectedProv.name).length > 15 ? "text-2xl md:text-4xl" : "text-3xl md:text-5xl"
              )}>
                {tlr(selectedProv.name)}
              </h2>
              <p className={cn("text-[9px] md:text-[10px] font-black uppercase tracking-[0.2em] opacity-40", theme === 'dark' ? "text-white" : "text-black")}>
                {t("map.popup.decomposition")}
              </p>
            </div>

            <div className="flex-1 overflow-y-auto pr-4 custom-scrollbar -mr-4 space-y-8">
              {/* Institutional Cluster Section */}
              <section className="relative">
                <div className={cn(
                  "sticky top-0 z-20 border-b border-primary/10 mb-4 transition-colors",
                  theme === 'dark' ? "bg-[#1a1a1a]" : "bg-white"
                )}>
                  <h4 className="py-2 text-[10px] font-black uppercase tracking-[0.3em] text-primary">
                    {t("map.popup.clusters")}
                  </h4>
                </div>
                
                <div className="space-y-3 max-h-[195px] overflow-y-auto pr-3 custom-scrollbar py-1">
                  {selectedProv.top_universitas && selectedProv.top_universitas.length > 0 ? (
                    selectedProv.top_universitas.map((u: any, i: number) => (
                      <motion.div 
                        key={`${selectedProv.name}-univ-${i}`} 
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: i * 0.1 }}
                        className="p-4 bg-secondary/30 hover:bg-secondary/60 rounded-[20px] border border-border flex justify-between items-center transition-all group"
                      >
                        <div className="flex flex-col min-w-0">
                          <span className={cn(
                            "font-black truncate pr-4 transition-all",
                            theme === 'dark' ? "text-white" : "text-black",
                            tlc(u.name).length > 25 ? "text-xs md:text-sm" : "text-sm md:text-base"
                          )}>
                            {tlc(u.name)}
                          </span>
                          <span className="text-[9px] uppercase font-bold opacity-30 tracking-widest">{t("map.popup.institution_label")}</span>
                        </div>
                        <div className={cn(
                          "px-4 py-2 rounded-xl text-xs font-black shadow-md flex-shrink-0 transition-colors", 
                          theme === 'dark' ? "bg-white !text-black" : "bg-primary text-white"
                        )}>
                          {u.count}
                        </div>
                      </motion.div>
                    ))
                  ) : (
                    <div className="p-6 text-center bg-secondary/10 rounded-[20px] border border-dashed border-border">
                      <p className="text-[10px] opacity-40 font-bold uppercase tracking-widest italic">{t("map.popup.no_data")}</p>
                    </div>
                  )}
                </div>
              </section>

              {/* Typology Distribution Section */}
              <section className="relative pb-10">
                <div className={cn(
                  "sticky top-0 z-20 border-b border-border mb-8 transition-colors",
                  theme === 'dark' ? "bg-[#1a1a1a]" : "bg-white"
                )}>
                  <h4 className="py-2 text-[10px] font-black uppercase tracking-[0.3em] text-[#8B0000] dark:text-white">
                    {t("stats.badge.typology")}
                  </h4>
                </div>
                
                <div className="space-y-10">
                  {selectedProv.jenis_kekerasan && selectedProv.jenis_kekerasan.length > 0 ? (
                    selectedProv.jenis_kekerasan.map((j: any, i: number) => {
                      const pct = (j.value / (selectedProv.count || 1) * 100).toFixed(1);
                      return (
                        <div key={`${selectedProv.name}-type-${i}`} className="flex flex-col gap-4">
                          <div className="flex justify-between text-xs font-black uppercase tracking-[0.2em]">
                            <span className={theme === 'dark' ? "text-white/60" : "text-black/60"}>
                              {j.label}
                            </span>
                            <span className={theme === 'dark' ? "text-white" : "text-[#8B0000]"}>
                              {pct}%
                            </span>
                          </div>
                          <div className="h-4 w-full bg-secondary/30 rounded-full overflow-hidden p-[3px] border border-border/50">
                            <motion.div 
                              initial={{ width: 0 }}
                              whileInView={{ width: `${pct}%` }}
                              transition={{ duration: 1.5, ease: "circOut" }}
                              className="h-full bg-primary rounded-full shadow-[0_0_15px_rgba(139,0,0,0.3)]"
                            />
                          </div>
                        </div>
                      );
                    })
                  ) : (
                    <div className="text-sm opacity-40 italic py-4">Data tipologi tidak tersedia.</div>
                  )}
                </div>
              </section>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

    </main>
  );
}
