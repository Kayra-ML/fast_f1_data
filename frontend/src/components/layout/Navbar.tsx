import { motion } from 'framer-motion';
import { Menu, ChevronDown } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';

export function Navbar() {
  const location = useLocation();

  return (
    <header className="fixed top-0 w-full z-50 flex justify-between items-center px-margin-desktop h-16 bg-background/80 backdrop-blur-xl border-b border-white/10">
      <div className="font-headline-md text-headline-md font-bold tracking-tighter text-primary uppercase">
        F1 ANALYTIX
      </div>
      
      <nav className="hidden md:flex items-center gap-8">
        <Link 
          to="/"
          className={`font-label-lg text-label-lg transition-all duration-200 pb-1 ${location.pathname === '/' ? 'text-primary border-b-2 border-primary' : 'text-on-surface hover:text-primary'}`}
        >
          HOME
        </Link>
        

        <Link 
          to="/dashboard"
          className={`font-label-lg text-label-lg transition-colors pb-1 ${location.pathname === '/dashboard' ? 'text-primary border-b-2 border-primary' : 'text-on-surface hover:text-primary'}`}
        >
          DASHBOARD
        </Link>
      </nav>
      
      <div className="hidden md:block">
        <Link to="/dashboard">
          <motion.button 
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="px-6 py-2 rounded-full bg-primary text-on-primary font-label-lg text-label-lg uppercase tracking-wide hover:bg-primary-fixed btn-glow transition-all duration-300"
          >
            LIVE PREDICTIONS
          </motion.button>
        </Link>
      </div>
      
      <button className="md:hidden text-primary">
        <Menu size={24} />
      </button>
    </header>
  );
}
