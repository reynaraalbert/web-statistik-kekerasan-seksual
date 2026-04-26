"use client";

import React, { useEffect, useState } from "react";
import Navbar from "@/components/navbar";
import { useLanguage } from "@/components/language-provider";
import { useTheme } from "next-themes";
import { cn, formatNumber } from "@/lib/utils";
import { motion, AnimatePresence } from "framer-motion";
import { Play, Newspaper, ExternalLink, MessageSquare, ThumbsUp, Eye, Search } from "lucide-react";

export default function Media() {
  const { t } = useLanguage();
  const { theme } = useTheme();
  const [data, setData] = useState<any>(null);
  const [activeTab, setActiveTab] = useState("yt");
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    fetch("/data/sigap.json")
      .then(res => res.json())
      .then(d => setData(d));
  }, []);

  if (!data) return null;

  const filteredYT = data.youtube_top.filter((v: any) => 
    v.judul.toLowerCase().includes(searchTerm.toLowerCase()) || 
    v.channel.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const filteredNews = data.berita_terbaru.filter((n: any) => 
    n.judul.toLowerCase().includes(searchTerm.toLowerCase()) || 
    n.sumber.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <main className="min-h-screen pt-32 pb-20 bg-background">
      <Navbar />

      <div className="container mx-auto px-6">
        <div className="max-w-5xl mx-auto mb-16 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <h1 className="text-5xl md:text-7xl font-black tracking-tighter mb-6 font-serif">{t("media.title")}</h1>
            <p className="text-xl text-foreground/40 max-w-2xl mx-auto font-medium leading-relaxed">
              {t("media.subtitle")}
            </p>
          </motion.div>
        </div>

        {/* Tab Selection & Search */}
        <div className="max-w-6xl mx-auto mb-12 flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex p-1.5 bg-secondary rounded-2xl border border-border w-full md:w-auto">
            <button
              onClick={() => setActiveTab("yt")}
              className={cn(
                "flex-1 md:flex-none px-8 py-3 rounded-xl font-bold text-sm flex items-center justify-center gap-2 transition-all",
                activeTab === "yt" 
                  ? (theme === 'dark' ? "bg-primary text-[#8B0000] shadow-lg" : "bg-primary text-white shadow-lg") 
                  : "text-foreground/60 hover:text-foreground"
              )}
            >
              <Play className="w-4 h-4" /> {t("media.tab.yt")}
            </button>
            <button
              onClick={() => setActiveTab("news")}
              className={cn(
                "flex-1 md:flex-none px-8 py-3 rounded-xl font-bold text-sm flex items-center justify-center gap-2 transition-all",
                activeTab === "news" 
                  ? (theme === 'dark' ? "bg-primary text-[#8B0000] shadow-lg" : "bg-primary text-white shadow-lg") 
                  : "text-foreground/60 hover:text-foreground"
              )}
            >
              <Newspaper className="w-4 h-4" /> {t("media.tab.news")}
            </button>
          </div>

          <div className="relative w-full md:w-96">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-foreground/30" />
            <input
              type="text"
              placeholder="Cari kata kunci..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-12 pr-4 py-4 bg-secondary/50 border border-border rounded-2xl focus:outline-none focus:ring-2 focus:ring-primary/50 font-medium"
            />
          </div>
        </div>

        {/* Content Area */}
        <AnimatePresence mode="wait">
          {activeTab === "yt" ? (
            <motion.div
              key="yt-grid"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto"
            >
              {filteredYT.map((video: any, idx: number) => (
                <div key={idx} className="glass-card rounded-[32px] overflow-hidden group hover:shadow-2xl transition-all hover:-translate-y-1">
                  <div className="relative aspect-video bg-black flex items-center justify-center overflow-hidden">
                    <img 
                      src={`https://img.youtube.com/vi/${video.video_id}/maxresdefault.jpg`} 
                      alt={video.judul}
                      className="w-full h-full object-cover opacity-60 group-hover:scale-105 transition-transform duration-500"
                    />
                    <div className="absolute inset-0 flex items-center justify-center">
                       <a 
                         href={video.url} 
                         target="_blank"
                         className="w-16 h-16 bg-white/20 backdrop-blur-md rounded-full flex items-center justify-center text-white border border-white/20 group-hover:scale-110 group-hover:bg-primary group-hover:border-transparent transition-all"
                       >
                         <Play fill="white" className="w-6 h-6 translate-x-0.5" />
                       </a>
                    </div>
                  </div>
                  <div className="p-8">
                    <div className="flex items-center gap-2 mb-4">
                      <span className="px-3 py-1 bg-primary/10 text-primary text-[10px] font-black uppercase tracking-widest rounded-lg">
                        {video.keyword}
                      </span>
                      <span className="text-[10px] font-bold text-foreground/40">{video.tanggal}</span>
                    </div>
                    <h3 className="text-xl font-bold tracking-tight mb-4 leading-snug line-clamp-2 h-14 group-hover:text-primary transition-colors">
                      {video.judul}
                    </h3>
                    <div className="text-sm font-bold text-foreground/40 mb-6 flex items-center gap-2">
                      <div className="w-6 h-6 rounded-full bg-secondary flex items-center justify-center text-[10px]">YT</div>
                      {video.channel}
                    </div>
                    <div className="flex items-center justify-between pt-6 border-t border-border">
                      <div className="flex gap-4">
                        <div className="flex flex-col items-center gap-0.5">
                          <Eye className="w-4 h-4 text-foreground/30" />
                          <span className="text-[10px] font-black">{formatNumber(video.views)}</span>
                        </div>
                        <div className="flex flex-col items-center gap-0.5">
                          <ThumbsUp className="w-4 h-4 text-foreground/30" />
                          <span className="text-[10px] font-black">{formatNumber(video.likes)}</span>
                        </div>
                        <div className="flex flex-col items-center gap-0.5">
                          <MessageSquare className="w-4 h-4 text-foreground/30" />
                          <span className="text-[10px] font-black">{formatNumber(video.komentar)}</span>
                        </div>
                      </div>
                      <a href={video.url} target="_blank" className="p-3 bg-secondary hover:bg-primary hover:text-white rounded-xl transition-all">
                        <ExternalLink className="w-4 h-4" />
                      </a>
                    </div>
                  </div>
                </div>
              ))}
            </motion.div>
          ) : (
            <motion.div
              key="news-list"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="max-w-4xl mx-auto space-y-6"
            >
              {filteredNews.map((news: any, idx: number) => (
                <div key={idx} className="glass-card p-8 rounded-[32px] group hover:border-primary/50 transition-all">
                  <div className="flex flex-col md:flex-row justify-between gap-6">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-4">
                        <span className="px-3 py-1 bg-accent/10 text-accent text-[10px] font-black uppercase tracking-widest rounded-lg">
                          {news.sumber}
                        </span>
                        <span className="text-[10px] font-bold text-foreground/40 uppercase tracking-widest">{news.tanggal}</span>
                      </div>
                      <h3 className="text-2xl font-bold tracking-tighter mb-4 font-serif group-hover:text-primary transition-colors">
                        {news.judul}
                      </h3>
                      <div className="flex items-center gap-2">
                        <div className="px-3 py-1 bg-secondary text-[10px] font-bold rounded-lg text-foreground/60">{news.keyword}</div>
                      </div>
                    </div>
                    <div className="flex md:flex-col justify-end items-center gap-4">
                      <a 
                        href={news.url} 
                        target="_blank"
                        className={cn(
                          "flex items-center gap-2 px-6 py-3 bg-primary font-black rounded-xl hover:shadow-lg transition-all",
                          theme === 'dark' ? "text-[#8B0000]" : "text-white"
                        )}
                      >
                        Baca Artikel <ExternalLink className="w-4 h-4" />
                      </a>
                    </div>
                  </div>
                </div>
              ))}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </main>
  );
}
