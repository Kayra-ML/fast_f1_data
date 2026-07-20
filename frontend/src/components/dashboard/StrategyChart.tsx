import { Activity } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const mockData = [
  { lap: 1, driver1: 90, driver2: 95 },
  { lap: 10, driver1: 85, driver2: 88 },
  { lap: 20, driver1: 82, driver2: 84 },
  { lap: 30, driver1: 75, driver2: 80 },
  { lap: 40, driver1: 60, driver2: 70 },
  { lap: 50, driver1: 55, driver2: 65 },
  { lap: 60, driver1: 45, driver2: 58 },
  { lap: 71, driver1: 30, driver2: 50 },
];

export function StrategyChart() {
  return (
    <div className="md:col-span-8 glass-panel rounded-xl p-6 flex flex-col">
      <div className="flex justify-between items-start mb-6">
        <div>
          <h3 className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-widest mb-1">STRAT SIM // GP24 BRAZIL</h3>
          <div className="font-headline-md text-headline-md text-on-background uppercase">RACE STRATEGY OPTIMIZATION</div>
        </div>
        <Activity className="text-primary" />
      </div>
      
      <div className="flex-1 w-full h-[300px] mt-8">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={mockData} margin={{ top: 10, right: 0, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="colorDriver1" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#ffb4a7" stopOpacity={0.8}/>
                <stop offset="95%" stopColor="#ffb4a7" stopOpacity={0}/>
              </linearGradient>
              <linearGradient id="colorDriver2" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#b6ebff" stopOpacity={0.8}/>
                <stop offset="95%" stopColor="#b6ebff" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <XAxis dataKey="lap" stroke="#9ca3af" tick={{fill: '#6b7280', fontSize: 12}} tickLine={false} axisLine={false} />
            <YAxis hide />
            <Tooltip 
              contentStyle={{ backgroundColor: '#ffffff', border: '1px solid #e5e7eb', borderRadius: '8px', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}
              itemStyle={{ color: '#111827', fontWeight: 600 }}
              labelStyle={{ color: '#6b7280', marginBottom: '4px' }}
            />
            <Area type="monotone" dataKey="driver1" stroke="#ffb4a7" strokeWidth={2} fillOpacity={1} fill="url(#colorDriver1)" className="chart-glow" />
            <Area type="monotone" dataKey="driver2" stroke="#b6ebff" strokeDasharray="3 3" strokeWidth={2} fillOpacity={1} fill="url(#colorDriver2)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
