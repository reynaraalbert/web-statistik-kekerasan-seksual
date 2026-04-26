"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { useLanguage } from "@/components/language-provider";
import { useTheme } from "next-themes";
import { 
  Sun, Moon, Languages, Menu, X, ArrowRight, ShieldCheck, 
  BarChart2, Map as MapIcon, PlayCircle, UploadCloud 
} from "lucide-react";
import { cn } from "@/lib/utils";

const Navbar = () => {
  const pathname = usePathname();
  const { language, setLanguage, t } = useLanguage();
  const { resolvedTheme: theme, setTheme } = useTheme();
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const handleScroll = () => setIsScrolled(window.scrollY > 20);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  if (!mounted) return null;

  const navLinks = [
    { href: "/", label: t("nav.home"), icon: ShieldCheck },
    { href: "/statistik", label: t("nav.stats"), icon: BarChart2 },
    { href: "/peta", label: t("nav.map"), icon: MapIcon },
    { href: "/media", label: t("nav.media"), icon: PlayCircle },
    { href: "/upload", label: t("nav.upload"), icon: UploadCloud },
  ];

  const toggleLanguage = () => setLanguage(language === "id" ? "en" : "id");
  const toggleTheme = () => setTheme(theme === "dark" ? "light" : "dark");

  return (
    <>
      <nav
        className={cn(
          "fixed top-0 left-0 right-0 z-[100] transition-all duration-700",
          isScrolled 
            ? "bg-background/90 backdrop-blur-2xl border-b border-foreground/5 py-3 shadow-lg" 
            : "bg-transparent py-8"
        )}
      >
        <div className="container mx-auto px-6 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-3 group">
            <div className="w-10 h-10 bg-[#8B0000] dark:bg-white rounded-xl flex items-center justify-center text-white dark:text-[#8B0000] shadow-xl group-hover:scale-110 transition-transform">
               <ShieldCheck className="w-6 h-6" />
            </div>
            <div className="flex flex-col">
              <span className={cn("text-xl font-black tracking-tighter leading-none", theme === 'dark' ? "text-white" : "text-[#8B0000]")}>SIGAP</span>
              <span className={cn("text-[8px] font-black uppercase tracking-[0.3em]", theme === 'dark' ? "text-white" : "text-black")}>Data Storytelling</span>
            </div>
          </Link>

          {/* Desktop Nav */}
          <div className="hidden lg:flex items-center gap-2">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={cn(
                  "px-6 py-2.5 rounded-xl text-xs font-black uppercase tracking-widest transition-all",
                  pathname === link.href 
                    ? (theme === 'dark' ? "bg-white/10 text-white" : "bg-[#8B0000]/10 text-[#8B0000]")
                    : (theme === 'dark' ? "text-white/80 hover:text-white" : "text-black/80 hover:text-black")
                )}
              >
                {link.label}
              </Link>
            ))}
          </div>

          <div className="flex items-center gap-2 md:gap-3">
             <div className="flex items-center p-1 bg-secondary rounded-xl border border-border">
                <button
                  onClick={toggleLanguage}
                  className="p-1.5 md:p-2 hover:bg-background rounded-lg transition-all !text-black dark:!text-white flex items-center gap-2"
                >
                  <Languages className="w-4 h-4" />
                  <span className="text-[9px] md:text-[10px] font-black uppercase">{language}</span>
                </button>
                <div className="w-px h-4 bg-border mx-0.5 md:mx-1" />
                <button
                  onClick={toggleTheme}
                  className="p-1.5 md:p-2 hover:bg-background rounded-lg transition-all !text-black dark:!text-white"
                >
                  {theme === "dark" ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
                </button>
             </div>

             <Link
               href="/upload"
               className="hidden sm:flex items-center gap-2 px-6 py-3 bg-primary text-background text-[10px] font-black uppercase tracking-widest rounded-xl hover:shadow-xl hover:-translate-y-0.5 transition-all"
             >
               {t("nav.cta")} <ArrowRight className="w-4 h-4" />
             </Link>

             {/* Mobile Toggle */}
             <button
               onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
               className="lg:hidden p-3 bg-secondary/50 rounded-xl border border-border text-foreground"
             >
               {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
             </button>
          </div>
        </div>
      </nav>

      {/* Mobile Menu Overlay */}
      <AnimatePresence>
        {isMobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="fixed inset-0 z-[90] bg-background pt-32 px-6 lg:hidden overflow-y-auto grainy-bg"
          >
            <div className="flex flex-col gap-4">
              {navLinks.map((link, idx) => (
                <motion.div
                  key={link.href}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: idx * 0.05 }}
                >
                  <Link
                    href={link.href}
                    onClick={() => setIsMobileMenuOpen(false)}
                    className={cn(
                      "flex items-center justify-between p-6 rounded-3xl transition-all",
                      pathname === link.href 
                        ? (theme === 'dark' ? "bg-white text-[#8B0000]" : "bg-[#8B0000] text-white")
                        : (theme === 'dark' ? "bg-white/5 border-white/10 text-white" : "bg-black/5 border-black/5 text-black")
                    )}
                  >
                    <div className="flex items-center gap-4">
                      <link.icon className={cn("w-6 h-6", pathname === link.href ? (theme === 'dark' ? "text-[#8B0000]" : "text-white") : (theme === 'dark' ? "text-white" : "text-[#8B0000]"))} />
                      <span className="text-xl font-black tracking-tight">{link.label}</span>
                    </div>
                    <ArrowRight className="w-5 h-5 opacity-40" />
                  </Link>
                </motion.div>
              ))}

              <div className="grid grid-cols-2 gap-4 mt-8">
                <button
                  onClick={toggleLanguage}
                  className={cn("flex flex-col items-center justify-center p-8 rounded-[32px] gap-3 border", theme === 'dark' ? "bg-white/5 border-white/10 text-white" : "bg-black/5 border-black/5 text-black")}
                >
                  <Languages className={cn("w-8 h-8", theme === 'dark' ? "text-white" : "text-[#8B0000]")} />
                  <span className="text-xs font-black uppercase tracking-widest">{language === 'id' ? 'Indonesia' : 'English'}</span>
                </button>
                <button
                  onClick={toggleTheme}
                  className={cn("flex flex-col items-center justify-center p-8 rounded-[32px] gap-3 border", theme === 'dark' ? "bg-white/5 border-white/10 text-white" : "bg-black/5 border-black/5 text-black")}
                >
                  {theme === "dark" ? <Sun className="w-8 h-8 text-white" /> : <Moon className="w-8 h-8 text-[#8B0000]" />}
                  <span className="text-xs font-black uppercase tracking-widest">{theme === 'dark' ? 'Light Mode' : 'Dark Mode'}</span>
                </button>
              </div>

              <Link
                href="/upload"
                onClick={() => setIsMobileMenuOpen(false)}
                className="mt-4 p-8 bg-foreground text-background rounded-[32px] flex flex-col items-center justify-center gap-3 shadow-2xl"
              >
                <ArrowRight className="w-8 h-8" />
                <span className="text-lg font-black uppercase tracking-widest">{t("nav.cta")}</span>
              </Link>
            </div>
            <div className="h-20" />
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

export default Navbar;
