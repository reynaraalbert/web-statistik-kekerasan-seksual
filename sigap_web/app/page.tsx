"use client";

import React, { useEffect, useState } from "react";
import Navbar from "@/components/navbar";
import { useLanguage } from "@/components/language-provider";
import { cn, formatNumber } from "@/lib/utils";
import { motion } from "framer-motion";
import { useTheme } from "next-themes";
import { ArrowRight, Info, Map as MapIcon, TrendingUp, AlertTriangle, ShieldCheck, Scale, Gavel } from "lucide-react";
import Link from "next/link";
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from "recharts";

export default function Home() {
  const { t, language } = useLanguage();
  const { resolvedTheme: theme } = useTheme();
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    fetch("/data/sigap.json")
      .then(res => res.json())
      .then(d => setData(d));
  }, []);

  if (!data) return (
    <div className="h-screen w-full flex items-center justify-center bg-background">
      <div className="flex flex-col items-center gap-4">
        <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin" />
        <p className="text-sm font-black tracking-widest text-foreground/40 animate-pulse uppercase">Memuat Riset...</p>
      </div>
    </div>
  );

  return (
    <main className="min-h-screen bg-background transition-colors duration-700 grainy-bg">
      <Navbar />

      {/* Hero Section - Refined Spacing */}
      <section className="relative min-h-[105vh] flex flex-col justify-center items-center pt-32 pb-40 overflow-hidden">
        <div className="container mx-auto px-6 relative z-20 text-center flex-1 flex flex-col justify-center">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1.2, ease: [0.16, 1, 0.3, 1] }}
            className="max-w-5xl mx-auto"
          >
            {/* Centered subtle badge */}
            <div className="flex justify-center mb-16">
              <motion.div 
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ delay: 0.5 }}
                className={cn(
                  "inline-flex items-center gap-3 px-6 py-2.5 rounded-full border text-[10px] font-black uppercase tracking-[0.3em] backdrop-blur-md",
                  theme === 'dark' 
                    ? "bg-[#FFB6C1] text-[#8B0000] border-none" 
                    : "bg-[#8B0000]/10 text-[#8B0000] border-[#8B0000]/20"
                )}
              >
                <ShieldCheck className="w-4 h-4" /> {t("hero.badge")}
              </motion.div>
            </div>

            <h1 className={cn(
              "text-5xl md:text-[100px] font-black tracking-tighter leading-[0.9] mb-16 font-serif transition-colors duration-500",
              theme === 'dark' ? "text-white" : "text-[#8B0000]"
            )}>
              {t("hero.title")}
            </h1>
            
            <p className={cn("text-xl md:text-2xl leading-relaxed mb-20 max-w-4xl mx-auto font-medium", theme === 'dark' ? "text-white" : "text-black")}>
              {t("hero.subtitle")}
            </p>
            
            <div className="flex flex-wrap justify-center gap-8">
              <Link
                href="/statistik"
                className={cn(
                  "px-12 py-6 font-black rounded-2xl flex items-center gap-3 hover:shadow-2xl transition-all hover:-translate-y-2 active:translate-y-0",
                  theme === 'dark' ? "bg-white text-[#8B0000]" : "bg-[#8B0000] text-white"
                )}
              >
                {t("hero.cta.stats")} <Scale className="w-5 h-5" />
              </Link>
              <Link
                href="/peta"
                className={cn(
                  "px-12 py-6 font-black rounded-2xl flex items-center gap-3 hover:opacity-90 transition-all hover:-translate-y-2 active:translate-y-0",
                  theme === 'dark' ? "bg-white text-[#8B0000]" : "bg-black text-white"
                )}
              >
                {t("hero.cta.map")} <MapIcon className="w-5 h-5" />
              </Link>
            </div>
          </motion.div>
        </div>

        {/* Scroll Indicator - Bottom positioned with enough space */}
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 2, duration: 1 }}
          className={cn(
            "mt-20 flex flex-col items-center gap-4 transition-colors duration-500",
            theme === 'dark' ? "text-white" : "text-[#8B0000]"
          )}
        >
          <span className="text-[10px] font-black tracking-[0.5em] uppercase">{t("hero.scroll")}</span>
          <div className={cn(
            "w-[2px] h-10 rounded-full bg-gradient-to-b from-current to-transparent"
          )} />
        </motion.div>
      </section>

      {/* Snapshot Section */}
      <section className="py-40">
        <div className="container mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10">
            {[
              { val: data.overview.total_laporan, label: t("stats.total_reports"), icon: AlertTriangle },
              { val: data.overview.total_kampus, label: t("stats.universities"), icon: Gavel },
              { val: data.overview.total_provinsi, label: t("stats.provinces"), icon: MapIcon },
              { val: `+${data.growth.growth_pct}%`, label: t("stats.growth"), icon: TrendingUp, highlight: true }
            ].map((stat, i) => (
              <motion.div 
                key={i}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                className={cn(
                  "p-8 md:p-10 rounded-[50px] transition-all duration-500 glass-card flex flex-col items-center text-center min-h-[350px] justify-center",
                  stat.highlight && "!bg-[#8B0000] text-white border-none shadow-[#8B0000]/20"
                )}
              >
                <div className={cn(
                  "w-14 h-14 rounded-2xl flex items-center justify-center mb-8",
                  stat.highlight ? "bg-white/20 text-white" : "bg-[#8B0000]/20 dark:bg-white/20 text-[#8B0000] dark:text-white"
                )}>
                  <stat.icon className="w-6 h-6" />
                </div>
                <div className={cn(
                  "text-3xl md:text-4xl lg:text-5xl font-black tracking-tighter mb-4 whitespace-nowrap",
                  stat.highlight ? "text-white" : (theme === 'dark' ? "text-white" : "text-black")
                )}>
                  {typeof stat.val === "number" ? formatNumber(stat.val) : stat.val}
                </div>
                <div className={cn(
                  "text-[9px] md:text-[10px] font-black uppercase tracking-[0.2em] leading-tight max-w-[150px]",
                  stat.highlight ? "text-white" : (theme === 'dark' ? "text-white/80" : "text-black/80")
                )}>
                  {stat.label}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Editorial Section */}
      <section className="py-60 border-y border-border/10">
        <div className="container mx-auto px-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-32 items-center">
            <motion.div
              initial={{ opacity: 0, x: -60 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
            >
              <div className="inline-flex items-center gap-6 text-primary font-black uppercase tracking-[0.4em] text-[10px] mb-12">
                <div className="w-16 h-[2px] bg-primary" /> ANALISIS YURIDIS
              </div>
              <h2 className="text-5xl md:text-7xl font-black tracking-tighter mb-12 leading-[1] font-serif text-primary">
                {t("story.trend.title")}
              </h2>
              <div className="text-xl leading-relaxed mb-10 text-foreground/80 font-medium italic border-l-4 border-primary pl-8">
                {t("story.trend.p1")}
              </div>
              <div className="text-lg leading-relaxed mb-12 text-foreground/40 font-medium">
                {t("story.trend.p2")}
              </div>
              <Link 
                href="/statistik"
                className="group inline-flex items-center gap-6 font-black text-foreground uppercase tracking-[0.3em] text-xs py-4 border-b-2 border-primary/20 hover:border-primary transition-all"
              >
                {t("story.trend.cta")} <ArrowRight className="w-6 h-6 group-hover:translate-x-4 transition-transform text-primary" />
              </Link>
            </motion.div>
            
            <motion.div 
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              className="h-[650px] glass-card p-16 rounded-[80px]"
            >
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={data.trend_tahunan}>
                  <defs>
                    <linearGradient id="colorJumlah" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#8B0000" stopOpacity={0.8}/>
                      <stop offset="95%" stopColor="#8B0000" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="5 5" stroke="var(--border)" vertical={false} />
                  <XAxis 
                    dataKey="tahun" 
                    stroke="var(--foreground)" 
                    fontSize={10} 
                    fontWeight={900}
                    axisLine={false}
                    tickLine={false}
                    dy={20}
                  />
                  <YAxis hide />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: "var(--background)", 
                      border: "1px solid var(--border)",
                      borderRadius: "30px",
                      padding: "20px",
                      color: "var(--foreground)"
                    }}
                  />
                  <Area 
                    name={language === 'id' ? 'Jumlah Laporan' : 'Total Reports'}
                    type="monotone" 
                    dataKey="jumlah" 
                    stroke="#8B0000" 
                    className="dark:stroke-white"
                    strokeWidth={5}
                    fillOpacity={0.3} 
                    fill="url(#colorJumlah)" 
                  />
                </AreaChart>
              </ResponsiveContainer>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-24 border-t border-border/10">
        <div className="container mx-auto px-6 text-center">
          <div className="text-4xl font-black tracking-tighter text-primary mb-12">
            SIGAP<span className="text-foreground">.</span>
          </div>
          <div className="flex justify-center gap-12 text-xs font-black uppercase tracking-[0.3em] mb-16">
            <Link href="/statistik" className="hover:text-primary transition-colors">Yuridiksi</Link>
            <Link href="/peta" className="hover:text-primary transition-colors">Teritori</Link>
            <Link href="/upload" className="hover:text-primary transition-colors">Advokasi</Link>
          </div>
          <p className="text-[10px] font-black text-foreground/20 uppercase tracking-[0.5em]">
            © 2026 SIGAP PROJECT • INVESTIGATIVE DATA DOCTRINE
          </p>
        </div>
      </footer>
    </main>
  );
}
