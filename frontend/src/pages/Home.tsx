import { motion } from 'framer-motion';
import { ArrowRight } from 'lucide-react';
import { HeroSection } from '../components/home/HeroSection';
import { DashboardSection } from '../components/home/DashboardSection';
import { Link } from 'react-router-dom';

export function Home() {
  return (
    <>
      <HeroSection />
      <DashboardSection />
      
      <section className="py-20 px-4 md:px-margin-desktop bg-background text-center border-t border-surface-container-high relative overflow-hidden">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-4xl h-[1px] bg-gradient-to-r from-transparent via-primary/50 to-transparent"></div>
        <div className="max-w-3xl mx-auto flex flex-col items-center">
          <motion.div 
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
            className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mb-6"
          >
            <div className="w-8 h-8 bg-primary rounded-full animate-pulse shadow-[0_0_15px_rgba(255,135,0,0.6)]"></div>
          </motion.div>
          <h2 className="font-['Montserrat'] text-4xl md:text-5xl text-on-background mb-6 tracking-tighter uppercase font-black italic">
            READY TO OUTSMART THE <span className="text-primary">COMPETITION?</span>
          </h2>
          <Link to="/dashboard">
            <motion.button 
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="px-10 py-5 rounded-full bg-primary text-on-primary font-headline-sm text-headline-sm uppercase tracking-wider hover:bg-primary-fixed btn-glow transition-all duration-300 flex items-center justify-center gap-3 mb-6 w-full sm:w-auto"
            >
              EXPLORE ALL PREDICTIONS
              <ArrowRight size={24} />
            </motion.button>
          </Link>
          <p className="font-body-md text-body-md text-on-surface-variant uppercase tracking-widest">
            Discover AI-driven insights and detailed outcome forecasts for every upcoming Grand Prix.
          </p>
        </div>
      </section>
    </>
  );
}
