import { motion } from 'framer-motion';

export function WinProbability() {
  const drivers = [
    { name: 'Max Verstappen', team: 'Red Bull Racing', prob: 65, color: '#3671C6' },
    { name: 'Lewis Hamilton', team: 'Mercedes', prob: 28, color: '#00A19B' },
    { name: 'Lando Norris', team: 'McLaren', prob: 7, color: '#FF8000' }
  ];

  return (
    <div className="glass-panel p-6 flex-1 flex flex-col justify-between">
      <div className="flex items-center justify-between mb-6">
        <h3 className="font-label-lg text-label-lg text-on-background font-bold uppercase tracking-wide">WIN PROBABILITY</h3>
        <span className="px-2 py-1 bg-surface-container-high rounded text-label-sm text-on-surface-variant font-bold">LIVE</span>
      </div>
      
      <div className="space-y-5">
        {drivers.map((driver, idx) => (
          <div key={driver.name}>
            <div className="flex justify-between items-center mb-2">
              <div className="flex items-center gap-3">
                <span className="w-2 h-10 rounded-full" style={{ backgroundColor: driver.color }}></span>
                <div>
                  <div className="font-label-lg text-on-background font-bold">{driver.name}</div>
                  <div className="text-[11px] text-on-surface-variant uppercase tracking-wider">{driver.team}</div>
                </div>
              </div>
              <span className="font-headline-sm text-primary font-bold">{driver.prob}%</span>
            </div>
            <div className="w-full bg-surface-container-high rounded-full h-2 overflow-hidden">
              <motion.div 
                initial={{ width: 0 }}
                whileInView={{ width: `${driver.prob}%` }}
                transition={{ duration: 1, ease: 'easeOut', delay: idx * 0.2 }}
                className="h-2 rounded-full" 
                style={{ backgroundColor: driver.color }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
