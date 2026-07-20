import { motion } from 'framer-motion';
import { Rocket, Activity } from 'lucide-react';

export function HeroSection() {
  return (
    <section className="relative w-full h-[80vh] min-h-[600px] flex items-center justify-center overflow-hidden">
      <div className="absolute inset-0 w-full h-full">
        <img 
          alt="A high-fidelity hero image for an F1 analytics landing page." 
          className="w-full h-full object-cover" 
          src="/hero-bg.jpg"
        />
        {/* Sadece en alt kısımda, beyaz arka plana yumuşak geçiş için ince bir gölge */}
        <div className="absolute inset-x-0 bottom-0 h-32 bg-gradient-to-t from-background to-transparent"></div>
      </div>
      
      <div className="relative z-10 text-center px-4 md:px-margin-desktop max-w-4xl mx-auto flex flex-col items-center">
        <motion.h1 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="font-['Montserrat'] md:text-[72px] text-5xl leading-tight mb-6 tracking-tighter uppercase font-black italic"
        >
          <span className="text-white drop-shadow-md">F1 ANALYTIX</span> <br/>
          <span className="text-primary drop-shadow-md">PREDICT THE PODIUM</span>
        </motion.h1>
        
        <motion.p 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="font-body-lg text-body-lg text-on-surface-variant mb-10 max-w-2xl uppercase tracking-widest border-l-2 border-primary pl-4 text-left"
        >
          Advanced Race Analysis & AI-Powered Score Predictions.
        </motion.p>
        
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto"
        >
          <button className="px-8 py-4 rounded-full bg-primary text-on-primary font-label-lg text-label-lg uppercase tracking-wide hover:bg-primary-fixed btn-glow transition-all duration-300 flex items-center justify-center gap-2">
            VIEW RACE PREDICTIONS
            <Rocket size={18} />
          </button>
          <button className="px-8 py-4 rounded-full bg-transparent border border-on-background/20 text-on-background font-label-lg text-label-lg uppercase tracking-wide hover:border-primary hover:bg-primary/10 transition-all duration-300 backdrop-blur-sm flex items-center justify-center gap-2">
            ANALYZE PAST RACES
            <Activity size={18} />
          </button>
        </motion.div>
      </div>
    </section>
  );
}
