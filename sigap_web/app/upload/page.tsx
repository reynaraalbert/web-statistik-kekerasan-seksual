"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import Navbar from "@/components/navbar";
import { useLanguage } from "@/components/language-provider";
import { motion } from "framer-motion";
import { useTheme } from "next-themes";
import { cn } from "@/lib/utils";
import { Info, ExternalLink, Loader2, UploadCloud, Database, ArrowRight, ShieldCheck } from "lucide-react";

export default function Upload() {
  const { language, t } = useLanguage();
  const { theme } = useTheme();
  const [loading, setLoading] = useState(true);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  const streamlitUrl = `http://localhost:8501/?embedded=true&theme=${theme === 'dark' ? 'dark' : 'light'}&lang=${language}`;

  return (
    <main className="min-h-screen pb-20 bg-background grainy-bg">
      {/* Minimal Header */}
      <div className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-xl border-b border-border py-4">
        <div className="container mx-auto px-6 flex justify-between items-center">
          <Link href="/" className="flex items-center gap-3 group">
            <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center text-white">
               <ShieldCheck className="w-5 h-5" />
            </div>
            <span className="text-lg font-black tracking-tighter text-primary">SIGAP</span>
          </Link>
          <Link href="/" className="flex items-center gap-2 px-5 py-2 bg-secondary hover:bg-primary hover:text-white rounded-xl text-[10px] font-black uppercase tracking-widest transition-all">
            <ArrowRight className="w-4 h-4 rotate-180" /> {t("upload.back")}
          </Link>
        </div>
      </div>

      <div className="container mx-auto px-6 pt-32">
        <div className="max-w-5xl mx-auto mb-10 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <h1 className={cn("text-3xl md:text-5xl font-black tracking-tighter mb-4 font-serif leading-tight", theme === 'dark' ? "text-white" : "text-[#8B0000]")}>{t("upload.title")}</h1>
            <p className={cn("text-sm md:text-base max-w-xl mx-auto font-medium opacity-60", theme === 'dark' ? "text-white" : "text-black")}>
              {t("upload.subtitle")}
            </p>
          </motion.div>
        </div>

        {/* Streamlit Iframe Container */}
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, scale: 0.98 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
            className="relative glass-card rounded-[40px] md:rounded-[60px] overflow-hidden border border-border shadow-4xl h-[900px] bg-background"
          >
            {loading && (
              <div className="absolute inset-0 flex flex-col items-center justify-center bg-background z-10 gap-6">
                <Loader2 className="w-12 h-12 animate-spin text-primary" />
                <p className="text-sm font-black tracking-widest text-black dark:text-white uppercase">Initializing Engine...</p>
              </div>
            )}
            
            <iframe
              src={streamlitUrl}
              className="w-full h-full border-none"
              onLoad={() => setLoading(false)}
              title="Streamlit Analysis Engine"
            />
          </motion.div>
        </div>
      </div>
    </main>
  );
}
