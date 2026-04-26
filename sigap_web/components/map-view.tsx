"use client";

import { useEffect, useState } from "react";
import { MapContainer, TileLayer, CircleMarker, Popup, useMapEvents } from "react-leaflet";
import * as L from "leaflet";
import "leaflet/dist/leaflet.css";

/**
 * MASTERPIECE MAP IMPLEMENTATION
 * Refined by Professor/Senior Practitioner standards.
 */

const fixLeafletIcon = () => {
  if (typeof window === "undefined") return;
  
  // @ts-ignore
  delete L.Icon.Default.prototype._getIconUrl;
  L.Icon.Default.mergeOptions({
    iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
    iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
    shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  });
};

// Component to handle zoom events
function ZoomHandler({ setZoom }: { setZoom: (z: number) => void }) {
  useMapEvents({
    zoomend: (e) => {
      setZoom(e.target.getZoom());
    },
  });
  return null;
}

import { useLanguage } from "./language-provider";

interface MapViewProps {
  data: any;
  theme: string | undefined;
  setSelectedProv: (prov: any) => void;
}

export default function MapView({ data, theme, setSelectedProv }: MapViewProps) {
  const [zoom, setZoom] = useState(5);
  const { t, language } = useLanguage();

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
    fixLeafletIcon();
  }, []);

  const tileUrl = theme === 'dark' 
    ? "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
    : "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png";

  const mapCenter = L.latLng(-2.5489, 118.0149);

  return (
    <MapContainer 
      center={mapCenter} 
      zoom={zoom} 
      scrollWheelZoom={true}
      style={{ height: '100%', width: '100%', background: 'transparent' }}
      zoomControl={false}
    >
      <ZoomHandler setZoom={setZoom} />
      <TileLayer
        key={theme}
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
        url={tileUrl}
      />
      
      {(data?.provinsi_geo || []).map((prov: any, idx: number) => {
        if (typeof prov.lat !== 'number' || typeof prov.lng !== 'number') return null;

        const position = L.latLng(prov.lat, prov.lng);
        
        // Dynamic radius: Increases as user zooms in. 
        const baseRadius = Math.sqrt(Number(prov.count) || 0) * 4;
        const zoomFactor = Math.pow(1.5, zoom - 5);
        const calcRadius = Math.max(baseRadius * zoomFactor, 8); // Balanced radius for clickability

        return (
          <CircleMarker
            key={`${idx}-${theme}-${zoom}`}
            center={position}
            radius={calcRadius}
            pathOptions={{
              fillColor: '#8B0000',
              fillOpacity: 0.6,
              color: '#8B0000',
              weight: 2
            }}
            eventHandlers={{
              click: () => setSelectedProv(prov)
            }}
          >
            <Popup className="premium-popup">
              <div className="p-2 min-w-[200px] leading-tight">
                <h3 className="font-black text-xl mb-2 tracking-tighter text-[#8B0000] uppercase leading-none">
                  {tlr(prov.name)}
                </h3>
                <p className="text-sm font-bold text-[#8B0000]">
                  {prov.count} {t("map.popup.total")} ({((Number(prov.count) / (data?.overview?.total_laporan || 1)) * 100).toFixed(1)}%)
                </p>
              </div>
            </Popup>
          </CircleMarker>
        );
      })}
    </MapContainer>
  );
}



