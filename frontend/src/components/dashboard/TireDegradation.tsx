import { motion } from 'framer-motion';

export function TireDegradation() {
  const tires = [
    { type: 'SOFT (C5)', remaining: 15, color: '#ef4444' }, // red
    { type: 'MEDIUM (C4)', remaining: 48, color: '#f59e0b' }, // yellow
    { type: 'HARD (C3)', remaining: 82, color: '#374151' } // dark gray
  ];

  return (
    <div className="glass-panel p-6 flex-1 flex flex-col justify-between">
      <h3 className="font-label-lg text-label-lg text-on-background font-bold uppercase tracking-wide mb-6">TIRE LIFE REMAINING</h3>
      
      <div className="space-y-6">
        {tires.map((tire, idx) => (
          <div key={tire.type}>
            <div className="flex justify-between font-label-sm font-bold text-on-surface-variant mb-2 uppercase">
              <span>{tire.type}</span>
              <span className={tire.remaining < 20 ? "text-error" : ""}>{tire.remaining}%</span>
            </div>
            <div className="w-full bg-surface-container-high rounded-full h-3 overflow-hidden">
              <motion.div 
                initial={{ width: 0 }}
                whileInView={{ width: `${tire.remaining}%` }}
                transition={{ duration: 1, ease: 'easeOut', delay: idx * 0.2 }}
                className="h-full rounded-full" 
                style={{ backgroundColor: tire.color }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
