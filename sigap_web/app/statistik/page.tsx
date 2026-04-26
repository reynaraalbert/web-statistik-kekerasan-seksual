"use client";

import React, { useEffect, useState } from "react";
import Navbar from "@/components/navbar";
import { useLanguage } from "@/components/language-provider";
import { cn, formatNumber } from "@/lib/utils";
import { motion } from "framer-motion";
import { useTheme } from "next-themes";
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, 
  PieChart, Pie, Cell, Legend, ComposedChart, Area, Scatter, LabelList
} from "recharts";
import { ArrowRight, TrendingUp, Users, MapPin, Building2, Calendar, Scale, Gavel } from "lucide-react";
import Link from "next/link";

export default function Statistik() {
  const { t, language } = useLanguage();
  const { resolvedTheme: theme } = useTheme();
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    fetch("/data/sigap.json")
      .then(res => res.json())
      .then(d => setData(d));
  }, []);

  if (!data) return null;

  const labelMap: Record<string, Record<string, string>> = {
    en: {
      "Dosen": "Lecturers",
      "Mahasiswa": "Students",
      "Pengurus BEM/Organisasi": "Student Leaders",
      "Rektor/Pimpinan": "University Leaders",
      "Alumni": "Alumni",
      "Senior/Kakak Tingkat": "Seniors",
      "Tenaga Kependidikan": "Educational Staff",
      "Panitia Kegiatan": "Event Committee",
      "Dosen Pembimbing": "Academic Advisor",
      "Pelecehan Fisik": "Physical Violence",
      "Pelecehan Verbal": "Verbal Harassment",
      "Kekerasan Seksual Berbasis Elektronik (KSBE)": "Digital Violence",
      "Pemerkosaan": "Rape",
      "Eksploitasi Seksual": "Exploitation",
      "Pelecehan Seksual": "Sexual Harassment",
      "Pemaksaan Seksual": "Sexual Coercion",
      "Kekerasan Seksual (Umum)": "Sexual Violence (General)",
      "KBGO": "OGBV",
      "Verbal Harassment": "Verbal Harassment",
      // University Names
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
    }
  };

  const tl = (label: string) => {
    if (language === 'id') return label;
    return labelMap.en[label] || label;
  };

  const translatedTypes = data.jenis_kekerasan.map((item: any) => ({
    ...item,
    label: tl(item.label)
  }));

  const translatedPerps = data.pelaku.map((item: any) => ({
    ...item,
    label: tl(item.label)
  }));

  const COLORS = ['#8B0000', '#000000', '#666666', '#4a0000', '#CCCCCC', '#333333'];

  // Helper for percentage
  const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, index }: any) => {
    const RADIAN = Math.PI / 180;
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
      <text x={x} y={y} fill="white" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central" fontSize={10} fontWeight={900}>
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    );
  };

  return (
    <main className="min-h-screen bg-background transition-colors duration-700 grainy-bg">
      <Navbar />

      <section className="container mx-auto px-6 max-w-7xl pt-32 pb-20">
        {/* Header - Reduced padding */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-20 text-center"
        >
          <div className={cn(
            "inline-flex items-center gap-4 font-black uppercase tracking-[0.4em] text-[10px] mb-8 transition-colors duration-500",
            theme === 'dark' ? "text-white" : "text-[#8B0000]"
          )}>
            <Scale className="w-4 h-4" /> {t("stats.badge.dissertation")}
          </div>
          <h1 className={cn(
            "text-4xl md:text-[80px] font-black tracking-tighter mb-8 font-serif leading-[0.9] transition-colors duration-500",
            theme === 'dark' ? "text-white" : "text-[#8B0000]"
          )}>
            {t("stats.title")}
          </h1>
          <p className={cn("text-lg md:text-2xl max-w-4xl mx-auto font-medium leading-relaxed", theme === 'dark' ? "text-white" : "text-black")}>
            {t("stats.subtitle")}
          </p>
        </motion.div>

        {/* 1. Spectrum Section */}
        <div className="mb-40">
          <div className="flex flex-col lg:grid lg:grid-cols-2 gap-10 lg:gap-20 items-center">
            {/* Title - Order 1 */}
            <motion.div
              initial={{ opacity: 0, x: -40 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="w-full order-1"
            >
              <div className={cn(
                "inline-flex items-center gap-4 font-black uppercase tracking-[0.3em] text-[8px] md:text-[10px] mb-4 md:mb-6 transition-colors duration-500",
                theme === 'dark' ? "text-white" : "text-[#8B0000]"
              )}>
                <div className={cn("w-12 h-[2px]", theme === 'dark' ? "bg-white" : "bg-[#8B0000]")} /> {t("stats.badge.typology")}
              </div>
              <h2 className={cn(
                "text-2xl md:text-5xl font-black tracking-tighter mb-4 md:mb-8 leading-tight font-serif transition-colors duration-500",
                theme === 'dark' ? "text-white" : "text-[#8B0000]"
              )}>
                {t("story.spectrum.title")}
              </h2>
            </motion.div>

            {/* Visual - Order 2, Side by side on Desktop */}
            <motion.div 
              initial={{ opacity: 0, scale: 0.95 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              className="h-[350px] md:h-[500px] w-full glass-card p-6 md:p-10 rounded-[40px] md:rounded-[60px] relative overflow-hidden order-2 lg:row-span-2"
            >
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={translatedTypes}
                    cx="50%"
                    cy="45%"
                    innerRadius="40%"
                    outerRadius="70%"
                    paddingAngle={5}
                    dataKey="value"
                    nameKey="label"
                    labelLine={false}
                    label={renderCustomizedLabel}
                  >
                    {data.jenis_kekerasan.map((entry: any, index: number) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip 
                    formatter={(value, name, props) => {
                      const total = data.jenis_kekerasan.reduce((acc: number, curr: any) => acc + curr.value, 0);
                      const percent = ((value as number / total) * 100).toFixed(1);
                      return [`${value} Kasus (${percent}%)`, language === 'id' ? 'Jumlah' : 'Total'];
                    }}
                    contentStyle={{ 
                      borderRadius: "20px", 
                      background: theme === 'dark' ? "#1a1a1a" : "var(--background)", 
                      border: "1px solid var(--border)",
                      boxShadow: "0 10px 30px rgba(0,0,0,0.5)"
                    }} 
                    itemStyle={{ color: theme === 'dark' ? "#FFFFFF" : "#8B0000", fontWeight: 900 }}
                    labelStyle={{ color: theme === 'dark' ? "#FFFFFF" : "#000000", fontWeight: 900, marginBottom: "4px" }}
                  />
                  <Legend verticalAlign="bottom" height={36} iconType="circle" wrapperStyle={{ fontSize: '10px', fontWeight: 'bold' }} />
                </PieChart>
              </ResponsiveContainer>
            </motion.div>

            {/* Description - Order 3 */}
            <motion.div
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true }}
              className="w-full order-3"
            >
              <div className="space-y-6">
                <p className={cn(
                  "news-article-p border-l-4 italic font-bold text-sm md:text-lg pl-6",
                  theme === 'dark' ? "border-white text-white" : "border-[#8B0000] text-[#8B0000]"
                )}>
                  {t("story.spectrum.p1")}
                </p>
                <p className="news-article-p text-black/80 dark:text-white/90 text-sm md:text-lg">
                  {t("story.spectrum.p2")}
                </p>
              </div>
            </motion.div>
          </div>
        </div>

        {/* 2. Perpetrator Section */}
        <div className="mb-40">
          <div className="flex flex-col lg:grid lg:grid-cols-2 gap-10 lg:gap-20 items-center">
            {/* Title - Order 1 */}
            <motion.div
              initial={{ opacity: 0, x: 40 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="w-full order-1 lg:col-start-2"
            >
              <div className={cn(
                "inline-flex items-center gap-4 font-black uppercase tracking-[0.3em] text-[8px] md:text-[10px] mb-4 md:mb-6 transition-colors duration-500",
                theme === 'dark' ? "text-white" : "text-[#8B0000]"
              )}>
                <div className={cn("w-12 h-[2px]", theme === 'dark' ? "bg-white" : "bg-[#8B0000]")} /> {t("stats.badge.power")}
              </div>
              <h2 className={cn(
                "text-2xl md:text-5xl font-black tracking-tighter mb-4 md:mb-8 leading-tight font-serif transition-colors duration-500",
                theme === 'dark' ? "text-white" : "text-[#8B0000]"
              )}>
                {t("story.perpetrator.title")}
              </h2>
            </motion.div>

            {/* Visual - Order 2, Column 1 on Desktop */}
            <motion.div 
              initial={{ opacity: 0, scale: 0.95 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              className="h-[350px] md:h-[500px] w-full glass-card p-4 md:p-10 rounded-[40px] md:rounded-[60px] order-2 lg:row-span-2 lg:col-start-1 lg:row-start-1"
            >
               <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={translatedPerps}
                  layout="vertical"
                  margin={{ top: 20, right: 30, left: 40, bottom: 20 }}
                >
                  <CartesianGrid strokeDasharray="5 5" horizontal={false} stroke="var(--border)" />
                  <XAxis type="number" hide />
                  <YAxis 
                    dataKey="label" 
                    type="category" 
                    width={180} 
                    fontSize={8} 
                    fontWeight={900}
                    stroke="currentColor"
                    tick={{ textAnchor: 'start', dx: -170 }}
                    className="uppercase tracking-widest text-black dark:text-white"
                  />
                  <Tooltip 
                    cursor={{fill: 'rgba(255,255,255,0.1)'}} 
                    formatter={(value) => {
                      const total = data.pelaku.reduce((acc: number, curr: any) => acc + curr.value, 0);
                      const percent = ((value as number / total) * 100).toFixed(1);
                      return [`${value} Laporan (${percent}%)`, language === 'id' ? 'Jumlah' : 'Total'];
                    }}
                    contentStyle={{ 
                      borderRadius: "20px", 
                      background: theme === 'dark' ? "#1a1a1a" : "var(--background)", 
                      border: "1px solid var(--border)",
                      boxShadow: "0 10px 30px rgba(0,0,0,0.5)"
                    }} 
                    itemStyle={{ color: theme === 'dark' ? "#FFFFFF" : "#8B0000", fontWeight: 900 }}
                    labelStyle={{ color: theme === 'dark' ? "#FFFFFF" : "#000000", fontWeight: 900, marginBottom: "4px" }}
                  />
                  <Bar 
                    dataKey="value" 
                    fill="#8B0000" 
                    className="dark:!fill-white"
                    radius={[0, 10, 10, 0]} 
                    barSize={20} 
                  >
                    <LabelList dataKey="value" position="right" fontSize={9} fontWeight={900} fill="currentColor" />
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </motion.div>

            {/* Description - Order 3 */}
            <motion.div
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true }}
              className="w-full order-3 lg:col-start-2"
            >
              <div className="space-y-6">
                <p className={cn(
                  "news-article-p border-l-4 italic font-bold text-sm md:text-lg pl-6",
                  theme === 'dark' ? "border-white text-white" : "border-black text-black"
                )}>
                  {t("story.perpetrator.p1")}
                </p>
                <p className="news-article-p text-black/80 dark:text-white/90 text-sm md:text-lg">
                  {t("story.perpetrator.p2")}
                </p>
              </div>
            </motion.div>
          </div>
        </div>

        {/* 3. Geography & Temporal */}
        <div className="space-y-40">
          <div className="flex flex-col lg:grid lg:grid-cols-2 gap-10 lg:gap-20 items-center">
            {/* Title - Order 1 */}
            <motion.div
              initial={{ opacity: 0, x: -40 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="w-full order-1"
            >
               <div className={cn(
                 "inline-flex items-center gap-4 font-black uppercase tracking-[0.3em] text-[8px] md:text-[10px] mb-4 md:mb-6 transition-colors duration-500",
                 theme === 'dark' ? "text-white" : "text-[#8B0000]"
               )}>
                <div className={cn("w-12 h-[2px]", theme === 'dark' ? "bg-white" : "bg-[#8B0000]")} /> {t("stats.badge.geography")}
              </div>
              <h2 className={cn(
                "text-2xl md:text-5xl font-black tracking-tighter mb-4 md:mb-8 leading-tight font-serif transition-colors duration-500",
                theme === 'dark' ? "text-white" : "text-[#8B0000]"
              )}>
                {t("story.geography.title")}
              </h2>
            </motion.div>

            {/* Visual - Order 2, Side by side */}
            <motion.div className="h-[300px] md:h-[400px] w-full glass-card p-4 md:p-10 rounded-[40px] md:rounded-[60px] order-2 lg:row-span-2">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data.kota_stats} margin={{ top: 20, right: 20, left: 0, bottom: 80 }}>
                  <CartesianGrid strokeDasharray="5 5" vertical={false} stroke="var(--border)" />
                  <XAxis 
                    dataKey="label" 
                    fontSize={7} 
                    fontWeight={900} 
                    stroke="currentColor"
                    interval={0}
                    angle={-45}
                    textAnchor="end"
                    height={100}
                    className="uppercase tracking-widest text-black dark:text-white"
                  />
                  <YAxis hide />
                  <Tooltip 
                    cursor={{fill: 'rgba(255,255,255,0.1)'}} 
                    formatter={(value) => {
                      const total = data.kota_stats.reduce((acc: number, curr: any) => acc + curr.value, 0);
                      const percent = ((value as number / total) * 100).toFixed(1);
                      return [`${value} ${t("stats.unit.cases")} (${percent}%)`, t("stats.unit.total")];
                    }}
                    contentStyle={{ 
                      borderRadius: "20px", 
                      background: theme === 'dark' ? "#1a1a1a" : "var(--background)", 
                      border: "1px solid var(--border)",
                      boxShadow: "0 10px 30px rgba(0,0,0,0.5)"
                    }} 
                    itemStyle={{ color: theme === 'dark' ? "#FFFFFF" : "#8B0000", fontWeight: 900 }}
                    labelStyle={{ color: theme === 'dark' ? "#FFFFFF" : "#000000", fontWeight: 900, marginBottom: "4px" }}
                  />
                  <Bar 
                    dataKey="value" 
                    name={t("stats.unit.total")} 
                    fill="#8B0000" 
                    className="dark:!fill-white"
                    radius={[10, 10, 0, 0]} 
                  >
                    <LabelList dataKey="value" position="top" fontSize={9} fontWeight={900} fill="currentColor" />
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </motion.div>

            {/* Description - Order 3 */}
            <motion.div
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true }}
              className="w-full order-3"
            >
              <div className="space-y-6">
                <p className={cn(
                  "news-article-p border-l-4 italic font-bold text-sm md:text-lg pl-6",
                  theme === 'dark' ? "border-white text-white" : "border-[#8B0000] text-[#8B0000]"
                )}>
                  {t("story.geography.p1")}
                </p>
                <p className="news-article-p text-black/80 dark:text-white/90 text-sm md:text-lg">
                  {t("story.geography.p2")}
                </p>
              </div>
            </motion.div>
          </div>

          <div className="text-center max-w-4xl mx-auto flex flex-col gap-6">
              {/* 4. Annual Escalation Section (New) */}
              <div className="w-full mt-40">
                <div className={cn(
                  "inline-flex items-center gap-4 font-black uppercase tracking-[0.4em] text-[8px] md:text-[10px] mb-4 md:mb-6 transition-colors duration-500",
                  theme === 'dark' ? "text-white" : "text-[#8B0000]"
                )}>
                  <TrendingUp className="w-4 h-4" /> {t("stats.badge.escalation")}
                </div>
                <h2 className={cn(
                  "text-2xl md:text-6xl font-black tracking-tighter mb-4 md:mb-8 leading-[1.1] md:leading-[0.9] font-serif transition-colors duration-500",
                  theme === 'dark' ? "text-white" : "text-[#8B0000]"
                )}>
                  {t("story.escalation.title")}
                </h2>
                
                <motion.div 
                  initial={{ opacity: 0, y: 40 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  className="h-[350px] md:h-[550px] w-full glass-card p-4 md:p-10 rounded-[40px] md:rounded-[60px] mb-12"
                >
                  <ResponsiveContainer width="100%" height="100%">
                    <ComposedChart data={data.trend_tahunan} margin={{ top: 20, right: 30, left: 0, bottom: 20 }}>
                      <defs>
                        <linearGradient id="colorTrend" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#8B0000" stopOpacity={0.8}/>
                          <stop offset="95%" stopColor="#8B0000" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="5 5" vertical={false} stroke="var(--border)" />
                      <XAxis 
                        dataKey="tahun" 
                        fontSize={10} 
                        fontWeight={900} 
                        stroke="currentColor"
                        className="tracking-widest text-black dark:text-white"
                      />
                      <YAxis 
                        fontSize={10} 
                        fontWeight={900} 
                        stroke="currentColor"
                        className="text-black dark:text-white"
                      />
                      <Tooltip 
                        contentStyle={{ 
                          borderRadius: "20px", 
                          background: theme === 'dark' ? "#1a1a1a" : "var(--background)", 
                          border: "1px solid var(--border)",
                          boxShadow: "0 10px 30px rgba(0,0,0,0.5)"
                        }} 
                        itemStyle={{ color: theme === 'dark' ? "#FFFFFF" : "#8B0000", fontWeight: 900 }}
                        labelStyle={{ color: theme === 'dark' ? "#FFFFFF" : "#000000", fontWeight: 900, marginBottom: "4px" }}
                        formatter={(value) => [`${value} ${t("stats.unit.reports")}`, t("stats.unit.escalation")]}
                      />
                      <Area 
                        type="monotone" 
                        dataKey="jumlah" 
                        stroke="#8B0000" 
                        strokeWidth={6}
                        fillOpacity={1} 
                        fill="url(#colorTrend)" 
                        animationDuration={2500}
                      />
                      <Scatter dataKey="jumlah" fill="#8B0000" />
                    </ComposedChart>
                  </ResponsiveContainer>
                </motion.div>

                <div className="grid md:grid-cols-2 gap-10 text-left max-w-6xl mx-auto">
                  <div className={cn(
                    "news-article-p border-l-4 italic font-bold text-sm md:text-lg pl-6",
                    theme === 'dark' ? "border-white text-white" : "border-[#8B0000] text-[#8B0000]"
                  )}>
                    {t("story.escalation.p1")}
                  </div>
                  <div className="news-article-p text-black/80 dark:text-white/90 text-sm md:text-lg">
                    {t("story.escalation.p2")}
                  </div>
                </div>
              </div>

              <div className="w-full mt-40">
                <div className={cn(
                  "inline-flex items-center gap-4 font-black uppercase tracking-[0.4em] text-[8px] md:text-[10px] mb-4 md:mb-6 transition-colors duration-500",
                  theme === 'dark' ? "text-white" : "text-[#8B0000]"
                )}>
                  <Calendar className="w-4 h-4" /> {t("stats.badge.temporal")}
                </div>
                <h2 className={cn(
                  "text-2xl md:text-6xl font-black tracking-tighter mb-4 md:mb-8 leading-[1.1] md:leading-[0.9] font-serif transition-colors duration-500",
                  theme === 'dark' ? "text-white" : "text-[#8B0000]"
                )}>
                  {t("story.temporal.title")}
                </h2>
                
                <motion.div 
                  initial={{ opacity: 0, y: 40 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  className="h-[300px] md:h-[450px] w-full glass-card p-4 md:p-10 rounded-[40px] md:rounded-[60px] mb-12"
                >
                  <ResponsiveContainer width="100%" height="100%">
                    <ComposedChart data={data.heatmap_bulanan.slice(-12)} margin={{ bottom: 20 }}>
                      <defs>
                        <linearGradient id="colorJumlah" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#8B0000" stopOpacity={0.8}/>
                          <stop offset="95%" stopColor="#8B0000" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="5 5" vertical={false} stroke="var(--border)" />
                      <XAxis 
                        dataKey="bulan_id" 
                        fontSize={8} 
                        fontWeight={900} 
                        stroke="currentColor"
                        className="uppercase tracking-widest text-black dark:text-white"
                        dy={10}
                      />
                      <YAxis hide />
                      <Tooltip 
                        contentStyle={{ 
                          borderRadius: "20px", 
                          background: theme === 'dark' ? "#1a1a1a" : "var(--background)", 
                          border: "1px solid var(--border)",
                          boxShadow: "0 10px 30px rgba(0,0,0,0.5)"
                        }} 
                        itemStyle={{ color: theme === 'dark' ? "#FFFFFF" : "#8B0000", fontWeight: 900 }}
                        labelStyle={{ color: theme === 'dark' ? "#FFFFFF" : "#000000", fontWeight: 900, marginBottom: "4px" }}
                        formatter={(value) => [`${value} ${t("stats.unit.reports")}`, t("stats.unit.total")]}
                      />
                      <Area 
                        name={language === 'id' ? 'Jumlah Laporan' : 'Total Reports'}
                        type="monotone" 
                        dataKey="jumlah" 
                        stroke="#8B0000" 
                        className="dark:!stroke-white dark:!fill-white/20"
                        strokeWidth={4}
                        fillOpacity={0.3} 
                        fill="url(#colorJumlah)" 
                      />
                    </ComposedChart>
                  </ResponsiveContainer>
                </motion.div>

                <div className="grid md:grid-cols-2 gap-10 text-left max-w-6xl mx-auto">
                  <div className={cn(
                    "news-article-p border-l-4 italic font-bold text-sm md:text-lg pl-6",
                    theme === 'dark' ? "border-white text-white" : "border-[#8B0000] text-[#8B0000]"
                  )}>
                    {t("story.temporal.p1")}
                  </div>
                  <div className="news-article-p text-black/80 dark:text-white/90 text-sm md:text-lg">
                    {t("story.temporal.p2")}
                  </div>
                </div>
              </div>
        </div>
        </div>

        {/* CTA */}
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          className={cn(
            "p-12 md:p-24 rounded-[60px] text-center relative overflow-hidden transition-colors duration-700",
            theme === 'dark' ? "bg-white" : "bg-[#8B0000]"
          )}
        >
          <div className="relative z-10">
            <div className={cn(
              "text-4xl md:text-8xl font-black tracking-tighter mb-8 uppercase font-serif",
              theme === 'dark' ? "text-[#8B0000]" : "text-white"
            )}>
              {t("stats.cta.title")}
            </div>
            <p className={cn(
              "text-xl md:text-3xl font-black tracking-tight mb-12 max-w-3xl mx-auto leading-tight",
              theme === 'dark' ? "text-[#8B0000]" : "text-white"
            )}>
              {t("stats.cta.subtitle")}
            </p>
          <Link
            href="/peta"
            className={cn(
              "inline-flex items-center gap-6 px-12 py-6 font-black rounded-[25px] hover:scale-105 active:scale-95 transition-all relative z-10 shadow-xl",
              theme === 'dark' ? "bg-[#8B0000] text-white" : "bg-white text-[#8B0000]"
            )}
          >
            {t("stats.cta.button")} <ArrowRight className="w-8 h-8" />
          </Link>
          </div>
        </motion.div>
      </section>
    </main>
  );
}
