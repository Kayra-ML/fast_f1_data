import { motion } from 'framer-motion';
import { Activity, Database, Gauge, BrainCircuit } from 'lucide-react';

export function DashboardSection() {
  const features = [
    {
      icon: <Database className="text-primary w-8 h-8" />,
      title: "BIG DATA INTEGRATION",
      desc: "Our engine ingests millions of data points from historical races, practice sessions, and live telemetry to build a comprehensive baseline for every track."
    },
    {
      icon: <Activity className="text-primary w-8 h-8" />,
      title: "MICRO-TELEMETRY ANALYSIS",
      desc: "We don't just look at lap times. We analyze braking points, throttle application, and cornering speeds at a micro-sector level to find true driver pace."
    },
    {
      icon: <Gauge className="text-primary w-8 h-8" />,
      title: "TIRE DEGRADATION MODELS",
      desc: "By combining track temperature, compound durability, and driver style, our algorithms simulate tire life to predict the absolute optimal pit stop windows."
    },
    {
      icon: <BrainCircuit className="text-primary w-8 h-8" />,
      title: "NEURAL NETWORK FORECASTS",
      desc: "Our machine learning models run thousands of race simulations per second, calculating dynamic win probabilities and podium chances for every driver."
    }
  ];

  return (
    <section className="py-24 px-4 md:px-margin-desktop bg-surface-container-lowest relative">
      <div className="max-w-7xl mx-auto">
        
        <div className="text-center mb-16">
          <motion.h2 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="font-['Montserrat'] text-3xl md:text-5xl font-black italic uppercase text-on-background tracking-tighter mb-4"
          >
            THE LOGIC BEHIND THE <span className="text-primary">PREDICTIONS</span>
          </motion.h2>
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="font-label-lg text-on-surface-variant uppercase tracking-widest max-w-2xl mx-auto"
          >
            We don't guess. We use advanced machine learning and raw telemetry to model race outcomes before the lights go out.
          </motion.p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {features.map((feature, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: idx * 0.1 }}
              className="glass-panel p-8 hover:border-primary transition-colors group"
            >
              <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                {feature.icon}
              </div>
              <h3 className="font-['Montserrat'] text-xl font-black italic uppercase text-on-background tracking-tight mb-3">
                {feature.title}
              </h3>
              <p className="font-body-md text-on-surface-variant leading-relaxed">
                {feature.desc}
              </p>
            </motion.div>
          ))}
        </div>

      </div>
    </section>
  );
}
